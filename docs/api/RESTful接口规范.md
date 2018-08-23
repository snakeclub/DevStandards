# RESTful接口规范

引用参考：

[微服务RESTful 接口设计规范](https://blog.csdn.net/zl1zl2zl3/article/details/73867113)

[Restful 接口设计最佳事件](https://www.sohu.com/a/150966309_468627)

[RESTful 接口规范](https://www.cnblogs.com/aini521521/p/7777328.html)

[RESTful Service API 常见问题解决方案](https://www.cnblogs.com/catherine9192/p/9081778.html)

## RESTful简介

网络应用程序，分为前端和后端两个部分。当前的发展趋势，就是前端设备层出不穷（手机、平板、桌面电脑、其他专用设备......）。因此，**必须有一种统一的机制**，方**便不同的前端设备与后端进行通信**。这导致API构架的流行，甚至出现["APIFirst"](http://www.google.com.hk/search?q=API+first)的设计思想。[RESTful  API](http://en.wikipedia.org/wiki/Representational_state_transfer)是目前比较成熟的一套互联网应用程序的API设计理论。

REST（Representational State Transfer）表述性状态转换，**REST指的是一组架构约束条件和原则**。 如果一个架构符合REST的约束条件和原则，我们就称它为RESTful架构。**REST本身并没有创造新的技术、组件或服务**，而隐藏在RESTful背后的理念就是使用Web的现有特征和能力， 更好地使用现有Web标准中的一些准则和约束。虽然REST本身受Web技术的影响很深， 但是理论上REST架构风格并不是绑定在HTTP上，只不过目前HTTP是唯一与REST相关的实例。

在RESTful架构中，每个网址代表一种资源（resource），所以**网址中不能有动词，只能有名词**，而且所用的名词往往与数据库的表格名对应。一般来说，数据库中的表都是同种记录的"集合"（collection），所以API中的名词也应该使用复数。

## 协议

基于HTTP和HTTPS协议，考虑到服务的安全性，建议使用**HTTPS**作为API的通信协议。

注：你的应用不知道要被谁，以及什么情况访问。有些是安全的，有些不是。使用SSL可以减少鉴权的成本：你只需要一个简单的令牌（token）就可以鉴权了，而不是每次让用户对每次请求签名。

## 域名

建议将API部署在专有域名下，以此屏蔽消费者对服务提供方的部署细节（可借助于平台的反向代理+路由网关），**在服务地图丰富起来之后可以考虑多级域名**。

例：使用 https://api.example.com 替代 https://example.org/api/

## URL格式

URL统一格式规范为：http(s)://server.com/{app-name}/{version}/{domain}/{rest-convention}

### {app-name}

应用（系统）名，用于区分API属于哪个应用（系统），如果API无需区分应用（系统），该定义可取消。

{app-name} 示例：核心系统  -  cbs、网上银行 - wbs

### {version}

api的主版本信息（子版本信息在协议报文头中定义），用于区分所调用的版本，同时实现api的多版本支持。主版本信息为api版本号的第1段（例如v1）。

注：api版本号以v开头的3段式编号，第1段为大版本，当有不兼容改造（breaking）时，大版本应加1；第2段为中版本，当有新功能（feature）改造时，中版本应加1；第3段为小版本，当有bug修复时（fix），小版本应加1；例如v0.0.1。**原则上只要大版本一样，api接口必须可以向下兼容，即如果当前版本是v1.3.1，可以兼容支持v1.0.0的调用。**

### {domain}

可以用来定义任何技术的区域（例如：安全-允许指定的用户可以访问这个区域）或者业务上的区域（例如：同样的功能在同一个前缀之下）。

推荐使用{domain}域用于区分业务上的区域，例如用户管理应用上，通过{domain}域区分user（用户管理）、right（权限管理）的业务功能分类。

### {rest-convention}

代表这个域(domain)下，约定的资源名和对资源的处理参数，注意资源名应为名词且应为复数形式。

{rest-convention}的格式为有以下两种：

1、针对所有资源集合处理，无处理参数方式，直接就是资源名，例如 **/users**

2、针对指定id的某一指定资源处理，格式为"**resource_name/id**"，例如 **/users/10** （该方式也等同于 /users?id=10）

3、针对特定参数的资源处理，通过url的参数方式

- 格式为“**resource_name?para_name=para_value&para_name=para_value**”

- 参数命名采用下划线分隔形式

- 如果参数值中有+，空格，/，?，%，#，&，=等特殊符号时，需进行转义，按如下表格转：

  | 特殊符号 | URL中原字符的说明            | 转义后的字符 |
  | :------- | ---------------------------- | ------------ |
  | +        | URL 中+号表示空格            | %2B          |
  | 空格     | URL中的空格可以用+号或者编码 | %20          |
  | /        | 分隔目录和子目录             | %2F          |
  | ?        | 分隔实际的URL和参数          | %3F          |
  | %        | 指定特殊字符                 | %25          |
  | #        | 表示书签                     | %23          |
  | &        | URL 中指定的参数间的分隔符   | %26          |
  | =        | URL 中指定参数的值           | %3D          |

- 如果参数值中有中文（或全角字符）的时候，应对字符进行转码，示例如下：

  ```java
  String string = "蔡君如";
  String eStr = URLEncoder.encode(string, "utf-8");
  System.out.println(eStr);
  System.out.println(URLDecoder.decode(eStr, "utf-8"));
  
  输出：
  %E8%94%A1%E5%90%9B%E5%A6%82
  ```

- 标准参数名定义如下：

  | 参数名   | 说明                                  | 示例                               |
  | -------- | ------------------------------------- | ---------------------------------- |
  | id       | 指定资源唯一标识                      | id=10                              |
  | sort     | 返回结果根据指定字段升序、降序排序    | sort=-manufactorer,+model          |
  | fields   | 返回结果只获取指定的字段              | fields=manufacturer,model,id,color |
  | page     | 指定返回结果为分页的第几页（从1开始） | page=1                             |
  | pagesize | 指定分页的每页大小                    | pagesize=15                        |

4、针对多资源关联的处理，使用多级url的方式，例如：**/users/10/message/3** 表示id为10的用户下id为3的消息对象

5、针对api对资源的的操作，可以将这个操作看成某个资源的附属资源来设计，例如 **/users/10/star** 将加/减星操作看成users的附属资源，

```
对指定用户加星：
PUT /users/:id/star

对指定用户减星：
DELETE /users/:id/star
```



  ## http协议类型表达资源操作

HTTP协议里的8种方法，及其他衍生方法，常用的GET、POST**可以间接的实现其余所有的操作**，根据框架和浏览器的兼容性选择性使用。

  GET（SELECT）：从服务器取出资源（一项或多项）

  POST（CREATE）：在服务器新建一个资源

  PUT（UPDATE）：在服务器更新资源（客户端提供改变后的完整资源）

  DELETE（DELETE）：从服务器删除资源

  HEAD：获取资源的帮助信息链接（json，格式见后续章节）

  OPTIONS：获取资源所支持的方法及url参数（json，格式见后续章节）

  TRACE：回显服务器收到的请求，主要用于测试或诊断（json，格式见后续章节）

  CONNECT：HTTP/1.1协议中预留给能够将连接改为管道方式的代理服务器（暂未定义）

注：所有方法均需大写

## http协议报文头信息

### 通用报文信息定义

#### Content-Length

指定待传输的内容（报文实体）的字节长度，例如

```
Content-Length:731017
```

注：正常情况报文头信息都应该有Content-Length，但当报文头信息含有“**Transfer-Encoding: chunked**”时除外，这两个参数为互斥参数，当有“**Transfer-Encoding: chunked**”参数时，报文实体数据将会被分拆为多个包发送，不能确定实际传输的长度。



#### Content-Type

指定报文实体数据的类型，本规范仅支持以下两种类型：

| 数据类型                 | 说明           |
| ------------------------ | -------------- |
| application/json         | json格式字符串 |
| application/octet-stream | 二进制文件流   |

同时通过Content-Type的第2个参数**charset**可以指定报文实体数据的编码（json格式时），例如：

```
Content-Type: application/json;charset=utf-8
或
Content-Type: application/octet-stream
```



#### Transfer-Encoding: chunked

指定报文实体内容的传输形式，使用拆分为多个包的方式进行传输，该参数主要针对无法确定传输内容的实际大小的情况（按数据流处理），接收端不使用Content-Length来判断接收数据的结束，而是通过Chunked编码的结束包来判断。

**注：该报文头信息通常与Content-Encoding一并使用，其实就是针对 Transfer-Encoding 的分块再进行 Content-Encoding。**

Chunked编码使用若干个Chunk串连而成，由一个标明**长度为0**的chunk标示结束。每个Chunk分为头部和正文两部分，头部内容指定下一段正文的字符总数（**十六进制的数字**）和数量单位（一般不写），正文部分就是指定长度的实际内容，两部分之间用**回车换行(CRLF)**隔开。在最后一个长度为0的Chunk中的内容是称为last-chunk的内容，是一些附加的Header信息（通常可以直接忽略）。

具体的Chunk编码格式如下：

```
Chunked-Body = *chunk
　　　　　　　　　　last-chunk
　　　　　　　　　　trailer
　　　　　　　　　　CRLF
chunk        = chunk-size [ chunk-extension ] CRLF
　　　　　　　　　 chunk-data CRLF
chunk-size   = 1*HEX
last-chunk   = 1*("0") [ chunk-extension ] CRLF
chunk-extension= *( ";" chunk-ext-name [ "=" chunk-ext-val ] )
chunk-ext-name = token
chunk-ext-val = token | quoted-string
chunk-data = chunk-size(OCTET)
trailer = *(entity-header CRLF)
```



#### Content-Encoding: gzip

指定实体内容的传输压缩编码格式，对于大文本数据传输建议采用该参数对数据进行压缩后再传输，以提高传输的效率，接收端需对根据对应的编码方式进行解码处理。

本规范只支持gzip的压缩方式。



#### X-Cache-Key

对于需缓存当前步骤结果，待下一次处理仍需使用上一步处理结果的情况，使用X-Cache-Key标识缓存信息。使用场景举例如下：

1、资源查询分页情况

（1）客户端请求查询资源清单，采用分页；

（2）服务端生成查询清单数据到缓存（或记录所处位置），返回数据同时返回标识该缓存数据的标识，放入X-Cache-Key中

（3）客户端请求下一页，带上上一次查询返回的X-Cache-Key

（4）服务端根据X-Cache-Key找到缓存数据，继续返回下一页的数据





### 请求报文信息定义

#### X-Access_Token

restful API是无状态的也就是说用户请求的鉴权和cookie以及session无关，每一次请求都应该包含鉴权证明。通过使用ssl我们可以不用每次都提供用户名和密码：我们可以给用户返回一个随机产生的token。这样可以极大的方便使用浏览器访问API的用户。这种方法适用于用户可以首先通过一次用户名-密码的验证并得到token，并且可以拷贝返回的token到以后的请求中。

#### X-Sub-Version

子版本信息，指定使用api的特定中版本和小版本，格式为“中版本号.小版本号”。如果不传入子版本信息，则代表后台需调用url中大版本下的最新中版本和小版本api；可以通过"x"指定调用最新的小版本。

示例如下：

```
假设最新api版本为v1.3.2，以下指定调用v1.3.1版本：
X-Sub-Version: 3.1

以下指定调用v1.3下的最新版本:
X-Sub-Version: 3.x
```



### 返回报文信息定义

#### X-Total-Count

对于获取信息的情况，通过该定义返回资源的总记录数。



## http状态码

### 总体规则

1xx：指示信息--表示请求已接收，继续处理 

2xx：成功--表示请求已被成功接收、理解、接受 

3xx：重定向--要完成请求必须进行更进一步的操作 

4xx：客户端错误--请求有语法错误或请求无法实现 

5xx：服务器端错误--服务器未能实现合法的请求

### 具体定义

200 ok - 成功返回状态，对应，GET,PUT,DELETE.

201 created - 成功创建。

304 not modified - HTTP缓存有效。

400 bad request - 请求格式错误。

401 unauthorized - 未授权。

403 forbidden - 鉴权成功，但是该用户没有权限。

404 not found - 请求的资源不存在

405 method not allowed - 该http方法不被允许。

410 gone - 这个url对应的资源现在不可用。

415 unsupported media type - 请求类型错误。

422 unprocessable entity - 校验错误时用。

429 too many request - 请求过多。

HTTP 500 - 内部服务器错误



## 返回结果为统一的json格式

一方面，出于平台标准化的API管理，另一方面，遵循微服务的宽进严出设计理念，建议RESTful采用标准的Json格式。

示例如下：

```json
   {
       "className": "com.fiberhome.smartas.pricecloud.User",
       "id": "1b434wtert564564sdffey32",
       "name": "lilei",
       "age": 18,
       "job": {
            "className": "com.fiberhome.smartas.pricecloud.Job",
            "id": "1b434wtert564564sdffeyey",
            "name": "微服务架构师"
        }
    }
```



## 标准返回格式

### 获取帮助信息（HEAD）

当客户端发起的方法为HEAD时，服务器端应返回以下格式的帮助文档信息链接:

```
{
	"link":
        { 
            "document": "https://www.example.com/docs#zoos",
            "href": "https://api.example.com/zoos",
            "title": "List of zoos",
            "type": "application/json"
        }
}
```

### 获取资源支持的方法（OPTIONS）

当客户端发起的方法为OPTIONS时，服务器端应返回以下格式的资源所支持的方法信息，格式参考如下（支持的方法，方法对应支持的url参数清单）:

```
{
    "support": 
    	{
            "GET": ["id", "sort", "fields"],
            "POST": [],
            "PUT": []
    	}
}
```

### 回显发送端的请求信息（TRACE）

当客户端发起的方法为TRACE时，服务器端应返回以下格式的请求调用信息，格式参考如下

```
{
    "trace":{
		"url": "https://api.example.com/zoos?id=10",
		"http-head": {
        	"Content-Type": "application/json",
        	......
		},
		"http-body": "报文体字符串（如果是二进制流则为HEX串）"
    }
}
```



## 最佳实践

### 使用 token 机制设计鉴权和验证系统（Authorization and Authentication）

常见的场景就是用户系统-结合 OAuth2，参考腾讯云微视频MVS API，这里给出一个实用的解决方案：

- 用户使用户名密码或者第三方登录，最终请求一个我们设计的登录 API（这个 API 接受用户名密码，或第三方登录验证结果）；

- 服务端认证成功以后，生成一个 token，并将这个 token 和用户信息关联在一起，同时返回这个 token 给调用客户端；

- 客户端记录并保存下这个 token；

- 下次客户端发起和用户相关请求 API 都要在 http header 中带上这个 token；

- 服务端通过这个 token 去区分用户是谁，判断这个用户是否已经登录和有什么样的权限；

- 服务端也要考虑 token 的失效时间；

- 客户端在发现 token 失效的时候重新请求新的 token


![img](1.png)

为什么要多一个步骤使用 token 呢？为什么不直接把用户名和密码放在 http header 中直接做授权和验证？原因是调用 API 一般会被频繁调用，这样用户名和密码频繁在网络上传输，增加了泄漏的危险。如果使用token，即使泄漏了也不会暴露用户的密码，何况 token 也被经常被设计成有时间限制的，超时以后当前 token 就会失效，需要客户端重新做验证获得新的 token，暴露之后的影响很快就会过去。 

其实获取 token，用 token 做授权和验证和 OAuth 2 如出一辙，手法完全相同的，只是 OAuth 2 有更复杂的标准步骤去换取这个token，并且这个 token 的用途不同。OAuth 2 的 token 用来授权给第三方使用，我们自己设计的系统 token 仅限在自己系统本身 API 使用。



### 考虑启用 HTTP 缓存机制

 HTTP协议本身支持两种缓存机制: [ETag](https://link.jianshu.com/?t=http%3A%2F%2Fen.wikipedia.org%2Fwiki%2FHTTP_ETag) 和 [Last-Modified](https://link.jianshu.com/?t=http%3A%2F%2Fwww.w3.org%2FProtocols%2Frfc2616%2Frfc2616-sec14.html%23sec14.29)

 **ETag**：HTTP 请求中在 header 中包含一个内容的 hash，如果返回结果没有变化，该请求会直接返回304 Not Modified，而不是所有数据内容本身

**Last-Modified**: 和 Etag 工作原理差不多，只是使用时间戳作为内容是否过期的标志。

 

### 限制 API 调用频次（Rate limiting）

如果一个客户端请求 API 的频率太快，根据HTTP协议，可以返回[429 Too Many Requests](https://link.jianshu.com/?t=http%3A%2F%2Ftools.ietf.org%2Fhtml%2Frfc6585%23section-4)。 

如果要为客户端提供更加详细的调用频次和访问次数之类的信息，除了提供文档说明以外，还可以在 http header 用自定义字段的形式提供，比如 [Twitter API](https://link.jianshu.com/?t=https%3A%2F%2Fdev.twitter.com%2Frest%2Fpublic%2Frate-limiting) 是这样做的:
**X-Rate-Limit-Limit**: 该请求的调用上限
**X-Rate-Limit-Remaining**: 15分钟内还可以调用多少次
**X-Rate-Limit-Reset**: 还有多少秒之后访问限制会被重置

 

### 尽可能的使用 HTTPS，涉及用户验证的 API 一定要强制启用 HTTPS

HTTPS 现在已经是各种网络服务的标配（比如 Xcode 默认不允许请求不安全的 HTTP 信息）

如果你的WEB Server 是 Nginx，在部署了 HTTPS 的情况下，下面两个选项务必仔细设置，因为这个两个简单的设置可以很大程度上避免一些安全问题:

- ssl_prefer_server_ciphers： 表示服务端加密算法优先于客户端加密算法，主要是防止[降级攻击 （downgrade attack）](https://link.jianshu.com/?t=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FDowngrade_attack)。
- Strict-Transport-Security（HSTS）：告诉浏览器这个域名在指定的时间（max-age）内应该强制使用 HTTPS 访问。

