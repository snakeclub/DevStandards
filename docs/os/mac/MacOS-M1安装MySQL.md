# MacOS-M1安装MySQL

1、获取镜像（只能获取最新版本，5.7没有arm版本的）

```
docker pull mysql/mysql-server
```

2、启动一个MySQL容器

```
docker run --name tf-mysql -e MYSQL_ROOT_PASSWORD=123456 -p 3306:3306 -d mysql/mysql-server
```

3、进入容器进行管理，修改登录密码及开启远程访问

```
# 进入容器操作系统
docker exec -it tf-mysql bash

# 登录mysql
mysql -u root -p

# 重置root密码
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '123456';

# 开启root的远程访问
create user 'root'@'%' identified by '123456';

# 给远程用户授权
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;

# 刷新权限
FLUSH PRIVILEGES;

# 查看所有数据库
SHOW DATABASES;

# 创建新数据库
create database if not exists dev_tf DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

```

4、用mysql客户端软件连接测试



# 修改MySQL容器配置

1、查看mysql的docker的内存占用，例如下面的例子内存占用达到388m(4.89%)

```
docker stats
CONTAINER ID   NAME       CPU %     MEM USAGE / LIMIT     MEM %     NET I/O           BLOCK I/O       PIDS
53b2d3d5cd91   tf-mysql   0.62%     388.6MiB / 7.765GiB   4.89%     16.5kB / 55.6kB   250kB / 257MB   41
```

2、修改配置文件

```
# 将配置文件从docker复制到当前目录
docker cp tf-mysql:/etc/my.cnf ./

# 编辑
vi my.cnf
# 在[mysqld]下新增或修改以下参数
performance_schema_max_table_instances=400  
table_definition_cache=400    # 缓存
performance_schema=off    # ⽤于监控MySQL server在⼀个较低级别的运⾏过程中的资源消耗、资源东西
table_open_cache=64    # 打开表的缓存
innodb_buffer_pool_chunk_size=64M    # InnoDB缓冲池⼤⼩调整操作的块⼤⼩
innodb_buffer_pool_size=64M    # InnoDB 存储引擎的表数据和索引数据的最⼤内存缓冲区⼤⼩

# 将修改后的配置覆盖回容器中
docker cp ./my.cnf tf-mysql:/etc/my.cnf 

# 检查容器中的文件是否已修改
docker exec -it tf-mysql bash
cat /etc/my.cnf
```

4、重启容器

```
docker stop tf-mysql
docker start tf-mysql
```

5、重新检查docker的内存占用，已经降到115mb

```
docker stats
CONTAINER ID   NAME       CPU %     MEM USAGE / LIMIT     MEM %     NET I/O     BLOCK I/O         PIDS
53b2d3d5cd91   tf-mysql   1.06%     115.7MiB / 7.765GiB   1.46%     876B / 0B   65.5kB / 12.8MB   38
```



# 批量执行sql文件的方法

```
# 复制sql文件到指定容器中
docker cp ./ tf-mysql:/tmp/sql/

# 进入容器
docker exec -it tf-mysql bash

# 进入目录执行sql文件
cd /tmp/sql/
for SQL in *.sql; do mysql -uroot -p"123456" dev_tf < $SQL; done
```

ERROR 1146 (42S02) at line 134: Table 'dev_tf.tf_cpt_send_messagedtl' doesn't exist