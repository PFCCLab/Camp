### 姓名
程延福 - [kevincheng2](https://github.com/kevincheng2)

### 实习项目
[项目四：组合机制前反向架构统一](https://github.com/PaddlePaddle/community/blob/master/hackathon/hackathon_5th/【PaddlePaddle Hackathon 5th】飞桨护航计划集训营项目合集.md#项目四组合机制前反向架构统一)

### 本周工作

1. **完成 pow、full_like、stack、unsequeeze 算子的前向拆解下沉**
   - [[Prim][PIR] pow forward sink](https://github.com/PaddlePaddle/Paddle/pull/59274)
   - [[Prim][PIR] full_like forward sink](https://github.com/PaddlePaddle/Paddle/pull/59534)
   - [[Prim][PIR] stack prim sink](https://github.com/PaddlePaddle/Paddle/pull/59713)
   - [[Prim][PIR] unsequeeze prim sink](https://github.com/PaddlePaddle/Paddle/pull/59798)
   
2. **完成组合机制前反向架构统一的分享**
   - [分享资料](https://github.com/PFCCLab/Camp/tree/main/Docs/04_TheUnityOfOperatorForwardAndBackwardInCombinationFeatures)
   
3. **继续整理开发文档**
   - 整理组合机制原理、背景、代码流程相关的开发文档
   - 整理在代码阅读中的常见问题，总结文档


4. **问题疑惑与解答**


	* pytorch 中的 Prim ops集合 和 ATen ops集合 的区别是什么？ 为什么会有这种设计
	
	    答：Prim ops集合有 250 个底层算子，相对较少，是针对组合机制的，因为组合机制可以对算子进行细粒度的拆解，之后使用后端编译器进行计算图优化，这样组合机制就不会导致性能损失。 ATen ops集合有 750 个典型算子，相对较多，这是针对于后端编译器无法进行优化的情况，使用 ATen ops 算子集合替换之后，哪怕不经过编译器的优化，也不会导致太大的性能损失。


### 下周工作

1. 组合机制部分反向算子的迁移工作
2. 整理代码阅读过程中的常见问题
3. 准备答辩

### 导师点评
通过relu和softmax对组合机制全流程大体了解，后续将进一步通过高复杂度的算子，尝试解决可能出现的框架问题。 建议根据自己的经验整理一份开发文档，未来将考虑基于这份开发文档面向所有开发者。
