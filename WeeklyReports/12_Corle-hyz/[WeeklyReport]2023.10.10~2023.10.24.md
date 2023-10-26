### 姓名

何咏哲

Github ID：[Corle-hyz](https://github.com/Corle-hyz)

### 实习项目

[全自动并行架构升级](https://github.com/PaddlePaddle/community/blob/master/hackathon/hackathon_5th/%E3%80%90PaddlePaddle%20Hackathon%205th%E3%80%91%E9%A3%9E%E6%A1%A8%E6%8A%A4%E8%88%AA%E8%AE%A1%E5%88%92%E9%9B%86%E8%AE%AD%E8%90%A5%E9%A1%B9%E7%9B%AE%E5%90%88%E9%9B%86.md#%E9%A1%B9%E7%9B%AE%E5%8D%81%E4%BA%8C%E5%85%A8%E8%87%AA%E5%8A%A8%E5%B9%B6%E8%A1%8C%E6%9E%B6%E6%9E%84%E5%8D%87%E7%BA%A7)

### 本周工作

1. **学习Llama显存模型的相关内容**
    - 阅读论文[《Reducing Activation Recomputation in Large Transformer Models》](https://arxiv.org/abs/2205.05198)，学习Megatron-LM中的选择重计算，了解如何推导出Transformer的显存公式
    - 阅读论文[《LLaMA: Open and Efficient Foundation Language Models》](https://arxiv.org/abs/2302.13971)，了解Llama 1模型相较于Transformer的改动，主要是以下三个方面：
        1. 预归一化：对Transformer各子层的输入进行归一化，而不对输出进行归一化，使用RMSNorm归一化函数。
        2. SwiGLU激活函数：用SwiGLU激活函数取代ReLU非线性从而提高性能。使用的维度是8d/3，而不是PaLM中的4d。
        3. 移除绝对位置嵌入，取而代之的是添加旋转位置嵌入(RoPE)。
2. **尝试建立一个初步的模型预估Llama 1-13B模型在单机8卡下的显存占用**
    - 鉴于Llama 1相较于Transformer改动不算很大，首先尝试将Transformer的显存模型直接套用到Llama上，得到的公式为sbhL(34+5as/h)，各个符号代表的含义如下表。
        | 符号 | 含义 |
        | --- | --- |
        | s | sequence length |
        | b | micro batch size |
        | h | hidden dimension size |
        | L | number of Transformer layers |
        | a | number of attention heads |
    - 但是论文中的公式计算的是激活内存，统计结果中的峰值内存还包括参数、优化器、NCCL占用等，因此差距较大。
    - 将上述结果/20+34000，结果相较于单机八卡的数据准确率在90%以上，但是这两个数字无法做出理论解释，不能推广到其他情况。


3. **问题疑惑与解答**
    - 问题a：Llama显存建模有什么用？

        答：在大模型语言训练的场景中，内存是限制并行模式选取的最主要因素之一。在实际的应用中，超过一半的并行策略会因为显存不足而无法实现。全自动并行课题的最终目的是能够快速地找到一个高效的并行策略。当我们在进行最优的并行策略搜索时，这些无法实现的策略会严重影响我们的搜索结果，通过显存建模我们可以预先剔除OOM的策略。
    - 问题b：我们要做的全自动并行和目前业界流行的Alpa有什么区别？
  
        答：Alpa仅仅关注了DP、MP、PP(1F1B)三种并行模式，而实际的业务场景中需要考虑的远远不止上述三种并行模式，我们要做的全自动并行除了上述三种模式之外，还需要考虑TP、SP、VPP(Interleaved PP)、Sharding、Recompute等因素。

### 下周工作

1. 明确Llama相较于Transformer修改的地方，仿照[《Reducing Activation Recomputation in Large Transformer Models》](https://arxiv.org/abs/2205.05198)的方式，从理论推导给出Llama的激活内存模型。

### 导师点评
