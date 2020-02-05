---
title: markdown-tutorial
tags: [markdown, thinking]
color: secondary
style: fill
description: markdown语法的整理
---

### 记录一下markdown的语法

---

- 语义标记:


| 描述 |  样式 | 代码 |
|---:|:-----:|:-----|
|加粗|**dyf**|`** dyf **`|
|斜体|*dyf*|`* dyf *`|
|加粗斜体| * **dyf** * | `* ** dyf ** *` |
|删除线|~~dyf~~|`~~ dyf ~~`|



- 语义标签:

| 描述 | 样式 | 代码 |
|---:|:---:|:----|
|上标|dyf<sup>s<sup>|`dyf<sup>s<sup>`|
|下标|dyf<sub>s<sub>|`dyf<sub>s<sub>`|
|键盘文本|<kbd>Ctrl<kbd>|`<kbd>Ctrl<kbd>`|

---  


- **标题：**

code:

```
# dyf
## dyf
### dyf
#### dyf 
##### dyf
###### dyf
####### dyf     //错误的代码

```
----
**demo：**





# dyf
## dyf
### dyf
#### dyf
##### dyf
###### dyf

----

＃号之所以能加粗是因为markdown本质是用语法糖封装的html语言，而html只有6种title-size，所以最多加6个#号

-  *分级标题*
  code：

  ```
  dyf
=========
  Stella Del Mattino
---------
  ```
Demo:


dyf
======
Stella Del Mattino
------  

---  

- **引用：**

代码：
``` 
>dyf

>>is

>>>really

>>cool

>!     //注意每行空开

```

Demo:

> dyf

>> is

>>> really

>> cool

> !


----  

- **行内标记：**

Demo:

PHP是世界上`最好`的语言

Code:

```
PHP是世界上`最好`的语言  //标记代码将变为一行

```
----  

- **代码块：**

Demo:
```c
printf("dyf is really cool");
```

Code:
```
 ` ` `C   //language
 printf("dyf is really cool");
 ` ` `
```
不同的语言可以显示不同的高亮，但与主题有关。

----  

- **插入链接：**

Demo:

1. [lavarel toturial](http://laravel-china.org/docs/laravel/5.5/)
2. [codeforces][1]
   [1]:http://codeforces.com/

Code:
``` 
[lavarel torurial](http://laravel-china.org/docs/laravel/5.5/)

[codeforces][1]
[1]http://codeforces.com/   //这是引入式写法

```
---  

- **插入图片**

Demo：

![稻城](https://github.com/Explainaur/hexo-blog/blob/master/source/pictures/%E7%A8%BB%E5%9F%8E.jpeg?raw=true)

Code：
``` 
![稻城](https://github.com/Explainaur/dyf_Blog/blob/master/images/a.jpg?raw=true)
```

上传照片需要图床，可用github当图床，语法格式与链接一致。

---  

到这里差不多就说完了，还有流程图和时序图没有讲，因为我的模板不兼容。


Ps：写道插入图片的时候我在听canon，这是世界上最好听的曲子，突然想起了和我一起去稻城亚丁的两个傻子。

