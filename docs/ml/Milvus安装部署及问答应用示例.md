# Milvus安装部署及问答应用示例

## 安装部署手册（ubuntu 18.04）

### 安装docker

1、删除以前的版本（ubuntu默认的docker安装版本比较低）

```
$ sudo apt-get remove docker docker-engine docker.io containerd runc
或
$ sudo apt-get autoremove docker docker-engine docker.io containerd runc
```

2、设置docker仓库（Docker repository）：

```
$ sudo apt-get update
$ sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
   
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
$ sudo apt-key fingerprint 0EBFCD88

$ sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
```

注：如果安装的包出现问题，有可能是apt资源镜像有问题，导致依赖问题无法安装，国内建议的镜像地址设置如下：

```
sudo vi /etc/apt/sources.list

修改为以下内容：
# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
 
# 预发布软件源，不建议启用
# deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-proposed main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-proposed main restricted universe multiverse
```

3、安装最新版本的docker

```
 $ sudo apt-get update
 $ sudo apt-get install docker-ce docker-ce-cli containerd.io
```

4、验证docker引擎是否正常

```
$ sudo docker run hello-world
```

5、确认 Docker daemon 正在运行（获取docker信息）

```
$ sudo docker info

Client:
 Debug Mode: false

Server:
 Containers: 1
  Running: 0
  Paused: 0
  Stopped: 1
 Images: 1
 Server Version: 19.03.11
 Storage Driver: aufs
  Root Dir: /var/lib/docker/aufs
  Backing Filesystem: extfs
  Dirs: 3
  Dirperm1 Supported: true
 Logging Driver: json-file
 Cgroup Driver: cgroupfs
 Plugins:
  Volume: local
  Network: bridge host ipvlan macvlan null overlay
  Log: awslogs fluentd gcplogs gelf journald json-file local logentries splunk syslog
 Swarm: inactive
 Runtimes: runc
 Default Runtime: runc
 Init Binary: docker-init
 containerd version: 7ad184331fa3e55e52b890ea95e65ba581ae3429
 runc version: dc9208a3303feef5b3839f4323d9beb36df0a9dd
 init version: fec3683
 Security Options:
  apparmor
  seccomp
   Profile: default
 Kernel Version: 5.3.0-53-generic
 Operating System: Ubuntu 18.04.4 LTS
 OSType: linux
 Architecture: x86_64
 CPUs: 16
 Total Memory: 31.27GiB
 Name: ubuntu18-System-Product-Name
 ID: KNRC:QGCU:2JKW:NPPI:M5KR:UTYI:NXF4:5BJZ:XEU6:HW7J:UOQN:X7TC
 Docker Root Dir: /var/lib/docker
 Debug Mode: false
 Registry: https://index.docker.io/v1/
 Labels:
 Experimental: false
 Insecure Registries:
  127.0.0.0/8
 Live Restore Enabled: false

WARNING: No swap limit support
WARNING: the aufs storage-driver is deprecated, and will be removed in a future release.
```

6、增加docker中国区镜像，提高下载速度

```
$sudo vi /etc/docker/daemon.json

新建或增加以下内容
{
    "registry-mirrors": ["https://registry.docker-cn.com"]
}
```



### 设置使用非root用户使用docker

1、创建docker用户组

```
$ sudo groupadd docker
```

2、将需要使用的用户加入该用户组

```
$ sudo usermod -aG docker ubuntu18
```



### 安装Milvus

官方文档：https://milvus.io/cn/docs/v0.10.0/guides/get_started/install_milvus/cpu_milvus_docker.md

1、通过docker pull获取docker镜像

```
sudo docker pull milvusdb/milvus:0.10.0-cpu-d061620-5f3c00
```

注:  安装过程可能会遇到以下问题，可参考以下解决方案

（1）docker pull中间取消后，重新获取出现“Repository milvusdb/milvus already being pulled by another client. Waiting.”错误，该问题是一个bug，可以通过重启docker方法解决：

```
sudo service docker stop
sudo service docker start
```

2、下载配置文件

```
$ mkdir -p /home/ubuntu18/milvus/conf
$ cd /home/ubuntu18/milvus/conf
$ wget https://raw.githubusercontent.com/milvus-io/milvus/v0.10.0/core/conf/demo/server_config.yaml
```

注：如果下载不了，可自行编辑创建该配置文件

3、启动容器

