# Hadoop伪分布式部署

Hadoop的伪分布式环境搭建，也就是在单个节点上进行部署。

## 准备工作

### 虚拟机准备

在安装Hadoop之前，我们需要安装Hadoop的运行环境-linux系统，我选择安装的是CentOS7 mini server版本。我们可以通过VMWare、VirtualBox等虚拟化软件来创建我们部署所需要的虚拟机，安装过程略。

需要注意的是，在安装时我们需要配置虚拟机的网卡信息，我们选择桥接网卡，这样虚拟机与虚拟机、虚拟机与主机之间都可以进行通信，同时也方便我们在虚拟机中下载安装时所需要的资源。

### 关闭防火墙

我们需要关闭我们系统的防火墙，CentOS 7默认关闭iptables，我们关闭firewalld防火墙即可。经测试，selinux防火墙无论关闭都可以。

#### 关闭firewalld防火墙

```bash
[root@huatec01 ~]# systemctl stop firewalld
[root@huatec01 ~]# systemctl disable firewalld
[root@huatec01 ~]# systemctl status firewalld
firewalld.service - firewalld - dynamic firewall daemon
   Loaded: loaded (/usr/lib/systemd/system/firewalld.service; disabled)
   Active: inactive (dead)
Oct 12 22:54:57 huatec01 systemd[1]: Stopped firewalld - dynamic firewall daemon.
```

在关闭firewalld防火墙之前，我们需要先systemctl stop firewalld来停止防火墙，避免其已经处于运行状态，导致关闭失败，然后调用systemctl disable firewalld让其彻底不可用。最后，我们执行systemctl status firewalld指令查看防火墙是否关闭成功。我们从上述的代码中可以看到最后的防火墙状态是inactive (dead)，说明操作成功。

#### 关闭selinux防火墙（拓展）

```bash
[root@huatec01 ~]# vi /etc/sysconfig/selinux
...
SELINUX=disabled
...
```

我们修改其中的一行，将SELINUX的值改为disabled即可。

SELINUX的取值有三个，分别为enforcing、permissive和disabled。enforcing表示SELINUX安全策略是强制性的，permissive表示SELINUX安全策略将会提示权限问题，输出提示信息，disabled是直接让其不可用。

### 网络配置

1、固定ip

```bash
[root@huatec01 ~]# vi /etc/sysconfig/network-scripts/ifcfg-eth0
...
BOOTPROTO="static"
ONBOOT="yes"
IPADDR=192.168.14.101
NETMASK=255.255.240.0
GATEWAY=192.168.0.1
DNS=202.106.0.20
...
```

重启网卡

```bash
[root@huatec01 ~]# systemctl restart network
```

2、主机名

```bash
[root@huatec01 ~]# hostnamectl set-hostname huatec01
[root@huatec01 ~]# hostname
huatec01

```

3、主机和ip映射

```bash
[root@huatec01 ~]# vi /etc/hosts
...
192.168.8.101 huatec01

```

### 安装jdk

Hadoop的运行需要依赖java环境，而且不同版本的Hadoop对JDK的版本要求也不同。我选择安装的是Hadoop 2.7.3版本，它要求JDK最低版本为1.7。

安装jdk

```bash
[root@huatec01 ～]# mkdir /usr/local/java/
[root@huatec01 java]# tar –xvf JDK-7u80-linux-x64.tar -C /usr/local/java/

```

配置环境变量

```bash
[root@huatec01 local]# vi /etc/profile
…
#java
JAVA_HOME=/usr/local/java/JDK1.7.0_80
export PATH=$PATH:$JAVA_HOME/bin

```

我们执行`source /etc/profile`指令来应用环境变量配置文件的更新，最后我们执行`java –version`指令检测是否安装成功。

## Hadoop环境搭建

### 下载与安装

