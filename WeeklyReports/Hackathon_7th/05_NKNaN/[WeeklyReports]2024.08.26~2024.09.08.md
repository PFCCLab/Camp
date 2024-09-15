### 姓名

李睿文

### 实习项目

框架 API 易用性提升

### 本周工作

1. **完成核对已修改的 58 个 API**

- 核对已修改的 58 个 API 的 API 映射文档、matcher、单测。

- pr 链接：https://github.com/PaddlePaddle/PaConvert/pull/463 、https://github.com/PaddlePaddle/docs/pull/6848 、https://github.com/PaddlePaddle/Paddle/pull/67772

2. **修复 `paddle.diff` 存在的 bug**

- 当 paddle.diff 输入 n!=1 且有 prepend 或 append 参数时返回结果与 pytorch 不一致。

- pr 链接：https://github.com/PaddlePaddle/Paddle/pull/67800

3. **增强 `paddle.optimizer.SGD/Adadelta/Adagrad/RMSprop` 等优化器的功能**

- paddle.optimizer.SGD/Adadelta/Adagrad/RMSprop 等优化器的 weight_decay 参数需增加 int 输入类型的支持

- pr 链接：https://github.com/PaddlePaddle/Paddle/pull/67947、https://github.com/PaddlePaddle/Paddle/pull/68033

4. **优化 `torch.gather/torch.Tensor.gather` 的 API 转换规则**

- 更新 PaConvert 中的 json 映射规则以及测试案例。

- pr 链接：https://github.com/PaddlePaddle/PaConvert/pull/449

5. **修复 `paddle.linalg.matrix_rank` 新增 kernel 存在的 bug**

- 修复当 rtol 输入为 None 的计算分支内关于 rtol_tensor 形状的问题

- pr 链接：https://github.com/PaddlePaddle/Paddle/pull/68108

6. **增强 `F.max_unpool1d/F.max_unpool2d/F.max_unpool3d` 输入 indices 的类型**

- F.max_unpool1d/F.max_unpool2d/F.max_unpool3d 的输入 indices 需增加 int64 类型输入的支持

- pr 链接：https://github.com/PaddlePaddle/Paddle/pull/68046

7. **修复 `F.batch_norm` 存在的 bug**

- 当 training=True 时，F.batch_norm 的 running_variance 计算结果与 pytorch 不同，因为 pytorch 使用的是无偏方差，paddle 是有偏方差

- pr 链接：https://github.com/PaddlePaddle/Paddle/pull/68159

8. **增强 `F.pad` 的 data_format 参数**

- F.pad 的 data_format 需自动适配3D/5D输入

- pr 链接：https://github.com/PaddlePaddle/Paddle/pull/68214

#### 问题疑惑与解答

暂无

### 下周工作

1. 完善未合入的 pr 以及对应的映射文档、matcher、json 映射法则以及 PaConvert 中的单测；
1. 分析 paddle.nonzero 修改的不兼容升级问题
1. paddle.load 增强输入类型
1. paddle.chunk 支持非整除情况

### 导师点评
