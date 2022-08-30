# Java开发环境搭建-VSCode-MacOS-M1

## 安装JDK

1、支持M1版本的JDK，可以获取 zulu jdk，官方下载网站：https://www.azul.com/downloads/

2、我们的下载选择：Java 11 LTS，MacOS，ARM 64bit，JDK

3、获取到下载选项后，下载 .dmg的 安装版本

4、下载完成后双击文件安装即可

5、打开命令窗口，执行以下命令验证是否安装成功：java -version

**注：安装路径在 “/Library/Java/JavaVirtualMachines/zulu-11.jdk” ，如果要卸载，直接删除该目录即可“rm -rf /Library/Java/JavaVirtualMachines/zulu-11.jdk”**



## 安装Maven

1、官网下载地址：https://maven.apache.org/download.cgi

2、选择二进制编译包下载，例如：[apache-maven-3.8.4-bin.tar.gz](https://dlcdn.apache.org/maven/maven-3/3.8.4/binaries/apache-maven-3.8.4-bin.tar.gz)

3、把程序包放到任意目录下，例如：/Users/lhj/software

4、解压缩安装包

5、在命令行执行，编辑环境变量：

```
vi ~/.bash_profile

# 在文件结尾添加以下内容：
export MAVEN_HOME=/Users/lhj/software/apache-maven-3.8.4
export PATH=$PATH:$MAVEN_HOME/bin

# 生效配置
source ~/.bash_profile

注：如果命令行的环境配置文件是 .zshrc（MacOs默认），则应也编辑该文件增加上述配置
```

6、执行以下命令验证安装结果：mvn -v

7、设置阿里云镜像：

```
# 编辑配置
vi ${MAVEN_HOME}/conf/settings.xml

# 在<mirrors>下增加镜像的配置
<mirror>
  <id>alimaven</id>
  <name>aliyun maven</name>
  <url>http://maven.aliyun.com/nexus/content/repositories/central/</url>
  <mirrorOf>central</mirrorOf>
</mirror>
```



## VSCode设置

1、安装java支持扩展插件，直接在应用市场搜索和安装 “Extension Pack for Java” 即可（注：该插件包含了几个主要的java开发插件）；

2、安装spring boot支持扩展插件， 直接在应用市场搜索和安装“Spring Boot Extension”；

3、安装 “Lombok Annotations Support for VS Code” 扩展插件；



## 基本使用 - 创建 Maven 项目

### 创建项目

1、新建一个项目，点击文件夹图标，选择创建 Java 项目，然后点击 Maven create from archetype；

![image-20220303152202187](Java%E5%BC%80%E5%8F%91%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA-VSCode-MacOS-M1.assets/image-20220303152202187.png)

2、在弹出的对话框中选择一个生成项目的目录,接着选择基于 `maven-archetype-quickstart` 创建；

3、按提示选择版本（例如1.4），输入group_id（可以按默认），输入名称，选择项目文件夹等；

4、等待插件自动创建目录和文件，以及下载依赖包，注意中途可能会要求手工进行选择，留意命令窗口的提示并进行操作即可；

5、完成以后，再通过vscode打开项目所在目录，工程结构如下图：

![image-20220303153008398](Java%E5%BC%80%E5%8F%91%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA-VSCode-MacOS-M1.assets/image-20220303153008398.png)

### 运行和调试

1、通过调试按钮切换到调试面板（或快捷键`⌘+⇧+D`）,执行“运行和调试按钮”（或者按F5），可以调试当前代码文件（也可以先创建 launch.json文件，后续可以修改调试参数）：

<img src="Java%E5%BC%80%E5%8F%91%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA-VSCode-MacOS-M1.assets/image-20220303153258869.png" alt="image-20220303153258869" style="zoom:50%;" />

2、可以在命令窗口看到运行输出结果。



## 基本使用 - 创建 Spring Boot项目

### 创建项目

1、使用快捷键(Ctrl+Shift+P)命令窗口，输入Spring 选择创建 Maven 项目（Spring Initializr: Create a Maven Project...）；

2、参数依次选择 ”2.6.4“，”java“，设置包名和项目名，选择Jar；依赖选择Spring Web（启动Web服务）；

3、选择项目创建的目录，等待自动创建完成，然后在VSCode中打开项目目录；

### 编码

1、编辑 src/main/resources/application.properties 文件，增加以下配置：

```
# web监听端口
server.port=8088
```

2、创建以下路径下的java文件：src/main/java/com/example/demo/helloworld/controller/HelloWorldController.java

```
package com.example.demo.helloworld.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
@ResponseBody
public class HelloWorldController {

    @RequestMapping("/hello")
    public String hello() {
        return "Hello World";
    }
}
```

3、编辑 pom.xml 文件，在 build 配置中指定主类（configuration的配置）

```
...
  <build>
		<plugins>
			<plugin>
				<groupId>org.springframework.boot</groupId>
				<artifactId>spring-boot-maven-plugin</artifactId>
				<configuration>
          <mainClass>com.example.demo.DemoApplication</mainClass>
        </configuration>
			</plugin>
		</plugins>
	</build>
```

### 编译打包运行

1、命令窗口进入项目目录，执行打包操作：

```
# 清理包
mvn clean
# 打包
mvn install
```

2、命令窗口进入target目录，执行命令启动服务

```
java -jar demo-0.0.1-SNAPSHOT.jar
```

3、在浏览器打开以下网站，可以看到服务的输出：http://localhost:8088/hello



### 创建可供引入的 Spring Boot 工具 Jar 包

1、同样步骤创建一个Spring Boot项目；

2、创建以下路径下的java文件：src/main/java/com/example/demo/jarhelloworld/controller/HelloWorldController.java

```
package com.example.demo.jarhelloworld.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
@ResponseBody
public class HelloWorldController {

    @RequestMapping("/jar/hello")
    public String hello() {
        return "JAR Hello World";
    }
}
```

3、编辑 pom.xml 文件，在 build 配置中增加classifier为exec的配置，目的是让编译打包时可以形成2个jar包，一个是可执行包（包含执行入口，无法被其他spring boot项目引入），另一个是引入包（不包含执行内容，可以被其他spring boot项目引入）：

```
   <build>
		<plugins>
			<plugin>
				<groupId>org.springframework.boot</groupId>
				<artifactId>spring-boot-maven-plugin</artifactId>
				<configuration>
           <classifier>exec</classifier>
        </configuration>
			</plugin>
		</plugins>
	</build>
```

4、按通用编译打包方式进行编译，分别得到 provider-0.0.1-SNAPSHOT-exec.jar、provider-0.0.1-SNAPSHOT.jar 两个jar包，其中provider-0.0.1-SNAPSHOT.jar为引入包；

5、在需要引入jar的主项目（例如前面创建的项目）的 src/main/resources目录下创建 lib 目录，并把 provider-0.0.1-SNAPSHOT.jar 放到该目录下；

6、修改主项目的pom.xml文件，修改两个地方：

```
1、在dependencies中增加本地包的依赖配置，示例如下（注意scope必须为system）：
       <dependency>
            <groupId>com.service</groupId>
            <artifactId>provider</artifactId>
            <version>0.0.1-SNAPSHOT</version>
            <scope>system</scope>
            <systemPath>${project.basedir}/src/main/resources/lib/provider-0.0.1-SNAPSHOT.jar</systemPath>
        </dependency>
2、在build的plugins下增加includeSystemScope参数，用于打包时将该jar包纳入主项目中：
    <plugins>
			<plugin>
				<groupId>org.springframework.boot</groupId>
				<artifactId>spring-boot-maven-plugin</artifactId>
				<configuration>
					<mainClass>com.service.server.ServerApplication</mainClass>
					<includeSystemScope>true</includeSystemScope>
				</configuration>
			</plugin>
		</plugins>
```

7、修改主项目的 Application入口类，增加ComponentScan自动扫描注解（注意项目自身的注解也需要通过指定包位置的方式设置）：

```
...
@SpringBootApplication
@ComponentScan(value = "com.service.server.hello.controller")
@ComponentScan(value = "com.service.provider")
public class ServerApplication {

	public static void main(String[] args) {
		SpringApplication.run(ServerApplication.class, args);
	}

}
```

8、编译启动主项目后，可以分别通过/hello和/jar/hello访问不同的服务函数。



```
http://localhost:8088/server/hello
http://localhost:8088/provider/hello
http://localhost:8088/service/hello
http://localhost:8088/service/hello/call1
http://localhost:8088/service/hello/call2
http://localhost:8088/springservice/hello
http://localhost:8088/springservice/hello/call1
http://localhost:8088/springservice/hello/call2
```