[Hadoop的下载地址](http://archive.apache.org/dist/Hadoop/core/stable/)

安装

```bash
[root@huatec01 ／]# mkdir /huatec
[root@huatec01 ／]# tar –zxvf hadoop-2.7.3.tar.gz –C /huatec

```

### 配置环境变量

```bash
[root@huatec01 local]# vi /etc/profile
…
#Hadoop
HADOOP_HOME=/huatec/Hadoop-2.7.3
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

```

我们执行`source /etc/profile`指令来应用环境变量配置文件的更新。

### 修改配置文件

要想启动Hadoop，我们还需要进入$HADOOP_HOME/etc/hadoop/目录，修改Hadoop的配置文件，主要有5个，分别为：

- [x] hadoop.env.sh
- [x] core-site.xml
- [x] hdfs-site.xml
- [x] mapped-site.xml
- [x] yarn-site.xml

（1）hadoop.env.sh

该文件为Hadoop的运行环境配置文件，Hadoop的运行需要依赖JDK，我们将其中的export JAVA_HOME的值修改为我们安装的JDK路径，如下所示：

```bash
export JAVA_HOME=/usr/local/java/JDK1.7.0_80
```

（2）core-site.xml

该文件为Hadoop的核心配置文件，配置后的文件内容如下所示：

```bash
<configuration>
        <property>
                <name>fs.defaultFS </name>
                <value>hdfs://huatec01:9000</value>
        </property>
        <property>
                <name>Hadoop.tmp.dir</name>
                <value>/huatec/hadoop-2.7.3/tmp</value>
        </property>
</configuration>
```

在上面的代码中，我们主要配置了两个属性，第一个属性用于指定HDFS的NameNode的通信地址，这里我们将其指定为huatec01;第二个属性用于指定Hadoop运行时产生的文件存放目录，这个目录我们无需去创建，因为在格式化Hadoop的时候会自动创建。

（3）hdfs-site.xml

该文件为HDFS核心配置文件，配置后的文件内容如下所示：

```bash
<configuration>
        <property>
                <name>dfs.replication</name>
                <value>1</value>
        </property>
</configuration>
```

Hadoop集群的默认的副本数量是3，但是现在我们只是在单节点上进行伪分布式安装，无需保存3个副本，我们将该属性的值修改为1即可。

（4）mapped-site.xml

这个文件是不存在的，但是有一个模版文件mapred-site.xml.template，我们将模版文
件改名为mapred-site.xml，然后进行编辑。该文件为MapReduce核心配置文件，配置后的文件内容如下所示：

```bash
[root@huatec01 Hadoop]# mv mapred-site.xml.template mapred-site.xml
[root@huatec01 Hadoop]# vi mapred-site.xml
...
<configuration>
     <property>
                <name>mapreduce.framework.name</name>
                <value>yarn</value>
        </property>
</configuration>

```

之所以配置上面的属性，是因为在Hadoop2.0之后，mapreduce是运行在Yarn架构上的，我们需要进行特别声明。

（5）yarn-site.xml

该文件为Yarn框架配置文件，我们主要指定我们的ResourceManager的节点名称及NodeManager属性，配置后的文件内容如下所示：

```bash
<configuration>
        <property>
                <name>yarn.resourcemanager.hostname</name>
                <value>huatec01</value>
        </property>
        <property>
                <name>yarn.nodemanager.aux-services</name>
                <value>mapreduce_shuffle</value>
        </property>
</configuration>

```

在上面的代码中，我们配置了两个属性。第一个属性用于指定ResourceManager的地址，因为我们是单节点部署，我们指定为huatec01即可；第二个属性用于指定reducer获取数据的方式。

### 启动Hadoop

初次启动需要先执行`hdfs namenode -format`格式化文件系统，然后再启动hdfs和yarn，后续启动直接启动hdfs和yarn即可。

1、启动

```bash
start-dfs.sh
start-yarn.sh
```

jps进程如下表示启动成功。

```bash
[root@huatec01 /]# jps
27408 NameNode
28218 Jps
27643 SecondaryNameNode
28066 NodeManager
27803 ResourceManager
27512 DataNode
```

2、关闭

```bash
stop-dfs.sh
stop-yarn.sh
```

### 访问Hadoop

通过`http://192.168.14.101:50070`或`http://huatec01:50070`访问Hadoop管理界面

![image](http://upload-images.jianshu.io/upload_images/5637154-23d535c0c5c1722d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

通过`http://192.168.14.101:8088`或`http://huatec01:8088`访问MapReduce管理界面

![image](http://upload-images.jianshu.io/upload_images/5637154-a9a2b11adcc9ac7b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
