### 姓名

方国勇

### 实习项目

CINN 符号推导

### 本周工作

1. 修复 prune_gate_by_capacity 的编译问题 https://github.com/PaddlePaddle/Paddle/pull/68644
2. 新增 random_routing 符号推导接口 https://github.com/PaddlePaddle/Paddle/pull/68670
   1. 没有单测
3. 关闭部分单测
   1. https://github.com/PaddlePaddle/Paddle/pull/68841
   2. https://github.com/PaddlePaddle/Paddle/pull/68851
   3. https://github.com/PaddlePaddle/Paddle/pull/68853
4. 新增 LSTM 符号推导
   1. 找到的 OpTest 单测，包含 LOD 信息，过于古老

### 下周工作

1. 本周完成已提交 pr 的修复和合入
    | pr | 类型 | 备注 |
    | --- | --- | --- |
    | https://github.com/PaddlePaddle/Paddle/pull/68907 | LSTM | 新提交的 pr| 
    |  https://github.com/PaddlePaddle/Paddle/pull/68670 | RandomRouting | 按照 review 意见修改完成|
    | https://github.com/PaddlePaddle/Paddle/pull/68644 | frame prune_gate_by_capacity | 按照 review 意见修改|
    | https://github.com/PaddlePaddle/Paddle/pull/68548 | eye  | ci 未过|
    | https://github.com/PaddlePaddle/Paddle/pull/68547 | is_empty det |  已 approve， ci 未过|
    | https://github.com/PaddlePaddle/Paddle/pull/68841 | 关闭检查 | 已 approve |
    | https://github.com/PaddlePaddle/Paddle/pull/68851 | 关闭检查 | 按照 review 意见修改完成  |
    |.https://github.com/PaddlePaddle/Paddle/pull/68853 | 关闭检查 |已 approve  |
2. 提交 lstsq, llm_int8_linear, instance_norm 的接口实现 pr
   1. 每天可以新增一个接口（涉及 kernel 的可能开始会比较慢）和对以往 pr 的修复

### 导师点评