```
$ sudo docker run -d --name milvus_cpu_0.10.0 \
-p 19530:19530 \
-p 19121:19121 \
-v /home/ubuntu18/milvus/db:/var/lib/milvus/db \
-v /home/ubuntu18/milvus/conf:/var/lib/milvus/conf \
-v /home/ubuntu18/milvus/logs:/var/lib/milvus/logs \
-v /home/ubuntu18/milvus/wal:/var/lib/milvus/wal \
milvusdb/milvus:0.10.0-cpu-d061620-5f3c00
```

上述命令中用到的 `docker run` 参数定义如下：

- `-d`: 运行 container 到后台并打印 container id。
- `--name`: 为 container 分配一个名字。
- `-p`: 暴露 container 端口到 host。
- `-v`: 将路径挂载至 container。

4、确认 Milvus 运行状态

```
$ docker ps
```

如果docker没有正常启动，可以执行以下命令查看错误日志：

```
 # 获得运行 Milvus 的 container ID。
 $ docker ps -a
 # 检查 docker 日志。
 $ docker logs <milvus container id>
```



### 运行示例程序

官方文档：https://milvus.io/cn/docs/v0.10.0/guides/get_started/example_code.md

1、安装 Milvus Python SDK

```
pip3 install pymilvus==0.2.13
pip3 install --upgrade pymilvus==0.2.1
```

2、创建示例代码example.py（下载地址：https://raw.githubusercontent.com/milvus-io/pymilvus/0.2.13/examples/example.py）：

```
# This program demos how to connect to Milvus vector database, 
# create a vector collection,
# insert 10 vectors, 
# and execute a vector similarity search.

import random
import numpy as np

from milvus import Milvus, IndexType, MetricType, Status

# Milvus server IP address and port.
# You may need to change _HOST and _PORT accordingly.
_HOST = '127.0.0.1'
_PORT = '19530'  # default value
# _PORT = '19121'  # default http value

# Vector parameters
_DIM = 128  # dimension of vector

_INDEX_FILE_SIZE = 32  # max file size of stored index


def main():
    # Specify server addr when create milvus client instance
    # milvus client instance maintain a connection pool, param
    # `pool_size` specify the max connection num.
    milvus = Milvus(_HOST, _PORT)

    # Create collection demo_collection if it dosen't exist.
    collection_name = 'example_collection_'

    status, ok = milvus.has_collection(collection_name)
    if not ok:
        param = {
            'collection_name': collection_name,
            'dimension': _DIM,
            'index_file_size': _INDEX_FILE_SIZE,  # optional
            'metric_type': MetricType.L2  # optional
        }

        milvus.create_collection(param)

    # Show collections in Milvus server
    _, collections = milvus.list_collections()

    # Describe demo_collection
    _, collection = milvus.get_collection_info(collection_name)
    print(collection)

    # 10000 vectors with 128 dimension
    # element per dimension is float32 type
    # vectors should be a 2-D array
    vectors = [[random.random() for _ in range(_DIM)] for _ in range(10)]
    print(vectors)
    # You can also use numpy to generate random vectors:
    #   vectors = np.random.rand(10000, _DIM).astype(np.float32)

    # Insert vectors into demo_collection, return status and vectors id list
    status, ids = milvus.insert(collection_name=collection_name, records=vectors)
    if not status.OK():
        print("Insert failed: {}".format(status))

    # Flush collection  inserted data to disk.
    milvus.flush([collection_name])
    # Get demo_collection row count
    status, result = milvus.count_entities(collection_name)

    # present collection statistics info
    _, info = milvus.get_collection_stats(collection_name)
    print(info)

    # Obtain raw vectors by providing vector ids
    status, result_vectors = milvus.get_entity_by_id(collection_name, ids[:10])

    # create index of vectors, search more rapidly
    index_param = {
        'nlist': 2048
    }

    # Create ivflat index in demo_collection
    # You can search vectors without creating index. however, Creating index help to
    # search faster
    print("Creating index: {}".format(index_param))
    status = milvus.create_index(collection_name, IndexType.IVF_FLAT, index_param)

    # describe index, get information of index
    status, index = milvus.get_index_info(collection_name)
    print(index)

    # Use the top 10 vectors for similarity search
    query_vectors = vectors[0:10]

    # execute vector similarity search
    search_param = {
        "nprobe": 16
    }

    print("Searching ... ")

    param = {
        'collection_name': collection_name,
        'query_records': query_vectors,
        'top_k': 1,
        'params': search_param,
    }

    status, results = milvus.search(**param)
    if status.OK():
        # indicate search result
        # also use by:
        #   `results.distance_array[0][0] == 0.0 or results.id_array[0][0] == ids[0]`
        if results[0][0].distance == 0.0 or results[0][0].id == ids[0]:
            print('Query result is correct')
        else:
            print('Query result isn\'t correct')

        # print results
        print(results)
    else:
        print("Search failed. ", status)

    # Delete demo_collection
    status = milvus.drop_collection(collection_name)


if __name__ == '__main__':
    main()
```

