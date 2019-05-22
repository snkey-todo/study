import tensorflow as tf
import os
from part2_read_data.TFRecord import CifarRead

"""

从TFRecord中读取数据

"""

# 定义cifar的数据等命令行参数
FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_string("cifar_dir", "/Users/zhusheng/WorkSpace/Tmp/dataset/cifar-10-batches-bin/", "文件的目录")
tf.app.flags.DEFINE_string("cifar_tfrecords", "./tmp/cifar.tfrecords", "存进tfrecords的文件")

if __name__=="__main__":

    # 构造文件名字的列表
    filename = os.listdir(FLAGS.cifar_dir)
    file_list = [os.path.join(FLAGS.cifar_dir, file) for file in filename if file[-3:] == "bin"]

    # 从TFRecord文件中读取数据，首先得有这个文件，我们先往里面保存数据。
    cfar = CifarRead(file_list)
    image_batch, label_batch = cfar.read_from_tfrecords(FLAGS.cifar_tfrecords)

    with tf.Session() as sess:
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=sess, coord=coord)

        print(sess.run([image_batch, label_batch]))

        coord.request_stop()
        coord.join(threads)

