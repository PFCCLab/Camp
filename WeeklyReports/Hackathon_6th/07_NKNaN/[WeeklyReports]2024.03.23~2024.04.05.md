### 姓名

李睿文

### 实习项目

框架 API 易用性提升

### 本周工作

1. **针对 `paddle.nn.initializer.XavierNormal` 和 `paddle.nn.initializer.XavierUniform` 的功能增强**

- 新增功能需求：添加缩放系数 gain。

- 提交 pr 并合入: https://github.com/PaddlePaddle/Paddle/pull/63134

2. **修复 `paddle.nanmedian` 存在的问题**

- 存在的问题：'min' 模式下 index 分配的内存空间大小等于output的空间大小，'avg' 模式下 index 分配的内存空间大小等于output的空间大小的 2 倍。由于之前修改 cpu kernel 时漏改了一处计算 index 的地方，造成了 cpu kernel 底层运算会出现崩溃。

- 提交 pr: https://github.com/PaddlePaddle/Paddle/pull/63221

3. **针对 `paddle.nn.initializer.KaimingNormal` 和 `paddle.nn.initializer.KaimingUniform` 的功能增强**

- 新增功能需求：添加参数 mode，以支持 'fan_in' 和 'fan_out' 两种模式

- 提交 pr：https://github.com/PaddlePaddle/Paddle/pull/63268

#### 问题疑惑与解答

     暂无

### 下周工作

1. 验证 paddle.distribution.Categorical 中 sample、entropy、log_prob 的底层计算逻辑是否和 PyTorch 一致
2. 计划修改 paddle.nn.initializer.TruncatedNormal：增加参数 a, b
3. 计划修改 paddle.nn.Layer 中的 named_sublayers：增加参数 memo

### 导师点评

李睿文本周完成了1个API的修改，1个之前API的Bug修复，1个不兼容升级API的修改（评审文档待开展）。

需要注意的是，不兼容升级需要进行评审，因此修改API只是一小部分工作，较多的工作是对历史存量代码进行扫描分析，看是否会导致其不兼容问题，历史存量代码可以参考飞桨官方Github Organization下的存量模型代码。https://github.com/PaddlePaddle/Paddle

后续可逐步开展更高难度的API修改工作。
