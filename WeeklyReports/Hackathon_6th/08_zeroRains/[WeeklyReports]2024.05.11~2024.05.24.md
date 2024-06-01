### 姓名

卢林军

### 实习项目

组合机制算子专项和机制建设

### 本周工作

本项目的主要工作是对尚未支持组合机制的算子添加组合机制并完善机制，本周主要工作如下：

1. 探索`sigmoid_cross_entropy_with_logits` op的方向计算kernel与自动微分不一致的原因

`sigmoid_cross_entropy_with_logits` op的反向kernel计算实现错误，根据求导规则进行重新推导并重新实现反向kernel。具体分析见：

- https://github.com/PaddlePaddle/Paddle/issues/64226


相关 PR:

- https://github.com/PaddlePaddle/Paddle/pull/64253

2. 反向拆解`swiglu_grad` op


相关 PR:

- https://github.com/PaddlePaddle/Paddle/pull/64376

3. 修复`binary_cross_entropy_with_logits`前向拆解的BUG

涉及到`sigmoid_cross_entropy_with_logits`和`mean_all`两个算子前向计算的拆解，以及动态shape的支持。

相关 PR:

- https://github.com/PaddlePaddle/Paddle/pull/61613

4. `softmax_with_cross_entropy` op 前向拆解以及动态shape的支持（开发中）

相关 PR:

- https://github.com/PaddlePaddle/Paddle/pull/64569

### 下周工作

1. 继续完成`softmax_with_cross_entropy` op的前向拆解
2. `softmax_with_cross_entropy_grad` op反向拆解


### 导师点评

