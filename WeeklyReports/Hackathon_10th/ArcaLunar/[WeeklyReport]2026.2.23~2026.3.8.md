### 姓名

徐启越

### 实习项目

FlashAttention 低精度训练算法研究与 Kernel 开发

### 本周工作

1. 完善 kernel benchmark
    - 补齐输入构造，benchmark 计时等，支持 causal/mask/scale 等 benchmarking 重要参数
    - 新增多项测评指标并接入自动注册体系
2. 继续实现 SageAttention + FlashMask
    - 新增 cuda/c++ 侧测试，检测精度、性能与显存占用
    - 目前编译可通过，小测试可通过

### 下周计划

1. 继续完善 sage attention+flashmask
    - 检查不同输入下的边界处理并添加相关测试
    - 完善测试数据
    - 将算子接入 kernel-bench 框架
2. 尝试利用已有实现而绕过编译的 cuda kernel 集成到 kernel-bench 的流程
3. 基于后续 benchmark 结果，对 kernel 进行 profiling 并分析 bottleneck

### 导师点评

