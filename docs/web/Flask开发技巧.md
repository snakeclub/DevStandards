# Flask开发技巧

## 开发工具问题

### 1、VSCode调试出现No module named XXX

使用VSCode调试Flask程序，如果把debug mode打开（app.debug = True），启动时Flask会加载2次，第二次可能会报“No module named XXX”的错误。

这个问题的原因是第二次Flask加载会找启动自己的模块重新执行，但因为环境变量的问题搜索不到对应路径而导致出错，解决办法如下：

（1）在python的site-packages目录（C:\Users\74143\AppData\Local\Programs\Python\Python37\Lib\site-packages）中新增pth文件指定可直接引用的当前项目包路径，例如“chat_robot.pth”;

（2）在pth文件内容中指定项目路径，例如：

```
# .pth file for the chat_robot extensions
D:/opensource/chat_robot/chat_robot
```

**注意：如果有多个项目的模块名是一样的情况，注意需要删除其他项目的pth文件，否则有可能因为搜索路径的问题，导致Flask执行了其他项目的相同模块代码。**

### 2、更新了静态文件，但调试时客户端没有改变

这个问题是因为Flask的缓存机制导致，可以通过指定 send_file_max_age_default 缓存参数，设定缓存过期时间为1秒来解决问题：

```
app.send_file_max_age_default = datetime.timedelta(seconds=1)  # 设置文件缓存1秒
```



# 参数设置技巧

### 1、获取到的JSON串显示中文

将 JSON_AS_ASCII 配置设置为False，不采用兼容 ASCII 的编码格式：

```
app.config['JSON_AS_ASCII'] = False  # 显示中文
```



### 2、限制上传文件大小

```
# 限制上传文件大小10M
app.config['MAX_CONTENT_LENGTH'] = math.floor(
    10 * 1024 * 1024
)
```

