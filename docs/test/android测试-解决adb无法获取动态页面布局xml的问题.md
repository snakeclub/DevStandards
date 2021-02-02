# 解决adb无法获取动态页面布局XML的问题

在测试中可以通过以下命令获取Android页面布局的XML文件：

```
# 生成当前页面的布局xml文件
adb shell /system/bin/uiautomator dump --compressed /data/local/tmp/uidump.xml
#  将文件导出到电脑指定文件夹
adb pull /data/local/tmp/uidump.xml C:/Users/14133/Desktop
```

但是该方法有两个比较重大的缺点：

1、命令耗时比较长，导出一个文件差不多要几秒钟；

2、对于不停刷新的页面，由于 dump 只会在 idle 的情况才抓取页面，因此会存在无法获取页面布局文件的问题。

经过查阅互联网上的资料，发现 uiautomator 的 dumpWindowHierarchy 方法可以得到动态界面的信息，因此可以通过 uiautomator 自动测试的方法实现获取动态页面布局xml的效果。

## 开发环境准备

1、安装 jdk1.8 并添加环境变量，要求可以正常执行 java 和 javac 命令（具体配置方法请百度）；

2、安装 **ADT Bundle** 

ADT Bundle包含了Eclipse、ADT插件和SDK Tools，是已经集成好的IDE，只需安装好Jdk即可开始开发，推荐初学者下载ADT Bundle，不用再折腾开发环境

下载页面：http://tools.android-studio.org/index.php

3、升级 ant 插件

ADT Bundle 自带的 ant 插件版本较低，不支持 jdk 1.8，因此需要到官网下载最新的版本进行替换：

（1）官网地址：http://ant.apache.org/bindownload.cgi

（2）可以下载 1.10.9 版本，zip后缀的文件；

（3）解压后，将对应的文件夹和文件覆盖到 adt bunndle 中 eclipse 的ant插件目录，例如：D:\adt-bundle-windows-x86_64-20140702\eclipse\plugins\org.apache.ant_1.8.3.v201301120609

## 创建工程

1、打开 eclipse，选择菜单“File -> New -> Java Project”，填入以下信息，然后点击 Finish 按钮创建工程：

<img src="android%E6%B5%8B%E8%AF%95-%E8%A7%A3%E5%86%B3adb%E6%97%A0%E6%B3%95%E8%8E%B7%E5%8F%96%E5%8A%A8%E6%80%81%E9%A1%B5%E9%9D%A2%E5%B8%83%E5%B1%80xml%E7%9A%84%E9%97%AE%E9%A2%98.assets/image-20210110103025621.png" alt="image-20210110103025621" style="zoom: 50%;" />

**注：如果涉及中文，请将项目编码设置为utf-8，在项目上点击鼠标右键，选择 properties，在弹出的界面上选择。**

2、在左边工程结构树上点击鼠标右键，选择 “Build Path -> configure Build Path...”，点击 “Add Library...” 按钮，添加JUnit，我们选择的是JUnit4版本：

<img src="android%E6%B5%8B%E8%AF%95-%E8%A7%A3%E5%86%B3adb%E6%97%A0%E6%B3%95%E8%8E%B7%E5%8F%96%E5%8A%A8%E6%80%81%E9%A1%B5%E9%9D%A2%E5%B8%83%E5%B1%80xml%E7%9A%84%E9%97%AE%E9%A2%98.assets/image-20210110103410824.png" alt="image-20210110103410824" style="zoom:50%;" />

3、点击 “Add External JARs...” 按钮，将对应Android版本的“android.jar”和“uiautomator.jar”添加到项目中，这两个jar包路径参考 “D:\adt-bundle-windows-x86_64-20140702\sdk\platforms\android-20”：

<img src="android%E6%B5%8B%E8%AF%95-%E8%A7%A3%E5%86%B3adb%E6%97%A0%E6%B3%95%E8%8E%B7%E5%8F%96%E5%8A%A8%E6%80%81%E9%A1%B5%E9%9D%A2%E5%B8%83%E5%B1%80xml%E7%9A%84%E9%97%AE%E9%A2%98.assets/image-20210110103720720.png" alt="image-20210110103720720" style="zoom:50%;" />

## 编辑测试代码

1、在工程根目录上点击鼠标右键，选择 “New -> Package” ，添加包名（这里为“com.snaker.testtools”），然后点击Finish按钮完成包的添加：

<img src="android%E6%B5%8B%E8%AF%95-%E8%A7%A3%E5%86%B3adb%E6%97%A0%E6%B3%95%E8%8E%B7%E5%8F%96%E5%8A%A8%E6%80%81%E9%A1%B5%E9%9D%A2%E5%B8%83%E5%B1%80xml%E7%9A%84%E9%97%AE%E9%A2%98.assets/image-20210110115438359.png" alt="image-20210110115438359" style="zoom:50%;" />



2、在刚才添加的包上点击鼠标右键，选择“New -> Class”，添加类名（这里为“uiDumpXml”），然后点击Finish按钮完成添加：

