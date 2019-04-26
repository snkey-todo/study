# Hive单节点部署

## 安装说明

我们在官网下载Hive安装包，我下载的Hive版本为apache-hive-2.1.1-bin.tar。

[下载地址](https://hive.apache.org/downloads.html)

我们在前面已经部署好的Zookeeper+Hadoop+HBase集群上安装Hive。Hive不需要以集群的方式提供服务，但是Hive的底层工作需要依赖HDFS，为了提高Hive的执行效率，我们决定将Hive安装到HDFS主节点上，HDFS主节点有两个：huatec01和huatec02，它们彼此组成NameNode高可用。我们将Hive安装到其中一个节点即可，这里我选择huatec01。

## 安装步骤

### 安装Hive

我们统一和前面的大数据软件安装到统一个目录下，方便管理。

```bash
[root@huatec01 ~]# tar -xvf apache-hive-2.1.1-bin.tar -C /huatec/
```

### 配置Hive环境变量

```bash
[root@huatec01 bin]# vi /etc/profile
...
#hive
export HIVE_HOME=/huatec/apache-hive-2.1.1-bin
export PATH=$PATH:$HIVE_HOME/bin
```

执行`source /etc/profile`使配置生效。

### 安装元数据库MySQL

这里我们使用MySQL作为元数据库，我们在huatec01节点上安装MySQL。

[安装步骤参考文章](http://note.youdao.com/noteshare?id=8a57c3b8f53bddbbeada1435cf0b607a)

安装完MySQL 后，进入mysql shell，执行

```bash
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'root' WITH GRANT OPTION;
```

说明：第一个*表示任何数据库，第二个*表示所有表，%表示任何ip都可以访问。

### 修改Hive配置文件

- hive-env.sh

模版文件为`hive-env.sh.template`,修改模版文件名称,然后添加如下内容：

```bash
 HADOOP_HOME=/huatec/hadoop-2.7.3
 export HIVE_CONF_DIR=/huatec/apache-hive-2.1.1-bin/conf
 export HIVE_HOME=/huatec/apache-hive-2.1.1-bin
```

- hive-site.xml

模版文件为`hive-default.xml.template`，修改模版文件名称,然后编辑文件中的内容，因为该文件的配置属性非常多，文件长度达到558行，所以建议在本地修改，我们以搜索的方式进行配置，然后将其拷贝到服务器。

（1）基本配置

>元数据库配置

```bash
//499行，指定数据库连接，hive第一次启动的时候会默认创建hive数据库；
<property>
    <name>javax.jdo.option.ConnectionURL</name>
    <value>jdbc:mysql://huatec01:3306/hive?createDatabaseIfNotExist=true</value>
    <description>
      JDBC connect string for a JDBC metastore.
      To use SSL to encrypt/authenticate the connection, provide database-specific SSL flag in the connection URL.
      For example, jdbc:postgresql://myhost/db?ssl=true for postgres database.
    </description>
  </property>
...
//931行，指定MySQL 的驱动方式为“com.mysql.jdbc.Driver”；
<property>
    <name>javax.jdo.option.ConnectionDriverName</name>
    <value>com.mysql.jdbc.Driver</value>
    <description>Driver class name for a JDBC metastore</description>
  </property>
...
//956行，指定了连接数据库的用户名和密码；
  <property>
    <name>javax.jdo.option.ConnectionUserName</name>
    <value>root</value>
    <description>Username to use against metastore database</description>
  </property>
...
//484行
<property>
    <name>javax.jdo.option.ConnectionPassword</name>
    <value>root</value>
    <description>password to use against metastore database</description>
  </property>
...
//685行，取消元数据库表认证
<property>
    <name>hive.metastore.schema.verification</name>
    <value>false</value>
    <description>
      Enforce metastore schema version consistency.
      True: Verify that version information stored in is compatible with one from Hive jars.  Also disable automatic
            schema migration attempt. Users are required to manually migrate schema after Hive upgrade which ensures
            proper metastore schema migration. (Default)
      False: Warn if the version information stored in metastore doesn't match with one from in Hive jars.
    </description>
  </property>
...
```

>配置缓存目录

用到缓存目录的属性有很多个，我们直接搜索`${system:java.io.tmpdir}`替换为`/huatec/apache-hive-2.1.1-bin/tmp`，并手动创建该路径。

（2）hwi服务配置

hwi服务的启动需要依赖`hive-hwi-2.1.1.jar`，这个jar包在`$HIVE_HOME/lib`是存在的，我们指定路径即可。

```bash
<property>
    <name>hive.hwi.war.file</name>
    <value>lib/hive-hwi-2.1.1.jar</value>
    <description>This sets the path to the HWI war file, relative to ${HIVE_HOME}. </description>
  </property>
```

该路径是相对于`${HIVE_HOME}`的相对路径。

（3）拷贝数据库连接驱动

我们需要将数据库连接驱动`mysql-connector-java-5.1.42-bin.jar`添加到hive安装路径的lib目录。

## 启动Hive

### 初始化元数据库

第一次启动Hive的时候，我们需要初始化元数据库。

```bash
[root@huatec01 bin]# ./schematool -initSchema -dbType mysql
```

![image](https://raw.githubusercontent.com/zhusheng/blog/master/47.png)

当控制台输出“schemaTool  completed”日志，表明元数据库初始化成功。

### 进入Hive shell

我们运行指令“hive”即可进入hive shell模式

![image](https://raw.githubusercontent.com/zhusheng/blog/master/48.png)

## 入门操作

尝试创建表

```bash
hive > create table trade_detail (id bigint, account string, income double, expenses double, time string) row format delimited fields terminated by '\t';
```

当我们在hive创建一张表时，首先会在mysql保存表的描述信息（表名、存储位置分配、列等信息），然后在hdfs上创建一个目录。

![image](https://raw.githubusercontent.com/zhusheng/blog/master/49.png)

我们连接元数据库，发现数据库中多出了很多表，如下图所示：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/50.png)

在TBLS表中，保存了我们的表名、表的类型信息,如下图所示：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/51.png)

在COLIUMNS_V2表中，保存了表的字段信息,如下图所示：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/52.png)

我们访问HDFS，发现多了一个目录“/user/hive/warehouse/trade_detail”，如下图所示：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/53.png)