# 进阶任务 #13 · 第 2 周周报（截止 2026-05-15）

> 定稿（2026-05-12）。本期重心：Phase 1 OV CPU+GPU 实测落地 + Phase 2 切片器实战修复 + Phase 3 评测体系搭桥 + 真实扫描国标 14 页复测验证 OCR 路径。

- **GitHub ID**：bob798
- **项目仓库**：[doc-qna-openvino](https://github.com/bob798/doc-qna-openvino)
- **任务**：基于 OpenVINO 的多模态文档理解与智能应用开发（任务 #13）
- **覆盖周期**：2026-05-09 ~ 2026-05-15

---

## 1. 本周进展

### 1.1 Phase 1 解封 —— 真实推理 Benchmark 数据落地

W1 阶段 Phase 1 代码完成但卡在 IR 落地，本周一次性打通：

- **IR 路径**：选用 ModelScope `zhaohb/PaddleOCR-VL-1.5-ov` 拆分布局（INT4 LLM + INT8 Vision + PP-DoclayoutV3 layout detector），免去自行 export，避免 optimum 的 PaddleOCR-VL 不支持问题
- **inference.py 适配层**（commit [`6a11524`](https://github.com/bob798/doc-qna-openvino/commit/6a11524)）：自动识别 `split` (zhaohb) / `vlmpipeline` (官方 notebook) 两种 IR 布局，对外 `infer(image, prompt) -> InferenceResult` 接口不变
- **依赖锁定**：`openvino==2025.4.1`、`openvino-tokenizers==2025.4.1.0`、`transformers==4.54.0`、`pdfplumber`、`pypdfium2`、`shapely`、`protobuf`、`pytesseract`

**Benchmark 1 · OpenVINO 推理（10 张测试图，1 warmup + 3 runs 取均值，2026-05-12 在 Intel AI PC 上实测）**：

| 类型 | CPU 范围 (ms) | GPU 范围 (ms) | 备注 |
|------|---------------|---------------|------|
| 公式 | 1137 – 1976 | 560 – 930 | 输出短，最快 |
| 纯文字 | 1323 – 4344 | 637 – 2573 | 取决于文字密度 |
| 表格 | 3310 – 3621 | 2325 – 2518 | 一致性最好 |
| 图文混排 | 3044 – 4373 | 2162 – 4027 | 输出 token 最多，最慢 |

**全图均值：CPU 2948 ms / GPU 2003 ms（GPU/CPU 加速 1.47×）**。原始数据：`openvino/results/phase1/benchmark_inference.cpu.{md,json}` + `openvino/results/phase1/gpu/benchmark_inference.{md,json}`。NPU 数据待本周补。

**PyTorch 基线被弃测**：HF 远端 `modeling_paddleocr_vl.py` 默认 FP32，torch 2.11.0+cpu 实测 text_01 单图 32 max_new_tokens ≈ 360 s；按默认 2048 token、10 张 × 3 runs 推算需 ~15 hr，单机不可行。同时 IR 自带 INT4(LLM)+INT8(Vision) 量化，"OV vs PT" 实质混合了"框架+量化"两个变量。改以"OV CPU vs OV GPU vs OV NPU"做框架内部对照，对评委（Intel + 百度 OpenVINO 团队）更直接展示 Intel AI PC 全家桶能力。期间发现并修了两个真实坑：
- 处理器调用缺 chat template，需 `apply_chat_template` 注入 `<|IMAGE_START|><|IMAGE_PLACEHOLDER|><|IMAGE_END|>`（修复点：`openvino/src/inference.py`）
- transformers 4.54 把 `create_causal_mask(inputs_embeds=...)` 重命名为 `input_embeds=...`，HF 远端代码未跟进（绕行：本地 monkey-patch 缓存的 `modeling_paddleocr_vl.py`，正式提 issue 给 PaddlePaddle 团队）

**Benchmark 2 · Tesseract vs PaddleOCR-VL 解析质量**（chi_sim+eng）：

| 维度 | Tesseract 字数 | PaddleOCR-VL 字数 | 结论 |
|------|----------------|-------------------|------|
| 表格（3 张）| 0 – 87 | **884 – 1122** | PaddleOCR-VL 输出完整 HTML `<table>`，Tesseract 几乎无法识别表格结构 |
| 图文混排 | 60 – 114 | **551 – 815** | PaddleOCR-VL 显著更全，能拼回阅读顺序 |
| 公式 | 输出明文（错） | 输出 LaTeX `$ E=mc^{2} $` ✅ | PaddleOCR-VL 识别公式语义 |
| 纯文字（密集） | 184 | 133（紧凑） | 互有胜负 |

原始数据 + 单图 diff：`openvino/results/phase1/quality_compare.{md,json}` + `quality_compare/<img>/`。

> 这两组实测数将在 W3 替换 `docs/进阶方案.md` 中"≥ 2×"、"显著优于传统 OCR"等占位说法。

### 1.2 Phase 2 收尾 —— 切片器实战修复

实测过程暴露了切片器的两个真实漏洞，已修复：

| 修复 | Commit | 影响 |
|------|--------|------|
| chunker 支持 HTML 表格 | [`7a097a7`](https://github.com/bob798/doc-qna-openvino/commit/7a097a7) | PaddleOCR-VL 输出 `<table>...</table>` HTML，原 chunker 仅识别 `\|...\|` 管道表格，所有表格漏切。新增 `_HTMLTableToRows`（stdlib `html.parser`）+ `_normalize_html_tables` 把 HTML 表格就地转 Markdown 管道表格，下游识别复用 |
| pdf_preprocessor 文字层路径补表格 | [`f20a2a3`](https://github.com/bob798/doc-qna-openvino/commit/f20a2a3) | text-layer 路径只用 `extract_text()`，pdfplumber 把表格吐成"型号 功率 工作温度 A100 300W..."平铺串。新增 `extract_tables()` 把每页表格转 Markdown 附在末尾，喂给 chunker 表格感知逻辑 |

**Phase 2 端到端验证**（3 份合成 PDF · 用 `scripts/run_phase2_pipeline.py`）：

| PDF | 路由 | 页 | 用时 | text / table_header / table |
|------|-------|----|------|------------------------------|
| `scanned.pdf` | OCR (2/2) | 2 | 4.2 s | 1 / 0 / 0 ⚠️ |
| `spec_with_tables.pdf` | text-layer (1/1) | 1 | 0.03 s | **3 / 1 / 3** ✅ |
| `text_pdf.pdf` | mixed (1 text + 1 OCR) | 2 | 2.1 s | 4 / 0 / 0 |

`spec_with_tables.pdf` 切片数从修复前的 3 → 7，每个表格行 chunk 都附带表头上下文（解决"300W 是哪一列"的歧义）。

### 1.3 工具链补齐

- 本机 Python 安装（winget Python 3.12.10），UTF-8 输出（`PYTHONUTF8=1`）
- Tesseract 5.4.0 (UB-Mannheim) + `chi_sim/eng/osd.traineddata`（用户 `~/tessdata/` + `TESSDATA_PREFIX`）
- 仓库拆分完成（W1 末已做，本周确认）：QNN 路径搬到 [`bob798/paddleocr-vl-qnn`](https://github.com/bob798/paddleocr-vl-qnn)，进阶任务 #26 小伴在 [`bob798/xiaoban`](https://github.com/bob798/xiaoban) 的 `submission/` 子目录

### 1.4 LLM 选型升级 —— Qwen2.5 → Qwen3-1.7B INT4

W1 原计划用 Qwen2.5-7B（后降到 1.5B）。Qwen3（2025-04 发布）现已成熟：

- **OpenVINO GenAI 原生支持** `Qwen3ForCausalLM`（>= 2025.2）
- **现成 IR** ：HF `OpenVINO/Qwen3-1.7B-int4-ov` 直接拉，免转换
- **RAG 场景**：`enable_thinking=False` 关掉思考模式（不需要长 CoT）
- **尺寸对照**：Qwen3-1.7B-INT4 ≈ Qwen2.5-1.5B-INT4（CPU 完全够），整体替换成本：换 model_id 字符串 + chat_template（Qwen3 默认正确）

`docs/进阶方案.md` §四、`docs/项目计划.md`、`docs/开发手册.md`、`README.md` 已统一同步。备选：Qwen3-0.6B（更快）或 Qwen3-4B（更强）。

### 1.5 评测体系定稿 —— 三层证据架构

把 Phase 4 评测从"主观对比"升级为可量化、可复现的三层证据（详见 [`docs/进阶方案.md` §七](../进阶方案.md)）：

1. **客观对照** — OmniDocBench (CVPR 2025) 子集 20 页 × {Tesseract, PaddleOCR-VL}，指标 Edit Distance / TEDS / CDM 调官方 `pdf_validation/` 脚本
2. **业务场景** — 自建 18+ 题 (Phase 3.3 跑通后扩到 30~50)，5 类分布参考 MMLongBench-Doc（lookup 35% / concept 25% / cross_doc 20% / refusal 15% / formula 5%）
3. **自动评测** — RAGAS 跑 faithfulness / answer_relevancy / context_precision / context_recall

**评测材料已就位（27 件）**：

| 类别 | 数量 | 获取 |
|------|------|------|
| 直链 PDF | 5 | PaddleOCR-VL 论文 ×2 + NVIDIA H100 PCIe/NVL PB + 小米手环 9 手册 |
| 人工 PDF | 2 | 昆仑芯 K100/K200 PB（主题贴合文心赛道）+ GB/T 2423.1-2008（扫描+文字层混合）|
| OmniDocBench | 标注 + 20 页 | HF `opendatalab/OmniDocBench` |

落地代码：`openvino/scripts/{download_eval_materials,run_omnidocbench_subset}.py` + `openvino/data/eval_questions.jsonl`（18 题 + schema）。

### 1.6 pdfplumber bbox 排序修复

W1 末实测时发现：表格 chunk 的 `section_title` 跟随页末标题（不是真正所属章节）。原因：`_extract_text_pages` 把 `page.extract_text()` 全部文字摆前面，所有 `extract_tables()` 结果统一附在页末，下游 chunker 给表格分配的章节自然错位。

修复（commit [`54e2fb2`](https://github.com/bob798/doc-qna-openvino/commit/54e2fb2)）：改用 `page.find_tables()` 拿 bbox，按 y 坐标交错拼接 **[上方文本, 表格 md, 表格之间文本, ...]**。2026-05-12 在 `spec_with_tables.pdf` 上回归验证：表格行 chunk 的 `section_title="主要参数"`（修复前是页末 `故障代码`），切片数稳定为 7 / 含 3 表行 + 1 表头。

---

## 2. 待办（W2 剩余）

按 [项目计划.md](../项目计划.md) 推进 Phase 3：

1. **Phase 3.1 · Embedding + 向量库**
   - 准备 BGE-small-zh 的 OpenVINO IR（INT8）
   - 接 ChromaDB（持久化），Phase 2 输出的 chunks.jsonl 一键灌入
   - 验证检索：用 5 条业务问题 × top-k=5，人工判定召回的 chunk 是否相关
2. **Phase 3.2 · LLM 生成（Qwen3-1.7B INT4）**
   - 使用 `openvino_genai.LLMPipeline` 加载 Qwen3-1.7B INT4 IR（HF `OpenVINO/Qwen3-1.7B-int4-ov` 现成），RAG 场景关 thinking（`enable_thinking=False`）
   - 设计 prompt 模板：`{system + retrieved_chunks + question}` → 带来源引用的回答
3. **Phase 3.3 · 端到端最小可运行链路**
   - `scripts/run_qa.py`：PDF → 解析 → 入库 → 提问 → 答案 + 来源
   - 跑通 5 条问题，记录耗时分解（embed / retrieve / LLM）

---

## 3. 风险与待办（非阻塞）

| 项 | 影响 | 状态 |
|----|------|------|
| 合成扫描图（`scanned.pdf`、`text_01.png`）PaddleOCR-VL 严重漏识别 | Phase 2 OCR 路径 chunk 数偏低；Phase 1 `text_01` 仅输出 14 字符 | ✅ W2 用 GB/T 2423.1-2008 真实扫描件复测：14 页全 OCR 路径，**切出 87 chunks（1 表头 + 6 表行 + 80 文本）**，约 22 s/页 CPU。原始数据：`openvino/results/phase2/gb_t_2423_1.{markdown,chunks.jsonl,summary.json}` |
| pdfplumber 表格 `section_title` 错位 | 表格 chunk 的 section 元数据可能与 PDF 实际位置不一致 | ✅ W2 修复，详见 §1.6 |
| PyTorch baseline 未跑 | Benchmark 1 暂无加速比 | ⚪ 弃测（详见 §1.1 脚注）；改以 OV CPU/GPU/NPU 三档内部对照 |
| OV NPU 数据未跑 | 三档对照缺第三档 | W3 第一晚补 `--device NPU` 一次跑完 |

---

## 4. 关键链接

- 仓库：https://github.com/bob798/doc-qna-openvino
- 子项目：[`openvino/README.md`](../../openvino/README.md)
- W1 周报存档：[`W1_2026-05-08.md`](W1_2026-05-08.md)
- W1 PFCCLab 提交：[PFCCLab/Camp #598](https://github.com/PFCCLab/Camp/pull/598)
