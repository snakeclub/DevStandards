# TensorFlow-mask物体识别训练及应用

本示例基于 TensorFlow Object Detection API 来开展mask物体识别的训练和应用，TensorFlow Object Detection API 的安装步骤可直接参考 《TensorFlow安装部署及简单应用-Python.md》。



# 创建自己的数据集

## 进行图像标注

首先需先进行要识别的物体图像标注，可以使用 LabelMe 工具进行标注处理，总体步骤说明如下：

1、执行以下命令安装 LabelMe：

```
$ pip install labelme
```

2、在命令行执行 “labelme” 打开主程序界面进行图像标注；

注：在Windodw安装后执行 labelme 可能会出现报错信息：“UnicodeDecodeError: 'gbk' codec can't decode byte 0xa3 in position 232: illegal multibyte sequence” , 这是由于获取配置文件时使用系统默认编码"gbk"解析导致出错，可以根据出错信息找到源码文件修改，指定使用 ”utf-8“ 打开配置文件。

例如可以看到以下错误信息：

```
 File "c:\users\74143\appdata\local\programs\python\python37\lib\site-packages\labelme\config\__init__.py", line 73, in get_config
    config_from_yaml = yaml.safe_load(f)
```

则可以编辑 ”c:\users\74143\appdata\local\programs\python\python37\lib\site-packages\labelme\config\__init__.py“ 文件，将73行报错代码的前面 open 部分指定使用 ”utf-8“ 编码：

```
with open(config_from_yaml) as f:
    logger.info(
        "Loading config file from: {}".format(config_from_yaml)
    )
    config_from_yaml = yaml.safe_load(f)
修改为：
with open(config_from_yaml, encoding='utf-8') as f:
    logger.info(
        "Loading config file from: {}".format(config_from_yaml)
    )
    config_from_yaml = yaml.safe_load(f)
```

3、使用 labelme 打开要标注的图片，对图片进行标注，注意 labelme并不支持物体内部有缕空的情况，因此如果遇到该情况，需要将缕空部分标注为 ”hole“ 的，以便后续训练数据生成时进行清除处理:

![image-20200926211535414](TensorFlow-mask%E7%89%A9%E4%BD%93%E8%AF%86%E5%88%AB%E8%AE%AD%E7%BB%83%E5%8F%8A%E5%BA%94%E7%94%A8.assets/image-20200926211535414.png)

**注意：保存标注文件（*.json）时，注意与图片要放在同一个目录下，便于后面转换格式的脚本直接进行处理。**

4、labelme 自带的标注数据处理

**注意：仅介绍 labelme 原理，本示例后续使用其他方式进行数据转换处理，因此实际无需执行本步骤**

labelme标注保存后将生成一个含标注的 json 文件，接着需要使用 labelme 的 json_to_dataset.py 工具将标注文件转换为可以处理的数据文件，该工具脚本位于 labelme 安装目录下的 cli 子目录中，命令如下：

```
cd c:\Users\74143\AppData\Local\Programs\Python\Python37\Lib\site-packages\labelme\cli
python json_to_dataset.py d:\logo.json
```

该命令将会生成供训练的数据文件并放置在json文件对应的 *_json 文件夹中，例如以上命令将生成 logo_json 文件夹，文件夹中包含以下文件（其中label.png是图片标注的分割掩模）：

![image-20200926220243416](TensorFlow-mask%E7%89%A9%E4%BD%93%E8%AF%86%E5%88%AB%E8%AE%AD%E7%BB%83%E5%8F%8A%E5%BA%94%E7%94%A8.assets/image-20200926220243416.png)

注意：json_to_dataset.py 存在一个bug，要求 hole 标注必须在后面完成才行，并且不支持生成多个文件，在此提供一个可支持按目录转换的工具 [path_to_dataset.py](TensorFlow-mask%E7%89%A9%E4%BD%93%E8%AF%86%E5%88%AB%E8%AE%AD%E7%BB%83%E5%8F%8A%E5%BA%94%E7%94%A8.assets/path_to_dataset.py) ，同时该工具修复了 hole 标注必须后面完成的bug，可执行以下命令进行批量转换：

