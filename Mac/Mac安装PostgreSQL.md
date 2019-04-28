# Mac安装PostgreSQL

## 安装

[参考文档1](https://www.jianshu.com/p/354442add14f )
[参考文档2](https://www.cnblogs.com/kaituorensheng/p/4667160.html)

已经设置为开机启动。

## 初始化数据库

第一次安装成功后，需要指定一个目录作为数据库的本地存放目录。

```bash
initdb /Users/zhusheng/LocalDB/LocalPostgreSQL -E utf8
```

指定 "/Users/zhusheng/LocalDB/LocalPostgreSQL" 为 PostgreSQL 的配置数据存放目录，并且设置数据库数据编码是 utf8，更多配置信息可以 initdb --help 查看。

示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/postgresql/01.png)

## 使用

- 查看数据库

我们可以在没有连接数据库的情况下，使用下面的指令查看有哪些数据库，我们看到已经有了4个数据库，Owner都是zhusheng，也就是我的电脑用户，也是系统默认的。

```bash
psql -l
````

示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/postgresql/02.png)

如果我们已经进入了数据库，查看数据库的指令如下：

```bash
\l
```

示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/postgresql/04.png)

- 进入数据库

默认我们的数据库都是属于当前系统用户名

```bash
psql -U zhusheng
```

示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/postgresql/03.png)

- 连接数据库

```bash
\c <dbname>
```

示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/postgresql/05.png)

- 创建数据库

```bash
CREATE DATABASE <dbname>;
```

- 表操作

```bash
\d
```

示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/postgresql/06.png)

- 删除数据库

```bash
DROP DATABASE <dbname>;
```

示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/postgresql/07.png)

- 创建用户

```bash
create user db_user1 password '111111';
```

我现在的用户：
用户1:zhusheng，密码:空
用户2:postgres，密码：111111