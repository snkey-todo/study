# Mac安装Jupyter

## 安装

方式1:安装Anaconda，然后勾选安装Jupyter

方式2:单独安装Jupyter

这里选择方式2，感觉Anaconda太耗资源，也比较卡顿。

- 创建隔离环境。因为Jupyter环境需要依赖Python以及一系列的库，这里为了方便进行Python环境管理，我创建一个隔离环境用于机器学习。

```bash
# 查看隔离环境列表
workon
# 创建隔离环境，名称为"machine_learning_default"
mkvirtualenv -p python3.6 machine_learning_default
```

运行示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/ai/01.png)

- 安装Jupyter。接下来，我子啊隔离环境下安装Jupyter，也就是说我的Jupyter只在该隔离环境下可用。

```bash
pip install jupyter
```

运行示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/ai/02.png)
![image](https://raw.githubusercontent.com/zhusheng/blog/master/ai/03.png)

- 启动Jupyter

```bash
python -m IPython notebook
```

运行示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/ai/04.png)
![image](https://raw.githubusercontent.com/zhusheng/blog/master/ai/05.png)