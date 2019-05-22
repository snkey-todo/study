import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] ='2'


# 创建队列
Q = tf.FIFOQueue(1000, tf.float32)

# 创建1个变量
var = tf.Variable(0.0)
# 自增
data = tf.assign_add(var, tf.constant(1.0))
# 放入队列
en_q = Q.enqueue(data)

# 定义队列管理器，指定有2个线程去运行这个op
qr = tf.train.QueueRunner(Q, enqueue_ops=[en_q]*2)

init_op = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init_op)

    coord = tf.train.Coordinator()
    # 创建线程去执行op
    threads = qr.create_threads(sess, coord, start=True)

    # 取数据
    for i in range(30):
       print(sess.run(Q.dequeue()))

    coord.request_stop()
    coord.join(threads)
