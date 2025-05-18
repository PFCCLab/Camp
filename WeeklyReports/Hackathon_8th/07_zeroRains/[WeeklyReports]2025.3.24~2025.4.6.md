### 姓名

卢林军

### 实习项目

大语言模型推理&服务化易用性提升专项

### 本周工作

本项目的主要工作是优化当前PaddleNLP大模型推理服务调用，本周主要工作如下：


1. 修复sm=86搜索GEMM cofig 和MOE cofig时，会因为搜索配置过程异常导致推理提前结束的bug。

相关 PR：

- https://github.com/PaddlePaddle/Paddle/issues/71944
- https://github.com/PaddlePaddle/Paddle/pull/71549
- https://github.com/PaddlePaddle/Paddle/pull/71963

2. 探索DeepSeekV2 在Group-Wise Weight Quant出现乱码的原因

在Qwen2中支持Group-Wise Weight Quant，推理300条数据无乱码出现，证明Group-Wise Weight Quant的实现基本没有问题。

DeepSeekV2不使用WeightOnly时不会出现乱码，使用Channel-Wise Weight Quant时也不会出现乱码，但使用Group-Wise Weight Quant的CPU和GPU Kernel均会出现乱码

说明DeepSeekV2中调用Group-Wise Weight Quant，或者根据Quant Weight计算时调用有错误。

当前发现是非Expert和Shared Expert的部分使用是Group-Wise的Weight Quant，但Expert的部分仍然使用Channel-Wise的Weight Quant。需要将Expert的Weight Quant支持Group-Wise，并同时检查Quant Weight在Expert中的使用逻辑。


### 下周工作

1. 分析DeepSeekV2使用Weight Quant，以及使用Quant Weight计算的逻辑。

### 导师点评



