# Python的笔记神器-Jupyter Notebook

## 简介

jupyter notebook是一种 **Web 应用**，能让用户将说明文本、数学方程、代码和可视化内容全部组合到一个易于共享的文档中。它可以直接在代码旁写出叙述性文档，而不是另外编写单独的文档。也就是它可以能将代码、文档等这一切集中到一处，让用户一目了然。

Jupyter这个名字是它要服务的三种语言的缩写：Julia，PYThon和R，这个名字与“木星（jupiter）”谐音。Jupyter Notebook 已迅速成为数据分析，机器学习的必备工具。因为它可以让数据分析师集中精力向用户解释整个分析过程。我们可以通过Jupyter notebook写出了我们的学习笔记。但是jupyter远远不止支持上面的三种语言，目前能够使用的语言他基本上都能支持，包括C、C++、C#，java、Go等等。

## 安装

### 基本安装

如果安装了anaconda，会自带安装Jupyter，或者可以直接使用 pip 命令进行安装：

```
pip install jupyter
```

**注：如果安装出错，可以尝试升级pip后再安装 pip install --upgrade pip ，或者使用 conda install jupyter 进行安装。**



安装完成以后，如果需要使用，先在命令行跳转到要使用的目录，然后输入以下命令启动：

```
jupyter notebook
```

会自动在浏览器打开页面应用，也可以自己在浏览器输入 "http://localhost:8888/tree" 打开应用，显示如下：

<img src="Python%E7%9A%84%E7%AC%94%E8%AE%B0%E7%A5%9E%E5%99%A8-Jupyter-Notebook.assets/image-20210203222339722.png" alt="image-20210203222339722" style="zoom: 50%;" />

注意：可以在不同目录启动多个jupyter notebook，只是每启动多一个应用，端口会自动加1，例如第2个为8889，第3个为8890.

### 安装代码自动补全插件

1、通过以下命令安装插件库（注意要在jupyter的安装环境）：

```
pip install jupyter_contrib_nbextensions
或
conda install jupyter_contrib_nbextensions
```

2、执行以下命令进行jupyter配置：

```
jupyter contrib nbextension install --user
```

4、部分网上教程说要装以下库并启动，不过我没有执行也一样可以：

```
pip install jupyter_nbextensions_configurator
jupyter nbextensions_configurator enable --user
```

4、重新启动jupyter notebook，可以看到界面上多了一个Nbextensions标签页，进入该标签页并取消“disable configuration for nbextensions without explicit compatibility (they may break your notebook environment, but can be useful to show for nbextension development)”，然后勾选上 “Codefolding” （折叠代码）和 “Hinterland” （自动补全），如下图：

<img src="Python%E7%9A%84%E7%AC%94%E8%AE%B0%E7%A5%9E%E5%99%A8-Jupyter-Notebook.assets/%E6%88%AA%E5%B1%8F2021-02-04%20%E4%B8%8B%E5%8D%8812.51.01.png" alt="截屏2021-02-04 下午12.51.01" style="zoom:50%;" />



## 命令行的基本使用

可以通过命令行管理已打开的jupyter notebook，常用的命令如下：

1、查看命令帮助

```
jupyter-notebook -h
jupyter-notebook --help
# 以下命令查看更为详细的帮助信息
jupyter-notebook --help-all
```

2、列出当前打开的notebook的信息

```
% jupyter-notebook list
Currently running servers:
http://localhost:8888/?token=dea62727318e8df4ec56c0451d2356a30a9f06ed32d38132 :: /Users/lhj/dev/projects/ml_time
```

3、关闭指定端口的notebook应用

```
% jupyter-notebook stop 8888
```

4、给notebook应用添加服务密码

```
% jupyter-notebook password
```

注意：添加了密码后，会创建一个配置文件存储登陆密码，新创建的jupyter notebook在浏览器打开时会要求输入密码才能访问；如果需要取消登陆密码，将生成的这个配置文件删除即可。

## 配置多环境支持

如果我们有多个python环境（使用anaconda创建）时，一方面可以在每个环境都安装jupyter，通过切换环境启动来支持多环境使用的问题。不过还有一种更为高级的方式，就是通过配置让某个环境的jupyter同时支持多个python环境，具体操作步骤如下：

