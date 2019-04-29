# Docker仓库

## Docker Hub账号

```bash
Username：zhushengdocker
Password：xxxxxxx
```

备注：Docker Hub逐渐迁移到Docker Store

阿里Docker Hub加速器可以提高国内对Docker的访问速度，我在阿里Docker Hub上注册了一个账号，系统会为每个人分配一个加速器地址，我的加速器地址为：`https://j95dutr4.mirror.aliyuncs.com`。我将其添加到我的Docker配置里面，如下图所示：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/24.png)

## Docker Hub仓库基本操作

Ubuntu是一个仓库，它的各个版本分支对应具体的镜像，也就是说镜像是存储在仓库里的。

```bash
# 搜索仓库
docker search Ubuntu
# 从仓库下载镜像
docker pull ubuntu:14.04
```

## 私有仓库的创建和使用

1、在192.168.1.241机器上下载registry镜像，并启动一个仓库容器。安装完docker之后，可以通过官方提供的registry镜像简单搭建一个本地私有仓库，指令自动下载并启动一个registry容器，创建本地的私有仓库服务。默认仓库创建在容器的/tmp/registry目录下，也可以通过-v指定位置。监听端口为5000。示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/25.png)

2、在Mac上或其它机器安装有docker的机器上上传镜像到仓库，在Mac上下载一个busybox镜像，然后改名为192.168.1.241:5000/busybox，我们注意到前面的名称为仓库的ip:5000。示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/26.png)

上传镜像

```bash
docker push 192.168.1.241:5000/busybox
```

示意图如下：
![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/27.png)

出错了是因为docker 1.3.x之后，与docker registry的交互默认采用的是https，我们修改Mac的docker配置文件daemon.json，在其中增加如下内容："insecure-registries": ["<ip>:5000"] ，我们可以同时增加多个ip。示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/28.png)

重新执行上传，上传成功！示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/29.png)

3、查看仓库镜像列表

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/30.png)

4、下载仓库镜像

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/31.png)