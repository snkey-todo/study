## Pig部署

- 下载

[最新版本：pig-0.17.0.tar](http://pig.apache.org)

- 安装

我们安装到一个节点即可，这里我们安装到huatec01节点，安装过程非常简单，解压即可完成安装，然后为其配置一下全局环境变量。

- 本地模式运行

以本地模式运行pig，进入pig shell模式

```bash
pig -x local
```

- MapReduce模式运行

这也是实际工作模式，连接到Hadoop集群。

第一步：配置MapReduce模式

1、设置PATH
（1）配置java环境变量
（2）配置hadoop环境变量
（3）配置pig环境变量

2、设置PIG_CLASSPATH环境变量

```bash
PIG_CLASSPATH = /huatec/hadoop-2.7.3/conf
```
![image](https://raw.githubusercontent.com/zhusheng/blog/master/77.png)

第二步：修改hosts

配置主机名和ip的映射关系

第三步：启动Pig

```bash
pig
```

效果图如下：
![image](https://raw.githubusercontent.com/zhusheng/blog/master/78.png)

### Pig运行说明

Pig的运行方式有3种：

- 脚本
- Grunt
- 嵌入式，嵌入到其它语言中进行运行。

建议使用Pig Latin语言编写".pig"脚本文件。

1、脚本运行

```bash
pig /home/zhusheng/student.pig
```

2、Grunt运行

指令运行，如LOAD、FOREACH、STORE、DUMP等，见上。

3、嵌入式

略