# Docker常用命令和技巧 -- 由浅入深学Docker系列(4)

非原创，参考部分网络材料并增加自己的补充内容：

《docker常用命令详解》：<http://blog.csdn.net/permike/article/details/51879578>

《Docker 命令大全》：<http://www.runoob.com/docker/docker-command-manual.html>

 

Docker的命令总的来说分为以下几种：

•       容器生命周期管理 — docker [run|start|stop|restart|kill|rm|pause|unpause]

•       容器操作运维 — docker [ps|inspect|top|attach|events|logs|wait|export|port]

•       容器rootfs命令 — docker [commit|cp|diff]

•       镜像仓库 — docker [login|pull|push|search]

•       本地镜像管理 — docker [images|rmi|tag|build|history|save|import]

•       其他命令 — docker [info|version]

 

## 一、容器生命周期管理

### 1、 run - 通过指定镜像（image）启动新的容器（container）

docker run命令首先会从特定的image创之上create一层可写的container，然后通过start命令来启动它。停止的container可以重新启动并保留原来的修改。run命令启动参数有很多，以下是一些常规使用说明，更多部分请参考http://www.cnphp6.com/archives/24899

当利用 docker run 来创建容器时，Docker 在后台运行的标准操作包括：

•       检查本地是否存在指定的镜像，不存在就从公有仓库下载

•       利用镜像创建并启动一个容器

•       分配一个文件系统，并在只读的镜像层外面挂载一层可读写层

•       从宿主主机配置的网桥接口中桥接一个虚拟接口到容器中去

•       从地址池配置一个 ip 地址给容器

•       执行用户指定的应用程序

•       执行完毕后容器被终止

**语法**

```
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
```

OPTIONS说明：

·        **-a stdin:** 指定标准输入输出内容类型，可选 STDIN/STDOUT/STDERR 三项；

·        **-d:** 后台运行容器，并返回容器ID；

·        **-i:** 以交互模式运行容器，通常与 -t 同时使用；

·        **-t:** 为容器重新分配一个伪输入终端，通常与 -i 同时使用；

·        **--name="nginx-lb":** 为容器指定一个名称；

·        **--dns 8.8.8.8:** 指定容器使用的DNS服务器，默认和宿主一致；

·     **--dns-search example.com:** 指定容器DNS搜索域名，默认和宿主一致；

·        **-h "mars":** 指定容器的hostname；

·        **-e username="ritchie":** 设置环境变量；

·        **--env-file=[]:** 从指定文件读入环境变量；

·        **--cpuset="0-2" or --cpuset="0,1,2":** 绑定容器到指定CPU运行；

·        **-m :**设置容器使用内存最大值；

·        **--net="bridge":** 指定容器的网络连接类型，支持 bridge/host/none/container: 四种类型；

·        **--link=[]:** 添加链接到另一个容器；

·        **--expose=[]:** 开放一个端口或一组端口；

**实例**

使用docker镜像nginx:latest以后台模式启动一个容器,并将容器命名为mynginx。

```
docker run --name mynginx -d nginx:latest
```

使用镜像nginx:latest以后台模式启动一个容器,并将容器的80端口映射到主机随机端口。

```
docker run -P -d nginx:latest
```

使用镜像nginx:latest以后台模式启动一个容器,将容器的80端口映射到主机的80端口,主机的目录/data映射到容器的/data。

```
docker run -p 80:80 -v /data:/data -d nginx:latest
```

使用镜像nginx:latest以交互模式启动一个容器,在容器内执行/bin/bash命令。

```
runoob@runoob:~$ docker run -it nginx:latest /bin/bash
root@b8573233d675:/# 
```

 

**运行出一个container放到后台运行**

```
# docker run -d ubuntu /bin/sh -c "while true; do echo hello world; sleep 2; done"
ae60c4b642058fefcc61ada85a610914bed9f5df0e2aa147100eab85cea785dc
```

它将直接把启动的container挂起放在后台运行（这才叫saas），并且会输出一个CONTAINER ID，通过docker ps可以看到这个容器的信息，可在container外面查看它的输出docker logs ae60c4b64205，也可以通过docker attach ae60c4b64205连接到这个正在运行的终端，此时在Ctrl+C退出container就消失了，按ctrl-p ctrl-q可以退出到宿主机，而保持container仍然在运行。

另外，如果-d启动但后面的命令执行完就结束了，如/bin/bash、echo test，则container做完该做的时候依然会终止。而且-d不能与--rm同时使用。

可以通过这种方式来运行memcached、apache等。

 

**映射host到container的端口和目录**

映射主机到容器的端口是很有用的，比如在container中运行memcached，端口为11211，运行容器的host可以连接container的 internel_ip:11211 访问，如果有从其他主机访问memcached需求那就可以通过-p选项，形如-p <host_port:contain_port>，存在以下几种写法：

```
-p 11211:11211 这个即是默认情况下，绑定主机所有网卡（0.0.0.0）的11211端口到容器的11211端口上
-p 127.0.0.1:11211:11211 只绑定localhost这个接口的11211端口
-p 127.0.0.1::5000
-p 127.0.0.1:80:8080
```

目录映射其实是“绑定挂载”host的路径到container的目录，这对于内外传送文件比较方便，在搭建私服那一节，为了避免私服container停止以后保存的images不被删除，就要把提交的images保存到挂载的主机目录下。使用比较简单，-v <host_path:container_path>，绑定多个目录时再加-v。

```
-v /tmp/docker:/tmp/docker
```

另外在两个container之间建立联系可用--link，详见高级部分或官方文档。

下面是一个例子：

```
# docker run --name nginx_test \
 -v /tmp/docker:/usr/share/nginx/html:ro \
 -p 80:80 -d \
 nginx:1.7.6
```

