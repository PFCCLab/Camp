### 姓名

田川

### 实习项目

PIR 动转静理想态单测推全验证任务（二期）

### 本周工作

#### **修复 Python 端不 hold 住反向 Program 导致跑反向时 Program 不存在的问题**

大致就是让 `program` 不要提早释放即可, 见 [#63694](https://github.com/PaddlePaddle/Paddle/pull/63694)

TODO: `test_eager_prim` 因为依赖关系比较复杂，暂时不拆分单测了，见[#63694 cmment](https://github.com/PaddlePaddle/Paddle/pull/63694/files#r1590676126) 和 [#63884](https://github.com/PaddlePaddle/Paddle/pull/63884), 应该会在老 ir 退场的时候才比较好解

#### **升级pybind v2.10.3 to v2.12.0**

##### 遇到的一些小问题

下面是最小复现案例，在 GUN 8 及其一下版本，这里的`_Pragma`不会生效。

比较诡异的是如果使用的编译命令是`gcc -c main.cpp -O3 -Wall -Wextra -save-temps`也就是保存预编译文件就不会有这个问题，且预编译情况也是正常的。

暂时使用 patch 的方式修复见：[#63949](https://github.com/PaddlePaddle/Paddle/pull/63949)

```c++
#define Py_tss_NEEDS_INIT   {0}

struct _Py_tss_t {
    int _is_initialized;
    unsigned long _key;
};

#define PYBIND11_TLS_KEY_INIT(var)                                                    \
    _Pragma ("GCC diagnostic push")                                         /**/       \
        _Pragma ("GCC diagnostic ignored \"-Wmissing-field-initializers\"") /**/       \
        _Py_tss_t var                                                                  \
        = Py_tss_NEEDS_INIT;                                                          \
    _Pragma ("GCC diagnostic pop")

int main()
{
    PYBIND11_TLS_KEY_INIT(tstate)
}
```

### 下周工作

1. PyFuncOp 迁移

### 导师点评