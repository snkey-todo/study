# Hive表操作

- Hive数据库
- Hive内部表
- Hive分区表
- Hive桶表

## Hive数据库

- 创建数据库

```bash
hive> CREATE DATABASE IF NOT EXISTS userdb;
OK
Time taken: 0.983 seconds
hive>
```

- 删除数据库

```bash
hive> DROP DATABASE IF EXISTS userdb;
OK
Time taken: 0.711 seconds
hive>
```

- 显示数据库

```bash
hive> show databases;
OK
default
hive_jdbc_test
Time taken: 0.089 seconds, Fetched: 2 row(s)
hive>
```

## Hive内部表

- 什么是内部表？

就是我们先创建元数据表，然后导入数据，这样的表就是内部表。

在元数据库中查看其表类型：TBLS type=MANAGE_TABLE

- 执行建表语句的过程

当我们在hive shell下执行建表语句，会先在mysql下创建元数据表，元数据表存储表的元数据信息，如：表类型、表数据在HDFS上的存储位置，表的字段信息、表的分区信息等等，HDFS上的默认存储位置为：/user/hive/warehouse/

- 创建内部表

user_info表

```bash
hive> use default;
OK
Time taken: 0.07 seconds
hive> CREATE TABLE IF NOT EXISTS user_info (id bigint, account string, name string, age int) row format delimited fields terminated by '\t';
OK
Time taken: 0.629 seconds
hive>
```

trade_detail表

```bash
CREATE TABLE IF NOT EXISTS trade_detail (id bigint, account string, income double, expenses double, time string) row format delimited fields terminated by '\t';
```

ms_order表

```bash
CREATE TABLE IF NOT EXISTS ms_order(id bigint, sn string, member_id int, status int, payment_id int, logi_id int, total_accoccount double, address_id int, createtime string, modifytime string) row format delimited fields terminated by '\t';
```

创建一个result表保存前一个sql执行的结果

```bash
create table result row format delimited fields terminated by '\t' as select t2.account, t2.name, t1.income, t1.expenses, t1.surplus from user_info t2 join (select account, sum(income) as income, sum(expenses) as expenses, sum(income-expenses) as surplus from trade_detail group by account) t1 on (t1.account = t2.account);
```

user表

```bash
create table user (id int, name string) row format delimited fields terminated by '\t'
```

- 导入MySQL数据到Hive

在前面我们创建的两个空表，我们将本地数据库的数据导入到相应的Hive表中。

导入mac下的mobileshop数据库的数据到ms_order

```bash
sqoop import --connect jdbc:mysql://192.168.8.3:3306/mobileshop --username root --password admin888 --table ms_order --hive-import --hive-overwrite --hive-table ms_order --fields-terminated-by '\t'
```

