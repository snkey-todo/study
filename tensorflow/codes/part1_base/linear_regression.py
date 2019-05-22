import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'


def mymigration():
    """
    自实现一个线性回归预测
    """
    # 1、通过一个公式模拟数据
    x = tf.random_normal([100,1], mean=1.75, stddev=0.5, name="x")
    # 矩阵相乘必须是二维的
    y_true = tf.matmul(x, [[0.7]]) + 0.8

    # 2、建立线性回归模型,1个权重、1个偏置， y = w * x + b
    # 随机给一个权重和偏置，让它去计算损失，也就相当于梯度下降的起点
    # 在这里，我们的weight和bias是需要去优化的，它是变化的，必须使用tf.Variable去定义
    # 在训练过程中，我们可以通过设置trainable=False来限制某个变量不跟随梯度下降进行优化，默认是True
    # 随机创建一个变量weight
    weight = tf.Variable(tf.random_normal([1, 1], mean=0.0, stddev=1.0, name="w"))
    print("weight-->", weight)
    bias = tf.Variable(0.0, name="b")
    print("bias-->", bias)
    y_predict = tf.matmul(x, weight) + bias

    # 3、建立损失函数，计算均方误差。
    # tf.square求方差，reduce_mean()求平均值
    loss = tf.reduce_mean(tf.square(y_true - y_predict))

    # 4、梯度下降优化损失，learning_rate=0~1, 2, 3, ...
    train_op = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

    # 通过会话运行程序
    # 定义一个初始化变量的op
    init_op = tf.global_variables_initializer()
    with tf.Session() as sess:
        # 初始化变量
        sess.run(init_op)

        # 将图写入事件文件，可以在tensorboard中进行可视化
        filew_ritter = tf.summary.FileWriter('logs/', graph=sess.graph)

        # 运行优化200次，也就是run op 200次
        print("随机最先初始化的权重和偏置：权重为:%f, 偏置为:%f" % (weight.eval(), bias.eval()))
        for i in range(200):
            sess.run(train_op)
            print("第%d次优化的权重和偏置：权重为:%f, 偏置为:%f" % (i, weight.eval(), bias.eval()))


if __name__ == "__main__":
    mymigration()