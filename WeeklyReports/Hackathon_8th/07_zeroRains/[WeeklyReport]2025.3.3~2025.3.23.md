### 姓名

卢林军

### 实习项目

大语言模型推理&服务化易用性提升专项

### 本周工作

本项目的主要工作是优化当前PaddleNLP大模型推理服务调用，本周主要工作如下：


1. 自定义算子二次封装与自动编译

1.1 在PaddleNLP的setup.py中，集成不同设备的编译（待验证）

1.2 设计二次封装自定义算子的多硬件派发方案，并完成初步实现

相关 PR：

- https://github.com/PaddlePaddle/PaddleNLP/pull/9794

2. 实现group-wise quant_weight的GPU kernel

包括int4_col_pack， int4_row_pack 以及int8的GPU kernel实现，经过验证int8的kernel实现与CPU对齐，int4的kernel在bfloat16的情况下，float16的情况下，当矩阵大于[256,256]时，无法对齐。

DEBUG int4 kernel的实现

修改PaddleNLP中deepseek模型调用quant_weight的方式（调用CPU Kernel改为调用GPU Kernel）并添加单测

相关 PR：

- https://github.com/PaddlePaddle/Paddle/pull/71549
- https://github.com/PaddlePaddle/PaddleNLP/pull/10174



### 下周工作

1. 讨论多硬件派发方案合理性，并完善与验证
2. Debug group-wise int4 quant_weight的实现

### 导师点评



