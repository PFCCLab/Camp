### 姓名

李睿文

### 实习项目

框架 API 易用性提升

### 本周工作

1. **继续进行针对 `F.pad` 的功能增强**

- 1. F.pad 在输入 len(pad) == 2 * x.ndim 时，axis 左对齐，需改为 axis 右对齐; 
  2. F.pad 不支持除了 len(pad) == 2 * x.ndim 或 len(pad) == 2 * (x.ndim - 2) 以外的情况，需添加其他情况的支持。

- pr 链接：https://github.com/PaddlePaddle/Paddle/pull/65903、https://github.com/PaddlePaddle/Paddle/pull/67298

2. **继续进行针对 `paddle.linalg.matrix_rank` 的功能增强**

- 增加 `atol` 和 `rtol` 参数。

- pr 链接：https://github.com/PaddlePaddle/Paddle/pull/66070

3. **针对 `paddle.put_along_axis_` 的功能增强**

- 增加 `broadcast` 参数，与非 inplace API 保持一致。

- pr 链接：https://github.com/PaddlePaddle/Paddle/pull/66687

4. **全面升级 `torch.scatter/torch.scatter_` 的 API 转换规则**

- 更新 PaConvert 中的 json 映射规则以及测试案例。

- pr 链接：https://github.com/PaddlePaddle/PaConvert/pull/440

5. **升级 `F.kl_div` 的 API 转换规则**

- 更新 PaConvert 中的 matcher 以及测试案例。

- pr 链接：https://github.com/PaddlePaddle/PaConvert/pull/438

6. **针对 `paddle.linalg.solve` 的功能增强**

- 增加 `left` 参数，以支持 `Out * X = Y` 的情况。

- pr 链接：https://github.com/PaddlePaddle/Paddle/pull/67071

#### 问题疑惑与解答

暂无

### 下周工作

1. 继续完善 `F.pad` 和 `paddle.linalg.matrix_rank` 的修改。
2. 优化 `torch.gather/torch.Tensor.gather` 的 API 转换规则；`torch.Tensor.scatter_` 增加对 x 的测试。
3. `paddle.linalg.lu` 当输入矩阵形状是 `[m, n]` 时，若返回 info，返回的 info 需改为 0D Tensor，暂不存在不兼容问题，可以修改。
4. `paddle.load` 对齐 `torch.load` 持更多路径对象。
5. `paddle.empty` 等包含 dtype 参数的 API 添加⽀持 paddle.dtype 类型的输入。

### 导师点评

后续注意对已修改API进一步完善转换规则，只有Paddle与PaConvert做好配套工作，互相结合，才能够帮助用户更好的使用Paddle。
