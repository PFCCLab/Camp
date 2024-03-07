### 姓名

卢林军

### 实习项目

组合机制算子专项和机制建设

### 本周工作

本项目的主要工作是对尚未支持组合机制的算子添加组合机制并完善机制，本周主要工作如下：

1. 前向拆解`square`算子

`squre`算子是非基础算子，需要将`square`算子的前向计算进行拆解，使其支持组合机制。

相关 PR：

- https://github.com/PaddlePaddle/Paddle/pull/61434

2. 前向拆解`binary_cross_entropy_with_logits`算子

`binary_cross_entropy_with_logits`算子由多个算子组合而成，经过与基础算子以及已经支持组合机制的组合算子对比，还需要支持`sigmoid_cross_entropy_with_logits`和`mean_all`两个算子对组合机制的支持，即对这两个算子进行前向拆解。

由于没有现成可以直接使用的单测，后续还需继续跟进单测的编写。

相关 PR:

- https://github.com/PaddlePaddle/Paddle/pull/61613

3. 反向拆解`put_along_axis`算子

`put_along_axis`算子是基础算子，其反向计算尚未支持组合机制，需要对其进行反向拆解。目前已弄清楚反向计算流程，但实现过程比较复杂，如何使用基础算子进行反向计算，还需要进一步研究。

相关 PR：

- https://github.com/PaddlePaddle/Paddle/pull/62090

4. 前向拆解`elu`算子

`elu`算子是非基础算子，需要将`elu`算子的前向计算进行拆解，使其支持组合机制。

相关 PR:

- https://github.com/PaddlePaddle/Paddle/pull/62255



### 下周工作

1. 学习在组合机制下，添加组合算子对动态shape支持的代码实现。
2. 尝试对一些组合算子添加动态shape的支持。

### 导师点评

