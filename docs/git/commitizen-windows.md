# Commitizen在Windows的安装使用手册

​	可以使用典型的git工作流程或通过使用CLI向导**Commitizen**来添加提交说明消息格式，让使用人员参考并生成符合Angular规范的提交说明。



## Commitizen安装部署（Windows）

[参考：Windows安装Git cz (commitizen)]: https://blog.csdn.net/u013456843/article/details/79403000

### 安装NVM For Windows

1. 下载nvm安装包：进入https://github.com/coreybutler/nvm-windows/releases下载nvm-setup.zip安装包。（参考下载包：nvm-setup1.1.6-windows.zip）；

2. 执行setup.exe，按默认安装即可；

3. 进入nvm安装目录：C:\Users\hi.li\AppData\Roaming\nvm，用管理员身份运行install.cmd，直接回车进行设置；

4. 编辑settings.txt文件，，在后面追加镜像配置(下载更快)：

   node_mirror: http://npm.taobao.org/mirrors/node/ 

   npm_mirror: https://npm.taobao.org/mirrors/npm/

5. 打开一个windows的cmd窗口，执行以下命令安装node.js：nvm install v8.11.3

6. 在cmd窗口执行：nvm use v8.11.3

7. 装完node.js，应该就是自带npm的，下面的安装npm步骤可以不执行：

   - 在cmd窗口执行（安装路径可指定其他路径，用于安装npm）：npm config set prefix "C:\Users\hi.li\AppData\Roaming\nvm\npm"
   - 在cmd窗口执行：npm install npm -g

8. 配置环境变量，变量名：NODE_PATH ；变量值： C:\Users\hi.li\AppData\Roaming\nvm\npm\node_modules



### 切换npm的安装源

如果执行npm的安装时下载不了或比较慢，可以将数据源切换为淘宝源：

临时使用淘宝源：

```
npm --registry https://registry.npm.taobao.org install node-red-contrib-composer@latest 
```

全局配置切换到淘宝源：

```
npm config set registry https://registry.npm.taobao.org 
```

全局配置切换到官方源：

```
npm config set registry http://www.npmjs.org 
```

检测是否切换到了淘宝源：

```
npm info underscore
```

```
输出信息里有registry.npm.taobao.org等字样，说明切换成功
tarball: 'http://registry.npm.taobao.org/underscore/download/underscore-1.8.3.tgz' },
```



### 离线安装npm包的方法

见：[npm用法及离线安装方法](npm用法及离线安装方法.md)



### 安装commitizen、conventional-changelog、standard-version

1. 在cmd窗口执行：npm install -g commitizen
2. 在cmd窗口执行：npm install -g conventional-changelog-cli
3. 在cmd窗口执行：npm install -g cz-conventional-changelog
4. 在cmd窗口执行，注意~应替换为用户目录（例如：C:\Users\hi.li\，可在命令行查看：echo %HOMEPATH%，还有最简单的方法是在git bash里输入~然后回车看，或者在git bash里执行这个命令）：echo '{ "path": "cz-conventional-changelog" }' > ~/.czrc
5. 配置环境变量，在系统环境变量的path上增加npm的安装目录：C:\Users\hi.li\AppData\Roaming\nvm\npm
6. 配置环境变量，在系统环境变量的path上增加npm的包安装目录：C:\Users\hi.li\AppData\Roaming\nvm\npm\node_modules
7. 在cmd窗口执行：npm i -g standard-version



## Commitizen的使用手册

### 项目配置

1. 在项目目录建一个空的package.json文件，然后执行：npm init --yes
2. 修改package.json文件，在根节点上增加以下配置项（注意路径为安装npm的路径）：

```
"config": {
    "commitizen": {
      "path": "cz-conventional-changelog"
    }
  }
```

3. 修改package.json文件，在根节点上增加以下配置项：

```
"scripts": {
    "release": "standard-version"
  }
```



