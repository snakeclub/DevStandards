# android测试-基于minicap和minitouch进行安卓手机Web端控制

## minicap简单应用

minicap属于STF框架的一个工具，可以高速截图、同步手机屏幕至浏览器等功能。在这个章节我们进行minicap的简单部署和应用。

源码：https://github.com/openstf/minicap

### 操作步骤

1、连接手机，开启USB调试模式；

2、执行以下命令查看手机CPU的架构、android版本、分辨率等信息：

```
> adb shell getprop ro.product.cpu.abi
arm64-v8a

> adb shell getprop ro.build.version.sdk
28

> adb shell wm size
Physical size: 1440x2560
```

我的测试机是 arm64-v8a 架构的，以这个为例执行下面的步骤。

3、下载minicap源码执行编译（具体编译方法参考github说明），不过我们可以偷懒拿已经编译好的版本，这样自己可以省去搭建编译环境的时间：

（1）到网易的开源测试框架Airtest官网：http://airtest.netease.com/ ， 下载 Airtest IDE 包；

（2）进入压缩包中的 “AirtestIDE\airtest\core\android\static\stf_libs” 目录，找到自己手机的CPU架构目录，获取 minicap 文件；

**注：如果你的SDK版本 < 16 ，要使用 minicap-nopie。**

（3）进入压缩包中的 “AirtestIDE\airtest\core\android\static\stf_libs\minicap-shared\aosp\libs\android-28\arm64-v8a” 目录，找到自己手机的android版本目录，获取 minicap.so 文件；

4、推送 minicap，minicap.so 两个文件到手机中：

```
adb push minicap /data/local/tmp
adb push minicap.so /data/local/tmp
```

5、对文件进行赋权：

```
adb shell chmod 777 /data/local/tmp/minicap
adb shell chmod 777 /data/local/tmp/minicap.so
```

6、测试是否可以正常运行（分辨率使用前面查到的屏幕大小）：

```
> adb shell LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -P 1440x2560@1440x2560/0 -t
PID: 15887
INFO: Using projection 1440x2560@1440x2560/0
INFO: (external/MY_minicap/src/minicap_28.cpp:241) Creating SurfaceComposerClient
INFO: (external/MY_minicap/src/minicap_28.cpp:244) Performing SurfaceComposerClient init check
INFO: (external/MY_minicap/src/minicap_28.cpp:255) Creating virtual display
INFO: (external/MY_minicap/src/minicap_28.cpp:261) Creating buffer queue
INFO: (external/MY_minicap/src/minicap_28.cpp:264) Setting buffer options
INFO: (external/MY_minicap/src/minicap_28.cpp:268) Creating CPU consumer
INFO: (external/MY_minicap/src/minicap_28.cpp:272) Creating frame waiter
INFO: (external/MY_minicap/src/minicap_28.cpp:276) Publishing virtual display
INFO: (jni/minicap/JpgEncoder.cpp:64) Allocating 11061252 bytes for JPG encoder
INFO: (external/MY_minicap/src/minicap_28.cpp:291) Destroying virtual display
OK
```

7、端口映射，把minicap映射到1717端口，也可以是其他端口：

```
adb forward tcp:1717 localabstract:minicap
```

adb forward 扩展：

```
# 查看已经映射的端口
adb forward --list
# 删除指定的映射
adb forward --remove tcp:11111
```

8、启动minicap服务：

```
adb shell LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -P 1440x2560@1440x2560/0
```

-P 后面的参数格式：{RealWidth}x{RealHeight}@{VirtualWidth}x{VirtualHeight}/{Orientation}
Orientation可以理解为手机的旋转角度，可选参数为 0 | 90 | 180 | 270

9、从以下地址下载 minicap 示例代码：https://github.com/openstf/minicap/tree/master/example ，关键是app.js 和 public 目录下的index.html；

10、启动Web服务（需要安装 node.js 环境）：

```
node app.js PORT=9002
```

注意，node.js 需要安装以下两个库：

