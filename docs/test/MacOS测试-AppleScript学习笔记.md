# MacOS测试-AppleScript学习笔记

AppleScript 是 Mac OS X内置的一种功能强大的脚本语言，使用 AppleScript 的目的是把一些重复繁琐并且耗费时间的任务自动化。

## 运行方式

### 脚本编辑器

脚本编辑器是Mac自带的AppleScript脚本编辑和运行器，可在启动台傻姑娘搜索“脚本编辑器”（或"Script Editor"）进行启动，启动后可以在上面编辑和运行脚本，如下图：

<img src="MacOS%E6%B5%8B%E8%AF%95-AppleScript%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0.assets/001.png" alt="001" style="zoom:50%;" />

脚本编辑器还有一个词典功能，通过菜单的 “文件 -> 打开词典...” 打开，通过词典可以查看MacOS里安装的应用程序对外暴露的调用接口和属性，可以通过AppleScript脚本调用。

<img src="MacOS%E6%B5%8B%E8%AF%95-AppleScript%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0.assets/002.png" alt="002" style="zoom: 33%;" />

### 命令行执行

可以通过 osascript 命令，通过命令行执行applescript脚本。该命令帮助内容如下：

```
usage: osascript [-l language] [-e script] [-i] [-s {ehso}] [programfile] [argument ...]
```

1、执行脚本文件

```
% osascript scriptfile.scpt
```

2、直接执行脚本

```
% osascript -e "display dialog \"Hello World\""
```

### 通过python执行

开源项目：https://github.com/rdhyee/py-applescript

可以通过python执行applescript脚本，需要安装  pyobjc 和 py-applescript 两个库：

```
% pip install pyobjc
% pip install py-applescript
```

编写以下python程序执行：

```
import applescript

# 执行脚本
applescript.AppleScript('say "Hello AppleScript"').run()
```



## AppleScript保留字

AppleScript保留字，按字母顺序列出：

| 1           | 2       | 3         | 4          | 5           |
| ----------- | ------- | --------- | ---------- | ----------- |
| about       | above   | after     | against    | and         |
| apart from  | around  | as        | aside from | at          |
| back        | before  | beginning | behind     | below       |
| beneath     | beside  | between   | but        | by          |
| considering | contain | contains  | contains   | continue    |
| copy        | div     | does      | eighth     | else        |
| end         | equal   | equals    | error      | every       |
| exit        | false   | fifth     | first      | for         |
| fourth      | from    | front     | get        | given       |
| global      | if      | ignoring  | in         | instead of  |
| into        | is      | it        | its        | last        |
| local       | me      | middle    | mod        | my          |
| ninth       | not     | of        | on         | onto        |
| or          | out of  | over      | prop       | property    |
| put         | ref     | reference | repeat     | return      |
| returning   | script  | second    | set        | seventh     |
| since       | sixth   | some      | tell       | tenth       |
| that        | the     | then      | third      | through     |
| thru        | timeout | times     | to         | transaction |
| true        | try     | until     | where      | while       |
| whose       | with    | without   |            |             |



## AppleScript基本语法

### 1、注释

脚本中可以使用  `--`、`#`、`(* *)`来进行注释，其中 `--`、`#` 是行尾注释，不支持换行，`(* *)` 为块注释，支持换行。

示例如下：

``` 
-- 这是行注释
# 这同样是行注释
display dialog "Hello World" -- 行尾进行注释
(*这个是块注释
可以跨行或
多行*)
```

### 2、变量和属性

AppleScript支持设置和使用变量，通过 `set ... to ...` 关键字设置名和变量值（**注：变量名不能为关键字，且变量名的第一个字符不能为数字**），例如：

```
set width to 8
set height to 9.3
set area to width * height
set str1 to "hello world"
```

通过 property 指定属性和赋值

```
property propertyCount : 4  # 定义属性
get propertyCount  # 直接访问即可
get propertyCount of me  # 通过 me 指定属性的归属是当前脚本，这对跨程序场景使用的指定特别有效
```

使用 global 指定变量为全局变量，使用 local 指定变量为局部变量

```
set currentCount1 to 0
set currentCount2 to 1
global currentCount3  # 声明该变量为全局变量
set currentCount3 to 2
global currentCount4
set currentCount4 to 4
property propertyCount : 4
on increment()
	global currentCount1 # 在函数中声明该变量为全局变量，因此可改变外部变量值
	set currentCount1 to currentCount1 + 2  # 全局变量
	set currentCount2 to 10  # 未声明全局变量，内部变量需要定义，否则会出错
	set currentCount2 to currentCount2 + 2  # 局部变量
	set currentCount3 to currentCount3 + 2  # 外部声明了是全局变量，因此可以直接访问
	local currentCount4  # 外部声明了变量为全局，但内部声明该变量名为局部变量，需要定义
	set currentCount4 to 20
	set currentCount4 to currentCount4 + 4
	set propertyCount to propertyCount + 2  # 属性可以直接使用
end increment

increment()
log currentCount1 --result: 2
log currentCount2 --result: 1
log currentCount3 --result: 4
log currentCount4 --result: 4
log propertyCount --result: 8
```

