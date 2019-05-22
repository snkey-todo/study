# Linux指令

## 文件操作

- 新建文件夹

```bash
mkdir -p /usr/local/<dirA>/<dirB>
```

说明：递归创建文件夹，创建文件夹A以及文件夹下的文件夹B。

## 数据迁移

- 服务器到本地

```bash
scp -r root@114.115.179.78: /usr/local/hiot/uploadfiles /Users/zhusheng/download/hiot
```

说明：-r表示递归。

## 端口和进程

- 查看端口占用

```bash
lsof -i:6379
```