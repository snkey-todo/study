# Hadoop与HBase高可用集群搭建（5Node)

生产集群搭建

## 准备工作

集群规划如下所示：

| 序号 | 主机名   | 软件                   |
| ---- | -------- | ---------------------- |
| 1    | huatec01 | hadoop hbase           |
| 2    | huatec02 | hadoop hbase           |
| 3    | huatec03 | hadoop hbase zookeeper |
| 4    | huatec04 | hadoop hbase zookeeper |
| 5    | huatec05 | hadoop hbase zookeeper |

安装步骤说明如下：

1. 安装虚拟机。使用Virtualbox创建1台虚拟机centos 7 minimal，选择桥接网卡，配置固定ip

2. 克隆虚拟机并准备环境。克隆创建好的虚拟机，然后将其复制4个，得到5个虚拟机。修改复制的虚拟机网卡和mac地址配置信息，并重新修改网络配置文件，让每个虚拟机都有独立的ip。最后为虚拟机配置主机和ip映射关系（含本机），并配置免密钥访问。

3. 安装jdk。在Huatec01上安装jdk并配置环境变量，然后将安装好的安装目录和环境变量配置文件拷贝到其它节点。记得每次迁移`/etc/profile`文件的时候，执行一下`source /etc/profile`指令。

4. 安装zookeeper集群。我们的hadoop和hbase都需要依赖zookeeper集群，我们将其部署到03、04、05上。

5. 安装hadoop集群。我们将其在每个节点上都部署，01、02负责hdfs的NameNode和yarn的ResourceManager组成高可用，03、04、05负责hdfs的DataNode和yarn的NodeManager。

6. 安装Hbase集群。hbase底层需要依赖hadoop集群，01、02负责HMaster并组成高可用，03、04、05负责HRegionServer。

## 开始安装

### 安装虚拟机

过程略

### 克隆虚拟机并准备环境

#### 配置固定ip

编辑网络配置文件`vi /etc/sysconfig/network-scripts/ifcfg-enp0s3`，编辑内容如下：

```
    BOOTPROTO=static
    ONBOOT=yes
    IPADDR=192.168.31.11
    NETMASK=255.255.255.0
    GATEWAY=192.168.31.1
    DNS=8.8.8.8
```

重启网卡

```
     systemctl restart network
```

执行`ip a`查看网络配置是否生效，执行`ping baidu.com`查看虚拟机是否可以上外网。

如果还是不行，配置`/etc/resolv.conf`

```
    nameserver 8.8.8.8
```

#### 修改主机名

```
    hostnamectl set-hostname huatec01
```

#### 配置主机名和ip映射关系

`vi /etc/hosts`增加内容

```
    192.168.31.11    huatec01
    192.168.31.12    huatec02
    192.168.31.13    huatec03
    192.168.31.14    huatec04
    192.168.31.15    huatec05
```

在本机也配置上述映射关系。

#### 关闭防火墙

centos 7关闭防火墙的步骤如下，配置完`reboot`系统sh生效。

1、selinux

临时：`setenforce 0`

永久：`vi /etc/sysconfig/selinux`

```
    SELINUX=disabled
```

2、firewalld

```
    systemctl stop firewalld
    systemctl disable firewalld
    systemctl status firewalld
```

实操发现，只要给虚拟机关闭selinux防火墙，虚拟机启动的时候就会出现卡白条的现象。

不关闭selinux防火墙我的集群一样都启动成功，所以第一步可以略过。

#### 配置ssh免登录

分别执行`ssh-keygen -t rsa`生成密钥，然后制作`authorized_keys`文件

在huatec01上执行如下指令，制作`/root/.ssh/authorized_keys`文件。

```
    cat ~/.ssh/id_rsa.pub>> ~/.ssh/authorized_keys
    ssh huatec02 cat ~/.ssh/id_rsa.pub>> ~/.ssh/authorized_keys
    ssh huatec03 cat ~/.ssh/id_rsa.pub>> ~/.ssh/authorized_keys
    ssh huatec04 cat ~/.ssh/id_rsa.pub>> ~/.ssh/authorized_keys
    ssh huatec05 cat ~/.ssh/id_rsa.pub>> ~/.ssh/authorized_keys
```

在其它节点上执行，将huatec01下的`authorized_keys`文件拷贝过来。

```
    ssh huatec01 cat ~/.ssh/authorized_keys>> ~/.ssh/authorized_keys
```

