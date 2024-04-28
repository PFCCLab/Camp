### 姓名

李睿文

### 实习项目

框架 API 易用性提升

### 本周工作

1. **针对 `paddle.argsort` 和 `paddle.sort` 的功能增强**

- 新增功能需求：添加参数 `stable` 支持稳定排序。

- 提交 pr 并合入: 
     - https://github.com/PaddlePaddle/Paddle/pull/63513
     - https://github.com/PaddlePaddle/PaddleCustomDevice/pull/1150
     - https://github.com/PaddlePaddle/PaddleCustomDevice/pull/1156

2. **分析 `paddle.nn.initializer.KaimingNormal` 和 `paddle.nn.initializer.KaimingUniform` 升级后在所有仓库中的不兼容问题**

- 对所有仓库中的存量代码进行搜索排查，找出可能存在的不兼容问题，并撰写不兼容升级评审报告。

3. **针对 `paddle.nn.functional.max_unpool1d`、`paddle.nn.functional.max_unpool2d`、`paddle.nn.functional.max_unpool3d` 的功能增强以及bug修复**

- 修复 `paddle.nn.functional.max_unpool1d` 的参数判断 bug：输入正确的 output_size 会报错。
- 对输入参数 `x` 添加支持 int64 输入。

- 提交 pr 并合入: https://github.com/PaddlePaddle/Paddle/pull/63648

4. **针对 `paddle.nn.functional.kl_div` 的功能增强**

- 新增功能需求：添加参数 `log_target` 支持用户传入属于 log 空间的 `label` 参数。

- 提交 pr 并合入: https://github.com/PaddlePaddle/Paddle/pull/63860

#### 问题疑惑与解答

     暂无

### 下周工作

1. 验证 paddle.distribution.Categorical 中 sample、entropy、log_prob 的底层计算逻辑是否和 PyTorch 一致
2. 计划修改 paddle.nn.initializer.TruncatedNormal：增加参数 a, b
3. 计划修改 paddle.nn.Layer 中的 named_sublayers：增加参数 memo

### 导师点评

李睿文近期工作取得较明显的进展，对kl_div、sort/argsort、group_norm等多个问题进行了开展。学习了XPU SDK的相关用法，并实现了xpu kernel的修改，后续继续保持工作的势头，多阅读paddle框架中已有的API/OP/kernel代码。