# 搭建并使用Docker私有仓库 -- 由浅入深学Docker系列(2)

## 一、资源准备

Docker私有仓库服务器：CentOS7  双网卡：192.168.186.103（NAT，可连接互联网）\92.168.220.103（主机模式，供Docker客户端访问）  已安装Docker

Docker客户端：CentOS7  双网卡：192.168.186.102（主机模式，只可访问内网）已安装Docker

 

## 二、通过可连接外网的服务器下载安装包（例如专用的YUM服务器）

1、安装yum的downloadonly插件：

```
yum install yum-plugin-downloadonly
```

2、安装yum-utils等依赖包（参考docker官网安装CE的步骤）

```
sudo yum install -y yum-utils \
  device-mapper-persistent-data \
  lvm2
```

3、设置Docker资源仓库地址

```
sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
```

4、通过downloadonly属性下载安装包，注意如果存在已安装了包的情况，使用reinstall，否则使用install：

```
yum reinstall --downloadonly --downloaddir=/root/dockerRpm/ yum-plugin-downloadonly

yum reinstall --downloadonly --downloaddir=/root/dockerRpm/ yum-utils device-mapper-persistent-data lvm2

yum install --downloadonly --downloaddir=/root/dockerRpm/ docker-ce
```

5、到/root/dockerRpm/检查相应的安装包是否已下载

 

## 三、在离线服务器上安装Docker（Docker私有仓库服务器和Docker客户端都要按照）

1、 将CentOS-7-x86_64-Everything-1708.iso放到光驱上（虚拟机加载），用于安装一些依赖包；

2、 挂载光驱

```
mkdir –p /mnt/cdrom
mount /dev/cdrom/ /mnt/cdrom
```

3、 编辑yum源配置

```
cd /etc/yum.repos.d/
vi CentOS-Media.repo
```

在baseurl上增加一行：file:///mnt/cdrom/

编辑完后的文件内容如下：

```
[c7-media]
name=CentOS-$releasever - Media
baseurl=file:///media/CentOS/
        file:///media/cdrom/
        file:///media/cdrecorder/
        file:///mnt/cdrom/
gpgcheck=1
enabled=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7
```

4、 安装perl验证yum源是否正确

```
yum --disablerepo=\* --enablerepo=c7-media install perl
```

5、 将下载好的安装包传到离线服务器上，目录为/root/dockerRpm/

6、 执行安装命令

```
cd /root/dockerRpm/

sudo yum --disablerepo=\* --enablerepo=c7-media localinstall -y yum-utils-1.1.31-42.el7.noarch.rpm

sudo yum --disablerepo=\* --enablerepo=c7-media localinstall -y device-mapper-persistent-data-0.7.0-0.1.rc6.el7.x86_64.rpm

sudo yum --disablerepo=\* --enablerepo=c7-media localinstall –y lvm2-2.02.171-8.el7.x86_64.rpm

sudo yum --disablerepo=\* --enablerepo=c7-media localinstall –y docker-ce-17.09.0.ce-1.el7.centos.x86_64.rpm
```

注：执行上述命令时会有依赖包的提示，按照提示安装对应的依赖包来解决问题

例如：

```
错误：软件包：docker-ce-17.09.0.ce-1.el7.centos.x86_64 (/docker-ce-17.09.0.ce-1.el7.centos.x86_64)
          需要：container-selinux >= 2.9
```

解决方法：

```
sudo yum --disablerepo=\* --enablerepo=c7-media localinstall –y container-selinux-2.21-2.gitba103ac.el7.noarch.rpm
```

 

7、 验证docker的安装

```
sudo systemctl start docker
sudo docker run hello-world
```

不过由于没有联网，因此执行镜像会有以下提示，但可以说明docker已安装成功：

```
Unable to find image 'hello-world:latest' locally

docker: Error response from daemon: Get https://registry-1.docker.io/v2/: dial tcp: lookup registry-1.docker.io on 192.168.220.2:53: read udp 192.168.220.102:45817->192.168.220.2:53: i/o timeout.
See 'docker run --help'.
```

 

## 四、搭建Docker私有仓库（Docker私有仓库服务器）

1、 确保该服务器能连外网；

2、 在服务器上建立镜像存储目录：mkdir /opt/docker-registry

3、 启动docker：sudo systemctl start docker

4、 下载registry镜像：sudo docker pull registry:2

5、 增加对https的配置支持，创建daemon.json文件并写入参数：

```
vi /etc/docker/daemon.json

{ "insecure-registries":["192.168.220.103:5000"] }
```

6、 下载完之后通过该镜像启动一个容器，指定镜像存储位置：

```
sudo docker run -d \
  -p 5000:5000 \
  --restart=always \
  --name registry \
  -v /opt/docker-registry:/var/lib/registry \
  registry:2
```

参数说明如下：

-v /opt/docker-registry:/var/lib/registry：默认情况下，会将仓库存放于容器内的/var/lib/registry目录下，指定本地目录挂载到容器

-p 5000:5000 ：端口映射

--restart=always ： 在容器退出时总是重启容器,主要应用在生产环境

--privileged=true ：在CentOS7中的安全模块selinux把权限禁掉了，参数给容器加特权，不加上传镜像会报权限错误OSError: [Errno 13] Permission denied: ‘/tmp/registry/repositories/liibrary’)或者（Received unexpected HTTP status: 500 Internal Server Error）错误

 

7、 查看docker是否已启动：sudo docker ps

```
[root@CentOS7 opt]# sudo docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED              STATUS              PORTS                    NAMES
fbf5500360cb        registry            "/entrypoint.sh /e..."   About a minute ago   Up About a minute   0.0.0.0:5000->5000/tcp   suspicious_roentgen
```

8、 本地验证私有仓库

从互联网下载镜像：

```
sudo docker pull hello-world
```

修改镜像的标记名：

```
sudo docker tag hello-world 192.168.220.103:5000/hello-world
```

上传到服务器：

```
sudo docker push 192.168.220.103:5000/hello-world
```

检查镜像是否已上传：

```
[root@CentOS7 /]# curl http://192.168.220.103:5000/v2/_catalog
{"repositories":["hello-world"]}
```

检查镜像版本：

```
[root@CentOS7 /]# curl http://192.168.220.103:5000/v2/hello-world/tags/list
{"name":"hello-world","tags":["latest"]}
```

重启docker，验证仓库内容是否持久化：

```
sudo systemctl restart docker
curl http://192.168.220.103:5000/v2/_catalog
curl http://192.168.220.103:5000/v2/hello-world/tags/list
```

 

## 五、局域网访问Docker私有仓库（Docker客户端）

1、 增加对https的配置支持，创建daemon.json文件并写入参数：

```
vi /etc/docker/daemon.json
{ "insecure-registries":["192.168.220.103:5000"] }
```

2、 启动或重启docker：sudo systemctl start docker

3、 检索docker私有仓库的镜像清单

```
curl http://192.168.220.103:5000/v2/_catalog
curl http://192.168.220.103:5000/v2/hello-world/tags/list
```

4、 查找本地镜像清单：docker images

5、 删除本地镜像：docker rmi 192.168.220.103:5000/hello-world

如果提示镜像被使用，通过“docker ps -a”查找镜像关联的容器，“docker rm 容器ID”删除容器后，再进行镜像的删除。

6、 拉取docker：docker pull 192.168.220.103:5000/hello-world

7、 启动docker：docker run 192.168.220.103:5000/hello-world

8、 上传镜像：sudo docker push 192.168.220.103:5000/hello-world