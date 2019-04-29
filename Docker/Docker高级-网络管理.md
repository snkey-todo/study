# Docker网络管理

[参考文章](http://blog.csdn.net/moonhillcity/article/details/52179249)

## docker四种网络模式

docker支持四种网络模式，可以在启动容器的时候使用—net参数选项指定，docker默认使用的网卡为docker0。

（1）host，--net=host，如果指定此模式，容器将不会获得一个独立的network namespace，而是和宿主机共用一个。容器将不会虚拟出自己的网卡，IP等，而是使用宿主机的IP和端口，也就是说如果容器是个web，那直接访问宿主机:端口，不需要做NAT转换，跟在宿主机跑web一样。容器中除了网络，其他都还是隔离的。

（2）container，--net=container:NAME_or_ID，与指定的容器共同使用网络，也没有网卡，IP等，两个容器除了网络，其他都还是隔离的。

（3）none ，--net=none，获得独立的network namespace，但是，并不为容器进行任何网络配置，需要我们自己手动配置。

（4）bridge，--net=bridge，默认docker与容器使用的网络，一般分配IP是172.17.0.0/16网段，宿主机为172.17.0.1,容器根据先后启动顺序依次分配172.17.0.2、172.17.0.3，一直到172.17.0.16。

要想改为其他网段，可以直接修改网桥IP地址，例如：

```bash
$ sudo ifconfig docker0 192.168.10.1 netmask 255.255.255.0
```

## 分析容器默认网络配置过程

先创建一个docker0的网桥，使用Veth pair创建一对虚拟网卡，一端放到新创建的容器中，并重命名eth0，另一端放到宿主机中。虚拟网卡以veth+随机7个字符串名字命名，并将这个网络设备加入到docker0网桥中，网桥自动为容器分配一个IP，并设置docker0的IP为容器默认网关。同时在iptables添加SNAT转换网桥段IP，以便容器访问外网。

Veth par是用于不同network namespace间进行通信的方式，而network namespace是实现隔离网络。
