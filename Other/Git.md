# git_tutorial

Git常用的操作笔记，做一下备忘。

## 本地项目共享到远程仓库

假设现在本地已经有一个项目，我想共享到Github上，操作如下：

第一步：本机生成ssh密钥，本机安装git，新建Github账号，并在Github中添加本机的ssh密钥；

过程略。

第二步：新建远程仓库。在Github下新建仓库，如下图所示，这里建议不要勾选箭头所指的几个部分，以免后续需要进行合并操作，创建一个完全空白的的仓库。

![image](https://raw.githubusercontent.com/zhusheng/blog/master/git/01.png)

第三步：创建本地仓库。进入到项目根路径，执行`git init`指令，将当前目录变成一个git仓库，
新建`.gitignore`文件，编写不需要提交的文件规则，
新建`README.md`文件，编写项目开发笔记，
然后执行`git add .`,`git commit -m "initial commit"`，将项目代码提交到本地仓库，

第四步：关联远程仓库。`git remote add origin https://github.com/zhusheng/heroku_tutorial.git`,你们需要将这里的git仓库地址写成自己新建的仓库地址。

第五步：推送本地仓库代码到远程仓库。执行`git push -u origin master`将本地项目第一次推送到远程仓库。由于新建的GitHub仓库是空的，所以第一次推送master分支时需要加-u参数，以后再推送就不用加了。

执行效果如下图所示：

![image](https://raw.githubusercontent.com/zhusheng/blog/master/git/02.png)

第六步：以后本地项目做了更新，依次执行以下指令即可。`git add .`,`git commit -am "added xxx"`，`git push origin master`。

通过上述的步骤，我们将我们本地的项目共享到了GitHub云端，本地仓库的项目删除了或者丢了都不用担心。

## 多个remote repositories操作

如上创建的`heroku_tutorial`项目是一个Heroku项目，它使用的也是git作为版本管理的，类似的还有码云等等。那么我们如何将我们的本地Git仓库项目共享到多个远程仓库呢，其实这里，我们只要关联多个远程仓库即可。

- 关联远程仓库。默认的仓库名是origin,我这里默认的origin名称给了Github，如果我关联到码云，我可以取名gitee，这个名称我们可以自己取。当我使用Heroku创建项目的时候，它自动为我分配了项目的公网链接和仓库链接，它的默认名是heroku。

格式如下：

```bash
# git_url 为你的远程仓库的 url，可采用 http 协议或 ssh（git） 协议
git remote add origin <url>
git remote add gitee <url>
```

- 查看远程仓库列表

```bash
# 查看关联的远程仓库的名称
git remote
# 查看关联的远程仓库的详细信息
git remote -v
```

执行效果如下所示：
![image](https://raw.githubusercontent.com/zhusheng/blog/master/git/03.png)

- 推送到远程仓库。如果我们的本地项目有多个仓库，在我们提交项目的时候，我们就需要特别主意了，我们想把项目推送到那个远程仓库下。示例如下：

```bash
git add .
git commit -m "fix bugs"
git push gitee master
git push heroku master
git push origin master
```

- 删除远程库。我们关联了远程库，自然也是可以删除的。

```bash
git remote remove <name>
```
- 修改远程仓库关联。比如，之前你关联的远程仓库使用的协议是 http ，你想将关联的远程仓库的 url 改为 ssh 协议的。修改关联的远程仓库的方法，主要有三种。

第一种：使用 git remote set-url 命令，更新远程仓库的 url。
`git remote set-url origin <newurl>`

第二种：先删除之前关联的远程仓库，再来添加新的远程仓库关联。远程仓库的名称推荐使用默认的名称 origin 。

```bash
# 删除关联的远程仓库
git remote remove <name>
 
# 添加新的远程仓库关联
git remote add <name> <url>
```

第三种：直接修改项目目录下的 .git 目录中的 config 配置文件。config文件如下图所示，它的内容和我们通过`git remote -v`看到的结果是一样的。

![image](https://raw.githubusercontent.com/zhusheng/blog/master/git/04.png)
