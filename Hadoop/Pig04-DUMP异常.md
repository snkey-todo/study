---
title: Pig04-DUMP异常
date: 2018-03-05 11:50:19
tags: "Pig"
---
# Pig04-DUMP异常

## 异常说明

在执行Pig DUMP指令时出现了如下异常信息

![image](https://raw.githubusercontent.com/zhusheng/blog/master/88.png)

DUMP指令会将语句转换成MapReduce任务执行。

<!--more-->

## 异常分析

10020端口连接异常

## 解决方法

参考文章：http://www.linuxidc.com/Linux/2015-02/113645.htm

我们在huatec01的配置文件map-site.xml中增加如下信息：

```
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

# 拓展

10020是历史服务器端口，19888是历史服务器的历史任务UI端口，我们在上面配置了， 可以在浏览器直接查看，截图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/91.png)

从图中，我们可以看到所有的历史Job信息，历史Job的数量可以通过修改配置文件`map-site.xml`进行配置。

```bash
<property>
    <name>mapreduce.jobhistory.joblist.cache.size</name>
    <value>20000</value>
</property>
```
