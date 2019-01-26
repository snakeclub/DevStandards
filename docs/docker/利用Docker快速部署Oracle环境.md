# 利用Docker快速部署Oracle环境

1、 启动docker：sudo systemctl start docker

 

2、 搜索docker资源中的oracle镜像：docker search oracle

```
NAME                                DESCRIPTION                                     STARS               OFFICIAL            AUTOMATED
oraclelinux                         Oracle Linux is an open-source operating s...   391                 [OK]                
frolvlad/alpine-oraclejdk8          The smallest Docker image with OracleJDK 8...   264                                     [OK
alexeiled/docker-oracle-xe-11g      This is a working (hopefully) Oracle XE 11...   219                                     [OK]
sath89/oracle-12c                   Oracle Standard Edition 12c Release 1 with...   201                                     [OK]
sath89/oracle-xe-11g                Oracle xe 11g with database files mount su...   126                                     [OK]
isuper/java-oracle                  This repository contains all java releases...   55                                      [OK
jaspeen/oracle-11g                  Docker image for Oracle 11g database            52                                      [OK]
oracle/glassfish                    GlassFish Java EE Application Server on Or...   28                                      [OK]
oracle/openjdk                      Docker images containing OpenJDK Oracle Linux   25                                      [OK]
ingensi/oracle-jdk                  Official Oracle JDK installed on centos.        21                                      [OK]
airdock/oracle-jdk                  Docker Image for Oracle Java SDK (8 and 7)...   21                                      [OK]
cogniteev/oracle-java               Oracle JDK 6, 7, 8, and 9 based on Ubuntu ...   19                                      [OK]
n3ziniuka5/ubuntu-oracle-jdk        Ubuntu with Oracle JDK. Check tags for ver...   14                                      [OK]
oracle/nosql                        Oracle NoSQL on a Docker Image with Oracle...   13                                      [OK]
wnameless/oracle-xe-11g             Dockerfile of Oracle Database Express Edit...   13                                      [OK]
collinestes/docker-node-oracle      A container with Node.js/Oracle instant cl...   9                                       [OK
sgrio/java-oracle                   Docker images of Java 7/8 provided by Orac...   7                                       [OK]
openweb/oracle-tomcat               A fork off of Official tomcat image with O...   7                                       [OK]
andreptb/oracle-java                Debian Jessie based image with Oracle JDK ...   7                                       [OK]
flurdy/oracle-java7                 Base image containing Oracle's Java 7 JDK       4                                       [OK]
davidcaste/debian-oracle-java       Oracle Java 8 (and 7) over Debian Jessie        3                                       [OK]
teradatalabs/centos6-java8-oracle   Docker image of CentOS 6 with Oracle JDK 8...   3                                      
publicisworldwide/oracle-core       This is the core image based on Oracle Lin...   1                                       [OK]
sigma/nimbus-lock-oracle                                                            0                                       [OK]
spansari/nodejs-oracledb            nodejs with oracledb installed globally on...   0  

 
```

 

3、 这里选择获取12c版本，下载镜像：docker pull sath89/oracle-12c

```
Using default tag: latest
latest: Pulling from sath89/oracle-12c
863735b9fd15: Pull complete 
4fbaa2f403df: Pull complete 
faadd00cf98e: Downloading [=======>                                          ] 394.8 MB/2.768 GB
829e2e754405: Download complete 
```

 

4、 检查镜像是否已完成下载：docker images

```
REPOSITORY TAG IMAGE ID CREATED SIZE
docker.io/sath89/oracle-12c latest b8bf52883bc7 5 weeks ago 5.692 GB
```

 

5、 创建持久化数据文件的映射磁盘：

```
mkdir /opt/oracle
```

 

6、 启动Oracle容器：

```
docker run -d -p 8080:8080 -p 1521:1521 -v /opt/oracle:/u01/app/oracle sath89/oracle-12c
```

 

7、 检查容器启动日志：

```
docker logs -f 2e978dc1b73d69478d990dcd0d77304c07c0a3dfd18d0fb08a4bfe62b496cf0f
提示：
Database not initialized. Initializing database.
Starting tnslsnr
Copying database files
1% complete
2% complete
4% complete
DBCA Operation failed.
Look at the log file "/u01/app/oracle/cfgtoollogs/dbca/xe/xe.log" for further details.

```

查看实际问题：cat /opt/oracle/cfgtoollogs/dbca/xe/xe.log