在主机的/tmp/docker下建立index.html，就可以通过http://localhost:80/或http://host-ip:80访问了。

 

**使用image创建container并进入交互模式, login shell是/bin/bash**

```
# docker run -i -t --name mytest centos:centos6 /bin/bash
bash-4.1#
```

上面的--name参数可以指定启动后的容器名字，如果不指定则docker会帮我们取一个名字。镜像centos:centos6也可以用IMAGE ID (68edf809afe7) 代替），并且会启动一个伪终端，但通过ps或top命令我们却只能看到一两个进程，因为容器的核心是所执行的应用程序，所需要的资源都是应用程序运行所必需的，除此之外，并没有其它的资源，可见Docker对资源的利用率极高。此时使用exit或Ctrl+D退出后，这个容器也就消失了。

 

**使用image创建container并执行相应命令，然后停止**

```
# docker run ubuntu echo "hello world"
hello word
```

这是最简单的方式，跟在本地直接执行echo 'hello world' 几乎感觉不出任何区别，而实际上它会从本地ubuntu:latest镜像启动到一个容器，并执行打印命令后退出（docker ps -l可查看）。需要注意的是，默认有一个--rm=true参数，即完成操作后停止容器并从文件系统移除。因为Docker的容器实在太轻量级了，很多时候用户都是随时删除和新创建容器。

容器启动后会自动随机生成一个CONTAINER ID，这个ID在后面commit命令后可以变为IMAGE ID

 

### 2、start/stop/restart - 开启/停止/重启container

容器可以通过run新建一个来运行，也可以重新start已经停止的container，但start不能够再指定容器启动时运行的指令，因为docker只能有一个前台进程。

容器stop（或Ctrl+D）时，会在保存当前容器的状态之后退出，下次start时保留有上次关闭时更改。而且每次进入attach进去的界面是一样的，与第一次run启动或commit提交的时刻相同。

```
CONTAINER_ID=$(docker start <containner_id>)
docker stop $CONTAINER_ID
docker restart $CONTAINER_ID
```

**语法**

```
docker start [OPTIONS] CONTAINER [CONTAINER...]
docker stop [OPTIONS] CONTAINER [CONTAINER...]
docker restart [OPTIONS] CONTAINER [CONTAINER...]
```

OPTIONS说明：

**·**        **-a, --attach=false         Attach STDOUT/STDERR and forward signals启动一个容器并打印输出结果和错误**

**·**        **-i, --interactive=false    Attach container's STDIN启动一个容器并进入交互模式**

**·**        **-t, --time=10      Seconds to wait for stop before killing the container停止或者重启容器的超时时间（秒），超时后系统将杀死进程。**

 

**实例**

启动已被停止的容器myrunoob

```
docker start myrunoob
```

停止运行中的容器myrunoob

```
docker stop myrunoob
```

重启容器myrunoob

```
docker restart myrunoob
```

启动一个 ID 为 b5e08e1435b3 的容器，并进入交互模式

```
docker start -i b5e08e1435b3
```

 

### 3、docker kill :杀掉一个运行中的容器

**语法**

```
docker kill [OPTIONS] CONTAINER [CONTAINER...]
```

OPTIONS说明：

·        **-s :**向容器发送一个信号，自定义发送至容器的信号

**实例**

杀掉运行中的容器mynginx，并向容器发送 KILL 信号

```
runoob@runoob:~$ docker kill -s KILL mynginx
mynginx
```

 

### 4、docker rm ：删除一个或多少容器

**语法**

```
docker rm [OPTIONS] CONTAINER [CONTAINER...]
```

OPTIONS说明：

·        **-f :**通过SIGKILL信号强制删除一个运行中的容器

·        **-l :**移除容器间的网络连接，而非容器本身

·        **-v :**-v 删除与容器关联的卷

**实例**

强制删除容器db01、db02

```
docker rm -f db01、db02
```

移除容器nginx01对容器db01的连接，连接名db

```
docker rm -l db 
```

删除容器nginx01,并删除容器挂载的数据卷

```
docker rm -v nginx01
```

删除所有停止的容器

```
docker rm $(docker ps -a -q)
```

 

### 5、 pause/unpause : 暂停/恢复容器中所有的进程

**docker pause** :暂停容器中所有的进程。

**docker unpause** :恢复容器中所有的进程。

**语法**

```
docker pause [OPTIONS] CONTAINER [CONTAINER...]
docker unpause [OPTIONS] CONTAINER [CONTAINER...]
```

**实例**

暂停数据库容器db01提供服务。

```
docker pause db01
```

恢复数据库容器db01提供服务。

```
docker unpause db01
```

 

### 6、docker create：创建一个新的容器但不启动它

