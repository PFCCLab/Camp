### 姓名
Github ID：SecretXV

### 实习项目

分布式能力矩阵建设


### 本周工作

1. **sharding stage3 + dp 卡住问题**

  `sharding stage3 + dp`卡住问题导致原因为单测中手动创建通信组时建立顺序存在问题。采用`fleet.init`中初始化创建的通信组后无此问题。

2. **sharding stage2 + dp 梯度累加功能验证d**

  完善`sharding stage2 + dp`单测。由于`sharding`采用reduce通信，`dp`默认采用allreduce通信，二者loss无法逐位对齐，因此使用`numpy.test.assert_allclose`替换`numpy.test.assert_array_equal`，绝对误差为`1e-5`(by NVIDIA)。由于gpus流水线没有4卡环境，暂时只在本地验证通过。

  PR链接：https://github.com/PaddlePaddle/Paddle/pull/58850

3. **sharding stage3 + dp 梯度累加功能验证**

  为`sharding stage3 + dp`添加相关验证单测。由于gpus流水线没有4卡环境，暂时只在本地验证通过。

  PR链接：https://github.com/PaddlePaddle/Paddle/pull/59468


4. **问题疑惑与解答**

	问题1：sharding 与 Deepspeed中 zero 的区别 ？
	
	答：sharding在不设置dp通信组的情况下，其与zero的整体功能基本一致。其主要的区别在于dp维度的设计，Deepspeed中实现了3D并行：zero（数据），tp（张量），pp（模型）。Paddle中对数据维度进行了拆分，实现了4D并行：sharding，dp，mp，pp。在多机训练中，当单机上（显存）已经可以放下整个模型时，Paddle中可以通过设置dp，减少通信次数。


### 下周工作

1. 完成 mp + stage2, mp + stage3 梯度累加功能验证
2. 学习sep相关代码，尝试 mp + sp + sharding 相关单测的添加

### 导师点评
