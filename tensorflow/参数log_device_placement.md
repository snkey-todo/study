# 参数log_device_placement

核心代码：`with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:`

以下是一个示例：

```python
import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

# 创建tensor
a = tf.constant(5.0)    
b = tf.constant(6.0)

# 创建op
sum = tf.add(a, b) 

# 通过Session执行graph
with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
    print(sess.run(sum))
```

输出信息如下所示：

```bash
(tensorflow) ➜  tensorflow git:(master) ✗ python b.py 
Device mapping: no known devices.
Add: (Add): /job:localhost/replica:0/task:0/device:CPU:0
Const: (Const): /job:localhost/replica:0/task:0/device:CPU:0
Const_1: (Const): /job:localhost/replica:0/task:0/device:CPU:0
11.0
```

参数log_device_placement，让我们可以看到我们的tensor、op是在哪台设备、哪颗CPU上运行的。
