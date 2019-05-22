# tensorflow读取二进制文件

数据集|The CIFAR-10 dataset，[我们选择下载二进制版本](https://www.cs.toronto.edu/~kriz/cifar-10-binary.tar.gz)，该数据集有5* 10000个样本图片和10000个测试样本图片。相关介绍如下所示：

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

也就是说，每个图片包含一个标签和3072个像素，每个图片包含3073 bytes。

## 读取二进制文件的步骤和核心代码

1、构造文件队列
```
file_queue = tf.train.string_input_producer(self.file_list)
```

2、创建文件阅读器
```
reader = tf.FixedLengthRecordReader(self.bytes)
key, value = reader.read(file_queue)
```
这里的`self.bytes`也就是3073.

3、解码
```
 label_image = tf.decode_raw(value, tf.uint8)
```
4、分割出图片和标签数据，切出特征值和目标值
```
label = tf.slice(label_image, [0], [self.label_bytes])
label = tf.cast(label, tf.int32)
image = tf.slice(label_image, [self.label_bytes], [self.image_bytes])
```

5、可以对图片的特征数据进行形状的改变 [3072] --> [32, 32, 3]
```
 image_reshape = tf.reshape(image, [self.height, self.width, self.channel])
```

6、批处理数据,总样本数为10000 *5 = 50000，为了节省运行时间，我改为100
```
image_batch, label_batch = tf.train.batch([image_reshape, label], batch_size=100, num_threads=1, capacity=100)
```

## 完整示例代码
```
import tensorflow as tf
import os

# 定义cifar的数据等命令行参数
FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string("cifar_dir", "/Users/zhusheng/WorkSpace/Tmp/dataset/cifar-10-batches-bin/", "文件的目录")
tf.app.flags.DEFINE_string("cifar_tfrecords", "./tmp/cifar.tfrecords", "存进tfrecords的文件")


class CifarRead(object):
    """
    读取二进制文件，写入tfrecords，读取tfrecords
    """

    def __init__(self, filelist):
        """
        构造器
        :param filelist:
        """
        # 文件列表
        self.file_list = filelist

        # 定义读取的图片的一些属性
        self.height = 32
        self.width = 32
        self.channel = 3
        # 二进制文件每张图片的字节
        self.label_bytes = 1
        self.image_bytes = self.height * self.width * self.channel
        self.bytes = self.label_bytes + self.image_bytes

    def read_and_decode(self):
        """
        读取二进制文件
        :return:
        """
        # 1、构造文件队列
        file_queue = tf.train.string_input_producer(self.file_list)

        # 2、构造二进制文件读取器，读取内容, 每个样本的字节数
        reader = tf.FixedLengthRecordReader(self.bytes)
        key, value = reader.read(file_queue)
        print("value", value)

        # 3、解码内容, 二进制文件内容的解码
        label_image = tf.decode_raw(value, tf.uint8)
        print("label_image", label_image)

        # 4、分割出图片和标签数据，切除特征值和目标值
        label = tf.slice(label_image, [0], [self.label_bytes])
        label = tf.cast(label, tf.int32)
        image = tf.slice(label_image, [self.label_bytes], [self.image_bytes])
        print("label", label)
        print("image", image)

        # 5、可以对图片的特征数据进行形状的改变 [3072] --> [32, 32, 3]
        image_reshape = tf.reshape(image, [self.height, self.width, self.channel])
        print("image_reshape", image_reshape)

        # 6、批处理数据,总样本数为10000 *5 = 50000，为了节省运行时间，我改为100
        image_batch, label_batch = tf.train.batch([image_reshape, label], batch_size=100, num_threads=1, capacity=100)
        print("image_batch:",image_batch, "\nlabel_batch:", label_batch)
        return image_batch, label_batch


if __name__ == '__main__':
    # 找到文件，放入列表   路径+名字  ->列表当中
    file_name = os.listdir(FLAGS.cifar_dir)
    # 下载的数据集中，有一个test_batch.bin，我改了一下名称为test_batch.binn,方便删选
    # 取出后缀为bin的文件
    file_list = [os.path.join(FLAGS.cifar_dir, file) for file in file_name if file[-3:] == "bin"]
    print(file_list)

    # 读取数据
    cf = CifarRead(file_list)
    image_batch, label_batch = cf.read_and_decode()

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

运行结果如下：
```
[array([[[[ 59,  43,  50],
         [ 68,  98, 119],
         [139, 145, 149],
         ...,
         [127, 126, 127],
         [130, 142, 130],
         [118, 120, 109]],
...,
       [1],
       [1],
       [4],
       [1]], dtype=int32)]

Process finished with exit code 0
```

