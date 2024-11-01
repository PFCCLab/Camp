### 姓名

方国勇

### 实习项目

CINN 符号推导

### 本周工作

1. 尝试在 Windows 上编译 CINN，未果
2. 修复之前发现的 ci 覆盖率为 0 的问题，并修复存量问题
   1. https://github.com/PaddlePaddle/Paddle/pull/68607
3. 完善 `det`, `is_empty`,`eye` 的接口实现
   1. https://github.com/PaddlePaddle/Paddle/pull/68547
   2. https://github.com/PaddlePaddle/Paddle/pull/68548
4. 提交 `prune_gate_by_capacity`, `frame` 的符号推导接口
   1. https://github.com/PaddlePaddle/Paddle/pull/68644
   2. 学习了 OpTest 的单测写法，给 `prune_gate_by_capacity` 新增了一个 Optest 单测
5. 在 4 的基础上，参考 OpTest 的符号检查，尝试给 unittest 添加符号推导检查的方法
   1. https://github.com/PaddlePaddle/Paddle/pull/68670
   2. 使用 Value 而不是 fetch_op 简化了检查写法
6. 优化 PIR 下检查 view tensor 被 inplace api 使用时检查和报错优化
   1. https://github.com/PaddlePaddle/Paddle/pull/68669

### 下周工作

1. 完善已提交 pr
2. 完成中等以及复杂的算子推导接口


### 导师点评