变量的赋值机制，实际上赋值的是引用地址，将变量赋值给变量的情况，如果原变量发生变化，引用地址的值不会随之改变：

```
set age to 30  # 将值30的引用地址赋值给age
set resultAge to age  # 将age对应的引用地址（也就是30的引用地址）赋值给resultAge
set age to 50  # 将值50的引用地址赋值给age
get resultAge  # 输出30，是age的原值引用地址，而不是age变量本身
```

### 3、基础数据类型

#### **（1）布尔类型 Boolean**

True 和 False （不区分大小写）

```
set a to true
set b to false
set c to "a" = "b"  # 通过表达式赋值
```

#### **（2）数字 Number**

数字基本上分为两类:整数(*intergers*)和分数(fractional numbers)。整数用来计数，比如循环次数。分数或者称作实数 (real numbers，简写作*reals*)用来计算。整数和实数都可以是负数。

```bash
set x to 25
set y to -123.234
```

#### **（3）字符串 Text**

字符串是通过双引号引起来的连串字符，可以通过 '&' 符号进行拼接。

```
set x to "abc"
set y to "def"
set z to x & "连接" & y
```

查看字符串长度： length of / the length of

```
set theLength to the length of "I'm Rose."  # 输出结果为9
```

字符串和数字的强制转换

```
set a to "14" as number  # 字符串转为数字，输出14
set a to 14 as string  # 数字转换为字符串，输出"14"
set a to "2.99" as real  # 字符串转换为实数，输出2.99
set a to "2.99" as integer  # 字符串转换为整数，损失小数精度，输出3
```

使用分隔符进行字符串切割/拼接（AppleScript's text item delimiters）

```
# 按分隔符将字符串分割为列表
set myString to "Hi there."
set oldDelimiters to AppleScript's text item delimiters  # 保存AppleScript's text item delimiters原有值
set AppleScript's text item delimiters to " "  # 将分隔符修改为空格
set myList to every text item of myString  # 按字符串逐个文本切割为数组
set AppleScript's text item delimiters to oldDelimiters  # 还原分隔符原有值
get myList  # 输出{"Hi", "there."}

# 使用分隔符将数组拼接为字符串
set listA to {"a", "b", "c", "d", "e", "f", "g", "h"}
set oldDelimiters to AppleScript's text item delimiters  # 保存AppleScript's text item delimiters原有值
set AppleScript's text item delimiters to "~~"  # 将分隔符修改为"~~"
set myList to listA as string  # 将数组转换为字符串
set AppleScript's text item delimiters to oldDelimiters  # 还原分隔符原有值
get myList  # 输出 "a~~b~~c~~d~~e~~f~~g~~h"
```

#### **（4）列表 List**

实际上就是数组，通过大括号包含多个数据项表示（注意不是括号）：

```
set myList to {12.4, 34, "Rose", "Hello world"}
set listLength to the length of {"a","b","c"}  # 获取列表长度，输出3
set listLength to the count of {"a","b","c"}  # 获取列表长度的另一种写法，输出3
```

列表可以通过&进行拼接（注意拼接的第一个必须为数组）：

```
# 多个拼接
set a to {"a"}
set b to {"b"}
set c to {"c"}
set d to a & b & c  # 输出 {"a", "b", "c"}
# 追加元素
set a to {"a"}
set c to a & "b"  # 输出{"a", "b"}
# 追加元素的另外写法
set listA to {1, 2, 3, 4}
set the end of listA to 5
get listA  # 输出{1, 2, 3, 4, 5}
# 如果第一个不是数组而是字符串，则拼接结果为字符串
set a to {"a", "b"}
set c to "c" & a  # 输出"cab"
```

进行列表元素获取

```
# 获取元素
set listA to {"a", "b"}
set secondItem to item 2 of listA  # 获取第二个元素，输出"b"
set lastItem to item -1 of listA  # 获取最后一个元素, 输出"b"
set lastItem to the last item of listA  # 获取最后一个元素的不同写法

# 获取指定范围的列表
set listA to {"a", "b", "c", "d", "e", "f", "g", "h"}
set rangeItems to items 2 through 5 of listA  # 获取第2个至第5个之间的列表，输出{"b", "c", "d", "e"}
set rangeItems to items 5 through 2 of listA  # 与上面的输出结果一样，并不会反向输出
```

进行列表元素值替换

```
set listA to {"a", "b"}
set item 2 of listA to "c"  # 将第2个元素替换为“c”
set the second item of listA to "c"  # 同样替换功能的不同写法
set the 2nd item of listA to "c"  # 同样替换功能的不同写法
get listA  # 输出 {"a", "c"}
```

使列表元素反向排序

```
set reversedList to reverse of {3, 2, 1}  # 输出{1, 2, 3}
```

类型转换

```
set b to "ab" as list  # 字符串转换为列表, 输出{"ab"}

# 将字符串转换为列表后进行拼接
set a to {"a"}
set c to ("b" as list) & a

# 字符串按字符转换为列表
set itemized to every character of "I'm Rose."  # 输出 {"I", "'", "m", " ", "R", "o", "s", "e"}

# 列表转换为字符串
set listA to {"a", "b", "c", "d", "e", "f", "g", "h"}
set listA to listA as string  # 输出“abcdefgh”
```

