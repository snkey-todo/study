import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


# 自定义命令行参数
FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_string('log_dir', 'logs/', 'tensorboard log路径')
tf.app.flags.DEFINE_string('model_dir', 'tmp/ckpt/model', '模型文件加载路径')
tf.app.flags.DEFINE_integer('max_step', 200, '模型训练的步数')

def mymigration():
    """
    自定义变量作用域
    :return:
    """
    with tf.variable_scope('data'):
        """
        使用函数模拟数据源
        """
        x = tf.random_normal([100,1], mean=1.75, stddev=0.5, name='x')
        y_true = tf.matmul(x, [[0.7]]) + 0.8

    with tf.variable_scope('model'):
        """
        随机给定一个权重weight、偏置bias，然后使用梯度下降算法来优化这两个参数，使得损失函数最小
        """
        weight = tf.Variable(tf.random_normal([1,1], mean=0.0, stddev=1.0, name='w'))
        bias = tf.Variable(0.0, name='b')
        y_predict = tf.matmul(x, weight) + bias

    with tf.variable_scope('loss'):
        """
        使用均方误差的方式计算损失函数。tf.square求方差，tf.reduce_mean求均值
        """
        loss = tf.reduce_mean(tf.square(y_true - y_predict))

    with tf.variable_scope('optimizer'):
        """
        使用学习率为0.1的梯度下降算法，求损失函数的最小值
        """
        train_op = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

    """
    在tensorboard中增加变量显示，通过图形化的方式了解参数的优化过程
    """
    # 1、收集变量
    # scalar，标量
    tf.summary.scalar('loss', loss)
    # histogram,直方图、柱状图
    tf.summary.histogram('weight', weight)

    # 2、合并变量，写入事件文件
    merge = tf.summary.merge_all()

    # 定义一个模型保存对象
    # 保存的最大副本数量
    saver = tf.train.Saver(var_list=None, max_to_keep=5)

    init_op = tf.global_variables_initializer()

    with tf.Session() as sess:
        sess.run(init_op)

        file_writer = tf.summary.FileWriter(FLAGS.log_dir, graph=sess.graph)

        print("随机给定的最初权重和偏置: 权重%f, 偏置%f" % (weight.eval(), bias.eval()))

        # 如果模型存在，加载模型
        if os.path.exists('tmp/ckpt/checkpoint'):
            saver.restore(sess, FLAGS.model_dir)

        for i in range(FLAGS.max_step):
            # 运行优化损失函数
            sess.run(train_op)
            print("第%d次优化的权重和偏置：权重%f, 偏置%f" % (i, weight.eval(), bias.eval()))

            # 3、运行合并的变量,并写入事件文件
            summary =  sess.run(merge)
            file_writer.add_summary(summary, i)

        saver.save(sess, FLAGS.model_dir)


if __name__ == '__main__':
    mymigration()