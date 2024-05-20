### 姓名

李睿文

### 实习项目

框架 API 易用性提升

### 本周工作

1. **针对 `paddle.nn.functional.group_norm` 和 `paddle.nn.GroupNorm` 的功能增强**

- 新增功能需求：支持 NCL, NLC, NCDHW, NDHWC 格式的输入。

- 主要修改的是 gpu kernel 中，针对 NHWC 格式且数据类型为 fp16 和 bf16 的输入做的优化计算分支，将其扩展到支持 3-D 和 5-D 输入类型。

- 提交 pr 并合入: https://github.com/PaddlePaddle/Paddle/pull/63881

2. **分析 `paddle.distribution.Categorical` 与 `torch.distributions.Categorical` 不一致的地方**

- 阅读 `torch.distributions.Categorical` 与 `paddle.distribution.Categorical` 的 API 实现上的差异，分析当 `logits` 参数矫正含义后， `sample`、`entropy`、`log_prob` 的底层计算逻辑是否需要修改以及如何修改。

3. **针对 `paddle.nn.initializer.TruncatedNormal` 的功能增强**

- 新增功能需求：添加截断参数 `a` 和 `b`，与 PyTorch 功能对齐。

- 提交 pr: https://github.com/PaddlePaddle/Paddle/pull/64110


#### 问题疑惑与解答

     问题：关于底层的类型提升机制可以参考哪部分的相关代码呢？

### 下周工作

1. 计划修改 paddle.nn.Layer 中的 stat_dict 方法：增加参数 keep_vars
2. 计划修改 paddle.io.BatchSampler：升级 sampler 参数，支持任意可迭代类型
3. 升级 paddle.add/sub/div/mul 等二元 API 以支持 python number 的任务，需进一步参考类型提升进行修改

### 导师点评

李睿文近期工作进展迅速，工作产出量饱满，后续期望继续保持投入，扫清更多API的功能薄弱之处，提升Paddle的产品易用性。同时在过程中可持续学习和积累代码开发经验。
