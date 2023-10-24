### 姓名
Github ID：SecretXV

### 实习项目

分布式能力矩阵建设


### 本周工作

1. **sharding stage1支持main_grad**

  主框架在`DygraphShardingOptimizer`中支持了sharing stage1的main_grad功能，但是在PaddleNLP套件中Sharing stage1对应的`distributed_scalar`并未实现main_grad相关逻辑。该PR仿照`GroupShardedScaler`为`distributed_scalar`添加了main_grad的支持。

  PR链接（已合入develop）：https://github.com/PaddlePaddle/Paddle/pull/57972

2. **sharding stage1支持bf16**

  为`distributed_scalar`添加bf16的支持。Sharing stage1已完全支持main_grad功能。

  PR链接（已合入develop）：https://github.com/PaddlePaddle/Paddle/pull/58212

3. **问题疑惑与解答**

	问题1：对于master_weight来说，其在梯度更新时，会首先将梯度类型提升到 FP32，然后将其更新到 FP32 类型参数备份中。对于master_grad来说，其在反向传播结束后将权重梯度cast为FP32。二者实际上在更新参数时，梯度值都是FP32类型。可以认为在更新参数方面。二者精度是一致的。master_grad在哪个环节会带来精度收益？
	
	答：**反向传播结束，参数更新前，**有一些模型可能会有例如梯度clip之类的操作，如果不转成fp32类型，有可能会在这些过程损失精度；对于fp16类型，一般会对loss进行scale，反向传播结束后还得unscale，恢复到原始的梯度范围，该过程也会丢失部分的**小数位精度**。


### 下周工作

1. 添加 sharding stage1 + dp 相关单测
2. 支持 sharding stage3 相关工作

### 导师点评
请联系导师填写