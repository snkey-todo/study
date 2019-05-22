# tensorflow读取csv文件

- tensorflow读取单个csv文件
- tensorflow读取csv文件集

## 单个文件读取

数据格式如下：
```
0,10,0,0,0
0,15,0,0,1
0,30,0,0,2
0,45,0,0,3
```

完整代码如下：
```python
from __future__ import print_function
import tensorflow as tf
import os 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def file_len(fname):
    """
   获取文件的长度，也就是有多少行
    """
    with open(fname) as f:
        for i, l in enumerate(f):
            # i为行，从0开始
            # l为每行的内容，
            pass
    # i还在内存中，可以直接调用
    return i + 1

def readcsv(filename):
    """
    读取csv文件
    """
    # 1、构造一个读取文件的队列
    filename_queue = tf.train.string_input_producer([filename])
    # 2、构建一个csv阅读器，去读取数据
    reader = tf.TextLineReader(skip_header_lines=0)
    # 开始读取数据，返回2个值，第一个值为行号，第二个值为内容
    _, csv_row = reader.read(filename_queue)
    # 3、文件解码setup CSV decoding
    record_defaults = [[0],[0],[0],[0],[0]]
    col1,col2,col3,col4,col5 = tf.decode_csv(csv_row, record_defaults=record_defaults)
    # turn features back into a tensor
    features = tf.stack([col1,col2,col3,col4])
    print("loading, " + str(file_length) + " line(s)\n")
    return features, col5

# 要读取的数据文件
filename = "csv_test_data.csv"
# 获取文件长度
file_length = file_len(filename)
# 读取文件
features,col5 = readcsv(filename)

with tf.Session() as sess:
    # 初始化变量
    tf.initialize_all_variables().run()

    # 4、开启线程操作
    # start populating filename queue
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord)

    for i in range(file_length):
        # 5、打印运行的结果
        # retrieve a single instance
        example, label = sess.run([features, col5])
        print(example, label)

    coord.request_stop()
    coord.join(threads)
```

运行结果如下所示：
```bash
[ 0 10  0  0] 0
[ 0 15  0  0] 1
[ 0 30  0  0] 2
[ 0 45  0  0] 3
```

## 读取csv文件集

在当前目录下的`data_csv/`文件夹中有3个csv文件，分别为`a.csv`、`b.csv`、`c.csv`，三个文件的内容如下所示：

a.csv
```
a1,20
a2,21
a3,22
```

b.csv
```
b1,15
b2,16
b3,17
```

c.csv
```
c1,15
c2,17
c3,19
```

完整代码如下所示：
```python
import tensorflow as tf
import os

def csvread(filelist):
    """
    读取CSV文件
    :param filelist: 文件路径+名字的列表
    :return: 读取的内容
    """
    # 1、构造文件的队列
    file_queue = tf.train.string_input_producer(filelist)

    # 2、构造csv阅读器读取队列数据（按一行）
    reader = tf.TextLineReader()
    # 读取数据，key为行号，value为每一行的内容
    key, value = reader.read(file_queue)

    # 3、对每行内容解码
    # record_defaults:指定每一个样本的每一列的类型，指定默认值[["None"], [4.0]]
    records = [["None"], [0]]
    example, label = tf.decode_csv(value, record_defaults=records)

    # 4、想要读取多个数据，就需要批处理
    # 一般capacity设置和batch_size一样，或者比它大。
    example_batch, label_batch = tf.train.batch([example, label], batch_size=9, num_threads=1, capacity=9)

    return example_batch, label_batch

if __name__ == "__main__":
    file_name = os.listdir("data_csv/")
    filelist = [os.path.join("data_csv/", file) for file in file_name]

    example_batch, label_batch = csvread(filelist)

    with tf.Session() as sess:
        # 初始化变量
        tf.initialize_all_variables().run()

        # 5、开启子线程
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)

        # 6、打印获取的数据
        print(sess.run([example_batch, label_batch]))

        # 关闭线程
        coord.request_stop()
        coord.join(threads)
```

运行结果如下所示：
```bash
[array([b'a1', b'a2', b'a3', b'c1', b'c2', b'c3', b'b1', b'b2', b'b3'],
      dtype=object), array([20, 21, 22, 15, 17, 19, 15, 16, 17], dtype=int32)]
```
