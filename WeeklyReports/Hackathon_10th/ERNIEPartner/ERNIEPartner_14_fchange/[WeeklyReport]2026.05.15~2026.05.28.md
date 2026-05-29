### 认领者 GitHub ID
fchange

### 赛题信息
- **进阶任务序号**：#14
- **赛题名称**：AMD：为 Paddle 框架适配 HIP BF16 精度类型
- **关联厂商**：AMD

### 本周工作

1. **确认赛题目标与验收要求**
   - 已确认本任务目标是在 Paddle 框架中适配 HIP BF16 精度类型，使 PaddleOCR-VL-1.5 等模型在 AMD GPU + ROCm 环境下能够以 BF16 精度完整推理。
   - 已梳理验收要求：需要向 Paddle 主仓库提交 Issue/PR 实现 HIP BF16 适配，并向 PaddleX 提交 Issue/PR 移除现有 ROCm BF16 workaround，最终提供 AMD GPU 上的验证截图。

2. **梳理现有 workaround 与改造方向**
   - 阅读了任务描述中提到的 PaddleX ROCm BF16 临时绕过方案，包括：
     - `is_bfloat16_available()` 在 ROCm 平台默认返回 False；
     - `PaddleOCRVLForConditionalGeneration` 中通过 `_keep_in_fp32_modules = ["visual", "mlp_AR"]` 强制回退 FP32；
     - 静态推理配置中禁用依赖 cuDNN 的 fuse pass。
   - 初步判断后续工作需要分两部分推进：
     - Paddle 侧补齐 HIP BF16 类型、算子注册、编译和测试；
     - PaddleX 侧在 Paddle 支持到位后移除 ROCm BF16 workaround，并验证 PaddleOCR-VL-1.5 推理链路。

3. **开源贡献与准备工作**
   - 本周期暂未向 PaddlePaddle/Paddle 或 PaddlePaddle/PaddleX 提交正式 Issue/PR。
   - 本周期有其他开源贡献记录，可作为个人开源活动参考：
     - https://github.com/biliup/biliup/pull/1628
     - https://github.com/biliup/biliup/issues/1627
     - https://github.com/biliup/biliup/issues/1630
     - https://github.com/TimFelixBeyer/MIDI2ScoreTransformer/issues/9
     - https://github.com/TimFelixBeyer/MIDI2ScoreTransformer/pull/10

4. **问题与解决**
   - 问题：当前尚未完成 AMD GPU + ROCm 环境下的本地验证，因此还不能提交带验证截图的 Paddle/PaddleX PR。
     解决：下一周期优先准备可复现环境，确认 Paddle 在 ROCm 下的 BF16 编译、运行和测试入口。
   - 问题：HIP BF16 适配涉及 Paddle 类型系统、算子注册、MIOpen/ROCm 支持边界，改动面需要进一步收敛。
     解决：下一步先提交 Issue 描述问题与计划，再基于最小可验证路径推进 PR。

### 下周计划

1. 在 PaddlePaddle/Paddle 仓库提交 Issue，明确 HIP BF16 在 ROCm 平台不可用的问题、复现路径和预期改造方案。
2. 搭建或确认 AMD GPU + ROCm 验证环境，优先跑通 PaddleOCR-VL-1.5 当前 FP32/workaround 路径，形成 baseline。
3. 梳理 Paddle 中 BF16 类型、HIP kernel、conv 相关算子和测试入口，确定首个最小 PR 的改动范围。
4. 在 Paddle 侧完成初版 HIP BF16 适配后，再推进 PaddleX 侧移除 workaround 的 Issue/PR。

### 当前阻塞（无则填"无"）

- 暂未完成 AMD GPU + ROCm 环境下的实机验证；需要后续准备算力环境并产出验证截图。
- Paddle/PaddleX 相关正式 Issue/PR 尚未提交。

### 交付物进展

| 交付物 | 状态 | 备注 |
|--------|:----:|------|
| RFC 文档 | 🔄 进行中 | 已完成任务目标、workaround 和改造方向初步梳理 |
| 代码实现 | ⬜ 未开始 | 暂无 Paddle/PaddleX PR |
| README | ⬜ 未开始 | 待验证链路明确后补充 |
| 演示视频/截图 | ⬜ 未开始 | 待 AMD GPU + ROCm 环境验证后提供 |
