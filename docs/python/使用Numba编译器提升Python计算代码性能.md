# 使用Numba编译器提升Python计算代码性能

## 简介

python由于是动态解释性语言的特性，执行代码来相比java、c++要慢很多，尤其在做科学计算的时候，当遇到十亿百亿级别的运算时劣势更加明显。

![Numba logo](%E4%BD%BF%E7%94%A8Numba%E7%BC%96%E8%AF%91%E5%99%A8%E6%8F%90%E5%8D%87Python%E8%AE%A1%E7%AE%97%E4%BB%A3%E7%A0%81%E6%80%A7%E8%83%BD.assets/numba-blue-horizontal-rgb.svg)

**numba**是一款可以将python函数编译为机器代码的 JIT 编译器，经过numba编译的python代码（仅数组运算及循环），其运行速度可以接近C或FORTRAN语言。

官网地址：https://numba.pydata.org/

官方参考手册：https://numba.readthedocs.io/en/stable/index.html

目前主流的提升python代码性能的编译器有Cython、pypy 和 numba，三个编译器的比较如下：

- **Cython**

已经不是单纯的Python了，而是一种法Python + C的便利性组合，生成的是一个混凝土程序，包含了Python脚本和本机代码。Cython允许类型和语法上混搭编写，能转为C编译的部分效率非常高。但是这种优化基本上无法考虑python原生代码的兼容性，必须按照Cython的要求来写，移植代价非常大。

- **pypy**

PyPy内置JIT，对纯Python项目兼容性极好，代码移植代价几乎是最小的，几乎可以直接运行并直接获得性能提升，目前主流的Web框架也都是支持pypy的；缺点有不支持一些Python的书写方式，以及对很多C语言库支持性不好。

- **numba**

Numba是一个库，可以在运行时将Python代码编译为本地机器指令，而不会强制大幅度的改变普通的Python代码；numba在科学计算方面的性能特别强大，最适合的场景是有大量计算的科学及算法场景。



## 建议使用场景

numba 主要对 numpy 和 python原生循环进行了针对性的编译优化，不要寄望于numba可以优化所有函数，因此在以下情况下可尝试使用 numba 进行性能优化：

- 代码中有大量for、while等循环处理逻辑（**注意：numba对没有循环或者只有非常小循环的函数加速效果并不明显，用不用都一样**）
- 代码需要使用 numpy 进行数组的科学计算
- 需要使用多线程提升性能 (nogil=True) 的场景（**注意：数据量越大、并发的效果越明显。反之，数据量小的时候，并发很有可能会降低性能**）
- 需要并行计算提升性能 (parallel=True) 的场景（**注意：开启并行计算搞不好可能更慢，如果代码里只是简单的for循环的话开启的效果就会比较明显**）
- 需要将纯Python函数编译成ufunc，使之速度与使用c编写的传统的ufunc函数一样（@vectorize 修饰符）

​      GIL锁说明：Python多线程并不能真正能发挥作用，因为在Python中，有一个GIL，即全局解释锁，该锁的存在保证在同一个时间只能有一个线程执行任务，也就是多线程并不是真正的并发，只是交替得执行。假如有10个线程炮在10核CPU上，当前工作的也只能是一个CPU上的线程。



## 使用方法

**1、安装 numba** 

方法很简单，使用pip安装即可：pip install numba



**2、使用 @jit 修饰符编译函数提升性能**

（1）可以不带任何参数使用修饰符，这时numba编译时会自动判断函数是否兼容，如果不兼容会自动关闭nopython 模式（由于有编译过程，执行时间反而会加长），因此建议显式指定 nopython 参数：

```
from numba import jit
@jit
def func(...):
	...
```

（2）修饰符传入指定参数控制优化效果，具体参数后面会逐个介绍：

```
from numba import jit
@jit(nopython=True, ...)
def func(...):
	...
```

