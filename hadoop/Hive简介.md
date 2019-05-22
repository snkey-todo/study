# Hive简介

Apache Hive是一个构建于Hadoop顶层的数据仓库。

Apache Hive是一个构建于Hadoop顶层的数据仓库，可以将结构化的数据文件映射为一张数据库表，并提供简单的SQL查询功能，可以将SQL语句转换为MapReduce任务进行运行。需要注意的是，Hive它并不是数据库。

Hive依赖于HDFS和MapReduce，其对HDFS的操作类似于SQL，我们称之为HQL，它提供了丰富的SQL查询方式来分析存储在HDFS中的数据。HQL可以编译转为MapReduce作业，完成查询、汇总、分析数据等工作。这样一来，即使不熟悉MapReduce 的用户也可以很方便地利用SQL 语言查询、汇总、分析数据。而MapReduce开发人员可以把己写的mapper 和reducer 作为插件来支持Hive 做更复杂的数据分析。

说到这里，你可能会对Hive和HBase之间的关系产生疑问？在不熟悉它们的作用之前，我们有这样的疑问是很正常的。我们知道HBase是一个NoSQL数据库，它可以进行海量数据存储，他可以将一些数据查询工作转换为MapReduce任务进行运作，HBase非常适用于大数据实时查询，它的查询效率非常高。而Hive适合于对一段时间内的数据进行分析查询，例如：趋势分析、日志分析等，虽然Hive也能够进行数据实时查询，但是它在这方面表现的很糟糕，它需要很长时间才可以返回结果，这并不是它所擅长的。Hive分析的数据可以来自于HDFS，也可以来自于HBase，你可以认为HBase是一个DB，而Hive是一个Tool。它们经常是在一起互相协作来完成一些工作的。

Hive主要特点如下：

1. 通过HQL语言非常容易的完成数据提取、转换和加载（ETL）。
2. 通过HQL完成海量结构化数据分析。
3. 灵活的数据存储格式，支持JSON，CSV，TEXTFILE，RCFILE，ORCFILE，SEQUENCEFILE等存储格式，并支持自定义扩展。
4. 多种客户端连接方式，支持JDBC、Thrift等接口。


## Hive架构

你可以认为Hive就是一款SQL解析引擎，它可以将SQL语句转换为相应的MapReduce程序，我们来看一下Hive的体系架构图:

![image](http://upload-images.jianshu.io/upload_images/5637154-bebabc03065f1346.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

下面我们分析这张图

（1）首先最顶层的是“User Interfaces”层，也就是用户接口层，它包括Web UI、Hive Command Line和HD Insight三种方式。其中Web UI让我们可以通过浏览器界面进行操作Hive，一般只能进行查看。Hive Command Line也就是Hive Command Line Interface，我们称之为CLI(Command Line Interface)，也就是Shell操作，这个是使用最多的，因为我们可以编写Shell脚本来进行运行HDInsight 是一种云技术驱动的 Hadoop 发行版。使用 HDInsight，我们可以在HDInsight 上预加载 Hive 库。基于 Linux 的 HDInsight，我们可以使用 Hive 客户端、WebHCat 和 HiveServer2。基于 Windows 的 HDInsight，我们可以使用 Hive 客户端和WebHCat。

（2）MetaStore，也就是元数据。Hive的元数据存储在元数据库中，Hive默认自带有元数据库derby，我们也可以使用其它的例如MySQL 数据库来存储元数据信息，具体我会在后续的任务中进行讲解。

（3）Hive QL Process Engine，HiveQL类似于SQL用于查询Metastore上的模式信息。它是MapReduce程序的传统方法的替代品之一。 代替在Java中编写MapReduce程序，我们可以为MapReduce作业编写一个查询并处理它。

（4）Excution Engine，Hive执行引擎，Hive QL Process Engine和MapReduce的连接部分是Hive Excution Engine，执行引擎处理查询并生成与MapReduce结果相同的结果。

（5）HDFS or HBase Data Storage，这是因为Hive主要进行数据分析，分析的数据来源于HDFS或HBase。

从上面的体系结构中可以看出，Hive其实就是利用Hive QL Process Engine和Excution Engine将用户的SQL语句解析成对应的MapReduce程序而已。

经过上面的说明，我们知道Hive的工作和Hadoop之间密不可分，它的工作执行要素之一需要依赖HDFS（也可以是HBase），执行要素之二需要依赖MapReduce。为了更加深入的理解其内部的执行机制，我们看一下Hive的工作流程图。

![image](http://upload-images.jianshu.io/upload_images/5637154-3fafd662e7029a7b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

上图展示了Hive工作时的内部流程，主要分为10个步骤：

（1）执行查询：Hive接口比如Command line首先会将用户输入的查询操作发送给数据库Driver比如JDBC、ODBC。

（2）Driver驱动在查询编译器的帮助下解析查询，并检查语法，生成一个查询计划。

（3、4）编译器向元数据库发送数据请求，然后元数据库返回数据给编译器。

（5）编译器检查查询计划的各个条件和要素是否满足，然后将查询计划重新发送给数据库驱动，截止到这里，解析和编译一个查询QL的工作已经完成。

（6）接下来，驱动就可以将查询计划发送给执行引擎了，包含对应的数据信息。

（7）执行引擎处理我们的查询计划，会从元数据库中获取数据信息，然后将其转换为一个MapReduce Job，然后就涉及到了MapReduce的工作机制了。首先这个查询计划会发送到JobTracker，然后分配给具体的TaskTracker去完成。MapReduce执行过程中会从HDFS读取数据。

（8）当执行引擎执行完查询计划后，会将结果返回到执行处，这样执行引擎就能知道MapReduce执行结果的数据具体保存在HDFS什么位置上。

（9）执行引擎执行完查询计划后，会将收到的结果返回给驱动。

（10）驱动将收到的结果返回给Hive接口，这样查询计划的执行者就可以看到查询计划的执行结果。
到这里，相信你对Hive的工作流程也有了一个清晰的认识。

## Hive数据类型

（1）数值型
TINYINT
SMALLINT
INT/INTEGER
BIGINT
FLOAT
DOUBLE
DECIMAL

（2）日期型
TIMESTAMP
DATE
INTERVAL

（3）字符型
String
Varchar
Char

（4）其它类型
BOOLEAN
BINARY

（5）复杂类型
arrays
maps
structs
union

## Hive表类型

内部表、分区表、外部表和桶表

外部表可以分区，内部表也可以分区
