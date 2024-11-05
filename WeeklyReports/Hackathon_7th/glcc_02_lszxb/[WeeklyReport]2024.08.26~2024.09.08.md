### 姓名
刘斯哲

### 实习项目
为开源大语言模型推理增加优化Pass

### 本周工作

1. **对目前demo中的静态图推理过程进行profile并进行优化**

	* 对之前提出的优化点进行了完善，对`constant_folding_pass`的相关代码进行了修改
    	* https://github.com/PaddlePaddle/Paddle/pull/68152


2. **了解Attention显存管理的相关工作，并尝试进行实现**

    * 依照vAttention框架的思路，实现了类似的基于VMM API的自定义算子`vtensor_reserve_on_token`
      * https://github.com/PaddlePaddle/PaddleNLP/pull/9126
      * 该算子可以作为`paddle.concat`的替代品，可以实现往tensor的末尾追加数据而不用复制整个tensor
      * 在有较长上下文时，性能有明显提升


3. **阅读QServe系统的代码，了解其具体实现，看看是否还有可以改进的地方**
    
    * 目前粗略阅读了`gemm_cuda.cu`源文件，暂时没什么想法
      * 使用的优化大概包括
        * block launch顺序重排，充分利用L2缓存
        * 用流水线方式重叠读取显存和计算
        * 利用寄存器级并行对4bit权重快速反量化
        * 利用INT8 TensorCore的高吞吐量
      * 关于和FP8结合，感觉有一定难度
        * QServe的一个优点在于可以快速地把4bit权重反量化为INT8
        * FP8 TensorCore没找到公开的kernel内部的C++接口，可能需要写PTX汇编才能调用

### 下周工作

1. 继续完善新实现的自定义算子，为新的自定义算子编写优化pass，使其能够自动覆盖PaddleNLP的大部分模型

### 导师点评
