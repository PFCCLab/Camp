### 姓名
罗震宇

### 实习项目
17-大模型复现

### 本周工作

1. **任务1：模型原文分析**
* **存在的问题：** 现有的解码器规模已经非常庞大，但是在语义搜索和句子嵌入领域仍表现不佳
* **解决方法：** 提出SGPT模型，通过提示或微调的进行语义搜索和句子嵌入
* **解决结果：** 相对于以前的最佳句子嵌入方法，提高了7%。此外，在 BEIR（Bi-Encoder Information Retrieval）搜索基准测试中，以1750亿参数的一种并行方法作为参照，表现更好



2. **任务2：复现指标分析**
* **Table1中的指标：** 显示的是SGPT-CE在非对称领域的性能表现
  1. 首先，Table1中使用的提示是来自于附录B.1中 在MSMARCO数据集上表现最好的prompt。
基于该prompt对所提出的SGPT-CE模型进行基准测试（此处提到与 OpenAI 的搜索端点进行比较，以区别于其嵌入端点。请参阅双编码器部分中的表 6，了解 OpenAI Embeddings 端点的基准。）
  2.Table1中的结果显示 SGPT-CE-6.1B 比基于编码器的最先进技术在更多数据集上获胜，但其平均得分更差。但是文中提到该问题可以通过不对所有数据集使用相同的提示 PG 来缓解。（在§3.2中展示了SGPT-CE-6.1B可以通过改变提示符在Quora上击败BM25+CE）
* **Table6中的指标：** 显示的是SGPT-BE在非对称搜索领域的性能表现。
在 BEIR [44] 上对 SGPT-BE-5.8B (SGPT-5.8B-weightedmean-msmarco-specb-bitfit) 进行基准测试，
其中：a) BM25 [41]，非语义快速基线 (b) SGPT-CE -6.1B 来自 §3 (c) BM25+CE [44]，BEIR (d) TAS-B [17] 上当前整体最先进的技术，原始双编码器最先进的技术BEIR (e) Contriever [20]，与 [27] 类似的训练方案，但使用编码器变压器 (f) GTR-XXL [29]，BEIR 上当前最先进的双编码器，拥有 48 亿个数据使用 T5 [38] (g) cpt-text 的类似 BERT 的编码器变压器的参数，这是[27]中同时提出的类似 GPT 的解码器变压器架构。相应的参数估计见表2。
* **补充内容：** 两张表都是关于非对称式搜索。补充两种搜索方法的应用场景：
   1. **对称式搜索：**
      1. 那些要求查询文本和候选文本之间具有相似处理方式的任务。例如，传统的文档检索任务通常需要对文档库中的文档和用户查询使用相似的表示方法，这时对称式搜索是合适的。
      2.	在一些机器翻译任务中，源语言和目标语言之间可能需要对称的表示，以实现翻译和对齐
   2. **非对称式搜索：**
	     在问回系统、搜索引擎优化、语义搜索等任务中非常重要。这些任务通常涉及用户提出的查询（通常较短）和大量的候选文本（例如，文档库中的文档），其中查询和候选文本之间存在明显的不对称性。
3. **任务3：结合复现指南及源码明确工作安排**
* 源码运行：能够正常运行
* 确定模型信息：EleutherAI/gpt-j-6B 和 GPT2Tokenizer
* 模型转换：gpt-j-6B在paddlenlp中存在相关资料，
3. **问题疑惑与解答**
主要问题集中在模型资料确定和复现环境配置上。由于初期对该模型信息不了解，在模型资料选择上花费了一些时间，后续在导师的指导下完成了模型复现资料确定。
关于复现环境配置上，由于服务器环境与paddle配置要求不匹配出现报错问题，目前未找到较好的解决方法，正在尝试通过miniconda重新搭建环境解决。


### 下周工作

1. 在完成仿真环境搭建的基础上，对gpt-j-6B模型依次进行权重转换、前向对齐、评价指标对齐、损失函数对齐
2. 完成数据集及GPT2Tokenizer资料调研及处理

### 导师点评

初期可能会踩一些坑，多参考Paddlenlp里面的实现，gpt这些模型都有相关的复现，前向对齐即可。
