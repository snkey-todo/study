---
title: Pig03-实战
date: 2018-03-05 10:49:34
tags: "Pig"
---
# Pig03-实战

## 示例1-分步骤执行

1. 拷贝数据到Pig

```bash
grunt> copyFromLocal /home/zhusheng/student.txt student.txt
```
效果图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/79.png)

<!--more-->

2. 加载数据

```bash
grunt> A =LOAD 'student.txt' USING PigStorage(',') AS (id:int, name, email, score:int);
```

效果图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/80.png)

3. 取出所需属性

```bash
grunt> B = FOREACH A GENERATE name,score;
```

效果图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/81.png)

4. 去除重复的记录

```bash
grunt> C = DISTINCT B;
```

效果图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/82.png)

5. 分组

```bash
grunt> D = FOREACH ( GROUP C BY name ) GENERATE group AS name, COUNT(C);
grunt> E = FOREACH ( GROUP C BY name ) GENERATE group AS name, SUM(C.score);
grunt> F = GROUP C By name;
```

效果图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/83.png)

6. 输出到屏幕

```bash
grunt> DUMP D;
```

这将会执行MapReduce任务，运行结果如下：


![image](https://raw.githubusercontent.com/zhusheng/blog/master/84.png)

7. 保存结果到文件

```bash
STORE F INTO '/home/zhusheng/student.rel' USING PigStorage();
```
我本以为结果会保存在Linux上，所以给了一个Linux路径，结果保存到了HDFS上，我在HDFS上找到了它。

效果图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/85.png)




## 示例2:Pig脚本

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
