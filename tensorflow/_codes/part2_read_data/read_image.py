import tensorflow as tf
import  os

# 定义命令行参数
FLAGS = tf.app.flags.FLAGS
# 158*158*1
tf.app.flags.DEFINE_string("pic_dir", "/Users/zhusheng/WorkSpace/Tmp/dataset/MSTAR/EOC-data/train/2S1-b01/", "图片文件路径")

def pic_read(file_list):
    """
    读取图片
    :param file_list:
    :return:
    """
    # 1、构造文件队列
    file_queue = tf.train.string_input_producer(file_list)

    # 2、构造阅读器
    reader = tf.WholeFileReader()
    key, value = reader.read(file_queue)
    print("value-->", value)

    # 3、解码
    image_decode = tf.image.decode_jpeg(value)
    print("image_decode-->",image_decode)

    # 4、处理图片的大小
    image_resize = tf.image.resize_images(image_decode, [158, 158])
    print("image_resize-->",image_resize)
    # 一定要把样本的形状固定 [200, 200, 3],在批处理的时候要求所有数据形状必须定义
    image_resize.set_shape([158,158,1])
    print("image_resize-->", image_resize)

    # 5、批处理
    image_batch = tf.train.batch([image_resize], batch_size=300, num_threads=1, capacity=300)
    print("image_batch-->", image_batch)

    return image_batch


if __name__ == '__main__':
    file_name = os.listdir(FLAGS.pic_dir)
    file_list = [os.path.join(FLAGS.pic_dir, file) for file in file_name]
    print(file_list)

    image_batch = pic_read(file_list)
    print("image_batch-->",image_batch)

    with tf.Session() as sess:
        # 定义线程协调器
        coord = tf.train.Coordinator()
        # 开启读取图片的线程
        threads = tf.train.start_queue_runners(sess=sess, coord=coord)

        # 打印读取的内容，也是图的运行结果
        print(sess.run([image_batch]))

        # 回收线程
        coord.request_stop()
        coord.join(threads)