```
python path_to_dataset.py D:/mask_rcnn_resnet101/train_set -o D:/mask_rcnn_resnet101/train_dataset/
```



## 转换为tf-record格式文件

**1、创建 label_map.pbtxt 文件**

label_map.pbtxt 文件是所有需要检测的类名及类标号的配置文件，该文件的后缀名为 **.pbtxt**，写法很简单，假如你要检测 ’person' ， 'car' ，'bicycle' 等类目标，则写入如下内容：

```
item {
    id: 1
    name: 'person'
}

item {
    id: 2
    name: 'car'
}

item {
    id: 3
    name: 'bicycle'
}

...

```

**2、将标注图片转换为tf-record格式文件**

参考网上博客的文章和代码，整理了一个直接将 labelme 标注文件转换为 tf-record 格式文件的脚本： [create_tf_record.py](TensorFlow-mask%E7%89%A9%E4%BD%93%E8%AF%86%E5%88%AB%E8%AE%AD%E7%BB%83%E5%8F%8A%E5%BA%94%E7%94%A8.assets/create_tf_record.py)  ，脚本的命令如下：

```
python create_tf_record.py \
  --images_dir=D:/mask_rcnn_resnet101/train_set \
  --label_map_path=D:/mask_rcnn_resnet101/labelmap.pbtxt \
  --output_path=D:/mask_rcnn_resnet101/tf_record \
  --output_name=train \
  --num_per_file=50
```

输入参数说明如下：

- images_dir : 必填，要处理的图片目录，支持子目录，但要求标注文件（*.json）与图片文件在同一个目录中
- label_map_path : 必填，类名映射字典文件（label_map.pbtxt）
- output_path : 必填，tf-record 文件的输出目录
- output_name : 选填，输出文件名，默认为 ”train“ ，tf-record 文件名，如果只生成单个文件，文件名将会是 ”train.record“；如果生成多个文件，文件名将为 ”train.record-00001-of-00005“ 样式的多个文件；
- num_per_file : 选填，每个文件包含的图片数量，如果不送代表全部图片生成单个文件；如果送入代表按图片文件数量拆分为多个文件（文件数量特别多的时候减少每个文件大小）

**3、通过以上步骤，进行标注处理和生成两个tf-record文件，一个是训练集(train)，用于进行训练；一个是验证集(val)，用于进行验证。**



# 训练 Mask R-CNN 模型

**1、获取预训练模型文件**

通过预训练模型文件可以加快训练收敛速度，如果需要重新训练可以跳过该步骤。

可以在以下地址选择要下载的预训练模型：https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf1_detection_zoo.md

我们挑选的是mask_rcnn_resnet101_atrous_coco，下载地址：http://download.tensorflow.org/models/object_detection/mask_rcnn_resnet101_atrous_coco_2018_01_28.tar.gz

将预训练模型放置到训练服务器上并解压缩。

**2、获取 Object Detection API 训练配置文件**

我们选择的是mask_rcnn_resnet101模型，可以从 Object Detection API 的安装目录 ”models\research\object_detection\samples\configs“ 下获取对应模型的训练配置样例文件进行修改，复制 "mask_rcnn_resnet101_atrous_coco.config", 并命名为 ”mask_rcnn_resnet101.config“。

**3、修改 mask_rcnn_resnet101.config 配置文件**

需要修改的点见中文注释：

