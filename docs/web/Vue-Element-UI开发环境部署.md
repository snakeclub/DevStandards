# Vue-Element-UI开发环境部署

版本：Vue 3.x

## 安装依赖软件及编辑器

**1、安装Node.js（v16或更高版本）及npm**

请自行查找安装教程，安装完成后可以通过以下命令查看版本：

```
// 查看node版本
> node -v
v17.0.1

// 查看npm版本
> npm -v
8.1.2
```

**注：请进来安装LST版本的Node.js，如过出现以下的webpack错误，可尝试更换Node的其他版本：Error: error:0308010C:digital envelope routines::unsupported at new Hash (node:internal/crypto/hash:67:19)**

**2、安装Vs Code**

安装完成后，可以安装以下插件提升开发效率：

Debugger for Chrome ：通过Chrome执行调试

vue ：支持vue代码高亮显示

volar : vue 3 语言支持

Vue 3 Snippets ： 支持vue代码提示

open in browser ：直接通过浏览器打开文件

JavaScript (ES6) code snippets ：javascript 代码提示

HTML Snippets ：html代码提示

HTML CSS Support ：在html中的css代码提示

Auto Close Tag ： 自动填入关闭标签

Auto Rename Tag ：修改标签时自动修改结束标签

element-ui-helper ：element-ui帮助提示

Element UI Snippets ：element-ui代码提示

Beautify ：代码格式美化

**3、Beautify插件配置**

（1）在项目根目录下创建 .jsbeautifyrc 配置文件，配置Beautify插件，内容如下：

```
{
  "brace_style": "none,preserve-inline",
  "indent_size": 2,
  "indent_char": " ",
  "jslint_happy": true,
  "unformatted": [""],
  "end_with_newline": true,
  "css": {
    "indent_size": 2
  }
}
```

（2）在代码中可以按 F1 调出任务，然后选择 Beautify file 美化文件的代码格式（注：也可以设置快捷键 "ctrl + b" 的方式执行美化）；

（3）如果代码中存eslint提示的错误，例如： “Delete \`CR\` (ESLINT prettier)” ，可以通过命令行进入项目目录，然后执行 npm run lint --fix 命令修复文件格式。

## Vue3.x与Vue2.x项目的一些重要限制区别

1、element-ui并不支持Vue3.x，需改用element-plus；

## 创建Vue3项目

1、输入命令创建项目

    > cd 要创建项目的目录
    > npm init vue@latest
    Vue.js - The Progressive JavaScript Framework
    
    ? Project name: › vue-project
    ✔ Project name: … vue_src
    ✔ Add TypeScript? … No / Yes (选No)
    ✔ Add JSX Support? … No / Yes （选Yes）
    ✔ Add Vue Router for Single Page Application development? … No / Yes （选Yes）
    ✔ Add Pinia for state management? … No / Yes  (选No)
    ✔ Add Vitest for Unit Testing? … No / Yes （选Yes）
    ✔ Add Cypress for End-to-End testing? … No / Yes  （选Yes）
    ✔ Add ESLint for code quality? … No / Yes  （选Yes）
    ✔ Add Prettier for code formatting? … No / Yes  （选Yes）

2、构建工具会在当前目录下创建对应的项目和相关文件，可以按以下步骤安装依赖并启动开发服务器

    > cd <your-project-name>
    > npm install
    > npm run dev

1、输入命令创建项目

```
> cd 要创建项目的目录
> vue create test-project
Vue CLI v4.5.13
? Please pick a preset: (Use arrow keys)
❯ Default ([Vue 2] babel, eslint) 
  Default (Vue 3) ([Vue 3] babel, eslint) 
  Manually select features        <-- 我们选择自定义创建
```

2、通过上下按钮和空格键选择特性，先按以下选项选取：

```
? Check the features needed for your project: 
 ◉ Choose Vue version   // 选择创建Vue的版本
 ◉ Babel  // 转码器，可以将ES6代码转为ES5代码，从而在现有环境执行。 
 ◯ TypeScript  // TypeScript是一个JavaScript（后缀.js）的超集（后缀.ts）包含并扩展了 JavaScript 的语法，需要被编译输出为 JavaScript在浏览器运行
 ◯ Progressive Web App (PWA) Support  // 谷歌提出的渐进式Web桌面应用程序
 ◉ Router  // vue-router（vue路由）
 ◉ Vuex  // vuex（vue的状态管理模式）
 ◉ CSS Pre-processors  // CSS 预处理器（如：less、sass）
 ◉ Linter / Formatter  // 代码风格检查和格式化（如：ESlint）
❯◉ Unit Testing  // 单元测试（unit tests）
 ◯ E2E Testing  // e2e（end to end） 测试
```

3、选择vue版本

```
? Choose a version of Vue.js that you want to start the project with 
  2.x 
❯ 3.x     <-- 我们选择3.x
```

4、是否使用`history`路由模式(不带#号的)，输入 n

```
Use history mode for router? (Requires proper server setup for index fallback in production) (Y/n) y
```

5、选择css 模式，我们选择 `node-sass`，css 预处理器，node-sass是自动编译实时的，dart-sass需要保存后才会生效（注：如果是mac M1芯片需要使用dart-sass）

```
? Pick a CSS pre-processor (PostCSS, Autoprefixer and CSS Modules are supported by default): 
  Sass/SCSS (with dart-sass) 
❯ Sass/SCSS (with node-sass) 
  Less 
  Stylus 
```

6、代码验证模式，我们选择最后一个 `ESLint + Prettier`

```
? Pick a linter / formatter config: 
  ESLint with error prevention only 
  ESLint + Airbnb config 
  ESLint + Standard config 
❯ ESLint + Prettier 
```

7、热更新模式，选 `Lint on save` 保存的时候就热更新

```
? Pick additional lint features: (Press <space> to select, <a> to toggle all, <i> to invert selection)
❯◉ Lint on save
 ◯ Lint and fix on commit
