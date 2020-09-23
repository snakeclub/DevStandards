# Redis6.0.5版本配置文件说明

版权声明：本文为CSDN博主「披星戴月，风雨兼程。」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/qq_42534026/java/article/details/106730314



## Redis版本

此文章中Redis版本为6.0.5。

```java
redis-server --version
Redis server v=6.0.5 sha=00000000:0 malloc=jemalloc-5.1.0 bits=64 build=e8c241ddd6b4e79c
```

## 配置文件说明

因Redis配置文件内容过多，我按照以模块的方式分别对配置项进行说明。

### ###UNIT（单位）###（了解）

```
1k => 1000 bytes
1kb => 1024 bytes
1m => 1000000 bytes
1mb => 1024*1024 bytes
1g => 1000000000 bytes
1gb => 1024*1024*1024 bytes
```

### ###INCLUDES（包含）###（了解）

用于启动时加载模块。如果服务器无法加载模块，它将中止。可以使用多个loadmodule指令。

### ###NETWORK（网络）###（需记）

**1. bind**
说明：Redis服务监听地址，用于Redis客户端连接，默认只监听本机回环地址。
默认配置项：bind 127.0.0.1

**2.protected-mode**
说明：Protected模式是一层安全保护。默认是开启的，配置bind ip或者设置访问密码访问，关闭后，外部网络可以直接访问。
默认配置项：protected-mode yes

**3.prot**
说明：Redis监听端口，默认为6379
默认配置项：port 6379

**4.tcp-backlog**
说明：此参数确定了TCP连接中已完成队列(完成三次握手之后)的长度， 当然此值必须不大于Linux系统定义的/proc/sys/net/core/somaxconn值，默认是511。

而Linux的默认参数值是128，当系统并发量大并且客户端速度缓慢的时候，建议修改值大于511。
默认配置项：tcp-backlog 511

**5.unixsocket**
说明：指定 unix socket 的路径
默认配置项：unixsocket /tmp/redis.sock

**6.unixsocketperm**
说明：指定 unix socket file 的权限。
默认配置项：unixsocketperm 700

**7.timeout**
说明：在客户端闲置多少秒后断开连接。
默认配置项：timeout 0

**8.tcp-keepalive**
说明：用来定时向client发送tcp_ack包来探测client是否存活的。
默认配置项：tcp-keepalive 300



### ###TLS / SSL（安全套接字）###（了解）

默认情况下，禁用TLS / SSL。要启用它，请使用“ tls-port”配置。



### ###GENERAL（通用）###（精通）

**1.daemonize**
说明：默认情况下，Redis不作为守护进程运行。如果你需要的话，用yes。
默认配置项：daemonize no

**2.supervised**
说明：可以通过upstart和systemd管理Redis守护进程，这个参数是和具体的操作系统相关的。
默认配置项：supervised no

**3.pidfile**
说明：配置pid文件路径，当redis以守护模式启动时，如果没有配置pidfile，pidfile默认值是/var/run/redis.pid 。
默认配置项：pidfile /var/run/redis_6379.pid

**4.loglevel**
说明：日志记录等级，有4个可选值，debug（开发），verbose（默认值），notice（生产），warning（警告）
默认配置项：loglevel notice

**5.logfile**
说明：日志文件的位置，当指定为空字符串时，为标准输出，如果redis已守护进程模式运行，那么日志将会输出到 /dev/null，若指定了路径，日志将会输出到指定文件 。
默认配置项：logfile " "

**6.syslog-enabled**
说明：是否把日志记录到系统日志。
默认配置项：syslog-enabled no

**7.syslog-ident**
说明：指定syslog里的日志标识
默认配置项：syslog-ident redis

**8.syslog-facility**
说明：指定syslog设备(facility)，必须是user或则local0到local7。
默认配置项：syslog-facility local0

**9.databases**
说明：可用数据库数量
默认配置项：databases 16

**10.always-show-logo**
说明：Redis显示一个ASCII艺术徽标只有当开始登录到标准输出，以及标准输出是否是TTY。
默认配置项：always-show-logo yes



