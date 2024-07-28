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


### 下周工作

1. 继续对目前demo中的静态图推理过程进行profile，并寻找可能的优化方案

### 导师点评

