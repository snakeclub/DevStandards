# JS模版导入导出详解

在js开发中，经常看到 module.exports，exports，require和export，export default，import等模版导入导出代码的使用，以下将针对这些代码进行详细的说明，搞清楚相关用法和区别。

这几个方法的分类如下：

（1）module.exports和exports属于Node.js的CommonJS模块规范，用于声明所导出模块暴露的内容，对应的导入代码是 require；

（2）export和export default属于ES6语法所支持的模块代码，用于声明所导出模块的接口，对应的导入代码是import。



## module.exports和exports

module.exports和exports属于Node.js的CommonJS模块规范。

在Node.js中，每个Node应用由模块组成，每个js文件就是一个模块，有自己的作用域。在一个模块（文件）里面定义的变量、函数、类等，都是私有的，对其他模块（文件）不可见。

根据CommonJS规范规定，每个模块（文件）内部，使用module变量代表当前模块。这个变量是一个对象，它的exports属性（即module.exports）是外部访问的标准接口。通过require加载某个模块（文件），其实是等同于加载该模块的module.exports属性。

以下面的example.js模块定义为例子：

```javascript
// example.js
var x = 5;
var addX = function(value){
  return value + x;
};

// 指定 module.exports 属性，输出可访问接口
module.exports = {
  x: x,
  addX: addX
};
```

该模块设置了 module.exports 的属性值，其他模块（文件）可通过 module.exports 属性访问example.js模块（文件）的变量及函数：

```javascript
// test.js
var example = require('./example.js');  // 引入模块，example变量实际指向example.js模块的module.exports属性

// 通过引入的example变量访问example.js模块的变量和方法
console.log(example.x); // 5
console.log(example.addX(1)); // 6
```



在Node.js中，module.exports 初始值为一个空对象 {}，因此也可以采用以下方式直接在 module.exports 对象添加属性值的方式进行访问接口的定义：

```javascript
// example.js
var x = 5;
var addX = function(value){
  return value + x;
};

// 通过添加exports属性值的方式定义module.exports的访问接口
module.exports.x = x;
module.exports.addX = addX;
```



在模块（文件）中，exports变量是指向module.exports的预定义变量，实际上等同在每个模块（模块）头部，默认有一行这样的命令：

`var exports = module.exports;`

因此在模块（文件）中也可以这样定义访问接口：

```javascript
// example.js
var x = 5;
var addX = function(value){
  return value + x;
};

// exports == module.exports, 可以通过添加exports属性值的方式定义module.exports的访问接口
exports.x = x;
exports.addX = addX;
```



除了以对象方式（{...}）设置module.exports，也可以将其定义为一个类构造函数形式的访问接口：

```javascript
// class.js
// 类构造函数
var CLASS = function(args){
	this.args = args;
};

// 指定exports属性为构造函数
module.exports = CLASS;
```

对于类构造函数形式的访问接口，使用时需要通过new先进行对象实例化：

```javascript
// test.js
var CLASS = require('./class.js');  // 引入模块

// 需要先实例化对象
var c = new CLASS('构造函数初始变量');
...
```



也可以将访问接口定义为已实例化的对象，例如：

```javascript
// class_object.js
// 类构造函数
var CLASS = function(){
	this.name = 'class';
};

CLASS.prototype.func = function(){
  alert(this.name);
};

// 指定exports属性实例化对象
module.exports = new CLASS();
```

已实例化的访问接口对象，可以直接使用：

```javascript
// test.js
var CLASS_OBJECT = require('./class_object.js');  // 引入模块

// 直接使用
CLASS_OBJECT.func();  // 弹出 "class" 内容的告警框
```



## export和export default

export和export default是ES6的模块导出语法。

每个js文件同样是一个模块，每个模块只加载一次，即 每个js文件只执行一次， 如果多次加载同目录下的相同文件，已加载的文件将直接从内存中读取。 在ES6中一个模块就是一个单例，或者说就是一个对象。

每一个模块内声明的变量都是局部变量， 不会污染全局作用域。

模块内部的变量或者函数可以通过export指定导出，一个模块中可以导出多个变量或函数。

一个模块可以导入别的模块。



以下面的export_sample.js模块定义为例子：

```javascript
// export_sample.js
let name = 'xiaoming';
let age = 18;
let fn1 = function() {console.log('sayHi')};

// 导出 name, age 变量，以及 fn1 函数, 其中将fn1导出接口为别名sayHi
export {name, age, fn1 as sayHi};
```

通过import导入模块定义的接口，对于export导出的接口，需要通过import {...} from '...' 的方式导入：

```javascript
// import.js
import {name, age, sayHi} from './export_sample.js'；

// 直接使用导入的接口
let add_age = age + 10;
sayHi();
```

在导入方面，也可以通过通配符 * 方式进行批量导入，例如：

```javascript
// import.js
import * as testModule from './export_sample.js'；

// 直接使用导入的接口
let add_age = testModule.age + 10;
testModule.sayHi();
```



指定导出接口，也可以通过直接在变量定义中指定export来进行导出，例如：

```javascript
// export_sample.js
// 直接在定义中指定export，不过注意这种方式无法导出为别名的方式
export const name = 'xiaoming';
export const age = 18;
export const fn1 = function() {console.log('sayHi')};
```



可以通过 export default 的方式，导出默认的接口，一个模块只能有一个默认接口，也就是一个js文件只能有一个  export default 导出，但可以有多个export导出，同时export和export default可以共存，例如：

```javascript
// export_sample.js
export const name = 'xiaoming';
export const age = 18;
let fn1 = function() {console.log('sayHi')};
export {fn1 as sayHi};

// 导出默认接口对象
export default {
  name: name,
  age: age,
  add_age: age + 10;
  sayHi: fn1
};
```

export default导出的默认接口对象需要通过import xxx from '...' 的方式导入，例如：

```javascript
// import.js
import defaultModule from './export_sample.js'；

// 使用默认接口
defaultModule.sayHi();
```



**注：import也可以支持导入文件夹，实际上如果导入的是文件夹，将自动导入该文件夹目录下的index.js文件（这是Node.js的获取机制）。**

