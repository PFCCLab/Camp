### 姓名

蔡越

### 实习项目

PaddleMIX 套件能力建设（文图方向）

### 本周工作

1. **完成AnimateAnyone前向推理对齐**
   
   * 对源库进行代码移植，对齐前向推理精度和生成效果；
   * 完成相关预训练权重转换，支持用户从bos拉取模型权重，解除对huggingface的权重下载依赖；
   * 支持fp16和fp32两种精度的前向推理，在同等配置下显存占用均相较源库高15%，但符合预期；
   
   PR link: https://github.com/PaddlePaddle/PaddleMIX/pull/435

2. **编写ai studio AnimateAnyone 角色动作生成项目**
   
   * 在前向推理的基础上，添加开发者客制化动作视频的功能，考虑该功能涉及onnxruntime及权重，故未将其合并ppdiffusers仓库；
   
   project link: https://aistudio.baidu.com/projectdetail/7490749?contributionType=1

3. **分析源库训练流程，与导师沟通确立结合paddlenlp.Trainer的训练支持方式**
   
   - 在单卡40G算力下，该模型训练需使用基于sharding的优化策略(源库基于deepspeed支持)，学习基于paddlenlp.Trainer的训练流程以及paddle分布式训练相关技术。

### 下周工作

1. 基于paddlenlp.Trainer，实现AnimateAnyone两阶段训练steploss对齐，按照no trainer->对齐loss->trainer的流程进行，以进一步完善该example;
2. 思考对该模型微调效果提升的具体方式，包括数据集构建、微调提升目标、用户执行方式。

### 导师点评

蔡越在本周围绕着AnimateAnyone展开了一系列任务，完成了前向的对齐、加载逻辑升级、以及相关aistudio项目的编写，相关pr已合入paddlemix，态度积极认真，有很强的学习能力。