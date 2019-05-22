# Hadoop简介

## Hadoop的作者和起源

作者：Doug Cutting

受Google三篇论文的启发(GFS、MapReduce、BigTable)

## 什么是Hadoop

>What Is Apache Hadoop?
The Apache™ Hadoop® project develops open-source software for reliable, scalable, distributed computing.

- Hadoop是Apache软件基金会旗下的一个开源分布式计算平台，为用户提供了系统底层细节透明的分布式基础架构。
- Hadoop是基于Java语言开发的，具有很好的跨平台特性，并且可以部署在廉价的计算机集群中。
- Hadoop的核心是分布式文件系统HDFS（Hadoop Distributed File System）和MapReduce。
- Hadoop被公认为行业大数据标准开源软件，在分布式环境下提供了海量数据的处理能力。
- 几乎所有主流厂商都围绕Hadoop提供开发工具、开源软件、商业化工具和技术服务，如谷歌、雅虎、微软、思科、淘宝等，都支持Hadoop。

## Hadoop能干什么？

hadoop擅长日志分析，facebook就用Hive来进行日志分析，2009年时facebook就有非编程人员的30%的人使用HiveQL进行数据分析；

淘宝搜索中的自定义筛选也使用的Hive；

利用Pig还可以做高级的数据处理，包括Twitter、LinkedIn上用于发现您可能认识的人，可以实现类似Amazon.com的协同过滤的推荐效果。淘宝的商品推荐也是！在Yahoo！的40%的Hadoop作业是用pig运行的，包括垃圾邮件的识别和过滤，还有用户特征建模。（2012年8月25新更新，天猫的推荐系统是hive，少量尝试mahout！）

## Hadoop发展简史

- Hadoop最初是由Apache Lucene项目的创始人Doug Cutting开发的一个文本搜索库，源自始于2002年的一个开源Apache Nutch项目，它是一个开源的网络搜索引擎并且也是Lucene项目的一部分。在2004年，Nutch项目模仿GFS（Google File System）开发了自己的分布式文件系统NDFS（Nutch Distributed File System），也就是HDFS的前身。同年，谷歌公司发表了另一篇具有深远影响的论文，阐述了MapReduce分布式编程思想。

- 在2005年，Nutch项目团队参考MapReduce分布式编程思想开发了MapReduce分布式处理框架。

- 2006年2月，Nutch项目将NDFS和MapReduce独立出来，使其成为Lucene项目的一个子项目，命名为Hadoop。

- 2008年1月，Hadoop正式成为Apache顶级项目，并逐渐被雅虎、FaceBook等大公司采用。

- 2008年4月，Hadoop打破世界纪录，成为最快排序1TB数据的系统，它采用一个由910个节点构成的集群进行运算，排序时间只用了209秒。并于2009年，将这个排序时间缩短到62秒。Hadoop从此名声大震，迅速发展成为大数据时代最具影响力的开源分布式开发平台。

## Hadoop的特点

Hadoop是一个能够对大量数据进行分布式处理的软件框架，并且是以一种可靠、高效、可伸缩的方式进行处理的，它具有以下几个方面的特性：

- 高可靠性（Reliable）。
> hadoop能自动地维护数据的多份副本，并且在任务失败后能自动地重新部署（redeploy）计算任务。

- 高效率（Efficient）。
> 通过分发数据，hadoop可以在数据所在的节点上并行地（parallel）处理它们，这使得处理非常的快速。

- 高可扩展性。
> 集群大小可扩展，核心进程例如NameNode、DataNode也可扩展。

- 高容错性。
> 分布式存储，数据多副本，分布式计算。

- 成本低（Economical）。
> 可以通过普通机器组成的服务器群来分发以及处理数据。这些服务器群总计可达数千个节点。

- 扩容能力（Scalable）：能可靠地（reliably）存储和处理千兆字节（PB）数据。

- 运行在Linux平台上

- 支持多种编程语言

## 发展现状

Hadoop凭借其在大数据处理领域的实用性以及良好的易用性，自2007年推出以来，很快就在工业界得到普及应用，并得到了学术界的广泛关注和研究。在短短的几年中，Hadoop很快成为到目前为止最为成功、最广泛接受使用的大数据处理主流技术和系统平台。现在它已发展成为一种大数据处理方面的工业标准，并在工业界应用中得到大量的进一步开发和改进，尤其是互联网行业。

在国外，Yahoo曾经就是Hadoop的最大支持者，截至2012年，Yahoo的Hadoop机器总节点数目超过420000个，有超过10万的核心CPU在运行Hadoop。最大的一个单Master节点集群有4500个节点，总的集群存储容量大于350PB，每月提交的作业数目超过1000万个。Facebook也使用Hadoop存储内部日志与多维数据，并以此作为报告、分析和机器学习的数据源。Facebook不尽大力支持Hadoop，还为Hadoop的发展作出了重要的贡献。Facebook在Hadoop基础上建立了一个名为Hive的高级数据仓库框架，用来进行数据清洗、处理等工作，目前Hive已经正式成为基于Hadoop的Apache一级项目。