#### **（5）记录 record**

实际上就是字典，用大括号包含的键值对

```
set friend to {age:10, nickName:"张三"}
```

注意记录中的单元叫做属性（property），不是元素（item），不能通过item来取出数据，访问属性的示例如下：

```
set friend to {age:10, nickName:"张三"}
set propertyCount to count of friend  # 获取记录属性数量，输出2
set temp to age of friend  # 访问记录中age的属性值，输出10
set age of friend to 20  # 将记录的age值修改为20
```

记录的变量赋值传递的是引用地址，因此两个变量指向的是同一个记录，如果改变值一起变：

```
set recordA to {age:30}  # recordA记录的是记录的引用地址
set resultA to recordA  # 将recordA对应的引用地址（也就是记录的地址）赋值给resultA
set age of recordA to 50  # 修改记录的值
get resultA  # 由于对应的是同一个引用地址，值一起发生变化，输出{age:50}
```

如果我们需要通过一个记录生成一个新的记录（地址不同），可以用copy...to...

```
set recordA to {age:30}
copy recordA to resultA  # 将recordA对应的记录赋值成一个新的记录赋值给resultA
set age of recordA to 50  # 修改recordA对应的记录
get resultA  # 新的记录不发生改变，输出{age:30}
```

可以将记录的每个属性值转换为列表

```
set a to {age:10, nickName:"张三"}
set b to (a as list)  # 输出{10, "张三"}
```

对记录进行遍历处理

```
# 在Stack Overflow中看有如下方法，引入了OC中的Foundation库，实现了record的遍历
use framework "Foundation"
set testRecord to {a:"aaa", b:"bbb", c:"ccc"}

set objCDictionary to current application's NSDictionary's dictionaryWithDictionary:testRecord
set allKeys to objCDictionary's allKeys()

repeat with theKey in allKeys
    log theKey as text
    log (objCDictionary's valueForKey:theKey) as text
end repeat
```

### 4、运算符

#### **（1）算数运算符**

 加+、减-、乘*、除/、乘方^

```
set add to 3.1+4 -- 输出7.1
set sum to 3^3  -- 输出27
```

#### **（2）&运算符**

用于合并字符串、合并数组

```
set str to "hello world"
set str2 to "good morning "
set str3 to str2 & str
```

#### **（3）\转义字符**

 当字符串中有引号时，通过转移字符转义处理：

```
set str6 to "他说:\"你好！\""
display dialog str6
```

如果字符串要显示“\”时，再加一个反斜杠

```
set str6 to "\\他说:\"你好！\""
display dialog str6
```

#### **（4）比较运算符号**

**数值的比较**

等于：=或is或is equal to
不等于：/=或≠或is not
大于：>或is greater than
小于：<或is less than
大于等于：>=或is greater than or equal to
小于等于：<=或is less than or equal to
不大于：is not greater than
不小于：is not less than

```bash
set num1 to 5
if num1 /= 4 then
    display dialog "不相等"
end if
```

**字符串的比较**

```
begins with (or, starts with)  以……开头
ends with                    以……结尾
is equal to                  一致
comes before                 在……之前（对字符串逐字母比较，区分大小写）
comes after                  在……之前（对字符串逐字母比较，区分大小写）
is in                       在……之中
contains                     包含
```

反义方式（如果是is开头的，变为is not开头；其他加上does not作为开头）：

```dart
does not start with 不以……开头
does not contain    不以……结尾
is not in          不在……之内
...
```

通过ignoring white space块指示比较时忽略空格，例如：

```
set stringA to "Ja c k"
set stringB to "Jack"
ignoring white space
    if stringA = stringB then beep  # 忽略空格后相等，输出哔一声
end ignoring
```

通过 considering case 在比较时考虑字符大小写（**注意：默认比较会忽略大小写**）

```
"BOB" = "bob" --result: true
considering case --考虑大小写
    "BOB" = "bob" --result: false
end considering
```

**列表的比较**

```
begins with 以……开头
ends with   以……结尾
is equal to 一致
is in       在……之中
contains    包含
```

示例：

```swift
set listA to {"a", "b", "c"}
if "a" is in listA then
    set c to 123  # 输出123
else
    set c to 456
end if
```

**记录的比较**

```
is equal to(也可以使用 =)    一致
contains                  包含
```

示例：

```
set recordA to {name:"Jack", age:20}
-- name of recordA is "Jack"
if recordA contains {name:"Jack"} then
    set c to 123  # 输出123
end if
```

#### **（5）逻辑运算符**

 and  与，or  或，not  非

```
# 赋值
set a to true
set b to not true
set c to "a" = "b"
set d to not ("a" = "b")
# 作为if的条件
set num1 to 5
set num2 to 4
if num1 /= 4 and num2 is 4 then
    display dialog "满足"
end if
```

### 5、循环与逻辑分支

#### （1）条件语句

```
# if ... else ... 模式
if [condition] then
    -- do something
else
    -- do something
end if

# 单行模式
if [condition] then [do something]
```

#### （2）循环语句

重复指定次数（repeat ... times）

```
set repetitions to 2
-- repeat 2 times
repeat repetitions times
    say "Hello world!"
end repeat
```

