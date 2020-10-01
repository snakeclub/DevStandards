#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
import cv2
import numpy as np
import tensorflow as tf
from PIL import Image, ImageDraw, ImageFont, ImageColor
# import matplotlib
# matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
# 将 object_detection 的安装路径导入
sys.path.append(r'D:\tensorflow\models\research\object_detection')
import object_detection.utils.label_map_util as label_map_util
import object_detection.utils.ops as utils_ops
# import object_detection.utils.visualization_utils as vis_util


# 指定冻结模型文件
PATH_TO_CKPT = r'D:\ccproject\mask_rcnn_resnet101\frozen_inference_graph.pb'

# 指定labelmap.pbtxt文件
PATH_TO_LABELS = os.path.join(
    r'D:\ccproject\mask_rcnn_resnet101', 'labelmap.pbtxt')

# 修改分类数量
NUM_CLASSES = 1

COLOR_MAP = {
    # X11 colour table from https://drafts.csswg.org/css-color-4/, with
    # gray/grey spelling issues fixed.  This is a superset of HTML 4.0
    # colour names used in CSS 1.
    "aliceblue": "#f0f8ff",
    "antiquewhite": "#faebd7",
    "aqua": "#00ffff",
    "aquamarine": "#7fffd4",
    "azure": "#f0ffff",
    "beige": "#f5f5dc",
    "bisque": "#ffe4c4",
    "black": "#000000",
    "blanchedalmond": "#ffebcd",
    "blue": "#0000ff",
    "blueviolet": "#8a2be2",
    "brown": "#a52a2a",
    "burlywood": "#deb887",
    "cadetblue": "#5f9ea0",
    "chartreuse": "#7fff00",
    "chocolate": "#d2691e",
    "coral": "#ff7f50",
    "cornflowerblue": "#6495ed",
    "cornsilk": "#fff8dc",
    "crimson": "#dc143c",
    "cyan": "#00ffff",
    "darkblue": "#00008b",
    "darkcyan": "#008b8b",
    "darkgoldenrod": "#b8860b",
    "darkgray": "#a9a9a9",
    "darkgrey": "#a9a9a9",
    "darkgreen": "#006400",
    "darkkhaki": "#bdb76b",
    "darkmagenta": "#8b008b",
    "darkolivegreen": "#556b2f",
    "darkorange": "#ff8c00",
    "darkorchid": "#9932cc",
    "darkred": "#8b0000",
    "darksalmon": "#e9967a",
    "darkseagreen": "#8fbc8f",
    "darkslateblue": "#483d8b",
    "darkslategray": "#2f4f4f",
    "darkslategrey": "#2f4f4f",
    "darkturquoise": "#00ced1",
    "darkviolet": "#9400d3",
    "deeppink": "#ff1493",
    "deepskyblue": "#00bfff",
    "dimgray": "#696969",
    "dimgrey": "#696969",
    "dodgerblue": "#1e90ff",
    "firebrick": "#b22222",
    "floralwhite": "#fffaf0",
    "forestgreen": "#228b22",
    "fuchsia": "#ff00ff",
    "gainsboro": "#dcdcdc",
    "ghostwhite": "#f8f8ff",
    "gold": "#ffd700",
    "goldenrod": "#daa520",
    "gray": "#808080",
    "grey": "#808080",
    "green": "#008000",
    "greenyellow": "#adff2f",
    "honeydew": "#f0fff0",
    "hotpink": "#ff69b4",
    "indianred": "#cd5c5c",
    "indigo": "#4b0082",
    "ivory": "#fffff0",
    "khaki": "#f0e68c",
    "lavender": "#e6e6fa",
    "lavenderblush": "#fff0f5",
    "lawngreen": "#7cfc00",
    "lemonchiffon": "#fffacd",
    "lightblue": "#add8e6",
    "lightcoral": "#f08080",
    "lightcyan": "#e0ffff",
    "lightgoldenrodyellow": "#fafad2",
    "lightgreen": "#90ee90",
    "lightgray": "#d3d3d3",
    "lightgrey": "#d3d3d3",
    "lightpink": "#ffb6c1",
    "lightsalmon": "#ffa07a",
    "lightseagreen": "#20b2aa",
    "lightskyblue": "#87cefa",
    "lightslategray": "#778899",
    "lightslategrey": "#778899",
    "lightsteelblue": "#b0c4de",
    "lightyellow": "#ffffe0",
    "lime": "#00ff00",
    "limegreen": "#32cd32",
    "linen": "#faf0e6",
    "magenta": "#ff00ff",
    "maroon": "#800000",
    "mediumaquamarine": "#66cdaa",
    "mediumblue": "#0000cd",
    "mediumorchid": "#ba55d3",
    "mediumpurple": "#9370db",
    "mediumseagreen": "#3cb371",
    "mediumslateblue": "#7b68ee",
    "mediumspringgreen": "#00fa9a",
    "mediumturquoise": "#48d1cc",
    "mediumvioletred": "#c71585",
    "midnightblue": "#191970",
    "mintcream": "#f5fffa",
    "mistyrose": "#ffe4e1",
    "moccasin": "#ffe4b5",
    "navajowhite": "#ffdead",
    "navy": "#000080",
    "oldlace": "#fdf5e6",
    "olive": "#808000",
    "olivedrab": "#6b8e23",
    "orange": "#ffa500",
    "orangered": "#ff4500",
    "orchid": "#da70d6",
    "palegoldenrod": "#eee8aa",
    "palegreen": "#98fb98",
    "paleturquoise": "#afeeee",
    "palevioletred": "#db7093",
    "papayawhip": "#ffefd5",
    "peachpuff": "#ffdab9",
    "peru": "#cd853f",
    "pink": "#ffc0cb",
    "plum": "#dda0dd",
    "powderblue": "#b0e0e6",
    "purple": "#800080",
    "rebeccapurple": "#663399",
    "red": "#ff0000",
    "rosybrown": "#bc8f8f",
    "royalblue": "#4169e1",
    "saddlebrown": "#8b4513",
    "salmon": "#fa8072",
    "sandybrown": "#f4a460",
    "seagreen": "#2e8b57",
    "seashell": "#fff5ee",
    "sienna": "#a0522d",
    "silver": "#c0c0c0",
    "skyblue": "#87ceeb",
    "slateblue": "#6a5acd",
    "slategray": "#708090",
    "slategrey": "#708090",
    "snow": "#fffafa",
    "springgreen": "#00ff7f",
    "steelblue": "#4682b4",
    "tan": "#d2b48c",
    "teal": "#008080",
    "thistle": "#d8bfd8",
    "tomato": "#ff6347",
    "turquoise": "#40e0d0",
    "violet": "#ee82ee",
    "wheat": "#f5deb3",
    "white": "#ffffff",
    "whitesmoke": "#f5f5f5",
    "yellow": "#ffff00",
    "yellowgreen": "#9acd32",
}

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')