3、运行示例代码

```
python3 example.py
```

如果结果中有Query result is correct，代表运行成功。



### 使用MySQL5.7作为数据管理

1、通过docker安装数据库

```
# 获取镜像
$ sudo docker pull mysql:5.7
```

2、自定义数据库的启动参数

```
# 创建本地目录
mkdir -p /home/ubuntu18/milvus/mysql/conf /home/ubuntu18/milvus/mysql/logs /home/ubuntu18/milvus/mysql/data

# 启动镜像
$ docker run -p 3306:3306 --name mysql5.7 -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.7

# 获取dockers的容器id (CONTAINER ID)
$ docker ps

# 复制docker默认的mysql配置文件，用于修改成自己的配置文件
$ docker cp 2d1d71afff2f:/etc/mysql/mysql.cnf /home/ubuntu18/milvus/mysql/conf/my.cnf

# 编辑my.cnf
$ vi my.cnf

# 删除临时docker
$ docker stop 2d1d71afff2f
$ docker rm 2d1d71afff2f
```

可以编辑的my.cnf内容如下，按需定制：

```
# 原默认内容
!includedir /etc/mysql/conf.d/
!includedir /etc/mysql/mysql.conf.d/

[client]
#客户端设置
port=3306
default-character-set=utf8mb4

[mysql.server]
default-character-set=utf8mb4

[mysqld_safe]
default-character-set=utf8mb4

[mysqld]
#mysql启动时使用的用户
user=mysql
#默认连接端口
port=3306
#端口绑定的ip地址，0.0.0.0表示允许所有远程访问，127.0.0.1表示只能本机访问，默认值为*
bind-address=0.0.0.0
 
#系统数据库编码设置，排序规则
character_set_server=utf8mb4
collation_server=utf8mb4_bin
 
#secure_auth 为了防止低版本的MySQL客户端(<4.1)使用旧的密码认证方式访问高版本的服务器。MySQL 5.6.7开始secure_auth 默认为启用值1
secure_auth=1
 
#linux下要严格区分大小写，windows下不区分大小写
#1表示不区分大小写，0表示区分大小写。
lower_case_table_names=0
```

3、启动正式的镜像

```
# 启动镜像
$ docker run -p 3306:3306 --name milvusdb \
-v /home/ubuntu18/milvus/mysql/conf/my.cnf:/etc/mysql/my.cnf \
-v /home/ubuntu18/milvus/mysql/data:/var/lib/mysql \
-v /home/ubuntu18/milvus/mysql/logs:/var/log/mysql \
-e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.7

# 进入mysql的容器命令行
$ docker exec -ti milvusdb bash

# 登陆
mysql -uroot -p123456

# 开启远程连接
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '123456' WITH GRANT OPTION;
FLUSH PRIVILEGES;

# 创建数据库
create database milvus;

# 退出
exit;
```

4、修改Milvus服务的配置文件`server_config.yaml` 

```
# 查找docker宿主机的访问IP地址
$ ip addr show docker0
3: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 56:84:7a:fe:97:99 brd ff:ff:ff:ff:ff:ff
    inet 172.17.42.1/16 scope global docker0
       valid_lft forever preferred_lft forever
    inet6 fe80::5484:7aff:fefe:9799/64 scope link 
       valid_lft forever preferred_lft forever

$ vi /home/ubuntu18/milvus/conf/server_config.yaml
```

将meta_uri参数修改为（注意IP地址）：

```
meta_uri: mysql://root:123456@172.17.42.1:3306/milvus
```

5、重启milvus服务

```
$ docker restart milvus_cpu_0.10.0
```



## 问答（QA）应用示例

开源项目：https://github.com/milvus-io/bootcamp/tree/master/solutions/QA_System

### 安装postgresql

1、安装postgresql软件

```
$ sudo apt update
$ sudo apt install postgresql postgresql-contrib
```

2、进入交互命令及简单操作

