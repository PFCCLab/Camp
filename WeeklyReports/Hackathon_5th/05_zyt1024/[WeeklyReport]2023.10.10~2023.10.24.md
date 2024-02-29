### 姓名
张玉涛
### 实习项目
**算子支持复数计算专项:** 本项目主要负责新增支持复数的算子，为已有算子添加复数 kernel, 以及为相关 API 添加复数功能支持等。

### 本周工作
本周主要工作如下：
1. **学习复数自动微分**

[自动微分](https://github.com/PaddlePaddle/community/tree/master/pfcc/paddle-code-reading/complex_autograd "自动微分")

2. **添加复数算子支持**

本周提交PR: [Partial_concat算子的复数支持](https://github.com/PaddlePaddle/Paddle/pull/58336)


####  Step1: 修改复数算子注册代码
有些算子在CPU、GPU和XPU上均可运行，因此要将所有后端的注册逻辑均添加支持复数计算，支持的复数类型有`complex64`和`complex128`。
代码示例如下：
``` C++
PD_REGISTER_STRUCT_KERNEL(partial_concat_grad,
                          CPU,
                          ALL_LAYOUT,
                          ops::PartialConcatGradientOpKernel,
                          float,
                          double,
                          int,
                          int64_t,
                          phi::dtype::complex<float>,
                          phi::dtype::complex<double>) {}
```
####  Step2: 添加复数算子测试代码
关于测试代码部分，输入的数据可能有复数计算，因此需要判断所要测试的算子类型是否是复数类型的，如果是则需要生成对应复数类型的数据。
示例代码如下：
``` python
if self.dtype == np.complex64 or self.dtype == np.complex128:
    self.vars = [
        (
            np.random.uniform(-1, 1, (self.batch_size, self.column))
            + 1j
            * np.random.uniform(-1, 1, (self.batch_size, self.column))
        ).astype(self.dtype)
        for num in range(self.var_num)
    ]
```
此外，还需要添加相应的测试代码，示例代码如下：
``` python
class TestPartialConcatOp2_Complex64(TestPartialConcatOp):
    def init_para(self):
        self.batch_size = random.randint(1, 10)
        self.column = random.randint(101, 200)
        self.start_index = -5
        self.length = -1
        self.var_num = 3

    def init_kernel_type(self):
        self.dtype = np.complex64
......
class TestPartialConcatOp2_Complex128(TestPartialConcatOp):
    def init_para(self):
        self.batch_size = random.randint(1, 10)
        self.column = random.randint(101, 200)
        self.start_index = -5
        self.length = -1
        self.var_num = 3

    def init_kernel_type(self):
        self.dtype = np.complex128
```

####  Step3: 算子检查类型支持复数类型
示例代码如下：
``` python 
        check_variable_and_dtype(
            x,
            'input[' + str(id) + ']',
            [
                'float16',
                'float32',
                'float64',
                'int32',
                'int64',
                'complex64',
                'complex128',
            ],
            'partial_concat',
        )
```

3. **问题疑惑与解答**
* complex64和complex128的区别？

    complex64: 分别用两个32位浮点数表示实部和虚部

    complex128: 分别用两个64位浮点数表示实部和虚部
### 下周工作

1. 完成`tril和tril_grad、triu和triu_grad、tril_triu和tril_triu_grad、put_along_axis和put_along_axis_grad`等算子的复数支持工作
2. 继续研读 复数自动微分文档

### 导师点评
按时完成学习任务及上手任务，期待下周更深入的工作