label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(
    label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


def load_image_into_numpy_array(image):
    """
    将图片转换为numpy数组
    """
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)


def run_inference_for_single_image(image, graph):
    with graph.as_default():
        with tf.Session() as sess:
            # Get handles to input and output tensors
            ops = tf.get_default_graph().get_operations()
            all_tensor_names = {output.name for op in ops for output in op.outputs}
            tensor_dict = {}
            for key in ['num_detections', 'detection_boxes', 'detection_scores', 'detection_classes', 'detection_masks']:
                tensor_name = key + ':0'
                if tensor_name in all_tensor_names:
                    tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(tensor_name)

            if 'detection_masks' in tensor_dict:
                # The following processing is only for single image
                detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
                detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
                # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
                real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
                detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
                detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
                # detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                #     detection_masks, detection_boxes, image.shape[0], image.shape[1])
                detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                    detection_masks, detection_boxes, image.size[1], image.size[0])
                detection_masks_reframed = tf.cast(
                    tf.greater(detection_masks_reframed, 0.5), tf.uint8)
                # Follow the convention by adding back the batch dimension
                tensor_dict['detection_masks'] = tf.expand_dims(
                    detection_masks_reframed, 0)
            image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

            # Run inference
            output_dict = sess.run(tensor_dict,
                                   feed_dict={image_tensor: np.expand_dims(image, 0)})

            # all outputs are float32 numpy arrays, so convert types as appropriate
            output_dict['num_detections'] = int(output_dict['num_detections'][0])
            output_dict['detection_classes'] = output_dict[
                'detection_classes'][0].astype(np.uint8)
            output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
            output_dict['detection_scores'] = output_dict['detection_scores'][0]
            if 'detection_masks' in output_dict:
                output_dict['detection_masks'] = output_dict['detection_masks'][0]
        return output_dict