```
# Mask R-CNN with Resnet-101 (v1), Atrous version
# Configured for MSCOCO Dataset.
# Users should configure the fine_tune_checkpoint field in the train config as
# well as the label_map_path and input_path fields in the train_input_reader and
# eval_input_reader. Search for "PATH_TO_BE_CONFIGURED" to find the fields that
# should be configured.

model {
  faster_rcnn {
    # 分类数量
    num_classes: 1
    image_resizer {
      keep_aspect_ratio_resizer {
        min_dimension: 800
        max_dimension: 1365
      }
    }
    number_of_stages: 3
    feature_extractor {
      type: 'faster_rcnn_resnet101'
      first_stage_features_stride: 8
    }
    first_stage_anchor_generator {
      grid_anchor_generator {
        scales: [0.25, 0.5, 1.0, 2.0]
        aspect_ratios: [0.5, 1.0, 2.0]
        height_stride: 8
        width_stride: 8
      }
    }
    first_stage_atrous_rate: 2
    first_stage_box_predictor_conv_hyperparams {
      op: CONV
      regularizer {
        l2_regularizer {
          weight: 0.0
        }
      }
      initializer {
        truncated_normal_initializer {
          stddev: 0.01
        }
      }
    }
    first_stage_nms_score_threshold: 0.0
    first_stage_nms_iou_threshold: 0.7
    first_stage_max_proposals: 300
    first_stage_localization_loss_weight: 2.0
    first_stage_objectness_loss_weight: 1.0
    initial_crop_size: 14
    maxpool_kernel_size: 2
    maxpool_stride: 2
    second_stage_box_predictor {
      mask_rcnn_box_predictor {
        use_dropout: false
        dropout_keep_probability: 1.0
        predict_instance_masks: true
        mask_height: 33
        mask_width: 33
        mask_prediction_conv_depth: 0
        mask_prediction_num_conv_layers: 4
        fc_hyperparams {
          op: FC
          regularizer {
            l2_regularizer {
              weight: 0.0
            }
          }
          initializer {
            variance_scaling_initializer {
              factor: 1.0
              uniform: true
              mode: FAN_AVG
            }
          }
        }
        conv_hyperparams {
          op: CONV
          regularizer {
            l2_regularizer {
              weight: 0.0
            }
          }
          initializer {
            truncated_normal_initializer {
              stddev: 0.01
            }
          }
        }
      }
    }
    second_stage_post_processing {
      batch_non_max_suppression {
        score_threshold: 0.0
        iou_threshold: 0.6
        max_detections_per_class: 100
        max_total_detections: 300
      }
      score_converter: SOFTMAX
    }
    second_stage_localization_loss_weight: 2.0
    second_stage_classification_loss_weight: 1.0
    second_stage_mask_prediction_loss_weight: 4.0
  }
}

train_config: {
  # 每批图片大小
  batch_size: 16
  optimizer {
    momentum_optimizer: {
      learning_rate: {
        manual_step_learning_rate {
          # 设置学习率
          initial_learning_rate: 0.0003
          schedule {
            step: 900000
            learning_rate: .00003
          }
          schedule {
            step: 1200000
            learning_rate: .000003
          }
        }
      }
      momentum_optimizer_value: 0.9
    }
    use_moving_average: false
  }
  gradient_clipping_by_norm: 10.0
  # 迁移训练指定的预训练模型
  fine_tune_checkpoint: "/home/ubuntu18/cc/training/mask_rcnn_resnet101/mask_rcnn_resnet101_atrous_coco_2018_01_28/model.ckpt"
  from_detection_checkpoint: true
  # Note: The below line limits the training process to 200K steps, which we
  # empirically found to be sufficient enough to train the pets dataset. This
  # effectively bypasses the learning rate schedule (the learning rate will
  # never decay). Remove the below line to train indefinitely.
  # 需要训练的总步数
  num_steps: 200000
  data_augmentation_options {
    random_horizontal_flip {
    }
  }
}

train_input_reader: {
  tf_record_input_reader {
    # 训练文件
    input_path: "/home/ubuntu18/cc/training/mask_rcnn_resnet101/dataset/train.record-?????-of-00002"
  }
  # pbtxt文件
  label_map_path: "/home/ubuntu18/cc/training/mask_rcnn_resnet101/dataset/labelmap.pbtxt"
  load_instance_masks: true
  mask_type: PNG_MASKS
}

eval_config: {
  # 验证集数量
  num_examples: 4
  # Note: The below line limits the evaluation process to 10 evaluations.
  # Remove the below line to evaluate indefinitely.
  max_evals: 10
}

eval_input_reader: {
  tf_record_input_reader {
    # 验证集
    input_path: "/home/ubuntu18/cc/training/mask_rcnn_resnet101/dataset/val.record"
  }
  # pbtxt文件
  label_map_path: "/home/ubuntu18/cc/training/mask_rcnn_resnet101/dataset/labelmap.pbtxt"
  load_instance_masks: true
  mask_type: PNG_MASKS
  shuffle: false
  num_readers: 1
}
```

