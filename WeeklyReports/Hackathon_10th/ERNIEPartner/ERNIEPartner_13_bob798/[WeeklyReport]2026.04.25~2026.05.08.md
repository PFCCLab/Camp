### 认领者 GitHub ID
bob798

### 赛题信息
- **进阶任务序号**：#13
- **赛题名称**：基于 OpenVINO 的多模态文档理解与智能应用开发
- **关联厂商**：Intel

### 本周工作

1. **项目脚手架与开发计划**
   - 整理项目仓库 [`bob798/doc-qna-openvino`](https://github.com/bob798/doc-qna-openvino)，确定方案：基于 PaddleOCR-VL + OpenVINO 的产品文档智能入库与客服问答系统
   - 编写按 Phase 1~5 拆周推进的项目计划（对齐 6/5 截止日期）和实践方案执行手册（逐 Phase 列明目标、步骤与验证标准）
   - 相关 PR/Issue 链接：
     - 项目计划：https://github.com/bob798/doc-qna-openvino/blob/main/docs/项目计划.md
     - 执行手册：https://github.com/bob798/doc-qna-openvino/blob/main/docs/开发手册.md

2. **Phase 1：环境搭建与模型验证**
   - OpenVINO 2025.4.1 环境搭建完成（openvino / openvino-genai / openvino-tokenizers）
   - PaddleOCR-VL 0.9B OpenVINO 推理跑通，输出结构化 Markdown
   - 完成 PyTorch vs OpenVINO 速度 Benchmark 脚本：支持 warmup + N 次取均值，输出 markdown 表 + json
   - 完成 Tesseract vs PaddleOCR-VL 解析质量对比脚本：并排展示、字符相似度、人工评分表模板
   - 相关 PR/Issue 链接：
     - https://github.com/bob798/doc-qna-openvino/blob/main/openvino/scripts/benchmark_inference.py
     - https://github.com/bob798/doc-qna-openvino/blob/main/openvino/scripts/benchmark_ocr_quality.py

3. **Phase 2：文档解析与切片模块（提前启动）**
   - PDF 预处理：pdfplumber 文字层抽取 + 命中率判断（≥90% 走文字层），未命中页用 pypdfium2 渲染（自带二进制，免装 poppler）
   - 文档解析：复用文字层 / 调用 PaddleOCR-VL 全图 prompt → 结构化 Markdown，按页携带 source 元信息
   - 表格感知切片：Markdown 表格识别（`|...|` + 分隔符）→ 表头 + 单行 chunk；非表格按段落切 200~500 字符，超长保留 50 字符 overlap
   - 端到端管线 + CLI：PDF → 预处理 → 解析 → 切片 → JSONL，元数据 `{doc_name, page, section_title, kind}`
   - 本地烟囱测试通过：
     - `chunker` 在合成 markdown 上输出 7 个分类正确的 chunk（3 文本 + 1 表头 + 2 表格行 + 1 尾部章节，元数据完整）
     - `preprocess_pdf` 对 3 份测试 PDF 的判定符合预期：`text_pdf` mode=mixed，`scanned` mode=ocr，`spec_with_tables` mode=text
   - 相关 PR/Issue 链接：
     - https://github.com/bob798/doc-qna-openvino/tree/main/openvino/src
     - https://github.com/bob798/doc-qna-openvino/blob/main/openvino/scripts/run_phase2_pipeline.py

4. **问题与解决**
   - 问题：PaddleOCR-VL 在官方 optimum 导出器中暂未原生支持，无法直接用 `optimum-cli export openvino` 一键转换？
     解决：调研后确定备选两条路径——(a) 从 ModelScope 下载 `zhaohb/PaddleOCR-VL-1.5-ov` 预转 IR（约 940MB，INT4 LLM + INT8 Vision + DocLayout）；(b) 通过社区 `paddleocr_vl_openvino` wheel 自行转换。下周一锁定具体路径
   - 问题：ModelScope 预转 IR 采用拆分布局（`llm_stateful_int4` / `vision_int8` / `vision_mlp` 等），与 `openvino_genai.VLMPipeline` 默认期望文件名不兼容？
     解决：计划在 `src/inference.py` 增加适配层，自动识别两种 IR 布局
   - 问题：真实业务 PDF 样本暂未到位，Phase 2 验证目前用合成样本，覆盖度不足？
     解决：下周补齐 3 份真实文档（说明书、规格书、扫描件）替换合成样本

### 下周计划

1. **IR 落地**（解封 Phase 1 实测数据）：周一锁定 IR 来源后跑通 `benchmark_inference.py` 与 `benchmark_ocr_quality.py`，将实测均值替换 `docs/进阶方案.md` 中的 "≥ 2×" / 解析准确率预估值
2. **Phase 2 真实样本验证**：用 3 份真实业务 PDF 替换合成样本，重跑 `run_phase2_pipeline.py`，人工抽检表格 chunk 完整性、段落切分合理性、元数据准确性
3. **Phase 3 启动**：BGE-small 转 OpenVINO IR + ChromaDB 入库；设计 prompt 模板，跑通"问题 → 检索 → LLM 回答 + 来源引用"端到端最小链路

### 当前阻塞（无则填"无"）

- PaddleOCR-VL 的 OpenVINO IR 落地路径：官方 optimum 导出器暂不支持，社区路径在 IR 文件布局上与 `openvino_genai.VLMPipeline` 默认期望不一致。已规划适配层方案，下周内闭环

### 交付物进展

| 交付物 | 状态 | 备注 |
|--------|:----:|------|
| RFC 文档 | ✅ 已完成 | 进阶方案：[`docs/进阶方案.md`](https://github.com/bob798/doc-qna-openvino/blob/main/docs/进阶方案.md)；项目计划：[`docs/项目计划.md`](https://github.com/bob798/doc-qna-openvino/blob/main/docs/项目计划.md)；执行手册：[`docs/开发手册.md`](https://github.com/bob798/doc-qna-openvino/blob/main/docs/开发手册.md) |
| 代码实现 | 🔄 进行中 | Phase 1 + Phase 2 代码已完成，本地烟囱测试通过；推理 Benchmark 实测数据待 IR 落地后补齐。仓库：https://github.com/bob798/doc-qna-openvino |
| README | 🔄 进行中 | 子项目 [`openvino/README.md`](https://github.com/bob798/doc-qna-openvino/blob/main/openvino/README.md) 含 Phase 1+2 运行指南；最终交付前会再做整理 |
| 演示视频/截图 | ⬜ 未开始 | 计划在 IR 落地、Phase 3 端到端跑通后录制 |