```

8、选择单元测试的框架，这里选择Jest

```
? Pick a unit testing solution: 
  Mocha + Chai 
❯ Jest 
```

9、配置文件存放在单独的文件里 选 `In dedicated config files`

```
? Where do you prefer placing config for Babel, ESLint, etc.? (Use arrow keys)
❯ In dedicated config files 
  In package.json 
```

10、是否保存创建的选项，保存的话，下次创建也会按这个选择来创建，我们先选择 n 不保存

```
? Save this as a preset for future projects? (y/N) n
```

11、看到以下项目

```
Successfully created project test-project.
Get started with the following commands:

 $ cd test-project
 $ npm run serve
```

12、按照提示启动项目，然后打开浏览器，可以看到对应的页面

```
DONE  Compiled successfully in 1566ms                                                                                                                                                        下午10:10:12


  App running at:
  - Local:   http://localhost:8080/ 
  - Network: http://192.168.3.46:8080/

  Note that the development build is not optimized.
  To create a production build, run npm run build.
```

13、如果要编译为生产运行的应用，执行 `npm run build` ，将会生成对应web静态资源的文件到dist目录下。

## 重要配置文件

### babel.config.js

Babel 是一个 JavaScript 编译器，可以将ES6代码转为ES5代码，从而兼容旧的浏览器使用。

在项目根目录下添加 babel.config.js 配置文件（如果没有），文件内容如下：

```
module.exports = {
  // 指定规则，presets字段设定转码规则，此处 @vue/cli-plugin-babel/preset就是规则
  presets: [
    '@vue/cli-plugin-babel/preset'
  ],

  // env定义环境模式下插件，此处定义的是development模式
  // dynamic-import-node插件（按需加载），需安装插件: npm install babel-plugin-dynamic-import-node
  env: {
    development: {
      plugins: ["dynamic-import-node"],
    },
  },
}
```

### 环境变量配置（.env.xxx）

参考：http://www.qianduan8.com/1704.html

官方文档：https://cli.vuejs.org/zh/guide/mode-and-env.html

vue cli 有以下4种方式指定环境变量（在项目根目录建立相应文件）：

```
.env                # 在所有的环境中被载入
.env.local          # 在所有的环境中被载入，但会被 git 忽略
.env.[mode]         # 只在指定的模式中被载入
.env.[mode].local   # 只在指定的模式中被载入，但会被 git 忽略
```

因此可以通过以上的方式来指定不同的环境变量，来支持开发、测试、生产等不同环境的编译信息，例如：

```
.env                     # 会在所有的环境中被载入
.env.local               # 会在所有环境中载入，但只限于本地，不会被git跟踪，git会忽略掉它
.env.development         # 只在开发环境中被载入
.env.production          # 只在生产环境中被载入
.env.development.local   # 会在本地开发环境中载入，不会被git跟踪，git会忽略掉它
.end.staging             # 演示环境中载入
```

定义了环境变量文件后，我们可以通过以下命令根据不同配置执行编译操作（注意：.env 将会在所有环境都被载入）：

```
npm run vue-cli-service serve  // 使用development环境变量编译及启动本地服务
npm run vue-cli-service build  // 默认使用production环境变量编译
npm run vue-cli-service test:e2e  // 默认使用production环境变量编译测试
npm run vue-cli-service test:unit  // 默认使用test环境变量编译测试
npm run vue-cli-service build --mode development // 使用development环境变量编译
npm run vue-cli-service build --mode production // 使用production环境变量编译
```

.env.xxx文件的定义参考如下：

```
// 非标准变量，代码中不可访问
ENV = 'XXX'

// 特殊变量，可直接访问，NODE_ENV只能为 "development"、"production" 或 "test" 中的一个
// 另外 BASE_URL 是不用配置可直接代码访问的变量，为vue.config.js 中的 baseUrl 选项，即你的应用会部署到的基础路径
NODE_ENV=development

// VUE_APP_* 开头的自定义变量，可以在代码中访问
VUE_APP_URL=http://xxx.com
VUE_APP_DIR=xxx
```

在代码中可以通过 `process.env.变量名` 来访问具体的变量值，例如 vue.config.js ：

```
module.exports = {
  publicPath: process.env.VUE_APP_URL,
  //这里在webpack配置时判断不同环境下使用不同配置
  configureWebpack: config => {
    if (process.env.NODE_ENV === "development") {
        config.devtool = "source-map";
    } else if (process.env.NODE_ENV === "production") {
        config.devtool = "eval-source-map";
    }
  },
  outputDir:process.env.VUE_APP_DIR
}
```

或者在About.vue页面中访问：

```
<template>
  <div class="about">
    <h1>This is an about page</h1>
    <h2>服务器地址:{{url}}</h2>
    <h3>当前环境：{{env}}</h3>
  </div>
</template>
<script>
export default {
  data(){
    return {
      url:process.env.VUE_APP_URL,
      env:process.env.NODE_ENV
    }
  }
}
</script>
```

**注意：process.env 不能直接放到html代码上访问，只能在js中使用。**

### package.json

`package.json` 文件描述NPM包的所有相关信息，包括作者、简介、包依赖、构建等信息，格式是严格的JSON格式。

官方说明：https://docs.npmjs.com/cli/v6/configuring-npm/package-json

**1、基础信息**

```
  "name": "项目名",
  "version": "当前版本，例如：3.7.0",
  "description": "项目描述",
  "author": "作者",
  "license": "许可类型",
  "private": true,  // 设为true这个包将不会发布到NPM平台下
  "keywords": ["key1", "key2"],  // 包的关键词信息，是一个字符串数组，同上也将显示在npm search的结果中
  "homepage": "包的主页地址",
  "repository": {
    "type": "git",
    "url": "git+https://github.com/xxx/xxx.git"
  },  // 包的仓库地址
  ...
