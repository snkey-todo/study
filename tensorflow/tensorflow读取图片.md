# tensorflow读取图片

## 图像基本知识

**图像三要素**
图像三要素：长度(height)、宽度(width)、通道数(channels)，我们可以使用一个3-D张量来表示：[height,width,channels]
说明：通道数为1，表示灰度值；通道数为3，表示RGB。

一般在拿到图片数据集后，我们都会对图片进行一些处理，指定3-D的shape大小，我们会将所有的图片进行缩放处理，变成统一大小的图片。

在处理图片数据的时候，我们最后会把数据包装成4-D张量：[nums,height,width,channels]，第一个值为样本数，如下所示：

`Tensor("batch:0", shape=(300, 200, 200, 1), dtype=float32)`

## 核心API

### 缩小图片

```
# 缩小图片
tf.image.resize_images(images, size)
```

参数说明：
- images：4-D形状[batch, height, width, channels]或3-D形状的张量[height, width, channels]的图片数据。
- size：1-D int32张量：new_height, new_width，图像的新尺寸返回4-D格式或者3-D格式图片。

### 图像读取API

**图像读取器**
```
# 将文件的全部内容作为值输出的读取器。
tf.WholeFileReader
```

参数说明：
- return：读取器实例

**WholeFileReader相关方法**

```
# 输出将是一个文件名（key）和该文件的内容（值）
read(file_queue)
```

**图像解码器**

```
# 将JPEG编码的图像解码为uint8张量
tf.image.decode_jpeg(contents)
```

参数说明：
- return:uint8张量，3-D形状[height, width, channels]

```
# 将PNG编码的图像解码为uint8或uint16张量
tf.image.decode_png(contents)
```

参数说明：
- return:张量类型，3-D形状[height, width, channels]

## 图片处理流程

1. 构造图片文件队列
2. 构造文件阅读器
3. 读取图片数据
4. 批处理图片
5. 在TensorFlow中运行

## 示例

```python
import tensorflow as tf
import os

def pictureRead(filelist):
    # 1、构造文件队列
    queue = tf.train.string_input_producer(filelist)

    # 2、构造阅读器去读取图片内容（默认读取一张图片）
    reader = tf.WholeFileReader()
    key,value = reader.read(queue)
    
    # Tensor("ReaderReadV2:1", shape=(), dtype=string)
    #print(value)

    # 3、解码
    images = tf.image.decode_jpeg(value)

    # Tensor("DecodeJpeg:0", shape=(?, ?, ?), dtype=uint8)
    #print(images)

    # 4、统一图片大小
    images_resize = tf.image.resize_images(images, [200, 200])

    # Tensor("resize/Squeeze:0", shape=(200, 200, ?), dtype=float32)
    #print(images_resize)

    # 注意：一定要把样本的形状固定 [200, 200, 1],在批处理的时候要求所有数据形状必须定义
    # 如果是RGB图片，设置成[200, 200, 3]
    images_resize.set_shape([200,200,1])

    # Tensor("resize/Squeeze:0", shape=(200, 200, 3), dtype=float32)
    #print(images_resize)

    # 5、批处理,获得4D tensor， 第一个为样本数量
    images_batch = tf.train.batch([images_resize], batch_size=300, num_threads=1, capacity=300)

    # Tensor("batch:0", shape=(50, 200, 200, 3), dtype=float32)
    #print(images_batch)
    return images_batch


if __name__ == "__main__":
    # 文件路径
    dir_mstar = "/Users/zhusheng/WorkSpace/Tmp/dataset/MSTAR/EOC-data/train/2S1-b01/"

    filenames = os.listdir(dir_mstar)
    filelist = [os.path.join(dir_mstar, file) for file in filenames]
    #print(filelist)
    
    images_batch = pictureRead(filelist)
    print(images_batch)

    with tf.Session() as sess:
        # 初始化变量
        sess.run(tf.local_variables_initializer())
        sess.run(tf.global_variables_initializer())
        
        # 开启线程去读取图片
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)
        print(sess.run(images_batch))
        
        # 回收线程
        coord.request_stop()
        coord.join(threads)
```

运行效果如下所示：

![屏幕快照 2019-05-15 23.40.53.png](https://upload-images.jianshu.io/upload_images/5637154-596c46102d47cd17.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
