import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] ='2'


# 创建队列，并放入数据
Q = tf.FIFOQueue(3, tf.float32)
queue_many = Q.enqueue_many([[0.1, 0.2, 0.3], ])

# 从队列取一个数据
data1 = Q.dequeue()
# 数据加一
data2 = data1 + 1
# 将数据放入队列
en_q = Q.enqueue(data2)


with tf.Session() as sess:
    # 初始化队列
    sess.run(queue_many)

    # 进行100次操作，tensorflow操作具有依赖性，执行该tensor即可
    for i in range(100):
        sess.run(en_q)

    # 取出队列中的数据
    for i in range(Q.size().eval()):
        print(sess.run(Q.dequeue()))

