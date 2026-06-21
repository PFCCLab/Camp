### 认领者 GitHub ID

bob798

### 赛题信息

- **进阶任务序号**：#13
- **赛题名称**：基于 OpenVINO 的多模态文档理解与智能应用开发
- **关联厂商**：Intel

---

### 本周工作

> 报告周期：2026-05-09 ~ 2026-05-22（与 W1 衔接的第二个双周）

1. **Phase 1 实测数据落地：OpenVINO CPU + GPU 推理 Benchmark 跑通**

   IR 路径选用 ModelScope `zhaohb/PaddleOCR-VL-1.5-ov` 拆分布局（INT4 LLM + INT8 Vision + PP-DoclayoutV3 layout detector），免去自行 export，规避 optimum 不支持 PaddleOCR-VL 的问题。`openvino/src/inference.py` 实现 `split` / `vlmpipeline` 双布局自动识别。

   10 张测试图（公式/纯文字/表格/图文混排各 2-3 张）× 1 warmup + 3 runs：

   | 类型 | OV CPU 范围 (ms) | OV GPU 范围 (ms) |
   |------|------------------|------------------|
   | 公式 | 1137 – 1976 | 560 – 930 |
   | 纯文字 | 1323 – 4344 | 637 – 2573 |
   | 表格 | 3310 – 3621 | 2325 – 2518 |
   | 图文混排 | 3044 – 4373 | 2162 – 4027 |

   **全图均值：OV CPU 2948 ms / OV GPU 2003 ms（GPU/CPU 加速 1.47×）**。NPU 数据下个双周补。

   原始数据：`openvino/results/phase1/benchmark_inference.cpu.{md,json}` + `openvino/results/phase1/gpu/benchmark_inference.{md,json}`。

   PyTorch FP32 基线被弃测：HF 远端 `modeling_paddleocr_vl.py` 在 torch 2.11.0+cpu 上单图 32 max_new_tokens ≈ 360 s，按默认 2048 token × 10 张 × 3 runs 推算需 ~15 hr，单机不可行；同时 IR 已自带 INT4 + INT8 量化，"OV vs PT" 实质混合了"框架 + 量化"两个变量。改以 OV CPU/GPU/NPU 三档内部对照（Intel AI PC 全家桶视角），对 Intel + 百度评委更直接。

   期间发现并修了 PyTorch 路径上的两个真实坑（即使本期弃测，留给未来使用）：
   - 处理器调用缺 chat template → 用 `apply_chat_template` 注入 `<|IMAGE_START|><|IMAGE_PLACEHOLDER|><|IMAGE_END|>`
   - transformers 4.54 把 `create_causal_mask(inputs_embeds=...)` 重命名为 `input_embeds=...`，HF 远端代码未跟进 → 本地 monkey-patch 缓存的 modeling 文件

