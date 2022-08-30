# Drools入门

**Drools**（JBoss Rules ）具有一个易于访问企业策略、易于调整以及易于管理的开源业务规则引擎。它提供一套商业规则引擎核心（Business Rules Engine  - BRE）。

官网地址：https://www.drools.org/



## Hello World

1、使用vscode创建一个新的Maven项目（command+shift+p），接着选择基于 `maven-archetype-quickstart` 创建，group_id为默认, 项目名为drools；

2、修改pom.xml文件，增加drools的maven依赖包，以及指定版本

```
...
<properties>
    ...
    <drools-version>7.66.0.Final</drools-version>
</properties>
...
<dependencies>
    ...
    <dependency>
      <groupId>org.drools</groupId>
      <artifactId>drools-core</artifactId>
      <version>${drools-version}</version>
    </dependency>
    <dependency>
      <groupId>org.drools</groupId>
      <artifactId>drools-compiler</artifactId>
      <version>${drools-version}</version>
    </dependency>
    <dependency>
      <groupId>org.drools</groupId>
      <artifactId>drools-templates</artifactId>
      <version>${drools-version}</version>
    </dependency>
</dependencies>
```

3、命令窗口进入项目目录，执行以下命令进行打包（从maven下载依赖包）：

```
# 清理包
mvn clean
# 打包
mvn install
```

4、在 src/main/resources/META-INF 目录下创建 kmodule.xml 文件：

```
<?xml version="1.0" encoding="UTF-8"?>
<kmodule xmlns="http://www.drools.org/xsd/kmodule">
    <kbase name="rules">
        <ksession name="all-rules"/>
    </kbase>
</kmodule>
```

注：这个文件是用来配置drools去哪里读取rules文件

5、创建 src/main/java/com/example/model/Person.java 类文件：

```
package com.example.model;

public class Person {

    public int age = 0;

    public void setAge(int age) {
        this.age = age;
    }

    public int getAge() {
        return this.age;
    }
}
```

6、创建 src/main/java/com/example/model/Car.java 类文件：

```
package com.example.model;

public class Car {
    public Person p;
    public int discount;

    public void setPerson(Person p) {
        this.p = p;
    }

    public Person getPerson() {
        return this.p;
    }

    public void setDiscount(int discount) {
        this.discount = discount;
    }

    public int getDiscount() {
        return this.discount;
    }

}
```

7、在 src/main/resources/com/rules 目录下创建 test.drl 规则脚本文件

```
package com.rules
import com.example.model.Car;
import com.example.model.Person;

rule "test-drool7-older than 60"

when
    $Car : Car( person.age > 60)
then
    $Car.setDiscount(80);
    System.out.println("test-drool7-older than 60"+$Car.getPerson().getAge());
end

rule "test-drool7-other"

when
    $Car : Car( person.age<=60)
then
    $Car.setDiscount(70);
    System.out.println("test-drool7-other"+$Car.getPerson().getAge());
end
```

8、编辑 src/main/java/com/example/App.java ，修改main函数，增加执行规则的代码：

```
package com.example;

import com.example.model.Car;
import com.example.model.Person;

import org.kie.api.KieServices;
import org.kie.api.runtime.KieContainer;
import org.kie.api.runtime.KieSession;

/**
 * Hello world!
 *
 */
public class App
{
    public static void main( String[] args )
    {
        System.out.println( "Hello World!" );
        KieServices kieServices = KieServices.Factory.get(); // 通过这个静态方法去获取一个实例
        KieContainer kieContainer = kieServices.getKieClasspathContainer();// 默认去读取配置文件
        KieSession kieSession = kieContainer.newKieSession("all-rules");// 根据这个名词去获取kieSession

        Person p1 = new Person();
        p1.setAge(30);
        Car c1 = new Car();
        c1.setPerson(p1);

        Person p2 = new Person();
        p1.setAge(70);
        Car c2 = new Car();
        c2.setPerson(p2);

        kieSession.insert(c1); // 将c1实例放入到session中,
        kieSession.insert(c2); //

        int count = kieSession.fireAllRules();// 开始执行规则,并获取执行了多少条规则
        kieSession.dispose();// 关闭session
        System.out.println("Fire " + count + " rule(s)!");
        System.out.println("The discount of c1 is " + c1.getDiscount() + "%");
        System.out.println("The discount of c2 is " + c2.getDiscount() + "%");
    }
}
```

8、对src/main/java/com/example/App.java执行调试，输入以下规则结果：

```
Hello World!
SLF4J: Failed to load class "org.slf4j.impl.StaticLoggerBinder".
SLF4J: Defaulting to no-operation (NOP) logger implementation
SLF4J: See http://www.slf4j.org/codes.html#StaticLoggerBinder for further details.
test-drool7-older than 6070
test-drool7-other0
Fire 2 rule(s)!
The discount of c1 is 80%
The discount of c2 is 70%
```

