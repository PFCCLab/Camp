### 姓名

李睿文

### 实习项目

框架 API 易用性提升

### 本周工作

1. **针对 `paddle.argsort` 和 `paddle.sort` 的功能增强**

- 新增功能需求：添加参数 `stable` 支持稳定排序。

- 提交 pr: 
     - https://github.com/PaddlePaddle/Paddle/pull/63513
     - https://github.com/PaddlePaddle/PaddleCustomDevice/pull/1150
     - https://github.com/PaddlePaddle/PaddleCustomDevice/pull/1156

2. **分析 `paddle.nn.initializer.KaimingNormal` 和 `paddle.nn.initializer.KaimingUniform` 升级后在所有仓库中的不兼容问题**

- 对所有仓库中的存量代码进行搜索排查，找出可能存在的不兼容问题，并撰写不兼容升级评审报告。

#### 问题疑惑与解答

     暂无

### 下周工作

1. 验证 paddle.distribution.Categorical 中 sample、entropy、log_prob 的底层计算逻辑是否和 PyTorch 一致
2. 计划修改 paddle.nn.initializer.TruncatedNormal：增加参数 a, b
3. 计划修改 paddle.nn.Layer 中的 named_sublayers：增加参数 memo

### 导师点评
