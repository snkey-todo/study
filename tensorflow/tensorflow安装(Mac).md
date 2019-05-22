# tensorflow安装(Mac)

（1）创建隔离环境

创建隔离环境，取名为`tensorflow`,指令如下：

```bash
mkvirtualenv -p python3.6 tensorflow
```

（2）安装tensorflow

方式1:

```bash
pip install [<u>https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.12.0-py3-none-any.whl</u>](https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.12.0-py3-none-any.whl)
```

说明：需要翻墙

方式2:安装最新版本

```bash
pip install --upgrade tensorflow
```

验证安装效果：

```bash
python -c "import tensorflow as tf; tf.enable_eager_execution(); print(tf.reduce_sum(tf.random_normal([1000, 1000])))"
```

方式3:安装指定版本

```bash
pip install tensorflow==1.12.0
```

安装完成效果图：

![屏幕快照 2019-05-09 11.56.21.png](https://upload-images.jianshu.io/upload_images/5637154-fdbd4838e5b2764b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
