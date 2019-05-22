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