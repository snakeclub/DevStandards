#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
性能优化示例 - numba
@module performance_optimizing_numba
@file performance_optimizing_numba.py
"""


import datetime
import math
import random
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from numba import jit, prange
try:
    from matplotlib.pylab import imshow, show
    have_mpl = True
except ImportError:
    have_mpl = False


# 使用numpy库创建图片
def mandel_no_jit(x, y, max_iters):
    """
    Given the real and imaginary parts of a complex number,
    determine if it is a candidate for membership in the Mandelbrot
    set given a fixed number of iterations.
    """
    i = 0
    c = complex(x, y)
    z = 0.0j
    for i in range(max_iters):
        z = z * z + c
        if (z.real * z.real + z.imag * z.imag) >= 4:
            return i

    return 255


def create_fractal_no_jit(min_x, max_x, min_y, max_y, image, iters):
    height = image.shape[0]
    width = image.shape[1]

    pixel_size_x = (max_x - min_x) / width
    pixel_size_y = (max_y - min_y) / height
    for x in range(width):
        real = min_x + x * pixel_size_x
        for y in range(height):
            imag = min_y + y * pixel_size_y
            color = mandel_no_jit(real, imag, iters)
            image[y, x] = color

    return image


@jit(nopython=True)
def mandel(x, y, max_iters):
    """
    Given the real and imaginary parts of a complex number,
    determine if it is a candidate for membership in the Mandelbrot
    set given a fixed number of iterations.
    """
    i = 0
    c = complex(x, y)
    z = 0.0j
    for i in range(max_iters):
        z = z * z + c
        if (z.real * z.real + z.imag * z.imag) >= 4:
            return i

    return 255


@jit(nopython=True)
def create_fractal(min_x, max_x, min_y, max_y, image, iters):
    height = image.shape[0]
    width = image.shape[1]

    pixel_size_x = (max_x - min_x) / width
    pixel_size_y = (max_y - min_y) / height
    for x in range(width):
        real = min_x + x * pixel_size_x
        for y in range(height):
            imag = min_y + y * pixel_size_y
            color = mandel(real, imag, iters)
            image[y, x] = color

    return image


# python循环计算
def foo_no_jit(range_num):
    s = 0
    for i in range(range_num):
        s += i
    return s


@jit(nopython=True)
def foo(range_num):
    s = 0
    for i in range(range_num):
        s += i
    return s


def foo_while_no_jit(range_num):
    s = 0
    i = 0
    while i < range_num:
        s += i
        i += 1
    return s


@jit(nopython=True)
def foo_while(range_num):
    s = 0
    i = 0
    while i < range_num:
        s += i
        i += 1
    return s


# 使用nogil提升多线程处理
# 第一个 kernel，nogil 参数设为了 False
@jit(nopython=True, nogil=False)
def nogil_disable(result, a, b):
    """
    关闭nogil

    @param {np.ndarray} result - 获取结果的数组
    @param {np.ndarray} a - 入参a数组
    @param {np.ndarray} b - 入参b数组
    """
    for i in range(len(result)):
        result[i] = 1 / (a[i] + math.exp(-b[i]))

# 第二个 kernel，nogil 参数设为了 True
@jit(nopython=True, nogil=True)
def nogil_enable(result, a, b):
    """
    启用nogil

    @param {np.ndarray} result - 获取结果的数组
    @param {np.ndarray} a - 入参a数组
    @param {np.ndarray} b - 入参b数组
    """
    for i in range(len(result)):
        result[i] = 1 / (a[i] + math.exp(-b[i]))


def make_single_task(kernel):
    """
    创建单线程任务

    @param {function} kernel - 传入执行计算的函数
    """
    def func(length, *args):
        result = np.empty(length, dtype=np.float32)
        kernel(result, *args)
        return result
    return func


def make_multi_task(kernel, n_thread):
    """
    创建多线程任务

    @param {function} kernel - 传入执行计算的函数
    @param {int} n_thread - 要创建的线程数
    """
    def func(length, *args):
        result = np.empty(length, dtype=np.float32)
        args = (result,) + args
        # 将每个线程接受的参数定义好
        chunk_size = (length + n_thread - 1) // n_thread
        chunks = [[arg[i * chunk_size:(i + 1) * chunk_size]
                   for i in range(n_thread)] for arg in args]
        # 利用 ThreadPoolExecutor 进行并发
        with ThreadPoolExecutor(max_workers=n_thread) as e:
            for _ in e.map(kernel, *chunks):
                pass
        return result
    return func


# fastmath, 牺牲计算精度的情况下提升速度
@jit(fastmath=False)
def fastmath_disable(A):
    acc = 0.
    # without fastmath, this loop must accumulate in strict order
    for x in A:
        acc += np.sqrt(x)
    return acc


@jit(fastmath=True)
def fastmath_enable(A):
    acc = 0.
    # with fastmath, the reduction can be vectorized as floating point
    # reassociation is permitted.
    for x in A:
        acc += np.sqrt(x)
    return acc


# 利用多核并行运算parallel, prange使用
@jit
def parallel_range_disable(t):
    a = np.random.rand(10 ** 8).astype(np.float32)
    n = len(a)
    acc = 0.
    for i in range(n * t):
        acc += np.sqrt(a[i % n])
    return acc


@jit(parallel=True)
def parallel_range_enable(t):
    a = np.random.rand(10 ** 8).astype(np.float32)
    n = len(a)
    acc = 0.
    for i in prange(n):
        acc += np.sqrt(a[i % n])
    return acc


if __name__ == '__main__':
    import numba
    numba.void
    exit(0)
    # 利用多核并行运算parallel, prange使用
    _start = datetime.datetime.now()
    parallel_range_disable(10)
    _end = datetime.datetime.now()
    print('parallel_range_disable time: %s' % str((_end - _start).total_seconds()))

    _start = datetime.datetime.now()
    parallel_range_enable(10)
    _end = datetime.datetime.now()
    print('parallel_range_enable time: %s' % str((_end - _start).total_seconds()))

    # fastmath, 牺牲计算精度的情况下提升速度
    _a = np.random.rand(10 ** 8).astype(np.float32)
    _start = datetime.datetime.now()
    fastmath_disable(_a)
    _end = datetime.datetime.now()
    print('fastmath_disable time: %s' % str((_end - _start).total_seconds()))

    _start = datetime.datetime.now()
    fastmath_enable(_a)
    _end = datetime.datetime.now()
    print('fastmath_enable time: %s' % str((_end - _start).total_seconds()))

    # 使用nogil提升多线程处理
    _length = 10 ** 8  # 计算长度
    _a = np.random.rand(_length).astype(np.float32)
    _b = np.random.rand(_length).astype(np.float32)

    # 包装函数方法
    _nogil_disable_single = make_single_task(nogil_disable)
    _nogil_disable_multi = make_multi_task(nogil_disable, 4)
    _nogil_enable_single = make_single_task(nogil_enable)
    _nogil_enable_multi = make_multi_task(nogil_enable, 4)

    _start = datetime.datetime.now()
    _nogil_disable_single(_length, _a, _b)
    _end = datetime.datetime.now()
    print('nogil_disable_single time: %s' % str((_end - _start).total_seconds()))

    _start = datetime.datetime.now()
    _nogil_disable_multi(_length, _a, _b)
    _end = datetime.datetime.now()
    print('nogil_disable_multi time: %s' % str((_end - _start).total_seconds()))

    _start = datetime.datetime.now()
    _nogil_enable_single(_length, _a, _b)
    _end = datetime.datetime.now()
    print('nogil_enable_single time: %s' % str((_end - _start).total_seconds()))

    _start = datetime.datetime.now()
    _nogil_enable_multi(_length, _a, _b)
    _end = datetime.datetime.now()
    print('nogil_enable_multi time: %s' % str((_end - _start).total_seconds()))

    # python 循环
    _start = datetime.datetime.now()
    foo_while_no_jit(100000000)
    _end = datetime.datetime.now()
    print('foo_while_no_jit time: %s' % str((_end - _start).total_seconds()))

    _start = datetime.datetime.now()
    foo_while(100000000)
    _end = datetime.datetime.now()
    print('foo_while time: %s' % str((_end - _start).total_seconds()))

    _start = datetime.datetime.now()
    foo_no_jit(100000000)
    _end = datetime.datetime.now()
    print('foo_no_jit time: %s' % str((_end - _start).total_seconds()))

    _start = datetime.datetime.now()
    foo(100000000)
    _end = datetime.datetime.now()
    print('foo time: %s' % str((_end - _start).total_seconds()))

    # 使用numpy画图
    _image_no_jit = np.zeros((500 * 2, 750 * 2), dtype=np.uint8)
    _image = np.zeros((500 * 2, 750 * 2), dtype=np.uint8)

    # 不使用jit的numpy操作
    _start = datetime.datetime.now()
    create_fractal_no_jit(-2.0, 1.0, -1.0, 1.0, _image_no_jit, 20)
    _end = datetime.datetime.now()
    print('create_fractal_no_jit time: %s' % str((_end - _start).total_seconds()))

    # 使用jit的numpy操作
    _start = datetime.datetime.now()
    create_fractal(-2.0, 1.0, -1.0, 1.0, _image, 20)
    _end = datetime.datetime.now()
    print('create_fractal time: %s' % str((_end - _start).total_seconds()))

    # 显示两个图片
    if have_mpl:
        imshow(_image_no_jit)
        show()
        imshow(_image)
        show()