# 指定要检测的图片
_image_path = r"D:\ccproject\mask_rcnn_resnet101\train_set\bangle_flat\0000000094.jpg"
# image = cv2.imread(_image_path)
# # image = cv2.imread("D:/tensorflow/models/research/object_detection/test_images/image2.jpg");
# cv2.imshow("input image", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# 显示图片匹配结果
_image = Image.open(_image_path).convert('RGB')

# Actual detection.
_output = run_inference_for_single_image(_image, detection_graph)


# 遍历在图片上增加对应的显示
_colors = ['red', 'green', 'blue', 'purple', 'skyblue', 'yellow']
# 可修改的识别和显示参数
_font = ImageFont.truetype("simhei.ttf", 20, encoding="utf-8")  # 显示字体
_min_score = 0.9  # 要显示的最低匹配百分比分数
_line_width = 3  # 物体框线大小
_alpha = 0.4  # Mask透明度
for _index in range(_output['num_detections']):
    if _output['detection_scores'][_index] < _min_score:
        # 匹配度低的不显示
        break

    # 颜色
    _color = _colors[(_output['detection_classes'][_index] - 1) % len(_colors)]

    # 添加遮罩
    _mask = _output['detection_masks'][_index]
    _rgb = ImageColor.getrgb(_color)
    _image_array = load_image_into_numpy_array(_image)

    _solid_color = np.expand_dims(
        np.ones_like(_mask), axis=2) * np.reshape(list(_rgb), [1, 1, 3])
    _pil_solid_color = Image.fromarray(np.uint8(_solid_color)).convert('RGBA')
    _pil_mask = Image.fromarray(np.uint8(255.0 * _alpha * _mask)).convert('L')
    _image = Image.composite(_pil_solid_color, _image, _pil_mask)
    np.copyto(_image_array, np.array(_image.convert('RGB')))
    _image = Image.fromarray(_image_array)

    # 画框图
    _draw = ImageDraw.Draw(_image)
    _class_name = category_index[_output['detection_classes'][_index]]['name']
    _box = tuple(_output['detection_boxes'][_index].tolist())
    _ymin, _xmin, _ymax, _xmax = _box
    _xmin = round(_xmin * _image.size[0])
    _xmax = round(_xmax * _image.size[0])
    _ymin = round(_ymin * _image.size[1])
    _ymax = round(_ymax * _image.size[1])
    _draw.rectangle(((_xmin, _ymin), (_xmax, _ymax)), outline=_color, width=_line_width)

    # 添加文字
    _draw.text(
        (_xmin + _line_width + 5, _ymin + _line_width + 5),
        '%s: %.2f%%' % (_class_name, _output['detection_scores'][_index] * 100.0),
        _color, font=_font
    )


plt.figure(_image_path)
plt.imshow(_image)
plt.show()


# Visualization of the results of a detection.
# vis_util.visualize_boxes_and_labels_on_image_array(
#     image,
#     _output['detection_boxes'],
#     _output['detection_classes'],
#     _output['detection_scores'],
#     category_index,
#     # instance_masks=_output.get('detection_masks'),
#     use_normalized_coordinates=True,
#     min_score_thresh=0.9,
#     line_thickness=8)