按条件执行（repeat while [condition] 及 repeat until [condition]）

```
set isRun to false
-- until 与 while 判断结果相反
-- while为当满足条件时执行，until为当满足条件时停止执行
repeat while isRun is false  # 当isRun为false时执行
    say isRun
end repeat
```

按步执行，类似for（repeat with [varName] from [start] to [end] by [stepLength]）

```
# 为i赋值1-5分别执行
repeat with i from 1 to 5
    say i
end repeat

# 可以设置步骤的间隔长度为2
repeat with i from 1 to 5 by 2
    say i
end repeat
```

循环遍历列表（repeat with [itemName] in [itemList]）

```
repeat with aItem in itemList
	...
end repeat
```

**注：在循环中，可以通过exit repeat跳出循环（相当于break）。**

### 6、异常处理

```
# 忽略异常
try
	word 5 of "one two three"
end try

# 处理异常但不抛出
try
	word 5 of "one two three"
on error
	log "There are not enough words."
end try

# 处理异常，并抛出自定义异常（通过 error）
try
    word 5 of "one two three"
on error
    error "There are not enough words."
end try
```

### 7、函数定义和执行

**括号传参形式的函数定义**

```
# 不带参数的函数定义
on helloWorld()
    display dialog "Hello World"
end

helloWorld() -- Call the handler

# 复杂函数定义
# 带位置参数（可指定数据类型，注意指定数据类型在10.10版本以上才支持），位置参数可以支持列表形式的参数（w，h可以直接调用）
# 带字典（record）方式的参数（注意定义中value值不是默认值，而是参数的引用名），调用时字典key值无需按顺序，传入不存在的参数也不会报错
# 带返回值
on test(x as integer, y, {w, h}, {para1:n, para2:s})
	log ((("x:" & x as text) & " y:" & y as text) & " w:" & w as text) & "h:" & h as text
	log ("para1:" & n as text) & " para 2:" & s
	return x
end test

set _size to {3, 4}
test(1, 2, _size, {para2:"change para2", para1:1, no_para:""})  -- 调用函数
```

**无括号传参形式的函数定义**

```
# 只有一个位置参数的函数定义，其中radius为入参
on areaOfCircleWithRadius:radius
	log radius ^ 2 * pi
end areaOfCircleWithRadius:

# 调用函数，需要用its或it的形式指定
its areaOfCircleWithRadius:5
tell it to areaOfCircleWithRadius:5

# 具有多个位置参数的函数定义，其中w,h,l为入参
# 无括号传参方式的函数定义并不灵活，只支持按位置入参的情况，实际上最重会转为带括号传参的形式执行
# 例如以下函数将转换为areaOfRectangleWithWidth_height_len(w, h, l)
on areaOfRectangleWithWidth:w height:h len:l
	log w * h
	log l
end areaOfRectangleWithWidth:height:len:

its areaOfRectangleWithWidth:10 height:5 len:4
```

**语意方式的函数定义(仅支持一个入参)**

```
# 以下定义实际函数名为rock，around是入参的参数名，clock是入参的引用值
on rock around the clock
	display dialog (clock as text)
end rock

rock around the current date -- call handler to display current date

# 上面例子的the只是为了自然语言通顺的助词，实际上去掉执行效果一样
on rock around clock
	display dialog (clock as text)
end rock

rock around the current date -- 增加或减少the并不会影响最后的效果
rock around current date -- call handler to display current date
```



### 8、脚本对象（Script Objects）

简单脚本定义和执行

```
-- 定义脚本对象
script testScript
    log "test script"
end script

run testScript  # 执行脚本对象
```

定义包含属性和执行函数的脚本（可以理解为类）：

```
script John
    property HowManyTimes:0  # 定义内部属性，用于计数

		# 执行函数，someone为入参
    to sayHello to someone
        set HowManyTimes to HowManyTimes + 1
        say "Hello " & someone
        return "Hello " & someone
    end sayHello

end script

# 通过 tell 声明执行函数
tell John to sayHello to "Herb"
John's sayHello to "Jake"  # 第二种声明执行方法
sayHello of John to "Jake"  # 第三种声明执行方法

# 访问脚本的属性
get HowManyTimes of John
get John's HowManyTimes  # 访问属性的另外一种写法
```

在函数中返回脚本对象

```
on makePoint(x, y)
    script thePoint
        property xCoordinate:x
        property yCoordinate:y
    end script
    return thePoint  # 返回在函数中定义的脚本对象
end makePoint

set myPoint to makePoint(10,20)  # 执行函数得到脚本对象
get xCoordinate of myPoint  # 访问脚本对象的值，输出10
get yCoordinate of myPoint  # 访问脚本对象的值，输出20
```

脚本的继承：

```
# 父脚本定义，内部定义了两个函数
script Alex
    on sayHello()
        return "Hello, " & getName()
    end sayHello
    on getName()
        return "Alex"
    end getName
end script
 
# 继承脚本定义
script AlexJunior
    property parent : Alex  # 设置 parent 属性指定父脚本对象
    
    # 定义相同名字的函数，覆盖父脚本函数
    on getName()
        return "Alex Jr"
    end getName
end script
 
-- Sample calls to handlers in the script objects:
tell Alex to sayHello() --result: "Hello, Alex"
tell AlexJunior to sayHello() --result: "Hello, Alex Jr."
 
tell Alex to getName() --result: "Alex"
tell AlexJunior to getName() --result: "Alex Jr"
```

