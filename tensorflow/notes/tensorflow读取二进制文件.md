# tensorflow读取二进制文件

## 数据集

[数据集|The CIFAR-10 dataset,我们选择下载二进制版本](https://www.cs.toronto.edu/~kriz/cifar-10-binary.tar.gz)，该数据集有5* 10000个样本图片和10000个测试样本图片。相关介绍如下所示：

```
Binary version
The binary version contains the files data_batch_1.bin, data_batch_2.bin, ..., data_batch_5.bin, as well as test_batch.bin. Each of these files is formatted as follows:
<1 x label><3072 x pixel>
...
<1 x label><3072 x pixel>
In other words, the first byte is the label of the first image, which is a number in the range 0-9. The next 3072 bytes are the values of the pixels of the image. The first 1024 bytes are the red channel values, the next 1024 the green, and the final 1024 the blue. The values are stored in row-major order, so the first 32 bytes are the red channel values of the first row of the image. 

Each file contains 10000 such 3073-byte "rows" of images, although there is nothing delimiting the rows. Therefore each file should be exactly 30730000 bytes long. 

There is another file, called batches.meta.txt. This is an ASCII file that maps numeric labels in the range 0-9 to meaningful class names. It is merely a list of the 10 class names, one per row. The class name on row i corresponds to numeric label i.
```

每个图片包含一个标签和3072个像素，32 * 32=1024, 1024*3 = 3072，3072是通道为RGB 3通道。

## 读取二进制文件

### 步骤分析

1、构造文件队列

```python
file_queue = tf.train.string_input_producer(file_list)
```

2、创建文件阅读器

```python
reader = tf.FixedLengthRecordReader(bytes)
key, value = reader.read(file_queue)
```
这里的`bytes`也就是3073.

3、对读取的每一行内容进行解码，解码为unit8格式。

```
 label_image = tf.decode_raw(value, tf.uint8)
```
4、分割出图片和标签数据，切出特征值和目标值

```
label = tf.slice(label_image, [0], label_bytes)
label = tf.cast(label, tf.int32)
image = tf.slice(label_image, label_bytes, image_bytes)
```

5、转换图片形状。可以对图片的特征数据进行形状的改变 [3072] --> [32, 32, 3]

```
image_reshape = tf.reshape(image, [height, width, channel])
```

6、批处理数据。总样本数为10000 *5 = 50000，为了节省运行时间，我改为100

```
image_batch, label_batch = tf.train.batch([image_reshape, label], batch_size=100, num_threads=1, capacity=100)
```

### 完整代码
```python
import tensorflow as tf
import os

"""
读取二进制文件
"""
# 定义cifar的数据等命令行参数
FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string("cifar_dir", "/Users/zhusheng/WorkSpace/Tmp/dataset/cifar-10-batches-bin/", "文件的目录")
tf.app.flags.DEFINE_string("cifar_tfrecords", "./tmp/cifar.tfrecords", "存进tfrecords的文件")

# 图片的基本数据

height = 32
width = 32
channel = 3
label_bytes = 1
image_bytes = height * width * channel
bytes = label_bytes + image_bytes


def read_and_decode(file_list):
    """
    读取二进制文件
    :return:
    """
    # 1、构造文件队列
    file_queue = tf.train.string_input_producer(file_list)

    # 2、构造二进制文件读取器，读取内容, 每个样本的字节数
    reader = tf.FixedLengthRecordReader(bytes)
    key, value = reader.read(file_queue)
    print("value", value)

    # 3、解码内容, 二进制文件内容的解码
    label_image = tf.decode_raw(value, tf.uint8)
    print("label_image", label_image)

    # 4、分割出图片和标签数据，切出特征值和目标值
    label = tf.slice(label_image, [0], [label_bytes])
    label = tf.cast(label, tf.int32)
    image = tf.slice(label_image, [label_bytes], [image_bytes])
    print("label", label)
    print("image", image)

    # 5、可以对图片的特征数据进行形状的改变 [3072] --> [32, 32, 3]
    image_reshape = tf.reshape(image, [height, width, channel])
    print("image_reshape", image_reshape)

    # 6、批处理数据,总样本数为10000 *5 = 50000，为了节省运行时间，我改为100
    image_batch, label_batch = tf.train.batch([image_reshape, label], batch_size=100, num_threads=1, capacity=100)
    print("image_batch:", image_batch, "\nlabel_batch:", label_batch)
    return image_batch, label_batch


if __name__ == '__main__':
    # 找到文件，放入列表   路径+名字  ->列表当中
    file_name = os.listdir(FLAGS.cifar_dir)
    # 下载的数据集中，有一个test_batch.bin，我改了一下名称为test_batch.binn,方便删选
    # 取出后缀为bin的文件
    file_list = [os.path.join(FLAGS.cifar_dir, file) for file in file_name if file[-3:] == "bin"]
    print(file_list)

    # 读取数据
    image_batch, label_batch = read_and_decode(file_list)

    # 开启会话运行结果
    with tf.Session() as sess:
        # 定义一个线程协调器
        coord = tf.train.Coordinator()
        # 开启读文件的线程
        threads = tf.train.start_queue_runners(sess, coord=coord)

        # 打印读取的内容
        print(sess.run([image_batch, label_batch]))

        # 回收子线程
        coord.request_stop()
        coord.join(threads)
```

## TFRecords

### TFRecords简介

TFRecords是Tensorflow设计的一种*内置文件格式*，是一种二进制文件，
它能更好的利用内存，方便进行数据的复制和移动。

TFRecords存储的文件格式为：*.tfrecords，文件写入的内容为：Example协议块。

为了将二进制数据和标签(训练的类别标签)数据存储在同一个文件中。

### 步骤分析

写入步骤：

1. 构造存储器
2. 构造每一个样本的Example
3. 写入序列化的Example

读取步骤：

1. 构造TFRecords阅读器
2. 解析Example
3. 转换格式，bytes解码

### 核心API

1、建立TFRecord存储器

```python
# 将内容写入tfrecords文件
tf.python_io.TFRecordWriter(path)
```

参数说明：

- path：TFRecords文件的路径，例如：`"./tmp/cifar.tfrecords"`,是一个以`.tfrecords`结尾的文件。
- return：返回一个文件写入器对象。

相关方法：

```python
# 向文件中写入一个字符串记录。
write(record)

# 关闭文件写入器。
close()
```

2、构造每个样本的Example协议块

```python
# 写入tfrecords文件的内容是协议块
tf.train.Example(features=None)
```

参数说明：

- features：tf.train.Features类型的特征实例
- return：example格式协议块

```python
# 构建每个样本的信息键值对
tf.train.Features(feature=None)
```

参数说明：

- feature:字典数据,key为要保存的名字，value为tf.train.Feature实例
- return:Features类型

```python
features = tf.parse_single_example(value, features={
            "image": tf.FixedLenFeature([], tf.string),
            "label": tf.FixedLenFeature([], tf.int64),
        })
```

3、解析

解析TFRecords的example协议内存块

```python
# 解析一个单一的Example原型
tf.parse_single_example(serialized,features=None,name=None)
```

参数说明：

- serialized：标量字符串Tensor，一个序列化的Example
- features：dict字典数据，键为读取的名字，值为FixedLenFeature
- return:一个键值对组成的字典，键为读取的名字

```python
tf.FixedLenFeature(shape,dtype)
```

参数说明：

- shape：输入数据的形状，一般不指定,为空列表
- dtype：输入数据类型，与存储进文件的类型要一致，类型只能是float32,int64,string。

### TFRecord写入完整代码

```python
import tensorflow as tf
import os

"""
保存数据到TFRecords
"""
# 定义cifar的数据等命令行参数
FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string("cifar_dir", "/Users/zhusheng/WorkSpace/Tmp/dataset/cifar-10-batches-bin/", "文件的目录")
tf.app.flags.DEFINE_string("cifar_tfrecords", "./tmp/cifar.tfrecords", "存进tfrecords的文件")


# 图片的基本数据
height = 32
width = 32
channel = 3
label_bytes = 1
image_bytes = height * width * channel
bytes = label_bytes + image_bytes


def read_and_decode(file_list):
    """
    读取二进制文件
    :return:
    """
    # 1、构造文件队列
    file_queue = tf.train.string_input_producer(file_list)

    # 2、构造二进制文件读取器，读取内容, 每个样本的字节数
    reader = tf.FixedLengthRecordReader(bytes)
    key, value = reader.read(file_queue)
    print("value", value)

    # 3、解码内容, 二进制文件内容的解码
    label_image = tf.decode_raw(value, tf.uint8)
    print("label_image", label_image)

    # 4、分割出图片和标签数据，切出特征值和目标值
    label = tf.slice(label_image, [0], [label_bytes])
    label = tf.cast(label, tf.int32)
    image = tf.slice(label_image, [label_bytes], [image_bytes])
    print("label", label)
    print("image", image)

    # 5、可以对图片的特征数据进行形状的改变 [3072] --> [32, 32, 3]
    image_reshape = tf.reshape(image, [height, width, channel])
    print("image_reshape", image_reshape)

    # 6、批处理数据,总样本数为10000 *5 = 50000，为了节省运行时间，我改为100
    image_batch, label_batch = tf.train.batch([image_reshape, label], batch_size=100, num_threads=1, capacity=100)
    print("image_batch:", image_batch, "\nlabel_batch:", label_batch)
    return image_batch, label_batch


def convert_to_tfrecords(image_batch, label_batch, file_path):
    """
    将图片的特征值和目标值存进tfrecords
    :param image_batch:
    :param label_batch:
    :return:
    """
    # 1、建立TFRecords存储器
    writer = tf.python_io.TFRecordWriter(file_path)

    # 2、循环将所有样本写入文件中，每张图片都要构造example协议
    for i in range(10):
        # 取出第i个图片的数据的特征值和目标值
        image = image_batch[i].eval().tostring()
        label = int(label_batch[i].eval()[0])

        # 构造一个样本的example
        example = tf.train.Example(features=tf.train.Features(feature={
            "image": tf.train.Feature(bytes_list=tf.train.BytesList(value=[image])),
            "label": tf.train.Feature(int64_list=tf.train.Int64List(value=[label])),
        }))

        # 写入单独的样本
        writer.write(example.SerializeToString())

    # 关闭
    writer.close()


if __name__ == '__main__':
    # 找到文件，放入列表   路径+名字  ->列表当中
    file_name = os.listdir(FLAGS.cifar_dir)
    # 下载的数据集中，有一个test_batch.bin，我改了一下名称为test_batch.binn,方便删选
    # 取出后缀为bin的文件
    file_list = [os.path.join(FLAGS.cifar_dir, file) for file in file_name if file[-3:] == "bin"]
    print(file_list)

    # 读取二进制数据
    image_batch, label_batch = read_and_decode(file_list)

    # 开启会话运行结果
    with tf.Session() as sess:
        # 定义一个线程协调器
        coord = tf.train.Coordinator()
        # 开启读文件的线程
        threads = tf.train.start_queue_runners(sess, coord=coord)

        # 打印读取的内容
        #print(sess.run([image_batch, label_batch]))

        # 将数据存储到TFRecords存储器中
        print("开始存储")
        convert_to_tfrecords(image_batch, label_batch, FLAGS.cifar_tfrecords)
        print("结束存储")

        # 回收子线程
        coord.request_stop()
        coord.join(threads)
```

### TFRecord读取完整代码

```python
import tensorflow as tf
import os

"""

从TFRecord中读取数据

"""

# 定义cifar的数据等命令行参数
FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_string("cifar_dir", "/Users/zhusheng/WorkSpace/Tmp/dataset/cifar-10-batches-bin/", "文件的目录")
tf.app.flags.DEFINE_string("cifar_tfrecords", "./tmp/cifar.tfrecords", "存进tfrecords的文件")


image_bytes = 32 * 32 * 3

def read_from_tfrecords(file_path):
    """
    读取tfrecords
    :return: None
    """
    file_queue = tf.train.string_input_producer([file_path, ])

    reader = tf.TFRecordReader()

    key, value = reader.read(file_queue)

    features = tf.parse_single_example(value, features={
        "image": tf.FixedLenFeature([], tf.string),
        "label": tf.FixedLenFeature([], tf.int64),
    })
    # 对读取的内容进行解码
    image = tf.decode_raw(features["image"], tf.uint8)

    # 设置静态形状，可用于转换动态形状
    image.set_shape([image_bytes])
    print(image)

    image_tensor = tf.reshape(image, [32, 32, 3])
    print(image_tensor)

    label = tf.cast(features["label"], tf.int32)
    print(label)

    image_batch, label_batch = tf.train.batch([image_tensor, label], batch_size=10, num_threads=1, capacity=10)
    print(image_batch)
    print(label_batch)

    return image_batch, label_batch


if __name__=="__main__":

    # 从TFRecord文件中读取数据，首先得有这个文件，我们先往里面保存数据。
    image_batch, label_batch = read_from_tfrecords(FLAGS.cifar_tfrecords)

    with tf.Session() as sess:
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=sess, coord=coord)

        print(sess.run([image_batch, label_batch]))

        coord.request_stop()
        coord.join(threads)
```

