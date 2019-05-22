# Hive外部表

## 什么是外部表？
先有数据在HDFS，而且数据在HDFS上的位置也不是Hive存储数据的默认位置，然后创建外部表和数据存储位置关连起来，从而实现使用Hive来管理数据。

- 注意

数据存储路径下的数据可以包含很多文件，但是只有创建的表的字段信息和数据的格式是一致的才能进行管理。

- 指定外部表

通过external指定为外部表，TBLS type=EXTERNAL_TABLE

## 创建外部表

创建表stubak

```bash
create external table stubak (id int, name string) row format delimited fields terminated by '\t' location '/stubak';
```

创建表td_ext

```bash
create external table td_ext(id bigint, account string, income double, expenses double, time string) row format delimited fields terminated by '\t' location '/td_ext';
```

## 关联数据

模拟数据：`/data/`,如果没有数据，可以模拟先上传一些数据：

```bash
hive> dfs -mkdir /data;
hive> dfs -put /home/zhusheng/student.txt /data/;
hive> dfs -put /home/zhusheng/student.txt /data/a.txt;
hive> dfs -put /home/zhusheng/student.txt /data/b.txt;
```

效果图如下：

![32.png](https://upload-images.jianshu.io/upload_images/5637154-e0382350f1c2aac6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

创建外部表并关连HDFS目录

```bash
create external table ext_student (id int, name string) row format delimited fields terminated by '\t' location '/data';
select * from ext_student;
```

无论是外部表还是内部表，HDFS目录对应的是Hive的数据表，放在改目录下的符合表格式的文件的内容都会被查询出来。我们通过HDFS shell向该目录上传数据文件，不做其它任何操作，通过hive shell就可以操作该目录下的文件。    
