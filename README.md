<h1 align="center"><a href="https://github.com/SnailMann" target="_blank">CAB Tool</a></h1>

> `CAB Tool`是一款针对CSDN进行博客备份的小工具
> 
> 可以将用户在CSDN博客中的markdown文章备份到本地，备份可以有html及markdown版本

<p align="center">
<a href="#"><img alt="python" src="https://img.shields.io/badge/python-3.7-blue.svg"/></a>
<a href="https://github.com/SnailMann/CAB-Tool/releases"><img alt="GitHub release" src="https://img.shields.io/github/release/SnailMann/CAB-Tool.svg"></a>
<a href="https://github.com/SnailMann/CAB-Tool/commits"><img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/SnailMann/CAB-Tool.svg?label=update"></a>

</p>

## 介绍

`CAB Tool`  就是**csdn-article-backp-tool**，只是我有点懒，不想打这么长


- 需要登录账户密码
- 目前不支持备份图片（`下次有空再实现`）
- 目前不支持备份私密文章，只能备份自己的公开文章
- `CAB Tool` 直接爬取的是csdn markdown编辑器的文本，备份的文本与编辑器上无异



## 引文

因为本撸发现在CSDN写的笔记好像也堆积了八九十篇啦。曾经没有数据备份意识的我本来想着从GayHub找找现成的Tool, 也不知道为什么GayHub上的不是过时了，就是效果不佳。可能大牛们嫌太简单，懒得放出来。于是，只能求人不如求己，没有玩过python的我，风风火火，简单地学习了下语法和爬虫就上马了。所以有Bug是正常嘛，见怪勿怪喔！



## 使用

### 方式一

![效果图](./asset/img/cab-tool.gif)

**第一步**

- 把项目克隆本地`git clone git@github.com:SnailMann/CAB-Tool.git`
- 确保本地有python3的环境, 并且可以使用pip安装依赖
- 进入项目目录,命令行输入`pip install -r requirements.txt`，使用pip安装py项目的必要依赖

**第二步**

- 打开`setting.yaml`配置文件
- 按照yaml规范填写CSDN的账号密码
- 安装yaml规范在download-path填写本地导出地址,不填默认为`D:\csdn-blog-backup`

**第三步**

- 确认配置无误后
- 项目路径打开命令行，输入`py main.py`


### 方式二

如果你是没有任何python基础的同学，或是懒得安装py环境。没有关系，这里也是支持小白式运行的

- 点击[cab-tool releases](https://github.com/SnailMann/CAB-Tool/releases)，下载`cabtool.exe`的最新版本
- 双击运行`cabtool.exe`就好啦


## 博客




**本撸的博客是[https://blog.csdn.net/SnailMann](https://blog.csdn.net/SnailMann)，如果对你有帮助，记得关个注，点个赞哟？！**

