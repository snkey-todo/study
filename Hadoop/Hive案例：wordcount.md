# Hive07-wordcount案例

## 启动集群

启动zookeeper+hadoop集群

```bash
[root@huatec01 ~]# jps
2035 NameNode
2532 Jps
2454 ResourceManager
2333 DFSZKFailoverController
[root@huatec01 ~]# 
```

## 准备数据源

在本地新建两个文件wc1.txt、wc2.txt，内容格式如下：

```bash
username zhaoming
username limei
...
```

单词之间的分隔符为' '，也就是一个空格。然后将两个文件上传到huatec01:/home/input/目录下，因为我们的Hive就安装在huatec01上。

```bash
➜  项目6 scp wc* root@huatec01:/home/input
root@huatec01's password: 
wc1.txt                                       100%  186   149.4KB/s   00:00    
wc2.txt                                       100%  180   221.7KB/s   00:00    
➜  项目6 
```

然后我们将数据上传到HDFS上,我们直接将input文件夹上传到HDFS根目录。

```bash
[root@huatec01 ~]# hadoop fs -put /home/input /
[root@huatec01 ~]# hadoop fs -ls /input
Found 2 items
-rw-r--r--   3 root supergroup        186 2018-01-10 09:53 /input/wc1.txt
-rw-r--r--   3 root supergroup        180 2018-01-10 09:53 /input/wc2.txt
[root@huatec01 ~]# 
```

## 启动Hive并统计词频

1. 导入数据

```bash
hive> create table docs(line string);
OK
Time taken: 0.456 seconds
hive> load data inpath '/input' overwrite into table docs;
Loading data to table default.docs
OK
Time taken: 0.795 seconds
```

2. 分析数据

编写数据分析Hive QL语句

```bash
hive> create table word_count as
    > select word, count(1) as count from (select explode(split(line, ' ')) as word from docs) 
    > w
    > group by word 
    > order by word;
```
执行效果如下图所示：

![46.png](https://upload-images.jianshu.io/upload_images/5637154-8e59646e3cd10132.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

从图中我们可以看出，我们的Hive QL语句转换为了MapReduce任务，最后的数据保存到一个新的表“word_count”中，我们查询表数据如下所示：

```bash
hive> select * from word_count;
OK
caolijie	1
fanye	3
limei	1
shaobing	4
username	20
wangxiargling	3
wujing	1
zhaoming	2
zhaoyanhui	3
zhusheng	2
Time taken: 0.152 seconds, Fetched: 10 row(s)
```

我们看到测试结果是成功的，我们的词频统计已经完成了，完成了编写MapReduce代码相同的功能。

