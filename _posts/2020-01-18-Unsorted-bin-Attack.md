---
title: Unsorted-bin Attack
tags: [HeapExploit, thinking]
color: pink
description: Unsorted bin Attack
---

## 前言
&emsp;&emsp;这两天学习Unsorted-bin Attack的过程中遇到了一些令我十分困惑的细节，我只好一边读glibc源码一边排查问题，记录一下我的心路历程，免得下次遇到又忘了。

## Unsorted-bin Attack
&emsp;&emsp;Unsorted-bin Attack的主要原理是通过修改unsorted-bin chunk的bk指针，然后可以将某段内存修改为一个很大的数。其实就是修改unsorted bin的front end chunk的bk指针，然后重新请求分配该chunk这个时候会发生一下事情：

```c
      while ((victim = unsorted_chunks (av)->bk) != unsorted_chunks (av))
        {
          bck = victim->bk;
          size = chunksize (victim);
          mchunkptr next = chunk_at_offset (victim, size);

          if (__glibc_unlikely (size <= 2 * SIZE_SZ)
              || __glibc_unlikely (size > av->system_mem))
            malloc_printerr ("malloc(): invalid size (unsorted)");
          if (__glibc_unlikely (chunksize_nomask (next) < 2 * SIZE_SZ)
              || __glibc_unlikely (chunksize_nomask (next) > av->system_mem))
            malloc_printerr ("malloc(): invalid next size (unsorted)");
          if (__glibc_unlikely ((prev_size (next) & ~(SIZE_BITS)) != size))
            malloc_printerr ("malloc(): mismatching next->prev_size (unsorted)");
          if (__glibc_unlikely (bck->fd != victim)
              || __glibc_unlikely (victim->fd != unsorted_chunks (av)))
            malloc_printerr ("malloc(): unsorted double linked list corrupted");
          if (__glibc_unlikely (prev_inuse (next)))
            malloc_printerr ("malloc(): invalid next->prev_inuse (unsorted)");
            /*
             If a small request, try to use last remainder if it is the
             only chunk in unsorted bin.  This helps promote locality for
             runs of consecutive small requests. This is the only
             exception to best-fit, and applies only when there is
             no exact fit for a small chunk.
           */
           ................
                     unsorted_chunks (av)->bk = bck;
		             bck->fd = unsorted_chunks (av);
```
