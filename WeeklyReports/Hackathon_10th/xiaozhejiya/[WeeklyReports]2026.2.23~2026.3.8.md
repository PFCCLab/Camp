## 姓名

李溯寒

## 实习项目

PaddleOCR + ERNIE × Open-Source Ecosystem

## 本周工作

### 数据库驱动科目与标签一致性

- **删除 `detect_subject` 硬编码关键词匹配**（`db/crud.py`）：
  - 原先通过 6 个关键词集合（约 50 个关键词）推断科目，无法覆盖新科目
  - 改由编排智能体在 OCR 分析阶段直接识别科目，`save_questions` 时传入
- **新增 `get_existing_subjects()` 和 `get_existing_tag_names()`**（`db/crud.py`）：
  - 从数据库查询已有科目和知识点标签，支持按科目过滤标签
- **Workflow 注入数据库上下文**（`src/workflow.py`）：
  - `split_questions_node` 启动时加载已有科目和标签，构建 `db_context` 文本注入到发给编排智能体的用户消息中
  - 编排智能体收到"历史数据参考"后，优先复用已有科目名称和标签，保证跨会话一致性

### OCR 双层重试机制

- **OCR 中间件加入 3 次指数退避重试**（`error_correction_agent/middleware/ocr_middleware.py`）：
  - `before_agent` 钩子中新增重试逻辑，延迟 15s / 30s / 60s，全部失败后注入 `retry_ocr` 使用提示
- **新增 `retry_ocr` 工具**（`error_correction_agent/tools/question_tools.py`）：
  - 供编排智能体在中间件重试全部失败后手动调用，创建 `PaddleOCRClient` 执行异步 OCR，返回简化后的数据 JSON
  - 形成"中间件自动重试 → 智能体手动重试"两层容错

### 分割并行化与重试增强

- **分割题目改为并行处理**（`src/workflow.py`）：
  - 原流程由编排智能体串行调用 `split_batch`，改为 workflow 层直接构建 2 页一批、1 页重叠的批次列表
  - 使用 `ThreadPoolExecutor` + `as_completed` 并行调用各批次，结果按批次序号排序后合并
  - 新增 `_build_overlapping_batches()`、`_run_ocr_and_simplify()`、`_load_db_context()`、`_identify_subject()` 等辅助函数
- **`split_batch` / `correct_batch` 加入 3 次重试，每次创建全新 agent 实例**（`error_correction_agent/tools/question_tools.py`）：
  - 避免上一次失败的消息历史污染新请求（解决 DeepSeek API 400 "insufficient tool messages" 错误）
- **知识点标签按科目过滤**（`src/workflow.py`）：
  - 调用 `get_existing_tag_names(db, subject=subject)` 按科目过滤，避免跨科目标签混入

### 多模型供应商支持

- **`_init_model` 支持 provider 参数**（`error_correction_agent/agent.py`）：
  - 支持 `"deepseek"` 和 `"ernie"` 两个供应商，ernie 通过 OpenAI 兼容接口连接百度 AIStudio
- **全链路透传 `model_provider`**（`src/workflow.py`、`error_correction_agent/tools/question_tools.py`、`web_app.py`）：
  - 前端选择 → 请求体传 → `WorkflowState` 存 → 工具透传 → `_init_model` 按字符串判断走哪个分支
- **前端模型选择器**（`frontend/src/App.vue`）：
  - 使用 HeadlessUI Listbox 替代原生 `<select>`，从 `/api/status` 动态获取可用模型列表及配置状态
  - 初始化时自动选择第一个已配置可用的模型
- **解决文心 ToolStrategy 兼容性问题**（`error_correction_agent/agent.py`）：
  - 文心通过 OpenAI 兼容接口不支持 function calling，`ToolStrategy` 陷入无限重试
  - 新增 `invoke_split()` / `invoke_correction()` 统一调用入口，ernie 改用 `model.with_structured_output()` 替代
  - 重试循环加入指数退避延迟，避免瞬间打满限频

### LLM 轻量模型科目识别

- **新增 `detect_subject_via_llm()`**（`error_correction_agent/agent.py`）：
  - 通过 `ERNIE_LIGHT_MODEL_NAME`（默认 `ernie-4.5-0.3b`）或 `DEEPSEEK_LIGHT_MODEL_NAME` 配置轻量模型
  - 极简 prompt，传入 ≤1500 字 OCR 文本 + 已有科目列表，只返回科目名称
- **`_identify_subject()` 改为三层 fallback**（`src/workflow.py`）：
  - LLM 预检 → 关键词匹配 → 内容特征推断，LLM 失败时静默回退到关键词匹配
