# Pig入门与实战

- Big：表
- Tuple：行、记录
- Field：属性

说明：Pig不要求同一个bag里面的各个tuple有相同数量、相同类型的field，也就是说pig的表行结构不固定。

## Pig Latin常用语法

- LOAD...AS：载入数据

示例：

```bash
records = LOAD '/home/zhusheng/sample.txt' 
USING PigStorage("#")
AS(year:chararray, temperature:int, quality:int);
```

说明：USING PigStorage("#")表示使用"#"做为分隔符，如果不指定，默认使用"\t"做为分隔符。

- FILTER...BY：过滤行

示例：

```bash
filtered_records = FILTER records BY temperature != 9999 AND (quality ==0 OR quality ==1);
```

- GROUP... By：分组

示例：

```bash
group_records = GROUP filtered_records BY year;
```

说明：按年分组，一年一条记录

- FOREACH...GENERATE：逐行扫描进行某种处理

示例1：

```bash
for_records = FOREACH group_records GENERATE group;
```

说明：取出年份保存到for_records

示例2:

```bash
max_records = FOREACH group_records GENERATE group，MAX(filtered_records.temperature);
```

说明：取出年份、最大值保存到max_records

- DUMP：将结果显示到屏幕

示例：

```bash
DUMP for_records;
DUMP max_records;
```

- STORE...INTO：将结果保存到文件

示例：

```bash
STORE max_records INTO '/home/zhusheng/result.txt' USING PigStorage();
```

说明：将结果保存到文件，使用默认分隔符。

### 语法示例

**示例1:Hadoop权威指南Pig示例**

![image](https://raw.githubusercontent.com/zhusheng/blog/master/75.png)

上面的示例代码一共有5条pig语句，用分号区分。

- 第一条语句：加载语句
- 第二条语句：过滤语句
- 第三条语句：分组，一年一条记录，类似group by
- 第四条语句：求最大值
- 第五条语句：输出到屏幕

**示例2:CSDN示例**

![image](https://raw.githubusercontent.com/zhusheng/blog/master/76.png)

- 第一条语句：加载文件
- 第二条语句：取出email
- 第三语句：输出结果到文件

## Pig部署

**下载**

[最新版本：pig-0.17.0.tar](http://pig.apache.org)

**安装**

我们安装到一个节点即可，这里我们安装到huatec01节点，安装过程非常简单，解压即可完成安装，然后为其配置一下全局环境变量。

**本地模式运行**

以本地模式运行pig，进入pig shell模式

```bash
pig -x local
```

**MapReduce模式运行**

这也是实际工作模式，连接到Hadoop集群。

第一步：配置MapReduce模式

1、设置PATH
（1）配置java环境变量
（2）配置hadoop环境变量
（3）配置pig环境变量

2、设置PIG_CLASSPATH环境变量

```bash
PIG_CLASSPATH = /huatec/hadoop-2.7.3/conf
```

![image](https://raw.githubusercontent.com/zhusheng/blog/master/77.png)

第二步：修改hosts

配置主机名和ip的映射关系

第三步：启动Pig

```bash
pig
```

效果图如下：
![image](https://raw.githubusercontent.com/zhusheng/blog/master/78.png)

### Pig运行说明

Pig的运行方式有3种：

- 脚本
- Grunt
- 嵌入式，嵌入到其它语言中进行运行。

建议使用Pig Latin语言编写".pig"脚本文件。

1、脚本运行

```bash
pig /home/zhusheng/student.pig
```

2、Grunt运行

指令运行，如LOAD、FOREACH、STORE、DUMP等，见上。

3、嵌入式

略

## Pig实战

### 示例1-分步骤执行

第一步：拷贝数据到Pig

```bash
grunt> copyFromLocal /home/zhusheng/student.txt student.txt
```

效果图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/79.png)

第二步：加载数据

```bash
grunt> A =LOAD 'student.txt' USING PigStorage(',') AS (id:int, name, email, score:int);
```

效果图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/80.png)

第三步：取出所需属性

```bash
grunt> B = FOREACH A GENERATE name,score;
```

效果图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/81.png)

第四步：去除重复的记录

```bash
grunt> C = DISTINCT B;
```

效果图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/82.png)

第五步：分组

```bash
grunt> D = FOREACH ( GROUP C BY name ) GENERATE group AS name, COUNT(C);
grunt> E = FOREACH ( GROUP C BY name ) GENERATE group AS name, SUM(C.score);
grunt> F = GROUP C By name;
```

效果图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/83.png)

第六步：输出到屏幕

```bash
grunt> DUMP D;
```

这将会执行MapReduce任务，运行结果如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/84.png)

第七步：保存结果到文件

```bash
STORE F INTO '/home/zhusheng/student.rel' USING PigStorage();
```

我本以为结果会保存在Linux上，所以给了一个Linux路径，结果保存到了HDFS上，我在HDFS上找到了它。

效果图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/85.png)

### 示例2:Pig脚本

我们将grunt语句写到pig脚本文件`student.pig`中

```bash
A =LOAD 'student.txt' USING PigStorage(',') AS (id:int, name, email, score:int);
B = FOREACH A GENERATE name,score;
C = DISTINCT B;
D = FOREACH ( GROUP C BY name ) GENERATE group AS name, COUNT(C);
E = FOREACH ( GROUP C BY name ) GENERATE group AS name, SUM(C.score);
F = GROUP C By name;

STORE D INTO '/student.rel-d' USING PigStorage();
STORE E INTO '/student.rel-e' USING PigStorage();
STORE F INTO '/student.rel-f' USING PigStorage();
```

截图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/86.png)

执行脚本

```bash
pig student.pig
```

查看结果

![image](https://raw.githubusercontent.com/zhusheng/blog/master/87.png)


## Pig DUMP异常

在执行Pig DUMP指令时出现了如下异常信息

![image](https://raw.githubusercontent.com/zhusheng/blog/master/88.png)

DUMP指令会将语句转换成MapReduce任务执行。

- 异常分析

10020端口连接异常

- 解决方法

参考文章：http://www.linuxidc.com/Linux/2015-02/113645.htm

我们在huatec01的配置文件map-site.xml中增加如下信息：

```bash
<property>
    <name>mapreduce.jobhistory.address</name>
    <value>0.0.0.0:10020</value>
</property>
<property>
    <name>mapreduce.jobhistory.webapp.address</name>
    <value>0.0.0.0:19888</value>
</property>
```

截图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/89.png)

配置完成后，在当前节点手动启动historyserver，也就是历史服务器

```bash
mr-jobhistory-daemon.sh  start historyserver
```

启动完成之后，我们会发现多了一个进程,截图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/90.png)

再次执行DUMP指令，会发现异常消失。

## 拓展

10020是历史服务器端口，19888是历史服务器的历史任务UI端口，我们在上面配置了， 可以在浏览器直接查看，截图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/91.png)

从图中，我们可以看到所有的历史Job信息，历史Job的数量可以通过修改配置文件`map-site.xml`进行配置。

```bash
<property>
    <name>mapreduce.jobhistory.joblist.cache.size</name>
    <value>20000</value>
</property>
```
