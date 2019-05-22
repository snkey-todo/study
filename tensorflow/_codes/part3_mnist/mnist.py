from __future__ import absolute_import
from tensorflow.examples.tutorials.mnist import input_data

import tensorflow as tf

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string('data_dir', './tmp/tensorflow/mnist/input_data',
                           """数据集目录""")
tf.app.flags.DEFINE_integer('max_steps', 2000,
                            """训练次数""")
tf.app.flags.DEFINE_string('summary_dir', './tmp/summary/mnist/train',
                           """事件文件目录""")

def main(sess):
    # 输入数据
    mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True)


    # 建立输入数据占位符
    x = tf.placeholder(tf.float32, [None, 784])

    # 初始化权重和偏置
    W = tf.Variable(tf.zeros([784, 10]))
    b = tf.Variable(tf.zeros([10]))

    # 输出结果y
    y = tf.matmul(x, W) + b


    # 建立类别占位符
    y_label = tf.placeholder(tf.float32, [None, 10])

    # 计算交叉熵损失平均值
    cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_label, logits=y))
    # 生成优化损失操作
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
    # 比较结果
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_label, 1))
    # 计算正确率平均值
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    tf.summary.scalar("loss",cross_entropy)

    tf.summary.scalar("accuracy", accuracy)

    tf.summary.histogram("W",W)

    tf.global_variables_initializer().run()

    # 合并所有摘要
    merged = tf.summary.merge_all()
    summary_writer = tf.summary.FileWriter(FLAGS.summary_dir, graph=sess.graph)

    # 训练
    for i in range(1000):

        print("第%d次训练"%(i))
        batch_xs, batch_ys = mnist.train.next_batch(100)

        sess.run(train_step, feed_dict={x: batch_xs, y_label: batch_ys})

        print(sess.run(accuracy,feed_dict={x: batch_xs, y_label: batch_ys}))

        summary = sess.run(merged,feed_dict={x: batch_xs, y_label: batch_ys})

        summary_writer.add_summary(summary,i)

    # 模型在测试数据的准确率
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_label, 1))
    test_accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    print("测试数据准确率：")
    print(sess.run(test_accuracy, feed_dict={x: mnist.test.images,y_label: mnist.test.labels}))

if __name__ == '__main__':
    with tf.Session() as sess:
        main(sess)