![image](https://raw.githubusercontent.com/zhusheng/blog/master/31.png)

- 导入本地数据到Hive

```bash
load data local inpath '/zhusheng/home/user.txt' into table user;  
```

## Hive分区表

- 什么是分区表？

就是使用分区字段对数据进行分区，方便快速查找数据。
比如：按年份进行分区，查找数据时，可以根据年份快速定位到要查询的数据。

- 普通表和分区表区别

有大量数据增加的需要建分区表，提高数据处理效率

- 创建分区表

创建表book

```bash
create table book (id bigint, name string) partitioned by (pubdate string) row format delimited fields terminated by '\t'; 
```

创建表td_part

```bash
create table td_part(id bigint, account string, income double, expenses double, time string) partitioned by (logdate string) row format delimited fields terminated by '\t';
```

- 创建分区表并加载数据

创建表member_address

```bash
create table member_address(address_id int, member_id int, province string, city string, region string, addr string, mobile string, receiver string, create_time string, modify_time string) partitioned by (address string) row format delimited fields terminated by '\t'; 
```

加载数据

```bash
load data local inpath '/home/member_address_hlj' overwrite into table member_address partition(address="HeiLongjiang");
load data local inpath '/home/member_address_hn' overwrite into table member_address partition(address="HuNan");
load data local inpath '/home/member_address_gd' overwrite into table member_address partition(address="GuangDong");
```

删除分区表数据时，需要先删除分区

```bash
ALTER TABLE member_address DROP IF EXISTS PARTITION(address="HLJS");
ALTER TABLE member_address DROP IF EXISTS PARTITION(address="黑龙江省");
```

- 创建外部分区表

创建表ext_beauties

```bash
create external table ext_beauties (id int, name string, size double)  partitioned by (nation string) row format delimited fields terminated by '\t' location '/beauty';
```

执行完该语句，会首先在mysql上保存该表的元数据信息，然后在hdfs上创建目录`beauty`，该目录对应`ext_beauties表`，beauty目录保存的是ext_beauties表的数据。表创建完成后，有四个字段：id\name\size\nation。

### Hive分区表示例

- 第一步：模拟数据

```bash
[root@huatec01 home]# hadoop fs -mkdir /member_address
[root@huatec01 home]# hadoop fs -mkdir /member_address/HeiLongjiang
[root@huatec01 home]# hadoop fs -mkdir /member_address/HuNan
[root@huatec01 home]# hadoop fs -mkdir /member_address/GuangDong
```

- 第二步：创建外部分区表并关联数据

```bash
create external table ext_member_address(address_id int, member_id int, province string, city string, region string, addr string, mobile string, receiver string, create_time string, modify_time string) partitioned by (address string) row format delimited fields terminated by '\t' location '/member_address'; 
```

- 第三步：添加分区

```bash
alter table ext_member_address add partition(address="HeiLongjiang") location '/member_address/HeiLongjiang';
alter table ext_member_address add partition(address="HuNan") location '/member_address/HuNan';
alter table ext_member_address add partition(address="GuangDong") location '/member_address/GuangDong';
```

- 第四步：加载数据到分区表

```bash
 load data local inpath '/home/zhusheng/beauty.c' into table ext_beauties partition (nation = 'China'); 
 load data local inpath '/home/zhusheng/beauty.j' into table ext_beauties partition (nation = 'Japan'); 
load data local inpath '/home/zhusheng/beauty.u' into table ext_beauties partition (nation = 'U.S.A');
```

我们到浏览器查看效果图：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/33.png)

- 第五步：查询数据

```bash
select * from ext_beauties;
select * from ext_beauties where nation ='China';    
```

- 扩展

我们手动在HDFS里面创建nation=China文件夹，将beauty.c放入该目录，然后通知元数据表。

```bash
hive> alter table ext_beauties add partition(nation='China') location '/beauty/nation=China';
hive> alter table ext_beauties add partition(nation='Japan') location '/beauty/nation=Japan';
hive> alter table ext_beauties add partition(nation='U.S.A') location '/beauty/nation=U.S.A';
```

## Hive外部表

- 什么是外部表？
先有数据在HDFS，而且数据在HDFS上的位置也不是Hive存储数据的默认位置，然后创建外部表和数据存储位置关连起来，从而实现使用Hive来管理数据。

==注意==

数据存储路径下的数据可以包含很多文件，但是只有创建的表的字段信息和数据的格式是一致的才能进行管理。

==指定外部表==

通过external指定为外部表，TBLS type=EXTERNAL_TABLE

- 创建外部表

创建表stubak

```bash
create external table stubak (id int, name string) row format delimited fields terminated by '\t' location '/stubak';
```

创建表td_ext

```bash
create external table td_ext(id bigint, account string, income double, expenses double, time string) row format delimited fields terminated by '\t' location '/td_ext';
```

- 关联数据

模拟数据：`/data/`,如果没有数据，可以模拟先上传一些数据：

```bash
hive> dfs -mkdir /data;
hive> dfs -put /home/zhusheng/student.txt /data/;
hive> dfs -put /home/zhusheng/student.txt /data/a.txt;
hive> dfs -put /home/zhusheng/student.txt /data/b.txt;
```

效果图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/32.png)

- 创建外部表并关连HDFS目录

```bash
create external table ext_student (id int, name string) row format delimited fields terminated by '\t' location '/data';
select * from ext_student;
```

