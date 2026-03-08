### 姓名  

李溯寒

### 实习项目  

PaddleOCR + ERNIE × Open-Source Ecosystem

### 本周工作  

1. 明确项目方向与目标人群  

   - 讨论并收敛两个核心场景：  
     - 拍卷子/作业：识别题目、选项、手写答案，生成可整理的错题本（错题由用户勾选）  
     - 拍书/PPT：自动整理成可复习笔记（作为后续扩展方向）  

   - 重点聚焦学生群体（大学生/考研党/考公党）的高频“拍照$\rightarrow$整理”需求，强调“输出可复习笔记/错题本”而非仅图片转文字。

2. 方案拆解：错题本生成流程

   - 制定端到端流程：PDF/图片输入 $\rightarrow$预处理 $\rightarrow$文本检测与裁剪 $\rightarrow$手写/印刷体分类 $\rightarrow$生成干净整洁的图片 $\rightarrow$PaddleOCR 结构化解析 $\rightarrow$题目切分与结构化 $\rightarrow$预览 $\rightarrow$用户勾选错题 $\rightarrow$导出错题本（md格式）。  

   - 决策：错题判断不做自动判定，交由用户选择，降低不确定性与复杂度。  

   - 手写识别阶段策略：先做“手写区域截图留存并关联题目”，不强制识别手写内容。

3. PaddleOCR 结构化 API 能力核验  

   - 基于 PaddleOCR-VL 的 JSON 返回结果确认：  
     - 提供阅读顺序字段 `block_order`（可用于阅读顺序重建）  
     - 提供结构化块 `parsing_res_list`（含 `block_label/block_content/block_bbox/group_id` 等）  
     - 提供可直接使用的 `markdown.text` 与图片映射 `markdown.images`  

   - 将第 6 步及之后的流程改为“优先用 PaddleOCR API 输出的结构化结果驱动题目切分”。

4. deepagents 和 LangGraph 工程环境与调试链路  

   - 完成 deepagents 、 langchain 、 langgraph  等依赖安装与环境检查（依赖清单整理为可复用 requirements 结构）。  

   - 成功启动 `langgraph dev` 本地服务（API: http://127.0.0.1:2024；Docs 可访问），并定位 Studio “Failed to fetch” 属于浏览器安全策略/本地网络访问限制，明确可用的解决策略。  

5. LangChain 结构化输出与 DeepSeek 兼容性排查  

   - 复现并定位 DeepSeek OpenAI 兼容接口对 `response_format` 结构化输出的限制（400: response_format unavailable）。  

   - 给出替代方案：改用 JSON 提示词 + JSON Parser（SimpleJsonOutputParser）或 function/tool calling（视模型支持情况），并修正 init_chat_model 参数使用错误（model vs model_name）。  

   - 排查并解释 UnicodeEncodeError（请求头 header 含非 ASCII 字符）属于环境变量或自定义 header 导致的编码问题，提供检查与清理思路。


### 下周计划  

1. 学习 LangGraph 的基本概念与开发方式（Graph/Node/Edge、编排与执行模型、调试方式）。  
2. 学习并掌握 LangGraph 中的 State 设计与管理（如 AgentState/状态流转、状态字段定义、如何在节点间传递与更新状态）。  
3. 基于学习结果，整理一份可复用的 LangGraph + AgentState 最小示例工程（便于后续将错题本流程接入 Graph 运行）。 

### 导师点评