### 9、其他实用语法

**代码换行**

为了易于阅读，可用 “¬” 字符 ( option+l ) 进行换行展示，这样可以把一行脚本分成多行编写：

```
display dialog "This is just a test." buttons {"Great", "OK"} ¬
default button "OK" giving up after 3   --默认选中OK按钮，3s后弹窗消失
```

**it 和 me**

it 和 me用于在不同代码块中引用对象，me用于引用脚本本身，it用于引用当前块的目标，例如：

```
property name : "me script"

tell application "Safari"
	# 获取整个脚本的name属性
	log (get name of me)
	log me's name
	# 获取当前块目标对象（application）的name属性
	log (get name of it)
	set a to its name
	log a
end tell
```

**定义对象别名（use）**

通过定义对象的别名，可以不使用 tell 设置当前对象的方式执行脚本

```
use Safari : application "Safari" # 定义应用对象的别名
set the URL of the front document of Safari to "https://www.baidu.com" # 通过别名访问应用，设置URL地址
set Ver to Safari's version # 通过别名访问应用，获取应用版本
log (Ver) # 打印版本
```

use也可以指定为后面上下文特定对象环境

```
use application "Safari"  # 指定当前环境的默认应用
search the web for "AppleScript"  # 执行默认应用的对应动作
```

**对象集合遍历（every）**

every用于遍历对象的子类清单，后面紧跟的是类名

```
# 通过every遍历列表
set a to {"a", "b", "c"}
repeat with _str in (every item of a)
	log _str
end repeat

# 通过every遍历记录的值
set a to {a:"a1", b:"b1", c:"c1"}
repeat with _str in (every item of a)
	log _str
end repeat

# 通过every遍历窗口对象
tell application "Safari"
	repeat with _win in (every window)
		...
	end repeat
end tell
```



## 常用动作索引

| 命令                                 | 说明                                                  | 示例                                                         |
| ------------------------------------ | ----------------------------------------------------- | ------------------------------------------------------------ |
| activate                             | 把应用激活到前端，如果应用没有打开将会打开应用        | `activate application "TextEdit"` 或 `tell application "TextEdit" to activate` |
| log "text"                           | 日志方式输出字符串信息，格式为： `“(*要输出的信息*)”` | log "输出文本信息"                                           |
| say "text"                           | 通过语音方式读出字符串信息                            | say "hello world"                                            |
| delay [seconds]                      | 暂停指定的时间（秒）                                  | delay 0.5                                                    |
| beep [times]                         | 响提示声音，不带数字默认响一次，可以带数字连续响多声  | Beep 10                                                      |
| display dialog "消息" buttons [list] | 弹出对话框，后面可以带buttons指示按钮列表             | display dialog "消息" buttons {"ok", "cancle"}               |
|                                      |                                                       |                                                              |
|                                      |                                                       |                                                              |
|                                      |                                                       |                                                              |
|                                      |                                                       |                                                              |
|                                      |                                                       |                                                              |



## 鼠标键盘操作

### 模拟键盘操作

**1、keystroke**

模拟输入一串字符串，可以是英文也可以是中文。

```
keystroke "模拟输入字符"  # 模拟输入字符串
```

**2、key code**

`key code <code>`主要用于单键模拟，适用于键盘上的任意按键，例如像 esc 这样的非字符按键。需注意键入操作必需在 System Events 内进行。

```
tell application "System Events"
	key code 53  # 模拟输入esc按键（key code为53）
end tell
```

完整的键盘编码参考：https://eastmanreference.com/complete-list-of-applescript-key-codes

如果需要组合⌘Command、⇧Shift、⌥Option、⌃Control 等修饰键一起输入，可以按以下方式处理：

```
tell application "System Events"
	key code 9 using {command down}  # 9是V的键值，命令等于粘贴快捷键⌘Command - V
	key code 123 using {control down, option down, command down}  # 同时按下left+control+option+command
end tell
```

### 模拟鼠标操作

待研究



## 路径操作

choose folder 选择文件夹（弹出选择框），路径的格式为 "硬盘:文件夹:子文件夹:子文件夹"，下面得到的结果类似 `alias "Macintosh HD:Users:lhj:Library:Mobile Documents:com~apple~ScriptEditor2:Documents:"` ,

```
choose folder  # 弹出文件夹选择框，返回选择的文件夹路径
```

choose file 选择文件（弹出选择框）

```
choose file # 弹出文件选择框，返回选择的文件路径
```

choose application 选择应用（弹出选择框）

```
# 直接选择和启动应用
choose application

# 选择应用并返回应用路径
set a to choose application as alias  --result: alias "Leopard:System:Library:CoreServices:Finder.app:"
```

打开文件夹

```
tell application "Finder"
    open folder "Macintosh HD:Users:lhj:opensource:DevStandards:docs:test:"
end tell
```

打开文件（可以用两种不同路径格式）

