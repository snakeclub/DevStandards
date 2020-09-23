# Anaconda安装使用手册

Anaconda [ˌænəˈkɑːndə] 是一个开源的数据科学工具管理平台，其包含了Conda、Python等180多个科学包及其依赖项。其中Conda  [ˈkɑːndə] 是一个开源的包、环境管理器，可以用于在同一个机器上安装不同版本的软件包及其依赖，并能够在不同的环境之间切换。通过Anaconda可以简化数据科学研究（包括人工智能）的环境准备工作，包含不同版本的环境切换、虚拟环境、包依赖等。

可以在以下官方地址下载对应操作系统和Python版本的安装包：https://www.anaconda.com/download/

# Windows安装手册

## 安装步骤

1、运行下载的图形安装包，例如：Anaconda3-2020.02-Windows-x86_64.exe，如无特殊说明则均选择默认配置即可。

2、选择当前用户使用还是全部用户（需要管理员权限），这里选择全部用户：

<img src="Anaconda%E5%AE%89%E8%A3%85%E4%BD%BF%E7%94%A8%E6%89%8B%E5%86%8C.assets/image-20200511131808508.png" alt="image-20200511131808508" style="zoom:50%;" />

3、选择安装路径，注意目标路径中**不能**含有**空格**，同时不能是“unicode”编码：

<img src="Anaconda%E5%AE%89%E8%A3%85%E4%BD%BF%E7%94%A8%E6%89%8B%E5%86%8C.assets/image-20200511131826049.png" alt="image-20200511131826049" style="zoom:50%;" />

3、高级安装选项，第一个选项是添加到PATH环境变量，但又可能会引发以前安装软件的问题；第二个是将Anaconda中的Python3.7作为系统的主版本，按默认选择即可：

<img src="Anaconda%E5%AE%89%E8%A3%85%E4%BD%BF%E7%94%A8%E6%89%8B%E5%86%8C.assets/image-20200511132034545.png" alt="image-20200511132034545" style="zoom:50%;" />

4、继续就是安装过程：

<img src="Anaconda%E5%AE%89%E8%A3%85%E4%BD%BF%E7%94%A8%E6%89%8B%E5%86%8C.assets/image-20200511132311305.png" alt="image-20200511132311305" style="zoom:50%;" />

5、安装完，勾选的这两个选项可以跳转到官网的教程：

<img src="Anaconda%E5%AE%89%E8%A3%85%E4%BD%BF%E7%94%A8%E6%89%8B%E5%86%8C.assets/image-20200511132405507.png" alt="image-20200511132405507" style="zoom:50%;" />

6、安装完成后，开始菜单又Anaconda3的菜单：

<img src="Anaconda%E5%AE%89%E8%A3%85%E4%BD%BF%E7%94%A8%E6%89%8B%E5%86%8C.assets/image-20200511132710272.png" alt="image-20200511132710272" style="zoom:50%;" />

## 安装后的验证

可以执行以下两个方法验证是否安装成功：

1、执行“开始 → Anaconda3（64-bit）→ 右键点击Anaconda Prompt → 以管理员身份运行”，在Anaconda Prompt中输入`conda list`，可以查看已经安装的包名和版本号。若结果可以正常显示，则说明安装成功。

2、若运行“Anaconda-Navigator”成功启动，则说明真正成功地安装了Anaconda；**如果未成功，请务必仔细检查以上安装步骤**。“Anaconda-Navigator”中已经包含“Jupyter Notebook”、“Jupyterlab”、“Qtconsole”和“Spyder”。

<img src="Anaconda%E5%AE%89%E8%A3%85%E4%BD%BF%E7%94%A8%E6%89%8B%E5%86%8C.assets/image-20200511133047720.png" alt="image-20200511133047720" style="zoom: 50%;" />



# Linux安装手册（ubuntu18版本示例）