### 使用git cz代替gitcommit

​	在commit时使用git cz代替git commit（注意不能在git bash中执行，而是要在powershell或cmd中执行），步骤如下：
**（1）选择提交的类型type（用光标移动）：**

```
C:\Users\hi.li\Desktop\GitTest\test>git cz
   cz-cli@2.10.1, cz-conventional-changelog@2.1.0

Line 1 will be cropped at 100 characters. All other lines will be wrapped after 100 characters.

? Select the type of change that you're committing: (Use arrow keys)

> feat:     A new feature
> fix:      A bug fix
> docs:     Documentation only changes
> style:    Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
> refactor: A code change that neither fixes a bug nor adds a feature
> perf:     A code change that improves performance
> test:     Adding missing tests or correcting existing tests
> (Move up and down to reveal more choices)
```

**（2）输入影响范围scope：**

```
? What is the scope of this change (e.g. component or file name)? (press enter to skip)
```

**（3）输入简要描述subject：**
```
? Write a short, imperative tense description of the change:
```

**（4）输入详细描述body：**
```
? Provide a longer description of the change: (press enter to skip)
```

**（5）选择是否有不兼容改造点breaking，如果有输入不兼容改造点描述：**
```
? Are there any breaking changes? Yes
? Describe the breaking changes:
```

**（6）选择是否有问题解决issues，如果有输入解决的问题清单（注意问题清单的格式该工具并未直接支持，需要自行录入完整描述内容，例如Closes #1333）：**
```
? Does this change affect any open issues? (y/N)
```



### git cz多行输入的设置

git cz默认控制每行字符长度100，当输入字符串长度超过100会自动切断，但由于不可控，建议涉及多行输入的情况自行通过其他编辑器编辑好内容后，再粘贴到git cz中，自己用"\\n"在想要换行的地方进行换行处理即可（在输入内容中不要带真正的换行符）。

1. 由于以上处理方法还是可能存在100个字节被换行的问题，可以修改Commitizen的代码，将最大长度改成5000，以避免自动换行，修改方法如下：
2. 找到commitizen的安装目录，如果是非全局的，目录在项目目录下的`node_modules\commitizen\`中；如果是全局安装，则应该在npm目录下，例如`C:\Users\hi.li\AppData\Roaming\nvm\npm\node_modules\commitizen\`
3. 在commitizen安装目录下载到engine.js文件，目录应该是在`commitizen\node_modules\cz-conventional-changelog\`(注意`C:\Users\hi.li\AppData\Roaming\nvm\npm\node_modules`里的cz-conventional-changelog中也会有，也应要修改)
4. 修改engine.js文件中的这行代码：

```
var maxLineWidth = 100;

修改为：

var maxLineWidth = 5000;
```



### 生成changelog

​	如果需要单独生成变更信息（CHANGELOG.md），通过以下命令将新的变更信息追加到原来的CHANGELOG.md上：

```
conventional-changelog -p angular -i CHANGELOG.md -s
```

​	如果需要全量生成CHANGELOG.md信息，执行以下命令：

```
conventional-changelog -p angular -i CHANGELOG.md -s -r o 
```



### 自动打包

​	通过standard-version可以自动根据所提交的信息进行产品版本号（例如V0.0.1）的更新（tag），如果存在breaking，则大版本号+1；如果存在提交类型type为feat，则中版本号+1；如果提交类型type为fix，则小版本号+1。

​	相关打包命令如下：

- 第一次打包版本：npm run release -- --first-release

- 基于原版本打包新版本：npm run release
- 基于原版本预打包（Vx.x.x-1）：npm run release -- --prerelease
- 预打包带指定版本号：npm run release -- --prerelease alpha
- 指定版本号打包：npm run release -- --release-as 1.1.0
- 测试打包但实际不输出：npm run release -- --dry-run
- 获取帮助：npm run release -- --help
- 打包版本后推送到服务器端：git push --follow-tags origin master

