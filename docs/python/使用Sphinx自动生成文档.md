# 使用Sphinx自动生成文档

官方文档: http://sphinx-doc.org/contents.html

中文入门：http://www.pythondoc.com/sphinx/rest.html#id15

中文文档 http://zh-sphinx-doc.readthedocs.org/en/latest/contents.html



## 安装Sphinx包及相应的格式主题包

需先按照Sphinx包（1.8.1版本），里面会带有默认的主题风格，如果需要其他的主题风格，需要按照相应的主题包。本实例只包括sphinx_rtd_theme和sphinx_bootstrap_theme两个主题的说明。

```
pip install -U Sphinx
pip install sphinx_rtd_theme
pip install sphinx_bootstrap_theme
pip install recommonmark   # 支持markdown格式文档
```

注：sphinx_bootstrap_theme的官网：https://sphinx-bootstrap-theme.readthedocs.io/en/latest/



## 生成Sphinx配置文档

先梳理自己项目的目录结构，以HiveNetLib的结构为例：

```
HiveNetLib
	|__docs
	|	|__standards     -   规范标准md文档所在目录
	|	|	|__...
	|	|__tutorial      -   通览md文档所在目录
	|	|	|__...
	|__HiveNetLib        -   HiveNetLib真正的代码所在目录（package根目录）
	|	|__...
	|__...
```

我们希望生成HiveNetLib的自动文档，文档目录放置在docs下，操作如下（注意“**#####**”标注了建议修改的项）：

```
cmd> cd docs
cmd> sphinx-quickstart
Welcome to the Sphinx 1.8.1 quickstart utility.

Please enter values for the following settings (just press Enter to
accept a default value, if one is given in brackets).

##### 以下项为文档根目录，由于我们已在docs目录下了，所以直接使用默认即可
Selected root path: .

You have two options for placing the build directory for Sphinx output.
Either, you use a directory "_build" within the root path, or you separate
"source" and "build" directories within the root path.
##### 将文档源码和生成路径分开，需设置为y
> Separate source and build directories (y/n) [n]: y

Inside the root directory, two more directories will be created; "_templates"
for custom HTML templates and "_static" for custom stylesheets and other static
files. You can enter another prefix (such as ".") to replace the underscore.
> Name prefix for templates and static dir [_]:

The project name will occur in several places in the built documentation.
##### 项目名和作者名、版本
> Project name: HiveNetLib
> Author name(s): 黎慧剑
> Project release []: 0.1.0

If the documents are to be written in a language other than English,
you can select a language here by its language code. Sphinx will then
translate text that it generates into that language.

For a list of supported codes, see
http://sphinx-doc.org/config.html#confval-language.
##### 项目语言
> Project language [en]: zh_CN

The file name suffix for source files. Commonly, this is either ".txt"
or ".rst".  Only files with this suffix are considered documents.
> Source file suffix [.rst]:

One document is special in that it is considered the top node of the
"contents tree", that is, it is the root of the hierarchical structure
of the documents. Normally, this is "index", but if your "index"
document is a custom template, you can also set this to another filename.
> Name of your master document (without suffix) [index]:
Indicate which of the following Sphinx extensions should be enabled:
##### 是否根据docstring自动生成文档
> autodoc: automatically insert docstrings from modules (y/n) [n]: y
##### 是否根据doctest块进行自动测试，这里我们选否，根据需要调整
> doctest: automatically test code snippets in doctest blocks (y/n) [n]:
##### 多项目文档之间进行链接，选y
> intersphinx: link between Sphinx documentation of different projects (y/n) [n]: y
> todo: write "todo" entries that can be shown or hidden on build (y/n) [n]:
##### 检查文档规模
> coverage: checks for documentation coverage (y/n) [n]: y
> imgmath: include math, rendered as PNG or SVG images (y/n) [n]:
> mathjax: include math, rendered in the browser by MathJax (y/n) [n]:
> ifconfig: conditional inclusion of content based on config values (y/n) [n]:
##### 很重要，输入y，表示将源码也放到文档中，你看很多python的模块的文档，其实都是包含代码的
> viewcode: include links to the source code of documented Python objects (y/n) [n]: y
##### 是否生成github的页面文件
> githubpages: create .nojekyll file to publish the document on GitHub pages (y/n) [n]: y

A Makefile and a Windows command file can be generated for you so that you
only have to run e.g. `make html' instead of invoking sphinx-build
directly.
> Create Makefile? (y/n) [y]:
> Create Windows command file? (y/n) [y]:

