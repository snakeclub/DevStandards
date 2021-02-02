# TensorFlow-自定义训练模型案例

## 执行前提

可以使用 Anaconda3 搭建独立的虚拟环境，执行命令如下：

```
conda create -n tf2 python=3.7.3
conda activate tf2
pip install -i https://mirrors.aliyun.com/pypi/simple/ tensorflow-cpu==2.4.0
pip install -i https://mirrors.aliyun.com/pypi/simple/ matplotlib
```

设置VSCode的Python目录，设定为虚拟环境：

1、通过菜单打开配置页 “file => preferences => setting”；

2、搜索配置项 “python.pythonPath”；

3、把配置项的值从默认的 “python” 修改为虚拟环境的路径，例如 “C:\Users\74143\.conda\envs\tf2”。

**注：如果需要切换为base环境，该配置需修改回 “C:\Users\74143\AppData\Local\Programs\Python\Python37\”**



## 自定义训练模型初阶 - 拟合一个线性模型

本案例以一个简单线性模型的训练来演示机器学习的步骤和原理，里面并没有用到太多TF的高阶API，因此并不支持形成标准冻结模型。

完整代码见：[customize_linear_model.py](TensorFlow-%E8%87%AA%E5%AE%9A%E4%B9%89%E8%AE%AD%E7%BB%83%E6%A8%A1%E5%9E%8B%E6%A1%88%E4%BE%8B.assets/customize_linear_model.py)

**1、定义要训练的模型**

```
class LinearModel(object):
    """
    自定义的线性模型 f(x) = W*x + b
    """

    def __init__(self):
        """
        初始化模型的两个变量W、b为(5.0, 0.0)
        在训练中，这两个变量应该初始化为随机值
        """
        self.W = tf.Variable(5.0)
        self.b = tf.Variable(0.0)

    def __call__(self, x):
        """
        模型调用函数

        @param {float} x - 模型入输入x

        @returns {float} - 模型输出f(x)
        """
        return self.W * x + self.b
```

该模型求解 f(x) = W*x + b 线性函数两个权重变量 W、b的最优解，通过训练数据[inputs_x, outputs_y]得到 W、b的近似最优值后，即可通过模型函数对新的输入 x 得到预测结果 y 。

**2、定义损失计算函数**

```
def loss(predicted_y, desired_y):
    """
    损失计算函数
    注：使用标准的L2损失(平方损失)

    @param {float} predicted_y - 预测值
    @param {float} desired_y - 期望值
    """
    # reduce_mean 用于计算张量tensor沿着指定的数轴（tensor的某一维度）上的平均值
    return tf.reduce_mean(tf.square(predicted_y - desired_y))
```

损失函数用于测量给定的训练输入所得到的模型输出与期望输出的匹配程度，这里我们使用标准的L2损失函数。

L2均方误差（MSE）是回归损失函数中最常用的误差，它是预测值与目标值之间差值的平方和，其公式如下所示：

![img](TensorFlow-%E8%87%AA%E5%AE%9A%E4%B9%89%E8%AE%AD%E7%BB%83%E6%A8%A1%E5%9E%8B%E6%A1%88%E4%BE%8B.assets/v2-bf6d99de6c4717f6ecf12c4f71156fc1_1440w.jpg)

**3、定义训练函数**

```
def train(model, inputs, outputs, learning_rate):
    """
    训练函数

    @param {LinearModel} model - 要训练的模型
    @param {tuple[float]} inputs - 训练输入数组
    @param {tuple[float]} outputs - 训练期望输出数组
    @param {float} learning_rate - 学习率
    """
    with tf.GradientTape() as t:
        current_loss = loss(model(inputs), outputs)  # 计算当前的损失值(loss)
        dW, db = t.gradient(current_loss, [model.W, model.b])  # 利用梯度带计算输出梯度
        # 按梯度(变化方向)和学习率改变变量值
        model.W.assign_sub(learning_rate * dW)
        model.b.assign_sub(learning_rate * db)

```

该训练函数每次使用全部训练数据，计算当前权重变量（W和b）得到的损失率，并使用TF提供的梯度带（GradientTape）求出变量数组的梯度方向（即切线，沿着梯度方向具有最大变化率，因此应该沿着负梯度方向减少函数值来得到优化目标），基于梯度方向更新模型的权重变量（W 和 b）来尝试减少损失。

**注：在`tf.train.Optimizer`实现中拥有许多梯度下降方案的变体，平常强烈建议使用这些实现，而不是自己实现。**

**4、生成训练数据**

