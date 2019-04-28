# Mac安装MongoDB

## 安装

[官方安装文档](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/)

示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/mongodb/01.png)

安装指令

```bash
brew tap mongodb/brew
brew install mongodb-community@4.0
```

执行效果图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/mongodb/02.png)

说明：我已经将mongodb安装成系统服务，无需手动去启动。

## 基本操作

- 连接mongodb 

```bash
mongo
```

- 创建数据库datapoint  

```bash
use datapoint
```