```
npm install ws -g
npm install express -g
lodash
qs
npm install commander -g
```

11、通过浏览器访问：http://localhost:9002/ 即可看到同步屏幕的视频展示。



### 服务可支持的参数

```
fprintf(stderr,
    "Usage: %s [-h] [-n <name>]\n"
    "  -d <id>:       Display ID. (%d)\n"
    "  -n <name>:     Change the name of the abtract unix domain socket. (%s)\n"
    "  -P <value>:    Display projection (<w>x<h>@<w>x<h>/{0|90|180|270}).\n"
    "  -Q <value>:    JPEG quality (0-100).\n"
    "  -s:            Take a screenshot and output it to stdout. Needs -P.\n"
    "  -S:            Skip frames when they cannot be consumed quickly enough.\n"
    "  -r <value>:    Frame rate (frames/s)"
    "  -t:            Attempt to get the capture method running, then exit.\n"
    "  -i:            Get display information in JSON format. May segfault.\n"
    "  -h:            Show help.\n",
    pname, DEFAULT_DISPLAY_ID, DEFAULT_SOCKET_NAME
  );
```



### 高阶：Python利用minicap进行录屏

1、以下代码利用minicap持续进行截屏，并写入一个个jpg图片中：

```
# coding: utf8
import socket
import sys
import time
import struct
from collections import OrderedDict


class Banner:
    def __init__(self):
        self.__banner = OrderedDict(
            [('version', 0),
             ('length', 0),
             ('pid', 0),
             ('realWidth', 0),
             ('realHeight', 0),
             ('virtualWidth', 0),
             ('virtualHeight', 0),
             ('orientation', 0),
             ('quirks', 0)
             ])

    def __setitem__(self, key, value):
        self.__banner[key] = value

    def __getitem__(self, key):
        return self.__banner[key]

    def keys(self):
        return self.__banner.keys()

    def __str__(self):
        return str(self.__banner)

class Minicap(object):
    def __init__(self, host, port, banner):
        self.buffer_size = 4096
        self.host = host
        self.port = port
        self.banner = banner

    def connect(self):
        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except :
            print('2')
            sys.exit(1)
        self.__socket.connect((self.host, self.port))

    def on_image_transfered(self, data):
        file_name = str(time.time()) + '.jpg'
        with open(file_name, 'wb') as f:
            for b in data:
                f.write(b)

    def consume(self):
        readBannerBytes = 0
        bannerLength = 24
        readFrameBytes = 0
        frameBodyLength = 0
        data = []
        while True:
            try:
                chunk = self.__socket.recv(self.buffer_size)
            except:
                print('11')
                sys.exit(1)
            cursor = 0
            buf_len = len(chunk)
            while cursor < buf_len:
                if readBannerBytes < bannerLength:
                    map(lambda i, val: self.banner.__setitem__(self.banner.keys()[i], val),
                        [i for i in range(len(self.banner.keys()))], struct.unpack("<2b5ibB", chunk))
                    cursor = buf_len
                    readBannerBytes = bannerLength
                    print(self.banner)
                elif readFrameBytes < 4:
                    frameBodyLength += (struct.unpack('B', chunk[cursor])[0] << (readFrameBytes * 8)) >> 0
                    cursor += 1
                    readFrameBytes += 1
                else:
                    print("frame length:{0} buf_len:{1} cursor:{2}".format(frameBodyLength, buf_len, cursor))
                    # pic end
                    if buf_len - cursor >= frameBodyLength:
                        data.extend(chunk[cursor:cursor + frameBodyLength])
                        self.on_image_transfered(data)
                        cursor += frameBodyLength
                        frameBodyLength = readFrameBytes = 0
                        data = []
                    else:
                        data.extend(chunk[cursor:buf_len])
                        frameBodyLength -= buf_len - cursor
                        readFrameBytes += buf_len - cursor
                        cursor = buf_len

if '__main__' == __name__:
    print('开始')
    mc = Minicap('localhost', 1717, Banner())
    mc.connect()
    mc.consume()
```

