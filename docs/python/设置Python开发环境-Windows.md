# 设置Python开发环境（Windows）

## 前提条件

- 安装Python3.6版本，下载地址：https://www.python.org/downloads/windows/

- 安装VSCode最新版本，下载地址：https://code.visualstudio.com/Download

- 在VSCode安装以下插件，如果服务器不能联网，下载以下VSCode的插件离线安装：

  Python ：https://marketplace.visualstudio.com/items?itemName=ms-python.python

  Guides ：https://marketplace.visualstudio.com/items?itemName=spywhere.guides

  vscode-icons : https://marketplace.visualstudio.com/items?itemName=robertohuertasm.vscode-icons

  autoDocstring  :  https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring

  离线安装命令（先转到插件目录）：code --install-extension spywhere.guides-0.9.2.vsix

- 安装以下Python库，如果服务器不能联网，通过能联网的电脑下载以下的Python库安装包并安装：

  pylint

  autopep8

  flake8

  yapf

- 下载Python库安装包的方法如下

  建立要保存安装包的目录，例如：C:\Python3\package

  在联网机通过pip打包文件：pip download -d C:\Python3\package pylint 

  在离线机安装文件：pip install --no-index --find-links=C:\Python3\package pylint 



## vscode-icons生效

在 **File > Preferences > File Icon Theme > VSCode Icons** 进行设置。



### flake8生效

打开VScode，文件->首选项->用户设置，在settings.json文件中输入"python.linting.flake8Enabled": true



### 切换格式化工具（autopep8或yapf）

打开VScode，文件->首选项->用户设置，在settings.json文件中输入"python.formatting.provider"，指定格式化工具：

autopep8 ： "python.formatting.provider": "autopep8" 

yapf ："python.formatting.provider": "yapf"   -- 测试过程中发现yapf似乎有问题



## DocString代码注释文档工具

可以从VSCode的市场中获取扩展插件安装包autoDocstring，可以支持google 、sphinx 、numpy 和其自身的一种注释格式，使用方法也很简单，可以通过以下3种方式生成注释：

- 在定义语句后面的空行，点击鼠标右键，选择“Generate Docstring”菜单
- 鼠标点击在定义语句后面的空行，按快捷键`ctr+shift+2`
- 在定义语句后面的空行输入“”“，然后回车



如果想自己修改风格，可以到作者的Github获取源码：https://github.com/NilsJPWerner/autoDocstring.git



另外如果需要遵循snakerpy规范（参考JSDoc），可以到本作者的GitHub获取源码及安装包（从autoDocstring拆出的一个分支版本）：https://github.com/snakeclub/autoDocstring.git



## User Setting

从菜单”File->Preferences->User Settings“打开，中文菜单是”文件->首选项->设置“，搜索并自定义以下项（全部修改的配置信息可以直接从”[vscode-python-user-setting.json](media/vscode-python-setting-win/vscode-python-user-setting.json)“获取）：

### python.formatting.autopep8Args

```
// python的autopep8格式化，限制最大宽度是100字符，缩进为4个空格
"python.formatting.autopep8Args": [
  "--max-line-length=100",
  "--indent-size=4"
]
```

### python.linting.flake8Args

```
// 设置flake8的参数，现在最大宽度是100字符
"python.linting.flake8Args": [
    "--max-line-length=100"
]
```



### editor.formatOnSave

```
// 保存时设置文件的格式。格式化程序必须可用，不能自动保存文件，并且不能关闭编辑器。
"editor.formatOnSave": true
```

### python.linting.pylintArgs

```
// 设置了pylint一些警告、错误提示的参数
"python.linting.pylintArgs": [
  "--include-naming-hint=n",
  "--disable=W0311",
  "--disable=C0103",
  "--disable=E1101"
]
```

### files.trimTrailingWhitespace

```
// 启用后，将在保存文件时剪裁尾随空格。
"files.trimTrailingWhitespace": true
```

### editor.tabSize

```
// 一个制表符等于的空格数。该设置在 "editor.detectIndentation" 启用时根据文件内容可能会被覆盖。
"editor.tabSize": 4
```

### files.exclude

注意这里是增加合并类型，不是直接替换

```
// 配置 glob 模式以在搜索中排除文件和文件夹。例如，文件资源管理器根据此设置决定文件或文件夹的显示和隐藏。
    "files.exclude": {
    ".vs*": true,
    "*.*~": true,
    "*.pyc": true,
    "*/*.pyc": true
}
```

### files.autoSave

```
// 控制何时自动保存已更新文件
"files.autoSave": "onWindowChange"
```

 

