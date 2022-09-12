# MacOS-M1安装MongoDB

1、拉取官方的最新版本的镜像：

```shell
$ docker pull mongo:latest
```

2、安装完成后，我们可以使用以下命令来运行 mongo 容器：

```shell
$ docker run -itd --name mongo -p 27017:27017 mongo --auth
```

参数说明：

- **-p 27017:27017** ：映射容器服务的 27017 端口到宿主机的 27017 端口。外部可以直接通过 宿主机 ip:27017 访问到 mongo 的服务。
- **--auth**：需要密码才能访问容器服务。

注：可以添加其他参数，介绍如下：

```
# 使用卷持久化数据
-v mongo-data:/data/db

# 设置副本集群方案
--replSet rs0
```

3、使用以下命令添加用户和设置密码，并且尝试连接

```
# 第一次连接数据库
$ docker exec -it mongo mongo admin
# 创建一个名为 admin，密码为 123456 的用户。
>  db.createUser({ user:'admin',pwd:'123456',roles:[ { role:'userAdminAnyDatabase', db: 'admin'},"readWriteAnyDatabase"]});
# 创建具备所有权限的用户
>  db.createUser({ user:'root',pwd:'123456',roles:["root"]});
# 尝试使用上面创建的用户信息进行连接。
> db.auth('admin', '123456')

# 设置了用户密码后再次连接数据库
$ docker exec -it mongo mongo -u admin -p 123456 admin
```

## 部署单节点集群（单机开启事务支持）

```
 在本机先创建keyfile
cd /Users/lhj/software/mongo_keyfile
openssl rand -base64 128 > ./keyFile
chmod 600 ./keyFile 

# 运行容器, 设置副本集群方案, 注意需要指定keyfile
docker run -itd --name mongo -v /Users/lhj/software/mongo_keyfile:/mongo_keyfile -p 27017:27017 mongo --auth --replSet rs0 --keyFile /mongo_keyfile/keyFile

# 第一次连接数据库
$ docker exec -it mongo mongo admin
# 初始化集群
> rs.initiate()
# 创建一个名为 admin，密码为 123456 的用户。
> db.createUser({ user:'admin',pwd:'123456',roles:[ { role:'userAdminAnyDatabase', db: 'admin'},"readWriteAnyDatabase"]});
# 尝试使用上面创建的用户信息进行连接。
> db.auth('admin', '123456')
# 创建具备所有权限的用户
> db.createUser({ user:'root',pwd:'123456',roles:["root"]});

# 连接数据库
docker exec -it mongo mongo -u root -p 123456 admin
```

## 基本操作命令

```
# 显示所有数据的列表
show dbs

# 显示当前数据库对象或集合
db

# 切换到local数据库
use local

# 当use指定的数据库不存在时，将自动创建数据库, 尝试创建testdb数据库
# 注意需在数据库中添加数据以后，show dbs才能看到对应的数据库
use testdb

# 创建集合命令db.createCollection(name, options)
# 集合相对于关系型数据库的表
# 带options的写法：db.createCollection("mycol", {capped: true, autoIndexId: true, size: 6142800, max: 10000})
db.createCollection("t_test")

# 查看已有集合列表，也可以用show tables
show collections

# 删除指定集合：db.collection.drop()，例如
db.t_test.drop()

# 插入文档命令，文档相对于关系型数据库的行记录
# db.COLLECTION_NAME.insert(document) - 插入记录,若插入的数据主键已经存在，则会抛出org.springframework.dao.DuplicateKeyException 异常，提示主键重复，不保存当前数据
# db.collection.insertOne() 或 db.collection.replaceOne() - 插入记录，如果记录存在则进行覆盖
# db.collection.insertMany() - 一次插入多条记录
# 注：插入文档时如果集合不存在，会自动创建集合
db.t_test.insert({title: 'MongoDB 教程', 
    description: 'MongoDB 是一个 Nosql 数据库',
    by: '菜鸟教程',
    url: 'http://www.runoob.com',
    tags: ['mongodb', 'database', 'NoSQL'],
    likes: 100
})

# 一次插入多条文档
> var res = db.t_test.insertMany([{"b": 3}, {'c': 4}])
> res

# 循环插入多个文档
> var arr = [];
> for(var i=1 ; i<=100 ; i++){
    arr.push({num:i});
}
> db.numbers.insert(arr);


# 查询文档命令 db.collection.find(query, projection)
# query ：可选，使用查询操作符指定查询条件
# projection ：可选，使用投影操作符指定返回的键 {KEY:1}, 如果要指定不需要显示的字典可以设置为0（例如_id总显示，可以设置为0不显示）。查询时返回文档中所有键值， 只需省略该参数即可（默认省略）
# 如果需要以易读的方式来读取数据，可以使用 pretty() 方法，例如: db.collection.find().pretty()
db.t_test.find()
db.t_test.find({"by":"菜鸟教程", "title":"MongoDB 教程"}, {"_id": 0, "title": 1}).pretty()


# 更新文档命令 db.collection.update
# 注意：默认情况下只会更新找到的第一条记录，如果需要更新所有匹配记录，需要指定multi参数为true，例如：
# db.col.update({'title':'MongoDB 教程'},{$set:{'title':'MongoDB'}},{multi:true})
> db.t_test_upd.insert({
    title: 'MongoDB 教程', 
    description: 'MongoDB 是一个 Nosql 数据库',
    by: '菜鸟教程',
    url: 'http://www.runoob.com',
    tags: ['mongodb', 'database', 'NoSQL'],
    likes: 100
})
> db.t_test_upd.update({'title':'MongoDB 教程'},{$set:{'title':'MongoDB'}})
> db.t_test_upd.find().pretty()

# 删除文档命令db.collection.remove
# 删除所有数据的方式：db.col.remove({})
# 注意：默认情况下删除命令会删除所有的匹配数据，如果需要只删除一条, 可设置 justOne 参数为true，例如
# db.t_test_del.remove({'title':'MongoDB 教程'}, {'justOne': true})
# 注：remove() 方法已经过时了，现在官方推荐使用 deleteOne() 和 deleteMany() 方法

> db.t_test_del.insert({title: 'MongoDB 教程', 
    description: 'MongoDB 是一个 Nosql 数据库',
    by: '菜鸟教程',
    url: 'http://www.runoob.com',
    tags: ['mongodb', 'database', 'NoSQL'],
    likes: 100
})
> db.t_test_del.insert({title: 'MongoDB 教程', 
    description: 'MongoDB 是一个 Nosql 数据库',
    by: '菜鸟教程',
    url: 'http://www.runoob.com',
    tags: ['mongodb', 'database', 'NoSQL'],
    likes: 100
})
> db.t_test_del.remove({'title':'MongoDB 教程'})
> db.t_test_del.find().pretty()


# 删除数据库, 需要先切换到数据库中
use testdb
db.dropDatabase()
```

