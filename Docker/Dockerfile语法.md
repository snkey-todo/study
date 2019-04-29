# Dockerfile语法

## Dockerfile使用步骤

（1）首先，在宿主机下新建一个文件下作为工作目录；

（2）进入该工作目录，创建一个Dockerfile，我们在Dockerfile文件中编写我们生成镜像的代码逻辑。
说明：我们可以将过程中需要用到的软件放到工作目录下，在Dockerfile中使用ADD添加，也可以在工作目录下编写一些脚本，然后在Dockerfile中调用；

（3）在工作目录下，执行创建镜像指令。指令示例如下：

```bash
docker build -t zhusheng/mysql5.6:dockerfile .
```

## Dockerfile基本语法

1、FROM-指定继承镜像

例如：

```bash
FROM ubuntu 
FROM ubuntu:14.04
```

2、MAINTAINER-维护者信息

例如：

```bash
MAINTAINER zhusheng 1537017271@qq.com
```

3、RUN-执行指令

例如：

```bash
RUN  apt-get update
RUN mkdir  /data
RUN  [“/bin/bash”, “-c”, “echo hello world”]
```

4、CMD-容器自启动时执行指令

例如：

```bash
CMD ["/run.sh"]
```

备注：每个Dockerfile只能有一条CMD指令

5、EXPOSE -暴露端口

例如：

```bash
EXPOSE  80
```

备注：可以同时暴露多个端口：EXPOSE  80 22 8443 

6、ENV-指定环境变量，会被后续的RUN指令时使用

例如：

```bash
ENV PG_MAJOR 9.3
ENV PATH /usr/local/postgres-$PG_MAJOR/bin:$PATH
```

7、ADD-复制

比如我们安装jdk的时候，把jdk安装包拷贝到工作目录，在Dockerfile中执行，例如：

```bash
ADD  jdk-7u80-linux-x64.tar
```

8、COPY-复制

格式：`COPY <src> <dest>`,复制指定的src到容器中的desc，目标路径不存在时自动创建

9、ENTRYPOINT

格式

```bash
ENTRYPOINT  [“exec”, “param1”, “param2”]
ENTRYPOINT command param1 param2  
```

说明：每个Dockerfile只能有一个ENTRYPOINT

10、VOLUME-挂载容器

例如：

```bash
VOLUME [“/data”]
```

11、USER-指定运行容器时的用户名或UID

```bash
USER daemon
```

12、WORKDIR-指定配置工作目录

格式：`WORKDIR <path>`为后续的CMD、RUN、ENTRYPOINT指定配置工作目录

13、ONBUILD-配置当前镜像为其它镜像的基础镜像

略