```

**2、scripts**

通过设置这个可以使NPM调用一些命令脚本，封装一些功能，设置了脚本，可以使用 `npm run key` 的方式执行脚本，建议配置如下：

```
  "scripts": {
    "serve": "vue-cli-service serve",
    "build:prod": "vue-cli-service build",
    "build:stage": "vue-cli-service build --mode staging",
    "lint": "vue-cli-service lint"

、   # 待研究
    "preview": "node build/index.js --preview",
  },
```

注：serve、build:prod、build:stage 这3个配置可配合环境变量 .env.development、.env.production、.end.staging 使用；

**3、dependencies**

指定依赖的其它包，这些依赖是指包发布后正常执行时所需要的，也就是线上需要的包。

将使用下面的命令来安装：

```
npm install --save packageName
```

**4、devDependencies**

这些依赖只有在开发时候才需要。将使用下面的命令来安装：

```
npm install --save-dev packageName 
```

**5、engines（较少用）**

指定包运行的环境。

```
"engines": {
  "node": ">=0.10.3 < 0.12",
  "npm": "~1.0.20"
}
```

**6、browserslist**

作用：根据提供的目标浏览器的环境来，智能添加css前缀，js的polyfill垫片,来兼容旧版本浏览器。避免不必要的兼容代码，以提高代码的编译质量。

```
{ 
  ...
  "browserslist": [
    "> 1%",
    "last 2 versions",
    "not dead"
  ]
}
```

解释：（1）全球超过1%人使用的浏览器；（2）所有浏览器兼容到最后两个版本根据CanIUse.com追踪的版本。

注：与根目录的 .browserslistrc 文件作用相同

### vue.config.js

`vue.config.js` 是一个可选的配置文件，如果项目的 (和 `package.json` 同级的) 根目录中存在这个文件，那么它会被 `@vue/cli-service` 自动加载。

参考文档：https://cli.vuejs.org/zh/config/

配置文件通过 module.exports 导出配置，格式及重要的参数说明如下：

```
// vue.config.js
"use strict";
const path = require("path");

function resolve(dir) {
  return path.join(__dirname, dir);
}

/**
 * @type {import('@vue/cli-service').ProjectOptions}
 */
