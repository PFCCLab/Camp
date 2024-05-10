### 姓名

梁书豪

### 实习项目

CINN 支持动态 Shape 专项（前端方向）

### 本周工作

本周工作为看CINN代码，主要以`reduce`算子为例，理解CINN的工作流程和关键Pass的内容。

1. 前端Pass代码理解

    * 前端的作用是在算子层面对计算图进行优化，例如算子融合、死代码消除；另外针对动态shape，还会进行shape表达式传递
    * `ShapeOptimizationPass`：将动态shape的维度定义为变量，并在算子间进行传递，从而可以通过运行时输入的shape推导后续算子的大小
    * `BuildCinnPass`：具体实现在`SubgraphDetector`，将子图（一组只有一个输出的算子）进行融合

2. 后端Tactic代码理解

    * 后端的作用是将已经融合的算子转换成高效的CUDA实现
    * 后端的流程为：首先将算子lower为多层循环表示，然后对循环进行reorder、fusion、inline、tiling等操作，再将循环绑定到cuda的thread和block上，最后lower得到可编译的cuda代码
    * 后端的一个重要概念为SpatialSpace（sp_space）和ReduceBroadcastSpace（rb_space），sp_space指的是可以并行的维度，例如`reduce`时的非`axis`维，rb_space则是不可并行的维度


### 下周工作

1. 检查`Convert0DTo1DPass`所影响的单测用例，总结0D Tensor影响的Pass，思考一种通用的解决0D Tensor问题的思路
2. 继续看后端代码中`PostProcess`的部分

### 导师点评

书豪初次接触 CINN 前端项目，用极短的时间迅速建立起对 CINN 整体执行流程的理解，并以构造单测的方式，从不同算子、不同参数的角度测试并分析 CINN 端到端执行流程。在此过程中，还发现算子支持不完备的场景，为 CINN 的正确性保障添砖加瓦。本周工作扎实饱满，继续保持。
