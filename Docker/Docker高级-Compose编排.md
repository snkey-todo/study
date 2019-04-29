# Docker Compose

Compose是Docker的服务编排⼯具，主要⽤来构建基于Docker的复杂应⽤，Compose 通过⼀个配置⽂件来管理多个Docker容器，⾮常适合组合使⽤多个容器进⾏开发的场景。Compose使得Docker应⽤管理更为⽅便快捷。

说明：Compose是Fig的升级版，Fig已经不再维护。Compose向下兼容Fig，所有
fig.yml只需要更名为docker-compose.yml即可被Compose使⽤。

[Compose官方文档](https://docs.docker.com/compose/)

## 项目结构

我们可以为一个已经存在的项目使用Compose来进行编排，一个Compose项目包含以下内容：

- 项目代码, 可以是一个文件或者一个文件夹，是项目的源代码。
- Dockerfile，可以参考[Dockerfile语法](https://github.com/zhusheng/notes/blob/master/Dockerfile%E8%AF%AD%E6%B3%95.md)。
- dokcer-compose.yml, 定义各个服务[或容器]之间的编排规则。
- requirement.txt，需要安装的软件，供Dockerfile文件使用，`RUN pip install -r requirements.txt`。

## 版本说明

Compose版本示意图如下：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/40.png)

我的版本是1.23.2，所以我在编写`docker-compose.yml`文件的时候，第一行写的是`version: “3”`

## 入门案例：composetest

[官方示例链接](https://docs.docker.com/compose/gettingstarted/)

编写完成后的项目目录结构如下所示：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/docker/41.png)

主要有requirement.txt、Dockerfile、docker-compose.yml三个核心文件。其中app.py是我们需要在项目中执行的代码文件。

- 编写app.py

```bash
import time
import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello Compose! I have been seen {} times.\n'.format(count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
```

- Dockerfile

```bash
FROM python:3.7-alpine
# 把当前目录拷贝到镜像的 "/code"下
ADD . /code
# 设置工作目录
WORKDIR /code
# 安装软件
RUN pip install -r requirements.txt
# 启动容器的时候执行"python app.py"
CMD [ "python", "app.py"]
```

- Docker-compose.yml

```bash
# 根据docker的版本来写，我的docker版本是1.18, 对应的是version 3
version: '3'
services: 
  web:
    build: .
    ports: 
      - "5000:5000"
    # 将当前目录挂载到容器的“/code”目录，可以实现本地修改代码，容器自动刷新，而不需要重新创建容器
    volumes: 
      - .:/code
  redis:
    image: "redis:alpine"
```

在上面的文件中，我们包含了2个服务，1个web服务，1个redis服务，我们的app.py文件运行在web服务中，并作端口映射；我们在代码中import redis，使用了redis的方法。

- 启动

```bash
# 启动
docker-compose up
# 在后台启动
docker-compose up
```

- 拓展：相关指令

```bash
# 查看服务
docker-compose ps
# 查看某个服务的环境信息
docker-compose run web env
docker-compose run redis env
# 停止服务
docker-compose stop
# 移除所有容器及挂载的数据卷
docker-compose down --volumes
```

## 案例：Compose and Django

[官方示例链接](https://docs.docker.com/compose/django/)