module.exports = {
    // 选项...

  // 部署应用包时的基本URL，如果应用部署在根目录下，应设置为"/"；如果应用被部署在一个子路径上，需要用这个选项指定这个子路径
  // 例如应用被部署在 https://www.my-app.com/my-app/，则设置 publicPath 为 /my-app/
  // 这个值也可以被设置为空字符串 ('') 或是相对路径 ('./')，这样所有的资源都会被链接为相对路径，这样打出来的包可以被部署在任意路径
  publicPath: process.env.NODE_ENV === "production" ? "/" : "/",

  // 运行 vue-cli-service build 时生成的生产环境构建文件的目录
  outputDir: "dist",

  // 放置生成的静态资源 (js、css、img、fonts) 的 (相对于 outputDir 的) 目录
  assetsDir: "static",

  // 如果你不需要生产环境的 source map，可以将其设置为 false 以加速生产环境构建
  productionSourceMap: false,

  // webpack-dev-server 相关配置， 参数说明见：https://webpack.js.org/configuration/dev-server/
  devServer: {
    // 监听的服务host地址
    host: "0.0.0.0",
    // 监听端口
    port: 8081,
    // 在服务启动后自动打开浏览器
    open: true,
    // 代理配置，更多配置方式查看: https://webpack.js.org/configuration/dev-server/#devserverproxy
    proxy: {
      // 以下配置指定'/api'路径使用代理，例如/api/users的请求将访问代理：http://localhost:3000/api/users
      "/api": {
        target: "http://localhost:3000",
      },
    },
    // 解决本地服务不能通过ip访问的问题
    disableHostCheck: true,
    ...
  },

  //  配置webpack，所配置的参数将通过 webpack-merge 合并入最终的 webpack 配置
  configureWebpack: {
    name: "项目名称",
    resolve: {
      // 替换规则
      alias: {
        "@": resolve("src"),
      },
    },
    ...
  },

  // Vue CLI 内部的 webpack 配置是通过 webpack-chain 维护的。这个库提供了一个 webpack 原始配置的上层抽象，使其可以定义具名的 loader 规则和具名插件，并有机会在后期进入这些规则并对它们的选项进行修改
  chainWebpack: (config) => {
    config.module
      .rule("vue")
      .use("vue-loader")
      .tap((options) => {
        // 修改它的选项...
        return options;
      });
  },

 ...
};
```

### .eslintrc.cjs

eslint格式及语法检查配置，参考配置如下：

```
// ESlint 检查配置
module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: ["plugin:vue/vue3-essential", "eslint:recommended"],
  parserOptions: {
    parser: "babel-eslint",
  },

  // add your custom rules here
  // it is base on https://github.com/vuejs/eslint-config-vue
  rules: {
    'vue/max-attributes-per-line': [2, {
      'singleline': 10,
      'multiline': {
        'max': 1,
        'allowFirstLine': false
      }
    }],
    'vue/singleline-html-element-content-newline': 'off',
    'vue/multiline-html-element-content-newline': 'off',
    'vue/name-property-casing': ['error', 'PascalCase'],
    'vue/no-v-html': 'off',
    'accessor-pairs': 2,
    'arrow-spacing': [2, {
      'before': true,
      'after': true
    }],
    'block-spacing': [2, 'always'],
    'brace-style': [2, '1tbs', {
      'allowSingleLine': true
    }],
    'camelcase': [0, {
      'properties': 'always'
    }],
    'comma-dangle': [2, 'never'],
    'comma-spacing': [2, {
      'before': false,
      'after': true
    }],
    'comma-style': [2, 'last'],
    'constructor-super': 2,
    'curly': [2, 'multi-line'],
    'dot-location': [2, 'property'],
    'eol-last': 2,
    'eqeqeq': ['error', 'always', { 'null': 'ignore' }],
    'generator-star-spacing': [2, {
      'before': true,
      'after': true
    }],
    'handle-callback-err': [2, '^(err|error)$'],
    'indent': [2, 2, {
      'SwitchCase': 1
    }],
    'jsx-quotes': [2, 'prefer-single'],
    'key-spacing': [2, {
      'beforeColon': false,
      'afterColon': true
    }],
    'keyword-spacing': [2, {
      'before': true,
      'after': true
    }],
    'new-cap': [2, {
      'newIsCap': true,
      'capIsNew': false
    }],
    'new-parens': 2,
    'no-array-constructor': 2,
    'no-caller': 2,
    'no-console': 'off',
    'no-class-assign': 2,
    'no-cond-assign': 2,
    'no-const-assign': 2,
    'no-control-regex': 0,
    'no-delete-var': 2,
    'no-dupe-args': 2,
    'no-dupe-class-members': 2,
    'no-dupe-keys': 2,
    'no-duplicate-case': 2,
    'no-empty-character-class': 2,
    'no-empty-pattern': 2,
    'no-eval': 2,
    'no-ex-assign': 2,
    'no-extend-native': 2,
    'no-extra-bind': 2,
    'no-extra-boolean-cast': 2,
    'no-extra-parens': [2, 'functions'],
    'no-fallthrough': 2,
    'no-floating-decimal': 2,
    'no-func-assign': 2,
    'no-implied-eval': 2,
    'no-inner-declarations': [2, 'functions'],
    'no-invalid-regexp': 2,
    'no-irregular-whitespace': 2,
    'no-iterator': 2,
    'no-label-var': 2,
    'no-labels': [2, {
      'allowLoop': false,
      'allowSwitch': false
    }],
    'no-lone-blocks': 2,
    'no-mixed-spaces-and-tabs': 2,
    'no-multi-spaces': 2,
    'no-multi-str': 2,
    'no-multiple-empty-lines': [2, {
      'max': 1
    }],
    'no-native-reassign': 2,
    'no-negated-in-lhs': 2,
    'no-new-object': 2,
    'no-new-require': 2,
    'no-new-symbol': 2,
    'no-new-wrappers': 2,
    'no-obj-calls': 2,
    'no-octal': 2,
    'no-octal-escape': 2,
    'no-path-concat': 2,
    'no-proto': 2,
    'no-redeclare': 2,
    'no-regex-spaces': 2,
    'no-return-assign': [2, 'except-parens'],
    'no-self-assign': 2,
    'no-self-compare': 2,
    'no-sequences': 2,
    'no-shadow-restricted-names': 2,
    'no-spaced-func': 2,
    'no-sparse-arrays': 2,
    'no-this-before-super': 2,
    'no-throw-literal': 2,
    'no-trailing-spaces': 2,
    'no-undef': 2,
    'no-undef-init': 2,
    'no-unexpected-multiline': 2,
    'no-unmodified-loop-condition': 2,
    'no-unneeded-ternary': [2, {
      'defaultAssignment': false
    }],
    'no-unreachable': 2,
    'no-unsafe-finally': 2,
    'no-unused-vars': [2, {
      'vars': 'all',
      'args': 'none'
    }],
    'no-useless-call': 2,
    'no-useless-computed-key': 2,
    'no-useless-constructor': 2,
    'no-useless-escape': 0,
    'no-whitespace-before-property': 2,
    'no-with': 2,
    'one-var': [2, {
      'initialized': 'never'
    }],
    'operator-linebreak': [2, 'after', {
      'overrides': {
        '?': 'before',
        ':': 'before'
      }
    }],
    'padded-blocks': [2, 'never'],
    'quotes': [2, 'single', {
      'avoidEscape': true,
      'allowTemplateLiterals': true
    }],
    'semi': [2, 'always'],
    'semi-spacing': [2, {
      'before': false,
      'after': true
    }],
    'space-before-blocks': [2, 'always'],
    'space-before-function-paren': [2, 'never'],
    'space-in-parens': [2, 'never'],
    'space-infix-ops': 2,
    'space-unary-ops': [2, {
      'words': true,
      'nonwords': false
    }],
    'spaced-comment': [2, 'always', {
      'markers': ['global', 'globals', 'eslint', 'eslint-disable', '*package', '!', ',']
    }],
    'template-curly-spacing': [2, 'never'],
    'use-isnan': 2,
    'valid-typeof': 2,
    'wrap-iife': [2, 'any'],
    'yield-star-spacing': [2, 'both'],
    'yoda': [2, 'never'],
    'prefer-const': 2,
    'no-debugger': process.env.NODE_ENV === 'production' ? 2 : 0,
    'object-curly-spacing': [2, 'always', {
      objectsInObjects: false
    }],
    'array-bracket-spacing': [2, 'never']
  }
};
```

### .eslintignore

配置忽略eslint格式及语法检查文件的配置参数，参考如下：

```
# 忽略build目录下类型为js的文件的语法检查
build/*.js
# 忽略src/assets目录下文件的语法检查
src/assets
# 忽略public目录下文件的语法检查
public
# 忽略当前目录下为js的文件的语法检查
*.js
# 忽略当前目录下为vue的文件的语法检查
*.vue
```

## 使用Vuex（4.x版本）

参考文档：https://vuex.vuejs.org/zh/

Vuex 是一个专门为vue.js应用程序开发的状态管理模式。对于状态（state），我们可以理解为需要共享给所有组件使用的变量（数据，也可以理解为全局性的变量）。也就是说，当我们需要向所有组件共享数据时，可以使用Vuex进行统一集中式的管理。

**vuex中，有默认的五种基本的对象：**

- state：存储状态（变量）

- getters：对数据获取之前的再次编译，可以理解为state的计算属性。我们在组件中使用 $sotre.getters.fun()

- mutations：修改状态，并且是同步的。在组件中使用$store.commit('',params)。这个和我们组件中的自定义事件类似。

- actions：异步操作。在组件中使用是$store.dispath('')

- modules：store的子模块，为了开发大型项目，方便状态管理而使用的。这里我们就不解释了，用起来和上面的一样。

### 安装

通过npm安装vuex包

```
npm install vuex@next --save
```

Vuex 依赖 [Promise](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Guide/Using_promises)。如果你支持的浏览器并没有实现 Promise (比如 IE)，那么你可以使用一个 polyfill 的库，例如 [es6-promise](https://github.com/stefanpenner/es6-promise)。

按以下命令进行安装：

```
npm install es6-promise --save
```

并将下列代码添加到你使用 Vuex 之前的一个地方：

```
import 'es6-promise/auto'
```

### 基本使用

在 ./src 目录下创建store.js文件（或创建store目录，并在 该目录下创建index.js），在该模块中创建Vuex的store对象（使用Vue Cli可自动创建该文件）：

```javascript
// ./src/store.js 或 ./src/store/index.js
import { createStore } from "vuex";

// 创建store对象，并作为默认访问接口
export default createStore({
  // 指定要存储的状态值
  state: {
    count: 0,
    jsonObj: { prop1: 'p1'},
  },

  // 获取基于state状态进行计算后的值，类似 vue 的 computed
  getters: {
    // 无入参方式，示例: 获取count值的平方
    countSquare: state => {
      return Math.pow(state.count, 2);
    },
    // 通过getters返回函数，来支持传参数，示例，获取count的多次方
    countPow: (state) => (n) => {
      return Math.pow(state.count, n);
    },
    // 接受其他 getter 作为第二个参数
    countSquareAddOne: (state, getters) => {
      return getters.countSquare + 1;
    }
  },

  // 状态值变更方法，注意所有方法都必须是同步方法
  mutations: {
    // 无入参的状态值变更方法
    increment (state) {
      state.count++;
    },
    // 带参数的状态值变更方法
    incrementByN (state, n) {
      state.count += n;
    },
    // 使用 payload 风格支持传入更多参数，以及更通用的执行方式
    incrementPayload(state, payload) {
      state.count += payload.amount; 
    },
    // 在对象上添加属性，需要遵循Vue的规则，保证Vue对变量状态的监控有效
    addProp(state) {
      Vue.set(state.jsonObj, 'newProp', 123); // 通过 Vue.set方法新增属性
      state.jsonObj = {...state.jsonObj, 'newProp1': 456}; // 使用新对象替换老对象，使用对象展开符的方式
    }
  },

  // 状态值的异步变更动作
  actions: {
    // 通过执行 mutations 方法进行状态值变更
    // 通过 context.commit 提交mutations变更, 通过 context.state, context.getters 分别获取state和getters
    increment (context) {
      context.commit('increment');
    },
    // 上面方法的简化写法, 通过ES2015的“参数解构”方式简化，context 替换为 { commit, state } 来减少代码量
    incrementSimple ({ commit }) {
      commit('increment');
    },
    // 支持异步处理函数
    incrementAsync ({ commit }) {
      setTimeout(() => {
        commit('increment');
      }, 1000);
    },
    // 同样支持入参的方式
    incrementPayload ({commit, state}, payload) {
      commit('incrementPayload', payload);
    },
  }
});
```

在应用的main.js入口文件中引入store：

```javascript
// ./src/main.js
...
import { createApp } from "vue";
...
import store from "./store"; // 引入store对象

// 通过use(store)装载store
createApp(App).use(store).use(router).mount("#app");
...
```

在各部分代码就可以通过 this.$store.state.xxx 来访问state中的对象：

```javascript
// js代码中直接访问，无需引入
const currentCount = this.$store.state.count; // 获取 store 的 state 状态值
// 通过getters获取计算值
const countSquare = this.$store.getters.countSquare; // 直接以属性方式获取值
const countPow = this.$store.getters.countPow(4); // 以函数方式调用返回函数对象的getters

// 执行同步的状态值变更
this.$store.commit('increment'); // 执行定义的变更方法修改 state 的状态值
this.$store.commit('incrementByN', 10); // 执行带参数的变更方法
this.$store.commit('incrementPayload', { amount: 8 }); // 执行payload风格的变更方法
this.$store.commit({ type: 'incrementPayload', amount: 8 }); // 执行payload风格变更方法的另一种模式
// 执行异步的状态值变更
this.$store.dispatch('increment'); // 通过store.dispatch触发异步状态更新
this.$store.dispatch('incrementPayload', { amount: 8 }); // 带参数方式的异步状态更新触发
this.$store.dispatch({ type: 'incrementPayload', amount: 10 }); // 执行payload风格的触发方式

// 通过引入store.js方式进行访问，除了无需使用 this.$ 前缀以外，跟上面的用法一样
import store from './store'
const currentCount = store.state.count;  // 获取 store的指定状态值
...
```

### actions组合及Promise模式

actions函数可以支持返回Promise对象，同时基于Promise的异步机制来实现多个actions的组合使用，如下所示：

```javascript
// Promise及组合示例
actions: {
  // 返回Promise对象的动作A
  actionA ({ commit }) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        commit('someMutation')
        resolve()
      }, 1000)
    })
  },
  // 支持通过入参的 dispatch 调用其他actions, 形成组合；actionB中执行actionA的示例，返回的仍然是Promise对象
  actionB ({ dispatch, commit }) {
    return dispatch('actionA').then(() => {
      commit('someOtherMutation')
    })
  },
  // 支持在action函数里面使用await的同步等待方式
  async actionC ({ commit }) {
    commit('gotData', await getData());
  },
  async actionD ({ dispatch, commit }) {
    await dispatch('actionC'); // 等待 actionA 完成
    commit('gotOtherData', await getOtherData());
  }
}
```

对于返回Promise对象的actions调用方式如下：

```javascript
this.$store.dispatch('actionA').then(() => {
  // ...
})
```

### 模块处理

对于复杂项目，全部状态放在一起处理会让代码变复杂。Vuex 允许将 store 分割成**模块（module）**。每个模块拥有自己的 state、mutation、action、getter、甚至是嵌套子模块——从上至下进行同样方式的分割：

```javascript
// a.js, 模块A的store定义
const moduleA = {
  state: () => ({ ... }),
  mutations: { ... },
  actions: { ... },
  getters: { ... }
}

// b.js, 模块b的store定义
const moduleB = {
  state: () => ({ ... }),
  mutations: { ... },
  actions: { ... }
}

// store.js，组合模块A和模块b定义，组合形成store对象
const store = new Vuex.Store({
  modules: {
    a: moduleA,
    b: moduleB
  }
})

// xx.js, 在state中指定模块别名访问不同模块的状态
this.$store.state.a.xx; // -> 访问moduleA 的状态
this.$store.state.b.xx; // -> 访问moduleB 的状态
```

**注：在store中，只有state才会区分模块存储，而getters、mutations、actions都会合并在一起。**

**getters**：与 state 不同的是，不同模块的 getters 会直接合并在 store.getters 下。**如果存在不同模块的getters重名的情况，Vuex 会报出 'duplicate getter key: [重复的getter名]' 错误**。

```javascript
// a.js, 模块A的store定义
const moduleA = {
    state: {
        count: 1
    },
    getters: {
        // 模块模式下，state-当前模块的局部state; getters-等同store.getters，可以访问其他getters函数; rootState-全局state，可以访问其他模块的 state
        maGetter(state, getters, rootState) {
            return state.count + rootState.b.count;
        }
    }
};

// b.js, 模块b的store定义
const moduleB = {
    state: {
        count: 2
    },
    getters: {
        mbGetter() {
            return 'Hello Vuex';
        }
    }
};

// store.js，组合模块A和模块b定义，组合形成store对象
const store = new Vuex.Store({
  modules: {
    a: moduleA,
    b: moduleB
  }
});

// xx.js, 使用getters无需区分模块
console.log(this.$store.getters.maGetter); // 3
console.log(this.$store.getters.mbGetter); // Hello Vuex
```

**Mutations**：mutations 与 getters 类似，会直接合并在 store.mutations，直接通过 store.commit 触发。不同的是不同模块的 mutation 可以重名，不会报错；实际执行中，**在执行一个 store.commit 时，重名的 mutation 将会依次执行**（也就是会确保每个模块的变更都会被执行）。

```javascript
// a.js, 模块A的store定义
const moduleA = {
    state: {
        count: 1
    },
    mutations: {
        sayCount(state) {
            console.log('Module A count: ', state.count);
        }
    }
};

// b.js, 模块b的store定义
const moduleB = {
    state: {
        count: 2
    },
    mutations: {
        sayCountB(state) {
            console.log('Module B count: ', state.count);
        },
        sayCount(state) {
            console.log('Module B count: ', state.count);
        }
    }
};

// store.js，组合模块A和模块b定义，组合形成store对象
const store = new Vuex.Store({
  modules: {
    a: moduleA,
    b: moduleB
  }
});

// xx.js, 直接执行mutations
store.commit('sayCount'); // 重名情况依次执行不同模块的mutation: Module A count: 1\nModule B count: 2
store.commit('sayCountB'); // Module B count: 2 
```

**Actions**：与 mutations 类似，不同模块的 actions 均可以通过 store.dispatch 直接触发。**当不同模块中有同名 action 时，通过 store.dispatch 调用，会依次触发所有同名 actions**。

action 的回调函数接收一个 context 上下文参数，context 包含：1. state、2. rootState、3. getters、4. mutations、5. actions 五个属性，为了简便可以在参数中解构。

```javascript
// a.js, 模块A的store定义
const moduleA = {
    state: {
        count: 1
    },
    mutations: {
        sayCountA(state) {
            console.log('Module A count: ', state.count);
        }
    },
    actions: {
        maAction(context) {
            context.dispatch('mbAction');
        }
    }
};

// b.js, 模块b的store定义
const moduleB = {
    state: {
        count: 2
    },
    mutations: {
        sayCountB(state, num) {
            console.log('Module B count: ', state.count+num);
        }
    },
    action: {
        mbAction({ commit, rootState }) {
            commit('sayCountA');
            commit('sayCountB', rootState.a.count);
        }
    }
};

// store.js，组合模块A和模块b定义，组合形成store对象
const store = new Vuex.Store({
  modules: {
    a: moduleA,
    b: moduleB
  }
});

// xx.js, 直接执行mutations
this.$store.dispatch('maAction'); // Module A count: 1、Module B count: 3
```

**注：除了state有全局和局部入参以外， getters、mutations、actions都是全局入参，可以直接访问其他模块所定义的函数。**

**命名空间**：默认情况下，模块内部的 action、mutation 和 getter 是注册在**全局命名空间**的——这样使得多个模块能够对同一 mutation 或 action 作出响应。如果我们需要保持模块之间的独立性，可以在定义模块时增加 `namespaced: true` 属性，让模块注册到自有的命名空间上。

命名空间对模块访问的影响见以下代码：

```javascript
const store = new Vuex.Store({
  modules: {
    account: {
      namespaced: true,  // 指定 account 模块具有独立命名空间
      // 模块内容（module assets）
      state: () => ({ ... }), // namespaced属性对其无影响
      // 受命名空间影响，需通过含命名空间路径 this.$store.getters['account/xxx'] 的方式来访问
      getters: {
        // state-当前模块; getters-当前命名空间； rootState-当前命名空间; rootGetters-全局
        isAdmin (state, getters, rootState, rootGetters) { ... } // -> this.$store.getters['account/isAdmin']
      },
      // 受命名空间影响，需通过含命名空间路径 this.$store.commit('account/xxx') 的方式来访问，命名空间内重名的情况依次执行
      mutations: {
        // 作用在当前模块
        login (state, payload) { ... } // -> this.$store.commit('account/login')
      },
      // 受命名空间影响，需通过含命名空间路径 this.$store.dispatch('account/xxx') 的方式来访问，命名空间内重名的情况依次触发
      actions: {
        // dispatch-当前命名空间; commit-当前命名空间, getters-当前命名空间, rootGetters-全局
        login ({ dispatch, commit, getters, rootGetters }) {
          // 访问全局getters和命名空间内部getters
          getters.someGetter // -> 'foo/someGetter'
          rootGetters.someGetter // -> 'someGetter'

                    // 触发全局actions和命名空间内部actions，通过指定第三个参数 { root: true }
          dispatch('someOtherAction') // -> 'foo/someOtherAction'
          dispatch('someOtherAction', null, { root: true }) // -> 'someOtherAction'

                    // 触发全局mutations和命名空间内部mutations，通过指定第三个参数 { root: true }
          commit('someMutation') // -> 'foo/someMutation'
          commit('someMutation', null, { root: true }) // -> 'someMutation'
        }, // -> this.$store.dispatch('account/login')

        // 在命名空间的模块内注册全局的actions，添加 root: true，并将这个 action 的定义放在函数 handler 中
        someAction: {
          root: true,
          handler (namespacedContext, payload) { ... } // -> 'someAction'
        }
      },

      // 嵌套模块
      modules: {
        // 继承父模块的命名空间
        myPage: {
          state: () => ({ ... }),
          getters: {
            profile () { ... } // -> getters['account/profile']
          }
        },

        // 进一步嵌套命名空间
        posts: {
          namespaced: true,

          state: () => ({ ... }),
          getters: {
            popular () { ... } // -> getters['account/posts/popular']
          }
        }
      }
    }
  }
})
```

**模块动态注册**：在 store 创建**之后**，可以使用 `store.registerModule` 方法注册模块：

```javascript
const store = new Vuex.Store({ /* 选项 */ })

