### 姓名

卢林军

### 实习项目

大语言模型推理&服务化易用性提升专项

### 本周工作

本项目的主要工作是优化当前PaddleNLP大模型推理服务调用，本周主要工作如下：

1. 大模型相关旧代码清理

当前PaddleNLP中已经实现了效率更高的`Block Attention`和`Append Attention`，需要清理当前默认使用的基本Attention方式，将Block Attention作为默认Attention进行大模型推理工作。

删除了当前`xxxInferenceModel`和`xxxForCausalLMInferenceModel`的定义，全面使用`xxxBlockInferenceModel`和`xxxForCausalLMBlockInferenceModel`。

移除当前`FusedMultiTransformerBase`的使用，全面使用`FusedBlockMultiTransformer`。

修改`Predictor`默认参数，默认开启`block attention`的使用

当前直接使用`block attention`仍然有部分BUG

ps: 此项工作与其他工作冲突较大，后续处理差不多后再进行推进

相关 PR：

- https://github.com/PaddlePaddle/PaddleNLP/pull/9770
- https://github.com/PaddlePaddle/Paddle/pull/70763

2. 自定义算子二次封装与自动编译

收集PaddleNLP中使用的自定义算子(csrc文件夹中)，构建二次封装接口

在setup.py中集成自定义算子编译

CI已过

相关 PR：

- https://github.com/PaddlePaddle/PaddleNLP/pull/9794



### 下周工作

1. 完善自定义算子分类
2. 分析Append Attention使用的Kernel结构，尝试解耦其实例化方式

### 导师点评



