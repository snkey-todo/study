# Docker大数据

## harisekhon大数据

在编写教材的过程中，为了⽅便测试我的案例代码，我需要在⾃⼰的电脑上搭建大数据环境，一步步去搭建无疑是耗时的，也需要去关注很多大数据的操作，不是很好，⽽使⽤Docker⽆疑是最好的选择，harisekhon开源了很多这⽅⾯的镜像。

[Docker harisekhon](https://hub.docker.com/r/harisekhon/)

[Github Dockerfile](https://github.com/HariSekhon/Dockerfiles)

harisekhon提供了很多关于⼤数据的镜像，包含Hadoop、Zookeeper、HBase、
Hive、Kafka、Spark等。 这⾥我使⽤的都是单⼀的容器环境，也就是单节点环境。多容器环境需要⽤到Compose编排⼯具，它可以创建⼀个项⽬包含多个容器。

## 镜像搜索

- docker默认关键词搜索

```bash
docker search harisekhon
```

说明：只能提供最多25个镜像，这是docker在搜索时做出的限制。

- harisekhon/pytools搜索镜像

搜索某个关键词的全部镜像列表,harisekhon制作了⼀个脚本dockerhub_search.py ⽤于查看搜索的全部的相关镜像。

```bash
# 查看帮助
docker	run	harisekhon/pytools	  dockerhub_search.py	harisekhon	--help
# 搜索关键词为harisekhon的镜像
docker	run	harisekhon/pytools	  dockerhub_search.py	harisekhon
# 搜索关键词为centos的镜像
docker	run	harisekhon/pytools	  dockerhub_search.py	centos
# 指定数量
docker	run	harisekhon/pytools	  dockerhub_search.py	centos -n 10
```

搜索镜像的全部tag列表。harisekhon/pytools还包含一个dockerhub_show_tags.py 脚本⽤于显示镜像的tag。

```bash
# 显示全部tag
docker	run	harisekhon/pytools	  dockerhub_show_tags.py	centos
```

## harisekhon/Dockerfiles

harisekhon提供了很多大数据的docker镜像，每个镜像的启动方式有2种：

1. docker-compose
2. make run

两种方式都不需要记复杂的指令，所有的镜像都适用。

## 启动Hadoop

方式1:

```bash
cd hadoop
docker-compose up
```

方式2:

```bash
cd hadoop
make run
```

HDFS:http://localhost:50070

MapReduce:http://localhost:8088/

## 启动HBase

方式1:

```bash
cd hbase
docker-compose up
```

方式2:

```bash
cd hbase
make run
```

HBase管理页面:http://localhost:16010

##启动Spark服务

方式1:

```bash
cd spark
docker-compose up
```

方式2:

```bash
cd spark
make run
```

Spark Master:http://localhost:8088/

Spark Worker:http://localhost:8081/

Spark UI:http://localhost:4040/

