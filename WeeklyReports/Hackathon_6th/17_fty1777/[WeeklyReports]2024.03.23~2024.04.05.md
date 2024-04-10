### 姓名

Github ID: [fty1777](https://github.com/fty1777)

### 实习项目

CINN 支持动态 Shape 专项（PIR 部分）

### 本周工作

1. **完善一系列算子的符号推导**

    推进完善pd_op中的searchsorted, masked_select, pad, unbind, unique和unique_consecutive的符号推导，并完成单元测试。expand_as算子由于上游API问题暂无法完成符号推导。

    PR: https://github.com/PaddlePaddle/Paddle/pull/63016

2. **从InferMeta学习einsum的形状推导规则**

2. **配置nsys环境，熟悉使用nsys profiler对paddle进行性能采集的过程**

### 下周工作

1. 推进符号推导PR合并。
2. 继续推进op_op.einsum符号推导实现。
3. 启动后端性能相关工作。

### 导师点评
