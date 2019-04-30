# Python for Virtualenv

## virtualenv + virtualenvwrapper打造隔离环境

### virtualenv

virtualenv 是一个创建隔绝的Python环境的工具。virtualenv创建一个包含所有必要的可执行文件的文件夹，用来使用Python工程所需的包。

- 安装

指令：

```bash
pip install virtualenv
```

效果如下图所示：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/python/01.png)

查看版本信息:

![image](https://raw.githubusercontent.com/zhusheng/blog/master/python/02.png)

### virtualenvwrapper

鉴于virtualenv不便于对虚拟环境集中管理，所以推荐直接使用virtualenvwrapper。 virtualenvwrapper提供了一系列命令使得和虚拟环境工作变得便利。它把你所有的虚拟环境都放在一个地方。

- 安装

指令：

```bash
pip install virtualenvwrapper
```

效果如下图所示：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/python/03.png)

配置环境变量如下所示:

![image](https://raw.githubusercontent.com/zhusheng/blog/master/python/04.png)

- virtualenvwrapper使用

virtualenv可以基于电脑现有的python环境创建克隆的隔离环境，我的系统安装了python2.7和Python 3.6.5，所以我可以创建基于python2.7或者Python 3.6.5的隔离环境，
系统自带的python为2.7，Python 3.6.5为后来安装的。如果在使用mkvirtualenv指令的时候不指定版本，默认是python2.7环境。以下是一些常用的指令：

（1）创建虚拟环境

```bash
mkvirtualenv test_env
mkvirtualenv -p python3.6 test_env2
```

（2）查看虚拟环境

```bash
workon
```

（3）删除虚拟环境

```bash
rmvirtualenv test_env
```

（4）切换虚拟环境

```bash
workon hello_virtualenv
```

（5）退出虚拟环境

```bash
deactivate
```