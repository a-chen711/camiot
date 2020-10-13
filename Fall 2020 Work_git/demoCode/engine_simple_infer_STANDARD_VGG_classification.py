import torch
import cv2
import numpy as np
from cv2 import Canny
from skimage.measure import label

CLASS_MAP = {
    0: 'coffeemaker',
    1: 'lamp',
    2: 'printer',
    3: 'toaster',
    4: 'tv',
}

INTERP_CODES = {
    'nearest': cv2.INTER_NEAREST,
    'bilinear': cv2.INTER_LINEAR,
    'bicubic': cv2.INTER_CUBIC,
    'area': cv2.INTER_AREA,
    'lanczos': cv2.INTER_LANCZOS4
}

NO_FIGURE_PIXEL_NUM_THRESHOLD = 200
IMG_SCALES = (256, 256)
NORM_CONFIG = {'mean': [123.675, 116.28, 103.53], 'std': [128.0, 128.0, 128.0], 'to_rgb': True}
NUM_CLASS = 5
# checkpoints
CHECKPOINT_FILE = '/Users/ApplePro/Desktop/School/GradSchool/Research /HCI/camiot/Feb 15/demoCode/epoch_300.pth'


import torch.nn as nn
import torch.nn.functional as F


def _conv3x3(in_planes, out_planes, dilation):
    "3x3 convolution with padding"
    return nn.Conv2d(
        in_planes,
        out_planes,
        kernel_size=3,
        padding=dilation,
        dilation=dilation
    )


def _make_vgg_layer(
        in_planes,
        out_planes,
        num_blocks,
        dilation,
        with_bn,
        ceil_mode,
        use_dropout,
        dropout_rate,
):
    layers = []
    for _ in range(num_blocks):
        layers.append(_conv3x3(in_planes, out_planes, dilation))
        if with_bn:
            layers.append(nn.BatchNorm2d(out_planes))
        layers.append(nn.ReLU(inplace=True))
        if use_dropout:
            layers.append(nn.Dropout(p=dropout_rate, inplace=False))
        in_planes = out_planes
    layers.append(nn.MaxPool2d(kernel_size=2, stride=2, ceil_mode=ceil_mode))

    return layers


class VGG(nn.Module):
    """VGG backbone.

    ~134,000,000 params

    (features): Sequential(
      (0): Conv2d(3, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (1): ReLU(inplace=True)
      (2): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (3): ReLU(inplace=True)
      (4): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=True)
      (5): Conv2d(64, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (6): ReLU(inplace=True)
      (7): Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (8): ReLU(inplace=True)
      (9): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=True)
      (10): Conv2d(128, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (11): ReLU(inplace=True)
      (12): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (13): ReLU(inplace=True)
      (14): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (15): ReLU(inplace=True)
      (16): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=True)
      (17): Conv2d(256, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (18): ReLU(inplace=True)
      (19): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (20): ReLU(inplace=True)
      (21): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (22): ReLU(inplace=True)
      (23): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=True)
      (24): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (25): ReLU(inplace=True)
      (26): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (27): ReLU(inplace=True)
      (28): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (29): ReLU(inplace=True)
    )

    Args:
        with_bn (bool): Use BatchNorm or not.
        num_classes (int): number of classes for classification. -1 for non FC layers.
        num_stages (int): VGG stages, normally 5.
        dilations (Sequence[int]): Dilation of each stage. (1, 1, 1, 1, 1) for no dilation.
        out_indices (Sequence[int]): Output from which stages. (0, 1, 2, 3, 4) for every stage.
        frozen_stages (int): Stages to be frozen (all param fixed). -1 for
            not freezing any parameters.
        bn_eval (bool): Whether to set BN layers as eval mode, namely, freeze
            running stats (mean and var).
        bn_frozen (bool): Whether to freeze weight and bias of BN layers.
        ceil_mode (bool): how to resolve downsampling %2 issue.
        with_last_pool (bool): whether to pool the last conv layer.
    """

    arch_settings = [2, 2, 3, 3, 3]
    plane_settings = [64, 128, 256, 512, 512]

    def __init__(
            self,
            with_bn,
            num_classes,
            num_stages,
            dilations,
            out_indices,
            frozen_stages,
            bn_eval,
            bn_frozen,
            ceil_mode,
            with_last_pool,
            use_dropout,
            dropout_rate,
    ):
        super(VGG, self).__init__()

        assert len(dilations) == num_stages

        self.num_classes = num_classes
        self.out_indices = out_indices
        self.frozen_stages = frozen_stages
        self.bn_eval = bn_eval
        self.bn_frozen = bn_frozen
        self.in_planes = 3
        self.range_sub_modules = []
        self.use_dropout = use_dropout
        self.dropout_rate = dropout_rate

        start_idx = 0
        vgg_layers = []
        for i, num_blocks in enumerate(self.arch_settings):
            num_modules = num_blocks * (2 + with_bn) + 1
            end_idx = start_idx + num_modules
            dilation = dilations[i]
            out_planes = self.plane_settings[i]
            vgg_layer = _make_vgg_layer(
                in_planes=self.in_planes,
                out_planes=out_planes,
                num_blocks=num_blocks,
                dilation=dilation,
                with_bn=with_bn,
                ceil_mode=ceil_mode,
                use_dropout=self.use_dropout,
                dropout_rate=self.dropout_rate,
            )
            vgg_layers.extend(vgg_layer)
            self.in_planes = out_planes
            self.range_sub_modules.append([start_idx, end_idx])
            start_idx = end_idx

        if not with_last_pool:
            vgg_layers.pop(-1)
        vgg_layers.append(nn.AdaptiveAvgPool2d((1, 1)))
        self.add_module('features', nn.Sequential(*vgg_layers))

        if self.num_classes > 0:
            self.add_module('classifier', nn.Sequential(nn.Linear(512, num_classes)))

    def forward(self, x):
        for i, layer in enumerate(self.features):
            x = layer(x)
        if self.num_classes > 0:
            x = x.view(x.size(0), -1)
            x = self.classifier(x)
        x = F.softmax(x).cpu().numpy()
        return x


