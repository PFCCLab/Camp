### 姓名
王龙志

### 实习项目
量化算子集成

### 本周工作

1. **编写完善 weight_only 的 PIR 的 pass**<br>
完成 fused_weight_only_linear_pass, 使得 PaddleNLP 中无需进行手动组网完成 weight_only 的量化。
相关 PR：
https://github.com/PaddlePaddle/Paddle/pull/59366

2. **迁移 quant_linear_fuse_pass 到 PIR**
将 quant_linear_fuse_pass 迁移到 PIR 中，目前 PIR 算子中还不支持 quant_linear op，这周尝试自己补全。
3. **补充完善 quant_linear_fuse_pass 在 bert 上的性能分析**<br>
使用 paddle 的 profiler 分析 quant_linear_fuse_pass 在 bert 上的性能瓶颈
![](./images/profiler.png)
### 下周工作
1. 完成 quant_linear_fuse_pass 的 PIR 的迁移。
2. 分析原生量化推理在 bert 模型上的性能瓶颈并解决。

### 导师点评

本周的工作同时对大模型工作和PIR工作都具有重要的意义；性能分析与优化工作也是高性能计算工程师的重要基本能力，因此本周的工作对Paddle的开源和个人成长都非常重要。希望能有完整和具备细节的性能分析报告并给出优化方向。