（3）@jit 修饰符的第一个参数是签名（signature_or_function），用于指定需要修饰的函数定义，如果不传该参数，numba会自动根据上下文判断并自动转换为适配的函数定义，不过自动转换可能会有类型与预期不一致的精度问题，因此如果希望避免精度问题或发现存在相关问题，建议主动指定定义。

参考：https://numba.readthedocs.io/en/stable/reference/types.html#signatures

**函数方式定义签名**

```
@jit(numba.int64(numba.int32[:]), ...)
def nb_sum(a):
	...
	return x
```

这种方式可直接使用numba内置的函数进行定义，可以直接找到numba所支持各种类型

**字符串方式定义签名**

```
@jit(“int64(int32[:])” ...)
def nb_sum(a):
	...
	return x
```

这种方式可以使用字符串方式进行定义，可以支持以下列表的命名方式：

| Type name(s)    | Shorthand | Comments                               |
| --------------- | --------- | -------------------------------------- |
| boolean         | b1        | represented as a byte                  |
| uint8, byte     | u1        | 8-bit unsigned byte                    |
| uint16          | u2        | 16-bit unsigned integer                |
| uint32          | u4        | 32-bit unsigned integer                |
| uint64          | u8        | 64-bit unsigned integer                |
| int8, char      | i1        | 8-bit signed byte                      |
| int16           | i2        | 16-bit signed integer                  |
| int32           | i4        | 32-bit signed integer                  |
| int64           | i8        | 64-bit signed integer                  |
| intc            | –         | C int-sized integer                    |
| uintc           | –         | C int-sized unsigned integer           |
| intp            | –         | pointer-sized integer                  |
| uintp           | –         | pointer-sized unsigned integer         |
| float32         | f4        | single-precision floating-point number |
| float64, double | f8        | double-precision floating-point number |
| complex64       | c8        | single-precision complex number        |
| complex128      | c16       | double-precision complex number        |

注：void是什么都不返回的函数的返回类型(即：Python调用时实际上返回None)

**数组定义方式**

可以通过[:]这类方式指定数组定义：

一维数组：numba.int64[:] 或 "int64[:]" 或 "i8[:]"

多维数组(以三维数组为例)：numba.int64[:, :, :] 或 "int64[:, :, :]" 或 "i8[:, :, :]"

（4） nopython 参数，是否指定强制编译为numba代码，如果强制指定该参数为True，则遇到不兼容numba的代码会抛出异常，建议强制指定；

（5）fastmath 参数，如果指定该参数为True，将通过牺牲少量精度的方式大幅提升计算性能；

（6）nogil 参数，如果指定该参数为True，对于多线程执行情况可绕开Python的GIL全局锁，提升多线程计算的执行性能；

（7）parallel 参数，如果指定该参数为True，可以利用多核进行数据的并行计算处理，该参数需要跟函数中的numba.prange 配合处理，prange是numba提供的兼容range的并行分组指示函数，遇到 parallel 参数将自动按多进程并行模式执行计算，改造原有函数逻辑时需要将 "for i in range(n):" 修改为  "for i in prange(n):" ；



**4、使用 @vectorize 装饰器将函数编译为 ufunc（universal functions）**

numba的 @vectorize 可以将纯Python函数动态编译成ufunc，使之速度与使用c编写的传统的ufunc函数一样

```
from numba import vectorize, float64

@vectorize([float64(float64, float64)])
def f(x, y):
    return x + y
```

如果函数需要支持多类型的入参和出参，可以在参数数组中传入多个签名定义，注意顺序，精度低的在前，高的在后，否则就会出奇怪的问题，例如int32就只能在int64之前：

```
@vectorize([int32(int32, int32),
            int64(int64, int64),
            float32(float32, float32),
            float64(float64, float64)])
def f(x, y):
    return x + y
```



**5、使用 @jitclass 修饰符指定类中的所有函数使用numba编译**

参考：https://numba.pydata.org/numba-doc/dev/user/jitclass.html

