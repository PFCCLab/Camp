### 姓名
刘斯哲

### 实习项目
为开源大语言模型推理增加优化Pass

### 本周工作

1. **对目前demo中的静态图推理过程进行profile并进行优化**

	* 根据之前的profiling，目前的静态图推理过程主要有三个优化点：
    	* 在每一个decoding step的后处理阶段有大量零碎的算子，GPU利用率低
    	* 在每一个decoding step的末尾会发生kv cache的复制，占用时间
    	* 由于kv cache分配的显存形状一直在变化，无法被分配器进行缓存，导致显存占用率一路上升，导致GC耗时
  	* 对上述第一个优化点进行了优化，通过利用CUDA异步执行的特性，在保证算子图中不存在会导致同步和阻塞的操作的情况下，在后处理阶段实际开始之前可以提前提交相关的操作到GPU，避免了CPU bound导致的GPU占用率低下。其中，发现并改写的会导致同步和阻塞的操作包括：
    	* 特定模式的`paddle.full`调用
    	* `if`语句
    	* `paddle.multinomial`


2. **调研W4A8KV4系统QServe的优化点**

	* 对该系统进行了初步的测试

3. **了解Attention显存管理的相关工作**

    * 阅读论文，初步了解了vAttention的工作原理


### 下周工作

1. 继续对目前demo中的静态图推理过程进行优化完善
2. 对QServe系统进行测试和benchmark
3. 继续了解Attention显存管理的相关工作（PagedAttention, GMLake, vAttention等），以及paddle框架的相关实现

### 导师点评

下周希望看到QServe的相关进一步进展，加油！
