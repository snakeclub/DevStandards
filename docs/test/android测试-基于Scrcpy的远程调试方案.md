# android测试-基于Scrcpy的远程调试方案

参考：https://testerhome.com/topics/21647

参考：https://github.com/wenxiaomao1023/scrcpy

## 原生Scrcpy体验

### 简单部署

原生Scrcpy支持在本机通过电脑同步手机画面并控制手机，在Windows可以最简单的进行体验：

1、在github上下载已经预编译好的App客户端的包：

32位系统：https://github.com/Genymobile/scrcpy/releases/download/v1.12.1/scrcpy-win32-v1.12.1.zip

64位系统：https://github.com/Genymobile/scrcpy/releases/download/v1.12.1/scrcpy-win64-v1.12.1.zip

2、解压包，注意包所放置的路径必须不包含中文（中文路径会出现问题），例如：D:\scrcpy-win64-v1.12.1

3、插上手机，打开USB调试选项；

4、打开一个命令窗口，跳转到解压后的目录，然后执行启动命令：

```
> cd D:\scrcpy-win64-v1.12.1
> scrcpy
```

弹出的窗口就可以同步界面进行手机控制了：

<img src="android%E6%B5%8B%E8%AF%95-%E5%9F%BA%E4%BA%8EScrcpy%E7%9A%84%E8%BF%9C%E7%A8%8B%E8%B0%83%E8%AF%95%E6%96%B9%E6%A1%88.assets/image-20210112105832753.png" alt="image-20210112105832753" style="zoom:25%;" />

### 启动命令支持

scrcpy支持在启动时带一些参数：

```
# 限制最大大小，通过减少屏幕大小来提升性能
scrcpy --max-size 1024
scrcpy -m 1024  # short version

# 指定视频传输率，默认为8M，可以减少至2M提升性能
scrcpy --bit-rate 2M
scrcpy -b 2M  # short version

# 限制刷新刷新帧
scrcpy --max-fps 15

# 只展示部分屏幕
scrcpy --crop 1224:1440:0:0   # 1224x1440 at offset (0,0)

# 录屏，Ctrl+C 结束录屏，如果结束不了可以断开设备
scrcpy --record file.mp4
scrcpy -r file.mkv

# 不显示镜像的情况下录屏
scrcpy --no-display --record file.mp4
scrcpy -Nr file.mkv

# 多设备时指定特定设备
scrcpy --serial 0123456789abcdef
scrcpy -s 0123456789abcdef  # short version

# 不控制设备（只同步显示）
scrcpy --no-control
scrcpy -n

# 关闭屏幕进行操作
scrcpy --turn-screen-off
scrcpy -S

# 显示触控
scrcpy --show-touches
scrcpy -t
```



### 操作快捷键

| Action                                  | Shortcut                      | Shortcut (macOS)             |
| --------------------------------------- | ----------------------------- | ---------------------------- |
| Switch fullscreen mode                  | `Ctrl`+`f`                    | `Cmd`+`f`                    |
| Resize window to 1:1 (pixel-perfect)    | `Ctrl`+`g`                    | `Cmd`+`g`                    |
| Resize window to remove black borders   | `Ctrl`+`x` \| *Double-click¹* | `Cmd`+`x` \| *Double-click¹* |
| Click on `HOME`                         | `Ctrl`+`h` \| *Middle-click*  | `Ctrl`+`h` \| *Middle-click* |
| Click on `BACK`                         | `Ctrl`+`b` \| *Right-click²*  | `Cmd`+`b` \| *Right-click²*  |
| Click on `APP_SWITCH`                   | `Ctrl`+`s`                    | `Cmd`+`s`                    |
| Click on `MENU`                         | `Ctrl`+`m`                    | `Ctrl`+`m`                   |
| Click on `VOLUME_UP`                    | `Ctrl`+`↑` *(up)*             | `Cmd`+`↑` *(up)*             |
| Click on `VOLUME_DOWN`                  | `Ctrl`+`↓` *(down)*           | `Cmd`+`↓` *(down)*           |
| Click on `POWER`                        | `Ctrl`+`p`                    | `Cmd`+`p`                    |
| Power on                                | *Right-click²*                | *Right-click²*               |
| Turn device screen off (keep mirroring) | `Ctrl`+`o`                    | `Cmd`+`o`                    |
| Rotate device screen                    | `Ctrl`+`r`                    | `Cmd`+`r`                    |
| Expand notification panel               | `Ctrl`+`n`                    | `Cmd`+`n`                    |
| Collapse notification panel             | `Ctrl`+`Shift`+`n`            | `Cmd`+`Shift`+`n`            |
| Copy device clipboard to computer       | `Ctrl`+`c`                    | `Cmd`+`c`                    |
| Paste computer clipboard to device      | `Ctrl`+`v`                    | `Cmd`+`v`                    |
| Copy computer clipboard to device       | `Ctrl`+`Shift`+`v`            | `Cmd`+`Shift`+`v`            |
| Enable/disable FPS counter (on stdout)  | `Ctrl`+`i`                    | `Cmd`+`i`                    |