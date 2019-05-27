import tensorflow as tf
import os


def pictureRead(filelist):
    # 1、构造文件队列
    queue = tf.train.string_input_producer(filelist)

    # 2、构造阅读器去读取图片内容（默认读取一张图片）
    reader = tf.WholeFileReader()
    key, value = reader.read(queue)

    # Tensor("ReaderReadV2:1", shape=(), dtype=string)
    # print(value)

    # 3、解码
    images = tf.image.decode_jpeg(value)

    # Tensor("DecodeJpeg:0", shape=(?, ?, ?), dtype=uint8)
    # print(images)

    # 4、统一图片大小
    images_resize = tf.image.resize_images(images, [200, 200])

    # Tensor("resize/Squeeze:0", shape=(200, 200, ?), dtype=float32)
    # print(images_resize)

    # 注意：一定要把样本的形状固定 [200, 200, 1],在批处理的时候要求所有数据形状必须定义
    # 如果是RGB图片，设置成[200, 200, 3]
    images_resize.set_shape([200, 200, 1])

    # Tensor("resize/Squeeze:0", shape=(200, 200, 3), dtype=float32)
    # print(images_resize)

    # 5、批处理,获得4D tensor， 第一个为样本数量
    images_batch = tf.train.batch([images_resize], batch_size=300, num_threads=1, capacity=300)

    # Tensor("batch:0", shape=(50, 200, 200, 3), dtype=float32)
    # print(images_batch)
    return images_batch


if __name__ == "__main__":
    # 文件路径
    dir_mstar = "/Users/zhusheng/WorkSpace/Tmp/dataset/MSTAR/EOC-data/train/2S1-b01/"

    filenames = os.listdir(dir_mstar)
    filelist = [os.path.join(dir_mstar, file) for file in filenames]
    # print(filelist)

    images_batch = pictureRead(filelist)
    print(images_batch)

    with tf.Session() as sess:
        # 初始化变量
        sess.run(tf.local_variables_initializer())
        sess.run(tf.global_variables_initializer())

        # 开启线程去读取图片
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)
        print(sess.run(images_batch))

        # 回收线程
        coord.request_stop()
        coord.join(threads)