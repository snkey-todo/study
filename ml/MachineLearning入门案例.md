# MachineLearning入门案例

[Github源代码下载](https://github.com/zhusheng/MachineLearning/tree/master/MLChapter1)

参考书籍：《机器学习系统设计》

## 应用案例说明

我们有一个数据集，是一个网站每小时的web访问量，随着公司业务的发展越来越好，我们需要扩展我们的服务器硬件资源，从一开始就扩展是很不划算的，我们可以在达到某一定访问量的时候进行扩展，比如在达到100万的时候扩展1次、在1000万的时候再次升级。

那么我们现有的访问量何时会达到100万、1000万次呢，重点来了，我们需要根据现有的数据训练出一个数据模型，并模拟未来的访问数据量在何时达到这个层次。

## 读取数据

通过下面的代码我们将现有的数据读取出来，我们可以打印看看这个数据是怎么样的。

```python
data = sp.genfromtxt('./data/web_traffic.tsv', delimiter="\t")
print data
```

执行结果如下，它是一个二维数组，每个数组有两个值，第一个数值为小时信息，它是从1、2、3依次递增的，第二个数值为该小时的web访问数量。我们看到是会存在在某个小时的web访问量是nan，也就是null。

```
➜  MLChapter1 git:(master) ✗ python test_scipy.py 
[[  1.00000000e+00   2.27200000e+03]
 [  2.00000000e+00              nan]
 [  3.00000000e+00   1.38600000e+03]
 ..., 
 [  7.41000000e+02   5.39200000e+03]
 [  7.42000000e+02   5.90600000e+03]
 [  7.43000000e+02   4.88100000e+03]]

```

## 数据预处理和数据清洗

我们将数据源data按照纬度切分为两个向量，x向量（其实就是一个一纬数组）表示小时，y向量表示web访问量。

web访问量为nan的数据是无效的数据，我们需要过滤掉，然后使用“～”取反得到有效的数值。

```python
#数据预处理
x = data[:,0]
y = data[:,1]

#数据清洗：挑选y值合法的选项
x = x[~sp.isnan(y)]
y = y[~sp.isnan(y)]
```

我们可以通过下面的方式统计有多少个数值为nan,

```python
print sp.sum(sp.isnan(y))
```

## 数据可视化1

可视化需要用到matplotlib框架，我们直接导入包就可以使用，核心代码如下：

```python
import matplotlib.pyplot as plt

#指定坐标为x，y
plt.scatter(x,y)
#指定图、横轴和纵轴的标题
plt.title("Web traffic over the last month")
plt.xlabel("Time")
plt.ylabel("Hits/hour")
#设置横轴的记号
plt.xticks( [w * 7 * 24 for w in range(10)], ['week %i' % w for w in range(10)])
#设置显示方式
plt.autoscale(tight==True)
plt.grid()
plt.show()
```

我们执行test_scipy.py文件

```python
python test_scipy.py
```

执行完成后，自动弹出一个图形化页面，如下图所示：

![11.png](https://upload-images.jianshu.io/upload_images/5637154-7c133e5389f57fc8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

考虑到后续会多次用到数据可视化代码，我们写一个方法，代码如下，它会将可视化的结果保存为一张图片。

```python
# plot input data and save the results as a picture
colors = ['g', 'k', 'b', 'm', 'r']
linestyles = ['-', '-.', '--', ':', '-']

def plot_models(x, y, models, fname, mx=None, ymax=None, xmin=None):
    plt.clf()
    # 指定坐标为x，y
    plt.scatter(x, y, s=10)
    # 指定标题
    plt.title("Web traffic over the last month")
    plt.xlabel("Time")
    plt.ylabel("Hits/hour")
    # 设置横轴的记号
    plt.xticks(
        [w * 7 * 24 for w in range(10)], ['week %i' % w for w in range(10)])

    if models:
        if mx is None:
            mx = sp.linspace(0, x[-1], 1000)
        for model, style, color in zip(models, linestyles, colors):
            # print "Model:",model
            # print "Coeffs:",model.coeffs
            plt.plot(mx, model(mx), linestyle=style, linewidth=2, c=color)

        plt.legend(["d=%i" % m.order for m in models], loc="upper left")

    plt.autoscale(tight=True)
    plt.ylim(ymin=0)
    if ymax:
        plt.ylim(ymax=ymax)
    if xmin:
        plt.xlim(xmin=xmin)
    plt.grid(True, linestyle='-', color='0.75')
    plt.savefig(fname)
```

有了上面的函数，我们可以调用该函数来进行可视化操作：其中x和y是我们前面的数据源，我们将可视化的结果保存到项目中，存为一张图片。其中“./images”路径需要我们手动创建一下。

```python
plot_models(x, y, None, os.path.join("./images", "1400_01_01.png"))
```

## 数据训练1

上面我们将我们的原始数据进行了可视化操作，但这个似乎只是体现了Scipy的强大，这并不是我们的目的，我们需要基于这个数据训练一个数据模型。

### 训练数据模型1

polyfit函数可以基于给出的数据训练出一个数据模型，下面的代码中，我们基于前面的数据x和y，并指出数据模型的阶数为1，训练的数据模型为fp1。

```python
fp1, res, rank, sv, rcond = sp.polyfit(x, y, 1, full=True)
print("Model parameters: %s" % fp1)
```

输出结果如下

```python
Model parameters: [   2.59619213  989.02487106]
```

也就是说我们的一阶数据函数是y=2.59619213 * x + 989.02487106

我们将数据模型转变为标准的模型函数，需要用到poly1d函数，它直接讲一个数据模型转变为模型函数。

```python
f1 = sp.poly1d(fp1)
```

### 训练结果1

我们将f1函数输出出来

```python
fx =sp.linspace(0,x[-1], 1000)
plt.plot(fx,f1(fx), linewidth=4)
plt.legend(["d=%i" % f1.order], loc="upper left")
plt.grid()
plt.show()
```

或

```python
plot_models(x, y, [f1], os.path.join("./images", "1400_01_01-1.png"))
```

效果图如下：

![12.png](https://upload-images.jianshu.io/upload_images/5637154-69360f83d3ce3a8a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

从图中我们可以看出，我们的一阶函数的误差很大，对于week4之后更是完全无法适用，所以我们需要尝试高级函数进行训练，

下面的代码它将训练模型和创建模型函数的过程融合到一起了，这样更为简洁，一共创建了2阶函数、3阶函数、10阶函数、100阶函数

```python
f2 = sp.poly1d(sp.polyfit(x, y, 2))
f3 = sp.poly1d(sp.polyfit(x, y, 3))
f10 = sp.poly1d(sp.polyfit(x, y, 10))
f100 = sp.poly1d(sp.polyfit(x, y, 100))
```

我们将它们进行可视化，我们可以同时在一个图上打印多个函数。

```python
plot_models(x, y, [f1], os.path.join("./images", "1400_01_02.png"))
plot_models(x, y, [f1, f2], os.path.join("./images", "1400_01_03.png"))
plot_models(x, y, [f1, f2, f3, f10, f100], os.path.join("./images", "1400_01_04.png"))
```

我们以图1400_01_04.png为例，它显示了所有的函数。

![13.png](https://upload-images.jianshu.io/upload_images/5637154-97e7ccbe6edd68ff.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 结论

从上面的图中，我们可以看出，越是高阶的函数与实际数据吻合的越是精准。

其实精准度（也就是误差值）是可以通过数值的方式表现的，我定义一个函数用于输出误差值：

```python
def error(f, x, y):
    return sp.sum((f(x) - y) ** 2)
```

然后调用这个函数

```python
print error(f1, x, y)
print error(f2, x, y)
print error(f3, x, y)
print error(f10, x, y)
print error(f100, x, y)
```

输出结果如下：

```python
317389767.34
179983507.878
139350144.032
121942326.364
109452402.923
```

从输出结果我们再次验证了图中的观点。

那么我们的训练函数是不是越复杂越好呢？答案自然不是，高阶函数会导致“过拟合”，低阶函数会导致“欠拟合”，使用这两种情况下的训练模型进行预测，其结果往往令人抓狂，和实际相差太大。

在上述的f1\f2\f3\f10\f100中，f1属于“欠拟合”的情况，f10和f100属于“过拟合”的情况，训练模型还不如f2和f3，但是f2和f3都不算最优的方案。

下面我们对数据分析，换一种方式进行训练。

## 数据训练2

我们换一个角度去看数据，似乎第3周和第4周之间的数据有一个拐点，我们可以以3.5周为一个界限，把数据分成两份，并训练出两个直线出来。

```python
inflection = int(3.5 * 7 * 24)
xa = x[:inflection]
ya = y[:inflection]
xb = x[inflection:]
yb = y[inflection:]
```

上面的代码中，我们将数据分割为两个数据集（xa,ya）和(xb,yb),然后我们生成两个模型函数并在原始数据图上进行可视化。

```python
fa = sp.poly1d(sp.polyfit(xa, ya, 1))
fb = sp.poly1d(sp.polyfit(xb, yb, 1))

plot_models(x, y, [fa, fb], os.path.join("./images", "1400_01_05.png"))
```

如下图所示：

![14.png](https://upload-images.jianshu.io/upload_images/5637154-7d5971bdaea1406f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们打印一下误差值

```python
print("Error inflection= %f" % error(fa, xa, ya))
print("Error inflection= %f" % error(fb, xb, yb))
```

结果如下：

```python
Error inflection= 110806407.089998
Error inflection= 22143941.107618
```

两条线的组合似乎比我们之前的任何模型都能更好的拟合，但是组合误差值仍然会比高阶多项式函数误差大，那么我们能否相信这个误差呢？

相比于高阶多项式，我们认为3.5周之后的直线表现更加符合未来数据的发展趋势，虽然100阶多项式非常努力的对给定的数据进行正确的建模，但是它们很明显无法推广到未来数据上，这叫做"过拟合"。

如何确定哪个训练模型更加符合未来数据呢？其实我们可以从先有数据中分出一部分来，剩下的数据用于训练，然后用分出来的数据测试我们训练出来的数据模型，最后确定最优的数据模型。

## 总结

我们始终要明白一件事，我们是机器学习的，数据的理解、分析才应该是我们最关心的事情，至于算法，这个不是我们关心的问题，各种插件已经帮我们实现了这些算法。而且实际情况下，不是越复杂的算法越能训练出好的数据模型。
