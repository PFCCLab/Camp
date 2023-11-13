### 姓名
程延福 - [kevincheng2](https://github.com/kevincheng2)

### 实习项目
[项目四：组合机制前反向架构统一](https://github.com/PaddlePaddle/community/blob/master/hackathon/hackathon_5th/【PaddlePaddle Hackathon 5th】飞桨护航计划集训营项目合集.md#项目四组合机制前反向架构统一)

### 本周工作

1. **完成relu算子、softmax算子的前向拆解下沉**
	* [[Prim][PIR] relu forward sink](https://github.com/PaddlePaddle/Paddle/pull/58502)  已合入
	* [[Prim][PIR] softmax forward sink](https://github.com/PaddlePaddle/Paddle/pull/58591)  未合入


2. **理解新IR下Relu的反向迁移过程**  -- 进度 8/10
	
	* 学习PR [[Prim][PIR] Support composite rules of Llama ops](https://github.com/PaddlePaddle/Paddle/pull/58018) 中的算子迁移方法
	
	* 理解 call_vjp 调用规则
	
	  ![whiteboard_exported_image](https://github.com/kevincheng2/Camp/blob/kevincheng2/WeeklyReport/WeeklyReports/04_kevincheng2/assets/backward.png)
	
3. **熟悉新IR下的前向拆解规则** -- 进度 8/10
	
	* 学习PR [[Prim][PIR] Sink Forward Prim](https://github.com/PaddlePaddle/Paddle/pull/58130) 中算子拆解下沉实现，理解 call_decomp 调用规则
	
	  ![whiteboard_exported_image (1)](https://github.com/kevincheng2/Camp/blob/kevincheng2/WeeklyReport/WeeklyReports/04_kevincheng2/assets/forward.png)
	
3. **问题疑惑与解答**


	* 为什么说前向拆非基础算子，反向拆基础算子？这个该怎么理解？
	
	    答：前向计算的时候拆解非基础算子是为了使用基础算子表示出所有算子。这个时候，所有的算子都使用基础算子来表示了，那么反向计算的时候也就没有非基础算子了，只有基础算子，这个时候只需要考虑基础算子的梯度计算就可以了，而基础算子的梯度计算也可以拆解成前向的基础算子。
	
	* 算子实现过程中，Tensor 0d的情况，不特意去支持好像也可以通过测试案例
	
	    答：可以测试一下，静态图下的一些基础算子在0d情况会不会出现问题，现在这个问题可能已经修复了


### 下周工作

1. 实现gelu和dropout算子的迁移工作
2. 其他算子的迁移工作
3. 结合源码，理解组合机制相关的逻辑实现

### 导师点评
通过relu和softmax对组合机制全流程大体了解，后续将进一步通过高复杂度的算子，尝试解决可能出现的框架问题。
建议根据自己的经验整理一份开发文档，未来将考虑基于这份开发文档面向所有开发者。
建议：遇到问题不好解决，及时抛出，有助于进一步提高效率。