### ###SNAPSHOTTING（快照）### （需记）

**1.save**
说明：多少秒保存数据到磁盘，格式是：save <seconds> <changes>。意思是至少有changes条key数据被改变时，seconds秒保存到磁盘。

默认配置项：
save 900 1
save 300 10
save 60 10000

2.stop-writes-on-bgsave-error
说明：默认情况下，如果 redis 最后一次的后台保存失败，redis 将停止接受写操作，这样以一种强硬的方式让用户知道数据不能正确的持久化到磁盘， 否则就会没人注意到灾难的发生。 如果后台保存进程重新启动工作了，redis 也将自动的允许写操作。
默认配置项：stop-writes-on-bgsave-error yes

3.rdbcompression
说明：当dump .rdb数据库的时候是否压缩数据对象，如果你想节约一些cpu资源的话，可以把它设置为no，这样的话数据集就可能会比较大。
默认配置项：rdbcompression yes

4.rdbchecksum
说明：存储和加载rdb文件时校验，会占用一部分资源。
默认配置项：rdbchecksum yes

5.dbfilename
说明：本地数据库文件名，默认值为dump.rdb
默认配置项：dbfilename dump.rdb

6.rdb-del-sync-files
说明：在没有持久性的情况下删除复制中使用的RDB文件
启用。默认情况下，此选项是禁用的。
默认配置项：rdb-del-sync-files no

7.dir
说明：本地数据库存放路径，默认值为 ./
默认配置项：dir ./



### ###REPLICATION（主从）###（必会）

1.replicaof
说明：格式：replicaof <masterip> <masterport>，当本机为从服务时，设置主服务的IP及端口。例如：replicaof 192.168.233.233 6379。
默认配置项：replicaof <masterip> <masterport>

2.masterauth
说明：当本机为从服务时，设置主服务的连接密码。
默认配置项：masterauth <master-password>

3.masteruser
说明：当本机为从服务时，设置主服务的用户名。
默认配置项：masteruser <username>

4.slave-serve-stale-data
说明：当slave失去与master的连接，或正在拷贝中，如果为yes，slave会响应客户端的请求，数据可能不同步甚至没有数据，如果为no，slave会返回错误"SYNC with master in progress"
默认配置项：replica-serve-stale-data yes

5.replica-read-only
说明：如果为yes，slave实例只读，如果为no，slave实例可读可写。
默认配置项：replica-read-only yes

6.repl-diskless-sync
说明：新的从站和重连后不能继续备份的从站，需要做所谓的“完全备份”，即将一个RDB文件从主站传送到从站。这个传送有以下两种方式：
硬盘备份：redis主站创建一个新的进程，用于把RDB文件写到硬盘上。过一会儿，其父进程递增地将文件传送给从站。

无硬盘备份：redis主站创建一个新的进程，子进程直接把RDB文件写到从站的套接字，不需要用到硬盘。

在硬盘备份的情况下，主站的子进程生成RDB文件。一旦生成，多个从站可以立即排成队列使用主站的RDB文件。在无硬盘备份的情况下，一次RDB传送开始，新的从站到达后，需要等待现在的传送结束，才能开启新的传送。

如果使用无硬盘备份，主站会在开始传送之间等待一段时间（可配置，以秒为单位），希望等待多个子站到达后并行传送。
在硬盘低速而网络高速（高带宽）情况下，无硬盘备份更好。
默认配置项：repl-diskless-sync no

7.repl-diskless-sync-delay
说明：无盘复制延时开始秒数，默认是5秒，意思是当PSYNC触发的时候，master延时多少秒开始向master传送数据流，以便等待更多的slave连接可以同时传送数据流，因为一旦PSYNC开始后，如果有新的slave连接master，只能等待下次PSYNC。可以配置为0取消等待，立即开始。
默认配置项：repl-diskless-sync-delay 5

8.repl-diskless-load
说明：是否使用无磁盘加载，有三项：
disabled：不要使用无磁盘加载，先将rdb文件存储到磁盘
on-empty-db：只有在完全安全的情况下才使用无磁盘加载
swapdb：解析时在RAM中保留当前db内容的副本，直接从套接字获取数据。
默认配置项：repl-diskless-load disabled

