### 姓名
Github ID：SecretXV

### 实习项目

分布式能力矩阵建设


### 本周工作

1. **mp + sharding stage2 梯度累加功能验证**

  为`mp + sharding stage2`添加相关验证单测。由于gpus流水线没有4卡环境，暂时只在本地验证通过。

  PR链接：https://github.com/PaddlePaddle/Paddle/pull/59880

2. **mp + sharding stage3 梯度累加功能验证**

  为`mp + sharding stage3`添加相关验证单测。由于gpus流水线没有4卡环境，暂时只在本地验证通过。

  PR链接：https://github.com/PaddlePaddle/Paddle/pull/59880

3. **mp + sp + sharding stage2 梯度累加功能验证**

  为`mp + sp + sharding stage2`添加相关验证单测。由于gpus流水线没有4卡环境，暂时只在本地验证通过。

  PR链接：https://github.com/PaddlePaddle/Paddle/pull/59880

4. **mp + sp + sharding stage3 梯度累加功能验证**

  为`mp + sp + sharding stage3`添加相关验证单测。由于gpus流水线没有4卡环境，暂时只在本地验证通过。

  PR链接：https://github.com/PaddlePaddle/Paddle/pull/59880

5. **问题疑惑与解答**

	问题1：混合并行单测添加注意事项
	
	答：在混合并行单测添加时，一般会采用`fleet.init`进行初始化，并从`hcg`中获取框架创建好对应的通信组。但是`fleet.init`内部会对初始化进行判断，避免重复初始化。在混合并行单测中，会遇到在单个单测文件中需要修改并行策略，然后重复调用`fleet.init`的情况，对于该种情况，可以参考如下hack代码，进行反初始化。从而实现单测文件中重复调用`fleet.init`。代码如下：

  ```python
  def finanlize_fleet():
    # hack to finanlize fleet
    # if call multi-times fleet.init(), must call finanlize_fleet() before call fleet.init()
    import paddle.distributed.fleet.base.topology as tp
    from paddle.distributed import parallel_helper

    parallel_helper.__parallel_ctx__clz__ = None
    tp._HYBRID_PARALLEL_GROUP = None
  ```


### 下周工作

1. 参与并行策略精度验证工作


### 导师点评