1、激活python虚拟环境，例如：conda activate 环境名称

2、执行以下命令添加共享：python -m ipykernel install --name 环境名称

3、这时候在base环境打开jupyter，在新建那里就可以看到添加的tf环境选项了，如下图：

<img src="Python%E7%9A%84%E7%AC%94%E8%AE%B0%E7%A5%9E%E5%99%A8-Jupyter-Notebook.assets/%E6%88%AA%E5%B1%8F2021-02-04%20%E4%B8%8B%E5%8D%8812.30.45.png" alt="截屏2021-02-04 下午12.30.45" style="zoom:50%;" />



还有一个更直接和便捷的方式，就是在环境创建完成以后一次性添加所有环境，在base执行以下命令：

```
conda install nb_conda
```



**注意：如果mac提示：Permission denied: '/usr/local/share'，需要按以下步骤放开相应目录的权限：**

1、关闭Rootless

（1）重启电脑，并在电脑重启时按 “command+R” 或 “command+option+R” 进入恢复分区（M1芯片的操作模式有所不同，是在关机后一直按着电源键-也就是指纹的那个键，一直到选项按钮出现）；

（2）用鼠标点击“选项”，然后点“继续”；等出来的恢复页面上选择用户，输入密码后进入到恢复OS状态；

（3）点击上方菜单的“实用工具”，打开“终端”；

（4）输入以下命令关闭Rootless：csrutil disable

（5）等待命令结束重启电脑；

2、输入以下命令对目录进行当前用户的授权：

```
sudo chown -R $(whoami) /usr/local/
```

3、执行你想要的具体操作；

4、重新启用Rootless，按关闭的步骤打开恢复OS的终端，执行以下命令恢复： csrutil enable

## 简单使用示例

1、在命令行跳转到要使用的路径，然后启动notebook：

```
% cd ~/dev/projects/ml_time
% jupyter notebook
```

2、选择“新建 - 要运行的环境”，新建一个notebook文件：

<img src="Python%E7%9A%84%E7%AC%94%E8%AE%B0%E7%A5%9E%E5%99%A8-Jupyter-Notebook.assets/%E6%88%AA%E5%B1%8F2021-02-04%20%E4%B8%8B%E5%8D%881.03.01.png" alt="截屏2021-02-04 下午1.03.01" style="zoom:50%;" />

3、下面我们以建立一个notebook为例说明具体步骤，最后建成的结果如下图：

<img src="Python%E7%9A%84%E7%AC%94%E8%AE%B0%E7%A5%9E%E5%99%A8-Jupyter-Notebook.assets/%E6%88%AA%E5%B1%8F2021-02-04%20%E4%B8%8B%E5%8D%882.33.50.png" alt="截屏2021-02-04 下午2.33.50" style="zoom:50%;" />

（1）通过工具栏 “+” 或者菜单 “插入” 可以添加代码块，整个notebook实际上就是一个按顺序的代码块集合；

（2）每个代码块的类型可以是代码，也可以是文本（markdown格式），可以通过工具栏上的下拉菜单调整当前代码块的类型；

（3）我们按照上图的形式逐个代码块进行编辑，可以完成测试笔记的编辑；

（4）可以通过工具栏保存笔记，或者通过菜单 “文件 -> 重命名” 修改所保存的文件名。

4、运行笔记代码，可以将notebook的代码运行理解为在python命令行逐行执行代码，因此只要不重启，变量状态是一直保留的，某些代码块可以人为控制重复执行多次观察执行结果；可以通过工具栏的 “运行” 图标执行当前的代码块，也可以通过双箭头图标重启并一次性运行所有代码块，例如以上示例运行后的结果如下：

<img src="Python%E7%9A%84%E7%AC%94%E8%AE%B0%E7%A5%9E%E5%99%A8-Jupyter-Notebook.assets/%E6%88%AA%E5%B1%8F2021-02-04%20%E4%B8%8B%E5%8D%882.51.55.png" alt="截屏2021-02-04 下午2.51.55" style="zoom:50%;" />

5、另外也可以通过菜单 “服务 -> 改变服务” 修改当前notebook的运行环境，切换到其他环境上。

