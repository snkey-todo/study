# Hive桶表

## 什么是桶表

在前面，我们讲到了内部表和外部表，以及使用分区表对数据进行细分管理。其实对于每一个表或者分区，Hive还可以进行更为细颗粒的数据细分划分和管理，也就是桶（Bucket）。Hive也是针对某一列进行桶的组织，Hive采用对列值哈希，然后除以桶的个数求余的方式决定该条记录存放在哪个桶当中。

## 采用桶表的理由

把表（或者分区）组织成桶（Bucket）有两个理由：

（1）获得更高的查询处理效率。桶为表加上了额外的结构，Hive 在处理有些查询时能利用。这个结构。具体而言，连接两个在（包含连接列的）相同列上划分了桶的表，可以使用Map 端连接 （Map-side join）高效的实现。比如JOIN操作。对于JOIN操作两个表有一个相同的列，如果对这两个表都进行了桶操作。那么将保存相同列值的桶进行JOIN操作就可以，可以大大较少JOIN的数据量。

（2）使取样（sampling）更高效。在处理大规模数据集时，在开发和修改查询的阶段，如果能在数据集的一小部分数据上试运行查询，会带来很多方便。

## 应用案例

桶表是基于已有的数据进行桶表操作的。

1. 我们先创建一个外部表，关联到相关数据作为已有数据。

```bash
create external table order_log (order_id int, sn string, member_id int, status int, payment_id int, logi_id int, total_amount double, address_id int, create_time string, modify_time string) 
row format delimited fields terminated by '\t' location '/mobileshop ';
```

示意图如下：
![34.png](https://upload-images.jianshu.io/upload_images/5637154-c79fe45980d2918d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2. 接下来，我们创建一个空的桶表

```
create table if not exists bk_order_log (order_id int, sn string, member_id int, status int, payment_id int, logi_id int, total_amount double, address_id int, create_time string, modify_time string) 
clustered by(order_id) into 4 buckets 
row format delimited fields terminated by '\t' ;
```

示意图如下：
![35.png](https://upload-images.jianshu.io/upload_images/5637154-d2c5abfb268c5b1b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3. 最后，我们将数据导入到桶表中，并分桶显示

```bash
set hive.enforce.bucketing = true;
insert into table bk_order_log select * from order_log;
```

示意图如下：
![36.png](https://upload-images.jianshu.io/upload_images/5637154-8cf575bda34ffdb3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

HDFS桶表结构如下：

![37.png](https://upload-images.jianshu.io/upload_images/5637154-42568a02c466c0c8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 桶表抽样

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
![38.png](https://upload-images.jianshu.io/upload_images/5637154-67cc41889953133b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

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

1. 随机从某表中取5条数据：

```bash
select * from bk_order_log order by rand() limit 5;
```

2. 数据块取样 (TABLESAMPLE (n PERCENT))抽取表大小的n%

```bash
select * from bk_order_log TABLESAMPLE (10 PERCENT);
```


3. 指定数据大小取样(TABLESAMPLE (nM)) M为MB单位

```bash
select * from bk_order_log TABLESAMPLE (10M);
```

4. 指定抽取条数(TABLESAMPLE (n ROWS))

```bash
select * from bk_order_log TABLESAMPLE (5 ROWS);
```

## 桶表高级应用案例-分区分桶表

### 分区分桶表

我们知道分区和分桶都是对数据的细分管理，如果两者结合使用，肯定是有层级和先后顺序的。实际也是如此，我们的数据是先分区管理，对每个分区的数据我们可以使用分桶进行管理。也就是说分区分桶表，其中的分桶必然在最末端的分区中。

### 实操示例

1. 我们创建一个外部表并导入数据作为基础数据

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
![39.png](https://upload-images.jianshu.io/upload_images/5637154-13c3b869fa8f443c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2. 创建分区分桶表

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
![40.png](https://upload-images.jianshu.io/upload_images/5637154-2c421291a9af2ef6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后我们导入外部表的基础数据，进行分区+分桶细分管理。

说明：

```bash
partitioned by(contry string,city string)
clustered by(f1) into 5 buckets
```

先写分区操作、在设置分桶操作

3. 导入数据到分区分桶表

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
![41.png](https://upload-images.jianshu.io/upload_images/5637154-17f3cb653f53a96e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

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

![42.png](https://upload-images.jianshu.io/upload_images/5637154-c82633ad6cb30550.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们以分区China-分区上海为例，如图所示：

![43.png](https://upload-images.jianshu.io/upload_images/5637154-a323579586cf8f32.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 建议

经过实操发现，分区的字段值如果是中文，会出现异常，比如上图中的二级分区“city=上海”,虽然在HDFS是陈工显示的，但是同时会在HDFS页面显示如下异常信息：

```bash
Path does not exist on HDFS or WebHDFS is disabled. Please check your path or enable WebHDFS
```
所以，如果分区数据中有中文名称，建议先清洗数据，将其名称全部替换为相应的英文名称，然后在进行数据分析、抽样操作。

