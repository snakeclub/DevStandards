# 使用Sphinx自动生成文档

官方文档: http://sphinx-doc.org/contents.html

中文入门：http://www.pythondoc.com/sphinx/rest.html#id15

中文文档 http://zh-sphinx-doc.readthedocs.org/en/latest/contents.html

扩展：https://blog.csdn.net/qq_27961843/article/details/104414244

## 安装Sphinx包及相应的格式主题包

需先按照Sphinx包（4.5.0版本），里面会带有默认的主题风格，如果需要其他的主题风格，需要按照相应的主题包。本实例只包括sphinx_rtd_theme和sphinx_bootstrap_theme两个主题的说明。

```
pip install -U Sphinx
pip install sphinx-autobuild
pip install sphinx_rtd_theme
pip install sphinx_bootstrap_theme
pip install recommonmark   # 支持markdown格式文档
pip install sphinx_markdown_tables
```

注：sphinx_bootstrap_theme的官网：https://sphinx-bootstrap-theme.readthedocs.io/en/latest/

## 生成Sphinx配置文档

先梳理自己项目的目录结构，以HiveNetAssemble的结构为例：

```
HiveNetAssemble
    |__docs
    |    |__standards     -   规范标准md文档所在目录
    |    |    |__...
    |    |__tutorial      -   通览md文档所在目录
    |    |    |__...
    |__HiveNetCore       -   子项目HiveNetCore的代码所在目录（项目package目录）
    |    |__...
    |__...
```

我们希望生成HiveNetAssemble的自动文档，文档目录放置在docs下，操作如下（注意“**#####**”标注了建议修改的项）：

```
cmd> cd docs
cmd> sphinx-quickstart
欢迎使用 Sphinx 4.5.0 快速配置工具。

请输入接下来各项设置的值（如果方括号中指定了默认值，直接
按回车即可使用默认值）。

##### 以下项为文档根目录，由于我们已在docs目录下了，所以直接使用默认即可
已选择根路径：.

有两种方式来设置 Sphinx 输出的创建目录：
一是在根路径下创建“_build”目录，二是在根路径下创建“source”
和“build”两个独立的目录。

##### 将文档源码和生成路径分开，需设置为y
> 独立的源文件和构建目录（y/n） [n]: y

项目名称将会出现在文档的许多地方。
##### 项目名和作者名、版本
> 项目名称: HiveNetAssemble
> 作者名称: 黎慧剑
> 项目发行版本 []: 0.1.0

如果用英语以外的语言编写文档，
你可以在此按语言代码选择语种。
Sphinx 会把内置文本翻译成相应语言的版本。

支持的语言代码列表见：
http://sphinx-doc.org/config.html#confval-language。
##### 项目语言
> 项目语种 [en]: zh_CN

创建文件 /Users/lhj/opensource/HiveNetAssemble/HiveNetCore/docs/source/conf.py。
创建文件 /Users/lhj/opensource/HiveNetAssemble/HiveNetCore/docs/source/index.rst。
创建文件 /Users/lhj/opensource/HiveNetAssemble/HiveNetCore/docs/Makefile。
创建文件 /Users/lhj/opensource/HiveNetAssemble/HiveNetCore/docs/make.bat。

完成：已创建初始目录结构。

你现在可以填写主文档文件 /Users/lhj/opensource/HiveNetAssemble/HiveNetCore/docs/source/index.rst 并创建其他文档源文件了。 用 Makefile 构建文档，例如：
 make builder
此处的“builder”是支持的构建器名，比如 html、latex 或 linkcheck。
```

## 对注释风格SnakerPy格式（JSDoc风格）的支持

Sphinx自带的扩展插件napoleon支持NumPy和Google风格的注释文档转换，如果要增加支持SnakerPy格式（JSDoc风格），可以到 https://github.com/snakeclub/sphinx-ext-napoleon-snakerpy 下载napoleon扩展，增加对SnakerPy注释风格支持（安装方法参考sphinx-ext-napoleon-snakerpy 的文档）

## 添加在线发布文档的依赖包安装支持

在docs目录下增加requirements.txt文件，添加生成文档的依赖包安装支持，例如  sphinx-ext-napoleon-snakerpy  支持需要安装six，以及 markdown 支持需要安装 sphinx_markdown_tables 依赖库，对应的requirements.txt文件内容参考如下：

```
Sphinx==4.5.0
recommonmark==0.7.1
six==1.16.0
sphinx_markdown_tables==0.0.17
...
```

**注：还需要添加上项目所依赖的其他开源库，以便生成文档时不会出现异常。**

## 修改Sphinx配置文档

修改sphinx-quickstart生成的配置文件：docs\source\conf.py，修改项及说明如下：

### 增加要检索的代码包路径

