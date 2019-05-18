# python库使用指引-peewee

[Peewee](http://docs.peewee-orm.com/en/latest/index.html) is a simple and small ORM. It has few (but expressive) concepts, making it easy to learn and intuitive to use.

- a small, expressive ORM
- python 2.7+ and 3.4+ (developed with 3.6)
- supports sqlite, mysql and postgresql
- [tons of extensions](http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#playhouse)

Peewee’s source code hosted on [GitHub](https://github.com/coleifer/peewee).

## 安装

最简单是用pi安装

```
pip install peewee
```

如果希望使用github源码安装

```
git clone https://github.com/coleifer/peewee.git
cd peewee
python setup.py install
```

Peewee包含两个可以被编译的C扩展库：

- Speedups她包含通过Cython重新实施的各种各样方法，如果你安装了Cython那么她可以自动被添加到库。
- Sqlite extensions她包含Cypthon
  SQlite日期操作函数的实现，正则运算，和全文搜索排序算法。这个模块可以通过命令build_sqlite_ext添加。

如果你想在git checkout里添加SQLite extension，你可以运行

```
# 构建sqlite扩展，并将共享库与其他模块一起放置。
python setup.py build_sqlite_ext -i
```

可选依赖关系

为使用peewee，你不需要任何额外的标准库，因为大部分的python发布版本都支持SQLite的编译。你可以通过在python控制台执行命令import sqlite3来测试。如果你想使用其他的数据库，有许多DB-API 2.0-compatible驱动，比如MySQL的pymysql和postgres的psycopg2。

- Cypthon:用于各种speedups。特别是在你使用SQLite时，可以极大的加速某些操作。 -
  apsw:可选的绑定SQLite第三方库，比标准库pysqlite具有更高的性能和更多更加清晰的语义，与APSWDatabase配合使用。
- pycrypto:用于AESEncryptedField. -
  bcrypt模块用于PasswordField. -
  vtfunc[<http://github.com/coleifer/sqlite-vtfunc>]用于为SQLite提供一些表值函数作为sqlite_udf扩展模块的一部分。
- gevent是SqliteQueueDatabase一个可选的依赖（虽然她很适用于threading） -
  BerkeleyDB:她与peewee一起使用可以编译一个SQLite前端。编译可能很棘手，所以可以看这里说明。



## 基本使用方法

```
# 引入包
from peewee import *

# 指定数据库
DATABASE = 'tweepee.db'
database = SqliteDatabase(DATABASE)

#############################
# 定义数据模型，可以通过pwiz命令生成模型代码
#############################
# 基础类，指定继承该类的表所属的数据库
class BaseModel(Model):
    class Meta:
        database = database

# User表的表结构
class User(BaseModel):
    username = CharField(unique=True)  # 指定字段为唯一索引
    password = CharField()
    email = CharField()
    join_date = DateTimeField()

# Relationship表的表结构，含外键及索引定义
class Relationship(BaseModel):
    from_user = ForeignKeyField(User, backref='relationships')
    to_user = ForeignKeyField(User, backref='related_to')

    class Meta:
        # 多字段索引的设置
        indexes = (
            (('from_user', 'to_user'), True),
        )

# Message表的表结构
class Message(BaseModel):
    user = ForeignKeyField(User, backref='messages')
    content = TextField()
    pub_date = DateTimeField()

#############################
# 连接及操作数据库
#############################
# 连接数据库
database.connect()

# 执行建表，只执行一次
with database:
	database.create_tables([User, Relationship, Message])

# 插入数据
try:
    # 自动提交模式
    with database.atomic():
        # 创建一条新的用户数据，如果用户名已被使用（唯一索引），数据库会返回IntegrityError异常
        user = User.create(
            username='username',
            password=md5('123456').hexdigest(),
            email='xxx@mail.com',
            join_date=datetime.datetime.now())
except IntegrityError:
    print('That username is already taken')

try:
    with database.atomic():
        Relationship.create(
            from_user=get_current_user(),
            to_user=user)
except IntegrityError:
    pass

# 链接表查询（join）
query1 = User
		 .select()
         .join(Relationship, on=Relationship.to_user)
         .where(Relationship.from_user == self)
         .order_by(User.username)

# 子查询
query2 = Message
            .select()
            .where(Message.user.in_(user.following()))
            .order_by(Message.pub_date.desc())

# 关闭数据库
database.close()
```



## peewee用法考察

原作者：yuchanns

链接：https://www.jianshu.com/p/182ea382b99f

### 前置准备

#### 在mysql中新建表

本文使用数据库名为peewee，三张表分别是user、balance和integral，结构如下：

```mysql
CREATE TABLE 'user' (
  'uid' int(11) NOT NULL AUTO_INCREMENT COMMENT '用户编号',
  'avartar' varchar(200) NOT NULL COMMENT '头像',
  'uname' varchar(50) NOT NULL COMMENT '用户名',
  'gender' char(1) NOT NULL DEFAULT '0' COMMENT '性别 0-保密|1-男|2-女',
  'password' varchar(200) NOT NULL COMMENT '密码',
  'balance' decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT '余额',
  'integral' int(11) NOT NULL DEFAULT '0' COMMENT '积分',
  'logintime' datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后登录时间',
  'addtime' datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
  PRIMARY KEY ('uid'),
  UNIQUE KEY 'uname' ('uname') COMMENT '用户名唯一'
) ENGINE=InnoDB AUTO_INCREMENT=10000 DEFAULT CHARSET=utf8 COMMENT='用户信息'
```

```mysql
CREATE TABLE 'balance' (
  'b_id' int(11) NOT NULL AUTO_INCREMENT COMMENT '操作编号',
  'uid' int(11) NOT NULL DEFAULT '0' COMMENT '用户编号',
  'change' decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT '变动金额',
  'total' decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT '剩余金额',
  'addtime' datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
  PRIMARY KEY ('b_id'),
  KEY 'uid' ('uid') COMMENT '用户编号'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='余额操作记录表'
```

```mysql
CREATE TABLE 'integral' (
  'i_id' int(11) NOT NULL AUTO_INCREMENT COMMENT '操作编号',
  'uid' int(11) NOT NULL DEFAULT '0' COMMENT '用户编号',
  'change' decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT '变动积分',
  'total' decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT '剩余积分',
  'addtime' datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
  PRIMARY KEY ('i_id'),
  KEY 'uid' ('uid') COMMENT '用户编号'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='积分操作记录表'
```

python连接mysql，需要pymysql或mysql-connector-python

```
pip install pymysql peewee
```

#### 生成映射模型

peewee分别提供**根据模型生成表**和**根据表生成模型**的功能。但peewee等orm要考虑兼容多种数据库，因此模型生成表的过程中只能使用所有数据库公有的字段类型，不能使用mysql的tinyint、char等类型，所以不考虑根据模型生成表。使用[pwiz](http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#pwiz)命令生成模型：

```
python -m pwiz -e mysql -H localhost -p3306 -uroot -P peewee > models.py
```

获得以下model文件：

```python
# -*- coding: utf-8 -*-
# models.py

from peewee import *

database = MySQLDatabase('peewee', **{'charset': 'utf8', 'use_unicode': True, 'host': 'localhost', 'port': 3306, 'user': 'root', 'password': ''})


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class Balance(BaseModel):
    addtime = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    b = AutoField(column_name='b_id')
    change = DecimalField(constraints=[SQL("DEFAULT 0.00")])
    total = DecimalField(constraints=[SQL("DEFAULT 0.00")])
    uid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = 'balance'


class Integral(BaseModel):
    addtime = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    change = DecimalField(constraints=[SQL("DEFAULT 0.00")])
    i = AutoField(column_name='i_id')
    total = DecimalField(constraints=[SQL("DEFAULT 0.00")])
    uid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = 'integral'


class User(BaseModel):
    addtime = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    avartar = CharField()
    balance = DecimalField(constraints=[SQL("DEFAULT 0.00")])
    gender = CharField(constraints=[SQL("DEFAULT '0'")])
    integral = IntegerField(constraints=[SQL("DEFAULT 0")])
    logintime = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    password = CharField()
    uid = AutoField()
    uname = CharField(unique=True)

    class Meta:
        table_name = 'user'
```

### Create

新建一个peewee_test.py文件，引入models，使用logging类库观察执行的sql语句。

#### 第一种添加方法

```python
# -*- coding: utf-8 -*-
# peewee_test.py

from models import *
import sys, logging, hashlib

# 使用日志观察执行的sql语句
logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


def create():
    """md5加密密码"""
    m = hashlib.md5()
    m.update('123456'.encode())
    pwd = m.hexdigest()
    """头像"""
    avartar = 'https://avatars2.githubusercontent.com/u/25029451'
    """第一种添加方法"""
    user = User(
        avartar=avartar, 
        uname='John', gender='1', password=pwd
    )
    uid = user.save()
    print('uid=%d' % uid)


if __name__ == '__main__':
    sys.exit(create())

```

运行peewee_test.py，查看控制台输出信息，我们得知第一种添加方法不会返回插入的自增pk（此时自增pk为uid=10000），而是成功返回1，失败返回0；

```
python peewee_test.py
('INSERT INTO `user` (`avartar`, `gender`, `password`, `uname`) VALUES (%s, %s, %s, %s)', ['https://avatars2.githubusercontent.com/u/25029451', '1', 'e10adc3949ba59abbe56e057f20f883e', 'John'])
uid=1

Process finished with exit code 0
```

#### 第二种添加方法

```python
def create():
    """第二种添加方法"""
    uid = User.create(
        avartar=avartar,
        uname='Jack', gender='1', password=pwd
    )
    print('uid=%s' % uid)
```

**注意**第二种方法中我打印uid使用格式化操作符是%s而不是%d，因为返回值是一个User对象
 查看控制台输出信息，可知第二种方法会返回自增pk；

```
python peewee_test.py
('INSERT INTO `user` (`avartar`, `gender`, `password`, `uname`) VALUES (%s, %s, %s, %s)', ['https://avatars2.githubusercontent.com/u/25029451', '1', 'e10adc3949ba59abbe56e057f20f883e', 'Jack'])
uid=10001

Process finished with exit code 0
```

#### 第三种添加方法

```
def create():
    """第三种添加方法"""
    uid = User.insert(
        avartar=avartar,
        uname='Micheal', gender='1', password=pwd
    ).execute()
    print('uid=%d' % uid)
```

查看控制台输出信息，第三种方法也会返回自增pk。

```
python peewee_test.py
('INSERT INTO `user` (`avartar`, `gender`, `password`, `uname`) VALUES (%s, %s, %s, %s)', ['https://avatars2.githubusercontent.com/u/25029451', '1', 'e10adc3949ba59abbe56e057f20f883e', 'Micheal'])
uid=10002

Process finished with exit code 0
```

**第一种需要调用save()方法才能插入数据，而第二种不需要调用其他方法，第三种则调用execute()方法进行插入。**第二种方法返回的是对象，第三种方法返回的是整型。工作中我经常需要在后续代码中使用到自增pk，因此我将采用insert()方法进行添加操作。

#### 批量添加方法

使用insert_many批量添加数据：在插入多条数据时，根据[文档描述](http://docs.peewee-orm.com/en/latest/peewee/querying.html#bulk-inserts)，create()方法每次都会开启事务（如果存储引擎支持），虽然可以遍历方式用上述方法逐条插入，但数据量一大就会导致效率低下，所以有必要进行批量插入优化。

```
If you are not wrapping the loop in a transaction then each call to create() happens in its own transaction. That is going to be really slow!
```

```python
def create():
    """批量添加数据"""
    data_source = [
        (avartar, 'Catherine', '2', pwd),
        (avartar, 'Jane', '2', pwd),
        (avartar 'Mary', '2', pwd),
    ]
    field = [User.avartar, User.uname, User.gender, User.password]
    uid = User.insert_many(data_source, field).execute()
    print('uid=%d' % uid)
```

控制台输出返回批量插入过程中第一条数据的自增pk；

```
python peewee_test.py
('INSERT INTO `user` (`avartar`, `uname`, `gender`, `password`) VALUES (%s, %s, %s, %s), (%s, %s, %s, %s), (%s, %s, %s, %s)', ['https://avatars2.githubusercontent.com/u/25029451', 'Catherine', '2', 'e10adc3949ba59abbe56e057f20f883e', 'https://avatars2.githubusercontent.com/u/25029451', 'Jane', '2', 'e10adc3949ba59abbe56e057f20f883e', 'https://avatars2.githubusercontent.com/u/25029451', 'Mary', '2', 'e10adc3949ba59abbe56e057f20f883e'])
uid=10003

Process finished with exit code 0
```

#### 批量块添加方法

如果要插入的数据量非常大，比如有千万条。一次性批量插入将会导致卡死，逐条插入也会导致耗时过长。此时可以折中寻求一个分批次批量插入的方案：使用peewee的chunked(it, n)方法将数据分割成小块数据（比如每次1000条，chunked(data_source, 1000)）分批次批量插入：

```
def create():
    """批量块添加数据"""
    data_source = [
        (avartar, 'Zoe', '2', pwd),
        (avartar, 'Lucy', '2', pwd),
        (avartar, 'Kara', '2', pwd),
        (avartar, 'Rex', '1', pwd),
    ]
    field = [User.avartar, User.uname, User.gender, User.password]
    for data_chunk in chunked(data_source, 2):
        User.insert_many(data_chunk, field).execute()
```

控制台输出的信息表明了chunked的实质：

```
python peewee_test.py
('INSERT INTO `user` (`avartar`, `uname`, `gender`, `password`) VALUES (%s, %s, %s, %s), (%s, %s, %s, %s)', ['https://avatars2.githubusercontent.com/u/25029451', 'Zoe', '2', 'e10adc3949ba59abbe56e057f20f883e', 'https://avatars2.githubusercontent.com/u/25029451', 'Lucy', '2', 'e10adc3949ba59abbe56e057f20f883e'])
('INSERT INTO `user` (`avartar`, `uname`, `gender`, `password`) VALUES (%s, %s, %s, %s), (%s, %s, %s, %s)', ['https://avatars2.githubusercontent.com/u/25029451', 'Kara', '2', 'e10adc3949ba59abbe56e057f20f883e', 'https://avatars2.githubusercontent.com/u/25029451', 'Rex', '1', 'e10adc3949ba59abbe56e057f20f883e'])

Process finished with exit code 0
```



### Update

#### 第一种更新方法

和添加操作一样，更新也有多种方法。当条件中包含了pk时，调用save()方法就是更新：

```python
def update():
    """第一种更新方法"""
    user = User(gender='1')
    user.uid = 1006
    user.save()
```

```
python peewee_test.py
('UPDATE `user` SET `gender` = %s WHERE (`uid` = %s)', ['1', 1006])

Process finished with exit code 0
```

#### 第二种更新方法

同insert()，改成update()就可以了，比第一种方法优越在于可以使用其他字段进行条件限定：

```python
def update():
    """第二种更新方法"""
    User.update(
        gender='2'
    ).where(User.uname == 'Zoe').execute()
```

```
python peewee_test.py
('UPDATE `user` SET `gender` = %s WHERE (`uname` = %s)', ['2', 'Zoe'])

Process finished with exit code 0
```



### Transaction

掌握了最基本的CUR操作后，我们终于可以进行一些更为高级的操作。比如很重要很常用并且是InnoDB比MyISAM更为优越的功能：事务操作。peewee提供了[两种事务开启的方法](http://docs.peewee-orm.com/en/latest/peewee/database.html?highlight=%40atomic#set-locking-mode-for-transaction)，这里只用第二种。
 首先，我们可以在models.py这个文件的BaseModel类中添加一个trans()方法，便于后面开启事务：

```python
# models.py
class BaseModel(Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trans = database.atomic

    class Meta:
        database = database
```

#### 开启事务的方法

```python
def transaction():
    user = User()
    """开启事务"""
    with user.trans():
        pass
```

在python中使用with开启的好处在于如果原子操作执行成功它可以自动提交、失败会自动回滚，不需要程序员手写提交和回滚代码，除此之外，视觉上更为优雅（*pythonic*）。当然如果你更习惯于完全手写也可以使用[database.manual_commit()](http://docs.peewee-orm.com/en/latest/peewee/api.html?#Database.manual_commit)的方法来开启手动提交回滚操作。

#### 应用情景

给*名为Jack*的用户添加*100.00余额*，同时需要在余额操作记录表上*插入一条记录*。两个操作必须全部成功，否则全部失败。

```python
def transaction():
    user = User()
    result = user.select(User.uid, User.balance).where(User.uname == 'Jack').get()  # 查询用户的现有余额以及用户编号
    """开启事务"""
    with user.trans():
        try:
            user.update(
                balance=result.balance+100
            ).where(User.uid == result.uid).execute()
            Balance.insert(
                uid=result.uid,
                change=100,
                total=result.balance+100
            ).execute()
        except Exception:
            print('更新失败')
        else:
            print('更新成功')
```

如果其中有一步操作失败，则整个事务自动回滚。

```
python peewee_test.py
('SELECT `t1`.`uid`, `t1`.`balance` FROM `user` AS `t1` WHERE (`t1`.`uname` = %s) LIMIT %s OFFSET %s', ['Jack', 1, 0])
('UPDATE `user` SET `balance` = %s WHERE (`uid` = %s)', [Decimal('100.00'), 10001])
('INSERT INTO `balance` (`change`, `total`, `uid`) VALUES (%s, %s, %s)', [100, Decimal('100.00'), 10001])
更新成功

Process finished with exit code 0
```



### Retrieve(1)

#### 读取单条数据

直接调用get()方法，可以添加过滤(filter)条件。查询结果是一个User对象，直接打印得到pk，通过调用成员变量可以获得对应字段的值。特别的，当筛选条件为pk时，可以使用get_by_id()方法直接查询：

```python
def retrieve():
    """读取一条数据"""
    # result = User.get_by_id(10000)
    result = User.get(User.uname == 'Jack')
    print('直接打印：%s' % result)
    """查看结构"""
    print('\n'.join(['%s:%s' % item for item in result.__data__.items()]))
    print('用户名为：%s' % result.uname)
```

控制台输出：

```
python peewee_test.py
('SELECT `t1`.`uid`, `t1`.`addtime`, `t1`.`avartar`, `t1`.`balance`, `t1`.`gender`, `t1`.`integral`, `t1`.`logintime`, `t1`.`password`, `t1`.`uname` FROM `user` AS `t1` WHERE (`t1`.`uname` = %s) LIMIT %s OFFSET %s', ['Jack', 1, 0])
直接打印：10001
uid:10001
addtime:2018-12-12 10:22:53
avartar:https://avatars2.githubusercontent.com/u/25029451
balance:0.00
gender:1
integral:0
logintime:2018-12-12 10:22:53
password:e10adc3949ba59abbe56e057f20f883e
uname:Jack
用户名为：Jack

Process finished with exit code 0
```

使用get()方法查询出来的数据包含了所有的字段。那么，当我们的需求是**查询单条数据中的限定字段(fields)**时，应该怎么查询呢？阅读get()方法的源码可以得知，其调用了select()方法返回的**ModelSelect类**中的get()方法：

```python
# peewee.py
@classmethod
def get(cls, *query, **filters):
    sq = cls.select()
    if query:
        sq = sq.where(*query)
    if filters:
        sq = sq.filter(**filters)
    return sq.get()
```

因此，我们可以直接调用select()方法，然后调用get()方法，就可以实现需求。

```python
def retrieve():
    """查询一条数据中的限定字段(uname)"""
    result = User.select(User.uname).where(User.uid == 10001).get()
    """查看结构"""
    print('\n'.join(['%s:%s' % item for item in result.__data__.items()]))
```

事实上，很多时候工作中遇到的单一查询都是只需要其中几个字段的数据，因此比起get()我用的更多的将会是select().get()。

```
python peewee_test.py
('SELECT `t1`.`uname` FROM `user` AS `t1` WHERE (`t1`.`uid` = %s) LIMIT %s OFFSET %s', [10001, 1, 0])
uname:Jack

Process finished with exit code 0
```

#### 读取多条数据

读取多条数据时，就要用到刚才提到的select()方法，这也是查询使用的主要方法。查阅select()方法源码可知，其返回一个**ModelSelect类**，然后我们再调用这个类的各种方法（where()、order_by()、limit()、offset()）来实现查询的条件限定。如果你有特殊的需求，可以在链式操作的最后调用dicts()方法，将结果转化为一个字典。例如，我们要查询*性别为男性*、按*注册日期降序*（升序写字段，降序在字段前面再加个负号）排列的*第二和第三位*用户的*编号和名称*：

```python
def retrieve():
    """读取多条数据"""
    query = User.select(User.uname, User.uid).order_by(-User.addtime).limit(2).offset(1).where(User.gender == '1')
    for row in query:
        print('%d:%s' % (row.uid, row.uname))
    """转换为字典形式"""
    print('转为字典形式：')
    query = User.select(User.uname, User.uid).order_by(-User.addtime).limit(2).offset(1).where(User.gender == '1').dicts()
    for row in query:
        print(row)
```

```
python peewee_test.py
('SELECT `t1`.`uname`, `t1`.`uid` FROM `user` AS `t1` WHERE (`t1`.`gender` = %s) ORDER BY `t1`.`addtime` DESC LIMIT %s OFFSET %s', ['1', 2, 1])
('SELECT `t1`.`uname`, `t1`.`uid` FROM `user` AS `t1` WHERE (`t1`.`gender` = %s) ORDER BY `t1`.`addtime` DESC LIMIT %s OFFSET %s', ['1', 2, 1])
10002:Micheal
10001:Jack
转为字典形式：
{'uname': 'Micheal', 'uid': 10002}
{'uname': 'Jack', 'uid': 10001}

Process finished with exit code 0
```



#### 查询表达式

根据[文档](http://docs.peewee-orm.com/en/latest/peewee/query_operators.html?highlight=where#query-operators)，peewee的查询操作符由以下组成：

| 比较符号 | 意义                      |
| -------: | :------------------------ |
|       == | x等于y                    |
|        < | x小于y                    |
|       <= | x小于等于y                |
|        > | x大于y                    |
|       >= | x大于等于                 |
|       != | x不等于y                  |
|       << | x在数组y中                |
|       >> | x是y，这个y是None或者Null |
|        % | x包含在y中                |
|       ** | 忽略大小写的x包含在y中    |
|        ^ | x异或y                    |
|        ~ | 非x                       |

举例，模糊查询*用户名包含J*的用户：

```python
def retrieve():
    """模糊查询用户名包含J的用户"""
    # 包含J结尾的查询条件
    # query = User.select(User.uname, User.uid).where(User.uname % '%J').dicts()
    # 包含J的查询条件
    # query = User.select(User.uname, User.uid).where(User.uname % '%J%').dicts()
    # 包含J开头的查询条件
    query = User.select(User.uname, User.uid).where(User.uname % 'J%').dicts()
    for row in query:
        print(row)
```

我们应该知道，模糊查询的时候使用右模糊查询可以有效地利用索引加快查询速度。

```
python peewee_test.py
('SELECT `t1`.`uname`, `t1`.`uid` FROM `user` AS `t1` WHERE (`t1`.`uname` LIKE BINARY %s)', ['J%'])
{'uname': 'Jack', 'uid': 10001}
{'uname': 'Jane', 'uid': 10004}
{'uname': 'John', 'uid': 10000}

Process finished with exit code 0
```

当然，因为操作符有限，无法表达全部功能，所以peewee同时也提供了方法用于代替操作符：

|                方法 | 意义                         |
| ------------------: | :--------------------------- |
|         .in_(value) | x在数组y中                   |
|       .not_in(value | x不在数组y中                 |
|   .is_null(is_null) | 判断是否为空，接受布尔值     |
|   .contains(substr) | 包含字符串，忽略大小写       |
| .startswith(prefix) | 以字符串开头，忽略大小写     |
|   .endswith(suffix) | 以字符串结尾，忽略大小写     |
| .between(low, high) | 在两个值的范围内             |
|        .regexp(exp) | 匹配正则表达式（大小写敏感） |
|       .iregexp(exp) | 匹配正则表达式，忽略大小写   |
|     .bin_and(value) | 二进制的和                   |
|      .bin_or(value) | 二进制的或                   |
|      .concat(other) | 将两个字符串或对象临时合并   |
|         .distinct() | 指定字段过滤重复记录         |
| .collate(collation) | 对列进行指定规则排序         |
|         .cast(type) | 将列的值按照指定类型转变     |

还是上面的查询例子，等效用方法进行查询可改为：

```
# 包含J结尾的查询条件
# query = User.select(User.uname, User.uid).where(User.uname.endswith('j')).dicts()
# 包含J的查询条件
# query = User.select(User.uname, User.uid).where(User.uname.contains('j')).dicts()
# 包含J开头的查询条件
query = User.select(User.uname, User.uid).where(User.uname.startswith('j')).dicts()
```

以及连接多个条件的逻辑运算符：

| 符号 | 意义 |
| ---: | :--- |
|    & | 且   |
|   \| | 或   |
|    ~ | 非   |



### Retrieve(2)

#### join

当我们查看操作记录的时候，往往需要用户信息和操作记录组合起来，也就是mysql的join操作。例如，我们要*时间降序*查询*用户编号为10001*的用户的*余额变更记录*：

```python
def retrieve2():
    """join查询"""
    query = Balance.select(
        User.uname, Balance.change,
        Balance.total, Balance.addtime
    ).join(
        User, JOIN.RIGHT_OUTER,
        on=(Balance.uid == User.uid)
    ).where(
        Balance.uid == 10001
    ).order_by(-Balance.addtime)
    for row in query:
        print('%s:%.2f:%.2f:%s' % (
            row.user.uname, row.change, row.total, row.addtime
        ))
```

```
python peewee_test.py
('SELECT `t1`.`uname`, `t2`.`change`, `t2`.`total`, `t2`.`addtime` FROM `balance` AS `t2` RIGHT OUTER JOIN `user` AS `t1` ON (`t1`.`uid` = `t2`.`uid`) WHERE (`t2`.`uid` = %s) ORDER BY `t2`.`addtime` DESC', [10001])
Jack:100.00:200.00:2018-12-12 17:24:32
Jack:100.00:100.00:2018-12-12 16:31:15

Process finished with exit code 0
```

#### union[ all]

关于union的操作姿势，[官方文档](http://docs.peewee-orm.com/en/latest/peewee/query_examples.html#combining-results-from-multiple-queries)也提供了多种方式，包括操作符、方法等等。

| 操作符 | 意义      |
| -----: | :-------- |
|     \| | union     |
|      + | union all |

当我们需要把余额操作记录和积分操作记录并作操作记录统计*时间降序*查看*第二和第三条*数据（尽管这意义不大，且实际上我本来是想用订单统计来作为示例）的时候，union|union all就可以派上用场：

```
def retrieve2():
    """union_all查询"""
    b_query = (Balance.select(
        Balance.b.alias('id'), Balance.change,
        Balance.total, Balance.addtime
    ))
    i_query = (Integral.select(
        Integral.i.alias('id'), Integral.change,
        Integral.total, Integral.addtime
    ))
    query = (b_query + i_query).order_by(SQL('addtime desc')).limit(2).offset(1)
    # query = b_query.union_all(i_query).order_by(SQL('addtime desc')).limit(2).offset(1)
    for row in query:
        print('%d:%.2f:%.2f:%s' % (row.id, row.change, row.total, row.addtime))
```

没错，union_all的操作看起来仿佛将两个元组连接一样(实际上源码 __add__ = union_all)。如果对此感到不习惯，也可以用方法union_all()来代替。值得注意的是，在方法order_by()中，不能直接写入'addtime desc'这样的字符串，因为peewee不会将其解析为sql语句。你需要使用SQL类将其转化为sql语句才能使排序生效([参考自StackOverflow](https://stackoverflow.com/questions/29960042/how-to-ordering-sql-result-in-union-peewee-orm))。

```
python peewee_test.py
('SELECT `t1`.`b_id` AS `id`, `t1`.`change`, `t1`.`total`, `t1`.`addtime` FROM `balance` AS `t1` UNION ALL SELECT `t2`.`i_id` AS `id`, `t2`.`change`, `t2`.`total`, `t2`.`addtime` FROM `integral` AS `t2` ORDER BY addtime desc LIMIT %s OFFSET %s', [2, 1])
1:300.00:300.00:2018-12-13 10:16:27
4:100.00:200.00:2018-12-12 17:24:32

Process finished with exit code 0
```

#### 聚合查询

聚合查询包括count、max、min、avg、sum。

##### count

```python
def count():
    """统计用户个数"""
    count = User.select().count()
    print('用户数量：%d' % count)
    """fn.COUNT用法"""
    fn_count = User.select(fn.COUNT(User.uid)).scalar()
    print('fn.COUNT:%d' % fn_count)
```

##### max

```python
def max():
    fn_max = User.select(fn.MAX(User.balance)).scalar()
```

##### min

```python
def min():
    fn_min = User.select(fn.MIN(User.balance)).scalar()
```

##### avg

```python
def avg():
    fn_avg = User.select(fn.AVG(User.balance)).scalar()
```

##### sum

```python
def sum():
    fn_sum = Balance.select(fn.SUM(Balance.change)).where(Balance.uid == 10001).scalar()
```

### Delete

删除调用delete()方法，使用execute()执行

```python
def delete():
    result = User.delete().where(User.uid == 10009).execute()
    print(result)
    result2 = User.delete().where(User.uid << (10006, 10007, 10008, 10009)).execute()
    print(result2)
```

返回值为成功删除的数据条数。

### 原生sql支持

使用pwiz生成models.py文件中，储存着一个类MySQLDatabase，包含了数据库连接的信息。这个类有一个cursor()方法，可以用来执行原生sql语句（如果你的peewee版本低于3.0，这个方法名是get_cursor()）。
 **在models.py中的BaseModel添加self.cursor = database.cursor**
 简单查询示例

```python
def sql():
    user = User()
    cursor = user.cursor()
    cursor.execute('SELECT `uid`, `uname`, `gender` FROM `user` WHERE `uid`=10001')
    for (uid, uname, gender) in cursor:
        print('%d:%s:%s' % (uid, uname, gender))
```

批量插入使用executemany()，参考自[CSDN](https://blog.csdn.net/mouday/article/details/80773131)。
 **在models.py中的BaseModel添加self.commit = database.commit**

```python
def sql():
    """执行批量插入"""
    user = User()
    cursor = user.cursor()
    """md5密码"""
    m = hashlib.md5()
    m.update('123456'.encode())
    pwd = m.hexdigest()
    """头像"""
    avartar = 'https://avatars2.githubusercontent.com/u/25029451'
    data_source = [
        (avartar, 'Rem', pwd),
        (avartar, 'Cosmos', pwd)
    ]
    result = cursor.executemany('insert into `user`(`avartar`, `uname`, `password`) values (%s, %s, %s) ', data_source)
    print(result)  # 返回插入条数
    user.commit()  # 需要手动提交事务插入才能成功
    cursor.close()
```





## 高阶1-连接数据库

### db_url 模块

连接数据库时，推荐使用 playhouse 中的 db_url 模块。[db_url](http://docs.peewee-orm.com/en/latest/peewee/database.html#connecting-using-a-database-url) 的 `connect` 方法可以通过传入的 URL 字符串，生成数据库连接。

函数定义为：connect(url, **connect_params)，通过传入的 url 字符串，创建一个数据库实例

**url形如**：

- `mysql://user:passwd@ip:port/my_db` 将创建一个 本地 MySQL 的 my_db 数据库的实例（will create a MySQLDatabase instance）
- `mysql+pool://user:passwd@ip:port/my_db?charset=utf8&max_connections=20&stale_timeout=300`

将创建一个本地 MySQL 的 my_db 的连接池，最大连接数为20（[In a multi-threaded application, up to max_connections will be opened. Each thread (or, if using gevent, greenlet) will have it’s own connection.](http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#connection-pool)），超时时间为300秒（will create a PooledMySQLDatabase instance）
**注意：charset 默认为utf8。如需要支持 emoji ，charset 设置为utf8mb4**，同时保证创建数据库时的字符集设置正确`CREATE DATABASE mydatabase CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`

推荐的用法为：

```python
from playhouse.db_url import connect

from dock.common import config

＃ url: mysql+pool://root:root@127.0.0.1:3306/appmanage?max_connections=300&stale_timeout=300
mysql_config_url = config_dict.get('config').get('mysql').get('url')
db = connect(url=mysql_config_url)
```



### 连接池的使用

peewee 的[连接池](http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#connection-pool)的类框架为：

class PooledDatabase(database[, max_connections=20[, stale_timeout=None[, timeout=None[, \*\*kwargs]]]])

[API定义](http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#pool-apis)的可传入的参数定义如下：

- **database** (*str*) – The name of the database or database file.
- **max_connections** (*int*) – Maximum number of connections. Provide `None` for unlimited.
- **stale_timeout** (*int*) – Number of seconds to allow connections to be used.
- **timeout** (*int*) – Number of seconds to block when pool is full. By default peewee does not block when the pool is full but simply throws an exception. To block indefinitely set this value to `0`.
- **kwargs** – Arbitrary keyword arguments passed to database class.

具体实现类包括：PooledPostgresqlDatabase、PooledPostgresqlExtDatabase、PooledMySQLDatabase、PooledSqliteDatabase、PooledSqliteExtDatabase

建立连接池的代码如下：

```
# 需导入连接池框架实现类
from playhouse.pool import PooledPostgresqlExtDatabase

# 创建数据库实例，或者使用db_url方式，类似：mysql+pool://user:passwd@ip:port/my_db?charset=utf8&max_connections=20&stale_timeout=300
db = PooledPostgresqlExtDatabase(
    'my_database',
    max_connections=8,
    stale_timeout=300,
    user='postgres')

# 指定表模型对应的数据库
class BaseModel(Model):
    class Meta:
        database = db
```

使用时需要显式的关闭连接，原因是超时连接不会自动关闭，只会在有新的请求时才会关闭。

如果不调用`_close`方法的话，**使用后** 的数据库连接就一直不会关闭(两个含义：回到pool中和关闭数据库连接)，这样会造成两个问题：

1. 每次都是新建数据库连接，因为 pool 中没有数据库连接实例。会导致稍微有一点并发量就会返回`Exceeded maximum connections.`错误
2. MySQL也是有 timeout 的，如果一个连接长时间没有请求的话，MySQL Server 就会关闭这个连接，但是，peewee的已建立（后面会解释为什么特指已建立的）的连接实例，并不知道 MySQL Server 已经关闭了，再去通过这个连接请求数据的话，就会返回 `Error 2006: “MySQL server has gone away”`错误，根据[官方文档](http://docs.peewee-orm.com/en/latest/peewee/database.html#error-2006-mysql-server-has-gone-away)

所以，每次操作完数据库就关闭连接实例。

```python
# 执行完成后自动关闭连接池连接
with db.execution_context():
    db.create_tables(...)
    ...
```



### 运行时才配置数据库

针对要执行时才能获取到实际数据库配置的情况，可以一开始不装载数据库：

```
database = PostgresqlDatabase(None)  # Un-initialized database.

class SomeModel(Model):
    class Meta:
        database = database

# 装载数据库配置
database_name = input('What is the name of the db? ')
database.init(database_name, host='localhost', user='postgres')

# 连接数据库
database.connect()
```



### 动态定义数据库

如果希望在运行中按配置切换使用不同的数据库，可以使用DatabaseProxy：

```python
database_proxy = DatabaseProxy()  # Create a proxy for our db.

class BaseModel(Model):
    class Meta:
        database = database_proxy  # Use proxy for our DB.

class User(BaseModel):
    username = CharField()

# Based on configuration, use a different database.
if app.config['DEBUG']:
    database = SqliteDatabase('local.db')
elif app.config['TESTING']:
    database = SqliteDatabase(':memory:')
else:
    database = PostgresqlDatabase('mega_production_db')

# Configure our proxy to use the db we specified in config.
database_proxy.initialize(database)
```



## 高阶2-tornado + peewee-async 异步ORM

原文出处：<https://blog.csdn.net/duxiangwushirenfei/article/details/79488617>

peewee官方文档](http://docs.peewee-orm.com/en/latest/peewee/database.html#tornado)

It looks like Tornado’s `RequestHandler` class implements two hooks which can be used to open and close connections when a request is handled.

```
from tornado.web import RequestHandler

db = SqliteDatabase('my_db.db')

class PeeweeRequestHandler(RequestHandler):
    def prepare(self):
        db.connect()
        return super(PeeweeRequestHandler, self).prepare()

    def on_finish(self):
        if not db.is_closed():
            db.close()
        return super(PeeweeRequestHandler, self).on_finish()
```

In your app, instead of extending the default `RequestHandler`, now you can extend `PeeweeRequestHandler`.

Note that this does not address how to use peewee asynchronously with Tornado or another event loop.



### [tornado + peewee-async 异步ORM](https://blog.csdn.net/duxiangwushirenfei/article/details/79488617)

#### 前言

习惯sql操作数据，需要做一些简单业务操作时sql操作数据的低复用显露无疑。惰性不愿手动写ORM，索性找一个python比较通用的ORM，选了peewee。为和tornado配合使用，改用在peewee基础上封装的peewee-async几经折腾，总算调试通过，演示环境MacOS，python3.5.2。 
类似还有torpeewee，不推荐使用。 
本篇所有演示代码可以在个人github中下载，演示[demo](https://github.com/wushirenfei/tornado_peewee)。

#### 安装

[peewee的使用文档](http://docs.peewee-orm.com/en/latest/) 
[peewee-async的使用文档](https://peewee-async.readthedocs.io/en/latest/) 
直接pip就能安装以上package

```
pip install peewee peewee-async
```

如果需要操作MySQL数据库需要额外安装

```
pip install aiomysql
```

如果需要操作PostgreSQL数据库需要额外安装

```
pip install aiopg
```


如果有使用Django的经验，基本秒懂peewee ORM的使用方式，整体上就是和Django类似的定义和使用。 
在peeweee-aysnc的使用文档中给出了peeweee-aysnc + tornado的使用范例，根本跑不通，以下使用tornado 5.0配合 peewee-async 0.5.11，peewee 2.9.1，iomysql 0.0.12 搭建整体框架。

#### tornado + peewee-async

修正文档中给出的示例，能够正常运行：

```python
import peewee
import peewee_async
import tornado.web
from tornado import httpserver


database = peewee_async.PooledMySQLDatabase(
    'alexdb', host='127.0.0.1', port=3306,
    user='root', password='')


# Define model
class TestNameModel(peewee.Model):
    name = peewee.CharField()

    class Meta:
        database = database

    def __str__(self):
        return self.name


# Create table, add some instances
TestNameModel.create_table(True)
TestNameModel.get_or_create(id=1, defaults={'name': "TestNameModel id=1"})
TestNameModel.get_or_create(id=2, defaults={'name': "TestNameModel id=2"})
TestNameModel.get_or_create(id=3, defaults={'name': "TestNameModel id=3"})
database.close()


# Define handlers
class RootHandler(tornado.web.RequestHandler):
    """
    Accepts GET methods.
    GET: get instance by id, `id` argument is required
    """
    async def get(self):
        obj_id = self.get_argument('id', None)
        try:
            obj = await self.application.objects.get(TestNameModel, id=obj_id)
            self.write({
                'id': obj.id,
                'name': obj.name,
            })
        except TestNameModel.DoesNotExist:
            raise tornado.web.HTTPError(404, "Object not found!")


def main():
    app = tornado.web.Application(handlers=[
        (r'/alex', 'demo.RootHandler'), ], debug=True)

    # Set up database and manager
    app.objects = peewee_async.Manager(database)

    # Run loop
    print("""Run application server http://127.0.0.1:8888s
        Try GET urls:
        http://127.0.0.1:8888?id=1
    ^C to stop server""")

    server = httpserver.HTTPServer(app, xheaders=True)
    server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
```

页面访问 http://127.0.0.1:8888/alex?id=1能够正常查询数据。更多的ORM查询语法可以参见peewee的查询方式。

注意： 
1，上述代码在tornado 4.4.2版本中不能正常运行，5.0中可以。 
2，peewee-async在get数据时，如果没有检索到符合条件的数据会触发一个DoesNotExist的异常。 
3，跟多的peewee ORM的细节使用方式请查询peewee给出的示例，应有尽有。 



### [通过peewee-async集成到tornado中](https://www.cnblogs.com/crazymagic/articles/10187807.html)

之所以集成peewee-async是因为peewee中存在大量的同步方法 execute （比如在更新和保存，删除），而我们需要异步的方法，peewee-async 中由asyncio提供的peewee ORM的异步接口，可以直接在tornado中使用 

安装 peewee-async　

```
`pip install ``-``-``pre peewee``-``async　`
```

 gihub 地址

```
`https:``/``/``github.com``/``05bit``/``peewee``-``async`
```

根据官方文档改写models/model.py

```python
from datetime import datetime

from peewee import *
from peewee import Model
import peewee_async

database = peewee_async.MySQLDatabase(
    'message', host="127.0.0.1", port=3306, user="root", password="mysql"
)

objects = peewee_async.Manager(database)

# No need for sync anymore!


database.set_allow_sync(False)


class BaseModel(Model):
    add_time = DateTimeField(default=datetime.now, verbose_name="添加时间")
    class Meta:
        database = database

class Supplier(BaseModel):
    name = CharField(max_length=100, verbose_name="名称", index=True)
    address = CharField(max_length=100, verbose_name="联系地址")
    phone = CharField(max_length=11, verbose_name="联系方式")
    class Meta:
        database = database
        table_name = "supplier"

class Goods(BaseModel):
    supplier = ForeignKeyField(Supplier, verbose_name="商家", backref="goods")
    name = CharField(max_length=100, verbose_name="商品名称", index=True)
    click_num = IntegerField(default=0, verbose_name="点击数")
    goods_num = IntegerField(default=0, verbose_name="库存数")
    price = FloatField(default=0.0, verbose_name="价格")
    brief = TextField(verbose_name="商品简介")

    class Meta:
        table_name = "goods"


def init_table():
    db.create_tables([Goods, Supplier])
if __name__ == "__main__":
    init_table()
```

peewee_async_test.py

```
import asyncio

from chapter04.models.model import Goods
from chapter04.models.model import objects


async def handler():
    await objects.create(Goods, supplier_id=1, name="53度水井坊臻酿八號500ml",
                         click_num=20, goods_num=1000, price=500, brief="州茅台酒厂（集团）保健酒业有限公司生产")
    goods = await objects.execute(Goods.select())
    for good in goods:
        print(good.name)

loop = asyncio.get_event_loop()
loop.run_until_complete(handler())
```

