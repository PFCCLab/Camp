## 姓名  

李溯寒

## 实习项目  

PaddleOCR + ERNIE × Open-Source Ecosystem

## 本周工作  



### 项目初始化

完成项目首次提交，搭建基础代码结构：
- `src/paddleocr_client.py`：封装 PaddleOCR API 客户端，使用 `requests` 库发送 base64 编码图片，解析返回的 `layoutParsingResults` 并保存结构化 JSON
- `src/workflow.py`：基于 `ErrorCorrectionWorkflow` 类编排 5 步工作流（prepare_input → paddleocr_parse → split_questions → build_preview → export_wrongbook）
- `src/utils.py`：实现 PDF 转图片（`pdf2image`）、图片标准化、HTML 预览生成、Markdown 错题本导出
- `error_correction_agent/`：基于 LangChain 创建 DeepSeek Agent，定义 4 个工具（`save_questions`、`log_issue`、`download_image`、`read_ocr_result`），用于智能分割题目
- 配置 `.env.example`、`requirements.txt`、`langgraph.json` 等工程文件



### 前端页面 & Bug 修复

- **新增 Web 前端**：使用 Flask 实现 `web_app.py`，提供文件上传、OCR 解析、题目预览、导出等 API 路由；`templates/index.html` 实现拖拽上传交互界面
- **修复数学公式无法渲染**（`templates/index.html`）：
  - 引入 MathJax 3（`tex-svg.js`），配置 `$...$` 行内和 `$$...$$` 独占行公式识别
  - 在题目预览渲染后调用 `MathJax.typesetPromise()` 触发动态公式渲染
  - 为 `display_formula` 块自动包裹 `$$` 标记，为图片块增加 `<img>` 标签直接展示
- **修复公式块多重堆叠**（`src/utils.py`）：
  - 导出 Markdown 时检测公式 content 是否已包含 `$$` / `$` 标记，避免双重包裹导致渲染异常
- **修复图片路径保存问题**（`src/utils.py`）：
  - image block 的 content 为空时，依次从 `image_refs` 数组和 `bbox` 坐标自动推导图片路径（按 PaddleOCR 输出命名规则 `img_in_image_box_{x1}_{y1}_{x2}_{y2}.jpg` 生成相对路径）

### 核心架构重写 & Agent 优化

- **工作流重写为 LangGraph 图**（`src/workflow.py`）：
  - 废弃原 `ErrorCorrectionWorkflow` 类的命令式调用，改用 `langgraph.graph.StateGraph` 定义 `WorkflowState`（TypedDict）
  - 将每个处理步骤定义为独立节点函数（`prepare_input_node`、`ocr_parse_node`、`split_questions_node`、`export_node`）
  - 使用 `MemorySaver` 作为 checkpointer 保存中间状态，在 `split_questions` 和 `export` 节点前设置 `interrupt_before` 中断，支持 Web 端分步交互
- **简化 Agent 内容块类型**（`error_correction_agent/prompts.py`）：
  - 移除 `display_formula` 和 `inline_formula` 两种块类型，只保留 `text` 和 `image`
  - 公式不再单独成块，改为用 LaTeX 标记直接嵌入 text 的 content 中（行内 `$...$`，独占行 `$$...$$`），由 MathJax 自动识别渲染
- **解决选项出现在题干中的问题**（`error_correction_agent/prompts.py`）：
  - 在 Agent 系统提示词中增加约束：如果选项已提取到 `options` 数组，必须从 `content_blocks` 文本中移除选项部分，避免重复
- **修复 Agent 失败时读取旧数据**（`src/workflow.py`）：
  - 在 `split_questions_node` 执行前先删除已有的 `questions.json`，防止 Agent 调用失败时读到上一次的过期结果
  - 增加 Agent 响应摘要打印（遍历 `response["messages"]` 输出每条非 human 消息前 200 字符），便于排查问题
- **合并协作者 PR**：
  - wangmeitian116：添加 API 接口文档
  - jinning090610：在 `web_app.py` 中增加文件大小校验提示、支持中文文件名上传（使用 uuid 生成存储文件名）、优化中文错误提示、添加处理日志记录

### PaddleOCR 异步调用

- 实现 PaddleOCR 异步并发解析（`src/paddleocr_client.py`）：

  - 新增 `async_parse_image()` 方法，使用 `aiohttp.ClientSession` 异步发送 POST 请求
  - 新增 `_async_download_image()` / `_async_save_images()` 方法，使用 `asyncio.gather()` 并发下载 OCR 结果中的所有图片资源（markdown images + outputImages）
  - 新增 `parse_images_async()` 入口方法，接收多张图片路径列表，通过 `asyncio.gather()` 并发解析所有图片，结果顺序与输入一致

### 多文件上传 & 重试机制

- **支持多文件上传**（`web_app.py` + `templates/index.html`）：
  - 后端 `/api/upload` 接口改为接收 `files` 字段的文件列表（`request.files.getlist('files')`），兼容单文件 `file` 字段
  - 循环校验每个文件的格式和大小，逐一保存后将路径列表传入工作流
  - 前端修复拖拽上传丢失文件问题：将 `e.dataTransfer.files`（FileList）通过 `Array.from()` 转为数组，避免部分浏览器在事件结束后清空 DataTransfer 对象
- **新增 OCR API 重试机制**（`src/paddleocr_client.py`）：
  - 在 `async_parse_image()` 的异步请求中增加最多 3 次重试，失败后按 `attempt * 5` 秒递增等待（5s / 10s / 15s），提升 API 调用稳定性
- **合并协作者 PR**：
  - chenmeihui812：前端新增上传进度条、图片点击预览弹窗、Ctrl+A 全选快捷键


### 下周计划  

1. 基于LangChain 实现Agent 异步调用
2. 复现[ [EnsExam](https://discovery.ucl.ac.uk/id/eprint/10174246/1/2023_ICDAR_paper_8652.pdf?utm_source=chatgpt.com) ]( [https://discovery.ucl.ac.uk/id/eprint/10174246/1/2023_ICDAR_paper_8652.pdf?utm_source=chatgpt.com) 探索擦除笔记的方法
3. 修复错误
   1. 上传多文件或PDF时会出现没有错题输出的情况
   2. 成功上传图片后如何没有进行分割问题再次上传图片会出现报错

### 导师点评