```
tell application "Finder"
	open file "Macintosh HD:Users:lhj:opensource:DevStandards:docs:test:android测试-解决adb无法获取动态页面布局xml的问题.md"
	open POSIX file "/Users/lhj/opensource/DevStandards/docs/test/android测试-解决adb无法获取动态页面布局xml的问题.md"
end tell
```

使用alias替身指定路径并赋值给变量，这样变量存储的是文件的id，好处是即使文件被移动或改名，仍然能通过id访问到文件：

```
tell application "Finder"
	set filePath to alias "Macintosh HD:Users:lhj:opensource:DevStandards:docs:test:android测试-解决adb无法获取动态页面布局xml的问题.md"
	open file filePath
end tell
```

POSIX路径和AppleScript路径的转换

```
set a to "/Users/lhj/opensource/DevStandards/docs/test/android测试-解决adb无法获取动态页面布局xml的问题.md"
set b to POSIX file a as string  # 转换为AppleScript路径
set c to POSIX path of b  # 将AppleScript路径转换为POSIX路径
```

移动文件

```
tell application "Finder"
    move file "Macintosh HD:Users:lhj:Desktop:test.h" to trash  # 移动文件到垃圾桶，删除
end tell
```

读取文本文件

```
tell application "Finder"
    set thePath to alias "Macintosh HD:Users:lhj:Desktop:ABC:record.txt"
    read thePath
end tell
```

创建文件夹

```
tell application "Finder"
	make new folder at desktop with properties {name:"TTT"}  # 在桌面下创建一个名为TTT的新文件夹
	# 在指定路径下创建名为TTT的新文件夹
	set destPath to alias "Macintosh HD:Users:lhj:opensource:DevStandards:docs:test:"
	make new folder at destPath with properties {name:"TTT"}
end tell
```

获取文件列表

```
tell application "Finder"
    -- 每种获取的都是不同的
    every file of desktop
    files of desktop
    every folder of desktop
    folders of desktop
    name of every file of desktop
end tell
```

提取符合条件的文件夹

```
tell application "Finder"
    every file of desktop whose name contains "cu"
end tell
```

获取Finder的当前路径

```
tell application "Finder"
    if exists Finder window 1 then
        set currentDir to target of Finder window 1 as alias
    else
        set currentDir to desktop as alias
    end if
end tell
return POSIX path of currentDir
```



## AppleScript Suite

#### 介绍

AppleScript Suite (AppleScript套件)，就是 AppleScript 类（class），及其元素（element）和属性（property）的集合。

一个类，可以是一个数据，比如 Safari HTML 文档（`document`）；也可以是一个函数，帮你完成一个特定功能，比如往 OmniFocus 里添加任务这个动作（`parse tasks into`）。

一个类中可能包含元素和属性，比如 `name` 是 `document` 的一个属性，代表 `document` 的名称。

我们可以在脚本编辑器的词典中找到每一个安装程序的 AppleScript Suite 的定义信息，以Safari为例子，我们看到左边框的Standard Suite是标准suite，即所有应用都具备的，Safari suite是 Safari 独有的suite；中间框有对应suite的动作（可执行）和类；右边边框是类包含的元素和属性；底下是具体的说明文档，用于了解如何执行或访问。

<img src="MacOS%E6%B5%8B%E8%AF%95-AppleScript%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0.assets/003.png" alt="003" style="zoom:50%;" />



#### suite说明文档解析

接下来介绍一下如何使用suite，首先要看懂说明文档。

<img src="MacOS%E6%B5%8B%E8%AF%95-AppleScript%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0.assets/004.png" alt="004" style="zoom:50%;" />

以上是动作对应的说明文档，第一行标识符后面的 “v” 代表这是可执行的动作，后面是功能说明（打印文档）；第2行说明用法，可支持file、document、window这3种类或元素对象执行；第3、4行为动作执行可选参数，传递参数的调用方式如下：

```
...
# with 可传递值类型的参数，对于bool类型的参数，直接使用with或without跟参数名指定即可
print with properties {...} with/without print dialog
...
```

<img src="MacOS%E6%B5%8B%E8%AF%95-AppleScript%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0.assets/005.png" alt="005" style="zoom:50%;" />

以上是类或元素对应的说明文档，第一行标识符后面的 “n” 代表这是类或元素（不可执行），后面是说明；ELEMENTS部分说明这个元素是application元素的子元素；PROPERTIES部分说明这个元素包含的属性；RESPONDS TO部分说明这个元素可支持执行的动作。

#### suite使用示例

```
tell application "Safari"
	# 告诉Safari应用（设置 Safari application 对象下的环境）
	activate # 启动浏览器
	set the URL of the front document to "https://www.baidu.com" # 将当前文档的URL属性设置为要打开的网站
	tell window 1
	  # 告诉第一个窗口对象
		set webName to name of current tab  # 设置变量值为当前tab的name属性值
		log webName  # 打印属性
	end tell
end tell
```

#### 获取指定子对象的方式