<img src="android%E6%B5%8B%E8%AF%95-%E8%A7%A3%E5%86%B3adb%E6%97%A0%E6%B3%95%E8%8E%B7%E5%8F%96%E5%8A%A8%E6%80%81%E9%A1%B5%E9%9D%A2%E5%B8%83%E5%B1%80xml%E7%9A%84%E9%97%AE%E9%A2%98.assets/image-20210110115559798.png" alt="image-20210110115559798" style="zoom:50%;" />

3、在刚才创建的类中增加以下代码：

```java
package com.snaker.testtools;

import java.io.File;

import com.android.uiautomator.core.UiDevice;
import com.android.uiautomator.core.UiObjectNotFoundException;
import com.android.uiautomator.testrunner.UiAutomatorTestCase;


public class uiDumpXml extends UiAutomatorTestCase {

    public void testDumpHierarchy() throws UiObjectNotFoundException {
    	System.out.println("create dir");
    	File file = new File("/data/local/tmp/local/tmp");
    	if(!file.exists()){
    		file.mkdirs();
    	}
    	String realPath = "uidump.xml";
    	File filename = new File("/data/local/tmp/local/tmp/" + realPath);
    	if(filename.exists()){
    		filename.delete();
    	}
        UiDevice uiDevice = getUiDevice();
        uiDevice.dumpWindowHierarchy(realPath);
        System.out.println("dump end");
    }
}
```

注意：dumpWindowHierarchy方法存在一个bug，就是实际上生成文件目录在 “/data/local/tmp/local/tmp”下，但如果目录不存在也不会报错，所以需要判断目录是否存在，如不存在则需要创建目录。

4、我们顺便把屏幕快照的功能也加上，重复上面步骤，添加 uiScreenShot.java 类，代码如下：

```java
package com.snaker.testtools;

import java.io.File;

import android.os.Bundle;

import com.android.uiautomator.core.UiDevice;
import com.android.uiautomator.core.UiObjectNotFoundException;
import com.android.uiautomator.testrunner.UiAutomatorTestCase;

public class uiScreenShot extends UiAutomatorTestCase {

    public void testScreenShot() throws UiObjectNotFoundException {
    	// 支持传入参数
    	Bundle runPara = getParams();
    	String filename = runPara.getString("filename");  // 保存文件名
    	if(filename==null){
    		filename = "uiShot.png";
    	}
    	String scale = runPara.getString("scale"); // 截图大小比例，默认为1.0
    	if(scale == null){
    		scale = "1.0";
    	}
    	String quality = runPara.getString("quality");  // 压缩质量，最高为100
    	if (quality==null){
    		quality = "100";
    	}
    	
    	System.out.println("create dir");
    	File file = new File("/data/local/tmp/");
    	if(!file.exists()){
    		file.mkdirs();
    	}
        UiDevice uiDevice = getUiDevice();
        File pic = new File("/data/local/tmp/" + filename);
        if (pic.exists()){
        	// 如果文件存在，则进行删除
        	pic.delete();
        }
        uiDevice.takeScreenshot(pic, Float.parseFloat(scale), Integer.parseInt(quality));
        System.out.println("screen shot end");
    }
}
```

5、进入 “D:\adt-bundle-windows-x86_64-20140702\sdk\tools” 目录，运行命令：android list，找到对应的SDK id号（我们选1）：

```
> cd D:\adt-bundle-windows-x86_64-20140702\sdk\tools
> android list
Available Android targets:
----------
id: 1 or "android-14"
     Name: Android 4.0
     Type: Platform
     API level: 14
     Revision: 4
     Skins: HVGA, QVGA, WQVGA400, WQVGA432, WSVGA, WVGA800 (default), WVGA854, WXGA720, WXGA800
 Tag/ABIs : default/armeabi-v7a
----------
id: 2 or "android-21"
     Name: Android 5.0.1
     Type: Platform
     API level: 21
     Revision: 2
     Skins: HVGA, QVGA, WQVGA400, WQVGA432, WSVGA, WVGA800 (default), WVGA854, WXGA720, WXGA800, WXGA800-7in
 Tag/ABIs : no ABIs.
```

5、执行以下命令创建 build 配置文件：

android create uitest-project -n <**name**> -t <**android-sdk-ID**>  -p <**path**>
注：name为将来生成的jar包的名字，**可以自定义**，android-sdk-ID为上一步的id，path是当前项目的路径

```
android create uitest-project -n UiTestTools -t 1 -p D:\workspace\uiautomatorDumpXml
```

执行完成后在工程上点击鼠标右键，点击 Reflesh 菜单，能看到工程中增加了 build.xml 文件。

6、编辑 build.xml 文件，

将开头的`<project name="UiTestTools" default="help">` 修改为 `<project name="UiTestTools" default="build">` 



## 进行编译

进入工程目录，通过ant进行编译，具体命令如下：

