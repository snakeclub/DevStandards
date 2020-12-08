# Python性能优化技巧

## Python程序调试工具

### Py-Spy

Py-Spy是Python程序的抽样分析器。 它允许您可视化查看Python程序在哪些地方花了更多时间，整个监控方式无需重新启动程序或以任何方式修改工程代码。 Py-Spy的开销非常低：它是用Rust编写的，速度与编译的Python程序不在同一个进程中运行。 这意味着Py-Spy可以安全地用于生成生产环境中的Python应用调优分析。

pypi地址：https://pypi.org/project/py-spy/

**安装**

```
pip install py-spy
```

**使用**

1、先运行要分析的python程序；

2、输出类似top信息的监控数据

```
# 通过pid监控
py-spy top --pid 12345
# 通过指定脚本监控
py-spy top -- python myprogram.py
```

得到以下的监控信息：

![py-spy-top](python%E5%BC%80%E5%8F%91%E6%8A%80%E5%B7%A7.assets/322405-20190609181003797-1530438906.gif)

3、也可以输出性能优化大师布兰登.格雷格推出的可视化图 [FlameGraphs](http://www.brendangregg.com/flamegraphs.html)

```
# 通过pid
py-spy record -o profile.svg --pid 12345
# 通过指定脚本
py-spy record -o profile.svg -- python myprogram.py
```

生成的可视化图如下：

![img](python%E5%BC%80%E5%8F%91%E6%8A%80%E5%B7%A7.assets/322405-20190609181752046-1247952020.png)



### line_profiler

line_profiler使用装饰器(@profile)标记需要调试的函数.用kernprof.py脚本运行代码,被选函数每一行花费的cpu时间以及其他信息就会被记录下来。

https://github.com/pyutils/line_profiler

**安装**

```
# 正常情况应该通过以下命令直接安装，但实际上有缺陷安装不了
pip install line-profiler

# 请按以下方式执行安装
git clone https://github.com/rkern/line_profiler.git
find line_profiler -name '*.pyx' -exec cython {} \;
cd line_profiler
pip install . --user
```

以上安装方式会把程序安装在 Scripts 目录，将该目录加入环境变量中：C:\Users\74143\AppData\Roaming\Python\Python37\Scripts

**使用**

对要分析的代码函数上增加 @profile 修饰符，例如 test.py：

```
@profile
def foo():
    task = []

    for a in range(0, 101):
        for b in range(0, 101):
            if a + b == 100:
                task.append((a, b))
    return task


@profile
def run():
    for item in foo():
        pass


if __name__ == '__main__':
    run()

```

执行分析命令：

```
# 只生成文件
kernprof -l test.py
# 生成文件并直接展示
kernprof -l -v test.py
```

将生成二进制的分析文件 test.py.lprof，通过以下命令查看：

```
$ python -m line_profiler test.py.lprof
Timer unit: 1e-07 s

Total time: 0.0083387 s
File: test.py
Function: foo at line 1

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     1                                           @profile
     2                                           def foo():
     3         1          5.0      5.0      0.0      task = []
     4
     5       102        317.0      3.1      0.4      for a in range(0, 101):
     6     10302      38893.0      3.8     46.6          for b in range(0, 101):
     7     10201      43278.0      4.2     51.9              if a + b == 100:
     8       101        888.0      8.8      1.1                  task.append((a, b))
     9         1          6.0      6.0      0.0      return task

Total time: 0.0145847 s
File: test.py
Function: run at line 12

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    12                                           @profile
    13                                           def run():
    14       102     145562.0   1427.1     99.8      for item in foo():
    15       101        285.0      2.8      0.2          pass
```

注：

- Hits是调用次数。
- %Time 列告诉我们哪行代码占了它所在函数的消耗的时间百分比



## 尽量减少在屏幕打印的信息(print / logging)

在程序调试时经常需要通过 print 或 logging 将信息输出到屏幕上，但在 Python 里往屏幕（cmd / shell）打印信息的性能非常查，将大幅度降低程序的执行速度，因此需要尽可能减少在屏幕打印的信息；此外，将信息输出至日志文件也同样会有性能损耗，从性能角度损耗从高至低的顺序为：

​	**logging输出屏幕 > print输出屏幕 > logging输出文件**

因此可以通过以下方法提升性能：

- 后续不会使用的信息不输出屏幕，也不记录至日志文件
- 如果必须输出信息，尽量使用输出至日志文件的方式，减少输出屏幕
- 如果需要进一步提升性能，尝试将信息输出至内存后再异步记录到日志文件的方案

下面通过实际代码比较不同方案的执行时长（完整代码见 [performance_optimizing_print.py](python%E6%80%A7%E8%83%BD%E4%BC%98%E5%8C%96%E6%8A%80%E5%B7%A7.assets/performance_optimizing_print.py) 文件）：

**不打印输出**

```
import datetime
_start = datetime.datetime.now()
_index = 0
while _index < 1000:
    _index += 1

_end = datetime.datetime.now()
_unuse_print_time = (_end - _start).total_seconds()
print('unuse print time: %s' % str(_unuse_print_time))
```

执行时长为：0.0 秒

**使用 print 输出屏幕**

```
import datetime
_start = datetime.datetime.now()
_index = 0
while _index < 1000:
    _index += 1
    print('use print index %d !' % _index)
_end = datetime.datetime.now()
_use_print_time = (_end - _start).total_seconds()
print('use print time: %s' % str(_use_print_time))
```

执行时长为：27.525331 秒

**使用 logging 输出屏幕**

使用官方的 logging 库输出屏幕，具体代码参见 performance_optimizing_print.py 

执行时长为：95.130044 秒

**使用 logging 输出到文件**

使用官方的 logging 库输出到文件，具体代码参见 performance_optimizing_print.py 

执行时长为：0.153621 秒

**使用 HiveNetLib.simple_log 输出到内存队列**

使用第三方库 HiveNetLib 的 simple_log 模块，将打印信息输出到内存后异步写入文件，具体代码参见 performance_optimizing_print.py

执行时长为：0.148296 秒



## 合理选用多线程及多进程

使用多线程/多进程实现任务并行处理是提升程序处理性能的通用思路。但在Python中需注意有GIL锁（全局解释锁）的限制，实际上Python多线程并不能真正能发挥作用，GIL锁的存在保证在同一个时间只能有一个线程执行任务，也就是多线程并不是真正的并发，只是交替争夺同一个CPU资源的执行。假如有10个线程跑在10核CPU上，当前可以工作的线程也只能是同一个CPU上的线程，也就是说在Python的多线程下同一时刻也只有一个线程在工作。

多线程和多进程的选用原则如下：

- **计算密集型（CPU密集型）**：应选择多进程单线程，通过多进程充分使用CPU的多核性能（注意如果是计算密集型采用多线程，由于频繁的线程间争夺CPU资源，性能反而比单线程差）；
- **IO密集型**：比如网络请求、数据库读写、文件读写等频繁等待IO阻塞处理的情况，应选择多线程，可以获得比单线程更高的性能。



## 使用协程



## 优化循环代码

相关示例完整代码见 [performance_optimizing_circle.py](python%E6%80%A7%E8%83%BD%E4%BC%98%E5%8C%96%E6%8A%80%E5%B7%A7.assets/performance_optimizing_circle.py)

### 避免在循环体内使用点操作及相同变量计算

1. Python 的解释器每次遇到点操作都会重新求一次该操作函数的值，例如遇到 'test'.upper() 会通过 str.upper 查找一次函数值，如果这个操作在循环内，也会产生一些性能损耗；因此可以在循环外先将点操作的函数赋给一个已知变量，这样可以减少查找函数值的一次操作损耗。

   **注：该优化方式代码可读性会降低，每次点操作性能损耗其实不算大，但如果循环次数非常多，或者对性能要求比较极致，可以考虑该优化方式。**

2. 将相同的变量计算移出循环体内，减少重复计算，可以大幅提升处理性能。

**点操作在循环内示例**

```
DOT_RANGE_NUM = 10000000
DOT_WORDS = [
    'test', 'for', 'circle', 'performance', 'optimizing', 'dot'
]
_str = ''
for _i in range(DOT_RANGE_NUM):
    _str = DOT_WORDS[_i % len(DOT_WORDS)].upper()
```

执行时长为：2.155711 秒

**点操作移出循环外示例**

```
DOT_RANGE_NUM = 10000000
DOT_WORDS = [
    'test', 'for', 'circle', 'performance', 'optimizing', 'dot'
]
_str = ''
_upper = str.upper
for _i in range(DOT_RANGE_NUM):
    _str = _upper(DOT_WORDS[_i % len(DOT_WORDS)])
```

执行时长为：1.943552 秒

**相同变量计算移出循环外**

```
DOT_RANGE_NUM = 10000000
DOT_WORDS = [
    'test', 'for', 'circle', 'performance', 'optimizing', 'dot'
]
_str = ''
_upper = str.upper
_len = len(DOT_WORDS)
for _i in range(DOT_RANGE_NUM):
    _str = _upper(DOT_WORDS[_i % _len])
```

执行时长为：1.445136 秒



## 使用 numba 加速循环及科学计算

numba 主要对 numpy 和 python原生循环进行了针对性的编译优化，不要寄望于numba可以优化所有函数，因此在以下情况下可尝试使用 numba 进行性能优化：

- 代码中有大量for、while等循环处理逻辑（**注意：numba对没有循环或者只有非常小循环的函数加速效果并不明显，用不用都一样**）
- 代码需要使用 numpy 进行数组的科学计算
- 需要使用多线程提升性能 (nogil=True) 的场景（**注意：数据量越大、并发的效果越明显。反之，数据量小的时候，并发很有可能会降低性能**）
- 需要并行计算提升性能 (parallel=True) 的场景（**注意：开启并行计算搞不好可能更慢，如果代码里只是简单的for循环的话开启的效果就会比较明显**）
- 需要将纯Python函数编译成ufunc，使之速度与使用c编写的传统的ufunc函数一样（@vectorize 修饰符）

详细使用方法见[《使用Numba编译器提升Python计算代码性能》](使用Numba编译器提升Python计算代码性能.md)



