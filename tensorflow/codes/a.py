import tensorflow as tf

x = tf.constant([[1,1],[2,2]], dtype=tf.float32)
a0 = tf.reduce_mean(x)
a1 = tf.reduce_mean(x,0)
a2 = tf.reduce_mean(x,1)

with tf.Session() as sess:
  print(sess.run([a0,a1,a2]))