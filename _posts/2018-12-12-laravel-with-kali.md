---
title: Laravel with kali
tags: [tutorial]
color: success
style: fill
description: Laravel的坑
---

### 记录一下在Kali下如可搭建Laravel环境
---  

&emsp;&emsp;我的天呐,**Kali**安装个**Laravel**是真的难,不是权限问题就是依赖问题,统一记录一下吧.
&emsp;&emsp;首先要新建一个普通用户  
```shell
useradd -m dyf -s zsh -d /home/dyf 
passwd  dyf                                             //然后就输入密码
usermod                                                 //可修改用户状态
userdel                                                 //可删除用户
visudoers 将用户加入sudoers
```
&emsp;&emsp;关于**useradd**的参数用法:
```shell
-c comment 指定一段注释性描述。
-d 目录 指定用户主目录，如果此目录不存在，则同时使用-m选项，可以创建主目录。
-g 用户组 指定用户所属的用户组。
-G 用户组，用户组 指定用户所属的附加组。
-s Shell文件 指定用户的登录Shell。
-u 用户号 指定用户的用户号，如果同时有-o选项，则可以重复使用其他用户的标识号。
```
&emsp;&emsp;接着是最恶心的部分,安装**php**依赖:
```shell
sudo apt-get install -y libapache2-mod-php7.0
sudo apt-get install -y php7.0-mysql
sudo apt-get install php7.2-zip
sudo apt-get install php-common php-mbstring php-xml php-zip php-json php-mcrypt
sudo apt-get install php-mbstring
sudo apt install libapache2-mod-php
```
&emsp;&emsp;弄完了这么一堆恶心的东西之后,心态差了许多.  
&emsp;&emsp;现在开始我们已经可以真正开始了.第一步是安装**php**的包管理**composer**:
```shell
sudo apt update
suod apt upgrade
sudo apt install -y composer
composer                       //此时有参数选项则安装成功
sudo chmod 777 /home/dyf                                  //增加写入权限
composer config -g repo.packagist composer https://packagist.laravel-china.org   //更换composer源
```
&emsp;&emsp;此时**composer**已经安装完毕,下面开始正式安装Laravel:
```shell
composer global require "laravel/installer"
PATH=$PATH:/home/dyf/.config/composer/vendor/bin        //修改为全局变量
```
到这里已经差多完了,缺啥东西自己去**stackoverflow**上面查吧,心力憔悴.  
然后嘞,你需要去修改`/etc/apache2/sites-aviliable/000-default.conf`把默认路径改一下.
```shell
composer create-project --prefer-dist laravel/laravel
chmod -R 777 public storage bootstrap                             //给权限
vim /etc/apache2/apache2.conf                  //找到'/var/www'将AllowOverride改为all
sudo a2enmod rewrite                           //开启重写模式
composer install
composer update
```
&emsp;&emsp;接着为新项目建立一个新的mysql账户,一定要安装php7.x-mysqli的包,否则 mysqliconnect() 将无法使用.安装php-curl

&emsp;&emsp;开始干活吧.
###### ps:我不小心重装了系统，结果又蹦了，首先是apache，接着是php版本冲突要用a2enmod php7.\*修改。

##### 我又双重装了系统，这次提供的node版本是11.0,根本不支持之前的版本，踏马只能用 **npm rebuild node-sass --force** 回滚原先的版本。
