# 彻底解决Github网站打不开的问题

## 一、确定ip

进入网址：[https://github.com.ipaddress.com](https://github.com.ipaddress.com/)

查看GitHub的ip地址：

```
140.82.114.4 github.com
```



## 二、确定域名ip

进入网址：https://fastly.net.ipaddress.com/github.global.ssl.fastly.net

确定域名：

```
199.232.69.194 github.global.ssl.fastly.net
```



## 三、确定静态资源ip

进入网址：https://github.com.ipaddress.com/assets-cdn.github.com

确定静态资源IP（多个）：

```
185.199.108.153 assets-cdn.github.com
185.199.109.153 assets-cdn.github.com
185.199.110.153 assets-cdn.github.com
185.199.111.153 assets-cdn.github.com
```



## 四、修改hosts文件

### Windows系统

1、打开 C:\Windows\System32\drivers\etc 找到hosts文件

2、使用记事本打开hosts文件，在底部加入前面获取到的内容，然后保存退出：

```
140.82.114.4 github.com
199.232.69.194 github.global.ssl.fastly.net
185.199.108.153 assets-cdn.github.com
185.199.109.153 assets-cdn.github.com
185.199.110.153 assets-cdn.github.com
185.199.111.153 assets-cdn.github.com
```

3、更新DNS，打开命令行执行以下命令：

```
> ipconfig /flushdns
```

### MacOS

1、打开访达（Finder）窗口（随便一个文件夹）；

2、按快捷键 “shift+command+G”；

3、输入“/etc/hosts ”，可直接找到hosts文件；

4、复制hosts文件到桌面，并使用文本编辑器打开副本进行编辑；

5、在底部加入前面获取到的内容，然后保存退出；

6、将修改后的hosts文件替换回/etc目录。