// 注册模块 `myModule`
store.registerModule('myModule', {
  // ...
});
// 注册嵌套模块 `nested/myModule`
store.registerModule(['nested', 'myModule'], {
  // ...
});
// 通过 preserveState: true 参数指定不复制state（假设原有模块已有对应的state，新增模块希望保留原有模块的state）
store.registerModule('myModule', module, { preserveState: true })；

// 动态卸载模块，注意，不能使用此方法卸载静态模块（即创建 store 时声明的模块）
store.unregisterModule('myModule');

// 检查模块是否存在
if (store.hasModule('myModule')){
  //...
}
```

## 单元测试

参考文档：https://lmiller1990.github.io/vue-testing-handbook/zh-CN/

JTest参考文档：https://jestjs.io/zh-Hans/docs/getting-started

通过vue cli安装，会自动安装相关依赖库、生成配置、以及生成测试目录和示例，具体说明如下：

（1）生成 jest.config.js 配置文件；

（2）在package.json配置文件上的script配置增加 "test:unit": "vue-cli-service test:unit"；

（3）在 .eslintrc.js 配置上增加以下配置：

```
  overrides: [
    {
      files: [
        "**/__tests__/*.{j,t}s?(x)",
        "**/tests/unit/**/*.spec.{j,t}s?(x)",
      ],
      env: {
        jest: true,
      },
    },
  ]
