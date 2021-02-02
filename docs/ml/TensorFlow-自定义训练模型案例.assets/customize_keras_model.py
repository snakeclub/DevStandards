#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import matplotlib.pyplot as plt
import tensorflow as tf

print("TensorFlow version: {}".format(tf.__version__))
print("Eager execution: {}".format(tf.executing_eagerly()))


# 创建训练数据集
def create_dataset():
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

    return train_dataset
