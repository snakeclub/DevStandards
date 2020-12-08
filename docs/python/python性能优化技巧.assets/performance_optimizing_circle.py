#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
性能优化示例-循环
@module performance_optimizing_circle
@file performance_optimizing_circle.py
"""

import datetime


DOT_RANGE_NUM = 10000000

DOT_WORDS = [
    'test', 'for', 'circle', 'performance', 'optimizing', 'dot'
]


def dot_in_circle():
    _str = ''
    for _i in range(DOT_RANGE_NUM):
        _str = DOT_WORDS[_i % len(DOT_WORDS)].upper()
    return _str


def dot_out_circle():
    _str = ''
    _upper = str.upper
    for _i in range(DOT_RANGE_NUM):
        _str = _upper(DOT_WORDS[_i % len(DOT_WORDS)])
    return _str


def var_out_circle():
    _str = ''
    _upper = str.upper
    _len = len(DOT_WORDS)
    for _i in range(DOT_RANGE_NUM):
        _str = _upper(DOT_WORDS[_i % _len])
    return _str


if __name__ == '__main__':
    # 循环内有"."操作
    _start = datetime.datetime.now()
    dot_in_circle()
    _end = datetime.datetime.now()
    print('dot_in_circle time: %s' % str((_end - _start).total_seconds()))

    # 循环内无"."操作
    _start = datetime.datetime.now()
    dot_out_circle()
    _end = datetime.datetime.now()
    print('dot_out_circle time: %s' % str((_end - _start).total_seconds()))

    # 变量计算移出循环
    _start = datetime.datetime.now()
    var_out_circle()
    _end = datetime.datetime.now()
    print('var_out_circle time: %s' % str((_end - _start).total_seconds()))
