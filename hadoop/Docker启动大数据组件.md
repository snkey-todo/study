# Docker启动大数据组件

拉取github项目：

`git clone git@github.com:HariSekhon/Dockerfiles.git`

该项目包含了一系列的大数据组件，如下所示：

>DockerHub public images for Docker & Kubernetes - Hadoop, Kafka, ZooKeeper, HBase, Cassandra, Solr / SolrCloud, Presto, Apache Drill, Nifi, Spark, Mesos, Consul, Riak, Jython, Advanced Nagios Plugins Collection & DevOps Tools repos on Alpine, CentOS, Debian, Fedora, Ubuntu, Superset, H2O, Serf, Alluxio / Tachyon

我们进入想要启动的组件目录下，进行启动：

方式1：使用docker-compose
```
cd hadoop
docker-compose up
```

关闭：
```
cd hadoop
docker-compose down
```

方式2：使用make run
```
cd hadoop
make run
```

方式3：使用指令
```
docker run -ti -p 8020:8020 -p 8032:8032 -p 8088:8088 -p 9000:9000 -p 10020:10020 -p 19888:19888 -p 50010:50010 -p 50020:50020 -p 50070:50070 -p 50075:50075 -p 50090:50090 harisekhon/hadoop
```