```
# 切换到postgresql所创建的postgres用户
$ sudo -i -u postgres

# 进入交互式环境
$ psql
psql (10.12 (Ubuntu 10.12-0ubuntu0.18.04.1))
Type "help" for help.
postgres=# 

# 查看所有表
postgres=# SELECT tablename FROM pg_tables; 

# 查看所有数据库用户，系统内置默认postgres用户
postgres=# \du
 Role name |                         Attributes                         | Member of 
-----------+------------------------------------------------------------+-----------
 postgres  | Superuser, Create role, Create DB, Replication, Bypass RLS | {}
```

常用命令如下：

```
\q：退出交互式命令
\h：查看SQL命令的解释，比如\h select
\l：查看所有数据库
\dt：列出当前数据库的所有表（\d）
\d table_name：列出某一张表格的结构
\du：查看所有用户
\c database_name：切换数据库
\c - user_name：切换用户
\conninfo：列出当前数据库和连接的信息
```

3、设置postgres用户的登陆密码

```
postgres=# \password postgres 
```



### 创建Python虚拟环境

1、使用anaconda创建虚拟环境

```
conda create --name milvus python=3.7

conda activate milvus
```

2、建立所需的库清单：

vi requriment.txt

```
flask-cors
numpy
flask
flask_restful
pymilvus==0.2.13
psycopg2-binary
bert-serving-server
bert-serving-client
```

3、安装所有依赖包

```
pip install -i https://mirrors.aliyun.com/pypi/simple/ tensorflow-cpu==1.15.2
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requriment.txt
```



### 启动bert服务

1、下载谷歌预训练的中文语义bert识别模型

模型地址：https://storage.googleapis.com/bert_models/2018_11_03/chinese_L-12_H-768_A-12.zip

开源项目地址：https://github.com/google-research/bert

2、解压模型

```
$ mkdir model
# 把chinese_L-12_H-768_A-12.zip上传至该目录，解压缩
$ unzip chinese_L-12_H-768_A-12.zi
```

3、启动模型服务

```
$ nohup bert-serving-start -model_dir /home/ubuntu18/milvus/model/chinese_L-12_H-768_A-12/ -num_worker=12 -max_seq_len=40 &

# 查看启动输出日志
$ tail -f nohup.out
```

注：也可以下载其他bert扩展模型，例如 https://github.com/ymcui/Chinese-BERT-wwm ， 直接利用下载的预训练模型启动即可：

```
$ cd /home/ubuntu18/milvus/model/chinese_wwm_ext_L-12_H-768_A-12
$ nohup bert-serving-start -model_dir /home/ubuntu18/milvus/model/chinese_wwm_ext_L-12_H-768_A-12 -num_worker=12 -max_seq_len=40 &
```





### 部署问答（QA）示例应用

1、从github获取应用源码

地址：https://github.com/milvus-io/bootcamp/tree/master/solutions/QA_System

2、部署到服务器上，路径: /home/ubuntu18/milvus/qa_system/

3、修改配置文件，主要是postgresql的登陆用户密码、及数据库信息：

```
$ vi /home/ubuntu18/milvus/qa_system/QA-search-server/src/config.py

# 编辑以下内容
MILVUS_HOST = os.getenv("MILVUS_HOST", "127.0.0.1")
MILVUS_PORT = os.getenv("MILVUS_PORT", 19530)


PG_HOST = os.getenv("PG_HOST", "127.0.0.1")
PG_PORT = os.getenv("PG_PORT", 5432)
PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD", "123456")
PG_DATABASE = os.getenv("PG_DATABASE", "postgres")

DEFAULT_TABLE = os.getenv("DEFAULT_TABLE", "milvus_qa")
```

4、导入测试问答数据

```
$ cd /home/ubuntu18/milvus/qa_system
$ python QA-search-server/main.py --collection milvus_qa --question data/question.txt --answer data/answer.txt --load
```

5、简单验证问答

```
$ cd /home/ubuntu18/milvus/qa_system
# 对应问题 “为什么嘴唇是红色的？”
$ python QA-search-server/main.py --collection milvus_qa --sentence 为什么人的嘴唇会是红色 --search
```

6、启动查询服务

```
$ cd /home/ubuntu18/milvus/qa_system
$ nohup python QA-search-server/app.py &

# 查看启动输出日志
$ tail -f nohup.out
```

7、构建并启动查询客户端

```
$ cd /home/ubuntu18/milvus/qa_system/QA-server-client
$ docker build .
Successfully built fdacd3745740
$ docker tag fdacd3745740 milvus-qa:latest
# 注意以下ip为宿主机的docker IP地址
$ docker run --name milvus_qa -d --rm -p 8001:80 -e API_URL=http://10.16.85.63:5000/ milvus-qa:latest
```

