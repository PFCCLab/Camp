### 姓名

卢林军

### 实习项目

组合机制建设和机制推全

### 本周工作

本项目的主要工作是对尚未支持组合机制的算子添加组合机制并完善机制，本周主要工作如下：

1. 为dropout_grad op 添加动态shape支持

相关 PR：

- https://github.com/PaddlePaddle/Paddle/pull/67757

2. 为prod_grad op 添加动态shape支持

相关 PR：

- https://github.com/PaddlePaddle/Paddle/pull/67775

3. 为cumprod_grad 支持动态shape

相关 PR：

- https://github.com/PaddlePaddle/Paddle/pull/67965

4. 为gather_grad, gather_nd_grad 支持动态shape

相关 PR：

- https://github.com/PaddlePaddle/Paddle/pull/67968

5. 为scatter_grad 添加动态shape支持，添加scatter_nd_add_grad的动态shape单测，为所有反向动态shape测试添加拆解检测

相关 PR：

- https://github.com/PaddlePaddle/Paddle/pull/68168

6. 为topk_grad添加动态shape支持

相关 PR：

- https://github.com/PaddlePaddle/Paddle/pull/68228

7. 为unsqueeze_grad, squeeze_grad 添加动态shape单测

相关 PR：

- https://github.com/PaddlePaddle/Paddle/pull/68076

### 下周工作

1. group_norm_grad, layer_norm_grad, masked_select_grad, roll_grad反向适配动态shape
2. one_hot, batch_norm_, batch_norm, bmm 前向适配动态shape

### 导师点评
按时完成工作任务，效率很高