```

（4）新增 tests/unit 的测试目录。

在使用上，可以通过以下命令运行测试：

```
// 自动执行所有 *.spec.js 测试文件
npm run test:unit
// 指定执行某个测试文件
npm run test:unit ./tests/unit/a.spec.js
```

**注意：测试文件必须放在 ./tests/unit/ 目录下，并且文件名必须以 .spec.js 结尾，否则会出现语法错误。**

## Vue3遇到的坑

### keepAlive

#### 多路由复用同一个组件的问题

如果有多个路由使用同一个组件，对这些路由页面使用keepAlive进行缓存处理，即使路由path不同，所有路由打开的页面都相同，展现的是同一个缓存内容，无法区别不同页面进行缓存。

```
<template>
  <section class="app-main">
    <router-view v-slot="{ Component }">
      <transition name="fade-transform" mode="out-in">
        <keep-alive >
          <component :is="Component"></component>
        </keep-alive>
      </transition>
    </router-view>
  </section>
</template>
```

这是由于在默认情况下，keepAlive是根据组件的名字进行缓存，由于所有组件名字一样，所以会导致缓存相同。要解决这个问题，可以在缓存的组件上增加key属性，设置不同路由页面组件唯一的key，这样就能按照不同路由缓存不同页面。

```
<template>
  <section class="app-main">
    <router-view v-slot="{ Component }">
      <transition name="fade-transform" mode="out-in">
        <keep-alive>
          <component :key="key" :is="Component"></component>
        </keep-alive>
      </transition>
    </router-view>
  </section>
