#  Pig介绍

## Pig数据模型

- Big：表
- Tuple：行、记录
- Field：属性

说明：Pig不要求同一个bag里面的各个tuple有相同数量、相同类型的field，也就是说pig的表行结构不固定。

## Pig Latin常用语法

### LOAD...AS：载入数据

示例：

```
records = LOAD '/home/zhusheng/sample.txt' 
USING PigStorage("#")
AS(year:chararray, temperature:int, quality:int);
```

说明：USING PigStorage("#")表示使用"#"做为分隔符，如果不指定，默认使用"\t"做为分隔符。

### FILTER...BY：过滤行

示例：

```
filtered_records = FILTER records BY temperature != 9999 AND (quality ==0 OR quality ==1);
```

### GROUP... By：分组

示例：

```
group_records = GROUP filtered_records BY year;
```
说明：按年分组，一年一条记录

### FOREACH...GENERATE：逐行扫描进行某种处理

示例1：

```
for_records = FOREACH group_records GENERATE group;
```

说明：取出年份保存到for_records

示例2:

```
max_records = FOREACH group_records GENERATE group，MAX(filtered_records.temperature);
```

说明：取出年份、最大值保存到max_records

### DUMP：将结果显示到屏幕

示例：

```
DUMP for_records;
DUMP max_records;
```
### STORE...INTO：将结果保存到文件

示例：

```
STORE max_records INTO '/home/zhusheng/result.txt' USING PigStorage();
```

说明：将结果保存到文件，使用默认分隔符。

## 示例

示例1:Hadoop权威指南Pig示例

![75.png](https://upload-images.jianshu.io/upload_images/5637154-9d70d3d4355a3450.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


上面的示例代码一共有5条pig语句，用分号区分。
- 第一条语句：加载语句
- 第二条语句：过滤语句
- 第三条语句：分组，一年一条记录，类似group by
- 第四条语句：求最大值
- 第五条语句：输出到屏幕

示例2:CSDN示例

![76.png](https://upload-images.jianshu.io/upload_images/5637154-d95016e751b678f8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 第一条语句：加载文件
- 第二条语句：取出email
- 第三语句：输出结果到文件
