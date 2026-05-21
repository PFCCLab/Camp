### 认领者 GitHub ID

bob798

### 赛题信息

- **进阶任务序号**：#13
- **赛题名称**：基于 OpenVINO 的多模态文档理解与智能应用开发
- **关联厂商**：Intel

---

### 本周工作

> 报告周期：2026-05-23 ~ 2026-06-05（最后一个完整双周，6/5 比赛截止）
> **方向校准延续**：W2 末收到导师反馈（见 [`docs/决策记录/2026-05-22_导师反馈方向校准.md`](https://github.com/bob798/doc-qna-openvino/blob/main/docs/决策记录/2026-05-22_导师反馈方向校准.md)），W3 收敛到端到端 Demo 主线；本期主要目标是把"提问→检索→带引用回答"的最小闭环跑通并落地可复现物料，评测体系扩张和 NPU 全链路验证按计划降为加分项。

1. **Phase 3 RAG 端到端最小闭环跑通**

   端到端链路：`PDF → PaddleOCR-VL 解析 → 表格感知切片 → Qwen3-Embedding-0.6B-int8 编码 → ChromaDB 持久化 → 提问 → Top-K 检索 → Qwen3-1.7B-int4 生成带 [doc_name p.页码] 引用的回答`。

   新增模块（`openvino/src/`，单 commit [`1851491`](https://github.com/bob798/doc-qna-openvino/commit/1851491) 落地）：

   | 模块 | 职责 | 关键设计 |
   |------|------|----------|
   | `embedding.py` | Qwen3-Embedding-0.6B-int8 OpenVINO 封装 | 直接 `openvino.Core.compile_model`，避免 optimum-intel 重依赖；last-token-pool + L2 normalize 对齐官方推荐 |
   | `vector_store.py` | ChromaDB Persistent 封装 | cosine 距离，按 `doc_name` 维护 id，支持 `where` 过滤；元数据自动 flatten 规避 Chroma 标量限制 |
   | `llm.py` | Qwen3-1.7B-int4 LLMPipeline 封装 | `enable_thinking=False` + 用户消息追加 `/no_think` 双保险；`<think>` 块后处理剥离支持「真闭合」「模板预填截断」「真实截断」三种形态 |
   | `rag.py` | embedder + store + LLM 编排 | Prompt 强制 `[doc_name p.页码]` 引用 + 抗幻觉拒答；context 拼接控制总长 3500 字符避免爆 LLM context |

   配套脚本：
   - `scripts/build_index.py` ——`results/phase2/*.chunks.jsonl` 灌入 ChromaDB
   - `scripts/run_qa.py` —— 端到端 QA Demo，支持 `--question` / `--questions_file` / `--eval_jsonl --question_ids` 三种问题来源，输出 JSON + Markdown 报告

2. **Embedding 模型选型决策：BGE-small-zh → Qwen3-Embedding-0.6B-int8-ov**

   原计划用 BAAI/bge-small-zh-v1.5 转 OV IR。实测 `huggingface.co/OpenVINO/` 官方仓库未提供该模型的预转 INT8 IR（只有英文版 `bge-base-en-v1.5-int8-ov`）；自行用 optimum-intel 转换会引入重依赖且转换正确性需独立验证。

   决策：换用 `OpenVINO/Qwen3-Embedding-0.6B-int8-ov`——官方预转 INT8 IR、多语言含中文、与 LLM 同源（Qwen3 系列）便于版本对齐。该决策保持了 Phase 1/2/3 "全程使用官方预转 IR" 的复现性原则。BGE 路径在 `openvino/README.md` 留出 `--embed_local_dir` 入口，用户想坚持 BGE 可用 optimum-intel 自行转换接入。

3. **Phase 3 实测：5 条业务问题 CPU 端跑通**

   demo 集 `data/demo_questions.txt`（5 题，打在 Phase 2 已切的 4 份 PDF / 99 chunks 上）：

   | # | 问题 | 结果 | 评注 |
   |---|------|------|------|
   | 1 | A100 型号的工作温度范围是多少？ | `-20~70℃ [spec_with_tables p.1]` | ✅ 表格事实正确 |
   | 2 | A300 型号的额定功率是多少瓦？ | `500W [spec_with_tables p.1]` | ✅ 表格事实正确 |
   | 3 | 故障代码 E01 或 E02 出现时应该如何处理？ | "文档中未提及处理方法" | ⚠️ 保守拒答（原文"联系售后"被判为不构成方法）——抗幻觉的取舍 |
   | 4 | GB/T 2423.1—2008 这份标准对应的国际标准编号是多少？ | `IEC 60068-2-1:2007 [gb_t_2423_1 p.3]` | ✅ 多页事实正确 |
   | 5 | GB/T 2423.1—2008 标准的实施日期是哪一天？ | "文档中未提及实施日期" | ✅ 正确拒答（含 "2009-10-01 实施" 的 chunk 因英文标题占主导未进 Top-5，模型未编造） |

   性能（CPU，Qwen3-Embedding-0.6B-int8 + Qwen3-1.7B-int4 + Chroma cosine）：

   | 阶段 | 平均耗时 (ms) |
   |------|--------------:|
   | embed query | 69 |
   | ChromaDB retrieve | 1.7 |
   | LLM 生成 | 3270 |
   | **end-to-end / 题** | **3340** |
   | LLM 吞吐 | ~10.7 tok/s |

   原始数据：`openvino/results/phase3/qa_run.{json,md}`（脚本生成，`.gitignore` 跟踪）。

4. **三处工程坑实战修复（W3 期间暴露并解决）**

   | 坑 | 现象 | 修复 |
   |----|------|------|
   | Windows 控制台 cp1252 编码 | `print` 中文直接 `UnicodeEncodeError` 崩溃 | `scripts/run_qa.py` 和 `build_index.py` 入口处 `sys.stdout.reconfigure(encoding='utf-8')` |
   | huggingface_hub symlink 权限 | 非管理员模式下载报 `WinError 1314 A required privilege is not held` | README 显式提示 `$env:HF_HUB_DISABLE_SYMLINKS=1`（开发者模式之外的兜底方案） |
   | Qwen3 `enable_thinking=False` 不生效 | 模板正确预填 `<think></think>`，但模型仍自发输出新 `<think>...</think>`，长 prompt 下会吃光 max_new_tokens 留下空答案 | 双保险：用户消息末追加 `/no_think` + 输出后 `strip_thinking` 处理三种形态（完整闭合 / 模板预填后接答案 / 真实截断） |

   后两个坑是 OpenVINO + Qwen3 + Windows 真实部署链路上**很容易踩**的坑，单独在 README 里写了一段 "Windows 启动前请先设置环境变量"，避免下游用户重复踩。

5. **README + 复现物料同步落地（不拖到 W5）**

   `openvino/README.md` 新增 Phase 3 章节：模型选型表 + 一次性环境变量准备 + 灌库命令 + 端到端问答命令 + Demo 输出示例表 + 性能数据 + 已知限制（Q3 风格保守拒答 / Q5 风格 retrieval miss）。

   独立"Phase 3 NPU 限制说明"段（呼应 W2 → W3 方向校准），明确主线 CPU/GPU/AUTO 的三条理由：① PP-DocLayoutV3 含 NPU 未覆盖算子 ② Qwen3 在 NPU 上的 dynamic-shape 支持仍不全 ③ NPU 路径放在 W4 加分项里专门试，时间不够就砍。

6. **问题与解决**

   - 问题：BGE-small-zh-v1.5 在 OpenVINO 官方仓库无预转 INT8 IR，是否要自行用 optimum-intel 转？
     解决：✅ 改用 `OpenVINO/Qwen3-Embedding-0.6B-int8-ov`（官方预转 + 多语言含中文 + 与 LLM 同源），保持 "全程官方 IR" 复现性原则。

   - 问题：Q5 风格的 retrieval miss——含目标事实的 chunk 因其他主题（英文标题、章节名）"语义稀释"被排在 Top-10 之外？
     解决：⚠️ 部分缓解。增加 `--top_k` 到 12 仍未召回，根因是 last-token-pool 在端拼 "2009-10-01 实施" 的 chunk 上仍被前部英文标题主导。W4 加分项内试 BGE-reranker-base 重排候选；当前版本依赖严格 system prompt 让模型正确拒答而不是编造。

   - 问题：Qwen3 在严格 prompt 下对短答案过度拒答（Q3 风格——原文"联系售后"被判为不构成完整方法）？
     解决：☑ 接受取舍。试过软化 prompt（允许"忠实复述原文事实"），代价是 Q5 风格 retrieval miss 转为幻觉日期。最终保留严格 prompt，README 已写明这是抗幻觉的代价。

---

### 下周计划

> 报告周期：2026-05-30 ~ 2026-06-05（W4，最后一周，6/5 比赛截止前最后冲刺）

**主线（必做，P0）— 最终交付物**

1. **P1-1 业务问题精选**（W3 收尾溢出）：从 `eval_questions.jsonl` 18 题里挑 3~5 题最能说明效果的，对 `data/eval_documents/` 真实评测 PDF 跑 Phase 2 → 灌库 → 跑 run_qa，把 Demo 主证据从 W3 的"已有 4 份 PDF" 升级到"业务真实评测 PDF"。
2. **P1-2 Tesseract vs PaddleOCR-VL 少量页对比**：选 2~3 个代表性页面（含表格 + 中文 + 公式），人工或脚本对比识别质量，不跑完整 OmniDocBench。
3. **演示视频/录屏（2~3 分钟）**：terminal 跑通端到端 + 回答带引用 + 性能输出截图。
4. **README 终稿 + 依赖说明 + 模型准备**：确保 PR 一键复现，特别核对 Windows 环境变量段、IR 下载量、磁盘需求。
5. **提交 PR 到 PFCCLab 仓库**：6/5 前最晚 6/4 提交，预留半天 review 反馈窗口。

**加分项（P2-P3，时间不够直接砍）**

6. **NPU 进取路径**：试把 Qwen3 LLM 或 Embedding 切到 NPU（NPU 明确支持的 workload），讲 "OCR-GPU / LLM-NPU / 检索-CPU" AI PC 全家桶叙事。
7. **OmniDocBench 子集** Edit Distance / TEDS / CDM、**RAGAS** faithfulness / answer_relevancy、**业务题扩到 30~50**、**Gradio UI**。

---

### 当前阻塞（无则填"无"）

- **NPU 全链路不可行（沿用 W2 阻塞，方向已明确）**：导师反馈指出 NPU 当前仅支持 PP-DocLayoutV2，本项目所用 IR `zhaohb/PaddleOCR-VL-1.5-ov` 含 PP-DocLayoutV3 算子，NPU 暂无法跑完整 OCR 链路。主线已收敛到 CPU/GPU/AUTO；W4 加分项里探索把 LLM/Embedding 这类 NPU 明确支持的 workload 切上去做 AI PC 全家桶叙事，时间不够就砍。
- 其余无阻塞。

---

### 交付物进展

| 交付物 | 状态 | 备注 |
|--------|:----:|------|
| Phase 1 推理 Benchmark | ✅ | OV CPU + GPU 实测落地（GPU/CPU 1.47×）；NPU 限制说明已写明 |
| Phase 2 文档解析 + 切片 | ✅ | 3 处切片器漏洞修复 + GB/T 2423.1 真实国标 14 页 87 chunks |
| **Phase 3 RAG 链路** | **✅ 本期完成** | **Embedder + ChromaDB + LLM 全链路跑通，5 题 CPU 端 ~3.3 s/题，带 `[doc p.页]` 引用** |
| Phase 4 对比评测 | 🔄 | W4 主线：业务题精选 + Tesseract vs PaddleOCR-VL 少量页对比；加分项：OmniDocBench/RAGAS 时间允许再上 |
| Phase 5 Notebook + README + 提交 | 🔄 | README 顶层 + `openvino/README.md` Phase 3 章节已落地；W4 终稿 + 演示视频 + PR 提交 |
| 代码实现 | 🔄 | https://github.com/bob798/doc-qna-openvino（W3 commit [`1851491`](https://github.com/bob798/doc-qna-openvino/commit/1851491)） |
| README | 🔄 | 顶层 + `openvino/README.md` Phase 3 完成；W4 加 Tesseract 对比章节 + 终稿 |
| 演示视频/截图 | ⬜ | W4 录制，端到端 terminal + 引用回答 + 性能数据 |

---

### 关键链接

- 项目仓库：https://github.com/bob798/doc-qna-openvino
- W1 周报：[PFCCLab/Camp#598](https://github.com/PFCCLab/Camp/pull/598)
- W2 周报：[PFCCLab/Camp#609](https://github.com/PFCCLab/Camp/pull/609)
- 进阶方案：[`docs/进阶方案.md`](https://github.com/bob798/doc-qna-openvino/blob/main/docs/进阶方案.md)
- Phase 3 模块：[`openvino/src/{embedding,vector_store,llm,rag}.py`](https://github.com/bob798/doc-qna-openvino/tree/main/openvino/src) + [`openvino/scripts/{build_index,run_qa}.py`](https://github.com/bob798/doc-qna-openvino/tree/main/openvino/scripts)
- Phase 3 运行手册：[`openvino/README.md` § Phase 3](https://github.com/bob798/doc-qna-openvino/blob/main/openvino/README.md)
- W2→W3 方向校准：[`docs/决策记录/2026-05-22_导师反馈方向校准.md`](https://github.com/bob798/doc-qna-openvino/blob/main/docs/决策记录/2026-05-22_导师反馈方向校准.md)