```
def create_dataset():
    """
    根据已知结果生成训练数据，并加上一些干扰

    @returns {tuple} - 返回训练的 输入/输出 数组
    """
    TRUE_W = 3.0
    TRUE_b = 2.0
    NUM_EXAMPLES = 1000

    inputs = tf.random.normal(shape=[NUM_EXAMPLES])  # 随机生成输入数组
    noise = tf.random.normal(shape=[NUM_EXAMPLES])  # 产生干扰数组
    outputs = inputs * TRUE_W + TRUE_b + noise  # 得到输出结果

    return inputs, outputs
```

在这里根据已知的模型函数，随机生成1000个训练数据集，同时利用随机数增加干扰。

**5、执行训练**

```
Ws, bs = [], []  # 记录变量的变化情况
epochs = range(10)  # 指定训练10次
for epoch in epochs:
    Ws.append(model.W.numpy())
    bs.append(model.b.numpy())
    current_loss = loss(model(inputs), outputs)

    train(model, inputs, outputs, learning_rate=0.1)
    print('Epoch %2d: W=%1.2f b=%1.2f, loss=%2.5f' %
          (epoch, Ws[-1], bs[-1], current_loss))
```

下图为执行前模型变量所处的位置，其中蓝色为最优期望结果，红色为当前模型的预测情况：

<img src="TensorFlow-%E8%87%AA%E5%AE%9A%E4%B9%89%E8%AE%AD%E7%BB%83%E6%A8%A1%E5%9E%8B%E6%A1%88%E4%BE%8B.assets/image-20210108103827697.png" alt="image-20210108103827697" style="zoom:50%;" />

下午为训练执行过程中，模型权重变量W和b的演变过程：

<img src="TensorFlow-%E8%87%AA%E5%AE%9A%E4%B9%89%E8%AE%AD%E7%BB%83%E6%A8%A1%E5%9E%8B%E6%A1%88%E4%BE%8B.assets/image-20210108103913308.png" alt="image-20210108103913308" style="zoom:50%;" />

## 自定义训练模型中阶 - 使用Keras构建模型 

Keras 是一个用于构建和训练深度学习模型的高阶API。它可用于快速设计原型、高级研究和生产，具有以下三个主要优势：

- 方便用户使用：Keras 具有针对常见用例做出优化的简单而一致的界面。它可针对用户错误提供切实可行的清晰反馈。
- 模块化和可组合：将可配置的构造块连接在一起就可以构建 Keras 模型，并且几乎不受限制。
- 易于扩展：可以编写自定义构造块以表达新的研究创意，并且可以创建新层、损失函数并开发先进的模型。

本案例使用TensorFlow标准教程中的鸢尾花分类问题进行说明（官方教程地址：https://tensorflow.google.cn/tutorials/customization/custom_training_walkthrough）

完整代码见：[customize_keras_model.py](TensorFlow-%E8%87%AA%E5%AE%9A%E4%B9%89%E8%AE%AD%E7%BB%83%E6%A8%A1%E5%9E%8B%E6%A1%88%E4%BE%8B.assets/customize_keras_model.py)

### 鸢尾花分类问题

想象一下，您是一名植物学家，正在寻找一种能够对所发现的每株鸢尾花进行自动归类的方法。机器学习可提供多种从统计学上分类花卉的算法。例如，一个复杂的机器学习程序可以根据照片对花卉进行分类。我们的要求并不高 - 我们将根据鸢尾花花萼和花瓣的长度和宽度对其进行分类。

鸢尾属约有 300 个品种，但我们的程序将仅对下列三个品种进行分类：

- 山鸢尾
- 维吉尼亚鸢尾
- 变色鸢尾

