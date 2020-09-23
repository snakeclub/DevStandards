# TensorFlow-Slim图像分类训练及应用

​	TensorFlow Slim 是Google 公司公布的一个图像分类工具包，它不仅定义了一些方便的接口，还提供了很多ImageNet 数据集上常用的网络结构和预训练模型。slim作为一种轻量级的tensorflow库，使得模型的构建，训练，测试都变得更加简单。
​     截至2017 年7 月， Slim 提供包括VGG16 、VGG19 、Inception Vl ~ V4, ResNet50 、ResNet101, MobileNet 在内大多数常用模型的结构以及预训练模型，更多的模型还会被持续添加进来。



# TF-Slim安装

slim是TensorFlow的一个子库（package），只要安装了TensorFlow，TF-Slim也对应完成了安装，TensorFlow的安装方法可以参考《TensorFlow安装部署及简单应用-Python.md》。

TensorFlow 安装后，可以通过以下命令测试 TF-Slim 是否安装成功：

```javascript
python -c "import tensorflow.contrib.slim as slim; eval = slim.evaluation.evaluate_once"
```



我们可以直接使用TF-Slim开源的预定义模型进行图像分类训练和应用，需要安装 TF-Slim 图像模型库 . 步骤如下：

1、在github上下载slim模型：[tensorflow/models/research/slim](https://github.com/tensorflow/models/tree/master/research/slim)

注：本示例安装的tensorflow版本为1.15， 对应要下载 https://github.com/tensorflow/models/releases 中的v1.13.0版本发布包，下载地址：https://github.com/tensorflow/models/archive/v1.13.0.zip

其主要文件夹和文件用途如下表所示：

| 文件夹或文件名               | 用途                                                         |
| ---------------------------- | ------------------------------------------------------------ |
| datasets                     | 定义一些数据集，默认预定义好了4个数据集，分别为MNIST，CIFAR-10，Flowers，ImageNet。如果需要训练自己的数据，则必须在该文件夹下定义，模仿其他数据集的定义即可 |
| nets                         | 定义一些常用网络结构，如AlexNet、VGG16、VGG19、ResNet、Inception等 |
| scripts                      | 一些训练示例脚本，只能在支持shell的系统下使用                |
| preprocessing                | 在模型读取图片之前，先进行图像的预处理和数据增强，这个文件夹下针对不同的网络，分别定义了其预处理方法 |
| download_and_convert_data.py | 下载并转换数据集格式的入口代码                               |
| train_image_classifier.py    | 训练模型的入口代码                                           |
| eval_image_classifier.py     | 验证模型性能的入口代码                                       |



2、将下载好的模型 **research/slim** 的路径添加到python path里:

Windows：

在操作系统上设置 “PYTHONPATH” 的值，增加以下路径: “D:\tensorflow\models;D:\tensorflow\models\research;D:\tensorflow\models\research\slim”。

如Windows的设置方式为 右击“我的电脑–>属性–>高级系统设置–>环境变量–>新建系统变量”。

Ubuntu:

```
vi ~/.bashrc

在文件结尾增加：
export PYTHONPATH="/home/ubuntu18/models-1.13.0:/home/ubuntu18/models-1.13.0/research:/home/ubuntu18/models-1.13.0/research/slim:$PYTHONPATH"

保存后在终端输入 $ source ~/.bashrc 使环境变量立即生效
```



# 准备训练数据集

## 下载数据集

可以下载或准备自己的训练数据集，实例中使用的是flowers样例数据集，可以通过以下方法直接下载并转换为TFRecord格式：

```
$ DATA_DIR=/home/ubuntu18/tensorflow-test/flowers/data
$ python download_and_convert_data.py \
    --dataset_name=flowers \
    --dataset_dir="${DATA_DIR}"
```



如果因为墙的原因没有办法下载，也可以自行下载数据集，并手工进行TFRecord格式的转换，可以使用以下两个地址进行下载：

下载地址：http://download.tensorflow.org/example_images/flower_photos.tgz

百度网盘：https://pan.baidu.com/s/1mupkKKK0CqqlOZ3cbxvJKQ  提取码：a5z4

1、下载后，解压到 DATA_DIR 目录, 解压后数据集的目录为：/home/ubuntu18/tensorflow-test/flowers/data/flower_photos/

```
$ cd /home/ubuntu18/tensorflow-test/flowers
$ mkdir data
$ tar zxvf flower_photos.tgz -C data/
```

2、修改 **research/slim/datasets/** 目录下的 download_and_convert_flowers.py 文件，屏蔽掉下载解压部分代码：

```
# dataset_utils.download_and_uncompress_tarball(_DATA_URL, dataset_dir)
```

3、执行命令生成TFRecord格式文件，最后删除压缩文件会报错（因为要保留文件，所以没有放到该目录进行解压），无需理会，最后生成对应的文件清单：

```
$ cd /home/ubuntu18/models-1.13.0/research/slim
$ DATA_DIR=/home/ubuntu18/tensorflow-test/flowers/data
$ python download_and_convert_data.py \
    --dataset_name=flowers \
    --dataset_dir="${DATA_DIR}"

$ cd /home/ubuntu18/tensorflow-test/flowers/data
$ ls
flower_photos                          flowers_train_00002-of-00005.tfrecord  flowers_validation_00000-of-00005.tfrecord  flowers_validation_00003-of-00005.tfrecord
flowers_train_00000-of-00005.tfrecord  flowers_train_00003-of-00005.tfrecord  flowers_validation_00001-of-00005.tfrecord  flowers_validation_00004-of-00005.tfrecord
flowers_train_00001-of-00005.tfrecord  flowers_train_00004-of-00005.tfrecord  flowers_validation_00002-of-00005.tfrecord  labels.txt
```



## 创建自己的数据集

如果打算做自己的数据集，可以参考flower_photos的目录结构（根目录下，每个子文件夹是一类图片，子文件夹名称为分类名称），可以按以下步骤处理（以水果分类fruit为例）:

1、准备水果的分类图片，放置目录如下：

```
fruit_photos
  |__apple
  |    |__0001.jpg
  |    |__0002.jpg
  |    |__ ...
  |__banana
  |    |__ ...
  |__ ...
```

2、复制 research/slim/datasets/download_and_convert_flowers.py 文件，修改文件名为convert_fruit.py，修改以下几个点：

全局配置：

```
# The number of images in the validation set.
# 修改实际数据集中需要预留的验证图片数量（比如拿其中5%的训练图片进行验证）
_NUM_VALIDATION = 350

# Seed for repeatability.
# 随机种子
_RANDOM_SEED = 0

# The number of shards per dataset split.
# 修改数据集需要分成的文件数量
_NUM_SHARDS = 5
```

获取文件名集分类的函数： def _get_filenames_and_classes(dataset_dir):

```
# 最简单的方法是只修改该行，获取根目录
flower_root = os.path.join(dataset_dir, 'fruit_photos')
```

获取数据集文件名：def _get_dataset_filename(dataset_dir, split_name, shard_id):

```
# 该行将flowers修改为fruits
output_filename = 'fruits_%s_%05d-of-%05d.tfrecord' % (
      split_name, shard_id, _NUM_SHARDS)
```

执行函数：def run(dataset_dir):

```
...
# 屏蔽该行下载的动作
# dataset_utils.download_and_uncompress_tarball(_DATA_URL, dataset_dir)
...
# 屏蔽该行，不删除原文件，以及提示信息调整为fruits
# _clean_up_temporary_files(dataset_dir)
print('\nFinished converting the fruits dataset!')
```

3、修改 research/slim/download_and_convert_data.py ，修改以下几个点：

```
...
from datasets import download_and_convert_cifar10
from datasets import download_and_convert_flowers
from datasets import download_and_convert_mnist
# 增加自定义数据集的处理
from datasets import convert_fruit
...
if FLAGS.dataset_name == 'cifar10':
    download_and_convert_cifar10.run(FLAGS.dataset_dir)
  elif FLAGS.dataset_name == 'flowers':
    download_and_convert_flowers.run(FLAGS.dataset_dir)
  elif FLAGS.dataset_name == 'mnist':
    download_and_convert_mnist.run(FLAGS.dataset_dir)
  elif FLAGS.dataset_name == 'fruits':
    # 增加水果的数据集处理
    convert_fruit.run(FLAGS.dataset_dir)
  else:
    raise ValueError(
        'dataset_name [%s] was not recognized.' % FLAGS.dataset_name)
```

4、执行转换处理（flowers目录可忽略，只是作者将数据集放到这个测试目录下，可自行调整目录）

```
$ DATA_DIR=/home/ubuntu18/tensorflow-test/flowers/data
$ python download_and_convert_data.py \
    --dataset_name=fruits \
    --dataset_dir="${DATA_DIR}"
```

5、复制 research/slim/datasets/flowers.py 文件，修改文件名为 fruits.py，并修改以下代码：

```
# 修改以下文件分隔的正则参数, flowers 修改为 fruits
_FILE_PATTERN = 'fruits_%s_*.tfrecord'

# 修改训练集和验证集的图片数量
SPLITS_TO_SIZES = {'train': 3320, 'validation': 350}

# 修改图片分类数量（子目录数量）
_NUM_CLASSES = 5
```

6、修改 research/slim/datasets/dataset_factory.py，

```
...
from datasets import cifar10
from datasets import flowers
from datasets import imagenet
from datasets import mnist
# 新增数据集处理库
from datasets import fruits

# 数据集映射增加fruits
datasets_map = {
    'cifar10': cifar10,
    'flowers': flowers,
    'imagenet': imagenet,
    'mnist': mnist,
    'fruits': fruits,
}
...
```

**注：第5、6点实际上不影响转换TFRecord文件，只是后续进行训练签需要进行相应的修改。**



## 验证TFRecord是否正确

我们可以用官方给的例子创建Dataset Descriptor，并验证我们制作的TFRecord是否正确。

在 /home/ubuntu18/models-1.13.0/research/slim/datasets 目录下创建 flower_descriptor.py 文件，代码如下：

```
import tensorflow as tf
from datasets import flowers
import pylab
 
slim = tf.contrib.slim
 
DATA_DIR= "/home/ubuntu18/tensorflow-test/flowers/data"
 
# Selects the 'validation' dataset.
dataset = flowers.get_split('validation', DATA_DIR)
 
# Creates a TF-Slim DataProvider which reads the dataset in the background
# during both training and testing.
provider = slim.dataset_data_provider.DatasetDataProvider(dataset)
[image, label] = provider.get(['image', 'label'])
 
#在session下读取数据，并用pylab显示图片
with tf.Session() as sess:
    #初始化变量
    sess.run(tf.global_variables_initializer())
    #启动队列
    tf.train.start_queue_runners()
    image_batch,label_batch = sess.run([image, label])
    #显示图片
    pylab.imshow(image_batch)
    pylab.show()
```

执行该py文件，如果文件格式正确，可以看到以下图片：

<img src="TensorFlow-Slim%E5%9B%BE%E5%83%8F%E5%88%86%E7%B1%BB%E8%AE%AD%E7%BB%83%E5%8F%8A%E5%BA%94%E7%94%A8.assets/image-20200731195236135.png" alt="image-20200731195236135" style="zoom: 33%;" />



# 训练模型

## 从头开始训练

执行以下命令启动训练处理：

```
$ cd /home/ubuntu18/models-1.13.0/research/slim
$ nohup python train_image_classifier.py \
  --train_dir=/home/ubuntu18/tensorflow-test/flowers/inception_v4 \
  --dataset_name=flowers \
  --dataset_split_name=train \
  --dataset_dir=/home/ubuntu18/tensorflow-test/flowers/data/ \
  --model_name=inception_v4 \
  --max_number_of_steps=2000 \
  --batch_size=32 \
  --learning_rate=0.0001 \
  --learning_rate_decay_type=fixed \
  --save_interval_secs=60 \
  --save_summaries_secs=60 \
  --log_every_n_steps=10 \
  --optimizer=rmsprop \
  --weight_decay=0.00004 \
  &
$ tail -f nohup.out
```

使用 nohup 的目的是使用后台执行训练，避免终端连接断开后训练被中断。

训练的主要参数说明如下：

- train_dir - 训练目录，用于保存训练过程数据，比如.ckpt数据
- dataset_name - 数据集名称，当前指定flowers数据集，如果自定义数据集需要修改dataset_factory，例如fruits
- dataset_dir - 数据集所在目录，即TFRecord文件所在目录
- model_name - 指定要训练的模型，当前选用inception_v4，可以按需要选择其他模型
- max_number_of_steps - 指定训练的步数（每步执行一次batch_size的图片数量），当前只是进行测试，所以只指定了2000步
- batch_size - 指定每一次step处理的图片数量，如果gpu内存足够大，这个值可以设置大一点提升训练效率，如果是cpu训练，batch_size 过大可能会报错，这时可以适当调小，设置为1可以确定可以不出错
- learning_rate - 学习率，该值越小越好，不过设置过小则训练收敛速度慢且容易陷入局部最优，因此一般开始训练设置较大值达到快速收敛的目的，后期训练设置较小值让其贴近最优值
- **train_image_size - 指定训练图片的大小，inception_v4的默认图片大小是299，可以尝试放大训练图片的大小以传入更多细节**



## 迁移学习训练

可以基于以前的训练结果进行迁移训练，来减少整体训练时间并提升识别准确率，可以在 https://github.com/tensorflow/models/tree/master/research/slim 上找到对应模型的预训练结果并下载，并通过预训练模型继续进行训练。

如我们下载inception_v4_2016_09_09.tar.gz后，进行解压处理，得到预训练文件 inception_v4.ckpt：

```
$ tar -xzvf inception_v4_2016_09_09.tar.gz
```

执行命令如下：

```
$ cd /home/ubuntu18/models-1.13.0/research/slim
$ nohup python train_image_classifier.py \
  --train_dir=/home/ubuntu18/tensorflow-test/flowers/inception_v4 \
  --dataset_name=flowers \
  --dataset_split_name=train \
  --dataset_dir=/home/ubuntu18/tensorflow-test/flowers/data/ \
  --model_name=inception_v4 \
  --checkpoint_path=/home/ubuntu18/tensorflow-test/flowers/inception_v4.ckpt \
  --checkpoint_exclude_scopes=InceptionV4/Logits,InceptionV4/AuxLogits/Aux_logits \
  --trainable_scopes=InceptionV4/Logits,InceptionV4/AuxLogits/Aux_logits \
  --max_number_of_steps=2000 \
  --batch_size=32 \
  --learning_rate=0.0001 \
  --learning_rate_decay_type=fixed \
  --save_interval_secs=60 \
  --save_summaries_secs=60 \
  --log_every_n_steps=10 \
  --optimizer=rmsprop \
  --weight_decay=0.00004 \
  &
$ tail -f nohup.out
```

增加的几个迁移学习参数说明如下：

- checkpoint_path - 预训练模型地址，如果是继续自己的训练，则应指定自己原来已训练的ckpt文件
- checkpoint_exclude_scopes - 当pre-trained checkpoint对应的网络最后一层分类的类别数量和现在数据集的类别数量不匹配时使用，可以指定checkpoint restore时哪些层的参数不恢复。
- trainable_scopes - 如果只希望某些层参与训练，其他层的参数固定时，就使用这个flag，在这个flag中指定需要训练的参数。

注：在微调模型时，我们需要注意恢复checkpoint的权重。 特别是，当我们自己的数据集的标签和数量与预训练模型不同时，我们将无法恢复最终的logits（分类器）层。 因此，我们将使用--checkpoint_exclude_scopes标志，阻止加载某些变量。当我们自己的数据集的标签和数量与预训练模型不同时，新模型将具有与预训练模型尺寸不同的“logits”层。 例如，如果在Flowers上微调ImageNet训练的模型，预训练的logits图层具有尺寸[2048 x 1001]，但我们的新logits层将具有尺寸[2048 x 5]。



## 监控训练情况

可以通过tensorboard监控训练的情况，执行以下命令启动tensorboard（指定训练目录）：

```
$ tensorboard --logdir=/home/ubuntu18/tensorflow-test/flowers/inception_v4/
```

然后在浏览器打开服务地址查看训练过程：http://主机IP:6006/

![image-20200801114747968](TensorFlow-Slim%E5%9B%BE%E5%83%8F%E5%88%86%E7%B1%BB%E8%AE%AD%E7%BB%83%E5%8F%8A%E5%BA%94%E7%94%A8.assets/image-20200801114747968.png)



## 验证训练后的效果

可以通过准备的数据集中的验证集验证模型效果，执行以下命令：

```
$ cd /home/ubuntu18/models-1.13.0/research/slim
$ python eval_image_classifier.py \
  --checkpoint_path=/home/ubuntu18/tensorflow-test/flowers/inception_v4 \
  --eval_dir=/home/ubuntu18/tensorflow-test/flowers/inception_v4 \
  --dataset_name=flowers \
  --dataset_split_name=validation \
  --dataset_dir=/home/ubuntu18/tensorflow-test/flowers/data/ \
  --model_name=inception_v4
```

从头开始训练2000步得到的结果如下：

```
eval/Accuracy[0.1875]  # 准确率, 准确识别的样本数除以所有的样本数, 只有18%，很低
eval/Recall_5[1]  # 召回率，该模型100%召回
```

迁移训练2000步得到的结果如下：

```
eval/Accuracy[0.6875]  # 准确率, 准确识别的样本数除以所有的样本数, 有68%，相对高很多
eval/Recall_5[1]  # 召回率，该模型100%召回
```



# 导出固化模型

## 导出前向传播图

在slim文件夹下有 export_inference_graph.py 文件，运行该脚本即可导出前向传播图，运行方式如下：

```
python export_inference_graph.py \
  --alsologtostderr \
  --dataset_dir=/home/ubuntu18/tensorflow-test/flowers/data/ \
  --dataset_name=flowers \
  --model_name=inception_v4 \
  --image_size=299 \
  --output_file=/home/ubuntu18/tensorflow-test/flowers/inception_v4_inf.pb
```

部分参数说明：

- image_size - 可以指定图的大小，可以设置更大支持更多的细节处理
- output_file - 要导出的钱向传播图的路径和文件名

这个文件是前向传播图，并没有参数，所以也不是最终的模型，因此文件较小。



## 冻结模型

可以使用TensorFlow的工具脚本 freeze_graph.py 冻结模型，该脚本文件在TensorFlow的安装目录中，如果是使用anaconda3安装的，路径参考如下: **/home/ubuntu18/anaconda3/envs/tensorflow/lib/python3.7/site-packages/tensorflow_core/python/tools/freeze_graph.py**



执行以下命令将参数冻结到模型图中

```
$ cd /home/ubuntu18/tensorflow-test/flowers
$ python -u /home/ubuntu18/anaconda3/envs/tensorflow/lib/python3.7/site-packages/tensorflow_core/python/tools/freeze_graph.py \
  --input_graph=inception_v4_inf.pb \
  --input_checkpoint=./inception_v4/model.ckpt-2000 \
  --output_graph=./inception_v4_freeze.pb \
  --input_binary=True \
  --output_node_name=InceptionV4/Logits/Predictions
  
# 生成分类文件
$ cp ./data/labels.txt ./inception_v4_freeze.label
```



## 转换为TFLite文件

tflite模型相比于pb要精简的多，只是针对嵌入式平台进行的优化，对移植到嵌入式平台建议使用该方式，因为执行速度会更快，但是tflite并不是所有模型都支持，只支持部分模型。

```
$ toco \
--graph_def_file=/home/ubuntu18/tensorflow-test/flowers/inception_v4_freeze.pb \
--input_format=TENSORFLOW_GRAPHDEF \
--output_file=/home/ubuntu18/tensorflow-test/flowers/inception_v4_int.tflite \
--output_format=TFLITE \
--input_shapes=1,299,299,3 \
--inference_type=FLOAT \
--input_type=FLOAT \
--input_arrays=input \
--output_arrays=InceptionV4/Logits/Predictions
```



# 进行图像分类测试

1、创建一个测试的脚本 [inception_v4_use.py](TensorFlow-Slim%E5%9B%BE%E5%83%8F%E5%88%86%E7%B1%BB%E8%AE%AD%E7%BB%83%E5%8F%8A%E5%BA%94%E7%94%A8.assets/inception_v4_use.py) ，代码如下：

```
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
```

2、执行命令进行测试

```
$ python inception_v4_use.py \
	--file=inception_v4_use.jpg \
	--model_name=inception_v4_freeze.pb \
	--label_file=inception_v4_freeze.label \
	--image_size=299 \
	--num_top_predictions=5
```

输出的结果如下：

<img src="TensorFlow-Slim%E5%9B%BE%E5%83%8F%E5%88%86%E7%B1%BB%E8%AE%AD%E7%BB%83%E5%8F%8A%E5%BA%94%E7%94%A8.assets/image-20200801172658587.png" alt="image-20200801172658587" style="zoom:67%;" />



调用tensorflow模型需要指定冻结模型入参和出参的层名，如果不知道，可以通过以下的工具函数获取图信息：

1、创建一个 [tf_graph_info.py](TensorFlow-Slim%E5%9B%BE%E5%83%8F%E5%88%86%E7%B1%BB%E8%AE%AD%E7%BB%83%E5%8F%8A%E5%BA%94%E7%94%A8.assets/tf_graph_info.py) 文件，代码如下：

```
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# 打印输出TesnorFlow冻结模型计算图层及数据

import os
import sys
import tensorflow as tf

FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_string('file', 'inception_v4_freeze.pb', """冻结模型文件(.pb)""")
tf.app.flags.DEFINE_string('outfile', '', """打印输出文件路径, 不传代表屏幕输出""")
tf.app.flags.DEFINE_string('print_value', 'N', """是否打印参数值 Y/N""")
tf.app.flags.DEFINE_integer('print_outer', 0, """只打印前后多少层，0代表不控制""")


class Logger(object):
    """
    输出重定向的类
    """

    def __init__(self, filename=""):
        self.terminal = sys.stdout
        self.with_file = False
        if filename != '':
            self.with_file = True
            self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        if self.with_file:
            self.log.write(message)

    def flush(self):
        pass

    def __del__(self):
        # 关闭文件
        if self.with_file:
            self.log.close()


def print_graph_info(file: str, outfile: str = '', print_value: str = 'N', print_outer: int = 0):
    """
    输出图信息

    @param {str} file - 冻结模型文件路径(.pb)
    @param {str} outfile='' - 打印输出文件路径
    @param {str} print_value='N' - 是否打印参数值 Y/N
    @param {int} print_outer=0 - 只打印前后多少层，0代表不控制
    """
    # 输出保存的模型中参数名字及对应的值
    with tf.gfile.GFile(file, "rb") as f:  # 读取模型数据
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())  # 得到模型中的计算图和数据

    with tf.Graph().as_default() as graph:  # 这里的Graph()要有括号，不然会报TypeError
        tf.import_graph_def(graph_def, name="")  # 导入模型中的图到现在这个新的计算图中，不指定名字的话默认是 import
        sys.stdout = Logger(filename=outfile)  # 重定向输出
        current_index = 0  # 当前顺序
        outer_end = list()  # 打印最后几层的数组
        for op in graph.get_operations():  # 打印出图中的节点信息
            current_index += 1
            _str = '%s%s' % (str(op.name), '' if print_value != 'Y' else ', ' + str(op.values()))
            if print_outer > 0:
                # 需要控制只打印外层
                if current_index <= print_outer:
                    # 打印前几层
                    print(_str)
                else:
                    # 后几层放入数组，最后再打印
                    if len(outer_end) >= print_outer:
                        outer_end.pop(0)
                    outer_end.append(_str)
            else:
                # 全部打印
                print(_str)

        if print_outer > 0:
            # 打印最后几层
            print('...')
            print('\n'.join(outer_end))


if __name__ == '__main__':
    # 当程序自己独立运行时执行的操作
    print_graph_info(
        FLAGS.file, FLAGS.outfile, FLAGS.print_value, FLAGS.print_outer
    )
```

2、运行脚本查看层信息

```
$ python test.py --print_outer=5

input
InceptionV4/Conv2d_1a_3x3/weights
InceptionV4/Conv2d_1a_3x3/weights/read
InceptionV4/InceptionV4/Conv2d_1a_3x3/Conv2D
InceptionV4/InceptionV4/Conv2d_1a_3x3/BatchNorm/Const
...
InceptionV4/Logits/Logits/biases
InceptionV4/Logits/Logits/biases/read
InceptionV4/Logits/Logits/MatMul
InceptionV4/Logits/Logits/BiasAdd
InceptionV4/Logits/Predictions
```

因此输入层为 “input:0” ，输出层为 “InceptionV4/Logits/Predictions:0” 。