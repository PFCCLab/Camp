### 姓名
杨新宇

### 实习项目
CINN 支持动态 Shape 专项（PIR 部分）

### 本周工作
本周主要工作如下：
1. 合入支持了logsumexp、logcumsumexp、linspace、logspace、min、poisson、repeat_interleave、topk, triu_indices等算子的符号推导
合入pr https://github.com/PaddlePaddle/Paddle/pull/62800
https://github.com/PaddlePaddle/Paddle/pull/63000
2. 配置nsys profile环境，学习使用nsys profile分析cuda kernel性能

### 下周工作

1. 使用nsys profile分析group norm算子的性能问题，尝试进行性能优化

### 导师点评

本周新宇进度较快、积极主动支持编译器后端相关的工作、infer_symbolic_shape 的任务已经收尾结束，并支持了单测提供了验证
