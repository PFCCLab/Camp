### 姓名

PrayerQX

### 实习项目

基于PaddleOCR在大模型GEO的优化

### 本周工作

1. 完成 PaddleOCR-VL-1.5 与 PP-StructureV3 的本地部署验证

   - 基于 PaddleOCR 官方命令行入口完成 `PaddleOCR-VL-1.5` 的本地 smoke test，核心调用方式为 `paddleocr doc_parser --pipeline_version v1.5`。
   - 统一设置模型缓存目录，避免 Hugging Face、Paddle、Torch 等缓存落到中文路径，降低 Windows 本地环境下的下载和运行风险。
   - 接入 `PP-StructureV3`，完成同一套 lite benchmark 数据集上的推理、标准化和评分流程。
   - 在仓库中整理部署说明和对比文档，方便后续复现。

2. 搭建并完善 PaddleOCR 相关文档解析 benchmark 仓库

   - 整理并发布 `doc-parsing-benchmark` 仓库，用于对 `PaddleOCR-VL-1.5`、`PP-StructureV3`、`MinerU`、`HunyuanOCR`、`MonkeyOCR` 等模型进行统一评测。
   - 设计统一输出格式，所有模型最终落成 `result.md`、`result.json`、`meta.json`，便于后续接入 official scorer 和汇总榜单。
   - 接入 `OmniDocBench` 和 `MDPBench` 两个数据集，并提供 full、resilient、lite 三套 benchmark profile。
   - 针对本机资源限制，构建 `OmniDocBench 80 页 + MDPBench 24 页` 的 lite 分层抽样方案，用于快速对比不同模型的效果和稳定性。

3. 完成 PaddleOCR-VL-1.5 与主流文档解析模型的 lite benchmark 对比

   - 在 lite 数据集上完成 `PaddleOCR-VL-1.5`、`PP-StructureV3`、`MinerU`、`HunyuanOCR`、`MonkeyOCR` 的统一推理、格式化、评分和 leaderboard 汇总。
   - 当前本机 lite 结果显示，`PaddleOCR-VL-1.5` 在两个数据集上都保持较强综合表现，尤其在跨数据集稳定性方面更适合作为默认主通道候选。
   - `HunyuanOCR` 在 `OmniDocBench Lite` 上表现最好，但在 `MDPBench Lite` 上波动较大。
   - `MinerU` 工程系统能力较强，但本次 lite 分数略低于 `PaddleOCR-VL-1.5`。
   - `PP-StructureV3` 在 `MDPBench Lite` 中排名第二，并且在 `OmniDocBench Lite` 上速度表现较好。

4. 修正 MonkeyOCR 接入方式并更新 benchmark 数据

   - 排查发现早期 `MonkeyOCR` 接入时仅使用 text-only 模式，导致表格结构没有进入统一评分流程，`Table TEDS` 被低估。
   - 将 `MonkeyOCR` runner 改为完整 parse 输出，并在标准化阶段读取 `content_list.json`，补齐 table、formula、text block 等结构化内容。
   - 重跑 `MonkeyOCR` 的 lite benchmark 后，`OmniDocBench Lite` 的 `Table TEDS` 从 `0.0000` 提升到 `0.8996`，`rank_score` 从 `0.4620` 提升到 `0.8818`。
   - 更新 GitHub 仓库 README 和对比文档，避免继续传播错误的旧分数。

5. 整理 PaddleOCR 相关文章和项目文档

   - 编写 `PaddleOCR-VL-1.5` 与 `PP-StructureV3` 的部署和实测对比文档，内容包括部署命令、飞桨官方资料、lite benchmark 结果、优缺点和适用场景。
   - 编写 `PaddleOCR-VL-1.5` 对比 `MinerU`、`HunyuanOCR`、`MonkeyOCR` 等主流工具的文档，重点分析 PDF 转 Markdown 在 RAG、知识库和文档解析场景中的选型逻辑。
   - 围绕 PaddleOCR 相关工作共整理三篇文章，分别覆盖 `PaddleOCR-VL-1.5` 部署、`PP-StructureV3` 对比、以及主流文档解析模型选型分析。
   - 完善 GitHub 主页和项目 README，使 `doc-parsing-benchmark`、`PPStructureV3-PDF-to-Markdown` 等 PaddleOCR 相关内容更容易被查看和复现。

6. 问题疑惑与解答

   - 问题：`PaddleOCR-VL-1.5` 和 `PP-StructureV3` 是否需要完全不同的部署环境？
   - 解答：两者都属于 PaddleOCR 体系，可以共用 `PaddlePaddle + PaddleOCR` 的基础运行环境；差异主要体现在调用入口、pipeline、模型权重和后处理逻辑上。
   - 问题：lite benchmark 是否能代表最终结论？
   - 解答：不能完全代表。lite benchmark 更适合做快速筛选和工程选型初判，最终结论仍需要全量数据集和更完整的场景切片验证。
   - 问题：`MonkeyOCR` 早期表格分为 0 是否说明模型没有表格能力？
   - 解答：不是。根因是本地接入方式只跑了 text-only 路线。改成完整 parse 后，表格能力已经在 `OmniDocBench Lite` 上体现出来。

### 下周工作

1. 继续完善 `doc-parsing-benchmark` 仓库和相关文章，结合本周实测数据，进一步论证 `PaddleOCR-VL-1.5` 在金融领域文档解析中的实用价值，并输出可复用的 GitHub repo 和文章材料。

2. 围绕金融领域 PDF、研报、表格密集文档和复杂版式文档，补充更贴近业务场景的测试样例，验证 `PaddleOCR-VL-1.5` 在表格、公式、阅读顺序和 Markdown 结构恢复上的表现。

3. 总结出一套更专业的领域数据测评方法论，包括样本选择、分层抽样、统一输入、统一输出格式、官方 scorer 接入、失败页记录和榜单汇总流程。

4. 沉淀标准化 benchmark 流程和工具文档，形成从数据准备、模型推理、结果标准化、评分到结果解读的一套可复用模板。

5. 补充更多工程指标，例如平均单页耗时、成功率、失败页类型、显存占用和批处理稳定性，为后续判断模型是否适合生产主通道提供依据。

### 导师点评

请联系导师填写。
