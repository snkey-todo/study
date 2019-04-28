# Docker端口映射和容器互联

Docker目前提供了映射容器端口到宿主机、以及容器互联机制来为容器提供网络服务。

方式：

1. 端口映射机制将容器内的应用服务提供给外部网络
2. 通过容器互联系统让多个容器之间进行快捷的网络通信

## 端口映射

在启动容器的时候，如果不指定对应参数，在容器外部是无法通过网络来访问容器内的应用和服务的。
我们可以通过-P来实现，-P随机端口，-p指定端口。

```bash
docker run -d -P training/webapp python app.py
```

（1）随机端口
该指令创建一个training/webapp镜像的容器，并运行app.py脚本

示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/32.png)

我们查看容器，本机(linux)的32768端口映射到了容器的5000端口，访问32768端口即可访问容器的应用。

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/33.png)

```bash
#我们查看应用信息
docker logs -f wonderful_hoover
```

示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/34.png)

我的Mac和linux是网络互通的，我在Mac下访问linux的32768端口来访问容器的应用。示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/35.png)

（2）指定端口

使用-p指定映射端口

```bash
docker run -d -p 192.168.1.241:7777:5000 training/webapp python app.py
```

示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/36.png)

浏览器访问,示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/37.png)

其它指令

```bash
docker run -d -p 5000:5000 -p 3000:80 training/webapp python app.py
docker run -d -p 192.168.1.241:5000:5000 -p 3000:80 training/webapp python app.py
```

查看容器的端口映射情况，示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/38.png)

## 容器互联

link语法：—link name:alias,指定要链接的容器名称，并为这个链接取一个名称

创建一个db容器

```bash
docker run -d --name postgres_db training/postgres
```

创建一个web容器，并link到postgres_db容器

```bash
docker run -d -P --name web --link db:postgres_db training/webapp python app.py
```

示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/39.png)