## 数据处理技巧

### 集合联合查询（left join）

```
use testdb

# 清空数据
db.orders.remove({})
db.inventory.remove({})
db.house.remove({})

# 订单数据
db.orders.insert([
   { "_id" : 1, "item" : "almonds", "price" : 12, "quantity" : 2, "house": "h1" },
   { "_id" : 2, "item" : "pecans", "price" : 20, "quantity" : 1, "house": "h2" },
   { "_id" : 3, "item" : "pecans", "price" : 20, "quantity" : 5, "house": "h1" },
   { "_id" : 4, "item" : "bread", "price" : 10, "quantity" : 3, "house": "h1" },
   { "_id" : 5, "item" : "cashews", "price" : 10, "quantity" : 3, "house": "h1" },
   { "_id" : 6  }
])

# 商品库存数据, sku字段可以与订单中的item字段关联起来
db.inventory.insert([
   { "_id" : 1, "sku" : "almonds", description: "product 1", "instock" : 120 },
   { "_id" : 2, "sku" : "bread", description: "product 2", "instock" : 80 },
   { "_id" : 3, "sku" : "cashews", description: "product 3", "instock" : 60 },
   { "_id" : 4, "sku" : "pecans", description: "product 4", "instock" : 70 },
   { "_id" : 5, "sku": null, description: "Incomplete" },
   { "_id" : 6 }
])

# 仓库信息
db.house.insert([
    { "_id" : 1, "hid": "h1", "name": "my house"},
    { "_id" : 2, "hid": "h2", "name": "test house"}
])

# 联表查询
# $lookup关联表inventory的数据, inventory的数据查询出来形成inventory_docs数组
# $lookup关联表house的数据, house的数据查询出来形成house_docs数组
# $match过滤主表的条件
db.orders.aggregate([
   {
     $lookup:
       {
         from: "inventory",
         localField: "item",
         foreignField: "sku",
         as: "inventory_docs"
       }
  },
  {
       $lookup:
       {
         from: "house",
         localField: "house",
         foreignField: "hid",
         as: "house_docs"
       }
  },
  {
      $match: {"item": "pecans"}
  }
])

# 联表查询
# 通过$unwind将inventory_docs的数组的第一个转换为该字段的子字典
# 通过$match进行调节过滤, 支持对关联字段的过滤
db.orders.aggregate([
   {
     $lookup:
       {
         from: "inventory",
         localField: "item",
         foreignField: "sku",
         as: "inventory_docs"
       }
  },
  { $unwind: "$inventory_docs" },
  {
     $match: {"item": {$in: ["pecans", "bread", "cashews"] }, "inventory_docs.sku": "pecans" }
  }
])
```
