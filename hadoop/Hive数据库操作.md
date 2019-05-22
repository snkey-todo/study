# Hive数据库操作

键入“hive”，启动hive的cli交互模式，然后进行以下操作。

## 创建数据库

```bash
hive> CREATE DATABASE IF NOT EXISTS userdb;
OK
Time taken: 0.983 seconds
hive>
```

## 删除数据库

```bash
hive> DROP DATABASE IF EXISTS userdb;
OK
Time taken: 0.711 seconds
hive>
```

## 显示数据库

```bash
hive> show databases;
OK
default
hive_jdbc_test
Time taken: 0.089 seconds, Fetched: 2 row(s)
hive>
```
