### 姓名
YibinLiu666

### 实习项目
高阶微分的性能分析和优化

### 本周工作

1. **paddle高阶微分性能分析**

	* 测试paddle现有高阶微分算子组合实现与大算子实现的性能。
	* 性能分析，定位到大算子性能较差的高阶微分算子，分析原因


2. **高阶微分算子组合实现添加**

	* 添加部分高阶微分算子的组合实现:
		1. abs_double_grad : https://github.com/PaddlePaddle/Paddle/pull/62335
		2. pow_grad : https://github.com/PaddlePaddle/Paddle/pull/62336
		3. pow_double_grad : https://github.com/PaddlePaddle/Paddle/pull/62338
        4. sin_double_grad : https://github.com/PaddlePaddle/Paddle/pull/62341
        5. cos_double_grad : https://github.com/PaddlePaddle/Paddle/pull/62340
        6. minimum_double_grad : https://github.com/PaddlePaddle/Paddle/pull/62342
        7. maximum_double_grad : https://github.com/PaddlePaddle/Paddle/pull/62343	

3. **问题疑惑与解答**
无

### 下周工作

1. 添加上述pr中实现算子的单测
2. 优化部分微分大算子的性能
3. 实现log_triple_grad和prod_double_grad的组合实现

### 导师点评
请联系导师填写
