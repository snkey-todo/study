import tensorflow as tf


class CifarRead(object):

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

        # 4、分割出图片和标签数据，切出特征值和目标值
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

    def convert_to_tfrecords(self, image_batch, label_batch, file_path):
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

    def read_from_tfrecords(self, file_path):
        """
        读取tfrecords
        :return: None
        """
        file_queue = tf.train.string_input_producer([file_path,])

        reader = tf.TFRecordReader()

        key, value = reader.read(file_queue)

        features = tf.parse_single_example(value, features={
            "image": tf.FixedLenFeature([], tf.string),
            "label": tf.FixedLenFeature([], tf.int64),
        })
        # 对读取的内容进行解码
        image = tf.decode_raw(features["image"], tf.uint8)

        # 设置静态形状，可用于转换动态形状
        image.set_shape([self.image_bytes])

        print(image)

        image_tensor = tf.reshape(image, [self.height, self.width, self.channel])

        print(image_tensor)

        label = tf.cast(features["label"], tf.int32)

        print(label)

        image_batch, label_batch = tf.train.batch([image_tensor, label], batch_size=10, num_threads=1, capacity=10)
        print(image_batch)
        print(label_batch)

        return image_batch, label_batch
