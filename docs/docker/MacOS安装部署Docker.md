# MacOS安装部署Docker

## 下载Docker Desktop

下载地址：https://docs.docker.com/docker-for-mac/install/

选择对应的版本进行下载即可

<img src="MacOS%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2Docker.assets/image-20210706180007988.png" alt="image-20210706180007988" style="zoom: 50%;" />

## 安装

1、如果Mac芯片为Apple silicon，需要安装 **Rosetta 2** 来运行一些Darwin/AMD64架构的镜像。安装方法如下，在命令行执行：

```
softwareupdate --install-rosetta
```

2、双击下载的安装文件，在弹出的窗口中将docker图标拖动到application图标上：

<img src="MacOS%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2Docker.assets/docker-app-drag.png" alt="Install Docker app" style="zoom: 67%;" />

3、找到安装好的程序图标，双击运行，第一次运行会同时安装帮助程序工具：

<img src="MacOS%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2Docker.assets/image-20210706181647279.png" alt="image-20210706181647279" style="zoom:50%;" />

4、第一次启动，会弹出开始帮助预览页面，如果已经熟悉了docker操作可以跳过帮助预览：

<img src="MacOS%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2Docker.assets/docker-tutorial-mac.png" alt="Docker Quick Start tutorial" style="zoom: 33%;" />

5、使用过程窗口界面可以直接关闭，看到图标栏有docker的图标，说明docker已经正常运行了。

6、这时候可以新打开一个终端窗口，输入以下命令查看docker信息：

```
% docker --version
Docker version 20.10.7, build f0df350
```



## 部署

1、镜像加速

在任务栏点击 Docker Desktop 应用图标 ->`Perferences`，在左侧导航菜单选择`Docker Engine`，在右侧像下边一样编辑 json 文件。修改完成之后，点击`Apply & Restart`按钮，Docker 就会重启并应用配置的镜像地址了。

```
{
  "registry-mirrors": [
    "https://hub-mirror.c.163.com",
    "https://mirror.baidubce.com"
  ]
}
```

执行 `docker info`，如果从结果中看到了如下内容，说明配置成功。

```text
Registry Mirrors:  https://hub-mirror.c.163.com/
```



## 使用实例（Redis）

1、在命令行，查找可用的Redis版本：

```
% docker search redis
NAME                             DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
redis                            Redis is an open source key-value store that…   9645      [OK]       
sameersbn/redis                                                                  83                   [OK]
grokzen/redis-cluster            Redis cluster 3.0, 3.2, 4.0, 5.0, 6.0, 6.2      78                   
rediscommander/redis-commander   Alpine image for redis-commander - Redis man…   61                   [OK]             
...
```

2、我们选择官方版本，拉取最新版本的镜像：

```
% docker pull redis:latest
latest: Pulling from library/redis
448f6bf000e3: Pull complete 
c1563d96d611: Pull complete 
39898690e366: Pull complete 
f2c1f534c176: Pull complete 
677225c5285b: Pull complete 
f57391477f51: Pull complete 
Digest: sha256:7c540ceff53f0522f6b1c264d8142df08316173d103586ddf51ed91ca49deec8
Status: Downloaded newer image for redis:latest
docker.io/library/redis:latest
```

3、查看已下载的本地镜像：

```
% docker images
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
redis        latest    cad8cf27ff34   12 days ago   99.7MB
```

4、创建Redis容器并运行

```
% docker run -itd --name redis-test -p 6379:6379 redis
48e02daa998070d56c5eed113fa273a4a9d4aa18530a65661010c4225eb1f7ea
```

5、 通过**docker ps** 命令查看容器的运行信息：

```
% docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED              STATUS              PORTS                                       NAMES
48e02daa9980   redis     "docker-entrypoint.s…"   About a minute ago   Up About a minute   0.0.0.0:6379->6379/tcp, :::6379->6379/tcp   redis-test
```

6、通过 redis-cli 连接测试使用 redis 服务

```
% docker exec -it redis-test /bin/bash
root@48e02daa9980:/data# redis-cli
127.0.0.1:6379> set test 1
OK
```

7、停止容器

```
docker stop 48e02daa9980
```

8、删除容器

```
docker rm 48e02daa9980
```

9、删除镜像

```
docker rmi cad8cf27ff34
```

