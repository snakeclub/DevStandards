#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
import matplotlib.pyplot as plt

# 定义模型


class LinearModel(object):
    """
    自定义的线性模型 f(x) = W*x + b
    """

    def __init__(self):
        """
        初始化模型的两个变量W、b为(6.0, 0.0)
        在训练中，这两个变量应该初始化为随机值
        """
        self.W = tf.Variable(6.0)
        self.b = tf.Variable(0.0)

    def __call__(self, x):
        """
        模型调用函数

        @param {float} x - 模型入输入x

        @returns {float} - 模型输出f(x)
        """
        return self.W * x + self.b


# 定义损失计算函数
def loss(predicted_y, desired_y):
    """
    损失计算函数
    注：使用标准的L2损失(平方损失)

    @param {float} predicted_y - 预测值
    @param {float} desired_y - 期望值
    """
    # reduce_mean 用于计算张量tensor沿着指定的数轴（tensor的某一维度）上的平均值
    return tf.reduce_mean(tf.square(predicted_y - desired_y))


# 定义训练函数
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


# 生成训练数据
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


def show_dataset(model, inputs, outputs):
    """
    显示当前模型变量所处位置

    @param {LinearModel} model - 模型对象
    @param {tuple[float]} inputs - 训练输入数组
    @param {tuple[float]} outputs - 训练期望输出数组
    """
    plt.scatter(inputs, outputs, c='b')
    plt.scatter(inputs, model(inputs), c='r')
    plt.show()
    print('Current loss: ', loss(model(inputs), outputs).numpy())


if __name__ == '__main__':
    # 当程序自己独立运行时执行的操作
    model = LinearModel()  # 初始化模型
    inputs, outputs = create_dataset()  # 生成训练数据
    show_dataset(model, inputs, outputs)  # 显示模型当前位置

    # 执行训练
    Ws, bs = [], []  # 记录变量的变化情况
    epochs = range(10)  # 指定训练10次
    for epoch in epochs:
        Ws.append(model.W.numpy())
        bs.append(model.b.numpy())
        current_loss = loss(model(inputs), outputs)

        train(model, inputs, outputs, learning_rate=0.1)
        print('Epoch %2d: W=%1.2f b=%1.2f, loss=%2.5f' %
              (epoch, Ws[-1], bs[-1], current_loss))

    # 显示训练过程中W和b变化
    plt.plot(epochs, Ws, 'r',
             epochs, bs, 'b')
    plt.plot([3.0] * len(epochs), 'r--',
             [2.0] * len(epochs), 'b--')
    plt.legend(['W', 'b', 'true W', 'true_b'])
    plt.show()
