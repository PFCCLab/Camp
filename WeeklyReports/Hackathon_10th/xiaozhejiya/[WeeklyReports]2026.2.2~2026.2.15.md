## 姓名

李溯寒

## 实习项目

PaddleOCR + ERNIE × Open-Source Ecosystem

## 本周工作

### 多智能体架构重构

- **拆分为双层多智能体架构**（`error_correction_agent/agent.py`、`error_correction_agent/prompts.py`）：
  - 废弃单一 Agent 架构，拆分为外层编排智能体（`create_orchestrator_agent`，基于 deepagents `create_deep_agent`）和内层分割智能体（`create_inner_split_agent`，基于 LangChain `create_agent` + `ToolStrategy`）
  - 外层负责分批策略与工具调用循环，内层专注于结构化题目分割，输出由 Pydantic Schema 强制校验
  - 新增 `SPLIT_PROMPT`（内层分割提示词）和 `ORCHESTRATOR_PROMPT`（外层编排提示词），分离职责
- **结构化输出改为厂商原生支持方式**（`error_correction_agent/agent.py`）：
  - 使用 `ToolStrategy(schema=QuestionSplitResult, handle_errors=True)` 替代手动 JSON 解析，利用 DeepSeek 的 function calling 能力保证输出格式
- **新增 `split_batch` 工具**（`error_correction_agent/tools/question_tools.py`）：
  - 封装内层分割智能体调用，接收 OCR 数据 JSON 和已处理题号列表，返回结构化题目列表

### PaddleOCR 中间件化

- **将 OCR API 调用改为中间件自动注入**（`error_correction_agent/middleware.py`）：
  - 实现 `OCRMiddleware`，在编排智能体收到图片路径后自动调用 PaddleOCR API 解析，将 OCR 结果注入到 agent messages 中
  - workflow 层只需传入图片路径，无需显式调用 OCR 解析函数，简化调用链路

### 分批去重策略

- **解决跨批次题目重复提取问题**（`error_correction_agent/prompts.py`、`error_correction_agent/tools/question_tools.py`）：
  - 采用 2 页一批、相邻批次重叠 1 页的分批策略，避免跨页题目被截断
  - `split_batch` 工具新增 `existing_ids` 参数，编排智能体在每批调用时传入已提取的题号列表，内层智能体跳过重复题目
  - 废弃原有的 `deduplicate_questions` 后处理函数，改为在分割阶段通过提示词直接避免重复

### OCR 纠错智能体

- **新增纠错智能体**（`error_correction_agent/agent.py`、`error_correction_agent/schemas.py`）：
  - 新增 `create_correction_agent()`，复用 `create_agent` + `ToolStrategy` 模式，输出约束为 `CorrectionResult` Schema
  - `Question` 模型新增 `needs_correction`（是否疑似 OCR 错误）和 `ocr_issues`（错误描述列表）两个字段
  - 新增 `CorrectedQuestion` 和 `CorrectionResult` Pydantic 模型
- **SPLIT_PROMPT 新增 OCR 错误标记指令**（`error_correction_agent/prompts.py`）：
  - 分割时同步检查乱码字符、公式残缺、文字缺失、选项错乱、变量下标丢失 5 类 OCR 错误并标记
- **新增变量下标还原规则**（`error_correction_agent/prompts.py`）：
  - 在 SPLIT_PROMPT 和 CORRECTION_PROMPT 中加入变量下标还原规则，解决 OCR 将 `xi`/`yi`/`an`/`Sn` 等带下标变量扁平化的问题
- **工作流新增 `correct_questions_node` 纠错节点**（`src/workflow.py`）：
  - 在 `split_questions` 和 `export` 之间插入纠错节点，仅对标记了 `needs_correction=True` 的题目调用纠错智能体，未标记题目直接通过（零额外 LLM 开销）
  - 纠错结果按 `question_id` 合并回原列表，更新 `questions.json`

### 前端渲染 & Bug 修复

- **预览页表格渲染及 LaTeX 公式兼容**（`templates/index.html`）：
  - 支持渲染题目中的 HTML `<table>` 表格结构，同时保持 MathJax 公式在表格内正常渲染
- **修复 `fileCount` 未定义 Bug**（前端）
- **合并协作者 PR**：
  - IDhammaI：Vue3 前端重构、后端目录整理（移至 `/backend`）、统一配置与目录管理、取消文件接口逻辑改进

### 下周计划

1. 探索低开销的手写/印刷体分类方法
2. 设计错题库持久化方案（SQLite 数据库表结构设计、入库去重逻辑）
3. 在 SPLIT_PROMPT 中加入知识点标注指令，分割时顺带标注知识点标签

### 导师点评
