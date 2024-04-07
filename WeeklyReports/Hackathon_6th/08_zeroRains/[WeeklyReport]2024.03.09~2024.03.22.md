### 姓名

卢林军

### 实习项目

组合机制算子专项和机制建设

### 本周工作

本项目的主要工作是对尚未支持组合机制的算子添加组合机制并完善机制，本周主要工作如下：

1. 跑blip2模型，统计模型涉及到的算子

2. 尝试让`dropout`算子的前向拆解计算支持动态shape

`dropout`算子目前已经实现了静态shape拆解的逻辑，但是尚未支持动态shape的拆解。需要根据动态shape的支持方式，参考静态实现进行修改。

目前已经基本实现动态shape的支持，但是由于静态图和静态图的随机性不一致，导致最终单测结果存在问题，需要进一步考虑解决方案。

相关 PR:

- https://github.com/PaddlePaddle/Paddle/pull/62660

3. 尝试让`flatten`算子的前向拆解计算支持动态shape

`flatten`算子目前已经实现了静态shape拆解的逻辑，但是尚未支持动态shape的拆解。需要根据动态shape的支持方式，参考静态实现进行修改。

相关 PR：

- https://github.com/PaddlePaddle/Paddle/pull/62706

4. 尝试让`group_norm`算子的前向计算支持动态shape

`group_norm`算子目前已经实现了静态shape拆解的逻辑，但是尚未支持动态shape的拆解。需要根据动态shape的支持方式，参考静态实现进行修改。

相关 PR:

- https://github.com/PaddlePaddle/Paddle/pull/62793

5. 完善`binary_cross_entropy_with_logits`算子前向拆解计算的单测编写

参考动态shape的测试单例中对组合机制拆解算子的测试方法，重新编写`binary_cross_entropy_with_logits`算子前向拆解的测试单例。

目前`binary_cross_entropy_with_logits`算子的子算子`sigmoid_cross_entropy_with_logits`的反向拆解测试中，部分单例无法通过，需要进一步排查原因。

相关 PR：

- https://github.com/PaddlePaddle/Paddle/pull/61613

### 下周工作

1. 继续对组合算子添加动态shape的支持。
2. 完善之前尚未merge的PR。

### 导师点评
对组合机制动态shape有了整体的了解，并能实现复杂组合算子拆解规则的动态shape。
