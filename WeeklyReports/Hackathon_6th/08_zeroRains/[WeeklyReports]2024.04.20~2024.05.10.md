### 姓名

卢林军

### 实习项目

组合机制算子专项和机制建设

### 本周工作

本项目的主要工作是对尚未支持组合机制的算子添加组合机制并完善机制，本周主要工作如下：

1. 对`reduce_as` op 实现`complex64/128`和`int8`的支持

`reduce_as`算子本身就支持对应类型的使用，我在原本的基础上，补充了对对应类型的单测。

相关 PR:

- https://github.com/PaddlePaddle/Paddle/pull/63782

2. 补充`reduce_as` op的中文文档

补充`reduce_as`的中文文档

相关 PR:

- https://github.com/PaddlePaddle/docs/pull/6621


3. `reduce_as` op的反向拆解

`reduce_as` op是组合机制中的prim op，在动态shape场景下，涉及到广播计算时非常关键。目前已经将`reduce_as`注册成prim op，并添加了对应的反向计算拆解。

相关 PR:

- https://github.com/PaddlePaddle/Paddle/pull/64016


### 下周工作

1. 探索`sigmoid_cross_entropy_with_logits` op中，`pos_weight`参数不为全1 Tensor时，拆解的反向计算和kernel的反向计算结果不一致的原因
2. 修改`reduce_as`的中文文档
3. 完善之前尚未merge的PR。


### 导师点评

