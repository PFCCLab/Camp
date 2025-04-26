### 姓名

卢林军

### 实习项目

大语言模型推理&服务化易用性提升专项

### 本周工作

本项目的主要工作是优化当前PaddleNLP大模型推理服务调用，本周主要工作如下：


1. 探索DeepSeekV2 在Group-Wise Weight Quant出现乱码的原因

为Expoert的计算API传入group_size信息，经过测试发现没有乱码出现，但部分prompt无法正确输出结束的Token。

通过比对bfloat和weight only inference的各中间变量结果，发现在执行Expert部分时，不论是group_wise的weight quant还是channel_wise的weight quant。对于相同的输入，量化前和量化后的计算差异比较大，估计确实是Expert的计算有问题。

后续会尝试修改expert的计算方式，以解决量化前后差异的问题。

相关 PR：

- https://github.com/PaddlePaddle/PaddleNLP/pull/10174

2. 修复最新PaddleNLP对DeepSeekV2采用weight only的int8/int4推理时，静态图/动态图推理，以及动转静导出触发的bug

在计算qkv_linear的逻辑中，新增了对kwargs信息的获取，但是调用时没有传入，导致变量获取不到。在调用时将kwargs一起传入即可

相关 PR：

- https://github.com/PaddlePaddle/PaddleNLP/pull/10491


### 下周工作

1. 分析DeepSeekV2使用Weight Quant，以及使用Quant Weight计算的逻辑。

### 导师点评



