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
