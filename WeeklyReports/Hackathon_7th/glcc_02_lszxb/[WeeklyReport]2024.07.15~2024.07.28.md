### 姓名
刘斯哲

### 实习项目
为开源大语言模型推理增加优化Pass

### 本周工作

1. **使用PaddleNLP的demo跑通大语言模型的BF16推理**

	* 跑通了LLaMA模型的推理并在不同的batch_size、input_len进行了benchmark
	* 修复了当前demo中指定src_length会导致报错的问题
        https://github.com/PaddlePaddle/PaddleNLP/pull/8768
    * 修复了当前demo中benchmark时token数计算错误的问题
        https://github.com/PaddlePaddle/PaddleNLP/pull/8769


2. **对目前demo中的静态图推理过程进行profile**

	* 使用Nsight System初步进行了profiling，发现了一些可能的优化点


3. **调研W4A8KV4系统QServe的优化点**

	* 该系统主要优化点可以分为两部分：使用W4A8量化与使用KV4量化。其中对于W4A8有以下优点：
		* W4A8相比W4A16能利用int8 Tensorcore，在大batch时具有更大的吞吐量
		* W4A8相比W8A8能在更小的batch上达到最大吞吐量
	* 该系统针对W4A8做了以下优化，着重于减少昂贵的cuda core运算，增加tensor core指令占比：
		* 权重使用两阶段量化：将权重先用channel-wise量化方法量化到8-bit，再将8-bit量化权重再次量化到4-bit。这样只需进行4-bit到8-bit的反量化即可直接进行tensor core运算，减少了cuda core运算
		* 权重重排：通过对模型权重事先进行重排序，减少指针运算
		* 寄存器级别并行：往32位的寄存器中塞入4个8bit数进行运算，使得一个thread可以同时对4个权重参数进行反量化，减少了cuda core开销


### 下周工作

1. 继续对目前demo中的静态图推理过程进行profile，并寻找可能的优化方案

### 导师点评

