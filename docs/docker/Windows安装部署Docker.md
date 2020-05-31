# Windows安装部署Docker

## 开启Hyper-V（家庭版）

(1) 新建hyperv.cmd文件，内容如下：

```
pushd "%~dp0" 

dir /b %SystemRoot%\servicing\Packages\*Hyper-V*.mum >hyper-v.txt 

for /f %%i in ('findstr /i . hyper-v.txt 2^>nul') do dism /online /norestart /add-package:"%SystemRoot%\servicing\Packages\%%i"

del hyper-v.txt

Dism /online /enable-feature /featurename:Microsoft-Hyper-V-All /LimitAccess /ALL
```

2、以管理员身份运行cmd文件，如果需要重启请重启。

3、打开控制面板（开始 ->  Windows 系统 -> 控制面板）,  点击 ”程序  ->  启用或关闭Windows功能“，检查下图中Hyper-V是否已经勾选，如未勾选，请勾选

![img](Windows%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2Docker.assets/2134179-ac729a571cfa1663.webp)



## 伪装成win10专业版

(1) 以管理员身份打开cmd，方法如下：在C:\Windows\System32目录下找到cmd.exe，右键选择以管理员身份运行

2、cmd中执行

```
REG ADD "HKEY_LOCAL_MACHINE\software\Microsoft\Windows NT\CurrentVersion" /v EditionId /T REG_EXPAND_SZ /d Professional /F
```



## 安装WSL

WSL(Ubuntu)将Ubuntu和Win10无缝连接起来，让开发人员可以不使用虚拟机，就轻松地在同一个系统中使用win10和Ubuntu，你可以用它代替Cywin32和babun.

1、在win10的设置中打开更新和安全，打开 ”开发人员选项“，选择 ”开发人员模式“

<img src="Windows%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2Docker.assets/image-20200518185229642.png" alt="image-20200518185229642" style="zoom: 33%;" />

2、打开控制面板（开始 ->  Windows 系统 -> 控制面板）,  点击 ”程序  ->  启用或关闭Windows功能“，勾选上”适用于Linux的WIndows子系统“：

<img src="Windows%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2Docker.assets/image-20200518185858420.png" alt="image-20200518185858420" style="zoom: 50%;" />

3、重启计算机后，打开应用商店搜索下载ubuntu18.04，进行安装；

4、安装完成后，会自动打开ubuntu，要求创建一个新用户并设置密码（这里可以考虑跟桌面登陆用户一致，比如我设置的用户是lhj）;

注：安装后ubuntu的文件系统路径在：`C:\Users\74143\AppData\Local\Packages\CanonicalGroupLimited.Ubuntu18.04onWindows_79rhkp1fndgsc\LocalState\rootfs`



## 配置WSL

**1、切换用户为root**

执行以下命令 "sudo -s" ，输入当前用户密码后进行切换。



**2、更换apt源**

```
cd /etc/apt/
sudo cp sources.list sources.list.bak && sudo vim sources.list
```

删除所有内容，使用以下内容进行替换：

```
deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
```

执行以下命令进行升级

```
sudo apt update
sudo apt upgrade
```



## 安装Docker in Windows10

下载地址：https://docs.docker.com/docker-for-windows/install/

1、下载后进行安装，采用默认选项即可；

2、启动后进行配置，勾选上“Expose daemon on localhost:2375 without TLS”，点击“Apply & Restart”：

![image-20200518202028584](Windows%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2Docker.assets/image-20200518202028584.png)



## 安装Docker CE

官方安装参考文档：https://docs.docker.com/engine/install/ubuntu/

**1、安装步骤**

以下使用root用户执行

```
# 删除老的docker版本
$ sudo apt-get remove docker docker-engine docker.io containerd runc

# 更新apt索引，并安装下载及安装docker的工具
$ sudo apt-get update
$ sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
    
# Add Docker’s official GPG key
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Verify that you now have the key with the fingerprint
$ sudo apt-key fingerprint 0EBFCD88
pub   rsa4096 2017-02-22 [SCEA]
      9DC8 5822 9FC7 DD38 854A  E2D8 8D81 803C 0EBF CD88
uid           [ unknown] Docker Release (CE deb) <docker@docker.com>
sub   rsa4096 2017-02-22 [S]

# 设置仓库
$ sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

# 执行安装最新版本的docker
$ sudo apt-get update
$ sudo apt-get install docker-ce docker-ce-cli containerd.io
```



注：如果安装制定版本的docker，可以通过以下命令执行安装

```
# 查看可选版本
$ apt-cache madison docker-ce
  docker-ce | 5:18.09.1~3-0~ubuntu-xenial | https://download.docker.com/linux/ubuntu  xenial/stable amd64 Packages
  docker-ce | 5:18.09.0~3-0~ubuntu-xenial | https://download.docker.com/linux/ubuntu  xenial/stable amd64 Packages
  docker-ce | 18.06.1~ce~3-0~ubuntu       | https://download.docker.com/linux/ubuntu  xenial/stable amd64 Packages
  docker-ce | 18.06.0~ce~3-0~ubuntu       | https://download.docker.com/linux/ubuntu  xenial/stable amd64 Packages
  ...

# 安装选定的版本
$ sudo apt-get install docker-ce=<VERSION_STRING> docker-ce-cli=<VERSION_STRING> containerd.io
```



**2、设置一般用户运行权限及安装Docker Compose**

以下切换为一般用户（lhj）执行

```
#

# 授于当前用户以root权限运行Docker CLI
sudo usermod -aG docker $USER

# 安装python3以及pip
$ sudo apt-get install -y python3 python3-pip

# 安装Docker Compose
$ sudo pip3 install --user -i https://pypi.tuna.tsinghua.edu.cn/simple/ docker-compose

# 连接Docker daemon
echo "export DOCKER_HOST=tcp://localhost:2375" >> ~/.bashrc && source ~/.bashrc
```

注：运行docker-compose如果出现问题，提示“The command 'docker-compose' could not be found in this WSL 1 distro”，需要升级Windows到预览版18917之后的版本（打开cmd可以看到版本号），然后安装WSL 2版本，参考文档：https://docs.microsoft.com/en-us/windows/wsl/install-win10



**3、执行以下命令验证docker是否已安装成功**

```
$ docker info
$ docker run hello-world
```



## Docker 与 Win10共享文件夹

WSL Ubuntu18里，默认映射Win C盘为`/mnt/c/`，可以需要手动改为`/c/`

```
sudo mkdir /c
sudo mount --bind /mnt/c /c
```

