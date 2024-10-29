### 姓名
刘斯哲

### 实习项目
为开源大语言模型推理增加优化Pass

### 本周工作

1. **对先前的优化Pass工作进行完善**

  * https://github.com/PaddlePaddle/PaddleNLP/pull/9002
    * 现在对图替换添加了更多的限制条件，要求`pd_op.assign_out_`算子的输出必须是`while`的循环变量，现在应该可以安全地应用到所有模型上了


2. **了解Attention显存管理的相关工作，并尝试进行实现**

    * 为先前的自定义算子`vtensor_reserve_on_token`实现了优化pass，作为对`concat`的替代
      * https://github.com/PaddlePaddle/PaddleNLP/pull/9126
      * 目前会在以下条件下替代`concat`：
        * `concat`的`axis`为1
        * `concat`的输入为两个`Tensor`且`dim`为4（KV Cache）
        * `concat`的输出必须直接连接到`cf.yield`（KV Cache为循环变量）
      * 当前的条件并不足够安全，如果KV Cache在其他位置发生了复制仍然会产生问题


### 下周工作

1. 继续调研W4A8系统QServe的实现，以及CUTLASS中W4 x FP8的实现。

### 导师点评