4、执行以下命令进行训练

```
# 启动训练
nohup python /home/ubuntu18/models-1.13.0/research/object_detection/model_main.py --logtostderr --model_dir=/home/ubuntu18/cc/training/mask_rcnn_resnet101/training/ --pipeline_config_path=/home/ubuntu18/cc/training/mask_rcnn_resnet101/mask_rcnn_resnet101.config &

# 实时查看最新训练日志
tail -f nohup.out

# 通过tensorboard可视化训练过程
tensorboard --logdir=/home/ubuntu18/cc/training/mask_rcnn_resnet101/training/
```

**注：Object Detection API 支持训练期间中断，只要不删除训练目录下的文件，下一次启动会自动在上一保存点的基础上继续训练；此外，完成训练后可以将对应的checkpoint文件保存下来，在下一次训练时可以指定训练 config 文件的 fine_tune_checkpoint 参数至该checkpoint文件，就可以在上次训练的基础上进行迁移训练。**



# 导出固化模型

模型训练完成后，接下来就是导出frozen_inference_graph.pb文件，该文件中包含了我们训练好的检测器以及网络架构信息和参数信息等。

导出模型的命令如下：

```
# 跳转到 Object Detection API 安装目录
cd /home/ubuntu18/models-1.13.0/research/object_detection
# 导出模型
python export_inference_graph.py --input_type=image_tensor --pipeline_config_path=/home/ubuntu18/cc/training/mask_rcnn_resnet101/mask_rcnn_resnet101.config --trained_checkpoint_prefix=/home/ubuntu18/cc/training/mask_rcnn_resnet101/training/model.ckpt-200000 --output_directory=/home/ubuntu18/cc/training/mask_rcnn_resnet101/export/r01
```



# 进行图片检测

可以通过脚本 [test_image.py](TensorFlow-mask%E7%89%A9%E4%BD%93%E8%AF%86%E5%88%AB%E8%AE%AD%E7%BB%83%E5%8F%8A%E5%BA%94%E7%94%A8.assets/test_image.py) 使用训练后的模型进行图片检测，检测前需修改脚本中的几个输入项：

```
# 将 object_detection 的安装路径导入
sys.path.append(r'D:\tensorflow\models\research\object_detection')
……
# 指定冻结模型文件
PATH_TO_CKPT = r'D:\ccproject\mask_rcnn_resnet101\frozen_inference_graph.pb'
……
# 指定labelmap.pbtxt文件
PATH_TO_LABELS = os.path.join(
    r'D:\ccproject\mask_rcnn_resnet101', 'labelmap.pbtxt')
……
# 修改分类数量
NUM_CLASSES = 1
……
# 指定要检测的图片
_image_path = r"D:\ccproject\mask_rcnn_resnet101\train_set\bangle_flat\0000000094.jpg"
……
# 可修改的识别和显示参数
_font = ImageFont.truetype("simhei.ttf", 20, encoding="utf-8")  # 显示字体
_min_score = 0.9  # 要显示的最低匹配百分比分数
_line_width = 3  # 物体框线大小
_alpha = 0.4  # Mask透明度
……
```



# 存在问题

mask_rcnn_resnet101网络对显存/内存要求比较高，在图片检测时会出现 “Allocation of xxx exceeds 10% of system memory” 的提示，并且检测速度比较慢，如果对速度要求比较高，可以改为使用 mask_rcnn_inception_v2 ，使用的代码脚本和步骤是一样的，更换训练配置文件为对应的配置即可。