在国内，很多互联网企业都逐渐使用Hadoop来处理离线数据，例如阿里巴巴、百度、淘宝、网易、华为、中国移动等。阿里巴巴的Hadoop集群数据非常庞大，它需要为淘宝、天猫、一淘、聚划算、CBU、支付宝提供底层的基础计算和存储服务。在2012年的时候，其集群已经有超过3200台服务器，总的存储容量超过60PB，每天的作业数目超过1500000个，到今天，这些数字只会越来越大。腾讯也是使用Hadoop最早的中国互联网公司之一，并依托大数据来处理腾讯社交广告平台、腾讯微博、QQ、财付通、微信、QQ音乐等平台的数据。因其庞大的用户量，其集群数量也是非常庞大的。据调查显示，截至2012年年底，腾讯的Hadoop集群机器总量超过5000台，最大单集群约为2000个节点。除此之外，腾讯还利用Hadoop-Hive构建了一套自己的数据仓库系统，取名为“TDW”。

Hadoop正随着行业的发展而发展，并逐渐改进和完善，相信在未来其应用领域和范围也会逐渐增大。

## Hadoop版本

### 1.0和2.0

Apache Hadoop版本分为两代，我们将第一代Hadoop称为Hadoop 1.0，第二代Hadoop称为Hadoop 2.0。

第一代Hadoop包含三个大版本，分别是0.20.x，0.21.x和0.22.x，其中，0.20.x最后演化成1.0.x，变成了稳定版，而0.21.x和0.22.x则增加了NameNode HA等新的重大特性。

第二代Hadoop包含两个版本，分别是0.23.x和2.x，它们完全不同于Hadoop 1.0，是一套全新的架构，均包含HDFS Federation和YARN两个系统，相比于0.23.x，2.x增加了NameNode HA和Wire-compatibility两个重大特性。

### 开源版本和商用版本

Hadoop作为开源项目，也衍生出了很多商用版本，Apache Hadoop、Hortonworks、Cloudera（CDH：Cloudera Distribution Hadoop）、MapR……，企业在选用时，我们需要考虑：

- 是否开源（即是否免费）
- 是否有稳定版
- 是否经实践检验
- 是否有强大的社区支持

## Hadoop项目架构

Hadoop的项目结构不断丰富发展，已经形成一个丰富的Hadoop生态系统

- Common:一系列接口和组建，用于分布式文件系统和通用I/O。
- Avro：一种序列化系统，用于支持高校、跨语言的RPC和持久化数据存储。
- HDFS：分布式文件系统，大数据存储
- MapReduce：分布式并行编程模型，大数据分析与处理
- YARN：资源管理和调度器
- Tez：运行在YARN之上的下一代Hadoop查询处理框架
- Hive：Hadoop上的数据仓库
- HBase：Hadoop上的非关系型的分布式数据库
- Pig：一个基于Hadoop的大规模数据分析平台，提供类似SQL的查询语言Pig Latin
- Sqoop：用于在Hadoop与传统数据库之间进行数据传递
- Oozie：Hadoop上的工作流管理系统
- Zookeeper：提供分布式协调一致性服务
- Storm：流计算框架
- Flume：一个高可用的，高可靠的，分布式的海量日志采集、聚合和传输的系统
- Ambari：Hadoop快速部署工具，支持Apache Hadoop集群的供应、管理和监控
- Kafka：一种高吞吐量的分布式发布订阅消息系统，可以处理消费者规模的网站中的所有动作流数据
- Spark：类似于Hadoop MapReduce的通用并行框架

说明：

1. 这一切是如何开始的—Web上庞大的数据!
2. 使用Nutch抓取Web数据
3. 要保存Web上庞大的数据——HDFS应运而生
4. 如何使用这些庞大的数据?
5. 采用Java或任何的流/管道语言构建MapReduce框架用于编码并进行分析
6. 如何获取Web日志，点击流，Apache日志，服务器日志等非结构化数据——fuse,webdav, chukwa, flume, Scribe
7. Hiho和sqoop将数据加载到HDFS中，关系型数据库也能够加入到Hadoop队伍中
8. MapReduce编程需要的高级接口——Pig, Hive, Jaql
9. 具有先进的UI报表功能的BI工具- Intellicus
10. Map-Reduce处理过程使用的工作流工具及高级语言
11. 监控、管理hadoop，运行jobs/hive，查看HDFS的高级视图—Hue, karmasphere, eclipse plugin, cacti, ganglia
12. 支持框架—Avro (进行序列化), Zookeeper (用于协同)
13. 更多高级接口——Mahout, Elastic map Reduce
14. 同样可以进行OLTP——Hbase