| ![Petal geometry compared for three iris species: Iris setosa, Iris virginica, and Iris versicolor](TensorFlow-%E8%87%AA%E5%AE%9A%E4%B9%89%E8%AE%AD%E7%BB%83%E6%A8%A1%E5%9E%8B%E6%A1%88%E4%BE%8B.assets/iris_three_species.jpg) |
| ------------------------------------------------------------ |
| **Figure 1.** [山鸢尾](https://commons.wikimedia.org/w/index.php?curid=170298) (by [Radomil](https://commons.wikimedia.org/wiki/User:Radomil), CC BY-SA 3.0), [变色鸢尾](https://commons.wikimedia.org/w/index.php?curid=248095), (by [Dlanglois](https://commons.wikimedia.org/wiki/User:Dlanglois), CC BY-SA 3.0), and [维吉尼亚鸢尾](https://www.flickr.com/photos/33397993@N05/3352169862) (by [Frank Mayfield](https://www.flickr.com/photos/33397993@N05), CC BY-SA 2.0). |

### 处理训练数据集

有人已经创建了一个包含有花萼和花瓣的测量值的[120 株鸢尾花的数据集](TensorFlow-%E8%87%AA%E5%AE%9A%E4%B9%89%E8%AE%AD%E7%BB%83%E6%A8%A1%E5%9E%8B%E6%A1%88%E4%BE%8B.assets/iris_training.csv)。这是一个在入门级机器学习分类问题中经常使用的经典数据集。

该数据集是一个csv格式的文件，内容如下：

```
120,4,setosa,versicolor,virginica
6.4,2.8,5.6,2.2,2
5.0,2.3,3.3,1.0,1
4.9,2.5,4.5,1.7,2
4.9,3.1,1.5,0.1,0
...
```

第一行说明数据集信息，总共有120个数据（每行一个数据），每个数据有4个特征值（前4列），最后一列为分类，0 - setosa， 1 - versicolor， 2 - virginica

我们通过以下代码可以创建相应的训练数据集：

```
train_dataset_fp = 'iris_training.csv'  # 数据集文件

# CSV文件中列的顺序
column_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']
label_name = column_names[-1]  # 分类列名

# 从csv文件创建数据集
batch_size = 32
train_dataset = tf.data.experimental.make_csv_dataset(
    train_dataset_fp,
    batch_size,
    column_names=column_names,
    label_name=label_name,
    num_epochs=1)

# 定义函数以将特征字典重新打包为形状为 (batch_size, num_features) 的单个数组
def pack_features_vector(features, labels):
    """将特征打包到一个数组中"""
    features = tf.stack(list(features.values()), axis=1)
    return features, labels

# 将每个 (features, label) 对中的 features 打包到训练数据集中
train_dataset = train_dataset.map(pack_features_vector)
```

每个步骤说明如下：

1、tf.data.experimental.make_csv_dataset 从csv文件中加载数据，获得 (features, label) 对所构建的 [`tf.data.Dataset`](https://tensorflow.google.cn/api_docs/python/tf/data/Dataset)  对象，需注意的是每 32 个（batch_size）随机数据形成一个  (features, label) 对，其中 features 是一个有序字典: `{'feature_name': value}`。我们看一下 features 的格式：

```
OrderedDict([('sepal_length', <tf.Tensor: shape=(32,), dtype=float32, numpy=
array([6.6, 5.8, 5. , 7.7, 4.6, 4.7, 5.5, 6.1, 6.5, 6.1, 5. , 6.4, 5.4,

       6. , 5.5, 7.2, 5.9, 6.4, 5. , 5.2, 5. , 6.4, 6.2, 5.1, 6.4, 5.8,
       5.1, 6.3, 6.5, 4.9, 7.4, 5.7], dtype=float32)>), ('sepal_width', <tf.Tensor: shape=(32,), dtype=float32, numpy=
array([2.9, 2.7, 3.4, 2.6, 3.1, 3.2, 2.4, 2.9, 3. , 2.6, 3.5, 3.1, 3.9,
       3. , 2.4, 3.6, 3.2, 3.2, 3.2, 3.5, 2.3, 2.7, 3.4, 3.8, 2.8, 2.6,
       2.5, 3.3, 3. , 3.1, 2.8, 3.8], dtype=float32)>), ('petal_length', <tf.Tensor: shape=(32,), dtype=float32, numpy=
array([4.6, 4.1, 1.5, 6.9, 1.5, 1.6, 3.8, 4.7, 5.5, 5.6, 1.6, 5.5, 1.7,
       4.8, 3.7, 6.1, 4.8, 4.5, 1.2, 1.5, 3.3, 5.3, 5.4, 1.9, 5.6, 4. ,
       3. , 6. , 5.8, 1.5, 6.1, 1.7], dtype=float32)>), ('petal_width', <tf.Tensor: shape=(32,), dtype=float32, numpy=
array([1.3, 1. , 0.2, 2.3, 0.2, 0.2, 1.1, 1.4, 1.8, 1.4, 0.6, 1.8, 0.4,
       1.8, 1. , 2.5, 1.8, 1.5, 0.2, 0.2, 1. , 1.9, 2.3, 0.4, 2.2, 1.2,
       1.1, 2.5, 2.2, 0.1, 1.9, 0.3], dtype=float32)>)])
```

2、需要通过 map 函数将数据集转换为形状为 `(batch_size, num_features)` 的单个数组形式，这里用到了 pack_features_vector 函数，将 features 组合为指定维度的数组集合，转换后 features 的格式变换为：

```
tf.Tensor(
[[5.  3.5 1.3 0.3]
 [4.8 3.1 1.6 0.2]
 [6.3 2.7 4.9 1.8]
 [7.4 2.8 6.1 1.9]
 [5.  3.2 1.2 0.2]
 ...
 ], shape=(32, 4), dtype=float32)
```