```
tell application "Safari"
	set tabCount to count tab of window 1 # 获取第一个窗口的tab页数量, 通过数字模式指定第几个窗口
	log (get name of last tab of first window) # 通过first和last指定要获取的窗口和tab页
	log (get name of tab -1 of window 1) # 数字模式支持负数的方式
	log (get name of window "百度一下，你就知道") # 通过name值方式指定窗口
	set myId to id of window 1
	log (get name of window id myId) # 通过id的方式指定窗口
	set myRef to ref to window 1
	log (get name of myRef) # 通过设置引用变量的方式指向窗口
	
	# 遍历tab页对象，碰到当前可见tab页时跳出遍历
	repeat with i from 1 to tabCount
		set visibelTab to tab i of window 1
		if visible of visibelTab then
			log ("visible: " & visibelTab's name)
			exit repeat
		end if
	end repeat
	
	# 通过every来遍历的方式
	repeat with _tab in (every tab of window 1)
		if visible of _tab then
			log ("visible: " & _tab's name)
			exit repeat
		end if
	end repeat
end tell
```



## 操作应用的UI元素

可以通过AppleScript直接操作应用的界面UI元素，实现对应用的自动操作。要访问到要操作的UI元素，需要了解UI元素在应用中的层级架构，大体如下图所示（以应用为Money Pro为例）：

<img src="MacOS%E6%B5%8B%E8%AF%95-AppleScript%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0.assets/006.png" alt="006" style="zoom: 67%;" />



如果想要访问某一个 UI 元素，必须按上图中的层级结构，一层一层按顺序进行访问：System Events 是最外围的框架 → Money Pro（具体某个应用）→ window 1（该应用的第1个窗口）→ button 1（窗口中的第1个按钮）。

### 获取界面的所有元素

要找到要操作的UI元素，我们可以先获取整个应用内所有 UI 元素，然后缩小范围（比如该应用第 x 个窗口），再然后再凭直觉筛选出一些可能是目标元素的语句，逐个试验它们，最终定位目标 UI 元素。

我们可以通过以下命令获取应用当前可见的所有UI元素（注意是可见的，也就是对于未展示的菜单是找不到的，如果需要获取应该前面操作让菜单展示出来）：

```
tell application "System Events"  -- 注意，entire contents必须在"System Events"应用下才能正常执行
	tell process "Safari"
		entire contents -- 获取所有 UI 元素
	end tell
end tell
```

得到以下的所有元素列表信息

<img src="MacOS%E6%B5%8B%E8%AF%95-AppleScript%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0.assets/007.png" alt="007" style="zoom: 50%;" />

可以根据要找的信息逐步深入缩小范围，例如我们可以按元素层级展开查看：

```
tell application "System Events"
	tell window 1 of process "Safari"  # 查看process下的window元素的所有元素，再逐步放大
		entire contents -- 获取所有 UI 元素
	end tell
end tell
```

### 逐层遍历找到所需UI元素

entire contents方法可以查看到所有元素，但是没有办法直观看到元素的属性值，因此很难在大量的元素中筛选出自己要的元素，可以用以下脚本方式按层逐步查找：

```
-- 动态创建字典
on createRecord(pKey, pValue)
	set src to "on run paraList
		return {" & pKey & ": item 1 of paraList}
	end run"
	set myRecord to run script src with parameters {pValue}
	return myRecord
end createRecord

# 窗口信息查询
set propertyInfo to {}
tell application "System Events"
	tell window 1 of application process "Safari"  # 可以在这里逐层向下找
		repeat with i from 1 to (count of UI element)
			set myLable to "e" & i as text
			set myRecord to createRecord(myLable, properties of UI element i) of me
			set propertyInfo to propertyInfo & myRecord
		end repeat
		get propertyInfo
	end tell
end tell

# 带单信息查询，有4种菜单类，因此按4种类遍历
set propertyInfo to {}
tell application "System Events"
	tell menu bar 1 of application process "Safari" # 可以在这里逐层向下找
		set mbCount to count of menu bar
		if mbCount > 0 then
			set menuRecord to {item_count:mbCount} -- 登记数量
			# 组成每个子对象字典
			repeat with i from 1 to mbCount
				set myLable to "e" & i as text
				set myRecord to createRecord(myLable, properties of menu bar i) of me
				set menuRecord to menuRecord & myRecord
			end repeat
			# 添加到主信息
			set propertyInfo to propertyInfo & {|menu bar|:menuRecord}
		end if
		
		set mbCount to count of menu bar item
		if mbCount > 0 then
			set menuRecord to {item_count:mbCount} -- 登记数量
			# 组成每个子对象字典
			repeat with i from 1 to mbCount
				set myLable to "e" & i as text
				set myRecord to createRecord(myLable, properties of menu bar item i) of me
				set menuRecord to menuRecord & myRecord
			end repeat
			# 添加到主信息
			set propertyInfo to propertyInfo & {|menu bar item|:menuRecord}
		end if
		
		set mbCount to count of menu
		if mbCount > 0 then
			set menuRecord to {item_count:mbCount} -- 登记数量
			# 组成每个子对象字典
			repeat with i from 1 to mbCount
				set myLable to "e" & i as text
				set myRecord to createRecord(myLable, properties of menu i) of me
				set menuRecord to menuRecord & myRecord
			end repeat
			# 添加到主信息
			set propertyInfo to propertyInfo & {|menu|:menuRecord}
		end if
		
		set mbCount to count of menu item
		if mbCount > 0 then
			set menuRecord to {item_count:mbCount} -- 登记数量
			# 组成每个子对象字典
			repeat with i from 1 to mbCount
				set myLable to "e" & i as text
				set myRecord to createRecord(myLable, properties of menu item i) of me
				set menuRecord to menuRecord & myRecord
			end repeat
			# 添加到主信息
			set propertyInfo to propertyInfo & {|menu item|:menuRecord}
		end if
		
		get propertyInfo
	end tell
end tell
```

