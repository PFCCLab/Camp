### 姓名
程延福 - [kevincheng2](https://github.com/kevincheng2)

### 实习项目
[项目四：组合机制前反向架构统一](https://github.com/PaddlePaddle/community/blob/master/hackathon/hackathon_5th/【PaddlePaddle Hackathon 5th】飞桨护航计划集训营项目合集.md#项目四组合机制前反向架构统一)

### 本周工作

1. **熟悉静态图场景组合机制case**
	* 理解了静态图下算子的组合机制代码调用方法
	* 熟悉 paddle 单元测试规则


2. **完成新IR下Relu的反向迁移  [[Prim][PIR] Support for rule operator backward under new ir](https://github.com/PaddlePaddle/Paddle/pull/58210)**
	
	* 学习PR [[Prim][PIR] Support composite rules of Llama ops](https://github.com/PaddlePaddle/Paddle/pull/58018) 中的算子迁移方法
	
	* 根据 [PR](https://github.com/PaddlePaddle/Paddle/pull/58018) 和 mentor 的指导，完成新IR下Relu的反向迁移，并提交 [Relu 反向迁移 PR](https://github.com/PaddlePaddle/Paddle/pull/58210)
	
	* 理解 call_vjp 调用规则 -- todo
	
3. **熟悉新IR下的前向拆解规则**
	* 学习PR [[Prim][PIR] Sink Forward Prim](https://github.com/PaddlePaddle/Paddle/pull/58130) 中算子拆解下沉实现，理解 call_decomp 调用规则 -- todo
	
	* 参考PR中的mean算子，实现relu的前向拆解下沉 -- todo
	
3. **问题疑惑与解答**


	* 基础算子和组合算子怎么界定？有什么区别？
	
	    答：区分基础算子和组合算子需要考虑这么几个规则，原子性、可组合性、可优化性、高频率、算子库支持度。但是在实际应用实现的过程中，基础算子和组合算子的界定没有特别严格，设计时需要考虑算子实现的颗粒、算子的性能和算子功能性等具体的方面，针对不同的算子的不同特点去考虑。
	
	* decomp_interface_gen_op_list.py 生成代码时，配置relu会同时生成 relu 和 relu_ 对应代码？
	
	    答：一个小bug，relu 和 relu_ 特性有区别，需要分开考虑，relu_ 不需要拆分，已提交pr [[Prim]fix interface decomp](https://github.com/PaddlePaddle/Paddle/pull/58322)


### 下周工作

1. 实现relu的前向拆解下沉
2. 结合源码，理解 call_decomp 、call_vjp 的调用规则
3. 其他算子的迁移和拆解工作

### 导师点评
对组合机制项目有初步的认识，通过relu的任务对组合机制流程有了大体掌握。
建议：遇到问题不好解决，及时抛出，有助于进一步提高效率。
