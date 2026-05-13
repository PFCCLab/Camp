### 认领者 GitHub ID
valorix25

### 赛题信息
- **进阶任务序号**：#16
- **赛题名称**：沐曦 优化 PaddleOCR-VL-1.5+Metax GPU
- **关联厂商**：沐曦（Metax）

### 本周工作

1. **Benchmark 环境修复与 Baseline 建立**
   - 解决 `/dev/shm` 溢出导致 SIGBUS：编译 `shm_redirect.so`（LD_PRELOAD 拦截 `shm_open`），将共享内存重定向到 `/tmp/shm`
   - 解决 OpenMP 库冲突（`libomp.so` 与 `libiomp5.so` 双重 dlopen 冲突）：从 `LD_LIBRARY_PATH` 中排除 `mxgpu_llvm/lib`
   - 修复 `benchmark.py` successful_files 计数、output 路径逻辑
   - 建立 Baseline：吞吐量 0.217 files/sec，平均批次延迟 73.72s，GPU 利用率 max 79%/avg 26%
   - 相关 PR：[valorix25/FastDeploy#2](https://github.com/valorix25/FastDeploy/pull/2)

2. **P0: PaddleX Layout 模型迁移到 Metax GPU（核心收益）**
   - 根因：PaddleX `get_default_device()` 仅检查 CUDA，不识别 metax_gpu custom device，导致 Layout 模型 (PP-DocLayoutV3) 回退到 CPU 运行，GPU 在此期间完全空闲
   - 方案：显式传递 `device="metax_gpu:0"` 给 `create_pipeline()`，通过 `_apply_device` 机制设置 `device_type=metax_gpu`，最终调用 `config.enable_custom_device("metax_gpu", 0)`
   - 效果：吞吐量 0.217→0.283 files/sec（+30.4%），平均批次延迟 73.72s→56.6s（-23.2%）
   - 相关 PR：[valorix25/FastDeploy#2](https://github.com/valorix25/FastDeploy/pull/2)

3. **P3: Routing Prefix Sum 优化**
   - 将 `compute_total_rows_before_expert` 的 binary search O(N×logM) 替换为 atomic counting O(N) + CUB exclusive sum O(M)
   - 新增 `atomic_moe_expert_counts` kernel，替换 `fused_moe_helper.h` 调用点
   - 预期收益：减少 ~5% MoE 阶段延迟

4. **P4: SwiGLU In-place Fusion**
   - 自定义 CUDA kernel 直接 in-place 计算 `SwiGLU(x) = silu(gate) * up`，替代 `paddle::experimental::swiglu()`
   - VecSize=8 向量化（16 字节 = 8 × BF16），256 threads/block，grid-stride loop
   - 预期收益：消除 fc1→swiglu→fc2 间 Tensor 分配和 Paddle 框架调度，减少 ~10% MoE 阶段延迟

5. **P3+P4 联合验证**
   - P3+P4 组合效果：吞吐量 +1.15%，平均批次延迟 -1.14%

6. **P5: RoPE + KV Cache Shared Memory 优化（代码完成，待编译验证）**
   - 在 `cache_kv_with_rope` kernel 中协作将 `block_tables` 加载到 shared memory
   - 预期 prefill 阶段 block_tables 查找延迟从 400-800 cycles 降至 ~2-10 cycles

### 下周计划

1. 在有完整 CUDA→MACA 编译链的环境编译 P5 `cache_kv_with_rope` kernel，验证 shared memory 优化效果
2. 全量回归测试 P0+P3+P4 组合效果
3. 探索 Fused Routing+PrefixSum Kernel（P3 Bonus），解决 race condition 问题

### 当前阻塞

- 本机 MACA SDK 缺少完整开发头文件（`mc_library_types.h`、`MxSmlExtension.h`），`mxcc` 不支持 `cudaStream_t`、`__nv_bfloat16` 等 CUDA 原生类型，P5 kernel 需外部环境编译验证

### 交付物进展

| 交付物 | 状态 | 备注 |
|--------|:----:|------|
| RFC 文档 | ✅ 已完成 | 已提交 RFC 文档至厂商邮箱 |
| 代码实现 | 🔄 进行中 | P0/P3/P4 已验证，P5 待编译验证 |
| README | ✅ 已完成 | PROGRESS.md 记录完整 |
| 演示视频/截图 | ⬜ 未开始 | - |
