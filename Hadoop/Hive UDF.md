# Hive UDF

- 什么是UDF？

它是User defined Function的简写，意思是用户自定义方法。

- 为什么要用UDF？
在使用Hive shell时，我们可以使用sum()、count()等函数，但是有写业务场合，我们希望有其它更多的函数。因为Hive执行QL语句就可以执行MapReduce，我们自然希望QL语句的功能更加强大，其结果就是我们想要的结果，这时，我们就需要自定义一些函数了，也就是UDF。

## Hive UDF开发

1、新建Java Application
2、导包

- 导入hive/lib下的所有包
- 导入hadoop-common.jar包（该包下有Text类，因为Hive QL需要走MapReduce，自然不能使用String）

3、代码开发

```java
public class NationUDF extends UDF{
	Text text = new Text();
	public static Map<String,String> nationMap = new HashMap<>();
	static {
		nationMap.put("China", "中国");
		nationMap.put("Japan", "日本");
		nationMap.put("U.S.A", "美国");
	}
	
	public Text evaluate(Text nation){
		String nationStr = nation.toString();
		String result = nationMap.get(nationStr);
		if(result == null){
			result = "未知";
		}
		text.set(result);
		return text;
	}
}
```

4、打jar包并上传

将项目打包成jar file包并上传到服务器，然后使用`Hive指令`指定jar包的位置，将其添加到Hive。

```bash
hive> add jar /home/zhusheng/NationUDF.jar;
```

5、hive 下创建临时函数

```bash
hive> create temporary function getNation as 'com.hive.udf.NationUDF';
```

备注：这里是临时函数，也就是说shell窗口关闭了，该函数就不可用了，下次使用需要重新创建。

6、hive下调用

```bash
hive> select id, name, size, getNation(nation) as nation from ext_beauties order by size desc;
```

效果图如下：
![image](https://raw.githubusercontent.com/zhusheng/blog/master/92.png)

7、保存并查看结果

```bash
hive> create table result row format delimited fields terminated by '\t' as
    > select id ,name, size, getNation(nation) as nation from ext_beauties
    > order by size desc;
```

查看结果
![image](https://raw.githubusercontent.com/zhusheng/blog/master/93.png)
