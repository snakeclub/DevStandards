# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os.path
import re
import sys
import tarfile

import numpy as np
from six.moves import urllib
import tensorflow as tf
import cv2
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_string('file', 'inception_v4_use.jpg', """image file path and name, """)
tf.app.flags.DEFINE_string('model_name', 'inception_v4_freeze.pb', '')
tf.app.flags.DEFINE_string('label_file', 'inception_v4_freeze.label', '')
tf.app.flags.DEFINE_integer('image_size', 299, """size of image to convert """)
tf.app.flags.DEFINE_integer('num_top_predictions', 5,
                            """Display this many predictions.""")


class EvalNode(object):

    def __init__(self, image_file, model_path, label_path,
                 image_size, num_top_predictions, output_node_name):
        self.image_file = image_file
        self.model_path = model_path
        self.label_path = label_path
        self.image_size = image_size
        self.num_top_predictions = num_top_predictions
        self.output_node_name = output_node_name
        self.node_id_to_name = None

    def load(self):
        node_id_to_name = {}
        with open(self.label_path) as f:
            for index, line in enumerate(f):
                node_id_to_name[index] = line.strip()
        self.node_id_to_name = node_id_to_name

    def id_to_string(self, node_id):
        if node_id not in self.node_id_to_name:
            return ''
        return self.node_id_to_name[node_id]


def create_graph(node_lookup):
    """Creates a graph from saved GraphDef file and returns a saver."""
    # Creates graph from saved graph_def.pb.
    with tf.gfile.FastGFile(node_lookup.model_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def preprocess_for_eval(image, height, width,
                        central_fraction=0.875, scope=None):
    with tf.name_scope(scope, 'eval_image', [image, height, width]):
        if image.dtype != tf.float32:
            image = tf.image.convert_image_dtype(image, dtype=tf.float32)
        # Crop the central region of the image with an area containing 87.5% of
        # the original image.
        if central_fraction:
            image = tf.image.central_crop(image, central_fraction=central_fraction)

        if height and width:
            # Resize the image to the specified height and width.
            image = tf.expand_dims(image, 0)
            image = tf.image.resize_bilinear(image, [height, width],
                                             align_corners=False)
            image = tf.squeeze(image, [0])
        image = tf.subtract(image, 0.5)
        image = tf.multiply(image, 2.0)
        return image


def infer(image_file, model_path, label_path,
          image_size=299, num_top_predictions=5, output_node_name='InceptionV4/Logits/Predictions:0'):
    with tf.Graph().as_default():
        image_data = tf.gfile.FastGFile(image_file, 'rb').read()
        image_data = tf.image.decode_jpeg(image_data)
        image_data = preprocess_for_eval(image_data, image_size, image_size)
        image_data = tf.expand_dims(image_data, 0)
        with tf.Session() as sess:
            image_data = sess.run(image_data)
    node_lookup = EvalNode(image_file, model_path, label_path, image_size,
                           num_top_predictions, output_node_name)
    create_graph(node_lookup)
    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name(node_lookup.output_node_name)
        predictions = sess.run(softmax_tensor, {'input:0': image_data})
        predictions = np.squeeze(predictions)
        if output_node_name == 'InceptionV4/Logits/AvgPool_1a/AvgPool:0':
            # 获取图像特征, 直接返回数组即可
            return predictions

        # 按照匹配排名
        node_lookup.load()
        top_k = predictions.argsort()[-node_lookup.num_top_predictions:][::-1]
        result = {}
        for node_id in top_k:
            human_string = node_lookup.id_to_string(node_id)
            score = predictions[node_id]
            result[human_string] = score
        return sorted(result.items(), key=lambda d: d[1], reverse=True)


if __name__ == '__main__':
    # 获取分类输出
    classfiy_result = infer(
        FLAGS.file, FLAGS.model_name, FLAGS.label_file,
        image_size=FLAGS.image_size,
        num_top_predictions=FLAGS.num_top_predictions,
        output_node_name='InceptionV4/Logits/Predictions:0'
    )

    # 获取特征变量
    vertor = infer(
        FLAGS.file, FLAGS.model_name, FLAGS.label_file,
        image_size=FLAGS.image_size,
        num_top_predictions=FLAGS.num_top_predictions,
        output_node_name='InceptionV4/Logits/AvgPool_1a/AvgPool:0'
    )
    print('图像特征向量: ', str(vertor))

    _r_list = [str(item) for item in classfiy_result]

    img = cv2.imread(FLAGS.file)  # 如想读取中文名称的图片文件可用cv2.imdecode()
    pil_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # cv2和PIL中颜色的hex码的储存顺序不同，需转RGB模式
    pilimg = Image.fromarray(pil_img)  # Image.fromarray()将数组类型转成图片格式，与np.array()相反
    draw = ImageDraw.Draw(pilimg)  # PIL图片上打印汉字
    # 参数1：字体文件路径，参数2：字体大小；Windows系统“simhei.ttf”默认存储在路径：C:\Windows\Fonts中
    font = ImageFont.truetype("simhei.ttf", 10, encoding="utf-8")
    draw.text((0, 0), '\n'.join(_r_list), (255, 0, 0), font=font)
    cv2img = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)  # 将图片转成cv2.imshow()可以显示的数组格式
    cv2.imshow(FLAGS.file, cv2img)
    cv2.waitKey()
    cv2.destroyAllWindows()
