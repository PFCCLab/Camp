### 姓名

田川

### 实习项目

动转静 SOT 模块 Python 3.12 支持

### 本周工作

1. **FOR_ITER段错误**

学习老的`create_inline_call_fn`，了解`FOR_ITER`的执行过程。参考 [#62261](https://github.com/PaddlePaddle/Paddle/pull/) 的注释

#### 遇到的问题，具体表现情况为下面三种情况:

* 生成跳转错误
```bash
[Resumed Function]: Inline call for loop function $resume_1@for_list_1_af1a0
 39           0 RESUME                   0
              2 LOAD_FAST                2 (object_168)
        >>    4 FOR_ITER                24 (to 56)

...
             54 END_FOR
        >>   56 LOAD_FAST                1 (i)
             58 LOAD_FAST                0 (x)
             60 LOAD_FAST                2 (object_168)
             62 BUILD_TUPLE              3
             64 RETURN_VALUE
```

* `END_FOR`字节码不生成
```bash
[Resumed Function]: Inline call for loop function $resume_1@undefined_var_case_0_af1a0
269           0 RESUME                   0
              2 LOAD_FAST                2 (object_165)
        >>    4 FOR_ITER                38 (84)

...
             74 JUMP_FORWARD             1 (to 78)
             76 JUMP_FORWARD             2 (to 82)
        >>   78 NOP
             80 JUMP_BACKWARD           39 (to 4)
        >>   82 NOP
             86 LOAD_FAST                0 (i)
...
```

* `resume`错误

在 Python3.12 下
```bash
 13           0 RESUME                   0

              2 END_FOR                                 # <-- 这里 resume 错误
              4 LOAD_FAST_CHECK          0 (zzz)
              6 LOAD_CONST               2 (1)
              8 BINARY_OP                0 (+)
             10 RETURN_VALUE
```

在 Python3.11 下
```bash
 13           0 RESUME                   0
              2 LOAD_FAST                0 (zzz)
              4 LOAD_CONST               2 (1)
              6 BINARY_OP                0 (+)

 14          10 STORE_FAST               0 (zzz)
             12 LOAD_FAST                0 (zzz)
             14 RETURN_VALUE
```

#### 解析

在 Python3.12 `_inline_call_for_loop`上正常生成的字节码为

```python
  8           0 RESUME                   0
              2 LOAD_FAST                2 (object_165)
        >>    4 FOR_ITER                37 (to 82)       # <-- 需要修改的跳转位置的位置

 10           8 STORE_FAST               0 (i)
             10 LOAD_GLOBAL              0 (sot)
             20 LOAD_ATTR                2 (psdb)
             40 LOAD_ATTR                5 (NULL|self + breakgraph)
             60 CALL                     0

 11          68 POP_TOP
             70 LOAD_FAST                0 (i)
             72 STORE_FAST               1 (zzz)
             74 JUMP_FORWARD             1 (to 78)
             76 JUMP_FORWARD             3 (to 84)
        >>   78 NOP
             80 JUMP_BACKWARD           39 (to 4)
        >>   82 END_FOR                                   # <-- 改变的位置
        >>   84 NOP
             86 LOAD_FAST                0 (i)
             88 LOAD_FAST                1 (zzz)
             90 LOAD_FAST                2 (object_165)
             92 BUILD_TUPLE              3
             94 RETURN_VALUE
```

在 Python3.11 `_inline_call_for_loop`生成的字节码为

```python
  8           0 RESUME                   0
              2 LOAD_FAST                2 (object_165)
        >>    4 FOR_ITER                37 (to 80)

 10           6 STORE_FAST               0 (i)
              8 LOAD_GLOBAL              0 (sot)
             20 LOAD_ATTR                1 (psdb)
             30 LOAD_METHOD              2 (breakgraph)
             52 PRECALL                  0
             56 CALL                     0

 11          66 POP_TOP
             68 LOAD_FAST                0 (i)
             70 STORE_FAST               1 (zzz)
             72 JUMP_FORWARD             1 (to 76)
             74 JUMP_FORWARD             2 (to 80)
        >>   76 NOP
             78 JUMP_BACKWARD           38 (to 4)
        >>   80 NOP
             82 LOAD_FAST                0 (i)
             84 LOAD_FAST                1 (zzz)
             86 LOAD_FAST                2 (object_165)
             88 BUILD_TUPLE              3
             90 RETURN_VALUE
```

#### 总结

我们可以看到`FOR_ITER`在 3.11 下会让 `iterator` 结束后跳出整个循环体内的字节码（也就是迭代器耗尽时），而在 3.12 下整个 for 是由 `FOR_ITER` 和 `END_FOR` 组成的，在大部分`FOR_ITER`及其超指令会在 `FOR_ITER` 字节码内跳过 `END_FOR` 字节码运行（仅做标识）。

* 关于为什么需要专门生成`END_FOR`:

因为需要与`FOR_ITER`对应。

* 为什么不直接拷贝:

因为需要再中间插入跳转，所以不直接拷贝

直接拷贝案例
```bash
...
             70 LOAD_FAST                0 (i)
             72 STORE_FAST               1 (zzz)
        >>   74 END_FOR
             76 JUMP_FORWARD             1 (to 80)
             78 JUMP_FORWARD             3 (to 84)
        >>   80 NOP
             82 JUMP_BACKWARD           39 (to 4)
        >>   84 NOP
...
```

* 关于生成跳转错误

`relocate_jump_target` 没有处理 JUMP 相关特化, 具体可以参考 cpython 中 `Lib/dis.py` 文件的 `findlabels` 和 `_get_instructions_bytes` 两个方法

* 预拦截

* * 对`FOR_ITER`跳转的拦截`check_for_iter_jump_to`

### 下周工作

1. PaddleSOT Python 3.12 单测适配

### 导师点评

川子太强了👍，极速推进 SOT Python 3.12 支持，单测基本推全完成，也完成了若干个疑难问题的修复，以一己之力推动 Paddle 领先竞品一个版本～

希望接下来可以沉淀整个 Python 3.12 支持过程中的疑难问题，注重问题的总结，另外最好产出类似[《Python 3.11 核心加速原理——指令特化》](https://nyakku.moe/posts/2023/08/27/python311-instruction-specializing.html)的 3.12 变动以及适配的文档，在之后一起分享

另一方面，可以在任务推进的过程中思考一下如果是你要如何从零规划整个任务，包括阶段划分、任务拆分、分配任务给其他同学等等

LGTMeow <img src="https://www.gstatic.com/android/keyboard/emojikitchen/20230803/u1f44d/u1f44d_u1f43e.png" width="14" alt="🐾"/>
