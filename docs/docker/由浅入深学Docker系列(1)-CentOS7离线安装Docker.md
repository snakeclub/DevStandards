# CentOS7离线安装Docker -- 由浅入深学Docker系列(1)

## 一、整体思路

在可以连接外网的机器（未安装过docker，同时跟局域网要安装docker的机器系统版本一致）通过yum命令将rpm以及相关的依赖下载完成

将下载完成的rpm包，拷贝到局域网机器上面

构建本地yum源

使用yum install docker安装，安装完成

 

## 二、通过可连接外网的服务器下载安装包

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

 

## 三、在离线服务器上安装Docker

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