```
# 新增检索代码的路径
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
# 增加snakerpy的注释类型支持插件搜索路径
sys.path.append(
    os.path.join(os.path.dirname(__file__), os.path.pardir, 'ext')
)
# 子项目HiveNetCore的检索路径
sys.path.append(os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    os.path.pardir, os.path.pardir, 'HiveNetCore'
))
# ... 可以添加多个子项目
```

### 修改文档的主题模板

如果使用sphinx_rtd_theme主题，采用以下修改方式：

```
import sphinx_rtd_theme  # 在文件开头新增导入

# html_theme = 'alabaster'
# 修改为
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]  # 新增
```

如果使用sphinx_bootstrap_theme主题，采取以下修改方式

```
import sphinx_bootstrap_theme  # 在文件开头新增导入

# html_theme = 'alabaster'
# 修改为
html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

# 取消 html_theme_options = {} ，修改为以下值，官网取值参考：https://sphinx-bootstrap-theme.readthedocs.io/en/latest/README.html#installation
html_theme_options = {
    'navbar_title': "HiveNetCore",
    'globaltoc_depth': 2,
    'globaltoc_includehidden': "true",
    'navbar_class': "navbar navbar-inverse",
    'navbar_fixed_top': "true",
    'bootswatch_theme': "united",
    'bootstrap_version': "3"
}
```

### 注释风格支持

修改配置文件增加插件参数：

```
# 例如增加'napoleon_snakerpy'插件支持
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'napoleon_snakerpy',
    'recommonmark',
    'sphinx_markdown_tables'
]  # 注: 最后两个是支持markdown文档的配置

# 增加Napoleon配置
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_snakerpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_use_keyword = True
napoleon_custom_sections = None
```

### 支持MarkDown文档

```
# 支持MarkDown需导入
import recommonmark
from recommonmark.parser import CommonMarkParser
from recommonmark.transform import AutoStructify


# source_suffix = '.rst' 修改为支持md文档
source_suffix = ['.rst', '.md']

# 支持markdown文档
source_parsers = {
    '.md': 'recommonmark.parser.CommonMarkParser',
}

# 增加启动处理
# app setup hook
github_doc_root = 'https://github.com/snakeclub/HiveNetAssemble/tree/main/docs/'


def setup(app):
    print('------------------启动会先执行-------------------')
    app.add_config_value('recommonmark_config', {
        'url_resolver': lambda url: github_doc_root + url,
        'auto_toc_tree_section': 'Contents',
        'enable_eval_rst': True,
    }, True)
    app.add_transform(AutoStructify)
```

## 生成API文档索引（rst）

### 使用sphinx-apidoc生成代码文档索引

```
#执行以下命令，执行所在路径是docs，注意前面的路径是源文件路径，后面的路径是项目路径，-e代表每个module一个页面，如果不用-e则代表一个package一个页面
docs> sphinx-apidoc -f -e -d 4 -o ./source/HiveNetCore ../HiveNetCore/HiveNetCore
docs> sphinx-apidoc -f -e -d 4 -o ./source/HiveNetWebUtils ../HiveNetWebUtils/HiveNetWebUtils
... 可以添加多个子项目
```

注意：如果代码发生了变化，必须重新执行一次生成最新的索引

### 添加自己的文档索引（markdown文件）

1、创建docs/source/tutorial目录，将当前项目的markdown文档放入该目录中；如果子项目有自己的文档，也可以在该目录下创建子项目名称目录，并将文档放入相关目录中；

2、新建tutorial.rst文件，用于展示md文件的概览文档，tutorial.rst内容如下（:glob:用于指定通配符找文件）：

```
Tutorial
========

.. toctree::
   :glob:

   tutorial/*


HiveNetCore
-----------

.. toctree::
   :glob:

   tutorial/HiveNetCore/*


utils
~~~~~

.. toctree::
   :glob:

   tutorial/HiveNetCore/utils/*


... 可以自己添加更多的目录检索
```

3、同理新建standards.rst索引文件，用于指定参考规范标准文档，文档放置在docs/source/standards下，文件内容如下：

```
Standards
==========

.. toctree::
   :glob:

   standards/*


HiveNetCore
-----------

.. toctree::
   :glob:

   standards/HiveNetCore/*
```

4、修改index.rst索引文件，调整主页的文档信息，修改的最终结果为（注意文档除新增tutorial、standards外，还要引用apidoc生成的索引，用于展示包的结构）：

```
.. HiveNetLib documentation master file, created by
   sphinx-quickstart on Fri Oct 19 14:07:15 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to HiveNetLib's documentation!
======================================

.. toctree::

   HiveNetLib
   tutorial
   standards


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```

## 生成HTML文档

执行以下命令，生成HTML文档

```
docs> make clean
docs> make html
```

# 借助Read the docs在线发布文档

官网地址：https://readthedocs.org/