无论是外部表还是内部表，HDFS目录对应的是Hive的数据表，放在改目录下的符合表格式的文件的内容都会被查询出来。我们通过HDFS shell向该目录上传数据文件，不做其它任何操作，通过hive shell就可以操作该目录下的文件。

## Hive桶表

- 什么是桶表

在前面，我们讲到了内部表和外部表，以及使用分区表对数据进行细分管理。其实对于每一个表或者分区，Hive还可以进行更为细颗粒的数据细分划分和管理，也就是桶（Bucket）。Hive也是针对某一列进行桶的组织，Hive采用对列值哈希，然后除以桶的个数求余的方式决定该条记录存放在哪个桶当中。

- 采用桶表的理由

把表（或者分区）组织成桶（Bucket）有两个理由：

（1）获得更高的查询处理效率。桶为表加上了额外的结构，Hive 在处理有些查询时能利用。这个结构。具体而言，连接两个在（包含连接列的）相同列上划分了桶的表，可以使用Map 端连接 （Map-side join）高效的实现。比如JOIN操作。对于JOIN操作两个表有一个相同的列，如果对这两个表都进行了桶操作。那么将保存相同列值的桶进行JOIN操作就可以，可以大大较少JOIN的数据量。

（2）使取样（sampling）更高效。在处理大规模数据集时，在开发和修改查询的阶段，如果能在数据集的一小部分数据上试运行查询，会带来很多方便。

### 桶表示例

桶表是基于已有的数据进行桶表操作的。

1、我们先创建一个外部表，关联到相关数据作为已有数据。

```bash
create external table order_log (order_id int, sn string, member_id int, status int, payment_id int, logi_id int, total_amount double, address_id int, create_time string, modify_time string) 
row format delimited fields terminated by '\t' location '/mobileshop ';
```

示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/34.png)

2、接下来，我们创建一个空的桶表

```bash
create table if not exists bk_order_log (order_id int, sn string, member_id int, status int, payment_id int, logi_id int, total_amount double, address_id int, create_time string, modify_time string) 
clustered by(order_id) into 4 buckets 
row format delimited fields terminated by '\t' ;
```

示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/35.png)

3、最后，我们将数据导入到桶表中，并分桶显示

```bash
set hive.enforce.bucketing = true;
insert into table bk_order_log select * from order_log;
```

示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/36.png)

HDFS桶表结构如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/37.png)

### 按桶抽样

桶表也是Hive表的一种，我们同样可以使用“select”等语句进行数据查询，例如“select * from bk_order_log”，除了这些基本的查询操作之外，我们还可以将桶作为查询条件。比如我们对桶表数据进行取样，相关指令格式如下：

```bash
select * from bk_users_log TABLESAMPLE(BUCKET x OUT OF y);
```

其中的x和y是参数，y尽可能是桶表的bucket数的倍数或者因子，而且y必须要大于x，当我们执行相关指令，Hive会根据y决定抽样的比例，x表示从哪个桶开始进行抽样。

例如“clustered by(id) into 16 buckets”，table总共分了16桶，当y=8时，抽取(16/8=)2个bucket的数据。
我们以我们创建的桶表“bk_order_log”为例，我们的桶表有4个桶，那么我们如果抽取同数据呢，常见的抽样操作如下所示：

（1）从bk_order_log分桶表抽出一桶数据：

假设x=2，y=4

```bash
select * from bk_order_log TABLESAMPLE(BUCKET 2 OUT OF 4);
```

示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/38.png)

其实我们看到抽样查询和普通的查询区别就在于我们的数据时样本数据，当数据的基数非常大的时候，我们可以基于抽样的数据进行抽样调查。

后续我会结合我们的“bk_order_log”表，继续给出抽样二桶、四桶、半桶数据的抽样语句，你们可以自己进行执行查看。当然如果我们的桶数非常多的话，我们也可以有更多的抽样选择。

（2）从bk_order_log分桶表抽出二桶数据：

假设x=2，y=2

```bash
select * from bk_order_log TABLESAMPLE(BUCKET 2 OUT OF 2);
```

（3）从bk_order_log分桶表抽出四桶数据：

假设x=1，y=1