```
> cd d:\workspace\uiautomatorDumpXml
> D:\adt-bundle-windows-x86_64-20140702\eclipse\plugins\org.apache.ant_1.8.3.v201301120609\bin\ant build
```

如果成功编译，将在 d:\workspace\uiautomatorDumpXml\bin\ 目录下生成 UiTestTools.jar 文件。



## 其他扩展功能

### 连续滑动支持（解锁九宫格）

```java
package com.snaker.testtools;

import android.os.Bundle;
import android.graphics.Point;

import com.android.uiautomator.core.UiDevice;
import com.android.uiautomator.core.UiObjectNotFoundException;
import com.android.uiautomator.testrunner.UiAutomatorTestCase;


public class uiSwipe extends UiAutomatorTestCase {

    public void testSwipe() throws UiObjectNotFoundException {
    	// 获取要滑动的参数
    	Bundle runPara = getParams();
    	String seconds = runPara.getString("seconds");  // 总共滑动花费时长，单位为秒
    	if (seconds == null){
    		seconds = "0.5";
    	}
    	int segmentSteps = (int)(Float.parseFloat(seconds) * 100.0f / 5.0f);
    	// System.out.println(seconds);
    	
    	String points = runPara.getString("points");  // x1,y1-x2,y2-... 格式
    	// System.out.println(points);
    	if (points == null){
    		// 没有指定点，直接不操作
    		return;
    	}
    	String[] temps = points.split("-");
    	// 组织节点
    	Point[] segments = new Point[temps.length];
    	for(int i=0;i<temps.length;i++){
    		String[] temps_point = temps[i].split(",");
    		segments[i] = new Point();
    		segments[i].x = Integer.parseInt(temps_point[0]);
    		segments[i].y = Integer.parseInt(temps_point[1]);
    	}
    	
        UiDevice uiDevice = getUiDevice();
        uiDevice.swipe(segments, segmentSteps);
        System.out.println("swipe end");
    }
}
```

### 查找并点击指定控件

```java
package com.snaker.testtools;

import java.util.Set;

import android.graphics.Point;
import android.os.Bundle;

import com.android.uiautomator.core.UiDevice;
import com.android.uiautomator.core.UiObjectNotFoundException;
import com.android.uiautomator.testrunner.UiAutomatorTestCase;
import com.android.uiautomator.core.UiObject;
import com.android.uiautomator.core.UiSelector;


public class uiClickControl extends UiAutomatorTestCase {

    public void testClickControl() throws UiObjectNotFoundException {
    	// 获取要查找对象的参数
    	UiSelector selector = new UiSelector();
    	Bundle runPara = getParams();
    	Set<String> keys = runPara.keySet();
    	for (String key : keys) {
    		System.out.println(key + ": " + runPara.getString(key));
    		if(key == "text"){
    			selector = selector.text(runPara.getString(key));
    		} else if(key == "className") {
    			selector = selector.className(runPara.getString(key));
    		} else if(key == "desc"){
    			selector = selector.description(runPara.getString(key));
    		}
    	}
    	
    	UiObject uiObject = new UiObject(selector);
    	if (uiObject.exists()){
    		uiObject.click();
    	}
    	else{
    		throw new UiObjectNotFoundException("control not found");
    	}
        System.out.println("click control end");
    }
}
```



## 如何使用

1、将手机连上电脑，将编译后的 jar 文件（实际上是一个测试案例）放入手机中：

```
> cd d:\workspace\uiautomatorDumpXml
> adb push bin\UiTestTools.jar /data/local/tmp/
```

2、执行 dump xml的命令：

```
> adb shell uiautomator runtest UiTestTools.jar -c com.snaker.testtools.uiDumpXml
```

3、将xml文件获取到电脑指定目录：

```
> adb pull /data/local/tmp/local/tmp/uidump.xml d:/douyin/temp/
```

4、执行截图命令

```
> adb shell uiautomator runtest UiTestTools.jar -c com.snaker.testtools.uiScreenShot && adb pull /data/local/tmp/uiShot.png d:/douyin/temp/
```

支持通过 -e 传入参数，参数包括：

filename - 指定截图的文件名（不支持路径调整）

scale - 截图比例，默认为1.0

quality - 图像压缩比例，默认为100

```
> adb shell uiautomator runtest UiTestTools.jar -e filename uiShot.png scale 1.0 quality 70 -c com.snaker.testtools.uiScreenShot
```

5、执行连续滑动处理

支持传入的参数：

points：格式为x1,y1-x2,y2-x3,y3-...

seconds: 整个操作耗时时长

```
> adb shell uiautomator runtest UiTestTools.jar -e points 300,500-300,800-300,400 -e seconds 1.0 -c com.snaker.testtools.uiSwipe
```

6、点击指定控件

支持传入参数：

text: 按text属性查找

className: 按class属性查找

desc: 按content-desc属性查找

```
> adb shell uiautomator runtest UiTestTools.jar -e text "说点什么..." -e className "android.widget.TextView" -c com.snaker.testtools.uiClickControl
```

