# npm用法及离线安装方法

转自cnblogs：[npm用法及离线安装方法](https://www.cnblogs.com/laozhbook/p/npm_help.html)

原作者：[laozhbook](http://www.cnblogs.com/laozhbook/)

### 基本的用法

查看某个模块的全部信息，或者可以查看单个信息

```
npm info name
npm info name version
npm info name homepage
```

install支持多种手段，包名，git路径，包括本地路径也可以

```
sudo npm install -global [package name]
npm install git://github.com/package/path.git
npm install git://github.com/package/path.git#0.1.0
npm install package_name@version
npm install path/to/somedir  //本地路径
```

前提是本地路径里面包含一个完整的包，或者文件里面有合格的package.json文件即可



查看装好了哪些包

```
npm list
npm -global list
```

### 配置文件基本用法

配置就是修改npmrc文件了。用命令行同样也是修改此文件。

npmrc存在三个位置，修改用户目录下的文件就更合适了。

~/.npmrc             （用户主目录，win系统在C:\Users\$用户名\.npmrc）

 

修改文件就不用说了，命令配置方法

```
npm config set key=value
npm config set proxy=http://127.0.0.1:8087
```

具体的用法和具体key value可以通过打开说明文档查看

```
npm help npm
```

配置项可以通过以下命令查看已经配置过的项

```
npm config list
npm config list -l
```

### 配置代理，全局目录，源

下面正式介绍对付国内网络的方法了

首先几个重要的配置项一一介绍

prefix   -- 全局安装的路径，也就是npm install -g 安装的模块在哪个位置。这个看个人喜好。我喜好将他设置到安装路径下面。

proxy -- 代理（http的代理是用这个），代理连外网的朋友这个就需要配置了。

https_proxy -- https代理

registry -- 类似linux的软件源，这个一定要修改的

```
npm config set prefix "c:\nodejs"
npm config set proxy=http://127.0.0.1:8087
npm config set https_proxy=http://127.0.0.1:8087
npm config set registry=http://registry.npmjs.org
```

registry=http://registry.npmjs.org 这句很重要，注意默认的源是https://registry.npmjs.org 是https的，反正我连默认的源是从来没成功过一次。
上例我把他修正为不加密http的就基本能正常了。

网络不行可以考虑一些国内的源试试，例如

```
npm config set registry "http://r.cnpmjs.org/"
```

### 离线安装

有许多环境下即便配置了代理，修改了源还是出现网络问题。常见的提示是shasum check failed。当然这不一定就是网络不行，但大部分情况下是网络连接不通畅导致的。

这种情况下可以手工下载并安装，其实也很简单。

首先找到想办法把你需要的包下载下来，这个可以多种办法了。或者从其他机器拷过来。

例如先npm info mysql 查看mysql这个包的信息，包信息里面会有软件主页或者代码仓库地址。一半在github上。（install因为要下载可能会失败，但是info指令信息少通常可以成功）。

例如node-mysql的地址在<https://github.com/felixge/node-mysql>

下载来之后解压到工程的node_modules目录下就是安装好了，就这么简单。

Project

　　---package.json

　　---index.js

　　---node_modules      // 解压到此目录就行了（每个包文件夹下面有package.json，index.js文件的。）

注意：你下载下来的源码包可能和模块名字不一样。要将改名成模块名再拷贝进node_modules 中去。例如将node-mysql文件夹改名成mysql。

 

包之间的依赖关系离线安装问题

上面方法安装的包不会包含依赖的包，不过依赖包同样用上面离线一个个安装的办法也可以。

例如mysql包就依赖bignumber.js , readable-stream , require-all 三个包。npm默认情况下安装的依赖包会是一层一层往下的。例如安装好mysql工程结构会是这样的

Project

　　---package.json

　　---index.js

　　---node_modules

　　　　　　---mysql

　　　　　　　　　　---node_modules

　　　　　　　　　　　　　　---bignumber.js

　　　　　　　　　　　　　　---readable-stream

　　　　　　　　　　　　　　---require-all

 

你同样只需要相同的操作将依赖的包放到相应的位置便可。这样包管理的结构虽然复杂但是依赖关系很清晰。但是这个规定不一定非要这样，你也可以将依赖包放到第一层的node_modules文件夹下。nodejs搜索模块路径会一层一层往上搜索。