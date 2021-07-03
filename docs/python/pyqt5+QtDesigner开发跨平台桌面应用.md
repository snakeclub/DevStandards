# pyqt5+QtDesigner开发跨平台桌面应用

# 安装及部署环境

1、安装pyqt5

```
pip install pyqt5
```

2、安装 PyQt5-stubs, 让 vscode 可以正常代码提示：

```
pip install PyQt5-stubs
```

3、安装Qt Designer（界面设计工具）

直接下载安装：https://build-system.fman.io/qt-designer-download



# 简单开发示例

## 通过Qt Designer设计界面

1、打开 Qt Designer 应用；

2、先创建一个Main Window（主窗口），如下图：

<img src="pyqt5+QtDesigner%E5%BC%80%E5%8F%91%E8%B7%A8%E5%B9%B3%E5%8F%B0%E6%A1%8C%E9%9D%A2%E5%BA%94%E7%94%A8.assets/image-20210622120217690.png" alt="image-20210622120217690" style="zoom:33%;" />

3、修改窗口属性，例如修改 “windowTitle” 的值为“主窗口”；

4、从左边的控件栏位拖动一个 “Label” 到窗口中，修改文字为 “输入框”；

5、从左边的控件栏位拖动一个 “Line Edit” 到窗口中，并修改该控件的属性值 “text” 为 “默认文本”；

6、从左边的控件栏位拖动一个 “Push Button” 到窗口中，并修改该控件的属性值 “text” 为 “按钮”；

7、保存当前界面设计，保存后文件名为 “main_window.ui”， 界面如下：

<img src="pyqt5+QtDesigner%E5%BC%80%E5%8F%91%E8%B7%A8%E5%B9%B3%E5%8F%B0%E6%A1%8C%E9%9D%A2%E5%BA%94%E7%94%A8.assets/image-20210622121703881.png" alt="image-20210622121703881" style="zoom: 50%;" />

## 转换界面设计为代码

可以通过pyqt5自带的工具将 “.ui” 设计转换为python代码，命令如下：

```
python -m PyQt5.uic.pyuic main_window.ui -o main_window.py
```

生成的界面代码如下：

```
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(320, 240)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 40, 60, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(100, 40, 161, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(100, 80, 113, 32))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 320, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "主窗口"))
        self.label.setText(_translate("MainWindow", "输入框"))
        self.lineEdit.setText(_translate("MainWindow", "默认文字"))
        self.pushButton.setText(_translate("MainWindow", "按钮"))
```

## 开发示例应用

在ui代码相同目录下建 demo.py 主程序，代码如下：

```
# -*- coding: utf-8 -*-

import sys
from typing import get_origin
from PyQt5 import QtWidgets
import main_window  # 加载生成的ui代码


def buttonClicked(girl):
    # 点击按钮事件，提示文本框内容
    QtWidgets.QMessageBox.information(None, '提示', girl.lineEdit.text())


if __name__ == '__main__':
    # 创建一个应用对象
    _app = QtWidgets.QApplication(sys.argv)
    # 创建QT主窗口对象
    _main_win = QtWidgets.QMainWindow()
    # 创建设计好的UI对象
    _ui = main_window.Ui_MainWindow()
    # 调用setupUi方法，将设计好的界面加载至主窗口上
    _ui.setupUi(_main_win)

    # 为按钮绑定事件
    _ui.pushButton.clicked.connect(lambda: buttonClicked(_ui))

    # 显示一个非模式的对话框，用户可以随便切窗口，.exec()是模式对话框，用户不能随便切
    _main_win.show()

    sys.exit(_app.exec_())

```

## 运行示例应用

执行以下命令进行运行：

```
python demo.py
```



# Qt Designer使用技巧

## 窗口类型选择（windowModality）

对于窗口类，可以设置windowModality属性，支持3种类型：

- Qt.NonModal : 不是模式窗口（正常应选择该类型）
- Qt.WindowModal : 单窗口层次结构模式，该模式会阻塞所有上级窗口和兄弟窗口的输入（类似对话框）
- Qt.ApplicationModal : 应用窗口模式，该模式会阻塞应用的所有其他窗口的输入



## Dialog、Widget、MainWindow使用

MainWindow ： 功能最完整的窗口类型，可以有menu菜单、tool工具栏、status状态栏、电脑显示屏右下脚的托盘等

Dialog : 对话框窗口，支持exec函数，如果通过该函数打开，则其父窗口不可选；不过如果通过show函数打开，所展示的窗口也可以被选择

Widget ： 窗口组件，主要是在上面放置布局和控件，是所有用户界面对象的基类。窗口部件是用户界面的一个基本单元：它从窗口系统接收鼠标、键盘和其它事件，并且在屏幕上绘制自己。每一个窗口部件都是矩形的，并且它们按Z轴顺序排列。一个窗口部件可以被它的父窗口部件或者它前面的窗口部件盖住一部分。



## 布局管理





管理团队共29人，分为RD产品研发、PD产品创新、售前管理、运营管理4个L4部门，各部门的职责、人员情况说明如下：

u RD产品研发部：共16人，主要负责国际结算及贸易金融相关系统的产品研发，以及新技术的研究、应用和推广工作；

u PD产品创新部：共8人，主要负责国际结算及贸易金融领域的产品创新管理，包括政策法规解读、市场调研、产品设计、产品推广等工作；

u 售前管理部：共2人，主要负责部门各产品条线的售前支持，包括配合销售部门的客户交流、POC测试、项目投标、客户关系维护等工作；

u 运营管理部：共3人，主要负责部门日常的运营管理，包括运营数据收集及分析、日常事务支持等工作。

 

交付团队共445人，分为DEL1、DEL2、DEL3、DEL4、SCF五个L4交付部门，各部门的职责、人员情况说明如下：

u DEL1：共82人，负责部门相关产品在华北地区范围及重点客户的现场交付工作，主要客户包括华夏、民生、邮储及华北区域范围的金融客户；

u DEL2：共144人，负责部门相关产品在华中地区、华西地区的现场交付工作，主要负责湖南、山东、河北、广西、四川、陕西等省份的金融客户；

u DEL3：共102人，负责部门相关产品在华南地区的现场交付工作，主要客户为广发、广农商等；

u DEL4：共83人，负责部门相关产品在华东地区的现场交付工作，主要负责江西、江苏、安徽、福建、上海、台湾等省份的金融客户；

u SCF：共34人，负责供应链金融、保理业务领域的解决方案研发及相应的项目交付工作，目前主要客户为保理公司等泛金融机构。