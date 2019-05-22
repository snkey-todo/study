# Hive分区表

## 什么是分区表？

就是使用分区字段对数据进行分区，方便快速查找数据。
比如：按年份进行分区，查找数据时，可以根据年份快速定位到要查询的数据。

## 普通表和分区表区别

有大量数据增加的需要建分区表，提高数据处理效率

## 创建分区表

创建表book

```
create table book (id bigint, name string) partitioned by (pubdate string) row format delimited fields terminated by '\t'; 
```

创建表td_part

```
create table td_part(id bigint, account string, income double, expenses double, time string) partitioned by (logdate string) row format delimited fields terminated by '\t';
```

## 创建分区表并加载数据

创建表member_address

```
create table member_address(address_id int, member_id int, province string, city string, region string, addr string, mobile string, receiver string, create_time string, modify_time string) partitioned by (address string) row format delimited fields terminated by '\t'; 
```

加载数据

```
load data local inpath '/home/member_address_hlj' overwrite into table member_address partition(address="HeiLongjiang");
load data local inpath '/home/member_address_hn' overwrite into table member_address partition(address="HuNan");
load data local inpath '/home/member_address_gd' overwrite into table member_address partition(address="GuangDong");
```

删除分区表数据时，需要先删除分区

```
ALTER TABLE member_address DROP IF EXISTS PARTITION(address="HLJS");
ALTER TABLE member_address DROP IF EXISTS PARTITION(address="黑龙江省");
```

## 创建外部分区表

创建表ext_beauties

```
create external table ext_beauties (id int, name string, size double)  partitioned by (nation string) row format delimited fields terminated by '\t' location '/beauty';
```

执行完该语句，会首先在mysql上保存该表的元数据信息，然后在hdfs上创建目录`beauty`，该目录对应`ext_beauties表`，beauty目录保存的是ext_beauties表的数据。表创建完成后，有四个字段：id\name\size\nation。


## 示例

第一步：模拟数据

```
[root@huatec01 home]# hadoop fs -mkdir /member_address
[root@huatec01 home]# hadoop fs -mkdir /member_address/HeiLongjiang
[root@huatec01 home]# hadoop fs -mkdir /member_address/HuNan
[root@huatec01 home]# hadoop fs -mkdir /member_address/GuangDong
```

第二步：创建外部分区表并关联数据

```
create external table ext_member_address(address_id int, member_id int, province string, city string, region string, addr string, mobile string, receiver string, create_time string, modify_time string) partitioned by (address string) row format delimited fields terminated by '\t' location '/member_address'; 
```

第三步：添加分区

```
alter table ext_member_address add partition(address="HeiLongjiang") location '/member_address/HeiLongjiang';
alter table ext_member_address add partition(address="HuNan") location '/member_address/HuNan';
alter table ext_member_address add partition(address="GuangDong") location '/member_address/GuangDong';
```

第四步：加载数据到分区表

```
 load data local inpath '/home/zhusheng/beauty.c' into table ext_beauties partition (nation = 'China'); 
 load data local inpath '/home/zhusheng/beauty.j' into table ext_beauties partition (nation = 'Japan'); 
load data local inpath '/home/zhusheng/beauty.u' into table ext_beauties partition (nation = 'U.S.A');
```

我们到浏览器查看效果图：

![33.png](https://upload-images.jianshu.io/upload_images/5637154-8c76bc72a15d3f2d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


第五步：查询数据

```
select * from ext_beauties;
select * from ext_beauties where nation ='China';    
```
第六步：扩展

我们手动在HDFS里面创建nation=China文件夹，将beauty.c放入该目录，然后通知元数据表。

```
hive> alter table ext_beauties add partition(nation='China') location '/beauty/nation=China';
hive> alter table ext_beauties add partition(nation='Japan') location '/beauty/nation=Japan';
hive> alter table ext_beauties add partition(nation='U.S.A') location '/beauty/nation=U.S.A';
```
