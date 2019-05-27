import tensorflow as tf
import os
from part2_read_data.TFRecord import CifarRead

"""
读取二进制文件
"""
# 定义cifar的数据等命令行参数
FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string("cifar_dir", "/Users/zhusheng/WorkSpace/Tmp/dataset/cifar-10-batches-bin/", "文件的目录")
tf.app.flags.DEFINE_string("cifar_tfrecords", "./tmp/cifar.tfrecords", "存进tfrecords的文件")


if __name__ == '__main__':
    # 找到文件，放入列表   路径+名字  ->列表当中
    file_name = os.listdir(FLAGS.cifar_dir)
    # 下载的数据集中，有一个test_batch.bin，我改了一下名称为test_batch.binn,方便删选
    # 取出后缀为bin的文件
    file_list = [os.path.join(FLAGS.cifar_dir, file) for file in file_name if file[-3:] == "bin"]
    print(file_list)

    # 读取数据
    cif = CifarRead(file_list)
    image_batch, label_batch = cif.read_and_decode()

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
