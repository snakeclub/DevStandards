# 使用xwiki部署知识库

## 环境及部署包准备

操作系统：CentOS7

数据库：MySQL5.7 （本示例数据库与xwiki服务装在同一台服务器上）

xwiki安装包：https://www.xwiki.org/xwiki/bin/view/Download/DownloadVersion/?projectVersion=10.11.1

- WAR Package for Servlet Container
- XIP Addon Package for Offline Installs

JDK1.8（jdk-8u202-linux-x64.tar.gz）：https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html

Tomcat：http://mirror.bit.edu.cn/apache/tomcat/tomcat-8/v8.5.37/bin/apache-tomcat-8.5.37.tar.gz

Nginx：[http://nginx.org/download](http://nginx.org/download/nginx-1.5.7.tar.gz)

MySQL JDBC Driver Jar：<http://repo1.maven.org/maven2/mysql/mysql-connector-java/5.1.34/mysql-connector-java-5.1.34.jar>



### 安装 JDK1.8（本文采用官网压缩包方式安装）

1、检查是否原来有安装

```
rpm -qa | grep java
rpm -qa | grep jdk
rpm -qa | grep gcj
```

如果已有安装，可以使用rpm -qa | grep java | xargs rpm -e --nodeps 批量卸载所有带有Java的文件；或rpm -e --nodeps jdk1.8指定卸载

2、上传安装包jdk-8u202-linux-x64.tar.gz到服务器上的/usr/java目录下（使用SecureFXP）

3、解压缩包：tar -zxvf jdk-8u202-linux-x64.tar.gz

4、删除压缩包： rm jdk-8u202-linux-x64.tar.gz

5、配置环境变量，编辑文件：vi /etc/profile

在结尾添加以下信息：

```
# set java environment
export JAVA_HOME=/usr/java/jdk1.8.0_202
export JRE_HOME=$JAVA_HOME/jre
export PATH=$PATH:$JAVA_HOME/bin:$JRE_HOME/bin
export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar:$JRE_HOME/lib
```

6、使配置文件生效：source /etc/profile

7、检查是否可正常使用：java -version



### 安装libreoffice

1、检查是否已安装过libreoffice

```
yum list installed | grep libreoffice
```

2、使用yum安装

https://blog.csdn.net/sheqianweilong/article/details/84475315

```
yum install libreoffice libreoffice-headless
```

注：如果是离线，要找一台可以联网的服务器下载相应的安装包，步骤如下：

```
（1）服务器要安装yum下载包
yum install yum-plugin-downloadonly
sudo yum install -y yum-utils \
  device-mapper-persistent-data \
  lvm2
（2）通过downloadonly属性下载安装包，注意如果存在已安装了包的情况，使用reinstall，否则使用install：
例如：
yum reinstall --downloadonly --downloaddir=/root/dockerRpm/ yum-plugin-downloadonly
yum reinstall --downloadonly --downloaddir=/root/dockerRpm/ yum-utils device-mapper-persistent-data lvm2
yum install --downloadonly --downloaddir=/root/dockerRpm/ docker-ce
本次安装的汇总命令如下：
yum install --downloadonly --downloaddir=/root/xwikirpm/ libreoffice libreoffice-headless
yum install --downloadonly --downloaddir=/root/xwikirpm/ autocorr-zh.noarch libreoffice-langpack-zh-Hans.x86_64 libreoffice-langpack-zh-Hant.x86_64
yum install --downloadonly --downloaddir=/root/xwikirpm/ gcc-c++ pcre pcre-devel zlib zlib-devel openssl openssl-devel
（3）将安装包的目录复制到要安装的服务器上，例如目录为：/root/centos7-libreoffice-yum-offline
（4）进入目录一次性安装所有包
cd /root/centos7-libreoffice-yum-offline
yum localinstall *.rpm
```



### 安装中文字体库

1、检查是否已安装过中文字体库

```
yum list installed | grep autocorr-zh.noarch
yum list installed | grep libreoffice-langpack-zh-Hans.x86_64
yum list installed | grep libreoffice-langpack-zh-Hant.x86_64
```

2、使用yum安装

```
yum install autocorr-zh.noarch libreoffice-langpack-zh-Hans.x86_64 libreoffice-langpack-zh-Hant.x86_64
```



### 安装Tomcat

1、将apache-tomcat-8.5.37.tar.gz复制到/usr/tomcat/目录下

2、解压缩

```
cd /usr/tomcat
tar -zxvf apache-tomcat-8.5.37.tar.gz
```

3、删除压缩包：rm apache-tomcat-8.5.37.tar.gz

4、编辑服务器配置：vi /usr/tomcat/apache-tomcat-8.5.37/conf/server.xml

找到Connector配置项，修改为以下样式：

```
    <Connector port="8080" protocol="HTTP/1.1"
               connectionTimeout="20000"
               redirectPort="8443" 
               URIEncoding="UTF-8"
               compression="on"
               compressionMinSize="2048"
               compressableMimeType="text/html,text/xml,text/css,text/javascript,application/x-javascript" />
```

5、配置防火墙，放开访问端口

```
firewall-cmd --zone=public --add-port=8080/tcp --permanent
firewall-cmd --reload
```

6、在/usr/tomcat/apache-tomcat-8.5.37/bin下建setenv.sh，用于启动tomcat时设置环境变量，文件内容如下：

```
# 设置catalina.sh启动时的环境变量，如果需要修改java配置也可以在这里处理
export CATALINA_HOME=/usr/tomcat/apache-tomcat-8.5.37
export CATALINA_BASE=/usr/tomcat/apache-tomcat-8.5.37
# 设置Tomcat的PID文件
CATALINA_PID="$CATALINA_BASE/tomcat.pid"
# 添加JVM选项
JAVA_OPTS="-server -Xms256m -Xmx512m -Xss1024K -XX:PermSize=128m -XX:MaxPermSize=256m"

```

7、将setenv.sh设置为可执行

```
chmod +x setenv.sh
```

8、设置开机自启动

在/usr/lib/systemd/system路径下添加tomcat.service文件，内容如下：

```
[Unit]
Description=Tomcat
After=syslog.target network.target remote-fs.target nss-lookup.target

[Service]
Type=forking
PIDFile=/usr/tomcat/apache-tomcat-8.5.37/tomcat.pid
ExecStart=/usr/tomcat/apache-tomcat-8.5.37/bin/startup.sh
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s QUIT $MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target

##[unit]配置了服务的描述，规定了在network启动之后执行，
##[service]配置服务的pid，服务的启动，停止，重启
##[install]配置了使用用户
```

将Tomcat加入服务管理

```
systemctl enable tomcat.service
systemctl disable tomcat.service
systemctl start tomcat.service
systemctl stop tomcat.service
systemctl restart tomcat.service
systemctl status tomcat
```

9、在浏览器中打开http://192.168.186.104:8080/进行验证



### 安装Nginx

1、安装依赖

```
1.安装gcc gcc是用来编译下载下来的nginx源码
  yum install gcc-c++

2、安装pcre和pcre-devel
    PCRE(Perl Compatible Regular Expressions) 是一个Perl库，包括 perl 兼容的正则表达式库。
	nginx 的 http 模块使用 pcre 来解析正则表达式，pcre-devel 是使用 pcre 开发的一个二次开发库。
    yum install -y pcre pcre-devel

3、安装zlib zlib提供了很多压缩和解方式，nginx需要zlib对http进行gzip
   yum install -y zlib zlib-devel

4、安装openssl openssl是一个安全套接字层密码库，nginx要支持https，需要使用openssl
    yum install -y openssl openssl-devel
```

2、将nginx-1.14.2.tar.gz复制到/usr/nginx目录

3、解压缩

```
cd /usr/nginx
tar -zxvf nginx-1.14.2.tar.gz
```

4、删除压缩包：rm tar -zxvf nginx-1.14.2.tar.gz

5、进入nginx安装包的目录，编译

```
./configure --prefix=/usr --sbin-path=/usr/sbin/nginx --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --pid-path=/var/run/nginx/nginx.pid --lock-path=/var/lock/nginx.lock --user=nginx --group=nginx --with-http_ssl_module --with-http_flv_module --with-http_gzip_static_module --http-log-path=/var/log/nginx/access.log --http-client-body-temp-path=/var/tem/nginx/client --http-proxy-temp-path=/var/tem/nginx/proxy --http-fastcgi-temp-path=/var/tem/nginx/fcgi --with-http_stub_status_module
```

6、安装

```
make && make install
```

7、默认为80端口服务，编辑配置文件进行代理转发：vi /etc/nginx/nginx.conf

```
server {
    listen       80;
    server_name  mydomain.com;

    # Normally root should not be accessed, however, root should not serve files that might compromise the security of your server. 
    root /var/www/html;

    location / {
        # All "root" requests will have /xwiki appended AND redirected to mydomain.com
        rewrite ^ $scheme://$server_name/xwiki$request_uri? permanent;
    }

    location ^~ /xwiki {
       # If path starts with /xwiki - then redirect to backend: XWiki application in Tomcat
       # Read more about proxy_pass: http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_pass
       proxy_pass http://localhost:8080;
       proxy_set_header        X-Real-IP $remote_addr;
       proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
       proxy_set_header        Host $http_host;
       proxy_set_header        X-Forwarded-Proto $scheme;
    }
}
```

8、执行启动验证安装：nginx -c /etc/nginx/nginx.conf

如果出现：nginx: [emerg] getpwnam("nginx") failed，执行：

```
useradd -s /sbin/nologin -M nginx
id nginx
```

如果出现 [emerg] mkdir() "/var/temp/nginx/client" failed (2: No such file or directory) 错误 执行：

```
sudo mkdir -p /var/tem/nginx/client
```

如果重启服务器后出现open() "/var/run/nginx/nginx.pid" failed (2: No such file or directory)，按如下方法解决：

```
vi /etc/nginx/nginx.conf
修改
#pid        logs/nginx.pid;
为
pid        /usr/sbin/nginxlogs/nginx.pid;

然后新增目录
sudo mkdir -p /usr/sbin/nginxlogs
```

8、配置防火墙，放开访问端口

```
firewall-cmd --zone=public --add-port=80/tcp --permanent
firewall-cmd --reload
```

9、设置开机自启动

在/usr/lib/systemd/system路径下添加nginx.service文件，内容如下：

```
[Unit]
Description=Nginx
After=syslog.target network.target remote-fs.target nss-lookup.target

[Service]
Type=forking
ExecStart=/usr/sbin/nginx -c /etc/nginx/nginx.conf
ExecReload=/usr/sbin/nginx -s reload
ExecStop=/usr/sbin/nginx -s quit
PrivateTmp=true

[Install]
WantedBy=multi-user.target

##[unit]配置了服务的描述，规定了在network启动之后执行，
##[service]配置服务的pid，服务的启动，停止，重启
##[install]配置了使用用户
```

将Nginx加入服务管理

```
systemctl enable nginx.service
systemctl disable nginx.service
systemctl start nginx.service
systemctl stop nginx.service
systemctl restart nginx.service
systemctl status nginx
```

9、在浏览器中打开http://192.168.186.104:80/进行验证



### 部署MySQL数据库

注：本章节默认数据库已完成安装及基本设置，所有操作在数据库服务器上执行；数据库建议使用支持事务处理的**InnoDB**引擎

查看数据库引擎的命令

```
show engines;
```

创建数据库并赋予访问权限

```
mysql -uroot -proot
create database xwiki default character set utf8 collate utf8_bin; 

# 设置允许简单密码
set global validate_password_policy=LOW;
set global validate_password_length=4;
SHOW VARIABLES LIKE 'validate_password%';

grant all privileges on xwiki.* to xwiki identified by 'xwiki';
flush privileges;
```



## 部署XWiki配置文件

1、进入tomcat目录建立应用目录

```
cd /usr/tomcat/apache-tomcat-8.5.37/webapps
mkdir xwiki
cd xwiki
```

2、将xwiki-platform-distribution-war-10.11.1.war放到该目录下，解压

```
unzip xwiki-platform-distribution-war-10.11.1.war
```

3、删除war包

```
rm xwiki-platform-distribution-war-10.11.1.war
```

4、将mysql-connector-java-5.1.34.jar放到/usr/tomcat/apache-tomcat-8.5.37/webapps/xwiki/WEB-INF/lib目录下

5、编辑数据库连接配置：vi /usr/tomcat/apache-tomcat-8.5.37/webapps/xwiki/WEB-INF/hibernate.cfg.xml，屏蔽掉Configuration for the default database的配置，打开 MySQL configuration 配置，参考配置如下：

```
    <property name="connection.url">jdbc:mysql://127.0.0.1:3360/xwiki?useSSL=false</property>
    <property name="connection.username">xwiki</property>
    <property name="connection.password">xwiki</property>
    <property name="connection.driver_class">com.mysql.jdbc.Driver</property>
    <property name="dialect">org.hibernate.dialect.MySQL5InnoDBDialect</property>
    <property name="dbcp.poolPreparedStatements">true</property>
    <property name="dbcp.maxOpenPreparedStatements">20</property>

    <property name="hibernate.connection.charSet">UTF-8</property>
    <property name="hibernate.connection.useUnicode">true</property>
    <property name="hibernate.connection.characterEncoding">utf8</property>

    <mapping resource="xwiki.hbm.xml"/>
    <mapping resource="feeds.hbm.xml"/>
    <mapping resource="activitystream.hbm.xml"/>
    <mapping resource="instance.hbm.xml"/>
    <mapping resource="notification-filter-preferences.hbm.xml"/>
    <mapping resource="mailsender.hbm.xml"/>
```

6、编辑openoffice配置：vi /usr/tomcat/apache-tomcat-8.5.37/webapps/xwiki/WEB-INF/xwiki.properties，启启用并修改以下两个配置：

```
openoffice.autoStart=true
openoffice.homePath=/usr/lib64/libreoffice/
```

7、字符集编码修改

vi /usr/tomcat/apache-tomcat-8.5.37/webapps/xwiki/WEB-INF/web.xml，应该不用修改，检查项

```
  <filter>
    <filter-name>Set Character Encoding</filter-name>
    <filter-class>org.xwiki.container.servlet.filters.internal.SetCharacterEncodingFilter</filter-class>
    <!-- The encoding to use. This must be the same as the one in xwiki.cfg (hopefully only one
         encoding will be used later). -->
    <init-param>
      <param-name>encoding</param-name>
      <param-value>UTF-8</param-value>
    </init-param>
    <!-- Whether to ignore and override the encoding specified by the client, when this actually
         happens. For example, AJAX requests made through XmlHttpRequests specify UTF-8. When this
         is set to false, the custom encoding is used only when there wasn't any encoding specified
         by the client. -->
    <init-param>
      <param-name>ignore</param-name>
      <param-value>false</param-value>
    </init-param>
  </filter>
```

vi /usr/tomcat/apache-tomcat-8.5.37/webapps/xwiki/WEB-INF/xwiki.cfg，应该不用修改，检查项

```
xwiki.encoding=UTF-8
```

8、修改附件以文件方式保存（不保存在数据库）：vi /usr/tomcat/apache-tomcat-8.5.37/webapps/xwiki/WEB-INF/xwiki.cfg，放开并修改以下项：

```
xwiki.store.attachment.hint=file
xwiki.store.attachment.versioning.hint=file
xwiki.store.attachment.recyclebin.hint=file
```

修改附件存放位置：vi /usr/tomcat/apache-tomcat-8.5.37/webapps/xwiki/WEB-INF/xwiki.properties

```
environment.permanentDirectory=/usr/tomcat/xwikidata/
```

9、设置不连接远程扩展仓库（注意第一次如果这样设置了向导会找不到常用插件的安装，建议整合完成后再设置）：vi /usr/tomcat/apache-tomcat-8.5.37/webapps/xwiki/WEB-INF/xwiki.properties，启用并置空该配置

```
extension.repositories=
```

10、一些提高性能的配置

xwiki.cfg

```
# 设置为0不保留版本轨迹
xwiki.store.versioning=0
# 调整xwiki.cfg配置文件中的Document cache（文件缓存）
xwiki.store.cache.capacity=1000
```



## 第一次启动配置

重新启动Tomcat，然后通过浏览器打开http://192.168.186.104:8080/xwiki/ 会自动启动初始化向导，按提示进行配置：

**Step 1 - Admin user** 

配置管理员用户：admin/admin

**Step 2 - Favol** 

安装最常用的扩展插件集，需要联网，建议在这里安装标准Favol，这样整体风格会很完整；如果实在无法联网，则下载org.xwiki.platform_xwiki-platform-administration-ui-10.11.1.xar安装管理插件后再进行各个插件的维护。

其他步骤按提示执行即可。



## 清空所有配置重新启动初始化向导的方法

如果需要重置XWiki并重来，无需重新全部安装，按照以下的方式可以快速进行重新配置。

1、重建数据库

```
mysql -uroot -proot

drop database xwiki;
create database xwiki default character set utf8 collate utf8_bin; 

# 设置允许简单密码
set global validate_password_policy=LOW;
set global validate_password_length=4;
SHOW VARIABLES LIKE 'validate_password%';

grant all privileges on xwiki.* to xwiki identified by 'xwiki';
flush privileges;
```

2、清空xwiki.properties配置中environment.permanentDirectory参数指定路径的文件和运行文件：

```
sudo rm -fr /usr/tomcat/xwikidata/ /usr/tomcat/apache-tomcat-8.5.37/Catalina/localhost/xwiki/
```

3、重启tomcat

```
systemctl restart tomcat.service
```



## 企业知识库的配置





### 插件使用

#### PDF Macro 3.0

by: Guillaume Lerouge          Displays PDF attachments in wiki pages

使用方法：将附件上传到页面中，然后使用以下语句将附件展示出来

{{pdf filename="资格审查表094403001423.pdf" width="1000px" height="400px"/}}



#### Office Macro

自带扩展控件

https://extensions.xwiki.org/xwiki/bin/view/Extension/Office%20Macro

