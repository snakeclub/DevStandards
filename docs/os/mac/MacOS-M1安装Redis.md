# MacOS-M1安装Redis

## docker模式安装单机版

```
# 获取最新版本的镜像
docker pull redis:latest

# 查看本地镜像，Redis是否下载成功
docker images

# 启动容器
docker run -itd --name redis-standalone -p 6379:6379 redis

# 注: 如果需要指定配置，可以挂载容器外部的配置文件，例如
# docker run -p 6379:6379 --name redis-standalone -v /data/redis/redis.conf:/etc/redis/redis.conf  -v /data/redis/data:/data -d redis redis-server /etc/redis/redis.conf --appendonly yes

# 如果需要停止nacos，先找到容器id，如果查找所有容器，可以加上 -a 参数，例如
docker ps -a

# 启动已存在的容器
docker start 容器ID

# 停止容器
docker stop 容器ID

# 如果需要删除docker
docker rm 容器ID
```



##  Redis连接测试

```
# 进入容器
docker exec -it redis-standalone /bin/bash

# 使用客户端连接redis
redis-cli

# 设置键值对
set test 1

# 获取test的值
get test

# 查询所有键值对的键名
keys *

# 删除 test 键值对
del test
```



