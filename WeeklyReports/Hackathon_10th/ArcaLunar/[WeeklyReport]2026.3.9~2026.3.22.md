### 姓名

徐启越

### 实习项目

FlashAttention 低精度训练算法研究与 Kernel 开发

### 本周工作

1. 使用 NCU, NSYS 工具对 Kernel 进行 profile，并以 NCU 分析为基础进行优化

  第一版 kernel 以正确性为第一目标进行实现。实现完成后，测得每个线程利用的 per-sector transmitted bytes 较低；achieved occupancy 偏低。

  经过分析优化，修改了 kernel 里的 thread mapping，将 blockDim 与 headDim 对齐，减少线程空置；此外，优化了访存模式，合并访存。
  
2. 为 kernel tests 添加若干 tests，包括 mask 功能、精度测试等

  对于 none, causal 型 mask，参与测试的 attention 包括 torch.fp32.attn, 原始 sage_attention, CUDA kernel. 对于其他 mask，只有 torch.fp32.attn, CUDA kernel 参与测试．

  目前的测试依赖与 baseline 的误差进行判断。后续会需要与论文对齐，用模型（应该会用小模型） + 指标进行判断

3. 调研现有的 cuda 库（cuTLASS, cuBLAS 等），尝试应用现有库做进一步优化

### 导师点评

### 下周计划

1. 进一步分析 kernel 性能与精度，并以此判断瓶颈做优化
2. 继续调研现有 cuda 库，尝试应用并优化
3. 尝试利用小模型，依照论文实验步骤，测试相关指标



