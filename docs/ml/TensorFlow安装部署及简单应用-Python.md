# TensorFlow安装部署及简单应用-Python

## TensorFlow安装部署（Python）

1、准备Python环境，可以安装Anaconda简化环境的要求，Anaconda的安装配置可参考《Anaconda安装使用手册》；

2、利用Anaconda创建对应Python版本的虚拟环境，以下以“tensorflow”作为演示的环境名称：

```
# 创建虚拟环境并切换至该环境
conda create --name tensorflow python=3.7
activate tensorflow

# 注:如果是linux执行  conda activate tensorflow
```

**注：要根据所选择的tensorflow版本来安装所适配的python版本，这里我们选择python 3.7以上的版本。**

3、安装对应版本的tensorflow：

由于演示打算使用TensorFlow Object Detection API做物品识别，而该API演示模型代码支持的是tensorflow1.X版本，所以选择了1.15.0版，且特定选择了cpu版本：

```
pip install tensorflow-cpu==1.15.0
```

其他安装参考：

```
# 使用国内镜像服务器下载安装（解决下载速度问题）
pip install -i https://mirrors.aliyun.com/pypi/simple/ tensorflow-cpu==1.15.0

# 安装最新版本（cpu + gpu版本）
pip install tensorflow

# 升级tensorflow版本
pip install --upgrade tensorflow
```

4、安装完以后检查是否成功安装

```
python
>>>import tensorflow
```

如果没有报错则代表安装成功

![image-20200513084358567](TensorFlow%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2%E5%8F%8A%E7%AE%80%E5%8D%95%E5%BA%94%E7%94%A8-Python.assets/image-20200513084358567.png)



注意：需要检查tensorflow和numpy的版本兼容性，如本所安装的tensorflow 1.15.0应对应numpy1.16.0版本，numpy版本太高可能会导致问题，降级或升级脚本如下：

```
pip install -U -i https://pypi.tuna.tsinghua.edu.cn/simple numpy==1.16.0
```



## GPU版本安装部署

### 安装版本说明

GPU版本的基础安装跟CPU版本的类似，只是需要安装tensorflow-gpu包，但需要注意的是GPU版本需要显卡的支持（物理显卡，安装对应的驱动程序），以及安装CUDA和cuDNN。

逐个包单独安装的步骤可以参考官方文档：

tensorflow安装：https://tensorflow.google.cn/install/source

GPU支持安装：https://tensorflow.google.cn/install/gpu



不同版本的tensorflow需要安装指定的CUDA、cuDNN版本，对应参考清单如下：

| 版本                  | Python 版本  | 编译器    | 构建工具     | cuDNN | CUDA |
| :-------------------- | :----------- | :-------- | :----------- | :---- | :--- |
| tensorflow-2.1.0      | 2.7、3.5-3.7 | GCC 7.3.1 | Bazel 0.27.1 | 7.6   | 10.1 |
| tensorflow-2.0.0      | 2.7、3.3-3.7 | GCC 7.3.1 | Bazel 0.26.1 | 7.4   | 10.0 |
| tensorflow_gpu-1.14.0 | 2.7、3.3-3.7 | GCC 4.8   | Bazel 0.24.1 | 7.4   | 10.0 |
| tensorflow_gpu-1.13.1 | 2.7、3.3-3.7 | GCC 4.8   | Bazel 0.19.2 | 7.4   | 10.0 |
| tensorflow_gpu-1.12.0 | 2.7、3.3-3.6 | GCC 4.8   | Bazel 0.15.0 | 7     | 9    |
| tensorflow_gpu-1.11.0 | 2.7、3.3-3.6 | GCC 4.8   | Bazel 0.15.0 | 7     | 9    |
| tensorflow_gpu-1.10.0 | 2.7、3.3-3.6 | GCC 4.8   | Bazel 0.15.0 | 7     | 9    |
| tensorflow_gpu-1.9.0  | 2.7、3.3-3.6 | GCC 4.8   | Bazel 0.11.0 | 7     | 9    |
| tensorflow_gpu-1.8.0  | 2.7、3.3-3.6 | GCC 4.8   | Bazel 0.10.0 | 7     | 9    |
| tensorflow_gpu-1.7.0  | 2.7、3.3-3.6 | GCC 4.8   | Bazel 0.9.0  | 7     | 9    |
| tensorflow_gpu-1.6.0  | 2.7、3.3-3.6 | GCC 4.8   | Bazel 0.9.0  | 7     | 9    |
| tensorflow_gpu-1.5.0  | 2.7、3.3-3.6 | GCC 4.8   | Bazel 0.8.0  | 7     | 9    |
| tensorflow_gpu-1.4.0  | 2.7、3.3-3.6 | GCC 4.8   | Bazel 0.5.4  | 6     | 8    |
| tensorflow_gpu-1.3.0  | 2.7、3.3-3.6 | GCC 4.8   | Bazel 0.4.5  | 6     | 8    |
| tensorflow_gpu-1.2.0  | 2.7、3.3-3.6 | GCC 4.8   | Bazel 0.4.5  | 5.1   | 8    |
| tensorflow_gpu-1.1.0  | 2.7、3.3-3.6 | GCC 4.8   | Bazel 0.4.2  | 5.1   | 8    |
| tensorflow_gpu-1.0.0  | 2.7、3.3-3.6 | GCC 4.8   | Bazel 0.4.2  | 5.1   | 8    |