```
The specified shared pool size or SGA size "292MB" does not meet the recommended minimum size requirement "331MB". This will make database creation fail. Do you want to continue?

Unique database identifier check passed.

/u01/app/oracle/ has enough space. Required space is 6140 MB , available space is 10659 MB.
File Validations Successful.
Copying database files
DBCA_PROGRESS : 1%
DBCA_PROGRESS : 2%
**ORA-00821: Specified value of sga_target 292M is too small, needs to be at least 364M**
ORA-01078: failure in processing system parameters
DBCA_PROGRESS : 4%
ORA-01034: ORACLE not available
ORA-01034: ORACLE not available
DBCA_PROGRESS : DBCA Operation failed.
```



8、 由于虚拟机仅设置了1G内存，怀疑是内存不足的问题，关闭虚拟机增加到2G内存后重启服务器，然后清除历史数据后重新执行操作：

```
cd /opt/oracle
rm -rf *
docker ps -a
docker rm xxxxx（需要删除的容器）

[root@CentOS7 ~]# sudo systemctl start docker

[root@CentOS7 ~]# docker run -d -p 8080:8080 -p 1521:1521 -v /opt/oracle:/u01/app/oracle sath89/oracle-12c
c1b48ca5e21fc730d165da69dc6a39bad001b42ae82d8307f5e20c22a2e89907

[root@CentOS7 ~]# docker logs -f c1b48ca5e21fc730d165da69dc6a39bad001b42ae82d8307f5e20c22a2e89907
Database not initialized. Initializing database.
Starting tnslsnr
Copying database files
1% complete
3% complete
11% complete
18% complete
26% complete
37% complete
Creating and starting Oracle instance
40% complete
45% complete
50% complete
55% complete
56% complete
60% complete
62% complete
Completing Database Creation
66% complete
70% complete
73% complete
85% complete
96% complete
100% complete
Look at the log file "/u01/app/oracle/cfgtoollogs/dbca/xe/xe.log" for further details.
Configuring Apex console
Database initialized. Please visit http://#containeer:8080/em http://#containeer:8080/apex for extra configuration if needed
Starting web management console

PL/SQL procedure successfully completed.
 
Starting import from '/docker-entrypoint-initdb.d':
found file /docker-entrypoint-initdb.d//docker-entrypoint-initdb.d/*

[IMPORT] /entrypoint.sh: ignoring /docker-entrypoint-initdb.d/*

Import finished

Database ready to use. Enjoy! ;)
```

 

9、 没有错误，查看容器是否在执行：docker ps

```
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                                            NAMES
c1b48ca5e21f        sath89/oracle-12c   "/entrypoint.sh "        11 minutes ago      Up 11 minutes       0.0.0.0:1521->1521/tcp, 0.0.0.0:8080->8080/tcp   brave_morse
```

 

10、            进入oracle容器中：docker exec -it c1b48ca5e21f /bin/bash

在容器中执行以下命令验证Oracle：

```
root@c1b48ca5e21f:/# su oracle

oracle@c1b48ca5e21f:/$ $ORACLE_HOME/bin/sqlplus / as sysdba   
SQL*Plus: Release 12.1.0.2.0 Production on Sun Nov 12 15:19:54 2017

Copyright (c) 1982, 2014, Oracle.  All rights reserved.

Connected to:
Oracle Database 12c Standard Edition Release 12.1.0.2.0 - 64bit Production
SQL>
```

 

11、            建立一张表用于检测持久化

```
SQL> create table tb_test(name varchar2(10));
Table created.

SQL> select * from tab where tname ='TB_TEST';
TNAME
\--------------------------------------------------------------------------------
TABTYPE  CLUSTERID
------- ----------
TB_TEST
TABLE
```

 

12、            重新启动docker

```
[root@CentOS7 pfile]# docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                                            NAMES
c1b48ca5e21f        sath89/oracle-12c   "/entrypoint.sh "        33 minutes ago      Up 33 minutes       0.0.0.0:1521->1521/tcp, 0.0.0.0:8080->8080/tcp   brave_morse
ce157a901e27        registry            "/entrypoint.sh /e..."   36 hours ago        Up 34 minutes       0.0.0.0:5000->5000/tcp                           elastic_brattain

[root@CentOS7 pfile]# docker stop c1b48ca5e21f
c1b48ca5e21f

[root@CentOS7 pfile]# docker start c1b48ca5e21f
c1b48ca5e21f
```

 

13、            此时可以远程访问Oracle数据库，数据库信息如下：

Oracle 使用的实例名，用户名，密码如下

\

```
---------------------------------------------
hostname: localhost
port: 1521
sid: xe
username: system
password: oracle
\---------------------------------------------
```

 

14、            创建一个测试用户：

```
docker exec -it c1b48ca5e21f /bin/bash

root@c1b48ca5e21f:/# su oracle

oracle@c1b48ca5e21f:/$ $ORACLE_HOME/bin/sqlplus / as sysdba
create user test identified by test123;

grant dba to test;
```

 