8、可以通过外部浏览器访问客户端：http://主机的IP地址:8001/



### 清除问答数据

1、清除答案库

```
# 切换到postgresql所创建的postgres用户
$ sudo -i -u postgres

# 进入交互式环境
$ psql
psql (10.12 (Ubuntu 10.12-0ubuntu0.18.04.1))
Type "help" for help.
postgres=# 

# 删除表数据
postgres=# delete from milvus_qa;
```

2、清除问题向量库





## 附件：MySQL的my.cnf配置参数参考

```
[client]
#客户端设置
port=3306
socket=/data/mysql/data/mysql.sock
default-character-set=utf8mb4

[mysqld]
#mysql启动时使用的用户
user=mysql
#默认连接端口
port=306
#为MySQL客户端程序和服务器之间的本地通讯指定一个套接字文件
socket=/data/mysql/data/mysql.sock
#数据库服务器id，这个id用来在主从服务器中标记唯一mysql服务器
server-id=1
#端口绑定的ip地址，0.0.0.0表示允许所有远程访问，127.0.0.1表示只能本机访问，默认值为*
bind-address=0.0.0.0
#默认名为 主机名.pid,在数据库/mysql/data/主机名.pid,记录mysql运行的process id
#如果存在，再次start时会报已经启动
pid-file=/data/mysql/data/mysql.pid
 
#安装目录
basedir=/usr/local/mysql
#数据库存放目录
datadir=/data/mysql/data/
 
#系统数据库编码设置，排序规则
character_set_server = utf8mb4
collation_server = utf8mb4_bin
 
#secure_auth 为了防止低版本的MySQL客户端(<4.1)使用旧的密码认证方式访问高版本的服务器。MySQL 5.6.7开始secure_auth 默认为启用值1
secure_auth = 1
 
#可能的连接数
#指出在MySQL暂时停止响应新请求之前的短时间内多少个请求可以被存在堆栈中。
back_log = 1024
 
#########################################
#################其他设置################
#########################################
 
#显式指定默认时间戳，即定义表中的timestamp时间戳的列时需要显示指定默认值
#默认为OFF，
#如果第一个TIMESTAMP列，没有显式设置DEFAULT，将自动分配DEFAULT CURRENT_TIMESTAMP和ON UPDATE CURRENT_TIMESTAMP属性
#timestamp列不能设置为NULL,第二列及以后的timestamp列都默认为"0000-00-00 00:00:00"
#如果设置为ON，
#第一个timestamp列可以设置为NULL，不会默认分配DEFAULT CURRENT_TIMESTAMP和ON UPDATE CURRENT_TIMESTAMP属性
#声明为NOT NULL且没有显式DEFAULT子句，在严格模式下会报错。
explicit_defaults_for_timestamp = ON
 
#linux下要严格区分大小写，windows下不区分大小写
#1表示不区分大小写，0表示区分大小写。
#lower_case_table_names = 0
lower_case_table_names = 0
 
#默认sql模式，严格模式
#sql_mode = ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,
#NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
#ONLY_FULL_GROUP_BY 
#NO_ZERO_IN_DATE 不允许年月为0
#NO_ZERO_DATE 不允许插入年月为0的日期
#ERROR_FOR_DIVISION_BY_ZERO 在INSERT或UPDATE过程中，如果数据被零除，则产生错误而非警告。如 果未给出该模式，那么数据被零除时MySQL返回NULL
#NO_ENGINE_SUBSTITUTION 不使用默认的存储引擎替代
sql_mode = STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
 
 
 
########################################################
############各种缓冲区及处理数据的最大值设置############
########################################################
 
#是MySQL执行排序使用的缓冲大小。如果想要增加ORDER BY的速度，首先看是否可以让MySQL使用索引而不是额外的排序阶段
#如果不能，可以尝试增加sort_buffer_size变量的大小
sort_buffer_size = 16M
 
#应用程序经常会出现一些两表（或多表）Join的操作需求，MySQL在完成某些 Join 需求的时候（all/index join），
#为了减少参与Join的“被驱动表”的读取次数以提高性能，需要使用到 Join Buffer 来协助完成 Join操作。
#当 Join Buffer 太小，MySQL 不会将该 Buffer 存入磁盘文件，而是先将Join Buffer中的结果集与需要 Join 的表进行 Join 操作
#然后清空 Join Buffer 中的数据，继续将剩余的结果集写入此 Buffer 中，
#如此往复。这势必会造成被驱动表需要被多次读取，成倍增加 IO 访问，降低效率。
#若果多表连接需求大，则这个值要设置大一点。
join_buffer_size = 16M
 
#索引块的缓冲区大默认16M
key_buffer_size = 15M
# 消息缓冲区会用到该列，该值太小则会在处理大包时产生错误。如果使用大的text,BLOB列，必须增加该值
max_allowed_packet = 32M
 
# mysql服务器最大连接数值的设置范围比较理想的是：服务器响应的最大连接数值占服务器上限连接数值的比例值在10%以上
# Max_used_connections / max_connections * 100% 
max_connections = 512
# 阻止过多尝试失败的客户端，如果值为10时，失败（如密码错误）10次，mysql会无条件阻止用户连接
max_connect_errors = 1000000
 
#表描述符缓存大小，可减少文件打开/关闭次数,一般max_connections*2。
table_open_cache = 1024
#MySQL 缓存 table 句柄的分区的个数,每个cache_instance<=table_open_cache/table_open_cache_instances
table_open_cache_instances = 32
#mysql打开最大文件数
open_files_limit = 65535
 
 
#InnoDB表中，表更新后，查询缓存失效，事务操作提交之前，所有查询都无法使用缓存。影响查询缓存命中率
#查询缓存是靠一个全局锁操作保护的，如果查询缓存配置的内存比较大且里面存放了大量的查询结果，
#当查询缓存失效的时候，会长时间的持有这个全局锁。
#因为查询缓存的命中检测操作以及缓存失效检测也都依赖这个全局锁，所以可能会导致系统僵死的情况
#在高并发，写入量大的系统，建义把该功能禁掉
query_cache_size = 0
#决定是否缓存查询结果。这个变量有三个取值：0,1,2，分别代表了off、on、demand。
query_cache_type = 0
#指定单个查询能够使用的缓冲区大小，缺省为1M
query_cache_limit = 1M
 
 
##############################################
#################线程相关配置#################
##############################################
 
#线程缓存；主要用来存放每一个线程自身的标识信息，线程栈大小
thread_stack = 256K
 
#thread_cahe_size线程池，线程缓存。用来缓存空闲的线程，以至于不被销毁，
#如果线程缓存在的空闲线程，需要重新建立新连接，则会优先调用线程池中的缓存，很快就能响应连接请求。
#每建立一个连接，都需要一个线程与之匹配。
thread_cache_size = 384
 
#External-locking用于多进程条件下为MyISAM数据表进行锁定
#服务器访问数据表时经常需要等待解锁,因此在单服务器环境下external locking开启会让MySQL性能下降
 
#单服务器环境,使用skip-external-locking，关闭外部锁定，
#多服务器使用同一个数据库目录时，必须开启external-locking,也就是说注释掉skip-external-locking
skip-external-locking
 
 
#最大的空闲等待时间，默认是28800，单位秒，即8个小时
#通过mysql客户端连接数据库是交互式连接，通过jdbc连接数据库是非交互式连接
#交互式连接超时时间，超过这个时间自动断开连接
interactive_timeout = 600
#非交互式连接超时时间，超过这个时间自动断开连接
wait_timeout = 600
 
#它规定了内部内存临时表的最大值，每个线程都要分配。（实际起限制作用的是tmp_table_size和max_heap_table_size的最小值。）
#如果内存临时表超出了限制，MySQL就会自动地把它转化为基于磁盘的MyISAM表，存储在指定的tmpdir目录下
tmp_table_size = 96M
max_heap_table_size = 96M
 
 
 
############################
##########日志设置##########
############################
 
# 日志时间戳，mysql5.7.2版本之后才有的属性，控制写入到文件上显示日志的时间，
# 不会影响general log 和 slow log 写到表(mysql.general_log, mysql.slow_log)中的日志的时间
# 可以设置的有：UTC 和 SYSTEM，默认UTC，即0时区的时间，比北京时间慢8小时，所以要设置为SYSTEM
log_timestamps = SYSTEM
 
#日志的输出位置一般有三种方式：file(文件)，table(表)，none(不保存)
#其中前两个输出位置可以同时定义，none表示是开启日志功能但是不记录日志信息。
#file就是通过general_log_file=/mydata/data/general.log 等方式定义的，
#而输出位置定义为表时查看日志的内容：mysql.general_log表
 
##二进制日志设置
#默认不开启二进制日志
log_bin = OFF
#log-bin = /data/mysqldata/3307/binlog/mysql-bin 设置二进制路径时，如果没有生命log_bin=OFF，会开启日志
#二进制日志缓冲大小
#我们知道InnoDB存储引擎是支持事务的，实现事务需要依赖于日志技术，为了性能，日志编码采用二进制格式。那么，我们如何记日志呢？有日志的时候，就直接写磁盘？
#可是磁盘的效率是很低的，如果你用过Nginx，，一般Nginx输出access log都是要缓冲输出的。因此，记录二进制日志的时候，我们是否也需要考虑Cache呢？
#答案是肯定的，但是Cache不是直接持久化，于是面临安全性的问题——因为系统宕机时，Cache中可能有残余的数据没来得及写入磁盘。因此，Cache要权衡，要恰到好处：
#既减少磁盘I/O，满足性能要求；又保证Cache无残留，及时持久化，满足安全要求。
binlog_cache_size = 16M
 
 
##慢查询，开发调式阶段才需要开启慢日志功能。上线后关闭
slow_query_log = OFF
#慢日志文件路径
slow_query_log_file = /data/mysql/logs/slow_query.log
#该值是ON，则会记录所有没有利用索引来进行查询的语句，前提是slow_query_log 的值也是ON
log_queries_not_using_indexes = ON
#记录管理语句
log-slow-admin-statements
#如果运行的SQL语句没有使用索引，
#则mysql数据库同样会将这条SQL语句记录到慢查询日志文件中。调试时候使用
#log-queries-not-using-indexes
#设定每分钟记录到日志的未使用索引的语句数目，超过这个数目后只记录语句数量和花费的总时间
#log_throttle_queries_not_using_indexes = 60
 
#MySQL能够记录执行时间超过参数 long_query_time 设置值的SQL语句，默认是不记录的。超过这个时间的sql语句会被记录到慢日志文件中
long_query_time = 2
 
##错误日志：记录启动，运行，停止mysql时出现的信息
log-error = /data/mysql/logs/error.log
 
##一般查询日志,记录建立的客户端连接用户的所有操作，增上改查等，
#不是为了调式数据库，建议不要开启，0关闭，1开启
general_log = OFF
general_log_file = /data/mysql/logs/general.log
 
#log-long-format 扩展方式记录有关事件
#它是记录激活的更新日志、二进制更新日志、和慢查询日志的大量信息。例如，所有查询的用户名和时间戳将记录下来
#log-short-format,相反，记录少量的信息
 
 
 
############################
######数据库存储引擎########
############################
 
#默认使用InnoDB存储引擎
default_storage_engine = InnoDB
 
############################
######innoDB setting########
############################
 
#控制打开.ibd文件的数量。
#如果未启用innodb_file_per_table，则默认值为300
#否则取决于300和innodb_open_files中的较大值
innodb_file_per_table = 1
innodb_open_files = 350
#表定义缓存(数据字典)数量400-2000,默认为400 + (table_open_cache / 2)，小网站可以设置为最低
table_definition_cache = 400
#InnoDB 用来高速缓冲数据和索引内存缓冲大小。更大的设置可以使访问数据时减少磁盘 I/O。
innodb_buffer_pool_size = 64M
 
#单独指定数据文件的路径与大小
#默认会在datadir目录下创建ibdata1，表空间tablespace
#如果想为innodb tablespace指定不同目录下的文件，必须指定innodb_data_home_dir，home目录
innodb_data_file_path = ibdata1:32M:autoextend
#对于多核的CPU机器，可以修改innodb_read_io_threads和innodb_write_io_threads来增加IO线程，来充分利用多核的性能。默认4
#innodb_write_io_threads = 4
#innodb_read_io_threads = 4
 
#并发线程数的限制值，表示默认0情况下不限制线程并发执行的数量
innodb_thread_concurrency = 0
#开始碎片回收线程。这个应该能让碎片回收得更及时而且不影响其他线程的操作，
#默认值1表示innodb的purge操作被分离到purge线程中，master thread不再做purge操作。
#innodb_purge_threads = 1
 
#配置MySql日志何时写入硬盘的参数，默认为1
#0：log buffer将每秒一次地写入log file中，并且log file的flush(刷到磁盘)操作同时进行。该模式下在事务提交的时候，不会主动触发写入磁盘的操作。
#1：每次事务提交时MySQL都会把log buffer的数据写入log file，并且flush(刷到磁盘)中去
#2：每次事务提交时mysql都会把log buffer的数据写入log file，但是flush(刷到磁盘)操作并不会同时进行。该模式下，MySQL会每秒执行一次 flush(刷到磁盘)操作
#通常设置为 1，意味着在事务提交前日志已被写入磁盘， 事务可以运行更长以及服务崩溃后的修复能力。
innodb_flush_log_at_trx_commit = 1
 
#InnoDB 将日志写入日志磁盘文件前的缓冲大小。理想值为 1M 至 8M。大的日志缓冲允许事务运行时不需要将日志保存入磁盘而只到事务被提交(commit)。
#因此，如果有大的事务处理，设置大的日志缓冲可以减少磁盘I/O。
innodb_log_buffer_size = 2M
#日志组中的每个日志文件的大小(单位 MB)。如果 n 是日志组中日志文件的数目，那么理想的数值为 1M 至下面设置的缓冲池(buffer pool)大小的 1/n。较大的值，
#可以减少刷新缓冲池的次数，从而减少磁盘 I/O。但是大的日志文件意味着在崩溃时需要更长的时间来恢复数据。
innodb_log_file_size = 128M
#指定有三个日志组
innodb_log_files_in_group = 3
#innodb_max_dirty_pages_pct作用：控制Innodb的脏页在缓冲中在那个百分比之下，值在范围1-100,默认为90.这个参数的另一个用处：
#当Innodb的内存分配过大，致使swap占用严重时，可以适当的减小调整这个值，使达到swap空间释放出来。建义：这个值最大在90%，最小在15%。
#太大，缓存中每次更新需要致换数据页太多，太小，放的数据页太小，更新操作太慢。
innodb_max_dirty_pages_pct = 75
#在回滚(rooled back)之前，InnoDB 事务将等待超时的时间(单位 秒)
innodb_lock_wait_timeout = 120
 
#Innodb Plugin引擎开始引入多种格式的行存储机制，目前支持：Antelope、Barracuda两种。其中Barracuda兼容Antelope格式。
#innodb_file_format = Barracuda
#限制Innodb能打开的表的数量
#innodb_open_files = 65536
 
 
 
#分布式事务
#innodb_support_xa = FALSE
 
#innodb_buffer_pool_size 一致 可以开启多个内存缓冲池，把需要缓冲的数据hash到不同的缓冲池中，这样可以并行的内存读写。
#innodb_buffer_pool_instances = 4
#这个参数据控制Innodb checkpoint时的IO能力
#innodb_io_capacity = 500
#作用：使每个Innodb的表，有自已独立的表空间。如删除文件后可以回收那部分空间。
#分配原则：只有使用不使用。但ＤＢ还需要有一个公共的表空间。
#innodb_file_per_table = 1
 
#当更新/插入的非聚集索引的数据所对应的页不在内存中时（对非聚集索引的更新操作通常会带来随机IO），会将其放到一个insert buffer中，
#当随后页面被读到内存中时，会将这些变化的记录merge到页中。当服务器比较空闲时，后台线程也会做merge操作
#innodb_change_buffering = inserts
#该值影响每秒刷新脏页的操作，开启此配置后，刷新脏页会通过判断产生重做日志的速度来判断最合适的刷新脏页的数量；
#innodb_adaptive_flushing = 1
 
#数据库事务隔离级别 ，读取提交内容
#transaction-isolation = READ-COMMITTED
 
#innodb_flush_method这个参数控制着innodb数据文件及redo log的打开、刷写模式
#InnoDB使用O_DIRECT模式打开数据文件，用fsync()函数去更新日志和数据文件。
#innodb_flush_method = O_DIRECT
#默认设置值为1.设置为0：表示Innodb使用自带的内存分配程序；设置为1：表示InnoDB使用操作系统的内存分配程序　　　　　
#innodb_use_sys_malloc = 1
 
############################
######myisam setting########
############################
bulk_insert_buffer_size = 8M
myisam_sort_buffer_size = 8M
# MySQL重建索引时所允许的最大临时文件的大小
myisam_max_sort_file_size = 10G
myisam_repair_threads = 1
#忽略表名大小写
lower_case_table_names=1
 
#数据库全量备份
[mysqldump]
#强制mysqldump从服务器一次一行地检索表中的行
quick
#可接收数据包大小
max_allowed_packet = 16M
 
#在mysqld服务器不使用的情况下修复表或在崩溃状态下恢复表
[myisamchk]
key_buffer_size = 8M
sort_buffer_size = 8M
read_buffer = 4M
write_buffer = 4M
```