9.repl-ping-replica-period
说明：指定slave定期ping master的周期，默认10秒钟。
默认配置项：repl-ping-replica-period 10

10.repl-timeout
说明：从服务ping主服务的超时时间，若超过repl-timeout设置的时间，slave就会认为master已经宕了。
默认配置项：repl-timeout 60

11.repl-disable-tcp-nodelay
说明：在slave和master同步后（发送psync/sync），后续的同步是否设置成TCP_NODELAY . 假如设置成yes，则redis会合并小的TCP包从而节省带宽，但会增加同步延迟（40ms），造成master与slave数据不一致 假如设置成no，则redis master会立即发送同步数据，没有延迟。
默认配置项：repl-disable-tcp-nodelay no

12.repl-backlog-size
说明：设置主从复制backlog容量大小。这个 backlog 是一个用来在 slaves 被断开连接时存放 slave 数据的 buffer，所以当一个 slave 想要重新连接，通常不希望全部重新同步，只是部分同步就够了，仅仅传递 slave 在断开连接时丢失的这部分数据。这个值越大，salve 可以断开连接的时间就越长。
默认配置项：repl-backlog-size 1mb

13.repl-backlog-ttl
说明：配置当master和slave失去联系多少秒之后，清空backlog释放空间。当配置成0时，表示永远不清空。
默认配置项：repl-backlog-ttl 3600

14.replica-priority
说明：当 master 不能正常工作的时候，Redis Sentinel 会从 slaves 中选出一个新的 master，这个值越小，就越会被优先选中，但是如果是 0 ， 那是意味着这个 slave 不可能被选中。 默认优先级为 100。
默认配置项：replica-priority 100

15.min-replicas-to-write&min-replicas-max-lag
说明：假如主redis发现有超过M个从redis的连接延时大于N秒，那么主redis就停止接受外来的写请求。这是因为从redis一般会每秒钟都向主redis发出PING，而主redis会记录每一个从redis最近一次发来PING的时间点，所以主redis能够了解每一个从redis的运行情况。上面这个例子表示，假如有大于等于3个从redis的连接延迟大于10秒，那么主redis就不再接受外部的写请求。上述两个配置中有一个被置为0，则这个特性将被关闭。默认情况下min-replicas-to-write为0，而min-replicas-max-lag为10。
默认配置项：
min-replicas-to-write 3
min-replicas-max-lag 10

16.replica-announce-ip&replica-announce-port
说明：常用于端口转发或NAT场景下，对Master暴露真实IP和端口信息。
默认配置项：
replica-announce-ip 5.5.5.5
replica-announce-port 1234

### ###KEYS TRACKING（键跟踪）###（了解）

关于键跟踪的一些描述

### ###SECURITY（安全）###（必会）

**1.acllog-max-len**
说明：ACL日志存储在内存中并消耗内存，设置此项可以设置最大值来回收内存。
默认配置项：acllog-max-len 128

2.requirepass
说明：设置Redis连接密码
默认配置项：requirepass foobared

3.rename-command
说明：将命令重命名。为了安全考虑，可以将某些重要的、危险的命令重命名。当你把某个命令重命名成空字符串的时候就等于取消了这个命令。
默认配置项：rename-command CONFIG " "

### ###CLIENTS（客户端）###（需记）

**1.maxclients**
说明：客户端最大连接数
默认配置项：maxclients 10000



### ###MEMORY MANAGEMENT（内存管理）###（按需）

**1. maxmemory**
说明：指定Redis最大内存限制。达到内存限制时，Redis将尝试删除已到期或即将到期的Key。
默认配置项：maxmemory <bytes>

2.maxmemory-policy
说明：Redis达到最大内存时将如何选择要删除的内容，有以下选项。
1.volatile-lru：利用LRU算法移除设置过过期时间的key (LRU:最近使用 Least Recently Used )
2.allkeys-lru：利用LRU算法移除任何key
3.volatile-random：移除设置过过期时间的随机key
4.allkeys-random：移除随机key
5.volatile-ttl：移除即将过期的key(minor TTL)
6.noeviction：不移除任何key，只是返回一个写错误 。默认选项

