### 姓名

李睿文

### 实习项目

框架 API 易用性提升

### 本周工作

1. **修复 `F.unpool1d` 存在的 bug**

- 修复 `F.unpool1d` 在输入参数 `output_size` 是 tuple 时产生的 bug。

- pr 链接: https://github.com/PaddlePaddle/Paddle/pull/65910

2. **针对 `Layer.named_sublayers/Layer.named_parameters/Layer.named_buffers` 的功能增强**

- 为 Layer.named_sublayers/Layer.named_parameters/Layer.named_buffers 增加 remove_duplicate 参数，默认为 True，当为 False 时返回的结果中可以有重复的 named_sublayers/named_parameters/named_buffers。

- pr 链接：https://github.com/PaddlePaddle/Paddle/pull/65946

3. **针对 `paddle.io.BatchSampler` 的功能增强**

- 为 `paddle.io.BatchSampler` 的输入参数 `sampler` 添加任意可迭代类型的支持。

- pr 链接：https://github.com/PaddlePaddle/Paddle/pull/66170

4. **针对 `F.pad` 的功能增强**

- 1. F.pad 在输入 len(pad) == 2 * x.ndim 时，axis 左对齐，需改为 axis 右对齐; 
  2. F.pad 不支持除了 len(pad) == 2 * x.ndim 或 len(pad) == 2 * (x.ndim - 2) 以外的情况，需添加其他情况的支持。

- pr 链接：https://github.com/PaddlePaddle/Paddle/pull/65903

5. **针对 `paddle.linalg.matrix_rank` 的功能增强**

- 增加 `atol` 和 `rtol` 参数。升级后使用 `tol` 时保持不变，增加使用 `atol` 和 `rtol` 的分支。

- pr 链接：https://github.com/PaddlePaddle/Paddle/pull/66070

#### 问题疑惑与解答

暂无

### 下周工作

1. 继续完善 `F.pad` 和 `paddle.linalg.matrix_rank` 的修改。
2. 全面升级 `torch.scatter/torch.scatter_` 到 `paddle.put_along_axis/paddle.put_along_axis_` 的 API 转换规则，为 `paddle.put_along_axis_` 添加 broadcast 参数等。
3. paddle.linalg.lu 若返回 info，返回的 info 需改为 0D Tensor，不兼容升级需分析存量代码。

### 导师点评

李睿文同学工作积极，近期开展了多个Paddle API算子易用性升级的工作。API易用性提升工作将会进一步升级，新增包括PaConvert、Paddle、文档的对齐，因为如果再由其他同学开展，则会存在较多信息传递偏差和沟通成本，因此纳入本项目一起管理。

API易用性升级的相关工作主要来源于 **[代码转换工具]** 的问题，后续需要熟悉PaConvert仓库，最终目标为使单测可以成功运行。在修改完一个API后，需同时提交 **PaConvert规则修改与单测修改**，一个API任务总计包括：

1. API本身修改
2. API中英文档修改
3. API映射文档修改
4. PaConvert映射规则修改
5. PaConvert单测修改

后续工作范围会更大更有挑战性，继续保持当前状态。
