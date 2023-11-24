### 姓名
程延福 - [kevincheng2](https://github.com/kevincheng2)

### 实习项目
[项目四：组合机制前反向架构统一](https://github.com/PaddlePaddle/community/blob/master/hackathon/hackathon_5th/【PaddlePaddle Hackathon 5th】飞桨护航计划集训营项目合集.md#项目四组合机制前反向架构统一)

### 本周工作

1. **完成gelu、dropout、sqrt、rsqrt算子的前向拆解下沉**

   - [[Prim][PIR] gelu forward sink](https://github.com/PaddlePaddle/Paddle/pull/58981)
   - [[Prim][PIR] dropout forward sink](https://github.com/PaddlePaddle/Paddle/pull/59176)
   - [[Prim][PIR] sqrt forward sink and fix Decomp bug](https://github.com/PaddlePaddle/Paddle/pull/59135)
   - [[Prim][PIR] rsqrt forward sink](https://github.com/PaddlePaddle/Paddle/pull/59202)

2. **理解前向decomp代码生成过程**

   - 修复decomp代码生成中，单个op_name 对应多个 op_kernel_func 导致生成代码过多的 bug

     [[Prim][PIR] sqrt forward sink and fix Decomp bug](https://github.com/PaddlePaddle/Paddle/pull/59135)

3. **整理开发文档**

   - 整理组合机制原理、背景、代码流程相关的开发文档
   - 整理在代码阅读中的常见问题，总结文档


4. **问题疑惑与解答**


	* paddle中c++端有没有Tensor填充随机值的方法？
	
	    答：可以在 paddle/fluid/primitive/primitive.yaml 添加 uniform 配置，这样会生成一个 uniform 的基础算子，在 primitive.h 中可以看到。
	    

### 下周工作

1. 实现 relus.py 中其他算子的迁移工作
2. 组合机制部分反向算子的迁移工作
3. 结合pytorch中的组合机制，理解组合机制的背景

### 导师点评
通过relu和softmax对组合机制全流程大体了解，后续将进一步通过高复杂度的算子，尝试解决可能出现的框架问题。 建议根据自己的经验整理一份开发文档，未来将考虑基于这份开发文档面向所有开发者。
