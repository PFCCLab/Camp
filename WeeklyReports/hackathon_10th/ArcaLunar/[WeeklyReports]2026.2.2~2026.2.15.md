### 姓名

徐启越

### 实习项目

FlashAttention 低精度训练算法研究与 Kernel 开发

### 本周工作

1. 搭建 CUDA Kernel + PyTorch Baseline 的统一测试框架 (ArcaLunar/kernel-bench)
    - 基于 PyTorch C++/CUDA Extension 设计 kernel adapter，便于后续 SageAttention / FA+FlashMask/ Sage+FlashMask 算子的统一接入和测试
    - 设计 metric registry，便于后续对所有算子在不同指标上进行统一测试，且易于拓展
    - 设计 reporter，便于导出为 csv,json 供进一步分析
2. 研读 SageAttention 算法细节与实现
3. 研读 FlashMask 算法细节与实现
4. 基于已有 Sage Attention 和 FlashMask 实现，开发 Sage+FlashMask（尚未进行测试）

### 下周计划

1. 进一步添加 metric 支持（如速度，FLOPs 等等）
2. Sage+FlashMask 算子开发
3. 将 Sage+FlashMask, Sage, FA+FlashMask 接入框架进行测试
4. 根据测试结果和性能分析，对算子进行优化

### 导师点评




