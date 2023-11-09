### 姓名
侯悦欣

### 实习项目
Nougat复现及优化

### 本周工作

1. **文献和源码阅读**

	* Nougat论文阅读
   * Nougat源码阅读
	* PPOcr相关源码阅读


2. **实现思路整理**

	* 在下游数据集上微调Nougat，作为精度标准 
	* 模型移植:
       * 数据加载和处理
       * 网络
       * 后处理
       * 损失函数
       * 指标评估
       * 优化器


3.. **问题疑惑与解答**


	* 问题a 网络部分，Nougat的Transfomer Encoder-Decoder架构和pporc的backbone-neck-head架构兼容性问题

        答：backbone 可以对应 encoder， head 可以对应decoder， neck是可选项可以去除。 逻辑可以参考NRTR这个纯Transformer的结构：https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.7/configs/rec/rec_mtb_nrtr.yml

	* 问题b 原仓库的数据集制作工具模块能够集成到pporc中吗？

        答：可以尝试移植，或者完成离线数据生成，不强制要求


### 下周工作

1. 复现原仓库推理结果、工具函数
2. 制作简单数据集，复现训练过程
3. 阅读原仓库源码，与PPOCR现有模块进行对比，确定可复用的模块和需要添加的新模块

### 导师点评
完成了初步的准备工作，下周可以优先跑出源码的推理结果，并尝试推理结果前向对齐。加油哦
