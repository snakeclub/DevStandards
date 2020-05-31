# pyppeteer安装及代码参考手册

曾经使用模拟浏览器操作（selenium + webdriver）来写爬虫，但是稍微有点反爬的网站都会对selenium和webdriver进行识别，网站只需要在前端js添加一下判断脚本，很容易就可以判断出是真人访问还是webdriver。虽然也可以通过中间代理的方式进行js注入屏蔽webdriver检测，但是webdriver对浏览器的模拟操作（输入、点击等等）都会留下webdriver的标记，同样会被识别出来，要绕过这种检测，只有重新编译webdriver，麻烦自不必说，难度不是一般大。

作为selenium+webdriver的优秀替代，pyppeteer就是一个很好的选择。

开源地址：https://github.com/pyppeteer/pyppeteer

## 安装手册

**1、通过pip安装包**

```
pip install -i https://mirrors.aliyun.com/pypi/simple/ pyppeteer
```



**2、安装所需的chromium浏览器**

pyppeteer第一次运行时（运行官方的示例），会自动下载chromium浏览器，但国内由于墙的原因可能无法正常下载，遇到这样的情况需要手工处理，步骤如下：

（1）执行以下代码获取所需下载的chromium浏览器版本、安装路径、下载地址等信息，其中win64是操作系统版本，根据自身操作系统的类型也可以修改为linux、mac、win32等值：

```
import pyppeteer.chromium_downloader
print('默认版本是：{}'.format(pyppeteer.__chromium_revision__))
print('可执行文件默认路径：{}'.format(pyppeteer.chromium_downloader.chromiumExecutable.get('win64')))
print('win64平台下载链接为：{}'.format(pyppeteer.chromium_downloader.downloadURLs.get('win64')))
```

输出结果大致如下：

```
默认版本是：575458
可执行文件默认路径：C:\Users\Administrator\AppData\Local\pyppeteer\pyppeteer\local-chromium\575458\chrome-win32\chrome.exe
win64平台下载链接为：https://storage.googleapis.com/chromium-browser-snapshots/Win_x64/575458/chrome-win32.zip
```

（2）到国内镜像服务器下载指定版本的chromium包，需找到对应的操作系统（win64）和版本号（575458），下载地址：http://npm.taobao.org/mirrors/chromium-browser-snapshots/

（3）将下载号的包解压缩至 `C:\Users\Administrator\AppData\Local\pyppeteer\pyppeteer\local-chromium\575458\` 目录中，到这里安装完成。



注：如果你希望将pyppeteer的基本目录（包含chromium浏览器）安装在其他路径，例如d盘上，可以分别通过以下两种方式实现：

- 方法1：设置系统环境变量“PYPPETEER_HOME”，指向你希望放置的目录（例如D:\test\），设置后对应将chromium的程序放置到相应目录下，例如：D:\test\local-chromium\575458\chrome-win32\
- 方法2：在代码前面增加设置局部环境变量的脚本 `os.environ['PYPPETEER_HOME'] = 'D:\test'` ，指定对应的基路径，同样需要将chromium的程序放置到相应目录下，这种方法的缺点是要每次使用pyppeteer前都需要执行该脚本指定路径。



## 代码参考手册

### 官方hello world代码

```
import asyncio
from pyppeteer import launch
 
async def main():
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto('http://www.baidu.com/')
    await asyncio.sleep(100)
    await browser.close()
 
asyncio.get_event_loop().run_until_complete(main())
```



### 打开浏览器

打开浏览器是通过pyppeteer.launcher.launch(options: dict = None, **kwargs) 方法，运行该函数后，会得到一个pyppeteer.browser.Browser实例，也就是说浏览器对象实例。

```
browser = await launch(headless=False)
或
browser = await launch({headless=False, ignoreHTTPSErrors=False})
```

launch方法是必须使用的方法，官方参考文档：https://pyppeteer.github.io/pyppeteer/reference.html#launcher

- ignoreHTTPSErrors (bool): 是否忽略HTTPS错误，某些情况下应设置为False.
- headless (bool): 是否以无头模式（无界面模式）执行，默认为True，为True时是不会弹出可视界面的，所以，上面代码运行时设置headless=False。注意，下面还有个devtools参数，表示是否出现打开调试窗口，如果devtools设置为True，headless就算设置为False也会弹出可视界面。
- executablePath (str): Chromium或Chrome浏览器的可执行文件路径，如果设置，则使用设置的这个路径，不使用默认设置.
- slowMo (int|float): 设置这个参数可以延迟pyppeteer的操作，单位是毫秒.
- args (List[str]): 要传递给浏览器进程的一些其他参数.
- ignoreDefaultArgs (bool): 如果有些参数你不想使用默认值，那么，通过这个参数设置，不过最好别用
- handleSIGINT (bool): 是否响应 SIGINT 信号，是否允许通过快捷键Ctrl+C来终止浏览器进程，默认值为True，也就是允许.
- handleSIGTERM (bool): 是否响应 SIGTERM 信号，也就是说kill命令关闭浏览器，，默认值为True，也就是允许.
- handleSIGHUP (bool): 是否响应 SIGHUP 信号，即挂起信号，默认值为True，也就是允许.
- dumpio (bool): 是要将浏览器进程的输出传递给process.stdout 和 process.stderr 对象，默认为False不传递。
- userDataDir (str): 用户数据文件目录.
- env (dict): 以字典的形式传递给浏览器环境变量.
- devtools (bool): 是否打开调试窗口，上面介绍headless参数是说过，默认值为False不打开.
- logLevel (int|str): 日志级别，默认和 root logger 对象的级别相同.
- autoClose (bool): 当所有操作都执行完后，是否自动关闭浏览器，默认True，自动关闭.
- loop (asyncio.AbstractEventLoop): 时间循环。
- appMode (bool): Deprecated.



### 调整窗口大小

如果你运行了上面的代码，你会发现，打开的页面只在窗口左上角一小块显示，看着很别扭，这是因为pyppeteer默认窗口大小是800*600。调整窗口大小通过方法实现，下面代码实现最大化窗口：

```
import asyncio
from pyppeteer import launch
 
