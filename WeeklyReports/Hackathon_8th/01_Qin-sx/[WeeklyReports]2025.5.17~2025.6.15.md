### 姓名
Qin-sx

### 实习项目
框架 API 易用性提升

### 本周工作

1. **在scaled_dot_product_attention函数中加入bool mask**

	* [对应pr](https://github.com/PaddlePaddle/Paddle/pull/72927)

2. **优化to_tensor函数中的bf16转换**

	* [对应pr](https://github.com/PaddlePaddle/Paddle/pull/73050)

3. **在fused_rms_norm函数中加入begin_norm_axis的默认值和维度检查**

	* [对应pr](https://github.com/PaddlePaddle/Paddle/pull/73123)

4. **修改tensor.data的返回，不包含梯度信息**

	* [对应pr](https://github.com/PaddlePaddle/Paddle/pull/73246)

5. **修改bernoulli的inplace实现，p为随机值为1的概率**

	* [对应pr](https://github.com/PaddlePaddle/Paddle/pull/73271)

6. **修复atleast函数中，输入为tensor的list的bug**

	* [对应pr](https://github.com/PaddlePaddle/Paddle/pull/73102)

7. **在smooth_l1_loss函数中加入is_huber参数**

	* [对应pr](https://github.com/PaddlePaddle/Paddle/pull/73325)

8. **scaled_dot_product_attention函数兼容3D输入**

	* [对应pr](https://github.com/PaddlePaddle/Paddle/pull/73336)

9. **在KaimingNormal中加入fan_out参数**

	* [对应pr](https://github.com/PaddlePaddle/Paddle/pull/73347)

10. **在paddle.tensor中加入float16和bfloat16接口**

	* [对应pr](https://github.com/PaddlePaddle/Paddle/pull/73351)

11. **问题疑惑与解答**

### 下周工作

1. 完善之前未合并的pr
2. 调研MultiLabelMarginLoss和Module.eval函数

### 导师点评