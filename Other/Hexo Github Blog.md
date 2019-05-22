# Hexo + Github搭建博客

## 创建仓库

在Github上新建一个仓库，仓库名格式为"用户名.github.io"，而且用户名必须为Github账户的名称，由此可见，每一个人只能创建一个这样的仓库。

有几点需要注意：

1. 注册的邮箱一定要验证，否则不会成功；
2. 仓库名字必须是：username.github.io，其中username是你的用户名；
3. 仓库创建成功不会立即生效，需要过一段时间，大概10-30分钟;

然后我创建好了我的仓库为zhusheng.github.io，如下图所示：

![hexo01](https://raw.githubusercontent.com/zhusheng/blog/master/hexo/01.png)

创建成功后，默认会在你这个仓库里生成一些示例页面，网站的所有代码都存放这个仓库里。

以后我们可以通过`https://zhusheng.github.io/`来访问我们的博客。

## 绑定自己的域名

### 阿里云域名配置和解析

如果我们有自己的域名的话，可以将我们的博客绑定到自己的域名。绑定域名分2种情况：带www和不带www的。

域名配置有很多种方式，最常见有2种方式，`CNAME`和`A记录`。我们在阿里云购买域名之后进行域名解析。如下图所示：

![hexo02](https://raw.githubusercontent.com/zhusheng/blog/master/hexo/02.png)
![hexo03](https://raw.githubusercontent.com/zhusheng/blog/master/hexo/03.png)

`CNAME`填写域名，`A记录`填写IP。由于不带www方式只能采用`A记录`，所以必须先ping一下你的`zhusheng.github.io`的IP，然后到你的域名DNS设置页，将`A记录`指向你ping出来的IP，将`CNAME`指向你的`zhusheng.github.io`，这样可以保证无论是否添加www都可以访问。

![hexo04](https://raw.githubusercontent.com/zhusheng/blog/master/hexo/04.png)

但是我们发现我们的`zhusheng.github.io`域名所对应的ip是会经常变动的，所以我们选择`CANME`方式进行域名配置，如下图所示：

![hexo05](https://raw.githubusercontent.com/zhusheng/blog/master/hexo/05.png)

在填写信息时，我们需要填写TTL，也就是DNS缓存时间，我们可以参考下图进行设置

![hexo06](https://raw.githubusercontent.com/zhusheng/blog/master/hexo/06.png)

解析完成之后如下所示：

![hexo07](https://raw.githubusercontent.com/zhusheng/blog/master/hexo/07.png)

### 绑定域名

我们将`zhusheng.github.io`项目clone到本地，在项目的根目录下新建文件`CANME`,在文件中填写我们的域名`snkey.cc`。

- 如果你填写的是没有www的，比如 mygit.me，那么无论是访问 `http://www.mygit.me` 还是 `http://mygit.me` ，都会自动跳转到 `http://mygit.me`
- 如果你填写的是带www的，比如 www.mygit.me ，那么无论是访问 `http://www.mygit.me` 还是 `http://mygit.me` ，都会自动跳转到 `http://www.mygit.me`

## 使用Hexo

Hexo是一个简单、快速、强大的基于 Github Pages 的博客发布工具，支持Markdown格式，有众多优秀插件和主题。

- 官网: `http://hexo.io`
- Github: `https://github.com/hexojs/hexo`

由于github pages存放的都是静态文件，博客存放的不只是文章内容，还有文章列表、分类、标签、翻页等动态内容，假如每次写完一篇文章都要手动更新博文目录和相关链接信息，相信谁都会疯掉，所以hexo所做的就是将这些md文件都放在本地，每次写完文章后调用写好的命令来批量完成相关页面的生成，然后再将有改动的页面提交到github。

### 安装hexo

安装指令如下：

```bash
npm install -g hexo
```

### 初始化

新建一个名为hexo的文件夹（名字可以随便取），由于这个文件夹将来就作为你存放代码的地方，所以最好不要随便放，我的路径`~/Databank/hexo`，然后执行初始化指令

```bash
cd /f/Workspaces/hexo/
hexo init
```

hexo会自动下载一些文件到这个目录，包括node_modules，目录结构如下图：

![hexo08](https://raw.githubusercontent.com/zhusheng/blog/master/hexo/08.png)

```bash
hexo g # 生成
```

执行以上命令之后，hexo就会在public文件夹生成相关html文件，这些文件将来都是要提交到github去的。

![hexo09](https://raw.githubusercontent.com/zhusheng/blog/master/hexo/09.png)

```bash
hexo s # 启动服务
```

执行以上命令之后，会在本地启动hexo服务，我们通过`http://localhost:4000/`可以查看预览效果。

### 修改主题

我们下载主题，然后将主题解压后放到`hexo/themes/`下，然后修改`_config.yml`文件，设置`theme: hexo-theme-yilia-master`属性即可。然后执行`hexo g`重新生成一下。

### 常用指令

```bash
hexo new "postName" #新建文章
hexo new page "pageName" #新建页面
hexo generate #生成静态页面至public目录
hexo server #开启预览访问端口（默认端口4000，'ctrl + c'关闭server）
hexo deploy #部署到GitHub
hexo help  # 查看帮助
hexo version  #查看Hexo的版本
```

指令缩写

```bash
hexo n == hexo new
hexo g == hexo generate
hexo s == hexo server
hexo d == hexo deploy
```

组合指令

```bash
hexo s -g #生成并本地预览
hexo d -g #生成并上传
```

### 配置文件_config.yml

这里面都是一些全局配置，每个参数的意思都比较简单明了，需要特别注意的地方是，冒号后面必须有一个空格，否则可能会出问题。

[参考文章](https://www.cnblogs.com/liuxianan/p/build-blog-website-by-hexo-github.html)