</template>

export default {
  ...
  computed: {
    // 用完整路由路径设置组件的唯一key，确保不同页面有不同缓存数据
    key() {
      return this.$route.fullPath;
    }
  },
  ...
};
```

#### 清除指定缓存

Vue3没有提供手工操作缓存的API，缓存管理由框架自行管理，因此要清除指定组件的缓存，只能通过  keepAlive 的 include 等条件进行处理，让组件名不符合缓存匹配条件，从而让框架自动删除缓存。

如以下代码，将需要缓存的组件名放入cachedComponents数组。如果需要清除某个组件的缓存，将组件名从数组移除，然后刷新页面即可，下面代码同步提供了一个不闪烁的刷新页面方法：

```
<template>
  <section class="app-main">
    <router-view v-slot="{ Component }">
      <transition name="fade-transform" mode="out-in">
        <keep-alive :include="cachedComponents">
          <component :key="key" v-if="isShow" :is="Component"></component>
        </keep-alive>
      </transition>
    </router-view>
  </section>
</template>
export default {
  ...
  computed: {
    // 是否显示组件
    isShow() {
      return this.$store.state.tagsView.appMainShow;
    },
    // 获取缓存的组件名
    cachedComponents() {
      return this.$store.state.tagsView.cachedComponents;
    },
    key() {
      return this.$route.fullPath;
    }
  },
  methods: {
    reload() {
      this.$store.dispatch('tagsView/setAppMainShow', false).then(() => {
        this.$nextTick(() => { this.$store.dispatch('tagsView/setAppMainShow', true); });
      });
    }
  },
  ...
};
```

注意点1：将组件名移除，则会将使用该组件的所有路由页面的缓存一并移除，如果存在一个组件多个路由使用的情况需谨慎；

注意点2：控制页面刷新的机制是通过 v-if="isShow" 移除组件然后又加载组件；注意这个操作不能放在 keep-alive 上，因为一旦移除了 keep-alive组件，所有缓存数据都会被移除（可以基于这个机制进行清除所有缓存的处理）。

#### 多级路由缓存的支持

keepAlive的缓存机制只能支持2级嵌套组件（2级路由），3级以上的组件嵌套将无法缓存。要支持3级以上的组件嵌套进行缓存，可以在子组件外面再继续嵌套使用 keep-alive 组件，如果有多级嵌套就使用多个 keep-alive 。例如：

```
<!-- 子组件 -->
<template>
  <div>
    <keep-alive>
      <component :is="route.meta.componentName"
        :query="route.query"
        :params="route.params"
        :pass-props="passProps"
      ></component>
    </keep-alive>
  </div>