1、前往官方下载页面(https://www.anaconda.com/download/)下载。有两个版本可供选择：Python 3.6 和 Python 2.7。

2、启动终端，在终端跳转至安装文件所在路径，输入命令`md5sum Anaconda3-5.0.1-Linux-x86_64.sh`或`sha256sum Anaconda3-5.0.1-Linux-x86_64.sh`

- 注意：将该步骤命令中的文件名替换为实际下载的文件名；
- 强烈建议：
  - 路径和文件名中不要出现空格或其他特殊字符。
  - 路径和文件名最好以英文命名，不要以中文或其他特殊字符命名。

3、在终端中输入：`bash Anaconda3-5.0.1-Linux-x86_64.sh`，或根据下载路径指定`bash ~/Downloads/Anaconda3-5.0.1-Linux-x86_64.sh`

- 注意：
  1. 首词bash也需要输入，无论是否用的Bash shell。
  2. 如果你的下载路径是自定义的，那么把该步骤路径中的`~/Downloads`替换成你自己的下载路径。
  3. 除非被要求使用root权限，否则均选择“Install Anaconda as a user”。

4、安装过程中，看到提示“In order to continue the installation process, please review the license agreement.”（“请浏览许可证协议以便继续安装。”），点击“Enter”查看“许可证协议”。

5、在“许可证协议”界面将屏幕滚动至底，输入“yes”表示同意许可证协议内容。然后进行下一步。

6、安装过程中，提示“Press Enter to accept the default install location, CTRL-C to cancel the installation or specify an alternate installation directory.”（“按回车键确认安装路径，按'CTRL-C'取消安装或者指定安装目录。”）如果接受默认安装路径，则会显示“PREFIX=/home/<user>/anaconda<2 or 3>”并且继续安装。安装过程大约需要几分钟的时间。

- 建议：直接接受默认安装路径。

7、安装器若提示“Do you wish the installer to prepend the Anaconda<2 or 3> install location to PATH in your /home/<user>/.bashrc ?”（“你希望安装器添加Anaconda安装路径在`/home//.bashrc`文件中吗？”），建议输入“yes”。

- 注意：
  1. 路径`/home//.bash_rc`中“<user>”即进入到家目录后你的目录名。
  2. 如果输入“no”，则需要手动添加路径，否则conda将无法正常运行。

8、当看到“Thank you for installing Anaconda<2 or 3>!”则说明已经成功完成安装。

9、关闭终端，然后再打开终端以使安装后的Anaconda启动。或者直接在终端中输入`source ~/.bashrc`也可完成启动。

10、验证安装结果。可选用以下任意一种方法：

- 在终端中输入命令`condal list`，如果Anaconda被成功安装，则会显示已经安装的包名和版本号。
- 在终端中输入`python`。这条命令将会启动Python交互界面，如果Anaconda被成功安装并且可以运行，则将会在Python版本号的右边显示“Anaconda custom (64-bit)”。退出Python交互界面则输入`exit()`或`quit()`即可。
- 在终端中输入`anaconda-navigator`。如果Anaconda被成功安装，则Anaconda Navigator将会被启动。



# 升级Conda

接下来均是以命令行模式进行介绍，Windows需打开“Anaconda Prompt”；macOS和Linux需打开“Terminal”（“终端”）进行操作。

**1、检查conda的版本**

```undefined
conda --version
```

终端上将会以`conda 版本号`的形式显示当前安装conda的版本号。

**2、更新conda至最新版本，并设置默认版本为最新版本**

```undefined
conda update conda
conda update -n base -c defaults conda
```

执行命令后，conda将会对版本进行比较并列出可以升级的版本。同时，也会告知用户其他相关包也会升级到相应版本。

当较新的版本可以用于升级时，终端会显示`Proceed ([y]/n)?`，此时输入`y`即可进行升级。

<img src="Anaconda%E5%AE%89%E8%A3%85%E4%BD%BF%E7%94%A8%E6%89%8B%E5%86%8C.assets/image-20200511140555137.png" alt="image-20200511140555137" style="zoom: 33%;" />

**3、查看conda帮助信息**

```bash
conda --help
```

或

```undefined
conda -h
```



# 升级pip

```
python -m pip install -i https://mirrors.aliyun.com/pypi/simple/ --upgrade pip
```



# Ubuntu多用户共享访问使用

如果使用的是root用户进行的按照，需要所有用户都使用Anacoda，可以按以下步骤进行处理（建议一开始安装到/usr/local目录下，但如果一开始安装到其他路径也可以处理）：

```
# 第一步使用root权限执行以下命令，假设安装至/home/ubuntu18/anaconda3
sudo groupadd anaconda # 创建anaconda组
sudo adduser <username> anaconda # 将需要的用户添加至anaconda组
sudo chgrp -R anaconda /home/ubuntu18/anaconda3 # 移交目录管理权
sudo chmod 770 -R /home/ubuntu18/anaconda3 # 设置读写权限
chmod -R g+s /home/ubuntu18/anaconda3 # 设置组继承


# 第二步，配置 /etc/profile 文件，在该文件最后加入这句话就可以了,然后执行 source /etc/profile
export PATH=/home/ubuntu18/anaconda3/bin:$PATH
```



# Anaconda使用手册

接下来均是以命令行模式进行介绍，Windows需打开“Anaconda Prompt”；macOS和Linux需打开“Terminal”（“终端”）进行操作。

## 虚拟环境管理

### 创建虚拟环境

```xml
conda create --name <env_name> <package_names>
或
conda create -n <env_name> <package_names>
```

- env_name为要创建的环境名，建议以英文命名，且不加空格，名称两边不加尖括号“<>”。
- package_names为要在环境中安装的包名，名称两边不加尖括号“<>”，可以在一个命令中传多个包名（用空格隔开）；可以在包名后面加“=version”指定要安装的包的版本，例如“python=3.5 numpy=1.0 pandas”；
- 默认情况下，新创建的环境将会被保存在`/Users/[name]/.conda/envs`目录下，其中[name]为操作系统用户名，可以在命令行提示中看到，例如 “C:\Users\74143\\.conda\envs\tensorflow” 。

示例：

```
# 创建名为ai的虚拟环境，使用默认的
conda create -n ai

# 指定python的版本，并同时安装numpy pandas两个包
conda create -n test python=3.5 numpy pandas
```



### 切换虚拟环境

 Linux 或 macOS

```bash
source activate <env_name>
```

Windows

```bash
activate <env_name>
```



### 退出虚拟环境

Linux 或 macOS

```bash
source deactivate
```

Windows

```undefined
deactivate
```



### 显示虚拟环境清单信息

```undefined
conda info --envs
```

或

```undefined
conda info -e
```

或

```cpp
conda env list
```

显示信息示例如下：

<img src="Anaconda%E5%AE%89%E8%A3%85%E4%BD%BF%E7%94%A8%E6%89%8B%E5%86%8C.assets/image-20200512115732697.png" alt="image-20200512115732697" style="zoom: 80%;" />



### 复制虚拟环境

```xml
conda create --name <new_env_name> --clone <copied_env_name>
```

- copied_env_name为被复制/克隆环境名。环境名两边不加尖括号“<>”。
- new_env_name即为复制之后新环境的名称。环境名两边不加尖括号“<>”。



### 删除虚拟环境

```
conda remove --name <env_name> --all
```



## 包管理

### 查找安装包

**精确查找**

```xml
conda search --full-name <package_full_name>
```

- `--full-name`为精确查找的参数。
- `package_full_name`是被查找包的**全名**。包名两边不加尖括号“<>”。

```
# 查找全名为“python”的包有哪些版本可供安装
conda search --full-name python
```

**模糊查找**

```
conda search <text>
```

- `text`是查找含有**此字段**的包名。此字段两边不加尖括号“<>”。

```
# 查找含有“py”字段的包，有哪些版本可供安装
conda search py
```



### 查看当前环境已安装包清单

```
conda list
```



### 命令行方式安装包

**在指定环境安装包**

```xml
conda install --name <env_name> <package_name>
```

- `env_name`是将包安装的指定环境名。环境名两边不加尖括号“<>”。
- `package_name`是要安装的包名。包名两边不加尖括号“<>”。

```
# 在名为“ai”的环境中安装pandas包
conda install --name ai pandas
```

**在当前环境安装包**

```
conda install <package_name>
```

**使用pip安装包**

当使用`conda install`无法进行安装时，可以使用pip进行安装。

```xml
pip install <package_name>
```

- <package_name>为指定安装包的名称。包名两边不加尖括号“<>”。

 注意：

1. pip只是包管理器，无法对环境进行管理。因此如果想在指定环境中使用pip进行安装包，则需要先切换到指定环境中，再使用pip命令安装包。
2. pip无法更新python，因为pip并不将python视为包。
3. pip可以安装一些conda无法安装的包；conda也可以安装一些pip无法安装的包。因此当使用一种命令无法安装包时，可以尝试用另一种命令。

### 从Anaconda.org安装包

当使用`conda install`无法进行安装时，可以考虑从Anaconda.org中获取安装包的命令，并进行安装。

在**当前环境**中安装来自于Anaconda.org的包时，需要通过输入要安装的包在Anaconda.org中的路径作为获取途径（channel）。查询路径的方式如下：

1. 在浏览器中输入：[http://anaconda.org](https://link.jianshu.com?t=http%3A%2F%2Fanaconda.org)，或直接点击[Anaconda.org](https://link.jianshu.com?t=http%3A%2F%2Fanaconda.org)

2. 在新页面“Anaconda Cloud”的上方搜索框中输入要安装的包名，然后点击右边“放大镜”标志。

   ![img](https:////upload-images.jianshu.io/upload_images/5101171-cd47636a24d4c531.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

3. 搜索结果中有数以千计的包可供选择，此时点击“Downloads”可根据下载量进行排序，最上面的为下载最多的包。（图中以搜索bottleneck包为例）

   ![img](https:////upload-images.jianshu.io/upload_images/5101171-3bbe1caef732a702.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

4. 选择满足需求的包或下载量最多的包，点击包名。

5. 复制“To install this package with conda run:”下方的命令，并粘贴在终端中执行。

   ![img](https:////upload-images.jianshu.io/upload_images/5101171-424cd0f31a4ffa9a.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

6. 完成安装。



### 卸载包

 **卸载指定环境中的包**

```xml
conda remove --name <env_name> <package_name>
```

**卸载当前环境中的包**

```csharp
conda remove <package_name>
```



### 更新包

**更新所有包**

```undefined
conda update --all
```

或

```undefined
conda upgrade --all
```

- 建议：在安装Anaconda之后执行上述命令更新Anaconda中的所有包至最新版本，便于使用。

**更新指定包**

```xml
conda update <package_name>
```

或

```xml
conda upgrade <package_name>
```

- 更新多个指定包，则包名以**空格**隔开，向后排列。如：`conda update pandas numpy matplotlib`即更新pandas、numpy、matplotlib包。



# VS Code接入Anaconda虚拟环境的设置

VS Code默认安装完成后接入的是机器本身的Python环境，但如果我们开发使用的是Conda所配置的虚拟环境，在VS Code检测的安装包就会不一致，实现不了代码的自动提示。因此需要修改VS Code的配置。

1、通过菜单打开配置页 “file => preferences => setting”；

2、搜索配置项 “python.pythonPath”；

3、把配置项的值从默认的 “python” 修改为虚拟环境的路径，例如 “C:\Users\74143\.conda\envs\tensorflow”。



每次使用 VSCode 打开 Python 文件，终端就会自动激活 Conda 环境，但这并不是我想要的，我只想关闭它，只需要在 VSCode 的settings.json中加入这一行配置即可：

```
"python.terminal.activateEnvironment": false
```

还有另一个方法直接设置Conda取消自动激活`base`，打开 Powershell：

```
conda config --set auto_activate_base false
```