如果类中包含属性定义 (self.xxx) ，则必须在修饰符函数中传入一个字典指定这些属性的类型，官方示例如下：

```
import numpy as np
from numba import int32, float32    # import the types
from numba.experimental import jitclass

spec = [
    ('value', int32),               # a simple scalar field
    ('array', float32[:]),          # an array field
]

@jitclass(spec)
class Bag(object):
    def __init__(self, value):
        self.value = value
        self.array = np.zeros(value, dtype=np.float32)

    @property
    def size(self):
        return self.array.size

    def increment(self, val):
        for i in range(self.size):
            self.array[i] += val
        return self.array

    @staticmethod
    def add(x, y):
        return x + y
```

使用 numba.typed 对象作为类的成员属性：

```
from numba import jitclass, types, typed

# 字典类型定义
kv_ty = (types.int64, types.unicode_type)

# 定义类
@jitclass([('d', types.DictType(*kv_ty)),
           ('l', types.ListType(types.float64))])
class ContainerHolder(object):
    def __init__(self):
        # initialize the containers
        self.d = typed.Dict.empty(*kv_ty)
        self.l = typed.List.empty_list(types.float64)

container = ContainerHolder()
container.d[1] = "apple"
container.l.append(123.)
```

可以使用 numba.typeof 使用 numba.typed 对象进行定义：

```
from numba import jitclass, typed, typeof

d = typed.Dict()
d[1] = "apple"
l = typed.List()
l.append(123.)

@jitclass([('d', typeof(d)), ('l', typeof(l))])
class ContainerInstHolder(object):
    def __init__(self, dict_inst, list_inst):
        self.d = dict_inst
        self.l = list_inst

container = ContainerInstHolder(d, l)
```

**注：@jitclass 并不支持成员属性为非numba标准类型的场景，例如python原生dict对象并不能作为类成员属性，需要使用typed.Dict()进行替代。**



## 需要注意的坑

**1、显式指定 nopython=True 参数**

切记 @jit 修饰符一定要显式指定 nopython 参数，该参数默认值为True，但有时候如果定义的函数中遇到 numba 支持不良好的部分，它就会自动关闭 nopython 模式，因此，**在使用 @jit 时候要明确写出nopython=True**。如果遇到问题，就找到这些支持不良好的部分，然后改写。

**2、精度自动转换问题**

在不指定函数定义时，numba 会自动转换数据类型以适应计算。但是在个别时候，**这种自动转变类型可能会引起一些计算误差**。通常这个误差是非常小的，几乎不会造成任何影响。但如果你所处理的问题会积累误差，比如求解非线性方程，那么在非常多的计算之后误差可能就是肉眼可见了。如果你发现有这样的问题，记得在 @jit 中指定输入输出的数据类型。

```
from numba import jit

@jit(numba.int64(numba.int32[:]))
def nb_sum(a):
    Sum = 0
    for i in range(len(a)):
        Sum += a[i]
    return Sum
```

numba具有C所有的数据类型，比如对上面的求和函数修饰符给出的定义中，numba.int64是说输出的数字为int64类型，numba.int32是说输入的数据类型为int32，而 [:] 是说输入的是数组。

同样也可以通过字符串方式简写为：@jit("i8(i4[:])")

**3、不同变量类型运算异常**

numba 编译器会根据调用代码猜测 JIT 处理函数中变量的数据类型，在编译时如果存在两种不同数据类型的计算操作，则可能会抛出异常，例如以下代码：

```
import numpy as np
from numba import jit

@jit(nopython=True)
def numpy_algorithm_jit(a):
    trace = 0
    # 假设输入变量是numpy数组
    for i in range(a.shape[0]):
        trace += np.tanh(a[i, i])
    return a + trace

x = np.arange(100).reshape(10, 10)
res = numpy_algorithm_jit(x)
```

