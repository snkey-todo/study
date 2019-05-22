# tensorflow读取数据

[tensorflow中文社区|读取数据参考文档]([http://www.tensorfly.cn/tfdoc/how_tos/reading_data.html](http://www.tensorfly.cn/tfdoc/how_tos/reading_data.html))

tensorflow可以读取以下三种形式的文件，不同类型文件的读取形式也不同，如下所示：
1. csv文件，读取一行
2. 二进制文件，指定一个样本的bytes读取
3. 图片文件，一张一张的读取

## 文件读取的流程

参考官网的文件读取流程图如下所示：

![](http://www.tensorfly.cn/tfdoc/images/AnimatedFileQueues.gif)

## 文件读取的步骤

**1. 构造文件队列**

将需要读取的数据放入队列。

核心API
`tf.train.string_input_producer(string_tensor,,shuffle=True)`：将输出字符串（例如文件名）输入到管道队列

参数说明：
- string_tensor	含有文件名的1阶张量
- num_epochs:过几遍数据，默认无限过数据
- return:具有输出字符串的队列

**2. 新建文件阅读器**

我们通过文件阅读器去读取数据。

根据文件格式，选择对应的文件阅读器:
`class tf.TextLineReader`：阅读文本文件逗号分隔值（CSV）格式,默认按行读取
return：读取器实例

`tf.FixedLengthRecordReader(record_bytes)`：要读取每个记录是固定数量字节的二进制文件
record_bytes:整型，指定每次读取的字节数
return：读取器实例

`tf.TFRecordReader`：读取TfRecords文件。

这些阅读器都有一个共同的读取方法：`read(file_queue)`：从队列中指定数量内容，返回一个Tensors元组（key文件名字，value默认的内容(行，字节)）。

**3. 文件内容解码**

将读取到的数据进行解码。由于从文件中读取的是字符串，需要函数去解析这些字符串到张量
`tf.decode_csv(records,record_defaults=None,field_delim = None，name = None)`：将CSV转换为张量，与tf.TextLineReader搭配使用

参数说明：
- records:tensor型字符串，每个字符串是csv中的记录行
- field_delim:默认分割符”,”
- record_defaults:参数决定了所得张量的类型，并设置一个值在输入字符串中缺少使用默认值,如

`tf.decode_raw(bytes,out_type,little_endian = None，name = None) `：将字节转换为一个数字向量表示，字节为一字符串类型的张量,与函数`tf.FixedLengthRecordReader`搭配使用，二进制读取为uint8格式


**4. 批处理**

读取多个数据。

`tf.train.batch(tensors,batch_size,num_threads = 1,capacity = 32,name=None)`：读取指定大小（个数）的张量。

参数说明：
- tensors：可以是包含张量的列表
- batch_size:从队列中读取的批处理大小
- num_threads：进入队列的线程数
- capacity：整数，队列中元素的最大数量
- return:tensors

`tf.train.shuffle_batch(tensors,batch_size,capacity,min_after_dequeue,num_threads=1,) `：乱序读取指定大小（个数）的张量。

参数说明：
- min_after_dequeue:留下队列里的张量个数，能够保持随机打乱

**5. 开启线程操作**

开启子线程去执行读取文件的操作。

`tf.train.start_queue_runners(sess=None,coord=None)`：收集所有图中的队列线程，并启动线程。

参数说明：
- sess:所在的会话中
- coord：线程协调器
- return：返回所有线程队列

