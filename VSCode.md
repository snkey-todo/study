# VSCode

## 让VSCode支持Virtualenv

为了方便开发项目，我在本地部署了`virtualenv`和`virtualenvwrapper`,虚拟环境管理目录为：`~/.envs`，但是VSCode Python项目如何使用虚拟环境呢？

因为VSCode默认只加载了系统自带的python2环境，以及我为系统安装的python3环境。
我使用virtualenv可以创建基于python2和python3的隔离环境，我想使用创建的隔离环境作为项目，
但是VSCode在左下角没有加载出来，让我不知道怎么为项目设置我创建的隔离环境。

实现方式有2种，第二种推荐。

- 方式1:在VSCode Terminal中使用`workon`指令切换到我们想要的那个虚拟环境。然后执行pip操作、`python manage.py runserver`操作，都是在虚拟环境下执行的。
但是这种方式在编写代码的时候很不友好，没有代码提示，代码下面有绿色的波浪线。不推荐。

- 方式2:配置VSCode，添加虚拟环境目录，让VSCode去扫描我的虚拟环境管理目录，然后我为项目选择即可。操作如下：

设置加载虚拟环境目录，如下图所示：
![image](https://raw.githubusercontent.com/zhusheng/blog/master/vscode/01.png)

VSCode自动加载虚拟环境目录，如下图所示：
![image](https://raw.githubusercontent.com/zhusheng/blog/master/vscode/02.png)

使用我给系统安装的python3环境，因为那个环境下没有相关的库，所以代码提示不好：
![image](https://raw.githubusercontent.com/zhusheng/blog/master/vscode/03.png)

切换到我为该项目创建的虚拟环境，一切OK,如下图所示：
![image](https://raw.githubusercontent.com/zhusheng/blog/master/vscode/04.png)