### 安装jdk8

首先解压安装jdk

```
    mkdir /usr/local/java
    tar -xvf /home/zhusheng/jdk-7u80-linux-x64.tar -C /usr/local/java/
```

接下来，我们配置JDK环境变量

`vi /etc/profile`增加如下内容

```
    # jdk8
    JAVA_HOME=/usr/local/java/jdk1.7.0_80
    PATH=$JAVA_HOME/bin:$PATH
    export PATH JAVA_HOME
```

执行`source /etc/profile`应用配置，然后执行`java -version`检测是否安装成功。

### 安装Zookeeper集群

在本机上下载zookeeper安装包，解压并修改相关配置文件，然后配置完成的目录拷贝到03、04、05，并配置环境变量。

安装目录为/huatec，后续与大数据相关的软件都安装到这里。

#### 配置zookeeper

`zoo.cfg`配置文件默认不存在，但是给了示例文件，我们可以将示例文件改为zoo.cfg

```
    cd /huatec/zookeeper-3.4.5/conf
    mv zoo_sample.cfg zoo.cfg
```

 然后编辑`zoo.cfg`，修改内容如下，主要修改了数据缓存目录，并增加了集群信息，其它默认即可。

```
    dataDir=/huatec/zookeeper-3.4.5/tmp
    ...
    server.1=huatec03:2888:3888
    server.2=huatec04:2888:3888
    server.3=huatec05:2888:3888
```

创建tmp目录，然后在目录中创建文件`myid`，编辑内容为`1`

最后，将文件夹拷贝到huatec01。

     scp -r zookeeper-3.4.5 root@huatec01:/huatec

#### 配置环境变量

在huatec01上对zookeeper配置环境变量

```
    # zookeeper3.4.5
    export ZOOKEEPER_HOME=/huatec/zookeeper-3.4.5
    export PATH=$PATH:$ZOOKEEPER_HOME/bin
```

执行`source /etc/profile`使配置生效。

#### 启动zookeeper集群

在03、04、05三个节点上分别执行

```
    zkServer.sh start
    zkServer.sh status
```

我们查看huatec01的启动结果，效果如下：

