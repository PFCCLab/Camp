### 姓名

卢林军

### 实习项目

大语言模型推理&服务化易用性提升专项

### 本周工作

本项目的主要工作是优化当前PaddleNLP大模型推理服务调用，本周主要工作如下：


1. 分析MOE架构中Expert计算部分，采用量化和不采用量化产生较大精度差异的原因

当前MOE架构中使用Cutlass编写的DeGEMM kernel处理反量化的expert计算，主要问题在于使用的是基本的DefaultScaleIterators去遍历量化后的Scale，目前是通过参考fpA_intB_GEMM 以及TRT-LLM的做法添加了scale iterator的设置，使用FineGrainedScaleZeroIterator处理group_size != -1的情况。

从DeepSeekV2推理的结果来看，基本解决了之前直接传入group_size参数出现的无法输出结束符的问题，但仍然在一些case上会有一些乱码的情况。

从数值结果上看，int8的量化和不量化的计算结果比较接近，int4的量化计算结果与不量化的计算结果仍然存在差距

相关 PR：

- https://github.com/PaddlePaddle/PaddleNLP/pull/10174

2. 学习fastsafetensors并使其兼容paddle调用

了解fastsafetensors的基本工作流程，目前已支持paddle在single模式下的Tensor加载，分布式加载(parallel)已经支持了cpu+gloo后端的加载，gpu+nccl后端的加载仍然存在一些问题，后续会继续进行分析。


相关仓库：

- https://github.com/zeroRains/fastsafetensors 的paddle分支


### 下周工作

1. 修复fastsafetensors兼容paddle时在gpu+nccl后端加载的问题
2. 使用其他case确保fastsafetensors的兼容性

### 导师点评



