### 姓名

PrayerQX

### 实习项目

基于 PaddleOCR + ERNIE 4.5 的金融文档理解与可复现实验流水线

### 本周工作

1. 完成 `paddleocr-ernie-pyfi` 项目的新版仓库整理与导入

   - 基于 `uv` 搭建本地可复现工程，整理 `pyproject.toml`、`.env.example`、`.gitignore` 和基础 README，明确依赖、环境变量和运行方式，相关内容已同步到 GitHub 仓库 [paddleocr-ernie-pyfi](https://github.com/PrayerQX/paddleocr-ernie-pyfi)。
   - 将项目结构拆分为 `cli`、`pipeline`、`dataset`、`manifest_runner`、`paddleocr_client`、`ernie_client`、`reporting` 等模块，形成较清晰的职责边界。
   - 补充 `contract`、`finance`、`invoice`、`research_paper` 四类 domain adapter 的 YAML 配置，为后续跨领域迁移保留统一接口。
   - 同步补齐测试骨架，覆盖 dataset manifest、router、prompt、pipeline、reporting、scoring 等核心模块，保证后续迭代有基本回归保护。

2. 搭建 PaddleOCR 远程解析 + ERNIE 4.5 的文档理解链路

   - 形成从 `PDF/Image -> PaddleOCR layout parsing -> OCR evidence -> ERNIE reasoning -> Markdown/JSON export` 的完整流程，相关说明已整理在仓库 [README](https://github.com/PrayerQX/paddleocr-ernie-pyfi/blob/main/README.md)。
   - 在 CLI 中提供 `dataset-info`、`dataset-download`、`parse`、`analyze`、`ask`、`manifest`、`run-manifest`、`score-manifest`、`export-architecture` 等命令，方便后续实验复现。
   - 增加 `QuestionRouter` 与 `OCRPresetResolver`，让不同题型和能力项可以自动选择 `light`、`medium`、`heavy` 等 OCR 策略。
   - 对图表类问题增加 chart consistency 校验逻辑，要求模型比对 OCR 重建表格和原图趋势，降低图表 OCR 失真后直接下结论的风险，架构说明已整理在 [docs/architecture.md](https://github.com/PrayerQX/paddleocr-ernie-pyfi/blob/main/docs/architecture.md)。

3. 围绕 PyFi 金融数据集搭建 benchmark 与评测流程

   - 接入 `PyFi-600K` 数据集，支持只查看 metadata、按 selection 下载核心文件，以及基于公开 CSV 构建本地 manifest。
   - 增加按 `capability` 分层采样的 301 样本 manifest 方案，并固定 seed，尽量保证多轮实验具备可比性和可复现性。
   - 在 manifest runner 中实现逐样本状态记录和 resume 机制，避免长跑实验中断后整轮重跑。
   - 默认关闭 web search，强调 benchmark 评测只基于数据集证据和 OCR 证据，避免引入额外检索噪声，整体流程已经沉淀到项目仓库 [paddleocr-ernie-pyfi](https://github.com/PrayerQX/paddleocr-ernie-pyfi)。

4. 完成两轮 `pyfi301` 实验并整理 benchmark 结果总结

   - 使用相同的 `ernie-4.5-21b-a3b` 模型，对两套 PaddleOCR 配置分别完成 301 样本实验，并在 [README](https://github.com/PrayerQX/paddleocr-ernie-pyfi/blob/main/README.md) 与 [docs/two_round_results_summary.md](https://github.com/PrayerQX/paddleocr-ernie-pyfi/blob/main/docs/two_round_results_summary.md) 中沉淀结果。
   - 第一轮采用较轻的 `layout-parsing + medium` 配置，得到 `163/295` 正确，准确率 `0.552542`。
   - 第二轮采用更重的 `baidu_sample` 配置，得到 `157/300` 正确，准确率 `0.523333`，虽然缺失预测从 `6` 降到 `1`，但整体精度下降。
   - 初步结论是更重的 OCR 配置提升了覆盖率，但在 `Calculation_analysis` 和 `Data_extraction` 上反而退步，说明更完整的 OCR 输出不一定等价于更高质量的数值证据。

5. 梳理当前链路的核心问题，并输出后续优化方向

   - 从现有文档总结看，当前最主要的问题仍然是视觉信息在 OCR 文本化过程中丢失，尤其体现在颜色、图例、空间位置、多子图关系等强视觉题目中。
   - 除了 OCR 失真外，也已经观察到一部分样本属于“证据已经够，但 ERNIE 仍然判断错误”，说明问题不只在 OCR，也在推理与输出约束层。
   - 在 `docs/architecture.md` 中进一步明确模块边界、证据流和可复现要求，避免后续项目扩展时重复耦合实现。
   - 结合两轮实验结果，当前更适合先把第一轮配置作为基线，再继续做 OCR 参数、提示词和视觉证据保留策略的定向优化。

### 下周工作

1. 重点对当前 `pyfi301` 样本集做人工检查，逐条核对题目、标准答案、OCR 证据和模型输出之间是否一致，优先确认样本集本身的准确程度和可评测性。

2. 在人工检查的基础上，筛出最值得突破的单个模块，优先选择最有希望通过工程优化拿到榜单最优成绩的能力项，集中投入优化。

3. 围绕选定模块继续做定向优化，重点验证 OCR preset、prompt 约束、证据组织方式和输出格式约束是否能够稳定拉升该模块成绩。

4. 对优化后的方案进行小规模反复复测，确认提升不是偶然结果，并尽量把该模块的分数推进到当前榜单最优。

5. 持续补充实验记录和文档，把人工核查结论、优化思路和最终结果同步回 GitHub 仓库，保证后续复现和展示都更完整。

### 导师点评

请联系导师填写。