用法同 [docker run](http://www.runoob.com/docker/docker-run-command.html)

**语法**

```
docker create [OPTIONS] IMAGE [COMMAND] [ARG...]
```

语法同 [docker run](http://www.runoob.com/docker/docker-run-command.html)

**实例**

使用docker镜像nginx:latest创建一个容器,并将容器命名为myrunoob

```
runoob@runoob:~$ docker create  --name myrunoob  nginx:latest      
09b93464c2f75b7b69f83d56a9cfc23ceb50a48a9db7652ee4c27e3e2cb1961f
```

 

### 7、docker exec ：在运行的容器中执行命令

**语法**

```
docker exec [OPTIONS] CONTAINER COMMAND [ARG...]
```

OPTIONS说明：

·        **-d :**分离模式: 在后台运行

·        **-i :**即使没有附加也保持STDIN 打开

·        **-t :**分配一个伪终端

**实例**

在容器mynginx中以交互模式执行容器内/root/runoob.sh脚本

```
runoob@runoob:~$ docker exec -it mynginx /bin/sh /root/runoob.sh
http://www.runoob.com/
```

在容器mynginx中开启一个交互模式的终端

```
runoob@runoob:~$ docker exec -i -t  mynginx /bin/bash
root@b1a0703e41e7:/#
```

 

## 二、容器操作

### 1、docker ps : 列出容器

**语法**

```
docker ps [OPTIONS]
```

OPTIONS说明：

·        **-a :**显示所有的容器，包括未运行的。

·        **-f :**根据条件过滤显示的内容。

·        **--format :**指定返回值的模板文件。

·        **-l :**显示最近创建的容器。

·        **-n :**列出最近创建的n个容器。

·        **--no-trunc :**不截断输出。

·        **-q :**静默模式，只显示容器编号。

·        **-s :**显示总的文件大小。

**实例**

列出所有在运行的容器信息。

```
runoob@runoob:~$ docker ps
CONTAINER ID   IMAGE          COMMAND                ...  PORTS                    NAMES
09b93464c2f7   nginx:latest   "nginx -g 'daemon off" ...  80/tcp, 443/tcp          myrunoob
96f7f14e99ab   mysql:5.6      "docker-entrypoint.sh" ...  0.0.0.0:3306->3306/tcp   mymysql
```

列出最近创建的5个容器信息。

```
runoob@runoob:~$ docker ps -n 5
CONTAINER ID        IMAGE               COMMAND                   CREATED           
09b93464c2f7        nginx:latest        "nginx -g 'daemon off"    2 days ago   ...     
b8573233d675        nginx:latest        "/bin/bash"               2 days ago   ...     
b1a0703e41e7        nginx:latest        "nginx -g 'daemon off"    2 days ago   ...    
f46fb1dec520        5c6e1090e771        "/bin/sh -c 'set -x \t"   2 days ago   ...   
a63b4a5597de        860c279d2fec        "bash"                    2 days ago   ...
```

列出所有创建的容器ID。

```
runoob@runoob:~$ docker ps -a -q
09b93464c2f7
b8573233d675
b1a0703e41e7
f46fb1dec520
a63b4a5597de
6a4aa42e947b
de7bb36e7968
43a432b73776
664a8ab1a585
ba52eb632bbd
...
```

 

### 2、docker inspect : 获取容器/镜像的元数据

**语法**

```
docker inspect [OPTIONS] NAME|ID [NAME|ID...]
```

OPTIONS说明：

·        **-f :**指定返回值的模板文件。

·        **-s :**显示总的文件大小。

·        **--type :**为指定类型返回JSON。

**实例**

获取镜像mysql:5.6的元信息。

```
runoob@runoob:~$ docker inspect mysql:5.6
[
    {
        "Id": "sha256:2c0964ec182ae9a045f866bbc2553087f6e42bfc16074a74fb820af235f070ec",
        "RepoTags": [
            "mysql:5.6"
        ],
        "RepoDigests": [],
        "Parent": "",
        "Comment": "",
        "Created": "2016-05-24T04:01:41.168371815Z",
        "Container": "e0924bc460ff97787f34610115e9363e6363b30b8efa406e28eb495ab199ca54",
        "ContainerConfig": {
            "Hostname": "b0cf605c7757",
            "Domainname": "",
            "User": "",
            "AttachStdin": false,
            "AttachStdout": false,
            "AttachStderr": false,
            "ExposedPorts": {
                "3306/tcp": {}
            },
...
```

获取正在运行的容器mymysql的 IP。

```
runoob@runoob:~$ docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mymysql
172.17.0.3
```

 

### 3、docker top : 查看容器中运行的进程信息，支持  **ps命令参数。**

**语法**

```
docker top [OPTIONS] CONTAINER [ps OPTIONS]
```

容器运行时不一定有/bin/bash终端来交互执行top命令，而且容器还不一定有top命令，可以使用docker top来实现查看container中正在运行的进程。

**实例**

查看容器mymysql的进程信息。

```
runoob@runoob:~/mysql$ docker top mymysql
UID    PID    PPID    C      STIME   TTY  TIME       CMD
999    40347  40331   18     00:58   ?    00:00:02   mysqld
```

查看所有运行容器的进程信息。

```
for i in  `docker ps |grep Up|awk '{print $1}'`;do echo \ &&docker top $i; done
```

 

### 4、docker attach : 连接到正在运行中的容器

**语法**

```
docker attach [OPTIONS] CONTAINER
```

要attach上去的容器必须正在运行，可以同时连接上同一个container来共享屏幕（与screen命令的attach类似）。

官方文档中说attach后可以通过CTRL-C来detach，但实际上经过我的测试，如果container当前在运行bash，CTRL-C自然是当前行的输入，没有退出；如果container当前正在前台运行进程，如输出nginx的access.log日志，CTRL-C不仅会导致退出容器，而且还stop了。这不是我们想要的，detach的意思按理应该是脱离容器终端，但容器依然运行。好在attach是可以带上--sig-proxy=false来确保CTRL-D或CTRL-C不会关闭容器。

**实例**

容器mynginx将访问日志指到标准输出，连接到容器查看访问信息。

```
runoob@runoob:~$ docker attach --sig-proxy=false mynginx
192.168.239.1 - - [10/Jul/2016:16:54:26 +0000] "GET / HTTP/1.1" 304 0 "-" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36" "-"
```

 

### 5、docker events : 从服务器获取实时事件

**语法**

```
docker events [OPTIONS]
```

OPTIONS说明：

·        **-f：**根据条件过滤事件；

·        **--since：**从指定的时间戳后显示所有事件;

·        **--until：**流水时间显示到指定的时间为止；

**实例**

显示docker 2016年7月1日后的所有事件。

```
runoob@runoob:~/mysql$ docker events  --since="1467302400"
2016-07-08T19:44:54.501277677+08:00 network connect 66f958fd13dc4314ad20034e576d5c5eba72e0849dcc38ad9e8436314a4149d4 (container=b8573233d675705df8c89796a2c2687cd8e36e03646457a15fb51022db440e64, name=bridge, type=bridge)
2016-07-08T19:44:54.723876221+08:00 container start b8573233d675705df8c89796a2c2687cd8e36e03646457a15fb51022db440e64 (image=nginx:latest, name=elegant_albattani)
2016-07-08T19:44:54.726110498+08:00 container resize b8573233d675705df8c89796a2c2687cd8e36e03646457a15fb51022db440e64 (height=39, image=nginx:latest, name=elegant_albattani, width=167)
2016-07-08T19:46:22.137250899+08:00 container die b8573233d675705df8c89796a2c2687cd8e36e03646457a15fb51022db440e64 (exitCode=0, image=nginx:latest, name=elegant_albattani)
...
```

显示docker 镜像为mysql:5.6 2016年7月1日后的相关事件。

```
runoob@runoob:~/mysql$ docker events -f "image"="mysql:5.6" --since="1467302400" 
2016-07-11T00:38:53.975174837+08:00 container start 96f7f14e99ab9d2f60943a50be23035eda1623782cc5f930411bbea407a2bb10 (image=mysql:5.6, name=mymysql)
2016-07-11T00:51:17.022572452+08:00 container kill 96f7f14e99ab9d2f60943a50be23035eda1623782cc5f930411bbea407a2bb10 (image=mysql:5.6, name=mymysql, signal=9)
2016-07-11T00:51:17.132532080+08:00 container die 96f7f14e99ab9d2f60943a50be23035eda1623782cc5f930411bbea407a2bb10 (exitCode=137, image=mysql:5.6, name=mymysql)
2016-07-11T00:51:17.514661357+08:00 container destroy 96f7f14e99ab9d2f60943a50be23035eda1623782cc5f930411bbea407a2bb10 (image=mysql:5.6, name=mymysql)
2016-07-11T00:57:18.551984549+08:00 container create c8f0a32f12f5ec061d286af0b1285601a3e33a90a08ff1706de619ac823c345c (image=mysql:5.6, name=mymysql)
2016-07-11T00:57:18.557405864+08:00 container attach c8f0a32f12f5ec061d286af0b1285601a3e33a90a08ff1706de619ac823c345c (image=mysql:5.6, name=mymysql)
2016-07-11T00:57:18.844134112+08:00 container start c8f0a32f12f5ec061d286af0b1285601a3e33a90a08ff1706de619ac823c345c (image=mysql:5.6, name=mymysql)
2016-07-11T00:57:19.140141428+08:00 container die c8f0a32f12f5ec061d286af0b1285601a3e33a90a08ff1706de619ac823c345c (exitCode=1, image=mysql:5.6, name=mymysql)
2016-07-11T00:58:05.941019136+08:00 container destroy c8f0a32f12f5ec061d286af0b1285601a3e33a90a08ff1706de619ac823c345c (image=mysql:5.6, name=mymysql)
2016-07-11T00:58:07.965128417+08:00 container create a404c6c174a21c52f199cfce476e041074ab020453c7df2a13a7869b48f2f37e (image=mysql:5.6, name=mymysql)
2016-07-11T00:58:08.188734598+08:00 container start a404c6c174a21c52f199cfce476e041074ab020453c7df2a13a7869b48f2f37e (image=mysql:5.6, name=mymysql)
2016-07-11T00:58:20.010876777+08:00 container top a404c6c174a21c52f199cfce476e041074ab020453c7df2a13a7869b48f2f37e (image=mysql:5.6, name=mymysql)
2016-07-11T01:06:01.395365098+08:00 container top a404c6c174a21c52f199cfce476e041074ab020453c7df2a13a7869b48f2f37e (image=mysql:5.6, name=mymysql)
 
```

如果指定的时间是到秒级的，需要将时间转成时间戳。如果时间为日期的话，可以直接使用，如--since="2016-07-01"。

 

### 6、docker logs : 获取容器的日志

**语法**

```
docker logs [OPTIONS] CONTAINER
```

OPTIONS说明：

·        **-f :** 跟踪日志输出

·        **--since :**显示某个开始时间的所有日志

·        **-t :** 显示时间戳

·        **--tail :**仅列出最新N条容器日志

**实例**

跟踪查看容器mynginx的日志输出。

```
runoob@runoob:~$ docker logs -f mynginx
192.168.239.1 - - [10/Jul/2016:16:53:33 +0000] "GET / HTTP/1.1" 200 612 "-" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36" "-"
2016/07/10 16:53:33 [error] 5#5: *1 open() "/usr/share/nginx/html/favicon.ico" failed (2: No such file or directory), client: 192.168.239.1, server: localhost, request: "GET /favicon.ico HTTP/1.1", host: "192.168.239.130", referrer: "http://192.168.239.130/"
192.168.239.1 - - [10/Jul/2016:16:53:33 +0000] "GET /favicon.ico HTTP/1.1" 404 571 "http://192.168.239.130/" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36" "-"
192.168.239.1 - - [10/Jul/2016:16:53:59 +0000] "GET / HTTP/1.1" 304 0 "-" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36" "-"
...
```

查看容器mynginx从2016年7月1日后的最新10条日志。

```
docker logs --since="2016-07-01" --tail=10 mynginx
```

 

### 7、docker wait : 阻塞运行直到容器停止，然后打印出它的退出代码

**语法**

```
docker wait [OPTIONS] CONTAINER [CONTAINER...]
```

**实例**

```
docker wait CONTAINER
```

 

### 8、docker export : 将文件系统作为一个tar归档文件导出到STDOUT

docker export命令创建一个tar文件，并且移除了元数据和不必要的层，将多个层整合成了一个层，只保存了当前统一视角看到的内容（译者注：expoxt后 的容器再import到Docker中，通过docker images –tree命令只能看到一个镜像；而save后的镜像则不同，它能够看到这个镜像的历史镜像）。

**语法**

```
docker export [OPTIONS] CONTAINER
```

OPTIONS说明：

·        **-o :**将输入内容写到文件。

**实例**

将id为a404c6c174a2的容器按日期保存为tar文件。

```
runoob@runoob:~$ docker export -o mysql-`date +%Y%m%d`.tar a404c6c174a2
runoob@runoob:~$ ls mysql-`date +%Y%m%d`.tar
mysql-20160711.tar
```

 

### 9、docker port : 列出指定的容器的端口映射，或者查找将PRIVATE_PORT NAT到面向公众的端口

**语法**

```
docker port [OPTIONS] CONTAINER [PRIVATE_PORT[/PROTO]]
```

**实例**

查看容器mynginx的端口映射情况。

```
runoob@runoob:~$ docker port mymysql
3306/tcp -> 0.0.0.0:3306
```

 

## 三、容器rootfs命令

### 1、docker commit : 从容器创建一个新的镜像

当我们在制作自己的镜像的时候，会在container中安装一些工具、修改配置，如果不做commit保存起来，那么container停止以后再启动，这些更改就消失了。

```
docker commit <container> [repo:tag]
```

后面的repo:tag可选

只能提交正在运行的container，即通过docker ps可以看见的容器，

查看刚运行过的容器

```
# docker ps -l
CONTAINER ID   IMAGE     COMMAND      CREATED       STATUS        PORTS   NAMES
c9fdf26326c9   nginx:1   nginx -g..   3 hours ago   Exited (0)..     nginx_test
```

启动一个已存在的容器（run是从image新建容器后再启动），以下也可以使用docker start nginx_test代替  

```
[root@hostname docker]# docker start c9fdf26326c9
c9fdf26326c9

docker run -i -t --sig-proxy=false 21ffe545748baf /bin/bash
nginx服务没有启动

# docker commit -m "some tools installed" fcbd0a5348ca seanlook/ubuntu:14.10_tutorial
fe022762070b09866eaab47bc943ccb796e53f3f416abf3f2327481b446a9503
-a "seanlook7@gmail.com"

```

请注意，当你反复去commit一个容器的时候，每次都会得到一个新的IMAGE ID，假如后面的repository:tag没有变，通过docker images可以看到，之前提交的那份镜像的repository:tag就会变成<none>:<none>，所以尽量避免反复提交。



另外，注意以下几点:

commit container只会pause住容器，这是为了保证容器文件系统的一致性，但不会stop。如果你要对这个容器继续做其他修改：

l  你可以重新提交得到新image2，删除次新的image1

l  也可以关闭容器用新image1启动，继续修改，提交image2后删除image1

 

当然这样会很痛苦，所以一般是采用Dockerfile来build得到最终image。

虽然产生了一个新的image，并且你可以看到大小有100MB，但从commit过程很快就可以知道实际上它并没有独立占用100MB的硬盘空间，而只是在旧镜像的基础上修改，它们共享大部分公共的“片”。

 

**语法**

```
docker commit [OPTIONS] CONTAINER [REPOSITORY[:TAG]]
```

OPTIONS说明：

·        **-a :**提交的镜像作者；

·        **-c :**使用Dockerfile指令来创建镜像；

·        **-m :**提交时的说明文字；

·        **-p :**在commit时，将容器暂停。

**实例**

将容器a404c6c174a2 保存为新的镜像,并添加提交人信息和说明信息。

```
runoob@runoob:~$ docker commit -a "runoob.com" -m "my apache" a404c6c174a2  mymysql:v1 
sha256:37af1236adef1544e8886be23010b66577647a40bc02c0885a6600b33ee28057
runoob@runoob:~$ docker images mymysql:v1
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
mymysql             v1                  37af1236adef        15 seconds ago      329 MB
```

 

### 2、docker cp : 用于容器与主机之间的数据拷贝

**语法**

```
docker cp [OPTIONS] CONTAINER:SRC_PATH DEST_PATH|-
docker cp [OPTIONS] SRC_PATH|- CONTAINER:DEST_PATH
```

OPTIONS说明：

·        **-L :**保持源目标中的链接

**实例**

将主机/www/runoob目录拷贝到容器96f7f14e99ab的/www目录下。

```
docker cp /www/runoob 96f7f14e99ab:/www/
```

将主机/www/runoob目录拷贝到容器96f7f14e99ab中，目录重命名为www。

```
docker cp /www/runoob 96f7f14e99ab:/www
```

将容器96f7f14e99ab的/www目录拷贝到主机的/tmp目录中。

```
docker cp  96f7f14e99ab:/www /tmp/
```

 

### 3、docker diff : 检查容器里文件结构的更改

**语法**

```
docker diff [OPTIONS] CONTAINER
```

**实例**

查看容器mymysql的文件结构更改。

```
runoob@runoob:~$ docker diff mymysql
A /logs
A /mysql_data
C /run
C /run/mysqld
A /run/mysqld/mysqld.pid
A /run/mysqld/mysqld.sock
C /tmp
```

 

 

## 四、镜像仓库

### 1、login/logout

**docker login :** 登陆到一个Docker镜像仓库，如果未指定镜像仓库地址，默认为官方仓库 Docker Hub

**docker logout :** 登出一个Docker镜像仓库，如果未指定镜像仓库地址，默认为官方仓库 Docker Hub

**语法**

```
docker login [OPTIONS] [SERVER]
docker logout [OPTIONS] [SERVER]
```

OPTIONS说明：

·        **-u :**登陆的用户名

·        **-p :**登陆的密码

**实例**

登陆到Docker Hub

```
docker login -u 用户名 -p 密码
```

登出Docker Hub

```
docker logout
```

 

### 2、docker pull : 从镜像仓库中拉取或者更新指定镜像

\# docker pull centos

上面的命令需要注意，在docker v1.2版本以前，会下载官方镜像的centos仓库里的所有镜像，而从v.13开始官方文档里的说明变了：will pull the centos:latest image, its intermediate layers and any aliases of the same id，也就是只会下载tag为latest的镜像（以及同一images id的其他tag）。

 

也可以明确指定具体的镜像：

```
# docker pull centos:centos6
```

 当然也可以从某个人的公共仓库（包括自己是私人仓库）拉取，形如docker pull username/repository<:tag_name> ：

```
# docker pull seanlook/centos:centos6
```

如果你没有网络，或者从其他私服获取镜像，形如docker pull registry.domain.com:5000/repos:<tag_name>

```
# docker pull dl.dockerpool.com:5000/mongo:latest
```

**语法**

```
docker pull [OPTIONS] NAME[:TAG|@DIGEST]
```

OPTIONS说明：

·        **-a :**拉取所有 tagged 镜像

·        **--disable-content-trust :**忽略镜像的校验,默认开启

**实例**

从Docker Hub下载java最新版镜像。

```
docker pull java
```

从Docker Hub下载REPOSITORY为java的所有镜像。

```
docker pull -a java
```

 

### **3、**  docker push : 将本地的镜像上传到镜像仓库,要先登陆到镜像仓库

与上面的pull对应，可以推送到Docker Hub的Public、Private以及私服，但不能推送到Top Level Repository。

```
# docker push seanlook/mongo
# docker push registry.tp-link.net:5000/mongo:2014-10-27
```

registry.tp-link.net也可以写成IP，172.29.88.222。

在repository不存在的情况下，命令行下push上去的会为我们创建为私有库，然而通过浏览器创建的默认为公共库。

**语法**

```
docker push [OPTIONS] NAME[:TAG]
```

OPTIONS说明：

·        **--disable-content-trust :**忽略镜像的校验,默认开启

**实例**

上传本地镜像myapache:v1到镜像仓库中。

```
docker push myapache:v1
```

 

### 4、docker search : 从Docker Hub查找镜像

**语法**

```
docker search [OPTIONS] TERM
```

OPTIONS说明：

·        **--automated :**只列出 automated build类型的镜像；

·        **--no-trunc :**显示完整的镜像描述；

·        **-s :**列出收藏数不小于指定值的镜像。

**实例**

从Docker Hub查找所有镜像名包含java，并且收藏数大于10的镜像

```
runoob@runoob:~$ docker search -s 10 java
NAME                  DESCRIPTION                           STARS   OFFICIAL   AUTOMATED
java                  Java is a concurrent, class-based...   1037    [OK]       
anapsix/alpine-java   Oracle Java 8 (and 7) with GLIBC ...   115                [OK]
develar/java                                                 46                 [OK]
isuper/java-oracle    This repository contains all java...   38                 [OK]
lwieske/java-8        Oracle Java 8 Container - Full + ...   27                 [OK]
nimmis/java-centos    This is docker images of CentOS 7...   13                 [OK]
```

 

## 五、本地镜像管理

### 1、 docker images : 列出本地镜像

我们可以根据REPOSITORY来判断这个镜像是来自哪个服务器，如果没有 / 则表示官方镜像，类似于username/repos_name表示Github的个人公共库，类似于regsistory.example.com:5000/repos_name则表示的是私服。

IMAGE ID列其实是缩写，要显示完整则带上--no-trunc选项.

**语法**

```
docker images [OPTIONS] [REPOSITORY[:TAG]]
```

OPTIONS说明：

·        **-a :**列出本地所有的镜像（含中间映像层，默认情况下，过滤掉中间映像层）；

·        **--digests :**显示镜像的摘要信息；

·        **-f :**显示满足条件的镜像；

·        **--format :**指定返回值的模板文件；

·        **--no-trunc :**显示完整的镜像信息；

·        **-q :**只显示镜像ID。

**实例**

查看本地镜像列表。

```
runoob@runoob:~$ docker images
REPOSITORY              TAG                 IMAGE ID            CREATED             SIZE
mymysql                 v1                  37af1236adef        5 minutes ago       329 MB
runoob/ubuntu           v4                  1c06aa18edee        2 days ago          142.1 MB
<none>                  <none>              5c6e1090e771        2 days ago          165.9 MB
httpd                   latest              ed38aaffef30        11 days ago         195.1 MB
alpine                  latest              4e38e38c8ce0        2 weeks ago         4.799 MB
mongo                   3.2                 282fd552add6        3 weeks ago         336.1 MB
redis                   latest              4465e4bcad80        3 weeks ago         185.7 MB
php                     5.6-fpm             025041cd3aa5        3 weeks ago         456.3 MB
python                  3.5                 045767ddf24a        3 weeks ago         684.1 MB
...
```

列出本地镜像中REPOSITORY为ubuntu的镜像列表。

```
root@runoob:~# docker images  ubuntu
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu              14.04               90d5884b1ee0        9 weeks ago         188 MB
ubuntu              15.10               4e3b13c8a266        3 months ago        136.3 MB
```

 

### 2、docker rmi : 删除本地一个或多少镜像

你可能在使用过程中会build或commit许多镜像，无用的镜像需要删除。但删除这些镜像是有一些条件的：

•   同一个IMAGE ID可能会有多个TAG（可能还在不同的仓库），首先你要根据这些 image names 来删除标签，当删除最后一个tag的时候就会自动删除镜像；

•   承上，如果要删除的多个IMAGE NAME在同一个REPOSITORY，可以通过docker rmi <image_id>来同时删除剩下的TAG；若在不同Repo则还是需要手动逐个删除TAG；

•   还存在由这个镜像启动的container时（即便已经停止），也无法删除镜像；

**语法**

```
docker rmi [OPTIONS] IMAGE [IMAGE...]
```

OPTIONS说明：

·        **-f :**强制删除；

·        **--no-prune :**不移除该镜像的过程镜像，默认移除；

**实例**

强制删除本地镜像runoob/ubuntu:v4。

```
root@runoob:~# docker rmi -f runoob/ubuntu:v4
Untagged: runoob/ubuntu:v4
Deleted: sha256:1c06aa18edee44230f93a90a7d88139235de12cd4c089d41eed8419b503072be
Deleted: sha256:85feb446e89a28d58ee7d80ea5ce367eebb7cec70f0ec18aa4faa874cbd97c73
```

 

### 3、docker tag : 标记本地镜像，将其归入某一仓库

tag的作用主要有两点：一是为镜像起一个容易理解的名字，二是可以通过docker tag来重新指定镜像的仓库，这样在push时自动提交到仓库。

将同一IMAGE_ID的所有tag，合并为一个新的

```
# docker tag 195eb90b5349 seanlook/ubuntu:rm_test
```

新建一个tag，保留旧的那条记录

```
# docker tag Registry/Repos:Tag New_Registry/New_Repos:New_Tag
```

**语法**

```
docker tag [OPTIONS] IMAGE[:TAG] [REGISTRYHOST/][USERNAME/]NAME[:TAG]
```

**实例**

将镜像ubuntu:15.10标记为 runoob/ubuntu:v3 镜像。

```
root@runoob:~# docker tag ubuntu:15.10 runoob/ubuntu:v3
root@runoob:~# docker images   runoob/ubuntu:v3
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
runoob/ubuntu       v3                  4e3b13c8a266        3 months ago        136.3 MB
```

 

### 4、docker build : 使用Dockerfile创建镜像

build命令可以从Dockerfile和上下文来创建镜像：

```
docker build [OPTIONS] PATH | URL | -
```

上面的PATH或URL中的文件被称作上下文，build image的过程会先把这些文件传送到docker的服务端来进行的。

如果PATH直接就是一个单独的Dockerfile文件则可以不需要上下文；如果URL是一个Git仓库地址，那么创建image的过程中会自动git clone一份到本机的临时目录，它就成为了本次build的上下文。无论指定的PATH是什么，Dockerfile是至关重要的，请参考Dockerfile Reference。

请看下面的例子：

```
# cat Dockerfile 
FROM seanlook/nginx:bash_vim
EXPOSE 80
ENTRYPOINT /usr/sbin/nginx -c /etc/nginx/nginx.conf && /bin/bash

# docker build -t seanlook/nginx:bash_vim_Df .
Sending build context to Docker daemon 73.45 MB
Sending build context to Docker daemon 
Step 0 : FROM seanlook/nginx:bash_vim
 ---> aa8516fa0bb7
Step 1 : EXPOSE 80
 ---> Using cache
 ---> fece07e2b515
Step 2 : ENTRYPOINT /usr/sbin/nginx -c /etc/nginx/nginx.conf && /bin/bash
 ---> Running in e08963fd5afb
 ---> d9bbd13f5066
 
Removing intermediate container e08963fd5afb
Successfully built d9bbd13f5066
```

上面的PATH为.，所以在当前目录下的所有文件（不包括.dockerignore中的）将会被tar打包并传送到docker daemon（一般在本机），从输出我们可以到Sending build context...，最后有个Removing intermediate container的过程，可以通过--rm=false来保留容器。

通过git获取dockerfile的例子：docker build github.com/creack/docker-firefox

**语法**

```
docker build [OPTIONS] PATH | URL | -
```

OPTIONS说明：

·        **--build-arg=[] :**设置镜像创建时的变量；

·        **--cpu-shares :**设置 cpu 使用权重；

·        **--cpu-period :**限制 CPU CFS周期；

·        **--cpu-quota :**限制 CPU CFS配额；

·        **--cpuset-cpus :**指定使用的CPU id；

·        **--cpuset-mems :**指定使用的内存 id；

·        **--disable-content-trust :**忽略校验，默认开启；

·        **-f :**指定要使用的Dockerfile路径；

·        **--force-rm :**设置镜像过程中删除中间容器；

·        **--isolation :**使用容器隔离技术；

·        **--label=[] :**设置镜像使用的元数据；

·        **-m :**设置内存最大值；

·        **--memory-swap :**设置Swap的最大值为内存+swap，"-1"表示不限swap；

·        **--no-cache :**创建镜像的过程不使用缓存；

·        **--pull :**尝试去更新镜像的新版本；

·        **-q :**安静模式，成功后只输出镜像ID；

·        **--rm :**设置镜像成功后删除中间容器；

·        **--shm-size :**设置/dev/shm的大小，默认值是64M；

·        **--ulimit :**Ulimit配置。

**实例**

使用当前目录的Dockerfile创建镜像。

```
docker build -t runoob/ubuntu:v1 . 
```

使用URL **github.com/creack/docker-firefox** 的 Dockerfile 创建镜像。

```
docker build github.com/creack/docker-firefox
```

 

### 5、docker history : 查看指定镜像的创建历史

**语法**

```
docker history [OPTIONS] IMAGE
```

OPTIONS说明：

·        **-H :**以可读的格式打印镜像大小和日期，默认为true；

·        **--no-trunc :**显示完整的提交记录；

·        **-q :**仅列出提交记录ID。

**实例**

查看本地镜像runoob/ubuntu:v3的创建历史。

```
root@runoob:~# docker history runoob/ubuntu:v3
IMAGE             CREATED           CREATED BY                                      SIZE      COMMENT
4e3b13c8a266      3 months ago      /bin/sh -c #(nop) CMD ["/bin/bash"]             0 B                 
<missing>         3 months ago      /bin/sh -c sed -i 's/^#\s*\(deb.*universe\)$/   1.863 kB            
<missing>         3 months ago      /bin/sh -c set -xe   && echo '#!/bin/sh' > /u   701 B               
<missing>         3 months ago      /bin/sh -c #(nop) ADD file:43cb048516c6b80f22   136.3 MB
```

 

### 6、docker save : 将指定镜像保存成 tar 归档文件

docker save命令会创建一个镜像的压缩文件，这个文件能够在另外一个主机的Docker上使用。和export命令不同，这个命令为每一个层都保存了它们的元数据。这个命令只能对镜像生效。

**语法**

```
docker save [OPTIONS] IMAGE [IMAGE...]
```

OPTIONS说明：

·        **-o :**输出到的文件。

**实例**

将镜像runoob/ubuntu:v3 生成my_ubuntu_v3.tar文档

```
runoob@runoob:~$ docker save -o my_ubuntu_v3.tar runoob/ubuntu:v3
runoob@runoob:~$ ll my_ubuntu_v3.tar
-rw------- 1 runoob runoob 142102016 Jul 11 01:37 my_ubuntu_v3.ta
```

 

### 7、docker load

从 tar 镜像归档中载入镜像， docker save 的逆操作。保存后再加载（saved-loaded）的镜像不会丢失提交历史和层，可以回滚。

将 ubuntu14.04.tar 文件载入镜像中

```
docker load -i ubuntu14.04.tar
```

参数：

```
  -i, --input=       Read from a tar archive file, instead of STDIN 加载的tar文件
```

 

#### **docker镜像文件导入与导出**

1. 查看镜像id

```
sudo docker images
REPOSITORY               TAG                 IMAGE ID            CREATED             SIZE
quay.io/calico/node      v1.0.1              c70511a49fa1        6 weeks ago         257 MB
hello-world              latest              48b5124b2768        2 months ago        1.84 kB
quay.io/coreos/flannel   v0.7.0              63cee19df39c        2 months ago        73.8 MB
quay.io/calico/cni       v1.5.5              ada87b3276f3        2 months ago        67.1 MB
```

2. 选择要打包的镜像，执行打包命令

```
sudo docker save -o quay.io-calico-node-1.tar quay.io/calico/node 
```

会在当前目录下生成导出文件xxx.tar，然后将此文件下载到本地

3. 在开发环境导入上述打包的镜像

```
docker load -i quay.io-calico-node-1.tar
0a43edc59c00: Loading layer 27.59 MB/27.59 MB
69a5574b2581: Loading layer 3.636 MB/3.636 MB
fb0933709f36: Loading layer 3.913 MB/3.913 MB
7384abd120f5: Loading layer 3.859 MB/3.859 MB
e34911610de0: Loading layer 27.06 MB/27.06 MB
d6ec327c8cbe: Loading layer 6.656 kB/6.656 kB
Loaded image ID: sha256:ada87b3276f307a6b1b1ada15820b6c9842fd839fe5cc46ad5db8af81f7fd271
```

 

### 8、docker import : 从归档文件中创建镜像

**语法**

```
docker import [OPTIONS] file|URL|- [REPOSITORY[:TAG]]
```

OPTIONS说明：

·        **-c :**应用docker 指令创建镜像；

·        **-m :**提交时的说明文字；

**实例**

从镜像归档文件my_ubuntu_v3.tar创建镜像，命名为runoob/ubuntu:v4

```
runoob@runoob:~$ docker import  my_ubuntu_v3.tar runoob/ubuntu:v4  
sha256:63ce4a6d6bc3fabb95dbd6c561404a309b7bdfc4e21c1d59fe9fe4299cbfea39
runoob@runoob:~$ docker images runoob/ubuntu:v4
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
runoob/ubuntu       v4                  63ce4a6d6bc3        20 seconds ago      142.1 MB
```

 

## 六、其他命令

### 1、docker info : 显示 Docker 系统信息，包括镜像和容器数

**语法**

```
docker info [OPTIONS]
```

**实例**

查看docker系统信息。

```
$ docker info
Containers: 12
Images: 41
Storage Driver: aufs
 Root Dir: /var/lib/docker/aufs
 Backing Filesystem: extfs
 Dirs: 66
 Dirperm1 Supported: false
Execution Driver: native-0.2
Logging Driver: json-file
Kernel Version: 3.13.0-32-generic
Operating System: Ubuntu 14.04.1 LTS
CPUs: 1
Total Memory: 1.954 GiB
Name: iZ23mtq8bs1Z
ID: M5N4:K6WN:PUNC:73ZN:AONJ:AUHL:KSYH:2JPI:CH3K:O4MK:6OCX:5OYW
```

 

### 2、docker version :显示 Docker 版本信息。

**语法**

```
docker version [OPTIONS]
```

OPTIONS说明：

·        **-f :**指定返回值的模板文件。

**实例**

显示 Docker 版本信息。

```
$ docker version
Client:
 Version:      1.8.2
 API version:  1.20
 Go version:   go1.4.2
 Git commit:   0a8c2e3
 Built:        Thu Sep 10 19:19:00 UTC 2015
 OS/Arch:      linux/amd64
 
Server:
 Version:      1.8.2
 API version:  1.20
 Go version:   go1.4.2
 Git commit:   0a8c2e3
 Built:        Thu Sep 10 19:19:00 UTC 2015
 OS/Arch:      linux/amd64
```

 