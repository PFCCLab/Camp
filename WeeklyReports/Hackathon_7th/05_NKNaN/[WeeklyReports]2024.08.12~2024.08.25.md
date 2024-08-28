### 姓名

李睿文

### 实习项目

框架 API 易用性提升

### 本周工作

1. **继续进行针对 `paddle.linalg.matrix_rank` 的功能增强**

- 增加 `atol` 和 `rtol` 参数。

- pr 链接：https://github.com/PaddlePaddle/Paddle/pull/66070

2. **修复 `test_pad_op.py` 存在的 bug**

- 补充动态图静态图；paddle.nn.functional.pad 传参时缺少了 value 参数。

- pr 链接：https://github.com/PaddlePaddle/Paddle/pull/67536

3. **修复 `paddle.linalg.lu` 存在的 bug**

- 当 paddle.linalg.lu 输入 `x` 形状为 [m, n] 时且 `get_infos=True`，将返回的 info Tensor 从 1-D Tensor 改为 0-D Tensor

- pr 链接：https://github.com/PaddlePaddle/Paddle/pull/67421

4. **优化 `torch.gather/torch.Tensor.gather` 的 API 转换规则**

- 更新 PaConvert 中的 json 映射规则以及测试案例。

- pr 链接：https://github.com/PaddlePaddle/PaConvert/pull/449

5. **排查已修改的 58 个 API**

- 核对已修改的 58 个 API 的 API 映射文档、matcher、单测。

- pr 链接：https://github.com/PaddlePaddle/PaConvert/pull/463 、https://github.com/PaddlePaddle/docs/pull/6848 、https://github.com/PaddlePaddle/Paddle/pull/67772

#### 问题疑惑与解答

暂无

### 下周工作

1. 继续排查已修改的 58 个 API。
1. 修改经排查发现的问题。
1. `paddle.load` 对齐 `torch.load` 持更多路径对象。
1. `paddle.empty` 等包含 dtype 参数的 API 添加⽀持 paddle.dtype 类型的输入。

### 导师点评
