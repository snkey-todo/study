# 变量 Variable

变量也是一种OP，是一种特殊的张量，能够进行存储持久化，它的值就是张量。

## 变量的创建

创建一个带值initial_value的新变量`tf.Variable(initial_value=None,name=None)`

参数说明：

- assign(value)：为变量分配一个新值返回新值
- eval(session=None)：计算并返回此变量的值
- name：属性表示变量名字

## 变量的初始化

变量必须进行初始化，我们以代码进行说明：

```python
import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

a = tf.constant([1,2,3,4,5])
# 创建正态分布随机数变量
var = tf.Variable(tf.random_normal([2,3], mean=0.0, stddev=1.0))

# 做显示初始化op
init_op = tf.global_variables_initializer()

with tf.Session() as sess:
    # 必须运行初始化op
    sess.run(init_op)
    print(sess.run([a,var]))
```

我们在会话前必须调用`init_op = tf.global_variables_initializer()`做变量显示的初始化，把变量初始化成一个op，然后在会话中调用` sess.run(init_op)`来初始化变量。
