# Docker容器

容器是镜像的实例，是一个独立的环境。

## 运行容器

- 方式1
  
使用docker create容器，容器默认是停止状态的，需要使用docker start来启动容器。

```bash
docker create -ti ubuntu:14.04
docker start c498a45c62a9
```

- 方式2
  
新建并启动-docker run,docker run等价与docker create +docker start

```bash
# 示例1
docker run ubuntu:14.04 /bin/echo "hello world"
# 示例2
docker run -it ubuntu:14.04 /bin/bash
# 示例3:指定容器名称
docker run -it --name ubuntu_test1 ubuntu /bin/bash
```

```bash
Options:
    -t, 让docker分配一个伪终端并绑定到容器的标准输入上
    -i, 让容器的标准输入保持打开
    -d, 表示在后台运行
```

补充示例：下面的指令会在后台启动一个容器，而且每隔1秒输出一条语句

```bash
docker run -d ubuntu:14.04 /bin/sh -c "while true; do echo hello zhusheng; sleep 1; done”
```

## 查看容器日志

```bash
Docker logs  <container id>
```

## 停止容器

```bash
# 停止容器
docker stop <docker id>
# 强制杀死容器
docker kill <docker id>
```

## 查看容器

```bash
# 查看所有的容器，包含Exited、Up 状态的所有容器
docker ps -a
# 查看运行的容器，Up 状态
docker ps
# 查看容器id
docker ps -a -q
docker ps  -q
```

## 启动容器

```bash
# 启动
docker start <docker id>
# 重启
docker restart <docker id>
```

## 进入容器

带有-d参数启动的容器会在后台运行，用户无法看到容器中的信息，如下所示:

```bash
# 启动容器在后台运行
docker run -d ubuntu:14.04 /bin/bash
```

如果现在我们需要进入容器，有几种方式，如下所示：
（1）attach,docker自带，但是窗口会自动同步
（2）exec, docker自带，更加高级
（3）nsenter工具，包含于util-linux包2.23之后的版本

- 使用attach进入容器

```bash
docker attach <container id> or <container name>
```

- 使用exec进入容器—推荐

```bash
docker exec -it dd744b6466bf /bin/bash
```

- 使用nsenter

安装nsenter

```bash
cd /tmp;curl https://www.kernel.org/pub/linux/utils/util-linux/v2.24/util-linux-2.24.tar.gz | tar -zxvf-; cd util-linux-2.24;

./configure --without-ncurses
```

如果提示缺少gcc、cc、cl.exe，执行`yum install -y gcc`后重新执行检查`make nsenter && cp nsenter /usr/local/bin`

使用nsenter

每一个容器都有.State.Pid，所以这个命令除了容器的id需要我们根据docker ps -a去查找，其他的全部为固定的格式。

```bash
# 获取.State.Pid
docker inspect -f {{.State.Pid}} <container id> or <container name>
# 根据.State.Pid进入容器
nsenter --target <PID> --mount --uts --ipc --net –pid
```

示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/06.png)

参数说明：

- mount参数是进去到mount namespace中
- uts参数是进入到uts namespace中
- ipc参数是进入到System V IPC namaspace中
- net参数是进入到network namespace中
- pid参数是进入到pid namespace中
- user参数是进入到user namespace中

## 删除容器

```bash
# 删除
docker rm d2016d5fe1b3
# 强制删除
docker rm -f d2016d5fe1b3
#停用全部运行中的容器
docker stop $(docker ps -q)
#删除全部容器
docker rm $(docker ps -aq)
#一条命令实现停用并删除容器
docker stop $(docker ps -q) & docker rm $(docker ps -aq)
```

## Docker备份

### 本地备份

（1）导出容器
不管这个容器是什么状态，使用docker export导出成为一个压缩文件

```bash
docker export ce5 > test_for_run.tar
```

（2）导入容器
导入的容器会成为一个镜像

```bash
cat test_for_run.tar | docker import - test/ubuntu:v1.0
```

示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/07.png)

### Docker Hub备份

（1）备份成镜像

```bash
docker commit -p huatec01 zhushengdocker/hadoop3node:huatec01
docker commit -p huatec02 zhushengdocker/hadoop3node:huatec02
docker commit -p huatec03 zhushengdocker/hadoop3node:huatec03
```

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/08.png)
![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/09.png)

（2）登录docker账号

```bash
docker login
#输入用户名和密码
```

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/10.png)

（3）上传镜像

```bash
docker push zhushengdocker/hadoop3node:huatec01
```

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/11.png)

（4）恢复镜像

```bash
docker pull zhushengdocker/hadoop3node:huatec01
```