默认配置项：maxmemory-policy noeviction

3.maxmemory-samples
说明：LRU 和 minimal TTL 算法都不是精准的算法，但是相对精确的算法(为了节省内存)，随意你可以选择样本大小进行检测。redis默认选择3个样本进行检测，你可以通过maxmemory-samples进行设置 样本数。

4.replica-ignore-maxmemory
说明：从 Redis 5 开始，默认情况下，replica 节点会忽略 maxmemory 设置（除非在发生 failover 后，此节点被提升为 master 节点）。 这意味着只有 master 才会执行过期删除策略，并且 master 在删除键之后会对 replica 发送 DEL 命令。

这个行为保证了 master 和 replicas 的一致性，并且这通常也是你需要的，但是若你的 replica 节点是可写的， 或者你希望 replica 节点有不同的内存配置，并且你确保所有到 replica 写操作都幂等的，那么你可以修改这个默认的行为 （请确保你明白你在做什么）。
默认配置项：replica-ignore-maxmemory yes

### ###LAZY FREEING（惰性删除）###（按需）

1.lazyfree-lazy-eviction
说明：针对redis内存使用达到maxmeory，并设置有淘汰策略时，在被动淘汰键时，是否采用lazy free机制。因为此场景开启lazy free, 可能使用淘汰键的内存释放不及时，导致redis内存超用，超过maxmemory的限制。
默认配置项：lazyfree-lazy-eviction no

2.lazyfree-lazy-expire
说明：针对设置有TTL的键，达到过期后，被redis清理删除时是否采用lazy free机制。此场景建议开启，因TTL本身是自适应调整的速度。
默认配置项：lazyfree-lazy-expire no

3.lazyfree-lazy-server-del
说明：针对有些指令在处理已存在的键时，会带有一个隐式的DEL键的操作。如rename命令，当目标键已存在,redis会先删除目标键，如果这些目标键是一个big key,那就会引入阻塞删除的性能问题。 此参数设置就是解决这类问题，建议可开启。
默认配置项：lazyfree-lazy-server-del no

4.replica-lazy-flush
说明：针对slave进行全量数据同步，slave在加载master的RDB文件前，会运行flushall来清理自己的数据场景，参数设置决定是否采用异常flush机制。如果内存变动不大，建议可开启。可减少全量同步耗时，从而减少主库因输出缓冲区爆涨引起的内存使用增长。
默认配置项：replica-lazy-flush no

5.lazyfree-lazy-user-del
说明：对于替换用户代码DEL调用的情况，也可以这样做
使用UNLINK调用是不容易的，要修改DEL的默认行为
命令的行为完全像UNLINK。
默认配置项：lazyfree-lazy-user-del no

### ###THREADED I/O（线程I/O）###（了解）

关于线程的一些配置及说明。



### ###APPEND ONLY MODE（追加）###（必会）

**1.appendonly**
说明：是否启用aof持久化方式 。即是否在每次更新操作后进行日志记录，默认配置是no，即在采用异步方式把数据写入到磁盘，如果不开启，可能会在断电时导致部分数据丢失。

默认配置项：appendonly no

2.appendfilename
说明：更新日志文件名，默认为appendonly.aof。
默认配置项：appendfilename “appendonly.aof”

3.appendfsync
说明：aof文件刷新的频率。有三种：
1.no 依靠OS进行刷新，redis不主动刷新AOF，这样最快，但安全性就差。
2.always 每提交一个修改命令都调用fsync刷新到AOF文件，非常非常慢，但也非常安全。
3.everysec 每秒钟都调用fsync刷新到AOF文件，很快，但可能会丢失一秒以内的数据。
默认配置项：appendfsync everysec

4.no-appendfsync-on-rewrite
说明：指定是否在后台aof文件rewrite期间调用fsync，默认为no，表示要调用fsync（无论后台是否有子进程在刷盘）。Redis在后台写RDB文件或重写AOF文件期间会存在大量磁盘IO，此时，在某些linux系统中，调用fsync可能会阻塞。
默认配置项：no-appendfsync-on-rewrite no

