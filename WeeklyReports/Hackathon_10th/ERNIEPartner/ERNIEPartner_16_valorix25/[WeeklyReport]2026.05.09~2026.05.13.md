### 认领者 GitHub ID

valorix25

### 赛题信息

- **进阶任务序号**：#16
- **赛题名称**：沐曦 优化 PaddleOCR-VL-1.5+Metax GPU
- **关联厂商**：沐曦（Metax）

### 本周工作

**一、Benchmark 环境修复与 Baseline 建立**

- 解决 `/dev/shm` 溢出导致 SIGBUS：编译 `shm_redirect.so`（LD\_PRELOAD 拦截 `shm_open`），将共享内存重定向到 `/tmp/shm`
- 解决 OpenMP 库冲突（`libomp.so` 与 `libiomp5.so` 双重 dlopen 冲突）：从 `LD_LIBRARY_PATH` 中排除 `mxgpu_llvm/lib`
- 原 FastDeploy/benchmarks/paddleocr\_vl 仅有 A100 评测脚本，经充分调参建立 Metax C500 Baseline，因OmniDocBench\_v1\_5 有1355张图像，评测时间较长，于是从中抽取128张图像作为 baseline
- 相关 PR/Commit：
  - `3f06e8b` [Establish baseline: add benchmark scripts, update image processor and model runner, pin dependencies](https://github.com/valorix25/FastDeploy/commit/3f06e8ba63aafad0dd46c4cf90912f1327f3b50b)

二、**各阶段优化效果汇总**

| 指标       | Baseline        | P0              | P0+P3+P4+P2     | 总变化    |
| :------- | :-------------- | :-------------- | :-------------- | :----- |
| 吞吐量 (文件) | 0.217 files/sec | 0.283 files/sec | 0.285 files/sec | +31.3% |
| 平均批次延迟   | 73.72s          | 56.6s           | 56.2s           | -23.8% |

<br />

1. **P0: PaddleX Layout 模型迁移到 Metax GPU**
   - 根因：PaddleX `get_default_device()` 仅检查 CUDA，不识别 metax\_gpu custom device，Layout 模型回退 CPU
   - 方案：显式传递 `device="metax_gpu:0"` 给 `create_pipeline()`
   - 相关 PR/Commit：
     - `2f961ac` [feat(metax\_ops): P0-P4 GPU operator optimizations](https://github.com/valorix25/FastDeploy/commit/2f961ac84fca4747988f0e501e54981f19e380ef)
2. **P3: Routing Prefix Sum 优化**
   - `compute_total_rows_before_expert`：binary search O(N×logM) → atomic counting + CUB exclusive sum O(N+M)
   - 相关 PR/Commit：
     - `6c06dd4` [feat(metax\_ops): P3/P4 MoE operator optimizations](https://github.com/valorix25/FastDeploy/commit/6c06dd46238f8e868b5a1195fde7574ae5f85057)
3. **P4: SwiGLU In-place Fusion**
   - 自定义 CUDA kernel 替代 `paddle::experimental::swiglu()`，VecSize=8 向量化
   - 相关 PR/Commit：
     - `6c06dd4` [feat(metax\_ops): P3/P4 MoE operator optimizations](https://github.com/valorix25/FastDeploy/commit/6c06dd46238f8e868b5a1195fde7574ae5f85057)
4. **P5: RoPE + KV Cache Shared Memory 优化（代码完成，待编译验证）**
   - `cache_kv_with_rope` kernel 协作将 `block_tables` 加载到 shared memory

### 下周计划

1. 在有完整 CUDA→MACA 编译链的环境编译 P5 `cache_kv_with_rope` kernel，验证 shared memory 优化效果
2. 探索 Fused Routing+PrefixSum Kernel，解决 race condition 问题
3. 扩展 mctlassEx grouped gemm 支持 BF16/FP16 非量化路径（当前仅支持 weight\_only\_int8）
4. topk softmax + radix sort 融合，减少 MoE dispatch 阶段串行 kernel launch
5. dispatch/ffn/reduce 三步 CUDA Graph 捕获，降低 decode 阶段 launch 开销

### 当前阻塞

- 本机 MACA SDK 缺少完整开发头文件（`mc_library_types.h`、`MxSmlExtension.h`），`mxcc` 不支持 `cudaStream_t`、`__nv_bfloat16` 等 CUDA 原生类型，P5 kernel 需外部环境编译验证

### 交付物进展

| 交付物     |   状态   | 备注                    |
| ------- | :----: | --------------------- |
| RFC 文档  |  ✅ 已完成 | 已提交 RFC 文档至厂商邮箱       |
| 代码实现    | 🔄 进行中 | P0/P3/P4 已验证，P5 待编译验证 |
| README  |  ✅ 已完成 | PROGRESS.md 记录完整      |
| 演示视频/截图 |  ⬜ 未开始 | -                     |

