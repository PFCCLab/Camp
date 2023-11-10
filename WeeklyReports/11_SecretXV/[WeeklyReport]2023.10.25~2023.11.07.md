### 姓名
Github ID：SecretXV

### 实习项目

分布式能力矩阵建设


### 本周工作

1. **pp + gradient merge支持sync send**

  主框架在`p2p_communication.py`中默认采用的是async send的操作，参考`four_direction_p2p_communication.py`，为`p2p_communication.py`添加了`PADDLE_P2P_SYNC_SEND`环境变量的支持。

  PR链接：https://github.com/PaddlePaddle/Paddle/pull/58607

2. **sharding stage1 + dp功能验证**

  为`sharding stage1 + dp`添加相关验证单测。由于gpus流水线没有4卡环境，暂时只在本地验证通过。

  PR链接：https://github.com/PaddlePaddle/Paddle/pull/58395

3. **梯度累计功能验证**

  为`sharding stage3 + dp`添加梯度累计相关单测，遇到`sharding stage3 + dp`卡住的问题，具体位置需要进一步定位。

4. **问题疑惑与解答**

	问题1：async send与sync send的区别是什么？
	
	答：从通信原理上来说send和recv操作必须成对调用，即一个进程调用了send，就必须要有另一个进程调用recv。否则会出现阻塞的情况。async send操作可以实现发送进程调用send后立即返回，不需要等待recv操作完成。async send操作为nccl通信库特有的操作，其原理是nccl内部实现了buffer，实现对send/recv操作的重新排布，当一次send的数据量超过buffer将会卡死（实测在nccl 2.11.0上该buffer<=64MB）。


### 下周工作

1. 定位 stage3 + dp 卡住的问题
2. 完成 stage3 + dp，mp + stage2, mp + stage3 梯度累加功能验证

### 导师点评