## Snippets代码片段

我们可以在VS Code上自行设置Snippets，实现输入自动提示和补充代码。比如我们输入for，在提示框中选择对应的snippet：

![](media/vscode-python-setting-win/1.png)

点击回车或者tab，就变成了：

```
for target_list in expression_list:
  pass
```

我们如果要定义自己的Snippets，比如我们想要快速输入for xx in enumerator()方式遍历，该如何做呢。首先打开文件—首选项—用户代码片段。vscode会提示你选择语言，我们输入Python并回车，打开了python.json。内容格式为json，在根级下面新增一个自己的object，内容如下：

```
"For in enumerator": {
    "prefix": "for/enum",
    "body": [
      "for ${1:index}, ${2:item} in enumerate(${3:array}):",
      "  ${4:pass}"
    ],
    "description": "For statement with enumerator"
  }
```

这样在我们输入for/enum再按回车后，就自动生成了：

```
 for target_list in expression_list:
  pass
```

光标停留在index上并选中该词，我们可以直接修改完，按tab切换到item，然后是array、pass。



## VS Code常用快捷键

| 按 Press             | 功能 Function                                               |
| -------------------- | :---------------------------------------------------------- |
| Ctrl+X               | 剪切行（空选定） Cut line (empty selection)                 |
| Ctrl+C               | 复制行（空选定）Copy line (empty selection)                 |
| Alt+ ↑ / ↓           | 向上/向下移动行 Move line up/down                           |
| Shift+Alt + ↓ / ↑    | 向上/向下复制行 Copy line up/down                           |
| Ctrl+Shift+K         | 删除行 Delete line                                          |
| Ctrl+] / [           | 缩进/缩进行 Indent/outdent line                             |
| Ctrl+Shift+[         | 折叠（折叠）区域 Fold (collapse) region                     |
| Ctrl+Shift+]         | 展开（未折叠）区域 Unfold (uncollapse) region               |
| Ctrl+K Ctrl+[        | 折叠（未折叠）所有子区域 Fold (collapse) all subregions     |
| Ctrl+K Ctrl+]        | 展开（未折叠）所有子区域 Unfold (uncollapse) all subregions |
| Ctrl+K Ctrl+0        | 折叠（折叠）所有区域 Fold (collapse) all regions            |
| Ctrl+K Ctrl+J        | 展开（未折叠）所有区域 Unfold (uncollapse) all regions      |
| Ctrl+K Ctrl+C        | 添加行注释 Add line comment                                 |
| Ctrl + F             | 查找 Find                                                   |
| Ctrl + H             | 替换 Replace                                                |
| F3 / Shift + F3      | 查找下一个/上一个 Find next/previous                        |
| Ctrl + 空格          | 触发建议 Trigger suggestion                                 |
| Ctrl + Shift + Space | 触发器参数提示 Trigger parameter hints                      |
| Tab                  | Emmet 展开缩写 Emmet expand abbreviation                    |
| Shift + Alt + F      | 格式化文档 Format document                                  |
| Ctrl + K Ctrl + F    | 格式选定区域 Format selection                               |
| Ctrl+N               | 新文件 New File                                             |
| Ctrl+O               | 打开文件... Open File...                                    |
| Ctrl+S               | 保存 Save                                                   |
| Ctrl+Shift+S         | 另存为... Save As...                                        |
| Ctrl+K S             | 全部保存 Save All                                           |
| Ctrl+F4              | 关闭 Close                                                  |
| F9                   | 切换断点 Toggle breakpoint                                  |
| F5                   | 开始/继续 Start/Continue                                    |
| Shift+F5             | 停止 Stop                                                   |
| F11 / Shift+F11      | 下一步/上一步 Step into/out                                 |
| F10                  | 跳过 Step over                                              |
| Ctrl+K Ctrl+I        | 显示悬停 Show hover                                         |

## 作者推荐安装的Snippets代码片段

[keybindings.json](keybindings.json) ：

修改位置：文件>首选项>按键快捷方式

- ctrl+shift+3 : 调出注释标签选择菜单（可以在鼠标定位在注释中执行）
- ctrl+shift+4 : 调出数据类型（type）选择菜单（可以在鼠标定位在注释中执行）
- ctrl+shift+5 : 调出异常类型（exception）选择菜单（可以在鼠标定位在注释中执行）

[python.json](python.json)

修改位置：文件>首选项>用户代码片段，然后选择python.json

- 输入“.c”获取代码片段（c代表code）
- 输入“.n”获取注释片段（n代表note）