Creating file .\source\conf.py.
Creating file .\source\index.rst.
Creating file .\Makefile.
Creating file .\make.bat.

Finished: An initial directory structure has been created.

You should now populate your master file .\source\index.rst and create other documentation
source files. Use the Makefile to build the docs, like so:
   make builder
where "builder" is one of the supported builders, e.g. html, latex or linkcheck.

```



## 修改Sphinx配置文档

修改sphinx-quickstart生成的配置文件：docs\source\conf.py，修改项及说明如下：

### 增加要检索的代码包路径

```
# 取消以下3行代码的注释，并新增要生成文档的包的路径，注意由于要处理HiveNetLib包，路径应该在该包的上一层
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'../../../HiveNetLib'))  # 新增检索路径
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
    'navbar_title': "HiveNetLib",
    'globaltoc_depth': 2,
    'globaltoc_includehidden': "true",
    'navbar_class': "navbar navbar-inverse",
    'navbar_fixed_top': "true",
    'bootswatch_theme': "united",
    'bootstrap_version': "3"
}
```

### 注释风格支持

Sphinx自带的扩展插件napoleon支持NumPy和Google风格的注释文档转换，如果要增加支持SnakerPy格式（JSDoc风格），可以到 https://github.com/snakeclub/sphinx-ext-napoleon-snakerpy 下载napoleon扩展，增加对SnakerPy注释风格支持（安装方法参考sphinx-ext-napoleon-snakerpy 的文档）。

修改配置文件增加插件参数：

```
# 增加'sphinx.ext.napoleon_snakerpy'插件支持
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.napoleon_snakerpy'
]

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
def setup(app):
    app.add_config_value('recommonmark_config', {
        #'url_resolver': lambda url: github_doc_root + url,
        'auto_toc_tree_section': 'Contents',
        'enable_eval_rst': True,
        'enable_auto_doc_ref': True,
    }, True)
    app.add_transform(AutoStructify)
```



## 生成API文档索引（rst）

### 使用sphinx-apidoc生成代码文档索引

```
#执行以下命令，执行所在路径是docs，注意前面的路径是源文件路径，后面的路径是项目路径，-e代表每个module一个页面，如果不用-e则代表一个package一个页面
docs> sphinx-apidoc -f -e -d 4 -o ./source ../HiveNetLib
```

### 添加自己的文档索引

新建tutorial.rst文件，用于展示概览文档，相关文档可以为md文件，注意需放置在docs/source/tutorial路径下（暂时没有研究出放其他路径的方法），tutorial.rst内容如下（:glob:用于指定通配符找文件）：

```
Tutorial
==========

.. toctree::
   :glob:
   
   tutorial/*


base_tools
----------

.. toctree::
   :glob:
   
   tutorial/base_tools/*
   

net_service
-----------

.. toctree::
   :glob:

   tutorial/net_service/*
   
```

新建standards.rst索引文件，用于指定参考规范标准文档，注意需放置在docs/source/standards下，文件内容如下：

```
Standards
==========

.. toctree::
   :glob:
   
   standards/*

```

修改index.rst索引文件，调整主页的文档信息，修改的最终结果为（注意文档除新增tutorial、standards外，还直接引用了HiveNetLib.rst，用于展示包的结构）：

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
docs> make html
```