5.auto-aof-rewrite-percentage
说明：aof文件增长比例，指当前aof文件比上次重写的增长比例大小。aof重写即在aof文件在一定大小之后，重新将整个内存写到aof文件当中，以反映最新的状态(相当于bgsave)。这样就避免了，aof文件过大而实际内存数据小的问题(频繁修改数据问题)。
默认配置项：auto-aof-rewrite-percentage 100

6.auto-aof-rewrite-min-size
说明：aof文件重写最小的文件大小，即最开始aof文件必须要达到这个文件时才触发，后面的每次重写就不会根据这个变量了(根据上一次重写完成之后的大小).此变量仅初始化启动redis有效.如果是redis恢复时，则lastSize等于初始aof文件大小。
默认配置项：auto-aof-rewrite-min-size 64mb

7.aof-load-truncated
说明：指redis在恢复时，会忽略最后一条可能存在问题的指令。默认值yes。即在aof写入时，可能存在指令写错的问题(突然断电，写了一半)，这种情况下，yes会log并继续，而no会直接恢复失败。
默认配置项：aof-load-truncated yes

8.aof-use-rdb-preamble
说明：在开启了这个功能之后，AOF重写产生的文件将同时包含RDB格式的内容和AOF格式的内容，其中RDB格式的内容用于记录已有的数据，而AOF格式的内存则用于记录最近发生了变化的数据，这样Redis就可以同时兼有RDB持久化和AOF持久化的优点（既能够快速地生成重写文件，也能够在出现问题时，快速地载入数据）。
默认配置项：aof-use-rdb-preamble yes

### ###LUA SCRIPTING（LUA 脚本）###（了解）

**1.lua-time-limit**
说明：一个Lua脚本最长的执行时间，单位为毫秒，如果为0或负数表示无限执行时间，默认为5000
默认配置项：lua-time-limit 5000



### ###REDIS CLUSTER（集群）###（必会）

**1.cluster-enabled**
说明：如果是yes，表示启用集群，否则以单例模式启动
默认配置项：cluster-enabled yes

2.cluster-config-file
说明：这不是一个用户可编辑的配置文件，这个文件是Redis集群节点自动持久化每次配置的改变，为了在启动的时候重新读取它。
默认配置项：cluster-config-file nodes-6379.conf

3.cluster-node-timeout
说明：超时时间，集群节点不可用的最大时间。如果一个master节点不可到达超过了指定时间，则认为它失败了。注意，每一个在指定时间内不能到达大多数master节点的节点将停止接受查询请求。
默认配置项：cluster-node-timeout 15000

4.cluster-replica-validity-factor
说明：如果设置为0，则一个slave将总是尝试故障转移一个master。如果设置为一个正数，那么最大失去连接的时间是node timeout乘以这个factor。
默认配置项：cluster-replica-validity-factor 10

5.cluster-migration-barrier
说明：一个master和slave保持连接的最小数量（即：最少与多少个slave保持连接），也就是说至少与其它多少slave保持连接的slave才有资格成为master。
默认配置项：cluster-migration-barrier 1

6.cluster-require-full-coverage
说明：如果设置为yes，这也是默认值，如果key space没有达到百分之多少时停止接受写请求。如果设置为no，将仍然接受查询请求，即使它只是请求部分key。
默认配置项：cluster-require-full-coverage yes

7.cluster-replica-no-failover
说明：此选项设置为yes时，可防止从设备尝试对其进行故障转移master在主故障期间。 然而，仍然可以强制执行手动故障转移。
默认配置项：cluster-replica-no-failover no

8.cluster-allow-reads-when-down
说明：是否允许集群在宕机时读取
默认配置项：cluster-allow-reads-when-down no

### ###CLUSTER DOCKER/NAT support （docker集群/NAT支持）###（按需）

**1.cluster-announce-ip**
说明：宣布IP地址
默认配置项：cluster-announce-ip 10.1.1.5

2.cluster-announce-port
说明：宣布服务端口
默认配置项：cluster-announce-port 6379

