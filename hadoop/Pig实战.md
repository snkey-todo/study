# Pig实战

## 示例1-分步骤执行

1. 拷贝数据到Pig

```
grunt> copyFromLocal /home/zhusheng/student.txt student.txt
```
效果图如下：

![79.png](https://upload-images.jianshu.io/upload_images/5637154-2bd72b5b0014c797.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

<!--more-->

2. 加载数据

```
grunt> A =LOAD 'student.txt' USING PigStorage(',') AS (id:int, name, email, score:int);
```

效果图如下：
![80.png](https://upload-images.jianshu.io/upload_images/5637154-3bad15b0453c0132.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3. 取出所需属性

```
grunt> B = FOREACH A GENERATE name,score;
```

效果图如下：

![81.png](https://upload-images.jianshu.io/upload_images/5637154-11ac3fa466c68c35.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

4. 去除重复的记录

```
grunt> C = DISTINCT B;
```

效果图如下：

![82.png](https://upload-images.jianshu.io/upload_images/5637154-c28c481e7118ecd9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

5. 分组

```
grunt> D = FOREACH ( GROUP C BY name ) GENERATE group AS name, COUNT(C);
grunt> E = FOREACH ( GROUP C BY name ) GENERATE group AS name, SUM(C.score);
grunt> F = GROUP C By name;
```

效果图如下：

![83.png](https://upload-images.jianshu.io/upload_images/5637154-59d9f3c6bda98f8c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

6. 输出到屏幕

```
grunt> DUMP D;
```

这将会执行MapReduce任务，运行结果如下：

![84.png](https://upload-images.jianshu.io/upload_images/5637154-ef3bd2e75e1d8f67.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

7. 保存结果到文件

```
STORE F INTO '/home/zhusheng/student.rel' USING PigStorage();
```
我本以为结果会保存在Linux上，所以给了一个Linux路径，结果保存到了HDFS上，我在HDFS上找到了它。

效果图如下：

![85.png](https://upload-images.jianshu.io/upload_images/5637154-62b6889c77b46f7b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 示例2:Pig脚本

我们将grunt语句写到pig脚本文件`student.pig`中

```
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

![86.png](https://upload-images.jianshu.io/upload_images/5637154-80c58a412ad40f7f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

执行脚本

```
pig student.pig
```

查看结果

![87.png](https://upload-images.jianshu.io/upload_images/5637154-a13201fbbeb43842.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
