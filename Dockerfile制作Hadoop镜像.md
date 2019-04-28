# Dockerfile制作Hadoop镜像

## 制作ssh镜像

- 新建工作目录,编写Dockerfile文件如下：

```bash
# 选择一个已有的os镜像作为基础  
FROM centos:6

# 镜像的作者  
MAINTAINER zhusheng 1537017271@qq.com

# 安装openssh-server和sudo软件包，并且将sshd的UsePAM参数设置成no  
RUN yum install -y openssh-server sudo  
RUN sed -i 's/UsePAM yes/UsePAM no/g' /etc/ssh/sshd_config  
#安装openssh-clients
RUN yum  install -y openssh-clients

# 添加测试用户root，密码root，并且将此用户添加到sudoers里  
RUN echo "root:root" | chpasswd  
RUN echo "root   ALL=(ALL)       ALL" >> /etc/sudoers  
# 下面这两句比较特殊，在centos6上必须要有，否则创建出来的容器sshd不能登录  
RUN ssh-keygen -t dsa -f /etc/ssh/ssh_host_dsa_key  
RUN ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key  

# 启动sshd服务并且暴露22端口  
RUN mkdir /var/run/sshd  
EXPOSE 22  
CMD ["/usr/sbin/sshd", "-D"]
```

- 制作镜像

```bash
docker build -t zhushengdocker/centos6-ssh .
```

镜像列表如下图所示：
![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/12.png)

## 制作jdk镜像

- 新建工作目录，将jdk安装包拷贝到里面，编写Dockerfile文件如下：

```bash
# 继承上面的ssh镜像
FROM zhushengdocker/centos6-ssh 

# 安装jdk
ADD jdk-7u80-linux-x64.tar /usr/local/
RUN mv /usr/local/jdk1.7.0_80 /usr/local/jdk1.7
ENV JAVA_HOME /usr/local/jdk1.7
ENV PATH $JAVA_HOME/bin:$PATH
```

- 制作镜像

```bash
docker build -t zhushengdocker/centos6-jdk .
```

镜像列表如下图所示：
![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/13.png)

## 制作hadoop镜像

- 新建工作目录，拷贝hadoop安装包到该目录，编写Dockerfile文件如下：

```bash
# 继承创建的jdk镜像
FROM zhushengdocker/centos6-jdk

# 安装Hadoop
ADD hadoop-2.7.3.tar.gz /usr/local
RUN mv /usr/local/hadoop-2.7.3 /usr/local/hadoop

# 配置环境变量
ENV HADOOP_HOME /usr/local/hadoop
ENV PATH $HADOOP_HOME/bin:$PATH
```

- 制作镜像

```bash
docker build -t zhushengdocker/centos6-hadoop .
```

镜像列表如下图所示：
![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/14.png)
