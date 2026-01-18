### 姓名
戚文斐

### 实习项目
Paddle API 兼容性增强

### 本周工作
1. **API C++ 下沉与文档修复** [PR #77078](https://github.com/PaddlePaddle/Paddle/pull/77078)
   - 完成了 paddle.inverse 算子的 C++ 下沉工作。
   - 修复了相关文档和 API 签名的冲突，解决了 _paddle_docs.py 中的冲突问题。

2. **参数别名支持与代码清理**
   - **paddle.deg2rad** [PR #77168](https://github.com/PaddlePaddle/Paddle/pull/77168): 实现了参数别名支持，使其符合 API 兼容性规范。
   - **paddle.lerp** [PR #77170](https://github.com/PaddlePaddle/Paddle/pull/77170): 实现了 `paddle.lerp` 的参数别名支持；将算子下沉至 C++ 实现，支持动态图模式调用，并基于 Scale 算子优化了底层实现逻辑。
   - **paddle.randint** [PR #77194](https://github.com/PaddlePaddle/Paddle/pull/77194): 为 paddle.randint 增加了参数别名装饰器，并添加了相应的单元测试，增强了接口的兼容性。
   - **paddle.nn.functional.relu / paddle.nn.functional.leaky_relu** [PR #77300](https://github.com/PaddlePaddle/Paddle/pull/77300): 支持 relu、leaky_relu 及其 inplace 版本, 同时修复了 relu_、leaky_relu_ 的参数别名，对齐 PyTorch 接口标准，提升了模型迁移的便利性。

3. **新 API 开发：paddle.addcmul** [PR #77333](https://github.com/PaddlePaddle/Paddle/pull/77333)
   - 完整实现了 paddle.addcmul 算子，支持对两个张量进行逐元素乘法后与标量相乘并加到输入张量上。
   - 包含了 Forward 和 Backward 的 C++ Kernel 实现（CPU/GPU）。
   - 完成了 PIR（Paddle IR）的符号化形状推断支持。
   - 封装了 Python API 接口，并添加了包含 52 个测试用例的完整测试套件，覆盖了动静图、广播机制及多种数据类型。

### 下周工作
1. 修复 addcmul、deg2rad、randint 和 inverse api 的 CI 问题
2. 增加 addcmul paconvert 的测试用例

### 导师点评