3.cluster-announce-bus-port
说明：宣布集群总线端口
默认配置项：cluster-announce-bus-port 6380

### ###SLOW LOG（慢查询日志）### （需记）

1.slowlog-log-slower-than
说明：决定要对执行时间大于多少微秒(microsecond，1秒 = 1,000,000 微秒)的查询进行记录。
默认配置项：slowlog-log-slower-than 10000

2.slowlog-max-len
说明：它决定 slow log 最多能保存多少条日志， slow log 本身是一个 FIFO 队列，当队列大小超过 slowlog-max-len 时，最旧的一条日志将被删除，而最新的一条日志加入到 slow log ，以此类推。
默认配置项：slowlog-max-len 128

### ###LATENCY MONITOR（延时监控）###（了解）

**1.latency-monitor-threshold**
说明：能够采样不同的执行路径来知道redis阻塞在哪里。这使得调试各种延时问题变得简单，设置一个毫秒单位的延时阈值来开启延时监控。

默认配置项：latency-monitor-threshold 0

### ###EVENT NOTIFICATION（事件通知）###（了解）

**1.notify-keyspace-events**
说明：键事件通知，可用参数：

K 键空间通知，所有通知以 keyspace@ 为前缀.
E 键事件通知，所有通知以 keyevent@ 为前缀
g DEL 、 EXPIRE 、 RENAME 等类型无关的通用命令的通知
$ 字符串命令的通知
l 列表命令的通知
s 集合命令的通知
h 哈希命令的通知
z 有序集合命令的通知
x 过期事件：每当有过期键被删除时发送
e 驱逐(evict)事件：每当有键因为 maxmemory 策略而被删除时发送
A 参数 g$lshzxe 的别名
书写：notify-keyspace-events Ex
默认配置项：notify-keyspace-events " "

### ### GOPHER SERVER（GOPHER协议服务）###（了解）

**1.gopher-enabled**
说明：开启gopher功能
默认配置项：gopher-enabled no

### ###ADVANCED CONFIG（高级配置）###（按需）

**1.hash-max-ziplist-entries**
说明：这个参数指的是ziplist中允许存储的最大条目个数，默认为512，建议为128。
默认配置项：hash-max-ziplist-entries 512

2.hash-max-ziplist-value
说明：ziplist中允许条目value值最大字节数，默认为64，建议为1024。
默认配置项：hash-max-ziplist-value 64

3.list-max-ziplist-size
说明：ziplist列表最大值，默认存在五项：
-5:最大大小:64 Kb <——不建议用于正常工作负载
-4:最大大小:32 Kb <——不推荐
-3:最大大小:16 Kb <——可能不推荐
-2:最大大小:8 Kb<——很好
-1:最大大小:4 Kb <——好
默认配置项：list-max-ziplist-size -2

4.list-compress-depth
说明： 一个quicklist两端不被压缩的节点个数。0: 表示都不压缩。这是Redis的默认值，1: 表示quicklist两端各有1个节点不压缩，中间的节点压缩。3: 表示quicklist两端各有3个节点不压缩，中间的节点压缩。
默认配置项：list-compress-depth 0

5.set-max-intset-entries
说明：当集合中的元素全是整数,且长度不超过set-max-intset-entries(默认为512个)时,redis会选用intset作为内部编码，大于512用set。
默认配置项：set-max-intset-entries 512

6.zset-max-ziplist-entries&zset-max-ziplist-value
说明：当有序集合的元素小于zset-max-ziplist-entries配置(默认是128个),同时每个元素的值都小于zset-max-ziplist-value(默认是64字节)时,Redis会用ziplist来作为有序集合的内部编码实现,ziplist可以有效的减少内存的使用。
默认配置项：zset-max-ziplist-entries 128
zset-max-ziplist-value 64

7.hll-sparse-max-bytes
说明：value大小 小于等于hll-sparse-max-bytes使用稀疏数据结构（sparse），大于hll-sparse-max-bytes使用稠密的数据结构（dense）。
默认配置项：hll-sparse-max-bytes 3000

