### 姓名

梁书豪

### 实习项目

CINN 支持动态 Shape 专项（前端方向）

### 本周工作

1. 修复CINN前端在reduce的axis为`None`时的错误 PR：https://github.com/PaddlePaddle/Paddle/pull/62612

2. CINN后端`TileFirstGeneralTactic`升级方案研究

    * 针对多种形状的reduce算子，手写CUDA代码进行测试，包括reduce维很大、axis在或不在最后一维、有多个不连续axis的情况
    * 针对global memory coalescing，总结了一种维度分配方法（warp维、thread维、block维和loop维），在手写算子中得到较好的性能

### 下周工作

1. 在`TileFirstGeneralTactic`中实现global memory coalescing策略

### 导师点评

书豪在收尾 0D Tensor 的过程中，展现出了较强的自驱能力，主动修复前端的补丁，相关单测建设得较为全面；希望再接再厉，在升级 global memory coalescing 的过程中，承担起「方案设计-实验测试-代码上线」的全流程工作
