### 姓名
刘斯哲

### 实习项目
为开源大语言模型推理增加优化Pass

### 本周工作

1. **对目前demo中的静态图推理过程进行profile并进行优化**

	* 根据之前的profiling，目前的静态图推理过程主要有三个优化点：
    	* 在每一个decoding step的后处理阶段有大量零碎的算子，GPU利用率低
        	* 进一步完善了先前的优化措施
            	* https://github.com/PaddlePaddle/PaddleNLP/pull/9011
        	* 关于特定模式的`paddle.full`调用会导致CUDA同步的问题，发现其是由于`constant_fold_pass`错误地将常量作为parameter存储在GPU上导致的，进行了相应修改解决了这一问题
    	* 在每一个decoding step的末尾会发生kv cache的复制，占用时间
        	* 发现这是由于Paddle框架的算子图会在while循环的末尾增加对于循环变量的assign算子，而转换到PIR中也仍然保留了该部分的算子，导致的非必要的内存拷贝。目前编写了一个PIR Pass删除这部分算子，解决了这个问题。
            	* https://github.com/PaddlePaddle/PaddleNLP/pull/9002
    	* 由于kv cache分配的显存形状一直在变化，无法被分配器进行缓存，导致显存占用率一路上升，导致GC耗时
        	* 进行了进一步的实验，目前发现实际上只有前几次解码会出现这种情况。同时，如果使用`FLAGS_use_virtual_memory_auto_growth=1`启用基于VMM的显存分配器，也可以避免这种情况。


2. **了解Attention显存管理的相关工作，并尝试进行实现**

    * 阅读论文，初步了解了GMLake和vAttention的工作原理
    * 依照vAttention框架的思路，尝试初步实现类似机制的自定义算子


### 下周工作

1. 对之前提出的目前demo中的静态图推理过程的优化点进行最后的完善
2. 阅读QServe系统的代码，了解其具体实现，看看是否还有可以改进的地方
3. 依照vAttention框架的思路，实现具有类似机制的自定义算子，并编写优化pass

### 导师点评