```bash
select * from bk_order_log TABLESAMPLE(BUCKET 1 OUT OF 1);
```

（4）从bk_order_log分桶表抽出半桶数据：

假设x=1，y=8

```bash
select * from bk_order_log TABLESAMPLE(BUCKET 1 OUT OF 8);
```

除了上述的抽样方式之外，Hive表还可以通过“by rand() limit x”进行指定条数随机取样，通过“TABLESAMPLE (n PERCENT)”进行块取样，通过“TABLESAMPLE (nM)”指定取样数据大小（单位为MB）等等。

### 抽样查询

1、随机从某表中取5条数据：

```bash
select * from bk_order_log order by rand() limit 5;
```

2、数据块取样 (TABLESAMPLE (n PERCENT))抽取表大小的n%

```bash
select * from bk_order_log TABLESAMPLE (10 PERCENT);
```

3、指定数据大小取样(TABLESAMPLE (nM)) M为MB单位

```bash
select * from bk_order_log TABLESAMPLE (10M);
```

4、指定抽取条数(TABLESAMPLE (n ROWS))

```bash
select * from bk_order_log TABLESAMPLE (5 ROWS);
```

### 桶表高级应用案例-分区分桶表

- 分区分桶表

我们知道分区和分桶都是对数据的细分管理，如果两者结合使用，肯定是有层级和先后顺序的。实际也是如此，我们的数据是先分区管理，对每个分区的数据我们可以使用分桶进行管理。也就是说分区分桶表，其中的分桶必然在最末端的分区中。

- 实操示例

1、我们创建一个外部表并导入数据作为基础数据

创建外部表

```bash
create external table if not exists tb_part_bk_users(
f1 string,
f2 string,
f3 string,
contry string,
city string
)
row format delimited fields terminated by'\t';
```

导入数据到外部表

```bash
load data local inpath '/home/par_buc.txt' into table tb_part_bk_users;
```

示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/39.png)

2、创建分区分桶表

```bash
create external table if not exists part_bk_users(
f1 string,
f2 string,
f3 string
)
partitioned by(contry string,city string)
clustered by(f1) into 5 buckets
row format delimited fields terminated by'\t';
```

示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/40.png)

然后我们导入外部表的基础数据，进行分区+分桶细分管理。

说明：先写分区操作、在设置分桶操作

```bash
partitioned by(contry string,city string)
clustered by(f1) into 5 buckets
```

3、导入数据到分区分桶表

混合方式将数据添加到分区分桶表：

（1）打开动态分区设置、设置动态分区模式为非严格模式

```bash
set hive.exec.dynamic.partition=true;
set hive.exec.dynamic.partition.mode=nonstrict;
```

（2）强制多个 reduce 进行输出桶文件

```bash
set hive.enforce.bucketing = true;
```

（3）只能以结果集的方式添加数据到分桶表

```bash
insert into table part_bk_users partition(contry='CA',city) 
select f1,f2,f3,city from tb_part_bk_users where contry='CA';
```

示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/41.png)

同理

```bash
insert into table part_bk_users partition(contry='Japan',city) 
select f1,f2,f3,city from tb_part_bk_users where contry='Japan';
```

```bash
insert into table part_bk_users partition(contry='China',city) 
select f1,f2,f3,city from tb_part_bk_users where contry='China';
```

我们尝试一下中文

```bash
insert into table part_bk_users partition(contry='中国',city) 
select f1,f2,f3,city from tb_part_bk_users where contry='中国';
```

我们去HDFS上查看一下分区分桶表的数据结构

![image](https://raw.githubusercontent.com/zhusheng/blog/master/42.png)

我们以分区China-分区上海为例，如图所示：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/43.png)

### 建议

经过实操发现，分区的字段值如果是中文，会出现异常，比如上图中的二级分区“city=上海”,虽然在HDFS是陈工显示的，但是同时会在HDFS页面显示如下异常信息：

```bash
Path does not exist on HDFS or WebHDFS is disabled. Please check your path or enable WebHDFS
```

所以，如果分区数据中有中文名称，建议先清洗数据，将其名称全部替换为相应的英文名称，然后在进行数据分析、抽样操作。