执行时会在 “**return a + trace**” 一行抛出 numba.core.errors.TypingError 异常，异常信息为 “Cannot unify array(int64, 2d, C) and array(float64, 2d, C) for '$56binary_add.2'”。

原因是在 JIT 编译 函数numpy_algorithm_jit 时根据 trace 变量的初始化语句猜测它为 int 型，而需要运算的入参 a 为 float 类型的 numpy.ndarray 数组，两个类型无法直接相加运算，因此抛出异常。

解决方法也很简单，修改脚本增加强制的类型转换即可： “**return a + float(trace)**”



## 示例代码及测试

相关示例的测试完整代码见 [performance_optimizing_numba.py](%E4%BD%BF%E7%94%A8Numba%E7%BC%96%E8%AF%91%E5%99%A8%E6%8F%90%E5%8D%87Python%E8%AE%A1%E7%AE%97%E4%BB%A3%E7%A0%81%E6%80%A7%E8%83%BD.assets/performance_optimizing_numba.py) （因为需同步测试对比效果，代码会有一点差异）。

**示例：python循环计算**

```
def foo(range_num):
    s = 0
    for i in range(range_num):
        s += i
    return s

foo(100000000)
```

执行时长：18.281504 秒

在 foo 函数加上修饰符 @jit(nopython=True) 后执行时长：0.55195 秒

```
def foo_while(range_num):
    s = 0
    i = 0
    while i < range_num:
        s += i
        i += 1
    return s
```

执行时长：29.925685 秒

在 foo_while 函数加上修饰符 @jit(nopython=True) 后执行时长：0.725884 秒

**示例：使用numpy的生成图**

```
import numpy as np
from numba import jit
try:
    from matplotlib.pylab import imshow, show
    have_mpl = True
except ImportError:
    have_mpl = False

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

image = np.zeros((500 * 2, 750 * 2), dtype=np.uint8)
create_fractal(-2.0, 1.0, -1.0, 1.0, image, 20)
if have_mpl:
    imshow(image)
    show()
```

执行时长：19.538666 秒

在 mandel 和 create_fractal 两个函数加上修饰符 @jit(nopython=True) 后执行时长：1.742044 秒

**示例：牺牲计算精度提升性能**

```
import numpy as np
from numba import jit

@jit(fastmath=False)
def fastmath_sum(A):
    acc = 0.
    # without fastmath, this loop must accumulate in strict order
    for x in A:
        acc += np.sqrt(x)
    return acc

_a = np.random.rand(10 ** 8).astype(np.float32)
fastmath_sum(_a)
```

fastmath关闭的执行时长：0.462997 秒

将 fastmath 启用 (fastmath=True) 后的执行时长：0.196996 秒

**示例：多线程使用nogil**

```
import math
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from numba import jit

@jit(nopython=True, nogil=False)
def nogil_demo(result, a, b):
    """
    nogil示例

    @param {np.ndarray} result - 获取结果的数组
    @param {np.ndarray} a - 入参a数组
    @param {np.ndarray} b - 入参b数组
    """
    for i in range(len(result)):
        result[i] = 1 / (a[i] + math.exp(-b[i]))

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

# 执行
_length = 10 ** 8  # 计算长度
_a = np.random.rand(_length).astype(np.float32)
_b = np.random.rand(_length).astype(np.float32)
_nogil_demo_multi = make_multi_task(nogil_demo, 4)
_nogil_demo_multi(_length, _a, _b)
```

nogil关闭的执行时长：0.902949 秒

将 nogil 启用 (nogil=True) 后的执行时长：0.338034 秒

**示例：使用多核并行计算prange**

```
@jit
def parallel_range(t):
    a = np.random.rand(10 ** 8).astype(np.float32)
    n = len(a)
    acc = 0.
    for i in range(n * t):
        acc += np.sqrt(a[i % n])
    return acc

parallel_range(10)
```

上述代码执行时长： 5.784032 秒

启用并行 (parallel=True) 并且将  range 修改为 prange，执行时长：1.796969 秒