# MacOS-M1安装Nacos

最简单的方法是通过docker的方式部署，按照以下操作步骤执行即可：

```
# 获取适配M1的镜像
docker pull zhusaidong/nacos-server-m1:2.0.3

# 启动docker，内存可以修改为256m
docker run --name nacos-standalone -e MODE=standalone -e JVM_XMS=512m -e JVM_XMX=512m -e JVM_XMN=256m -p 8848:8848 -d zhusaidong/nacos-server-m1:2.0.3

# 启动后可以访问以下地址登录Nacos，默认的用户名密码：nacos/nacos
http://127.0.0.1:8848/nacos/index.html

# 如果需要停止nacos，先找到容器id，如果查找所有容器，可以加上 -a 参数，例如
docker ps -a

# 启动已存在的容器
docker start 容器ID

# 停止容器
docker stop 容器ID

# 如果需要删除docker
docker rm 容器ID
```



小内存启动命令

```
docker run --name nacos-standalone -e MODE=standalone -e JVM_XMS=128m -e JVM_XMX=128m -e JVM_XMN=64m -p 8848:8848 -d zhusaidong/nacos-server-m1:2.0.3
```



进入容器中命令

```
docker exec -it nacos-standalone bash
```

