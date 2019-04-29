# Docker镜像

我们可以把常用的环境制作成Docker镜像， 然后基于镜像生成容器。比如我们可以把Hadoop做成一个镜像，然后我们可以基于这个镜像快速提供一个处于运行中的Hadoop环境。

Docker官方为我们提供了镜像仓库，Docker Hub，我们可以从其中搜索和下载我们需要的镜像。

## 下载镜像

从Docker Hub的Ubuntu仓库下载最新的镜像

```bash
docker pull ubuntu或docker pull ubuntu:latest
```

下载指定版本的镜像

```bash
docker pull ubuntu:14.04
```

说明：上面指令的实际全称是：`docker pull registry.hub.docker.com/ubuntu:14.04`,默认的注册服务器为`registry.hub.docker.com`.

## 显示镜像列表

```bash
docker images
```

说明：罗列本地主机上已有的镜像，ID是镜像的唯一标示号，同一个ID的镜像可以有多个TAG，如果ID一样说明镜像就是相同的。

## 获取镜像详细信息

```bash
docker inspect <ID>
```

## 运行镜像

使用镜像创建一个容器，并运行bash应用

```bash
docker run -it ubuntu /bin/bash
```

## 删除镜像

根据TAG或IMAGE ID进行删除操作，可以同时删除多个

```bash
docker rmi <IMAGE1 IMAGE2 ...>
```

根据TAG删除，先删除TAG，如果只有一个TAG，直接删除镜像本身

```bash
docker rmi sshd
```

根据id删除，直接删除镜像本身，无论有几个TAG。如果镜像有容器，需要先停止和删除相关的容器，然后才可以删除镜像。

```bash
docker rmi 433478589107 c84640d67d8a
```

我们也可以强制删除镜像，但不建议使用，可能会造成很多遗留问题。

```bash
docker rmi -f 433478589107
```

说明：如果镜像有容器的话，需要先删除容器，然后删除镜像。查看本机上的所有容器“docker ps -a”，删除容器“docker rm e81”。无论是删除容器还是删除镜像，在填写ID的时候我们可以只写前面的几个字符，只要保证是唯一的即可。

## 制作镜像

方式有三种：基于已有镜像的容器创建、基于本地模版导入、基于Dockerfile创建。最常见的是基于Dockerfile创建，其次是基于已有镜像的容器创建。

- 方式1:基于已有镜像的容器创建

根据已有的镜像创建一个容器；在容器中修改内容，如安装软件、新增文件等；保存容器为新的
镜像。指令格式如下：`docker commit [options] CONTAINER [REPOSITORY[:TAG]]`

```bash
options:
    -a, author，作者信息
    -m,	message，提交信息
    -p, pause， 提交时暂停容器运行
```

示例如下：

```bash
docker commit -m "Added json gem" -a "zhusheng" 0b2616b0e5a8 ouruser/sinatra:v2
```

说明：说明：`0b2616b0e5a8`为容器ID；`ouruser/sinatra:v2`为`REPOSITORY:TAG`

- 方式2:基于本地模版导入

模版下载地址，推荐使用[OpenVZ模版](http://openvz.org/Download/templates/precreated)

示例：下载ubuntu-14.04模版压缩包，进行导入操作

```bash
cat ubuntu-14.04-x86_64-minimal.tag.gz |docker import - ubuntu:14.04
```

- 方式3:使用Dockerfile制作镜像

Dockerfile是一个文本格式的配置文件，用户可以使用Dockerfile快速创建自定义的镜像。制作镜像的指令:`docker build -t <IMAGE NAME> .`

Dockerfile使用步骤：首先，在宿主机下新建一个文件下作为工作目录；然后，进入该工作目录，创建一个Dockerfile，我们在Dockerfile文件中编写我们生成镜像的代码逻辑。我们可以将过程中需要用到的软件放到工作目录下，在Dockerfile中使用ADD添加，也可以在工作目录下编写一些脚本，然后在Dockerfile中调用；最后，在工作目录下，执行创建镜像指令。

示例：

```bash
docker build -t zhusheng/mysql5.6:dockerfile .
```

注意：结尾有一个“.”

## 存出和载入镜像

- 存出镜像为本地文件

```bash
docker save -o ubuntu_14.04.tar ubuntu:14.04
```

示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/01.png)

- 导入本地文件为镜像

```bash
docker load < ubuntu_14.04.tar
或
docker load --input ubuntu_14.04.tar
```

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/02.png)

## 上传镜像到Docker Hub仓库

首先需要注册Docker账号;

其次是tag名称格式必须为：`<docker username>/imagename:tag`

示例:

```bash
# 添加新的标签
docker tag hello-world zhushengdocker/hello-world:1.0
# 上传镜像
docker push zhushengdocker/hello-world:1.0
```

示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/03.png)

我们登录Docker账号查看效果:

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/04.png)

## 阿里云镜像加速

[阿里云访问地址](https://cr.console.aliyun.com/cn-hangzhou/instances/mirrors)

进入阿里云容器Hub服务的控制台，并申请成为开发者。点击左侧的加速器帮助页面就会显示你的专属加速器地址。阿里为每个人都给了一个私有的个人加速器。我的个人加速器地址为：`https://j95dutr4.mirror.aliyuncs.com`

示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/05.png)