### 安装显卡驱动（ubuntu18）

对于已安装了显卡驱动的情况，如果遇到Linux的内核升级情况，将会导致已安装的驱动无效，执行`nvidia-smi`命令会出现“NVIDIA-SMI has failed because it couldn't communicate with the NVIDIA driver”的错误提示。

这时候需要重新安装显卡驱动，以下是安装步骤：

1、删除原有NVIDIA驱动

```
sudo apt-get remove --purge nvidia*
```

2、禁用nouveau

```
sudo vi /etc/modprobe.d/blacklist.conf
```

在最后一行添加

```
blacklist nouneau
```

3、升级配置，执行

```
sudo update-initramfs -u
```

4、重启系统并检查nouveau是否已被禁用

```
sudo reboot

# 没输出代表禁用生效, 要在重启之后执行
lsmod | grep nouveau 
```

5、从[NVIDIA显卡驱动](https://www.cnblogs.com/youpeng/p/)下载对应的显卡驱动，例如“NVIDIA-Linux-x86_64-418.43.run”

6、执行以下命令进行安装：

```
sudo chmod a+x NVIDIA-Linux-x86_64-418.43.run

sudo ./NVIDIA-Linux-x86_64-418.43.run --no-opengl-files --no-x-check --no-nouveau-check
```

- –no-opengl-files 只安装驱动文件，不安装OpenGL文件。这个参数最重要
- –no-x-check 安装驱动时不检查X服务
- –no-nouveau-check 安装驱动时不检查nouveau

7、检验是否安装成功，命令`nvidia-smi`，如果成功安装驱动将显示以下信息：

```
(tensorflow) ubuntu18@ubuntu18-System-Product-Name:~$ nvidia-smi
Fri May 29 13:17:54 2020       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 440.82       Driver Version: 440.82       CUDA Version: 10.2     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  GeForce RTX 208...  Off  | 00000000:01:00.0 Off |                  N/A |
| 41%   33C    P8     3W / 260W |    112MiB / 11016MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID   Type   Process name                             Usage      |
|=============================================================================|
|    0      1128      G   /usr/lib/xorg/Xorg                            20MiB |
|    0      1749      G   /usr/lib/xorg/Xorg                            90MiB |
+-----------------------------------------------------------------------------+
```

8、ubuntu一旦重启经常会更新内核，一旦更新内核后，显卡驱动就会失效，需要重新安装驱动，最好的办法是禁止ubuntu的自动更新，执行以下命令：

```
sudo apt-mark hold linux-image-generic linux-headers-generic 
```

如果想重新启动内核更新，可以执行：

```
sudo apt-mark unhold linux-image-generic linux-headers-generic
```



### 安装CUDA及cuDNN

我们可以使用Anaconda更简单地一步进行安装（前提是显卡驱动已经安装好）, Conda会自动将依赖的CUDA和cuDNN安装上：

```
conda install tensorflow-gpu==1.15.0
```

安装后，可以通过以下方法进行Tensorflow是否使用gpu的验证：

**方法1**

```
import tensorflow as tf
if tf.test.gpu_device_name():
    print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))
else:
    print("Please install GPU version of TF")
```

**方法2**

```
import tensorflow as tf

tf = tf.Session(config=tf.ConfigProto(log_device_placement=True))
tf.list_devices()
```

**方法3**

```
import tensorflow as tf

tf.test.gpu_device_name()
```

**方法4**

```
from tensorflow.python.client import device_lib 

device_lib.list_local_devices()
```



## 常见安装问题及解决方案

**运行中出现CPU的告警提示（AVX2）**

如果在运行过程中有出现以下告警提示：

```
Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2
```

意思是当前机器的CPU支持AVX指令扩展，但是安装的TensorFlow版本并未针对AVX指令扩展编译，因此无法使用这些优化的指令（使用标准SSE指令）。

AVX指令引入了融合乘法累加（FMA）操作，加速了线性代数计算，即点积，矩阵乘法，卷积等。而几乎所有机器学习训练都涉及大量这些操作，支持AVX和FMA的CPU处理更快（最高达300％）。

注：要检查自己的CPU支持的指令集，可以通过CPU-Z（Windows）查看，下载地址：https://www.cpuid.com/downloads/cpu-z/cpu-z_1.92-cn.zip



解决这个告警有两个办法：

（1）忽略告警信息（掩耳盗铃的方法）

在代码中增加以下环境变量配置：

```
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
```

（2）安装支持AVX的版本

可以到 https://github.com/fo40225/tensorflow-windows-wheel 直接下载不同版本（支持CPU指令集、操作系统、Python版本）的whl安装包。



**import出现ImportError错误（Windows）**

1、安装后检查如果发现 “ImportError：DLL load failed” 的错误，很大概率是因为没有安装[Microsoft Visual C++ Redistributable for Visual Studio 2015, 2017 and 2019](https://support.microsoft.com/zh-cn/help/2977003/the-latest-supported-visual-c-downloads) ， 可以到微软的官网下载安装：

<img src="TensorFlow%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2%E5%8F%8A%E7%AE%80%E5%8D%95%E5%BA%94%E7%94%A8-Python.assets/image-20200512235003955.png" alt="image-20200512235003955" style="zoom:50%;" />

如果安装完还有同样的问题，也有可能是环境变量PATHEXT缺少了“.DLL”导致（Win10默认没有这个变量值），可以在环境变量上加上试一下：

<img src="TensorFlow%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2%E5%8F%8A%E7%AE%80%E5%8D%95%E5%BA%94%E7%94%A8-Python.assets/image-20200512235205476.png" alt="image-20200512235205476" style="zoom:50%;" />



## TensorFlow简单应用 - 自训练物体识别模型

Google开源了TensorFlow Object Detection API，该API可以方便地让一般开发人员自行进行物体识别模型的训练，以下利用该API来演示TensorFLow的入门应用。

**注意：由于TensorFlow 2.X版本取消了 “tf.contrib” 的支持，因此无法兼容TensorFlow Object Detection API的运行，请选择TensorFlow 1.X版本运行该示例。**

### 安装TensorFlow Object Detection API

1、安装机器学习应用常用的科学包（后面演示应用要使用到）：

```
pip install protobuf
pip install pillow
pip install lxml
pip install Cython
pip install jupyter
pip install matplotlib
pip install pandas
pip install opencv-python
pip install pycocotools
pip install contextlib2
# 降级numpy到适配的版本
pip install -U numpy==1.16.0

带镜像获取的安装命令：
pip install -i https://mirrors.aliyun.com/pypi/simple/ protobuf
pip install -i https://mirrors.aliyun.com/pypi/simple/ pillow
pip install -i https://mirrors.aliyun.com/pypi/simple/ lxml
pip install -i https://mirrors.aliyun.com/pypi/simple/ Cython
pip install -i https://mirrors.aliyun.com/pypi/simple/ jupyter
pip install -i https://mirrors.aliyun.com/pypi/simple/ matplotlib
pip install -i https://mirrors.aliyun.com/pypi/simple/ pandas
pip install -i https://mirrors.aliyun.com/pypi/simple/ opencv-python
pip install -i https://mirrors.aliyun.com/pypi/simple/ pycocotools
pip install -i https://mirrors.aliyun.com/pypi/simple/ contextlib2
pip install -U -i https://pypi.tuna.tsinghua.edu.cn/simple numpy==1.16.0
```

**注意：**

- **pandas和opencv-python不是该API所必须的包，但是后面在做测试的时候可能会用到;**

- **对应不同的tensorflow版本，protobuf的版本可能有要求，如果出现一些问题可以考虑降低protobuf的版本，本案例用的版本是3.11.4 ;**

- **建议使用国内镜像服务提升下载安装速度，例如 “`pip install -i https://mirrors.aliyun.com/pypi/simple/ protobuf`” ;**

- **pycocotools是API演示案例要使用的COCO算法的工具；由于pycocotools作者压根就没考虑windows版本，所以如果安装Windows版本需要采取以下方式：**

  - 安装Visual C++ 编译环境问题

    pycocotools需要Microsoft Visual C++ 14.0进行编译，可以下载**官方c++运行库安装工具**进行安装，下载地址：https://blog.csdn.net/qq_38161040/article/details/88203864

  - 从 https://github.com/philferriere/cocoapi 下载技术大佬改写的支持Windows安装的pycocotools源码包，解压到本地，例如 "d:\\cocoapi\\";

  - 执行以下命令进行安装：

    ```
    cd d:\cocoapi\PythonAPI
    python setup.py build_ext install
    ```

  - 如果安装过程遇到Wno-cpp和Wno-unused-function问题，按以下方式解决再执行安装：

    **错误提示大致为：**cl: 命令行 error D8021 :无效的数值参数“/Wno-cpp” 和 cl: 命令行 error D8021 :无效的数值参数“/Wno-unused-function

    **解决方式：** 删除`cocoapi\PythonAPI\setup.py`里的Wno-cpp和Wno-unused-function参数。

    ![img](TensorFlow%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2%E5%8F%8A%E7%AE%80%E5%8D%95%E5%BA%94%E7%94%A8-Python.assets/13068476-6618ef3135277c23.webp)



2、下载TensorFlow Object Detection API，地址：https://github.com/tensorflow/models , 由于我们安装的tensorflow版本为1.15， 对应要下载 https://github.com/tensorflow/models/releases 中的v1.13.0版本发布包，下载地址：https://github.com/tensorflow/models/archive/v1.13.0.zip



3、将下载的源码包解压到D:\tensorflow\models目录下;

注：如果下载的速度慢，可以通过 https://g.widora.cn/  / http://g.widyun.com/这个代理网站加速下载。



4、配置API对应路径的环境变量，确保相应文件路径可以被找到：

**方法1：设置系统级别的环境变量**

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



**方法2：命令行设置局部环境变量**

```
Windows：
set PYTHONPATH=D:\tensorflow\models;D:\tensorflow\models\research;D:\tensorflow\models\research\slim

Ubuntu：
export PYTHONPATH=/home/ubuntu18/models-1.13.0:/home/ubuntu18/models-1.13.0/research:/home/ubuntu18/models-1.13.0/research/slim
```

注：这样的方法需要每次激活虚拟环境后都要重新执行一次。

5、编译Protobuf

对于Protobuf的介绍，请参见 (https://www.ibm.com/developerworks/cn/linux/l-cn-gpb/index.html) 。

执行以下命令将.proto文件编译为.py执行脚本：

```
d:
cd d:\tensorflow\models\research
protoc .\object_detection/protos/*.proto --python_out=.
```

7、安装API

```
cd d:\tensorflow\models\research
python setup.py build
python setup.py install
```

6、检查安装结果

```
cd d:\tensorflow\models\research\object_detection\builders
python model_builder_test.py
```

如果出现下面的结果，则表示安装成功：

![image-20200513001347182](TensorFlow%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2%E5%8F%8A%E7%AE%80%E5%8D%95%E5%BA%94%E7%94%A8-Python.assets/image-20200513001347182.png)

注：如果出现 “AttributeError: module 'tensorflow' has no attribute 'contrib'” ，说明你使用的是TensorFlow2.X版本，应安装TensorFlow1.X版本。



7、试跑官方演示模型

（1）使用jupyter执行演示，运行以下脚本跳转到object_detection路径，打开jupyter

```
cd d:\tensorflow\models\research\object_detection\
jupyter-notebook
```

（2）在打开的页面中，点击object_detection_tutorial.ipynb

<img src="TensorFlow%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2%E5%8F%8A%E7%AE%80%E5%8D%95%E5%BA%94%E7%94%A8-Python.assets/image-20200514223959306.png" alt="image-20200514223959306" style="zoom:50%;" />

（3）在打开的脚本页面上，点击 “Cell -> Run All” 菜单，执行该演示脚本

<img src="TensorFlow%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2%E5%8F%8A%E7%AE%80%E5%8D%95%E5%BA%94%E7%94%A8-Python.assets/image-20200514224154470.png" alt="image-20200514224154470" style="zoom:50%;" />

（4）等待脚本执行完成（可能要等几分钟到十几分钟，有可能第一次执行很长时间没有出结果，这时候可以运行多一次），最后会出现通过模型识别的两张演示图，如果正常则说明安装成功。

<img src="TensorFlow%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2%E5%8F%8A%E7%AE%80%E5%8D%95%E5%BA%94%E7%94%A8-Python.assets/image-20200514224451806.png" alt="image-20200514224451806" style="zoom: 33%;" />

**注：脚本是否在运行可以观察脚本框前面的 “In [  ]” ，如果中括号里面为“*”代表等待执行，如果为数字代表完成执行，例如 “In [\*]”  代表等待执行，“In [1]” 代表已经执行完成。**



### 训练自己的识别模型

#### 利用标注工具对训练图片进行标注

首先需要获取图片集，并从图片集挑选形成训练图片集和测试图片集（比例大致可以为5:1），然后利用标注工具LabelImg（下载地址：https://github.com/tzutalin/labelImg/releases ）进行标注，LabelImg的具体使用方式可以参考这篇博客（ https://blog.csdn.net/lwplwf/article/details/78367929 ）。

为了节省时间，我们直接从 https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10 中获取一个开源作者已经标注好的训练图片和测试图片， 选取的是扑克样本。

<img src="TensorFlow%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2%E5%8F%8A%E7%AE%80%E5%8D%95%E5%BA%94%E7%94%A8-Python.assets/image-20200514234650959.png" alt="image-20200514234650959" style="zoom: 33%;" />

将图片放到自己设置的训练目录中，本例中的路径是 “D:\tensorflow\my_test” 。示例中训练图片的目录是train，测试图片目录是test，进行标注后每个图片都会生成一个对应的 .xml 文件记录标注信息。

<img src="TensorFlow%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2%E5%8F%8A%E7%AE%80%E5%8D%95%E5%BA%94%E7%94%A8-Python.assets/image-20200515084008918.png" alt="image-20200515084008918" style="zoom:50%;" />



#### 将.xml文件转换成.csv文件

为了便于处理，可以将多个文件xml的信息转换成在一个csv文件的内容，csv的格式为：

| filename | width  | height | class      | xmin     | ymin    | xmax      | ymax       |
| -------- | ------ | ------ | ---------- | -------- | ------- | --------- | ---------- |
| 文件名   | 图片宽 | 图片高 | 选框分类名 | left坐标 | top坐标 | right坐标 | bottom坐标 |

1、在图片的上级目录中创建 “xml_to_csv.py” 代码脚本（“D:\tensorflow\my_test\xml_to_csv.py”），代码内容如下（具体要处理的路径和目录可根据需要自行修改）：

```
import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET


def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def main():
    # 可以按需要自行调整路径
    for folder in ['train', 'test']:
        image_path = os.path.join(os.getcwd(), folder)
        xml_df = xml_to_csv(image_path)
        xml_df.to_csv((folder + '_labels.csv'), index=None)
        print('Successfully converted xml to csv.')


main()

```

2、执行脚本进行转换

```
cd d:\tensorflow\my_test
python xml_to_csv.py
```

看到成功提示说明转换成功，两个目录的xml信息将通过脚本转换为train_labels.csv和test_labels.csv两个文件。



#### 将.csv文件转换成TFRecord文件

正常情况下我们训练文件夹经常会生成 train, test 或者val文件夹，这些文件夹内部往往会存着成千上万的图片或文本等文件，这些文件被散列存着，这样不仅占用磁盘空间，并且再被一个个读取的时候会非常慢，繁琐。占用大量内存空间（有的大型数据不足以一次性加载）。

使用TFRecord格式的文件存储形式会很合理的帮我们存储数据。TFRecord内部使用了“Protocol Buffer”二进制数据编码方案，它只占用一个内存块，只需要一次性加载一个二进制文件的方式即可，简单，快速，尤其对大型训练数据很友好。而且当我们的训练数据量比较大的时候，可以将数据分成多个TFRecord文件，来提高处理效率。

1、在图片的上级目录中创建 “generate_tfrecord.py” 代码脚本（“D:\tensorflow\my_test\generate_tfrecord.py”），代码内容如下（具体要处理的路径和目录可根据需要自行修改）：

```
"""
Usage:
  # From tensorflow/models/
  # Create train data:
  python generate_tfrecord.py --csv_input=images/train_labels.csv --image_dir=images/train --output_path=train.record

  # Create test data:
  python generate_tfrecord.py --csv_input=images/test_labels.csv  --image_dir=images/test --output_path=test.record
"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
import pandas as pd
import tensorflow as tf

from PIL import Image
from object_detection.utils import dataset_util
from collections import namedtuple, OrderedDict

flags = tf.app.flags
flags.DEFINE_string('csv_input', '', 'Path to the CSV input')
flags.DEFINE_string('image_dir', '', 'Path to the image directory')
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
FLAGS = flags.FLAGS


# TO-DO replace this with label map
def class_text_to_int(row_label):
    """
    将分类名转换成对应的映射int值

    @param {str} row_label - 分类名
    @returns {int} - int值
    """
    if row_label == 'nine':
        return 1
    elif row_label == 'ten':
        return 2
    elif row_label == 'jack':
        return 3
    elif row_label == 'queen':
        return 4
    elif row_label == 'king':
        return 5
    elif row_label == 'ace':
        return 6
    else:
        None


def split(df, group):
    """
    对csv记录按group标签进行分组

    @param {TextFileReader} df - 打开的csv文件内容
    @param {str} group - 分组标签

    @returns {list} - namedtuple对象的数组
        [(filename, )]
    """
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)  # 按传入的group进行分组处理
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def create_tf_example(group, path):
    # with tf.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
    with tf.io.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = group.filename.encode('utf8')
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        xmins.append(row['xmin'] / width)
        xmaxs.append(row['xmax'] / width)
        ymins.append(row['ymin'] / height)
        ymaxs.append(row['ymax'] / height)
        classes_text.append(row['class'].encode('utf8'))
        classes.append(class_text_to_int(row['class']))

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example


def main(_):
    # 创建TFRecord生成器，保存文件由output_path参数定义
    # writer = tf.python_io.TFRecordWriter(FLAGS.output_path)
    writer = tf.io.TFRecordWriter(FLAGS.output_path)

    # 获取由image_dir定义的图片文件所在目录
    path = os.path.join(os.getcwd(), FLAGS.image_dir)

    # 通过pandas读取csv文件，所读取的csv文件由csv_input参数定义
    examples = pd.read_csv(FLAGS.csv_input)

    # 按filename进行分组
    grouped = split(examples, 'filename')

    # 按filename分组生成样本Example并写入TFRecord生成器
    for group in grouped:
        tf_example = create_tf_example(group, path)
        writer.write(tf_example.SerializeToString())

    writer.close()
    output_path = os.path.join(os.getcwd(), FLAGS.output_path)
    print('Successfully created the TFRecords: {}'.format(output_path))


if __name__ == '__main__':
    # tf.app.run()
    tf.compat.v1.app.run()

```

2、执行以下脚本对每个csv文件及图片文件目录处理成TFRecord文件

```
cd d:\tensorflow\my_test
python generate_tfrecord.py --csv_input=train_labels.csv --image_dir=train --output_path=train.record
python generate_tfrecord.py --csv_input=test_labels.csv  --image_dir=test --output_path=test.record
```

看到成功提示说明转换成功，训练图片和测试图片信息转换为train.record和test.record两个文件。



#### 选择及配置训练模型

该API为已经提供了很多的预训练的模型，可以在github地址中下载已预训练的模型：https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md

<img src="TensorFlow%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2%E5%8F%8A%E7%AE%80%E5%8D%95%E5%BA%94%E7%94%A8-Python.assets/image-20200516081043437.png" alt="image-20200516081043437" style="zoom: 33%;" />

注：各领域机器学习数据集汇总：https://blog.csdn.net/lingpy/article/details/79918345?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-2.nonecase&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-2.nonecase



可以根据具体效果要求（例如识别精度及速度等）选择合适的模型，这个案例中我们选择faster_rcnn_inception_v2_coco这个模型。

1、在“D:\tensorflow\my_test\training” 创建分类映射文件 labelmap.pbtxt（“D:\tensorflow\my_test\training\labelmap.pbtxt”），该文件用于设置分类名和int的映射关系，文件内容如下：

```
item {
  id: 1
  name: 'nine'
}

item {
  id: 2
  name: 'ten'
}

item {
  id: 3
  name: 'jack'
}

item {
  id: 4
  name: 'queen'
}

item {
  id: 5
  name: 'king'
}

item {
  id: 6
  name: 'ace'
}
```

2、我们准备不用预训练好的模型，所以不用下载，可以从之前安装的路径中获取对应的配置文件（D:\tensorflow\models\research\object_detection\samples\configs）：faster_rcnn_inception_v2_coco.config。

将该文件复制至 “D:\tensorflow\my_test\training” 路径中，然后按以下中文注释的点进行修改

```
# Faster R-CNN with Inception v2, configuration for MSCOCO Dataset.
# Users should configure the fine_tune_checkpoint field in the train config as
# well as the label_map_path and input_path fields in the train_input_reader and
# eval_input_reader. Search for "PATH_TO_BE_CONFIGURED" to find the fields that
# should be configured.

# 模型设置
# 定义了什么类型的模型，比如说选择SSD/FASTER RCNN/RFCN等模型，什么特征提取器
# 简单的说就是我们平常在代码中写的关于模型的配置参数“挪到”了这个配置文件中，让代码不那么”冗余”
model {
  faster_rcnn {
    # 修改分类数量，示例为6个
    num_classes: 6
    image_resizer {
      keep_aspect_ratio_resizer {
        min_dimension: 600
        max_dimension: 1024
      }
    }
    feature_extractor {
      type: 'faster_rcnn_inception_v2'
      first_stage_features_stride: 16
    }
    first_stage_anchor_generator {
      grid_anchor_generator {
        scales: [0.25, 0.5, 1.0, 2.0]
        aspect_ratios: [0.5, 1.0, 2.0]
        height_stride: 16
        width_stride: 16
      }
    }
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
  }
}

# 决定应使用哪些参数来训练模型参数（即SGD参数，输入的张量需要哪些预处理和怎么初始化特征提取器-卷积核的值）
train_config: {
  # 批大小，在深度学习中，一般采用SGD训练，即每次训练在训练集中取batchsize个样本训练
  batch_size: 1
  optimizer {
    momentum_optimizer: {
      learning_rate: {
        manual_step_learning_rate {
          initial_learning_rate: 0.0002
          schedule {
            step: 900000
            learning_rate: .00002
          }
          schedule {
            step: 1200000
            learning_rate: .000002
          }
        }
      }
      momentum_optimizer_value: 0.9
    }
    use_moving_average: false
  }
  gradient_clipping_by_norm: 10.0
  # 从头开始训练目标检测器可能需要数天时间。为了加快训练过程，建议用户重新使用先前在目标分类或检测的checkpoint保存好的参数；如果不需要预训练结果而重新训练模型，可屏蔽掉fine_tune_checkpoint参数
  # fine_tune_checkpoint: "PATH_TO_BE_CONFIGURED/model.ckpt"
  # from_detection_checkpoint: true
  # fine_tune_checkpoint: "D:/tensorflow/my_test/model.ckpt"
  from_detection_checkpoint: false
  # Note: The below line limits the training process to 200K steps, which we
  # empirically found to be sufficient enough to train the COCO dataset. This
  # effectively bypasses the learning rate schedule (the learning rate will
  # never decay). Remove the below line to train indefinitely.
  num_steps: 200000
  data_augmentation_options {
    random_horizontal_flip {
    }
  }
}

# 定义了模型中的训练集
train_input_reader: {
  tf_record_input_reader {
    # 设置输入的训练记录集文件
    input_path: "D:/tensorflow/my_test/train.record"
  }
  # 设置分类名映射文件
  label_map_path: "D:/tensorflow/my_test/training/labelmap.pbtxt"
}

# 决定了什么样的指标将在报告被用来评估（目前只支持PASCAL VOC指标）
eval_config: {
  num_examples: 8000
  # Note: The below line limits the evaluation process to 10 evaluations.
  # Remove the below line to evaluate indefinitely.
  max_evals: 10
}

# 定义了模型中的测试集
eval_input_reader: {
  tf_record_input_reader {
    # 设置测试的记录集文件
    input_path: "D:/tensorflow/my_test/test.record"
  }
  # 设置分类名映射文件
  label_map_path: "D:/tensorflow/my_test/training/labelmap.pbtxt"
  # shuffle表示是否随机选取测试图片
  shuffle: false
  num_readers: 1
}
```

#### 训练模型

执行以下命令进行模型的训练：

Windows版本的命令：

```
cd d:\tensorflow\models\research\object_detection
python model_main.py --logtostderr --model_dir=D:/tensorflow/my_test/training/ --pipeline_config_path=D:/tensorflow/my_test/training/faster_rcnn_inception_v2_coco.config
```

ubuntu版本的命令：

```
conda activate tensorflow

cd /home/ubuntu18/models-1.13.0/research/object_detection

# 启动机器训练
nohup python model_main.py --logtostderr --model_dir=/home/ubuntu18/tensorflow-test/poker/training/ --pipeline_config_path=/home/ubuntu18/tensorflow-test/poker/training/faster_rcnn_inception_v2_coco.config &

# 实时查看命令输出结果
tail -f nohup.out
```

**注：训练过程中可随时中断训练，重新启动训练会从中断的点继续执行，由于训练时间会比较长，我们可以在执行一定步数后就中断训练分析准确率，发现准确率过低可以继续执行。**



执行过程中可能会出现以下问题：

**问题1：找不到ckpt文件**

错误信息大致为：tensorflow.python.framework.errors_impl.NotFoundError: Unsuccessful TensorSliceReader constructor: Failed to find any matching files for D:/tensorflow/my_test/model.ckpt

原因：指定了fine_tune_checkpoint参数，但找不到参数指定的预训练中断点信息文件。

解决方法：配置正确的预训练中断点信息文件（包括的文件：checkpoint、.data-xx-of-xx、.index、.meta）；或者使用# 屏蔽掉该参数。



**问题2：Cannot add tensor to the batch**

错误信息大致为：tensorflow.python.framework.errors_impl.InvalidArgumentError: Cannot add tensor to the batch: number of elements does not match. Shapes are: [tensor]: [576,1024,3], [batch]: [800,600,3]

原因：可能是batch_size的配置与所训练的数量不匹配，如果要避免该问题。

解决方法：将参数设置为1，或合适的批次。



**问题3：object of type <class 'numpy.float64'> cannot be safely interpreted as an integer**

错误信息大致为： Invalid argument: TypeError: object of type <class 'numpy.float64'> cannot be safely interpreted as an integer.

原因：可能是由于你所安装的tensorflow和numpy版本不兼容导致，版本兼容性参考如下：

| tensorflow | numpy  |
| ---------- | ------ |
| 2.0.0      | 1.16.4 |
| 1.14       | 1.16.0 |
| 1.12       | 1.15.4 |
| 1.8.0      | 1.14.5 |

解决方法：将numpy升级或降级到可兼容的版本，例如本例：

```
pip install -U -i https://pypi.tuna.tsinghua.edu.cn/simple numpy==1.16.0
```



#### 导出模型检测器（Inference Graph）

模型训练完成后，接下来就是导出frozen_inference_graph.pb文件，该文件中包含了我们训练好的检测器以及网络架构信息和参数信息等。

执行以下命令：

Windows:

```
cd d:\tensorflow\models\research\object_detection
python export_inference_graph.py --input_type image_tensor --pipeline_config_path D:/tensorflow/my_test/training/faster_rcnn_inception_v2_coco.config --trained_checkpoint_prefix D:/tensorflow/my_test/training/model.ckpt-1347 --output_directory D:/tensorflow/my_test/export
```

Ubuntu：

```
cd /home/ubuntu18/models-1.13.0/research/object_detection
python export_inference_graph.py --input_type image_tensor --pipeline_config_path /home/ubuntu18/tensorflow-test/poker/training/faster_rcnn_inception_v2_coco.config --trained_checkpoint_prefix /home/ubuntu18/tensorflow-test/poker/training/model.ckpt-200000 --output_directory /home/ubuntu18/tensorflow-test/poker/export
```

- pipeline_config_path 传入的是训练所用的config文件
- trained_checkpoint_prefix 传入checkpoint文件的路径以及对应的训练点文件，例如我是中间中断了训练，文件夹里最大的checkpoint文件步数是1347，因此选择这个中断点生成
- output_directory 传入模型导出的文件路径



#### 测试训练好的检测器

我们从网上找一张扑克的照片对检测器进行测试，创建一个测试的python文件（D:\tensorflow\my_test\object_detection_image.py），代码如下：

```
######## Image Object Detection Using Tensorflow-trained Classifier #########
#
# Author: Evan Juras
# Date: 1/15/18
# Description:
# This program uses a TensorFlow-trained neural network to perform object detection.
# It loads the classifier and uses it to perform object detection on an image.
# It draws boxes, scores, and labels around the objects of interest in the image.

# Some of the code is copied from Google's example at
# https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb

# and some is copied from Dat Tran's example at
# https://github.com/datitran/object_detector_app/blob/master/object_detection_app.py

# but I changed it to make it more understandable to me.

# Import packages
import os
import cv2
import numpy as np
import tensorflow as tf
import sys

# This is needed since the notebook is stored in the object_detection folder.
# 在python的搜索路径增加object_detection的安装路径
sys.path.append("d:/tensorflow/models/research/object_detection")

# Import utilites
from utils import label_map_util
from utils import visualization_utils as vis_util

# Name of the directory containing the object detection module we're using
# MODEL_NAME = 'export'
# 指定导出的模型文件frozen_inference_graph.pb所在的路径
MODEL_NAME = 'export/ubuntu'
# 测试图片名称
IMAGE_NAME = 'test1.jpg'

# Grab path to current working directory
CWD_PATH = os.getcwd()

# Path to frozen detection graph .pb file, which contains the model that is used
# for object detection.
PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME, 'frozen_inference_graph.pb')

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH, 'training', 'labelmap.pbtxt')

# Path to image
PATH_TO_IMAGE = os.path.join(CWD_PATH, IMAGE_NAME)

# Number of classes the object detector can identify
NUM_CLASSES = 6

# Load the label map.
# Label maps map indices to category names, so that when our convolution
# network predicts `5`, we know that this corresponds to `king`.
# Here we use internal utility functions, but anything that returns a
# dictionary mapping integers to appropriate string labels would be fine
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(
    label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# Load the Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.Session(graph=detection_graph)

# Define input and output tensors (i.e. data) for the object detection classifier

# Input tensor is the image
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# Output tensors are the detection boxes, scores, and classes
# Each box represents a part of the image where a particular object was detected
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

# Each score represents level of confidence for each of the objects.
# The score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

# Number of objects detected
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

# Load image using OpenCV and
# expand image dimensions to have shape: [1, None, None, 3]
# i.e. a single-column array, where each item in the column has the pixel RGB value
image = cv2.imread(PATH_TO_IMAGE)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image_expanded = np.expand_dims(image_rgb, axis=0)

# Perform the actual detection by running the model with the image as input
(boxes, scores, classes, num) = sess.run(
    [detection_boxes, detection_scores, detection_classes, num_detections],
    feed_dict={image_tensor: image_expanded})

# Draw the results of the detection (aka 'visulaize the results')

vis_util.visualize_boxes_and_labels_on_image_array(
    image,
    np.squeeze(boxes),
    np.squeeze(classes).astype(np.int32),
    np.squeeze(scores),
    category_index,
    use_normalized_coordinates=True,
    line_thickness=8,
    min_score_thresh=0.40)

# All the results have been drawn on image. Now display the image.
cv2.imshow('Object detector', image)

# Press any key to close the image
cv2.waitKey(0)

# Clean up
cv2.destroyAllWindows()
```



执行测试代码得到图形展示的识别输出：

```
cd D:\tensorflow\my_test
python object_detection_image.py
```



输出结果如下图（只执行了1347步训练的模型，识别率很差）：

![image-20200517164857410](TensorFlow%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2%E5%8F%8A%E7%AE%80%E5%8D%95%E5%BA%94%E7%94%A8-Python.assets/image-20200517164857410.png)

（完成了200000步训练的模型，识别率相对高一点）

![image-20200530073252920](TensorFlow%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2%E5%8F%8A%E7%AE%80%E5%8D%95%E5%BA%94%E7%94%A8-Python.assets/image-20200530073252920.png)



#### 使用TensorBoard监控或查看训练情况

执行以下命令打开tensorboard，其中需指定日志路径为训练路径

```
cd D:/tensorflow/my_test/training
tensorboard --logdir=D:/tensorflow/my_test/training
```



执行后，可以通过浏览器打开TensorBoard地址（http://localhost:6006/）查看训练情况，注意如果通过主机名无法访问，需要自行修改为本机地址：

![image-20200517172721804](TensorFlow%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2%E5%8F%8A%E7%AE%80%E5%8D%95%E5%BA%94%E7%94%A8-Python.assets/image-20200517172721804.png)

![image-20200517172553520](TensorFlow%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2%E5%8F%8A%E7%AE%80%E5%8D%95%E5%BA%94%E7%94%A8-Python.assets/image-20200517172553520.png)