def cut_query_img_with_finger(img):
    imageYCrCb = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2YCR_CB)
    # skin detection
    min_YCrCb = np.array([0, 133, 77], np.uint8)
    max_YCrCb = np.array([255, 173, 127], np.uint8)
    skinRegionYCrCb = cv2.inRange(imageYCrCb, min_YCrCb, max_YCrCb)
    # preprocessing
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    skinRegionYCrCb = cv2.erode(skinRegionYCrCb, kernel, iterations=2)
    skinRegionYCrCb = cv2.dilate(skinRegionYCrCb, kernel, iterations=2)
    skinRegionYCrCb = cv2.GaussianBlur(skinRegionYCrCb, (3, 3), 0)

    image_canny_filter = Canny(image=img.astype('uint8'), threshold1=20, threshold2=40)
    image_canny_filter = (image_canny_filter < 100).astype(np.int32)
    # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}_canny_as_filter.jpg'.format(item.split('.')[0], 'skin')), image_canny_filter*255)
    image_canny_filter_left = np.roll(image_canny_filter, 1, axis=0)
    image_canny_filter_right = np.roll(image_canny_filter, -1, axis=0)
    image_canny_filter_up = np.roll(image_canny_filter, 1, axis=1)
    image_canny_filter_down = np.roll(image_canny_filter, -1, axis=1)
    # image_sobel = image_sobel * image_canny_filter * image_canny_filter_left * image_canny_filter_right * image_canny_filter_up * image_canny_filter_down
    image_sobel = skinRegionYCrCb * image_canny_filter * image_canny_filter_left * image_canny_filter_right * image_canny_filter_up * image_canny_filter_down
    # largest island
    image_sobel = label(image_sobel)
    image_sobel = image_sobel == np.argmax(np.bincount(image_sobel.flat)[1:]) + 1

    # postprocessing
    image_sobel = image_sobel.astype(np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
    image_sobel = cv2.dilate(image_sobel, kernel, iterations=2)
    image_sobel = cv2.GaussianBlur(image_sobel, (3, 3), 0)
    image_sobel = image_sobel.astype(np.int32)
    if np.count_nonzero(image_sobel) <= NO_FIGURE_PIXEL_NUM_THRESHOLD:
        return img
    else:
        points_x, points_y = np.where(image_sobel == 1)
        top_line_index = np.min(points_x)
        bot_line_index = np.max(points_x)
        if bot_line_index <= 0.95 * img.shape[0]:
            return img
        else:
            mid_y = np.mean(points_y)
            left_y = max(0, int(mid_y - 0.3 * img.shape[1]))
            right_y = min(img.shape[1], int(mid_y + 0.3 * img.shape[1]))
            if top_line_index - int(0.65 * img.shape[0]) >= 0:
                upper_line = top_line_index - int(0.65 * img.shape[0])
            else:
                upper_line = 0
            return img[upper_line:top_line_index, left_y:right_y, :]


def _scale_size(size, scale):
    """Rescale a size by a ratio.

    Args:
        size (tuple): w, h.
        scale (float): Scaling factor.

    Returns:
        tuple[int]: scaled size.
    """
    w, h = size
    return int(w * float(scale) + 0.5), int(h * float(scale) + 0.5)


def _imresize(img, size, return_scale=False, interpolation='bilinear'):
    """Resize image to a given size.

    Args:
        img (ndarray): The input image.
        size (tuple): Target (w, h).
        return_scale (bool): Whether to return `w_scale` and `h_scale`.
        interpolation (str): Interpolation method, accepted values are
            "nearest", "bilinear", "bicubic", "area", "lanczos".

    Returns:
        tuple or ndarray: (`resized_img`, `w_scale`, `h_scale`) or
            `resized_img`.
    """
    h, w = img.shape[:2]
    resized_img = cv2.resize(
        img, size, interpolation=INTERP_CODES[interpolation])
    if not return_scale:
        return resized_img
    else:
        w_scale = size[0] / w
        h_scale = size[1] / h
        return resized_img, w_scale, h_scale


def _impad(img, shape, pad_val=0):
    """Pad an image to a certain shape.

    Args:
        img (ndarray): Image to be padded.
        shape (tuple): Expected padding shape.
        pad_val (number or sequence): Values to be filled in padding areas.

    Returns:
        ndarray: The padded image.
    """
    if not isinstance(pad_val, (int, float)):
        assert len(pad_val) == img.shape[-1]
    if len(shape) < len(img.shape):
        shape = shape + (img.shape[-1], )
    assert len(shape) == len(img.shape)
    for i in range(len(shape) - 1):
        assert shape[i] >= img.shape[i]
    pad = np.empty(shape, dtype=img.dtype)
    pad[...] = pad_val
    pad[:img.shape[0], :img.shape[1], ...] = img
    return pad


def imrescale(img, scale, return_scale=False, interpolation='bilinear'):
    """Resize image while keeping the aspect ratio. H and W will be fixed.

    Args:
        img (ndarray): The input image.
        scale (float or tuple[int]): The scaling factor or maximum size.
            If it is a float number, then the image will be rescaled by this
            factor.
            If it is a tuple, its should be (width, height). Then the image will
            be rescaled as large as possible within the scale.
        return_scale (bool): Whether to return the scaling factor besides the
            rescaled image.
        interpolation (str): Same as :func:`resize`.

    Returns:
        ndarray: The rescaled image.
    """
    h, w = img.shape[:2]
    if isinstance(scale, (float, int)):
        if scale <= 0:
            raise ValueError(
                'Invalid scale {}, must be positive.'.format(scale))
        scale_factor = scale
    elif isinstance(scale, tuple):
        # scale = (width, height)
        scale_factor = min(scale[1] / h, scale[0] / w)
    else:
        raise TypeError(
            'Scale must be a number or tuple of int, but got {}'.format(type(scale)))

    new_size = _scale_size((w, h), scale_factor)
    rescaled_img = _imresize(img, new_size, interpolation=interpolation)
    if return_scale:
        return rescaled_img, scale_factor
    else:
        return rescaled_img


def imnormalize(img, mean, std, to_rgb=True):
    img = img.astype(np.float32)
    if to_rgb:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return (img - mean) / std

def appliance_recognition(img_path):
    # load image
    img = cv2.imread(img_path, cv2.IMREAD_COLOR).astype(np.float32)
    img = cut_query_img_with_finger(img)
    img, scale_factor = imrescale(
        img=img,
        scale=IMG_SCALES,
        return_scale=True,
        interpolation='bilinear',
    )
    img = _impad(img=img, shape=(IMG_SCALES[1], IMG_SCALES[0]), pad_val=(0, 0, 0))
    img = imnormalize(img, NORM_CONFIG['mean'], NORM_CONFIG['std'], NORM_CONFIG['to_rgb']).astype(
        np.float32)
    img = torch.from_numpy(np.expand_dims(img.transpose(2, 0, 1), 0)).cpu()

    # model build
    model = VGG(
        with_bn=False,
        num_classes=NUM_CLASS,
        num_stages=5,
        dilations=(1, 1, 1, 1, 1),
        out_indices=[],
        frozen_stages=-1,
        bn_eval=True,
        bn_frozen=False,
        ceil_mode=True,
        with_last_pool=True,
        use_dropout=False,
        dropout_rate=None,
    ).to('cpu')
    if hasattr(model, 'module'):
        model = model.module

    # load checkpoint
    checkpoint = torch.load(CHECKPOINT_FILE, map_location='cpu')
    # optimizer.state_dict -> state, param_groups
    # state -> var series number -> step / exp_avg / exp_avg_sq
    # param_groups -> lr / betas / eps / weight_decay / amsgrad / params
    model.load_state_dict(checkpoint['state_dict'], strict=True)
    # enable dropout during inference
    model.eval()

    # model run
    with torch.no_grad():
        result_prob = model(
            x=img,
        )
    # [0.22918019 0.1116754  0.08907871 0.49464667 0.07541901]
    result_prob = np.squeeze(result_prob, 0)
    # [3 0 1 2 4]
    result_index = result_prob.argsort()[::-1]
    # ['toaster', 'coffeemaker', 'lamp', 'printer', 'tv']
    result_items = [CLASS_MAP[index] for index in result_index]
    result_prob = np.sort(result_prob)[::-1]

    return result_prob, result_items
#
#
# def main():
#     result_prob, result_items = appliance_recognition('/yuanProject/CAMIOT/query_image_v2/coffeemaker/CF_5.png')
#     print(result_prob)
#     print(result_items)
#
#
# if __name__ == '__main__':
#     main()