![25.png](https://upload-images.jianshu.io/upload_images/5637154-8bcd0fc5984e4fbd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

三个节点中有1个为leader，2个为follower。

如果出现`Error contacting service. It is probably not running.`异常信息，请参考如下链接：
`http://blog.csdn.net/xiewendong93/article/details/50500471`

### 安装Hadoop集群

首先在本机上解压hadoop，修改相关配置信息，然后将其拷贝到`所有节点`上。

#### 修改配置文件

修改配置文件：

- hadoop-env.sh，配置hadoop运行所依赖的jdk环境变量。

```
 export JAVA_HOME=/usr/local/java/jdk1.7.0_80
```

- core-site.xml

```
<configuration>
    <!-- 指定hdfs的nameservice为ns1 -->
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://ns1</value>
    </property>
    <!-- 指定hadoop临时目录 -->
    <property>
        <name>hadoop.tmp.dir</name>
        <value>/huatec/hadoop-2.7.3/tmp</value>
        </property>
    <!-- 指定zookeeper地址 -->
    <property>
        <name>ha.zookeeper.quorum</name>
        <value>huatec03:2181,huatec04:2181,huatec05:2181</value>
    </property>
</configuration>
```

- hdfs-site.xml

```
<configuration>
    <!--指定hdfs的nameservice为ns1，需要和core-site.xml中的保持一致 -->
    <property>
        <name>dfs.nameservices</name>
        <value>ns1</value>
    </property>
    <!-- ns1下面有两个NameNode，分别是nn1，nn2 -->
    <property>
        <name>dfs.ha.namenodes.ns1</name>
        <value>nn1,nn2</value>
    </property>
    <!-- nn1的RPC通信地址 -->
    <property>
        <name>dfs.namenode.rpc-address.ns1.nn1</name>
        <value>huatec01:9000</value>
    </property>
    <!-- nn1的http通信地址 -->
    <property>
        <name>dfs.namenode.http-address.ns1.nn1</name>
        <value>huatec01:50070</value>
    </property>
    <!-- nn2的RPC通信地址 -->
    <property>
        <name>dfs.namenode.rpc-address.ns1.nn2</name>
        <value>huatec02:9000</value>
    </property>
    <!-- nn2的http通信地址 -->
    <property>
        <name>dfs.namenode.http-address.ns1.nn2</name>
        <value>huatec02:50070</value>
    </property>
    <!-- 指定NameNode的元数据在JournalNode上的存放位置 -->
    <property>
        <name>dfs.namenode.shared.edits.dir</name>
        <value>qjournal://huatec03:8485;huatec04:8485;huatec05:8485/ns1</value>
    </property>
    <!-- 指定JournalNode在本地磁盘存放数据的位置 -->
	<property>
        <name>dfs.journalnode.edits.dir</name>
		<value>/huatec/hadoop-2.7.3/journal</value>
	</property>
	<!-- 开启NameNode失败自动切换 -->
	<property>
		<name>dfs.ha.automatic-failover.enabled</name>
		<value>true</value>
	</property>
	<!-- 配置失败自动切换实现方式 -->
	<property>
		<name>dfs.client.failover.proxy.provider.ns1</name>
		<value>org.apache.hadoop.hdfs.server.namenode.ha.ConfiguredFailoverProxyProvider</value>
	</property>
	<!-- 配置隔离机制方法，多个机制用换行分割，即每个机制暂用一行-->
	<property>
		<name>dfs.ha.fencing.methods</name>
		<value>
			sshfence
			shell(/bin/true)
		</value>
	</property>
	<!-- 使用sshfence隔离机制时需要ssh免登陆 -->
	<property>
		<name>dfs.ha.fencing.ssh.private-key-files</name>
		<value>/home/hadoop/.ssh/id_rsa</value>
	</property>
	<!-- 配置sshfence隔离机制超时时间 -->
	<property>
		<name>dfs.ha.fencing.ssh.connect-timeout</name>
		<value>30000</value>
	</property>
</configuration>
```

4. mapred-site.xml

```
<configuration>
	<!-- 指定mr框架为yarn方式 -->
	<property>
		<name>mapreduce.framework.name</name>
		<value>yarn</value>
	</property>
</configuration>	

```

5. yarn-site.xml

```
<configuration>
	<!-- 开启RM高可靠 -->
	<property>
	   <name>yarn.resourcemanager.ha.enabled</name>
	   <value>true</value>
	</property>
	<!-- 指定RM的cluster id -->
	<property>
	   <name>yarn.resourcemanager.cluster-id</name>
	   <value>yrc</value>
	</property>
	<!-- 指定RM的名字 -->
	<property>
	   <name>yarn.resourcemanager.ha.rm-ids</name>
	   <value>rm1,rm2</value>
	</property>
	<!-- 分别指定RM的地址 -->
	<property>
	   <name>yarn.resourcemanager.hostname.rm1</name>
	   <value>huatec01</value>
	</property>
	<property>
	   <name>yarn.resourcemanager.hostname.rm2</name>
	   <value>huatec02</value>
	</property>
	<!-- 指定zk集群地址 -->
	<property>
	   <name>yarn.resourcemanager.zk-address</name>
	   <value>huatec03:2181,huatec04:2181,huatec05:2181</value>
	</property>
	<property>
	   <name>yarn.nodemanager.aux-services</name>
	   <value>mapreduce_shuffle</value>
	</property>
</configuration>

```

6. slaves

```
huatec03
huatec04
huatec05
```


然后将数据拷贝到所有节点


```
scp -r hadoop-2.7.3 root@huatec01:/huatec
scp -r hadoop-2.7.3 root@huatec02:/huatec
scp -r hadoop-2.7.3 root@huatec03:/huatec
scp -r hadoop-2.7.3 root@huatec04:/huatec
scp -r hadoop-2.7.3 root@huatec05:/huatec
```

   
#### 配置环境变量

在huatec01上配置环境变量，`vi /etc/profile`

```
 # hadoop2.7.3
	export HADOOP_HOME=/huatec/hadoop-2.7.3
	export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin
```

执行`source /etc/profile`

拷贝

    scp -r /etc/profile root@huatec02:/etc
    scp -r /etc/profile root@huatec03:/etc
    scp -r /etc/profile root@huatec04:/etc
    scp -r /etc/profile root@huatec05:/etc
    
分别执行`source /etc/profile`
    
#### 初次启动

1、启动zookeeper集群

03、04、05分别执行

以05为例
```
[root@huatec05 ~]# zkServer.sh start
[root@huatec05 ~]# jps
2239 QuorumPeerMain
2329 Jps
```

2、启动JournalNode

03、04、05分别执行

以05为例
```
[root@huatec05 ~]# hadoop-daemon.sh start journalnode
[root@huatec05 ~]# jps
2239 QuorumPeerMain
2280 JournalNode
2329 Jps
```

3、格式化hdfs

01执行

```
[root@huatec01 ~]# hdfs namenode –format

[root@huatec01 ~]# scp -r tmp/ huatec02:/huatec/hadoop-2.7.3/
```

之所以采用拷贝的方式，是为了保证完全一样，避免出错。

4、格式化ZK

```
[root@huatec01 ~]# hdfs zkfc -formatZK
```

5、启动HDFS with HA

01执行

```
[root@huatec01 ~]# start-dfs.sh
```

6、启动YARN with HA

01执行

```
[root@huatec01 ~]# start-yarn.sh
[root@huatec02 ~]# yarn-daemon.sh start resourcemanager
```

浏览器访问验证：
HDFS
http://huatec01:50070
http://huatec02:50070

MapReduce
http://huatec01:8088
http://huatec02:8088

![23.png](https://upload-images.jianshu.io/upload_images/5637154-427867b8236a8e33.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![26.png](https://upload-images.jianshu.io/upload_images/5637154-b2cb53ec4b7550f1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![24.png](https://upload-images.jianshu.io/upload_images/5637154-8d828355e7e8872a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### 后续启动

1、启动zookeeper集群

03、04、05分别执行

以05为例
```
[root@huatec05 ~]# zkServer.sh start
[root@huatec05 ~]# jps
2239 QuorumPeerMain
2329 Jps
```

5、启动HDFS with HA

01执行

```
[root@huatec01 ~]# start-dfs.sh
```

6、启动YARN with HA

01执行

```
[root@huatec01 ~]# start-yarn.sh
[root@huatec02 ~]# yarn-daemon.sh start resourcemanager
```

### HBase安装

将hbase下载到本机，修改配置文件，然后拷贝到所有节点，并配置环境变量。

#### 修改配置文件

1、hbase-env.sh

```
//指定jdk
export JAVA_HOME=/usr/java/jdk1.7.0_55
//告诉hbase使用外部的zk，将值设置为false
export HBASE_MANAGES_ZK=false
```

2、hbase-site.xml

```
<configuration>
    <!-- 指定hbase在HDFS上存储的路径 -->
    <property>
            <name>hbase.rootdir</name>
            <value>hdfs://ns1/hbase</value>
    </property>
    <!-- 指定hbase是分布式的 -->
    <property>
            <name>hbase.cluster.distributed</name>
            <value>true</value>
    </property>
    <!-- 指定zk的地址，多个用“,”分割 -->
    <property>
            <name>hbase.zookeeper.quorum</name>
            <value>huatec03:2181,huatec04:2181,huatec05:2181</value>
    </property>
</configuration>

```

3、regionservers

```
huatec03
huatec04
huatec05
```

4、hdfs-site.xml和core-site.xml

因为HBase底层依赖HDFS，我们需要配置两个与Hadoop相关的文件hdfs-site.xml和core-site.xml，为了方便起见，我们直接拷贝Hadoop配置文件中的hdfs-site.xml和core-site.xml, 放到hbase/conf下。

#### 拷贝和配置环境变量

```
 scp -r hbase-1.2.6 root@huatec01:/huatec
 scp -r hbase-1.2.6 root@huatec02:/huatec
 scp -r hbase-1.2.6 root@huatec03:/huatec
 scp -r hbase-1.2.6 root@huatec04:/huatec
 scp -r hbase-1.2.6 root@huatec05:/huatec
```

在01上配置环境变量，然后拷贝

```
scp -r /etc/profile root@huatec02:/etc
scp -r /etc/profile root@huatec03:/etc
scp -r /etc/profile root@huatec04:/etc
scp -r /etc/profile root@huatec05:/etc
```

#### 启动集群

01执行

```
start-hbase.sh
```

02执行 for HBase HA

```
hbase-daemon.sh start master
```

浏览器访问：

`http://huatec01:16010`

![27.png](https://upload-images.jianshu.io/upload_images/5637154-1df28323e7ca36b8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

`http://huatec02:16010`

![28.png](https://upload-images.jianshu.io/upload_images/5637154-bc7c9d3215e684af.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