def screen_size():
    """使用tkinter获取屏幕大小"""
    import tkinter
    tk = tkinter.Tk()
    width = tk.winfo_screenwidth()
    height = tk.winfo_screenheight()
    tk.quit()
    return width, height
 
async def main():
    browser = await launch(headless=False)
    page = await browser.newPage()
    width, height = screen_size()
    await page.setViewport({ # 最大化窗口
        "width": width,
        "height": height
    })
    await page.goto('http://www.baidu.com/')
    await asyncio.sleep(100)
    await browser.close()
 
asyncio.get_event_loop().run_until_complete(main())  
```



### 设置userAgent

```
import asyncio
from pyppeteer import launch
 
async def main():
    browser = await launch(headless=False)
    page = await browser.newPage()
    # 设置请求头userAgent
    await page.setUserAgent('Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Mobile Safari/537.36')
    await page.goto('http://www.baidu.com/')
    await asyncio.sleep(100)
    await browser.close()
 
asyncio.get_event_loop().run_until_complete(main())
```



### 执行js脚本

有时候，为了达成某些目的（例如屏蔽网站原有js），我们不可避免得需要执行一些js脚本。执行js脚本通过evaluate方法。

如下所示，我们通过js来修改window.navigator.webdriver属性的值，由此绕过网站对webdriver的检测：

```
import asyncio
from pyppeteer import launch
 
async def main():
    js1 = '''() =>{
        Object.defineProperties(navigator,{
        webdriver:{
            get: () => false
            }
        })
    }'''

    js2 = '''() => {
        alert (
            window.navigator.webdriver
        )
    }'''
    browser = await launch({'headless':False, 'args':['--no-sandbox'],})

    page = await browser.newPage()
    await page.goto('https://h5.ele.me/login/')
    await page.evaluate(js1)
    await page.evaluate(js2)
 
asyncio.get_event_loop().run_until_complete(main())
```



### 模拟操作

pyppeteer提供了Keyboard和Mouse两个类来实现模拟操作，前者是用来实现键盘模拟，后者实现鼠标模拟（还有其他触屏之类的就不说了）。

主要来说说输入和点击：

```
import asyncio
from pyppeteer import launch
 
async def main():
    browser = await launch(headless=False, args=['--disable-infobars'])
    page = await browser.newPage()
    await page.goto('https://h5.ele.me/login/')
    await page.type('form section input', '12345678999') # 模拟键盘输入手机号
    await page.click('form section button') # 模拟鼠标点击获取验证码
    await asyncio.sleep(200)
    await browser.close()
 
asyncio.get_event_loop().run_until_complete(main())
```

上面的模拟操作中，无论是模拟键盘输入还是鼠标点击定位都是通过css选择器，似乎pyppeteer的type和click直接模拟操作定位都只能通过css选择器（或者是我在官方文档中没找到方法）。当然，要间接通过xpath先定位，然后再模拟操作也是可以的，不过，这种方法要麻烦一些，不推荐。



### 某电商平台模拟登陆

某些电商平台会检测机器人并进行禁止，通过webdriver对浏览器的每一步操作都会留下特殊的痕迹，会被平台识别，这个必须通过重新编译chrome的webdriver才能实现，下面直接上pyppeteer实现的代码：

```
import asyncio
from pyppeteer import launch
 
def screen_size():
    """使用tkinter获取屏幕大小"""
    import tkinter
    tk = tkinter.Tk()
    width = tk.winfo_screenwidth()
    height = tk.winfo_screenheight()
    tk.quit()
    return width, height
 
 
async def main():
    js1 = '''() =>{
 
        Object.defineProperties(navigator,{
        webdriver:{
            get: () => false
            }
        })
    }'''
 
    js2 = '''() => {
        alert (
            window.navigator.webdriver
        )
    }'''
    browser = await launch({'headless':False, 'args':['--no-sandbox'],})
 
    page = await browser.newPage()
    width, height = screen_size()
    await page.setViewport({ # 最大化窗口
        "width": width,
        "height": height
    })
    await page.goto('https://h5.ele.me/login/')
    await page.evaluate(js1)
    await page.evaluate(js2)
    input_sjh = await page.xpath('//form/section[1]/input[1]')
    click_yzm = await page.xpath('//form/section[1]/button[1]')
    input_yzm = await page.xpath('//form/section[2]/input[1]')
    but = await page.xpath('//form/section[2]/input[1]')
    print(input_sjh)
    await input_sjh[0].type('*****手机号********')
    await click_yzm[0].click()
    ya = input('请输入验证码：')
    await input_yzm[0].type(str(ya))
    await but[0].click()
    await asyncio.sleep(3)
    await page.goto('https://www.ele.me/home/')
    await asyncio.sleep(100)
    await browser.close()
 
asyncio.get_event_loop().run_until_complete(main())
```

注：如果出现以下错误：pyppeteer.errors.NetworkError: Protocol Error (Runtime.callFunctionOn): Session closed. Most likely the page has been closed.

可以通过修改源码解决，找到pyppeteer包下的connection.py模块，在其43行和44行改为下面这样：

```
self._ws = websockets.client.connect(
# self._url, max_size=None, loop=self._loop)
self._url, max_size=None, loop=self._loop, ping_interval=None, ping_timeout=None)
```