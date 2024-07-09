### 姓名

李睿文

### 实习项目

框架 API 易用性提升

### 本周工作

1. **针对 `paddle.nn.layer.state_dict` 的功能增强**

- 新增功能需求：增加参数 keep_vars，表示返回 state dict 中的 tensor 是否脱离计算图。

- 提交 pr 并合入: https://github.com/PaddlePaddle/Paddle/pull/64358

2. **修复 `paddle.median` 的 min 分支存在的 bug**

- 修复 paddle.median 在之前增加的 min 分支下输入 int32/int64 数据类型时产生的 bug。

- 反思总结：以后在修改已有 API 时需要更严谨一些，要在完全理解已有代码的基础上进行修改，并且测试案例需要覆盖完备，所有支持的输入数据类型都要测试到。

- 提交 pr：https://github.com/PaddlePaddle/Paddle/pull/64444


#### 问题疑惑与解答

暂无

### 下周工作

1. 计划修改 paddle.io.BatchSampler：升级 sampler 参数，支持任意可迭代类型
2. 尝试进行升级 paddle.add/sub/div/mul 等二元 API 以支持 python number 的任务

### 导师点评

none