2、下面的代码将持续的截屏转换为视频：

```
import cv2
import glob
import os
from datetime import datetime


def frames_to_video(fps, save_path, frames_path, max_index):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    videoWriter = cv2.VideoWriter(save_path, fourcc, fps, (960, 544))
    imgs = glob.glob(frames_path + "/*.jpg")
    frames_num = len(imgs)
    for i in range(max_index):
        if os.path.isfile("%s/%d.jpg" % (frames_path, i)):
            frame = cv2.imread("%s/%d.jpg" % (frames_path, i))
            videoWriter.write(frame)
    videoWriter.release()
    return


if __name__ == '__main__':
    t1 = datetime.now()
    frames_to_video(22, "result.mp4", 'face_recog_frames', 1000)
    t2 = datetime.now()
    print("耗时 ：", (t2 - t1))
    print("完成了 !!!")
```



## minitouch简单应用

minitouch提供了一个socket接口用来出来在Android设备上的多点触摸事件以及手势，它能够支持api 10以上的设备且不需要通过root。

源码：https://github.com/openstf/minitouch

### 操作步骤

1、连接手机，开启USB调试模式；

2、执行以下命令查看手机CPU的架构，以及安卓的sdk版本：

```
> adb shell getprop ro.product.cpu.abi
arm64-v8a

> adb shell getprop ro.build.version.sdk
28
```

我的测试机是 arm64-v8a 架构的，以这个为例执行下面的步骤。

3、下载minitouch源码执行编译（具体编译方法参考github说明），不过我们可以偷懒拿已经编译好的版本，这样自己可以省去搭建编译环境的时间：

（1）到网易的开源测试框架Airtest官网：http://airtest.netease.com/ ， 下载 Airtest IDE 包；

（2）进入压缩包中的 “AirtestIDE\airtest\core\android\static\stf_libs” 目录，找到自己手机的CPU架构目录，获取 minitouch 文件；

**注：如果你的SDK版本 < 16 ，要使用 minitouch-nopie。**

4、推送  minitouch 文件到手机中：

```
adb push minitouch /data/local/tmp
```

5、对文件进行赋权：

```
adb shell chmod 777 /data/local/tmp/minitouch
```

6、通过执行帮助查看文件是否可正常执行：

```
> adb shell /data/local/tmp/minitouch -h
Usage: /data/local/tmp/minitouch [-h] [-d <device>] [-n <name>] [-v] [-i] [-f <file>]
  -d <device>: Use the given touch device. Otherwise autodetect.
  -n <name>:   Change the name of of the abtract unix domain socket. (minitouch)
  -v:          Verbose output.
  -i:          Uses STDIN and doesn't start socket.
  -f <file>:   Runs a file with a list of commands, doesn't start socket.
  -h:          Show help.
```

7、端口映射，把minitouch映射到1111端口，也可以是其他端口：

```
adb forward tcp:1111 localabstract:minitouch
```

8、启动minitouch服务，以下命令启动一个socket的监听服务，需要通过网络方式编码进行请求执行：

```
adb shell /data/local/tmp/minitouch
```

9、安装 pyminitouch 尝试使用：

```
pip install pyminitouch
```

pyminitouch是使用python连接minitouch的一个实现，开源地址：https://github.com/williamfzc/pyminitouch

10、直接使用官方的开源网站的demo就可以进行操作，创建一个test.py文件，内容如下：

```
from pyminitouch import MNTDevice

_DEVICE_ID = 'WGY0217527000271'
device = MNTDevice(_DEVICE_ID)

# single-tap
device.tap([(400, 600)])
# multi-tap
device.tap([(400, 400), (600, 600)])
# set the pressure, default == 100
device.tap([(400, 600)], pressure=50)

# 可以直接用简洁的API调用minitouch提供的强大功能！

# 在使用完成后，需要显式调用stop方法将服务停止
device.stop()
```

11、执行该脚本：

```
python test.py
```