15、            通过主机远程连接数据库：

```
sqlplus test/test123@192.168.220.105:1521/xe
```

 

注：如果主机访问不了虚拟机，先在主机上ping和telnet，很有可能是VMware的网络自身问题，通过在网络连接中设置VMnet1、VMnet8、本地连接这3个网卡的共享属性可以解决。

 

以下为镜像作者的使用说明，供参考：

# Oracle Standard Edition 12c Release 1

[![https://badge.imagelayers.io/sath89/oracle-12c:latest.svg](file:///C:\Users\Administrator\AppData\Local\Temp\msohtmlclip1\01\clip_image001.png)](https://imagelayers.io/?images=sath89/oracle-12c:latest)

Oracle Standard Edition 12c Release 1 on Ubuntu
 This **Dockerfile** is a [trusted build](https://registry.hub.docker.com/u/sath89/oracle-12c/) of [Docker Registry](https://registry.hub.docker.com/).

[![https://asciinema.org/a/45878.png](file:///C:\Users\Administrator\AppData\Local\Temp\msohtmlclip1\01\clip_image001.png)](https://asciinema.org/a/45878)

### Installation

```
docker pull sath89/oracle-12c
```

Run with 8080 and 1521 ports opened:

```
docker run -d -p 8080:8080 -p 1521:1521 sath89/oracle-12c
```

Run with manual database initialization:

```
docker run -d -p 8080:8080 -p 1521:1521 -p 6800:6800 -e MANUAL_DBCA=true -e VNC_PASSWORD=passwd sath89/oracle-12c
#Default VNC_PASSWORD=oracle
#Open in Browser http://localhost:6800/vnc_auto.html
```

Run with data on host and reuse it:

```
docker run -d -p 8080:8080 -p 1521:1521 -v /my/oracle/data:/u01/app/oracle sath89/oracle-12c
```

Run with Custom DBCA_TOTAL_MEMORY (in Mb):

```
docker run -d -p 8080:8080 -p 1521:1521 -v /my/oracle/data:/u01/app/oracle -e DBCA_TOTAL_MEMORY=1024 sath89/oracle-12c
```

Connect database with following setting:

```
hostname: localhost
port: 1521
sid: xe
service name: xe.oracle.docker
username: system
password: oracle
```

To connect using sqlplus:

<pre>

sqlplus system/oracle@//localhost:1521/xe.oracle.docker

</pre>

Password for SYS & SYSTEM:

```
oracle
```

Connect to Oracle Application Express web management console with following settings:

```
http://localhost:8080/apex
```

```
workspace: INTERNAL
```

```
user: ADMIN
```

```
password: 0Racle$
```

Apex upgrade up to v 5.*

```
docker run -it --rm --volumes-from ${DB_CONTAINER_NAME} --link ${DB_CONTAINER_NAME}:oracle-database -e PASS=YourSYSPASS sath89/apex install
```

Details could be found here: <https://github.com/MaksymBilenko/docker-oracle-apex>

Connect to Oracle Enterprise Management console with following settings:

```
http://localhost:8080/em
```

```
user: sys
```

```
password: oracle
```

```
connect as sysdba: true
```

By Default web management console is enabled. To disable add env variable:

```
docker run -d -e WEB_CONSOLE=false -p 1521:1521 -v /my/oracle/data:/u01/app/oracle sath89/oracle-12c
```

```
#You can Enable/Disable it on any time
```

Start with additional init scripts or dumps:

```
docker run -d -p 1521:1521 -v /my/oracle/data:/u01/app/oracle -v /my/oracle/init/SCRIPTSorSQL:/docker-entrypoint-initdb.d sath89/oracle-12c
```

By default Import from `docker-entrypoint-initdb.d` is enabled only if you are initializing database (1st run).

To customize dump import use `IMPDP_OPTIONS` env variable like `-e IMPDP_OPTION="REMAP_TABLESPACE=FOO:BAR"`
 To run import at any case add `-e IMPORT_FROM_VOLUME=true`

**In case of using DMP imports dump file should be named like ${IMPORT_SCHEME_NAME}.dmp**

**User credentials for imports are ${IMPORT_SCHEME_NAME}/${IMPORT_SCHEME_NAME}**

If you have an issue with database init like DBCA operation failed, please reffer to this [issue](https://github.com/MaksymBilenko/docker-oracle-12c/issues/16)

**TODO LIST**

- Web management      console HTTPS port
- Add functionality      to run custom scripts on startup, for example User creation
- Add Parameter that      would setup processes amount for database (Currently by default      processes=300)
- Spike with      clustering support
- Spike with DB      migration from 11g

**In case of any issues please post it** [**here**](https://github.com/MaksymBilenko/docker-oracle-12c/issues)**.**

 