</template>
```

#### 同一组件多路由复用的独立缓存方案

在“多路由复用同一个组件的问题”已提到可以支持多路由复用组件的缓存方式，但是这个方式无法清除单个路由页面的缓存，也就是无法单独刷新某个页面。由于keepAlive的缓存机制是以组件名作为唯一key进行缓存，因此vue原生方式无法解决该问题。

这里提供的方案思路是基于组件动态生成真正使用的组件并放到不同的动态路由上，这样由于动态生成的组件名不同，keepAlive机制会认为这是不同的组件，从而能实现独立的缓存，也能支持单页面的刷新。

（1）在需要创建路由时（使用前），复制所需的组件，并按不同的组件名（例如用nanoid随机生成）注册为全局组件。组件操作相关的核心方法如下：

```
import appObj from '@/main'; // main.js生成的全局app对象

/**
 * 将组件注册为全局组件
 * @param {string} name - 注册组件名
 * @param {Object} component - 组件对象
 * @returns
 */
export const regGlobalComponent = (name, component) => appObj.component(name, component);

/**
 * 判断组件是否已注册
 * @param {string} name - 组件名
 * @returns {bool} - 是否已注册
 */
export const hasGlobalComponent = (name) => appObj._context.components[name] !== undefined;

/**
 * 获取全局注册组件
 * @param {string} name - 组件名
 * @returns {Object} - 组件对象
 */
export const getGlobalComponent = (name) => appObj._context.components[name];

/**
 * 复制指定组件注册为新组件
 * 注意：该复制不会包含style内容
 * @param {string} name - 新组件名
 * @param {string} copyName - 要复制的组件名
 */
export const copyGlobalComponent = (name, copyName) => {
  if (!hasGlobalComponent(name)) {
    const component = getGlobalComponent(copyName);
    const newComponent = {
      extends: component
    };
    newComponent.name = name; // 需要修改控件名，否则获取到的控件名为undefined
    regGlobalComponent(name, newComponent);
  }
};

/**
 * 删除指定的注册组件
 * @param {string} name - 要删除的组件名
 */
export const delGlobalComponent = (name) => {
  if (hasGlobalComponent(name)) {
    delete appObj._context.components[name];
  }
};
```

（2）使用 router.addRoute(routerItem) 方法创建使用该组件的动态路由，routerItem的格式与正常配置的路由格式一致，只是component属性放入上面动态创建的组件对象；这里可以直接用组件名作为路由名，便于后续删除路由使用；

（3）将动态创建的组件对象的组件名放入 keep-alive 的 include 数组中，让缓存生效；

（4）正常通过路由访问对应的页面；

（5）如果不再需要该路由，可以按相反的步骤删除路由：将组件名移出include数组、删除动态路由、取消全局组件的注册。

### iframe页面状态保持

vue路由切换和组件信息保存的机制较为复杂，同时iframe的页面内容并无法通过keep-alive的vnode机制进行保存，所以iframe页面状态的保持难以按照vue常用的方案实现。

以下是尝试失败的方式：

（1）直接使用包含iframe标签的组件，vue只保存组件的状态，并无法保存iframe内容，因此每次切换路由都会重新加载iframe内容页面；

（2）在router-view同级通过v-for动态创建包含iframe标签的组件，通过v-show显示当前组件内容，结果也是每次都重新加载；

（3）在router-view同级创建一个可供显示的div标签，切换路由时动态操作dom在div标签上增加iframe元素或显示已创建的iframe元素，结果仍然每次切换路由会重新加载，可能动态操作dom所产生的iframe元素并无法在vue的缓存机制下保存。

最后发现以下方案可行：

（1）实现包含iframe标签的组件，用于展示iframe内容；

（2）在router-view同级通过v-for动态创建包含iframe标签的组件，但**必须设置key属性，每个iframe页面要设置不同的key**，这样才能确保vue能区用一个组件动态生成的不同对象并进行缓存；

（3）v-for生成的组件**使用v-show控制是否显示**，注意不能通过dom原生的方式处理隐藏和显示；

（4）如果要保存某个页面不刷新，**v-for所对应的iframe数组所对应该页面的元素不能发生变化**，也就是应该通过push增加新iframe对象，通过splice删除数组中无需保存状态的iframe对象；注意如果修改了数组中对应元素的引用地址（例如“array[i] = 新配置”），这样即使新配置信息和原信息一样，也会触发vue的变量变动监听，导致组件重新刷新；

（5）如果需要刷新iframe页面，可以在包含iframe标签的组件内部通过v-if来取消和包含iframe标签实现重新加载。
