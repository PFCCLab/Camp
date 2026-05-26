### 认领者 GitHub ID
Dryoung95

### 赛题信息
- **进阶任务序号**：#16
- **赛题名称**：沐曦：优化 PaddleOCR-VL-1.5+Metax GPU
- **关联厂商**：沐曦（MetaX）

### 本周工作

1. **第二阶段性能基准测试与优化验证**
   - 在 MetaX C500 GPU 上完成了 PaddleOCR-VL + FastDeploy 的完整性能基准测试
   - 测试配置：`max_model_len=2048`、`max_num_seqs=4`、`max_num_batched_tokens=2048`
   - 测试内容包含：冷启动单请求、顺序50请求（稳态）、并发4x8请求
   - 基准测试结果（vs 阶段一原始基线）：

     | 指标 | 基线 | 当前(mlen2048) | 改善 |
     |------|------|---------------|------|
     | Sequential avg latency | 0.3572s | 0.308s | +13.8% |
     | Sequential throughput | 2.7987 req/s | 3.25 req/s | +16.0% |
     | Concurrent avg latency | 0.5757s | 0.538s | +6.5% |
     | Concurrent P50 latency | 0.5784s | 0.537s | +7.2% |

   - mlen512 配置下吞吐提升 +21.1%，已达 20% 目标
   - mlen2048 配置下吞吐提升 +16.0%，仍差 4%

2. **develop 分支 PR 提交与 CI 推进**
   - 提交 PR: https://github.com/PaddlePaddle/FastDeploy/pull/7619
   - PR 标题：`[Metax][Optimization] Optimize PaddleOCR-VL vision path on Metax GPU`
   - 主要优化内容：
     - PaddleOCR-VL projector 侧 packing 流程优化，支持直接返回 packed image features
     - `extract_vision_features_paddleocr()` 中复用 host 侧 `grid_thw_lst` 元数据，减少不必要的 tensor-to-CPU 同步
     - Siglip vision embeddings 中 packed position embedding 准备优化
     - Siglip attention 和 encoder layer 支持 batch=1 快速路径
     - `apply_rotary_pos_emb_vision()` 显式要求 float32 输入，保证精度
   - PR 当前状态：open，已收到 19 条 review comments（来自 PaddlePaddle-bot），正在处理 review 意见

3. **已完成的优化项回顾**（opt1~opt6 累计效果）
   - **opt1-opt3**：PaddleOCR-VL 视觉特征提取链路精简，减少 host 侧张量拼装开销
   - **opt4-opt5**：encoder cache warm path 优化，重复图片场景约 14% warm-path 改善
   - **opt6**：encoder cache A/B 对比验证（在独立 worktree `FastDeploy_opt6_metax` 中）

4. **性能热点分析与候选优化点梳理**
   - 基于阶段一 profiling 结果，整理了 5 个候选优化热点，确认优先级：
     - 候选1：重复图片链路的缓存复用（已部分实现，收益最大）
     - 候选2：`extract_vision_features_paddleocr()` host 侧张量拼装开销
     - 候选3：Metax attention prefill 元数据构造开销
     - 候选4：首请求冷态 warmup 策略
     - 候选5：多模态边界计算 CPU 开销

5. **问题与解决**
   - 问题：mlen2048 配置下并发 P95 延迟出现退步（0.669s -> 0.688s，-2.9%）
     解决：初步判断为更大上下文长度带来的额外内存/计算开销，需进一步排查调度抖动
   - 问题：PR review 中 bot 提出 batch=1 快速路径与通用路径代码重复、rotary embedding 精度保护移除等意见
     解决：正在处理 review 意见，准备更新 PR

### 下周计划

1. 处理 PR #7619 的 review comments，更新代码并推动合入
2. 将 opt6 encoder cache 改进合入 develop 分支，补齐 mlen2048 剩余 4% 差距
3. 针对并发 P95 tail latency 退步问题进行排查
4. 准备阶段二最终交付物（benchmark 报告 + profiling 证据）

### 当前阻塞

- PR #7619 CI 流水线需要 rerun（Jenkins remoting 层偶发失败，非代码问题）

### 交付物进展

| 交付物 | 状态 | 备注 |
|--------|:----:|------|
| RFC 文档 | ✅ 已完成 | 阶段一报告已提交至 community/rfcs/FastDeploy/ |
| 代码实现 | 🔄 进行中 | PR #7619 已提交，review 中；opt6 待合入 |
| README | ⬜ 未开始 | - |
| 演示视频/截图 | ⬜ 未开始 | - |
| PR 提交 | 🔄 进行中 | https://github.com/PaddlePaddle/FastDeploy/pull/7619 |