以Safari为例，通过多层搜索，可以找到地址输入框的元素位置为：UI element 2 of UI element 4 of UI element 2 of window 1 of process "Safari"，我们可以看到这样元素的属性：

```
-- 新建标签页按钮
tell application "System Events"
	tell UI element 6 of UI element 2 of window 1 of application process "Safari"
		get properties
	end tell
end tell

{minimum value:missing value, orientation:missing value, position:{1358, 25}, class:button, accessibility description:"新建标签页", role description:"按钮", focused:false, title:missing value, size:{35, 52}, help:missing value, entire contents:{}, enabled:true, maximum value:missing value, role:"AXButton", value:missing value, subrole:missing value, selected:missing value, name:missing value, description:"新建标签页"}

-- 地址栏输入框
tell application "System Events"
	tell UI element 2 of UI element 4 of UI element 2 of window 1 of process "Safari"
		get properties
	end tell
end tell

结果：
{minimum value:missing value, orientation:missing value, position:{491, 90}, class:text field, accessibility description:"地址和搜索", role description:"文本栏", focused:false, title:missing value, size:{488, 28}, help:missing value, entire contents:{}, enabled:true, maximum value:missing value, role:"AXTextField", value:"", subrole:missing value, selected:missing value, name:missing value, description:"地址和搜索"}
```

### 通过Accessibility Inspector查找UI元素

通过脚本方式查找存在较多不遍，实际上可以通过xcode中自带的一个检测工具Accessibility Inspector来进行可视化的查找。我们可以在Xcode->Open Developer Tool->Accessibility Inspector打开该工具, 该工具需要在Mac的安全性与隐私里边设置辅助功能的权限, 即允许该工具控制电脑. 

打开后,会发现该检测工具会一直悬浮在屏幕的最前端, 且能够检测到电脑屏幕上的所有界面的层级结构, 包括Mac中的应用, 浏览器, iOS APP等。将要查找的窗口置于最前端，然后点击工具的“瞄准”按钮，在窗口中点击选中要查找的元素即可。

<img src="MacOS%E6%B5%8B%E8%AF%95-AppleScript%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0.assets/008.png" alt="008" style="zoom: 50%;" />

选中元素后，可以查看到元素的属性值，如下图所示：

<img src="MacOS%E6%B5%8B%E8%AF%95-AppleScript%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0.assets/009.png" alt="009" style="zoom: 33%;" />

也可以看到对象在窗口中所处的层级关系，方便我们实际获取和操作对象，如下图所示：

<img src="MacOS%E6%B5%8B%E8%AF%95-AppleScript%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0.assets/010.png" alt="010" style="zoom: 50%;" />

注：有个更好用的第三方软件 UI Browser for Mac，可以更直观和清晰找到元素位置。

### 对UI元素进行操作

找到所需的UI元素以后，我们可以对元素进行操作，例如按钮和菜单元素我们可以进行鼠标点击操作，对文本元素可以编辑文本内容，示例如下：

```
-- 打开应用并把界面放到前台，目的只是为了展现效果，实际上只要应用被启动了，就算看不到页面也一样可以操作
tell application "Safari"
	activate -- 把应用激活并带到前台
	-- 检测应用是否已打开
	repeat until window 1 exists
		-- 直到 Safari 应用的一个窗口存在之前，不停循环检测
		delay 0.5
	end repeat
end tell

-- 对元素进行操作处理
tell application "System Events"
	-- 点击新建标签页按钮
	click UI element 6 of UI element 2 of window 1 of process "Safari"
	
	delay 2 -- 延迟2秒再进行下一个操作
	
	-- 地址栏输入网址并跳转
	tell UI element 2 of UI element 4 of UI element 2 of window 1 of process "Safari"
		set value of attribute "AXFocused" of it to true -- 让地址栏输入框具有焦点
		set value of it to "http://www.baidu.com" -- 输入网址
		key code 36 -- 按回车按钮
		log "finished"
	end tell
end tell
```



### 点击时间之间的延迟问题

MacOS为了保证点击UI元素的反馈能正常处理，在两次点击之间增加了5秒左右的延迟机制，因此正常情况下你没有办法快速进行两次UI元素的点击操作，可以通过以下的方案绕过该机制：

```
# 第一次点击
tell application "System Events"
    tell process "XXX"
        ignoring application responses --忽略应用的反馈
            click button 1 of window 1
        end ignoring
    end tell
end tell

-- 杀掉 System Events 应用
delay 0.1 --自定义 UI 反馈的等待时间为0.1 秒
do shell script "killall System\\ Events"

# 第二次点击
tell application "System Events"
    tell process "XXX"
        -- 第二次点击操作
    end tell
end tell
```