- **新增 `_extract_text_sample()`**（`src/workflow.py`）：从 OCR 前 2 页提取文本，原逻辑抽取为独立函数

### 移除外层编排智能体

- **移除 `create_orchestrator_agent()` 及相关模块**（`error_correction_agent/agent.py`）：
  - 删除 `ORCHESTRATOR_PROMPT`、`agent` 变量、deepagents / OCRMiddleware 导入
  - 删除 `middleware/ocr_middleware.py`、`middleware/__init__.py`、`tests/test_ocr_middleware.py`、`langgraph.json`
  - 外层编排职责已在 3/1 并行化重构中被 workflow 层完全接管

### 解题智能体与模型评测

- **新增解题智能体**（`backend/solve_agent/`）：
  - 接收题目文本，调用 LLM 生成解答
- **新增评测模块**（`backend/benchmark/`）：
  - 基于 C-Eval 数据集评测解题准确率，替代原先自采 OCR 数据的评测方式
  - 移除旧的 OCR 数据采集模块，改用专业数据集

### PaddleOCR V2 异步任务 API 适配

- **重写 `PaddleOCRClient`**（`backend/src/paddleocr_client.py`）：
  - 适配 PaddleOCR V2 异步任务 API（提交任务 → 轮询结果），替代旧版同步接口
  - `_poll_job` 添加 300s 超时上限，防止无限轮询
- **移除 PDF 转图片逻辑**（`backend/src/workflow.py`）：
  - PDF 直传 OCR API，由服务端处理，简化本地预处理流程

### 代码质量与安全加固

- **消除模块级副作用**（`backend/config.py`、`backend/llm.py`）：
  - `config.py` 的目录创建改为 `ensure_dirs()` 显式调用，不在 `import` 时触发
  - `llm.py` 移除模块级 `load_dotenv()`，添加 provider 校验
- **提取共享工具函数**（`backend/src/utils.py`）：
  - `simplify_ocr_results`、`run_async` 等函数提取到 `utils.py`，消除 workflow / 工具间的重复代码
- **统一数据库会话管理**（`backend/web_app.py`）：
  - 使用 `with SessionLocal() as db:` 上下文管理器，统一序列化辅助函数
- **修复文件名解析崩溃**（`backend/web_app.py`）：
  - 使用 `os.path.splitext()` 替代 `rsplit('.', 1)`（无扩展名时会崩溃）
  - 修复锁内列表推导式重新赋值的线程安全问题，改为原地修改
- **`delete_question` 添加事务回滚保护**（`backend/db/crud.py`）
- **`SPLIT_PROMPT` 明确 `block_type` 只允许 `text` 或 `image`**（`error_correction_agent/prompts.py`）

### 前端改进

- **图片预览弹窗缩放**（`frontend/src/App.vue`）：
  - 滚轮缩放（0.25x ~ 5x），弹窗打开时禁止背景滚动，缩放带平滑过渡
- **安全加固与可访问性改进**（`frontend/src/App.vue`）：
  - 样式提取、XSS 防护、ARIA 属性补充
- **提取纯函数到 `utils.js`**（`frontend/src/utils.js`）
- **新增前端测试脚本**（`frontend/tests/`）

### 测试套件

- **新增 / 补充测试**（`backend/tests/`，11 个文件）：
  - `test_workflow_helpers.py`：`_simplify_ocr_results`、`_build_overlapping_batches`、`_identify_subject`（含 LLM 预检层）、`_extract_text_sample` 等辅助函数测试
  - `test_question_tools.py`、`test_schemas.py`、`test_crud.py`、`test_correct_node.py`、`test_export.py`、`test_web_routes.py`
  - `test_split_integration.py`：集成测试，支持 `--model-provider` 指定厂商
  - `test_ocr_api.py`：PaddleOCR API 集成测试
  - 集成测试添加 `skip_no_api_key` 保护，测试数据固化到 `fixtures/`
  - 提取公共 fixture 到 `conftest.py`（`db` 内存数据库、`make_question` 工厂函数）
- **CLAUDE.md 新增后端开发、测试、Git 提交规范**

### 文档与许可证

- **添加 AGPL-3.0 开源许可证**
- **README 补充文心一言模型配置说明**

### 下周计划

1. 基于 C-Eval 数据集对比测试 DeepSeek 与文心一言的解题正确率
2. 新增错题库页面，加载数据库中持久化的历史错题
3. 对错题知识点进行统计分析，识别薄弱知识点并进行可视化展示
4. 集成手写字迹擦除模型，提升 OCR 识别准确率

### 导师点评
