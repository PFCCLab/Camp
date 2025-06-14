### 姓名

卢林军

### 实习项目

大语言模型推理&服务化易用性提升专项

### 本周工作

本项目的主要工作是优化当前PaddleNLP大模型推理服务调用，本周主要工作如下：

1. 使fastsafetensors其支持paddle

了解fastsafetensors的基本工作流程，目前已支持paddle在single模式下的Tensor加载，分布式加载(parallel)已经支持了cpu+gloo后端的加载，gpu+nccl后端的加载仍然存在一些问题，后续会继续进行分析。
通过替换torch API以及添加必要的cpp函数，已经实现了fastsafetensors对paddle的支持。

修复UIN16数据类型的模型加载。使用bfloat16的Tensor接收数据

修复多卡GPU并行加载Tensor的BUG。实现基于rank的device设置

修复分布式场景下Tensor加载异常的问题。将broadcast和scatter改为同步OP。

相关仓库：

- https://github.com/zeroRains/fastsafetensors 的paddle分支


### 下周工作

1. 跟进fastsafetensors的torch和paddle依赖分离的PR

### 导师点评



