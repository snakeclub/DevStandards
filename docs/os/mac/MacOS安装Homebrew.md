# MacOS安装Homebrew

参考：https://zhuanlan.zhihu.com/p/341831809

## 安装 ARM 版 Homebrew

直接执行：

```bash
/bin/bash -c "$(curl -fsSL https://cdn.jsdelivr.net/gh/ineo6/homebrew-install/install.sh)"
```

然后还需设置环境变量，具体操作步骤如下，一定要仔细阅读。

PS: 终端类型根据执行命令`echo $SHELL`显示的结果：

- `/bin/bash` => `bash` => `.bash_profile`
- `/bin/zsh` => `zsh` => `.zprofile`

**如果遇到环境变量无效问题，建议回过头来查看终端类型，再做正确的设置。**

从`macOS Catalina`(10.15.x) 版开始，`Mac`使用`zsh`作为默认`Shell`，使用`.zprofile`，所以对应命令：

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

如果是`macOS Mojave` 及更低版本，并且没有自己配置过`zsh`，使用`.bash_profile`：

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.bash_profile
eval "$(/opt/homebrew/bin/brew shellenv)"
```



## 安装 X86 版 Homebrew

因为目前很多软件包没有支持`ARM`架构，我们也可以考虑使用`x86`版的`Homebrew`。

在命令前面添加`arch -x86_64`，就可以按X86模式执行该命令，比如：

```bash
arch -x86_64 /bin/bash -c "$(curl -fsSL https://cdn.jsdelivr.net/gh/ineo6/homebrew-install/install.sh)"
```

## 多版本共存

如果你同时安装了ARM和X86两个版本，那你需要设置别名，把命令区分开。

同样是`.zprofile`或者`.bash_profile`里面添加：

至于操作哪个文件，请参考前文关于终端类型的描述，下文如有类似文字，保持一样的操作。

```bash
alias abrew='arch -arm64 /opt/homebrew/bin/brew'
alias ibrew='arch -x86_64 /usr/local/bin/brew'
```

`abrew`、`ibrew`可以根据你的喜好自定义。

然后再执行`source ~/.zprofile`或`source ~/.bash_profile`命令更新文件。

## 设置镜像

**注意：本文中的安装脚本会设置中科大源镜像，如果你也想设置`cask`和`bottles`的镜像，请按下面注释部分选择执行代码。**

更详细的教程可以参考前面「mac下镜像飞速安装Homebrew教程」

执行时根据实际情况修改`"$(brew --repo)"`代码中的`brew`。

意思是如果你只是使用一个版本`Homebrew`，直接执行命令即可，如果你想多个版本共存或者使用了别名，就把`brew`关键字替换为别名名称，如前面的`abrew`、`ibrew`。

```bash
# brew
git -C "$(brew --repo)" remote set-url origin https://mirrors.ustc.edu.cn/brew.git

# core
git -C "$(brew --repo homebrew/core)" remote set-url origin https://mirrors.ustc.edu.cn/homebrew-core.git

# cask
git -C "$(brew --repo homebrew/cask)" remote set-url origin https://mirrors.ustc.edu.cn/homebrew-cask.git

# bottles for zsh 和下面2选1
echo 'export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles/bottles' >> ~/.zprofile
source ~/.zprofile

# bottles for bash 和上面2选1
echo 'export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles/bottles' >> ~/.bash_profile
source ~/.bash_profile
```

具体镜像设置参考 [mac下镜像飞速安装Homebrew教程](https://zhuanlan.zhihu.com/p/90508170) “设置镜像”一节。



## 卸载Homebrew

在命令行执行以下脚本：

```
/bin/bash -c "$(curl -fsSL https://cdn.jsdelivr.net/gh/ineo6/homebrew-install/uninstall.sh)"
```

