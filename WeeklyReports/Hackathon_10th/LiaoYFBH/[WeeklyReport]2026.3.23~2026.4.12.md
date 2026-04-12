### 姓名

LiaoYFBH

### 实习项目

[PaddleOCR + ERNIE × Open-Source Ecosystem 高价值开源项目案例征集]

### 本周工作

1. 在端到端科研Agent流程中，增加了基于LLM的评审模型（Reviewer），使用独立的轻量模型（ernie-speed-128k）在文献检索完成、报告生成等关键节点对主模型输出进行幻觉检测和质量评审。
2. 增加了PDF生成模块（PaperForge集成），支持将Agent生成的Markdown研究报告（含图表、参考文献）导出为标准论文格式的PDF。
3. 调研了可用于科研Agent评测的benchmark，初步集成了ScienceAgentBench（102个科学计算任务），后续还将考虑MLAgentBench、GAIA等benchmark。

### 下周工作

1. 修复评审模型未生效的问题（当前reviewer反馈未注入回agent对话），使评审结果能实际引导agent修正输出。
2. 增加终端交互模式，支持不依赖Gradio UI直接在命令行运行和交互。
3. 在ScienceAgentBench等benchmark上进行实际评测，收集性能指标（任务完成率、步骤数、程序生成率等）。
4. 找一些用户进行实际体验，收集反馈建议。
