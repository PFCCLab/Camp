### 姓名

李睿文

### 实习项目

框架 API 易用性提升

### 本周工作

1. **排查 distribution API 的 0D 输入问题**

- 修复 0-D 参数输入；sample/rsample 方法增加默认值 `[]`

- pr 链接：https://github.com/PaddlePaddle/Paddle/pull/69090， https://github.com/PaddlePaddle/Paddle/pull/69141

2. **数学计算类API支持整数类型输入**

- 仿照 type promotion 的逻辑，统一对数学计算类一元API增加 autocast 逻辑

- pr 链接：https://github.com/PaddlePaddle/Paddle/pull/69252

3. **修复 `paddle.Tensor.square_`**

- 针对 paddle.Tensor.square_ 无法正确调用的问题，对 square_ op 添加注册

- pr 链接：https://github.com/PaddlePaddle/Paddle/pull/69451

4. **增强 `paddle.bernoulli`**

- paddle.bernoulli 增加参数 `p`

- pr 链接：https://github.com/PaddlePaddle/Paddle/pull/69529


#### 问题疑惑与解答

暂无

### 下周工作

1. 完善已修改 API 的映射文档以及 PaConvert 中的 json 映射规则/mathcer/单测
1. 根据新的需求列表继续进行其他任务的开发

### 导师点评
李睿文同学后续继续完成剩余API的修复，护航计划的剩余时间不多，力争取得一个更丰富的产出。
