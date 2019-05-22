import tensorflow as tf
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# 定义命令行参数
FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_string("csv_dir", "/Users/zhusheng/WorkSpace/Tmp/dataset/iris/", "csv文件路径")


def read_csv(file_list):
    """
    读取csv文件
    :param file_list:
    :return:
    """
    # 1、构造文件队列
    csv_queue = tf.train.string_input_producer(file_list)

    # 2、创建阅读器,跳过第一行的表头
    reader = tf.TextLineReader(skip_header_lines=1)
    key, value = reader.read(csv_queue)
    print(value)

    # 3、对每一行的内容进行解码
    # 默认值
    record_defaults = [["NAN"], [0.0], [0.0], [0.0], [0.0], ["NAN"]]
    serial_number, \
    sepal_length, \
    sepal_width, \
    petal_length, \
    petal_width, \
    species = tf.decode_csv(value, record_defaults=record_defaults)
    print("species-->", species)

    # 4、批处理
    serial_number_batch, \
    sepal_length_batch, \
    sepal_width_batch, \
    petal_length_batch, \
    petal_width_batch, \
    species_batch = tf.train.batch([serial_number, sepal_length, sepal_width, petal_length, petal_width, species],
                                   batch_size=150, num_threads=1, capacity=150)
    print("species_batch-->", species_batch)

    return serial_number_batch, \
           sepal_length_batch, \
           sepal_width_batch, \
           petal_length_batch, \
           petal_width_batch, \
           species_batch


if __name__ == '__main__':
    # 获取文件名称列表
    file_name = os.listdir(FLAGS.csv_dir)
    # 获取文件路径列表，过滤只读取csv结尾的文件
    file_list = [os.path.join(FLAGS.csv_dir, file) for file in file_name if file[-3:] == "csv"]
    print(file_list)

    serial_number_batch, \
    sepal_length_batch, \
    sepal_width_batch, \
    petal_length_batch, \
    petal_width_batch, \
    species_batch = read_csv(file_list)

    with tf.Session() as sess:
        # 创建线程协调器
        coord = tf.train.Coordinator()
        # 开启读取数据的子线程
        threads = tf.train.start_queue_runners(sess, coord=coord)

        # 打印读取的内容

        print(sess.run([
            serial_number_batch,
            sepal_length_batch,
            sepal_width_batch,
            petal_length_batch,
            petal_width_batch,
            species_batch]))

        # 回收线程
        coord.request_stop()
        coord.join(threads)
