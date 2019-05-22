# MachineLearning案例：鸢尾花二分分类

【拓展】
机器学习分为：监督学习和无监督学习。
监督学习主要为：离散分类和线性回归。
无监督学习主要为：聚类。

## 数据集

[鸢尾花数据集下载](http://archive.ics.uci.edu/ml/datasets/Iris)

在这个数据集中，鸢尾花分为三种，我们使用二分类法将其分类出来，首先利用其中的一个特征值，区分出一种，然后再区分剩下的两种。

事实上很多复杂的分类都可以使用二分分类的互相组合、嵌套来完成分类。

## 原始数据可视化

这个可以通过前面给出的链接去下载该数据集，也可以直接使用sklearn.datasets来导入这个数据集，我将数据集打印出来，发现它其实是一个JSON字符串。但是这个JSON在字符串是有点问题的，当我使用JSON格式化工具去格式化这个数据的时候，它会出现错误。但是使用键去取值的时候，却又是可以的。

我编写类`iris01.py`，进行数据可视化，该类的代码如下：

```python
# -*- coding:utf-8 -*-

from sklearn.datasets import load_iris
from matplotlib import pyplot as plt

# 直接调用sklearn.datasets数据集中的方法取得数据,它是一个JSON字符串,我将其打印出来拷贝到"./data/json.txt"文件中
data = load_iris()
#print data

# 数据特征值及名称，我们需要根据这4个特征来分类
# ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']
feature_names = data['feature_names']
features = data['data']

# 三种类型的花，0-setosa，1-versicolor，2-virginica
target = data['target']

# 有4个特征值，采用（x,y）坐标显示的话就有6中形式，我们将已有的数据可视化为6个图
pairs = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]

for i,(p0,p1) in enumerate(pairs):
    plt.subplot(2,3,i+1)
    for t,marker,c in zip(range(3),">ox","rgb"):
        plt.scatter(features[target == t,p0], features[target == t,p1], marker=marker, c=c)

    # x轴为sepal length，y轴为sepal width
    plt.xlabel(feature_names[p0])
    plt.ylabel(feature_names[p1])
    plt.xticks([])
    plt.yticks([])

plt.savefig('./images/1400_02_01.png')
```

我们进入py文件所在位置，执行`python iris01.py`将自动生成图片，并保存到images目录下。

```bash
➜  MLChapter2 git:(master) ✗ pwd
/Users/zhusheng/PycharmProjects/MachineLearning/MLChapter2
➜  MLChapter2 git:(master) ✗ ls
data      images    iris01.py iris02.py
➜  MLChapter2 git:(master) ✗ python iris01.py
➜  MLChapter2 git:(master) ✗
```

效果图如下：

![15.png](https://upload-images.jianshu.io/upload_images/5637154-972cd243bc11f547.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