8.stream-node-max-bytes&stream-node-max-entries
说明：Streams单个节点的字节数，以及切换到新节点之前可能包含的最大项目数。
默认配置项：stream-node-max-bytes 4096
stream-node-max-entries 100

9.activerehashing
说明：主动重新散列每100毫秒CPU时间使用1毫秒，以帮助重新散列主Redis散列表（将顶级键映射到值）。
默认配置项：activerehashing yes

10.client-output-buffer-limit normal
说明：对客户端输出缓冲进行限制可以强迫那些不从服务器读取数据的客户端断开连接，用来强制关闭传输缓慢的客户端。
默认配置项：client-output-buffer-limit normal 0 0 0

11.client-output-buffer-limit replica
说明：对于slave client和MONITER client，如果client-output-buffer一旦超过256mb，又或者超过64mb持续60秒，那么服务器就会立即断开客户端连接。
默认配置项：client-output-buffer-limit replica 256mb 64mb 60

12.client-output-buffer-limit pubsub
说明：对于pubsub client，如果client-output-buffer一旦超过32mb，又或者超过8mb持续60秒，那么服务器就会立即断开客户端连接。
默认配置项：client-output-buffer-limit pubsub 32mb 8mb 60

13.client-query-buffer-limit
说明：客户端查询缓冲区累积新命令。 默认情况下，它被限制为固定数量，以避免协议失步（例如由于客户端中的错误）将导致查询缓冲区中的未绑定内存使用。 但是，如果您有非常特殊的需求，可以在此配置它，例如我们巨大执行请求。
默认配置项：client-query-buffer-limit 1gb

14.proto-max-bulk-len
说明：在Redis协议中，批量请求（即表示单个字符串的元素）通常限制为512 MB。 但是，您可以在此更改此限制。
默认配置项：proto-max-bulk-len 512mb

15.hz
说明：默认情况下，hz设置为10.提高值时，在Redis处于空闲状态下，将使用更多CPU。范围介于1到500之间，大多数用户应使用默认值10，除非仅在需要非常低延迟的环境中将此值提高到100。
默认配置项：hz 10

16.dynamic-hz
说明：启用动态HZ时，实际配置的HZ将用作基线，但是一旦连接了更多客户端，将根据实际需要使用配置的HZ值的倍数。
默认配置项：dynamic-hz yes

17.aof-rewrite-incremental-fsync
说明：当一个子进程重写AOF文件时，如果启用下面的选项，则文件每生成32M数据会被同步。
默认配置项：aof-rewrite-incremental-fsync yes

18.rdb-save-incremental-fsync
说明：当redis保存RDB文件时，如果启用了以下选项，则每生成32 MB数据将对文件进行fsync。 这对于以递增方式将文件提交到磁盘并避免大延迟峰值非常有用。
默认配置项：rdb-save-incremental-fsync yes

### ###ACTIVE DEFRAGMENTATION（活跃的碎片整理）###（了解）

**1.activedefrag **
说明：是否启用碎片整理
默认配置项：activedefrag no

2.active-defrag-ignore-bytes
说明：启动活动碎片整理的最小碎片浪费量
默认配置项：active-defrag-ignore-bytes 100mb

3.active-defrag-threshold-lower
说明：启动碎片整理的最小碎片百分比
默认配置项：active-defrag-threshold-lower 10

4.active-defrag-threshold-upper
说明：使用最大消耗时的最大碎片百分比
默认配置项：active-defrag-threshold-upper 100

5.active-defrag-cycle-min
说明：在CPU百分比中进行碎片整理的最小消耗
默认配置项：active-defrag-cycle-min 1

6.active-defrag-cycle-max
说明：在CPU百分比达到最大值时，进行碎片整理
默认配置项：active-defrag-cycle-max 25

7.active-defrag-max-scan-fields
说明：从set / hash / zset / list 扫描的最大字段数
默认配置项：active-defrag-max-scan-fields 1000

8.jemalloc-bg-thread
说明：默认情况下，用于清除的Jemalloc后台线程是启用的。
默认配置项：jemalloc-bg-thread yes
