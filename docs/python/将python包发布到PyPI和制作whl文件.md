# 将python包发布到PyPI和制作whl文件

引用自：https://blog.csdn.net/winycg/article/details/80025432

本文只作为自己本地存档参考，如要转载请联系原文出处博主。



参考链接： 
[wheel和egg的不同](https://blog.csdn.net/nirendao/article/details/70768713) 
[怎样将自己写的包传达到PyPi](https://blog.csdn.net/crisschan/article/details/51840552) 
[发布你自己的轮子 - PyPI打包上传实践](https://segmentfault.com/a/1190000008663126#articleHeader7) 
[PyPI官网上传包教程](https://packaging.python.org/tutorials/distributing-packages/)

# wheel文件

Wheel和Egg都是python的打包格式，目的是支持不需要编译或制作的安装过程，实际上也是一种压缩文件，将.whl的后缀改为.zip即可可看到压缩包里面的内容。按照官网说法，wheels是发行版Python的新标准并且要取代.egg。 
 Egg格式是由setuptools在2004年引入，而Wheel格式是由PEP427在2012年定义。 Wheel现在被认为是Python的二进制包的标准格式。

以下是Wheel和Egg的主要的不同点：

- Wheel有一个官方的PEP427来定义，而Egg没有PEP定义。
- Wheel是一种分发格式，即打包格式。而Egg既是一种分发格式，也是一种 运行时安装的格式，并且是可以被import的。
- Wheel文件不会包含.pyc文件
- Wheel使用和PEP376兼容的.dist-info目录，而Egg使用.egg-info目录。
- Wheel有着更丰富的命名规则。
- Wheel是有版本的，每个Wheel文件都包含wheel规格的版本和打包它的实现。
- Wheel在内部被sysconfig path type管理，因此转向其他格式也更容易。

# distutils和setuptools工具

用来Python环境中构建和安装额外的模块，模块可以基于Python，也可以C/C++写的扩展模块，可以是python包，包中包含了C和Python编写的模块。setuptools是 Python Enterprise Application Kit(PEAK)的一个副项目,它是一组Python的 distutilsde工具的增强版(适用于 Python 2.3.5 以上的版本,64 位平台则适用于 Python 2.4 以上的版本),可以让程序员更方便的创建和发布 Python 包,特别是那些对其它包具有依赖性的状况。

## setuptools重点在于setup.py文件编写：

setup.py参数介绍：

- name : 打包起来的包的文件名
- version : 版本号,添加为打包文件的后缀名
- author : 作者
- author_email : 作者的邮箱
- py_modules : 打包的.py文件
- packages: 打包的python文件夹
- include_package_data : 项目里会有一些非py文件,比如html和js等,这时候就要靠include_package_data 和 package_data 来指定了。package_data:一般写成{‘your_package_name’: [“files”]}, include_package_data还没完,还需要修改MANIFEST.in文件.MANIFEST.in文件的语法为: include xxx/xxx/xxx/*.ini*/(所有以.ini结尾的文件,也可以直接指定文件名)
- license : 支持的开源协议
- description : 对项目简短的一个形容
- ext_modules : 是一个包含Extension实例的列表,Extension的定义也有一些参数。
- ext_package : 定义extension的相对路径
- requires : 定义依赖哪些模块
- provides : 定义可以为哪些模块提供依赖
- data_files :指定其他的一些文件(如配置文件),规定了哪些文件被安装到哪些目录中。如果目录名是相对路径,则是相对于sys.prefix或sys.exec_prefix的路径。如果没有提供模板,会被添加到MANIFEST文件中。

## 将python文件(.py)封装成可安装使用的模块

参考：<https://docs.python.org/3.6/distutils/introduction.html#distutils-simple-example> 
printtest.py

```python
def test():
    print('print test')12
```

将以上.py文件做成python模块，需要在相同目录下创建setup.py文件，setup.py中输入配置信息:

```python
from setuptools import setup
setup(name='printtest',
      version='1.0',
      py_modules=['printtest'],
      )12345
```

打开终端，定位到该文件夹下，输入：

```
python setup.py sdist1
```

此时在目录中生成dist文件夹，文件夹中有testpg-1.0.tar.gz文件，用户安装的话只需要testpg-1.0.tar.gz文件即可。将此文件解压得到testpg-1.0文件夹，会发现该文件夹有我们刚刚书写的3个py文件，还有一个PKG-INFO，打开该文件，会显示该模块的具体信息：由于我们没有设置，所以为UNKOWN

```
Metadata-Version: 1.0
Name: printtest
Version: 1.0
Summary: UNKNOWN
Home-page: UNKNOWN
Author: UNKNOWN
Author-email: UNKNOWN
License: UNKNOWN
Description: UNKNOWN
Platform: UNKNOWN
1234567891011
```

终端定位到此文件夹下，输入以下命令，模块将会被安装到解释器对应的Lib/site-packages目录下：

```
python setup.py install
```

安装后，会发现Lib/site-packages目录下存在printtest.py文件和printtest-1.0-py3.6.egg-info 
应用：

```
import printtest

printtest.test()123
```

输出：

```
print test1
```

# 封装Python包

导入单个Python文件时成为Python模块，而包含多个Python文件的文件夹成为一个Python包。本节主要讲述怎样封装一个Python包。 
1.创建一个文件夹，将需要封装的pagtest文件夹（里面为.py文件，需要包括一个`__init__.py`文件，内容可以为空）放到该文件夹中，然后创建setup.py文件对包进行配置：

```python
from setuptools import setup

setup(name='pagtest',
      version='1.0.0',
      description='A print test for PyPI',
      author='winycg',
      author_email='win@163.com',
      url='https://www.python.org/',
      license='MIT',
      keywords='ga nn',
      project_urls={
            'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
            'Funding': 'https://donate.pypi.org',
            'Source': 'https://github.com/pypa/sampleproject/',
            'Tracker': 'https://github.com/pypa/sampleproject/issues',
      },
      packages=['pagtest'],
      install_requires=['numpy>=1.14', 'tensorflow>=1.7'],
      python_requires='>=3'
     )1234567891011121314151617181920
```

2.创建README.txt文件用于对文件的安装以及使用信息做描述 
3.目前文件夹的目录的架构为：

```
pagtest/
    __init__.py
    print1.py
    print2.py
setup.py
README.txt123456
```

输入以下命令进行打包，制作source distribution（源代码发布包），此命令将会把所有内容在dist/目录打包为pagtest-1.0.0.tar.gz

```
python setup.py sdist
```

4.将命令行定位到此文件夹下，输入命令对dist目录下的pagtest-1.0.0.tar.gzt包进行上传，twine为Python包需要安装（安装过程需要输入pipy官网的用户名和密码，注册地址：https://pypi.org/）：

```
twine upload dist/*
```

# 制作python包为wheel文件

wheel是一个已经编译好的包，在安装时不需要编译过程，安装whl文件时要比发布的源文件安装要快。 
在如上第2步后，输入如下命令即可在生成.whl

```
python setup.py bdist_wheel
```

.whl文件在dist目录下，上传到PyPI：

```
twine upload dist/*
```

# 更新Python包

修改setup.py中的版本号，然后直接上传即可