### 姓名
Qin-sx

### 实习项目
框架 API 易用性提升

### 本周工作

1. **升级paddle.nn.LayerList函数**

	* [对应issue](https://github.com/PaddlePaddle/Paddle/issues/71224)
	* [对应pr](https://github.com/PaddlePaddle/Paddle/pull/71540)
    * 调研和测试了对应的PyTorch函数，优化了paddle.nn.LayerList函数


2. **解决paddle.logsumexp函数的bug**

	* [对应issue](https://github.com/PaddlePaddle/Paddle/issues/71225)
	* 测试了不同版本的paddle，issue中的`paddle.logsumexp`函数没有问题，`log_softmax`函数的问题可以复现。
    * `log_softmax`函数在输入大于8G时会出现类似问题，目前在ai studio上通过注释函数定位问题。
    * 应该是以下代码出现了问题，但是还没有定位到具体原因。推测是因为启动的block数量远大于硬件block上限，正在查找相关理论依据。

    ```c++
    AccT thread_max = ThreadVecReduce<MaxFunctor, T, AccT, kVecSize>(
      batch_input,
      dim_size,
      input_align_shift,
      MaxFunctor<T, AccT>(),
      -std::numeric_limits<AccT>::infinity());
    BlockReduceMax<AccT>(&thread_max);
    ```


3. **问题疑惑与解答**


### 下周工作

1. 继续解决paddle.logsumexp函数的bug

### 导师点评
