# tensorflow队列和线程

## 队列

tensorflow有两种队列：
- tf.FIFOQueue：先进先出队列，按顺序出队列
- tf.RandomShuffleQueue：随机出队列

两个API的使用基本差不多，我们以FIFOQueue为例说明。

**核心API**

```python
FIFOQueue(capacity, dtypes, name='fifo_queue')
```

参数说明：
- capacity：整数。可能存储在此队列中的元素数量的上限。
- dtypes：DType对象列表。长度dtypes必须等于每个队列元素中的张量数,dtype的类型形状，决定了后面进队列元素形状。

 **FIFOQueue队列对象的相关方法**

- dequeue(name=None)：出队列
- enqueue(vals, name=None)：入队列
- enqueue_many(vals, name=None)：入队列，vals为列表或者元组
- size(name=None)：队列元素大小

我们通过一个示例来说明队列的作用，大致流程如下：
1. 创建一个可以存放3个数据的队列；
2. 放数据到队列中；
3. 定义一个从队列中取数据、将数据执行+1操作，然后将处理后的数据放回到队列中；

说明：tensor的操作有依赖性。

**示例代码**

```python
import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

# 1、定义队列，并放入数据
Q = tf.FIFOQueue(3, tf.float32)
enq_many = Q.enqueue_many([[0.1, 0.2, 0.3],])

# 2、定义读数据、取数据的过程、取数据+1，入队列
de_q= Q.dequeue()
data = de_q + 1
en_q = Q.enqueue(data)

with tf.Session() as sess:
    # 初始化队列
    sess.run(enq_many)

    # 处理数据
    for i in range(100):
        # tensorflow的操作有依赖性
        sess.run(en_q)
    # 训练数据
    for i in range(Q.size().eval()):
        print(sess.run(Q.dequeue()))
```

运行结果如下图所示；

```bash
33.2
33.3
34.1
```

## 线程

线程涉及到2个核心概念：队列管理器和线程协调器。

### 队列管理器QueueRunner

什么是队列管理器？
我们可以把我们的队列放到队列管理器中，并创建一个线程来运行我们的队列。

**核心API**
```python
# 创建一个QueueRunner
tf.train.QueueRunner(queue, enqueue_ops=None)
```

参数说明：
- queue：A Queue
- enqueue_ops：添加线程的队列操作列表，[]*2,指定两个线程

**QueueRunner相关方法**

create_threads(sess, coord=None,start=False)：创建线程来运行给定会话的入队操作

参数说明：
- start：布尔值，如果True启动线程；如果为False调用者必须调用start()启动线程 
- coord：线程协调器，后面线程管理需要用到
- return：线程的实例

### 线程协调器Coordinator

什么是线程协调器？
用来协调子线程和主线程，当我们在会话中开启子线程去做一些事情的时候，我们的会话执行完了，但是子线程还在运行，可是子线程的运行必须依赖会话，所以就会报错。有了线程协调器，我们可以在会话中等待子线程运行结束。

**核心API**

```python
# 线程协调员,实现一个简单的机制来协调一组线程的终止，返回一个Coordinator对象。
tf.train.Coordinator()
```

**Coordinator相关方法**

request_stop()：请求停止，等待子线程运行结束后停止。
should_stop()：检查是否要求停止，立即停止。
join(threads=None, stop_grace_period_secs=120) ：将子线程加入Coordinator，等待线程终止进行回收。

**示例代码**

```python
import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

# 1、定义1个队列，可以放1000个数据
Q = tf.FIFOQueue(1000, tf.float32)

# 2、定义要做的事情（例如：循环 +1， 放入线程）
var  = tf.Variable(0.0)
# 实现一个自增
data = tf.assign_add(var, tf.constant(1.0))
# 把数据放入队列
en_q = Q.enqueue(data)

# 3、定义队列管理器op, 指定多少个子线程，子线程该干什么事
qr = tf.train.QueueRunner(Q, enqueue_ops=[en_q] * 2)

# 初始化变量的op
init_op = tf.global_variables_initializer()

with tf.Session() as sess:
    # 初始化变量
    sess.run(init_op)

    # 线程协调器、线程管理员
    coord = tf.train.Coordinator()
    # 真正开启子线程,去做那些事
    threads = qr.create_threads(sess, coord=coord, start=True)
    # 主线程，不断的去从队列中读取数据
    for i in range(300):
        print(sess.run(Q.dequeue()))
    # 回收子线程
    coord.request_stop()
    coord.join(threads)
```

运行结果如下：
```bash
24.0
300.0
524.0
668.0
1001.0
1002.0
1003.0
...
1294.0
1295.0
1296.0
```



