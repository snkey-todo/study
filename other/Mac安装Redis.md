# Mac安装Redis

## 下载

https://redis.io/download

## 安装

（1）解压
（2）拷贝到/usr/local

```bash
sudo mv redis-5.0.3 /usr/local
```

（3）编译测试

 ```bash
cd /usr/local/redis-5.0.3
sudo make test
```

（4）编译安装

```bash
sudo make install
```

（5）运行redis

```bash
redis-server
```

## 配置

（1）在redis目录下建立bin，etc，db三个目录

```bash
sudo mkdir bin
sudo mkdir etc
sudo mkdir db
```

（2）把/usr/local/redis/src目录下的mkreleasehdr.sh，redis-benchmark， redis-check-rdb， redis-cli， redis-server拷贝到bin目录。

```bash
sudo cp src/mkreleasehdr.sh bin
sudo cp src/redis-benchmark bin
sudo cp src/redis-check-rdb bin
sudo cp src/redis-cli bin
sudo cp src/redis-server bin
```

（3）拷贝 redis.conf 到 /usr/local/redis/etc下，修改redis.conf

```bash
sudo cp redis.conf etc
vi etc/redis.conf
```

（4）启动服务,进入redis目录，执行如下指令。

```bash
bin/redis-server etc/redis.conf //后台运行
tail -f log-redis.log. //查看日志
```

## 客户端操作

- 进入客户端

```bash
bin/redis-cli
```

示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/redis/01.png)

## 设置密码

- 设置密码
  
修改redis.conf文件，增加如下属性:

```bash
requirepass root
```

- 使用密码登录

```bash
redis-5.0.3 bin/redis-cli
127.0.0.1:6379> keys *
(error) NOAUTH Authentication required.
127.0.0.1:6379> auth root
OK
127.0.0.1:6379> keys *
1) "9561f578-dd4e-4333-8ccc-8f64fb6e7819"
127.0.0.1:6379>
```

示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/redis/02.png)

## 远程访问

指令格式如下

```bash
redis-cli -h <yourIp> -p <yourPort> -a <youPassword>
```

我在华为云上也部署了redis，我可以通过远程方式进行访问：

```bash
redis-cli -h 114.115.179.78 -p 6379 -a root
```

示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/redis/03.png)