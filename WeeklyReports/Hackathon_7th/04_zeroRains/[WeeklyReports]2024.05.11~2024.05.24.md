### 姓名

卢林军

### 实习项目

组合机制建设和机制推全

### 本周工作

本项目的主要工作是对尚未支持组合机制的算子添加组合机制并完善机制，本周主要工作如下：

1. 为sum和mean op的反向拆解添加动态shape支持


相关 PR:

- https://github.com/PaddlePaddle/Paddle/pull/64789

2. 完善Reduce_as 算子计算方式

之前reduce_as op的实现是在计算好reduce_dim之后将reduce_dim作为输入传给reduce_sum kernel。当reduce_dim为空数组时，reduce_sum会默认执行reduce_all的计算，但是在reduce_as op中，当reduce_dim为空时，期望是不对输入做任何操作。

相关 PR:

- https://github.com/PaddlePaddle/Paddle/pull/65002

3. 为add, subtract, multiply和 divide op的反向拆解添加动态shape支持

同时修复了之前写法导致算子性能下降的BUG，修复multiply_grad的反向拆解在一个输入动态shape另一个输入是静态shape的场景下出现的bug，同时为同类算子新增对应的单测

相关 PR：

- https://github.com/PaddlePaddle/Paddle/pull/65003
- https://github.com/PaddlePaddle/Paddle/pull/65005
- https://github.com/PaddlePaddle/Paddle/pull/65007
- https://github.com/PaddlePaddle/Paddle/pull/65006
- https://github.com/PaddlePaddle/Paddle/pull/65357
- https://github.com/PaddlePaddle/Paddle/pull/65643

5. 为concat_grad添加动态shape支持，添加split_grad动态shape的单测

相关 PR：

- https://github.com/PaddlePaddle/Paddle/pull/65148

6. 为relu_grad的反向拆解过程支持动态shape，添加relu_grad和sigmoid_grad的动态shape单测

相关 PR：

- https://github.com/PaddlePaddle/Paddle/pull/65482
- https://github.com/PaddlePaddle/Paddle/pull/65832

7. 完善get_reduce_dims_from_out函数功能

目前发现get_reduce_dims_from_out在某些动态shape场景下也能正常工作，但是函数设计的本身目的是用于处理静态shape的场景，因此在该函数中添加了动态shap的检测

相关 PR：

- https://github.com/PaddlePaddle/Paddle/pull/65666

8. 为elementwise_pow_grad添加动态shape支持，添加pow_grad动态shape的单测

相关 PR：

- https://github.com/PaddlePaddle/Paddle/pull/65692

9. 为softmax_grad添加动态shape支持

相关 PR：

- https://github.com/PaddlePaddle/Paddle/pull/65961

10. 前向拆解lerp op并添加动态shape支持

相关 PR：

- https://github.com/PaddlePaddle/Paddle/pull/65967

11. 前向拆解log_loss op并添加动态shape支持

相关 PR：

- https://github.com/PaddlePaddle/Paddle/pull/65968

12. 为动态shape场景，添加GetOutputDimsForDynamicShape函数

相关 PR：

- https://github.com/PaddlePaddle/Paddle/pull/66172

13. 修复stack op在旧IR组合机制下的BUG

当Tensor不开启梯度计算时，在旧IR下梯度初始化似乎不是初始化为空值，而是初始化成一个维度为[]的Tensor，这旧导致了其会进入到反向计算prim拆解的流程中，而其中涉及到了一个对梯度（维度为[]）reshape操作，这就导致了这个测试失败。因此需要在初始化变量时开启梯度计算

相关 PR：

- https://github.com/PaddlePaddle/Paddle/pull/66457

14. 前向拆解kldiv_loss op，并支持动态shape

相关 PR：

- https://github.com/PaddlePaddle/Paddle/pull/66510

### 下周工作

1. 收集待拆解算子并为其支持组合机制

### 导师点评

