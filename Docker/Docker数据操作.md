# Docker数据操作

如何在Docker宿主机及容器之间进行数据传输。方式1:使用`cp`指令进行数据拷贝；方式2:使用数据卷。

## 文件拷贝

语法：

```bash
docker cp <src> <containerName>:<desc>
docker cp <containerName>:<desc> <src>
```

无论是哪一种操作都需要退出容器进行操作。

示例1:

```bash
# 宿主机到容器
docker cp jdk-7u80-linux-x64.tar hadoop:/home
# 容器到宿主机
docker cp hadoop:/home/jdk-7u80-linux-x64.tar ~/Downloads
```

示例2:

```bash
# 启动容器
docker run --name ubuntu111 -itd ubuntu:14.04 /bin/bash
# 宿主机到容器，拷贝文件,根据容器名称
docker cp run.sh ubuntu111:/home
# 宿主机到容器，拷贝文件,根据容器ID
docker cp authorized_keys 6a6a:/home
# 容器到宿主机
docker cp ubuntu111:/home/run.sh ~/
```

## 数据卷

[参考文档](https://www.cnblogs.com/sammyliu/p/5932996.html)

### 简介

如果用户需要在容器之间共享一些持续更新的数据，最简单的方式是使用数据卷容器。数据卷容器其实就是一个普通的容器，专门用于提供数据卷拱其它容器挂载使用。

数据卷的作用：

1. 使用数据卷容器可以让用户在容器之间自由地升级和移动数据卷。
2. 使用数据卷容器对其中的数据卷进行备份、恢复，实现数据迁移。

### 创建数据卷容器、挂载及测试

1、创建一个数据卷容器，名称为dbcontainer，并在其中创建一个数据卷挂载到/dbdata目录，那么，/dbdata目录就是一个数据卷。

```bash
docker run -it -v /dbdata --name dbcontainer ubuntu
```

示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/15.png)

2、查看/dbdata目录

```bash
docker exec -it dd744b6466bf /bin/bash
```

示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/16.png)

3、创建两个其它容器，使用—volumes-from来挂载dbcontainer数据卷容器中的数据卷

```bash
docker run -it --volumes-from dbcontainer --name db1 ubuntu
docker run -it --volumes-from dbcontainer --name db2 ubuntu
```

示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/17.png)

此时，db1容器和db2容器都挂载到dbcontainer容器，具体的数据卷为/dbdata。三个容器任何一方在该目录写入，其它容器都可以看到。

4、测试数据共享

在dbcontainer容器修改数据。

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/18.png)

在db1查看数据

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/19.png)

5、可以多次使用—volumes-from从不同的容器挂载数据卷，也可以从已经挂载数据卷的容器挂载数据卷，示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/20.png)

## 查看数据卷列表

```bash
docker volume ls
```

## 删除数据卷

```bash
# 删除容器的同时删除卷
docker rm -vf web5
```

使用 docker run -v 启动的容器被删除以后，在主机上会遗留下来孤单的卷。可以使用下面的简单方法来做清理

```bash
docker volume ls -qf dangling=true
docker volume rm $(docker volume ls -qf dangling=true)
docker volume ls
```

## 数据卷备份和恢复

1、备份

```bash
docker run --volumes-from dbcontainer -v $(pwd):/backup --name worker ubuntu tar cvf /backup/backup.tar /dbdata
```

上面的指令解析：

- --volumes-from dbcontainer  挂载到数据卷容器；
- -v $(pwd):/backup   挂载本地的当前目录到worker容器的/backup目录，所以在本地的当前目录也有一份备份数据；
- --name worker ubuntu 创建容器worker；
- tar cvf /backup/backup.tar /dbdata将数据卷/dbdata备份为worker容器内的/backup/backup.tar。

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/21.png)

2、恢复

先创建一个带有数据卷的容器

```bash
docker run -v /dbdata --name container2 ubuntu /bin/bash
```

然后创建一个容器，挂载数据卷容器；使用untar解压备份文件到挂载的数据卷中

```bash
docker run --volumes-from container2 -v $(pwd):/backup busybox tar xvf /backup/backup.tar
```

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/22.png)

## 新版功能：docker volume

Docker 新版本中引入了 docker volume 命令来管理 Docker volume。

（1）新建数据卷

```bash
docker volume create --name voll
docker volume inspect voll
```

示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/23.png)

（2）挂在数据卷

```bash
docker run -d -P --name web4 -v vol1:/volume training/webapp python app.py
```

说明：将 voll 对应的主机上的目录挂载给容器内的 /volume 目录。