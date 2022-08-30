# MacOS-M1安装PgSQL

1、获取镜像

```
docker pull postgres
```

2、启动一个PgSQL容器

```
docker run -it --name mypgsql -e "POSTGRES_PASSWORD=123456" -e POSTGRES_USER=root -p 5432:5432 -d postgres
```

3、检查容器是否正常启动

```
docker ps -a | grep postgres
```

4、进入容器进行验证数据库

```
# 进入容器操作系统
docker exec -it mypgsql bash

# 登录数据库
psql -U 'root' -p 5432 -h '0.0.0.0'

# 查看数据库版本
select version();

# 创建数据库
create database test_db;

# 切换到数据库
\c test_db;

# 创建schema
create schema myschema;

# 创建表, schema在默认的public下 
CREATE TABLE COMPANY(
   ID INT PRIMARY KEY     NOT NULL,
   NAME           TEXT    NOT NULL,
   AGE            INT     NOT NULL,
   ADDRESS        CHAR(50),
   SALARY         REAL
);

# 创建表, schema在默认的myschema下 
CREATE TABLE myschema.COMPANY(
   ID INT PRIMARY KEY     NOT NULL,
   NAME           TEXT    NOT NULL,
   AGE            INT     NOT NULL,
   ADDRESS        CHAR(50),
   SALARY         REAL
);

# 查看数据库列表
select datname from pg_database order by datname;

# 查看表清单
select schemaname, tablename from pg_tables where schemaname in ('public', 'myschema');
```

注1：pgsql数据库中的database、schema、table关系为“database —> schema —> table“，可以数据库之间是相互独立的，schema可以理解为database下的表集合，不同数据库下可以有相同的schema名；同理，同一个数据库的不同schema下可以有相同的table名。

注2：可以使用DBeaver连接pgsql数据库



# MacOS-M1安装psycopg2

psycopg2是python连接pgsql数据库的库，直接使用pip安装会存在问题，可以按以下步骤安装：

1、安装依赖库

```
brew install openssl
brew install postgresql
```

注：如果出现类似Error: ca-certificates: no bottle available的报错，可以更新brew源解决，操作命令如下：

```
echo 'export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles' >> ~/.zshrc
source ~/.zshrc
brew update
```

2、安装psycopg2

```
pip3 install psycopg2
pip3 install psycopg2-binary
```

3、如果需要安装异步驱动，安装aiopg

```
pip3 install aiopg
```



# MacOS-M1安装psycopg 3

文档地址：https://www.psycopg.org/psycopg3/docs/index.html

```
brew install libpq5
pip install psycopg
```