2. **Phase 2 切片器实战修复（3 处真实漏洞）**

   实测过程暴露切片器在真实文档上的三个漏洞，全部修复并验证：

   | 修复 | Commit | 影响 |
   |------|--------|------|
   | chunker 支持 HTML 表格 | [`7a097a7`](https://github.com/bob798/doc-qna-openvino/commit/7a097a7) | PaddleOCR-VL 输出 `<table>...</table>` HTML，原 chunker 仅识别 `\|...\|` 管道表格，所有表格漏切；新增 `_HTMLTableToRows` + `_normalize_html_tables` 把 HTML 表格就地转 Markdown |
   | pdf_preprocessor 文字层路径补表格 | [`f20a2a3`](https://github.com/bob798/doc-qna-openvino/commit/f20a2a3) | text-layer 路径只用 `extract_text()`，pdfplumber 把表格吐成平铺串；新增 `extract_tables()` 输出 Markdown 表格 |
   | pdfplumber bbox 排序修复 | [`54e2fb2`](https://github.com/bob798/doc-qna-openvino/commit/54e2fb2) | `_extract_text_pages` 把文字摆前面、表格统一附在页末，导致表格 chunk 的 `section_title` 跟随页末标题；改用 `page.find_tables()` 拿 bbox，按 y 坐标交错拼接 |

   在 `spec_with_tables.pdf` 上回归验证：表格行 chunk 的 `section_title = "主要参数"`（修复前是页末 `故障代码`），切片数稳定为 7（3 表行 + 1 表头 + 3 文本）。

3. **真实扫描件复测：GB/T 2423.1-2008 中文国标 14 页**

   W1 用合成 `scanned.pdf` 仅产出 1 chunk，是工程占位；本期下载 [GB/T 2423.1-2008《环境试验·低温试验方法》](https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=4B30041DEFB4D9283C1DC9592735F67E)（1.7 MB / 14 页，扫描+文字层混合）跑全 OCR 路径：

   ```
   14 页 → 87 chunks（1 table_header + 6 table + 80 text）
   总耗时 309 s（约 22 s/页 CPU OCR）
   ```

   证明 PaddleOCR-VL OCR 路径在真实中文国标上能正确切出表格结构（7 个表行 chunk 均带表头进入向量库），满足 §三 表格感知切片设计要求。原始数据：`openvino/results/phase2/gb_t_2423_1.{markdown,chunks.jsonl,summary.json}`。

4. **Phase 3 评测体系三层证据架构定稿**

   把 Phase 4 评测从"主观对比"升级为可量化、可复现的三层证据（详见 [`docs/进阶方案.md` §七](https://github.com/bob798/doc-qna-openvino/blob/main/docs/进阶方案.md)）：

   | 层 | 内容 | 指标 |
   |---|------|------|
   | ① 客观对照 | OmniDocBench (CVPR 2025) 子集 20 页 × {Tesseract, PaddleOCR-VL} | Edit Distance / TEDS / CDM |
   | ② 业务场景 | 自建 18 题（Phase 3.3 跑通后扩 30~50 题），5 类分布参考 MMLongBench-Doc | keyword_match / must_refuse / manual_rubric |
   | ③ 自动评测 | RAGAS | faithfulness / answer_relevancy / context_precision / context_recall |

   评测材料 27 件已就位：5 份直链 PDF + 2 份人工 PDF（K100/K200 PB + GB/T 2423.1） + OmniDocBench 标注 + 20 张采样图。落地代码：`openvino/scripts/{download_eval_materials,run_omnidocbench_subset}.py` + `openvino/data/eval_questions.jsonl`（18 题 + schema）。

5. **LLM 选型升级：Qwen2.5 → Qwen3-1.7B INT4**

   W1 原计划 Qwen2.5-1.5B。Qwen3（2025-04 发布）现已成熟：
   - OpenVINO GenAI 原生支持 `Qwen3ForCausalLM`（>= 2025.2）
   - 现成 IR：HF `OpenVINO/Qwen3-1.7B-int4-ov` 直接拉
   - RAG 场景 `enable_thinking=False` 关思考模式
   - 替换成本：换 `model_id` 字符串 + chat_template（Qwen3 默认正确）

   `docs/进阶方案.md` §四、`docs/项目计划.md`、`docs/开发手册.md`、`README.md` 已同步。

6. **问题与解决**

   - 问题：合成扫描图（W1 `scanned.pdf`、`text_01.png`）PaddleOCR-VL 严重漏识别（合成图风格不像真实扫描）？
     解决：✅ 本期用 GB/T 2423.1-2008 真实国标 14 页复测，全 OCR 路径产 87 chunks，OCR 路径证据已立。

   - 问题：pdfplumber 文字层路径表格的 `section_title` 错位到页末标题？
     解决：✅ commit [`54e2fb2`](https://github.com/bob798/doc-qna-openvino/commit/54e2fb2) 改用 `find_tables()` + bbox y 坐标交错拼接。

   - 问题：PyTorch FP32 CPU 单图 360s 无法跑全套 benchmark？
     解决：✅ 弃测并书面说明（IR 已 INT4/INT8 量化，OV vs PT 不是单变量对照）；改以 OV CPU/GPU/NPU 三档内部对照。本期跑完 CPU + GPU，NPU 下个双周补。

   - 问题：HF 远端 `modeling_paddleocr_vl.py` 对 transformers 4.54 不兼容（`inputs_embeds` 旧参数名）？
     解决：本地 monkey-patch 缓存文件，正式 issue 待提 PaddlePaddle 团队。

---

### 下周计划

> 报告周期：2026-05-23 ~ 2026-06-05（最后一个完整双周，6/5 比赛截止）

1. **OV NPU 数据补齐**：`scripts/benchmark_inference.py --device NPU` 跑一次，完成 CPU/GPU/NPU 三档对照表。同时把 §五"实测"列从两档补到三档。
2. **Phase 3.1 · Embedding + 向量库**：BGE-small-zh 转 OpenVINO IR（INT8）→ ChromaDB 持久化 → Phase 2 输出的 chunks.jsonl 灌入 → 5 条业务问题人工验证 Top-K 召回相关性。
3. **Phase 3.2 · LLM 生成（Qwen3-1.7B INT4）**：用 `openvino_genai.LLMPipeline` 加载现成 IR，RAG prompt 模板设计 + 输出带 (doc_name, page) 引用。
4. **Phase 3.3 · 端到端最小可运行链路**：`scripts/run_qa.py` 完整 PDF → 解析 → 入库 → 提问 → 答案，跑 5 条问题记录耗时分解（embed / retrieve / LLM）。
5. **Phase 4 评测启动**：OmniDocBench 子集跑 Tesseract vs PaddleOCR-VL Edit Distance / TEDS / CDM；业务集扩到 30 题并跑 RAGAS。
6. **Notebook 整理 + Gradio 演示**（若时间允许）：把 §七.4 演示叙事顺序编排为一份 Notebook + Gradio 上传交互界面。

---

### 当前阻塞（无则填"无"）

- **OV NPU 路径未验证**：本期受时间限制只跑了 CPU + GPU，NPU 是否能加载 INT4 LLM + INT8 Vision 的 split 布局未验证。若 NPU 不能跑完整 IR，需要 HETERO:NPU,CPU 兜底；下个双周第一晚先跑通。
- **PaddleOCR-VL HF 远端代码与 transformers 4.54 兼容性问题**：`inputs_embeds` → `input_embeds` 重命名未跟进，本地 monkey-patch 可工作但不可移植。已记录为 issue 准备提给 PaddlePaddle 团队，不阻塞本项目（OV 路径不依赖远端 PT 代码）。

---

### 交付物进展

| 交付物 | 状态 | 备注 |
|--------|:----:|------|
| Phase 1 推理 Benchmark | ✅ | OV CPU + GPU 实测落地；NPU 下个双周补。原始数据：`openvino/results/phase1/` |
| Phase 2 文档解析 + 切片 | ✅ | 3 处切片器漏洞修复 + 真实扫描件 14 页验证 87 chunks |
| Phase 3 RAG 链路 | 🔄 | 评测体系三层架构 + 材料 27 件已就位；Embedding/向量库/LLM 下个双周实现 |
| Phase 4 对比评测 | 🔄 | OmniDocBench 子集 + 自建 18 题 + RAGAS 框架定稿；执行下个双周 |
| Phase 5 Notebook + README + 提交 | ⬜ | 计划 W7（6/2 ~ 6/5） |
| 代码实现 | 🔄 | https://github.com/bob798/doc-qna-openvino |
| README | 🔄 | 顶层 README + `openvino/README.md` 已写；最终交付前回填实测数字 |
| 演示视频/截图 | ⬜ | Phase 3 端到端跑通后录制 |

---

### 关键链接

- 项目仓库：https://github.com/bob798/doc-qna-openvino
- W1 周报：[PFCCLab/Camp#598](https://github.com/PFCCLab/Camp/pull/598)
- 进阶方案：[`docs/进阶方案.md`](https://github.com/bob798/doc-qna-openvino/blob/main/docs/进阶方案.md)
- Phase 1 结果：[`openvino/results/phase1/benchmark_inference.cpu.md`](https://github.com/bob798/doc-qna-openvino/blob/main/openvino/results/phase1/) (gitignored，仓库说明可复现)
