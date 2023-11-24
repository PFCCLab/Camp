### 姓名

何咏哲

Github ID：[Corle-hyz](https://github.com/Corle-hyz)

### 实习项目

[全自动并行架构升级](https://github.com/PaddlePaddle/community/blob/master/hackathon/hackathon_5th/%E3%80%90PaddlePaddle%20Hackathon%205th%E3%80%91%E9%A3%9E%E6%A1%A8%E6%8A%A4%E8%88%AA%E8%AE%A1%E5%88%92%E9%9B%86%E8%AE%AD%E8%90%A5%E9%A1%B9%E7%9B%AE%E5%90%88%E9%9B%86.md#%E9%A1%B9%E7%9B%AE%E5%8D%81%E4%BA%8C%E5%85%A8%E8%87%AA%E5%8A%A8%E5%B9%B6%E8%A1%8C%E6%9E%B6%E6%9E%84%E5%8D%87%E7%BA%A7)

### 本周工作

1. **建立了在单卡训练时的Llama-1显存模型**
   - 了解深度学习训练的各个步骤对于显存的占用情况
        ```
            1.模型定义：定义了模型的网络结构，产生模型参数；
            while(训练):
                2.前向传播：执行模型的前向传播，产生中间激活值；
                3.后向传播：执行模型的后向传播，产生梯度；
                4.梯度更新：执行模型参数的更新，第一次执行的时候产生优化器状态。
        ```
    - 为每一部分的内存提供了理论分析，并得到内存模型
        - 模型参数：参数量在模型定义时指定，例如Llama-1 13B的参数量是13B，即130亿；GPT-2 1.5B的参数量是1.5B，即15亿。当下的大模型训练为了减少对内存的消耗使用的是混合精度运算，每个参数是fp16或bf16，占2个字节。
        - 模型梯度：梯度与参数一一对应，大小一致。
        - 优化器状态：取决于选用的优化器。例如，对于SGD优化器，只需要保存一份fp32的模型参数副本，每个参数副本占4个字节；对于Adam优化器，除了参数副本外还需要额外维护两个状态变量v和r，都是fp32，每个参数对应的优化器状态共计12字节。
        - 激活内存：Llama基于Transformer结构做了一些改进（详见上周周报），分析改进的各个部分后可以得到总的激活内存。
    - Llama-1模型在单卡训练时的显存公式为`M=(4+K)P+(86sbh/3+5abs^2)L`，其中各个参数的含义如下：
        - P: Number of Parameters
        - a: Attention Heads
        - b: Global Batch Size
        - h: Hidden Dimension Size
        - s: Sequence Length
        - L: Number of Transformer Layers
        - K: 4 for SGD Optimizer and 12 for Adam Optimizer


2. **问题疑惑与解答**
    - 问题a：fp16和bf16格式的区别是什么？为什么现在工业界在进行大规模训练时逐渐用bf16取代了fp16？

        答：FP16指的是半精度浮点数表示，通常意义上其表示为Nvidia提供的半精度浮点数表示方案，也被IEEE 754-2008方案所采纳，用5bit表示指数，10bit表示小数；而BF16是对FP32单精度浮点数截断数据，即用8bit表示指数，7bit表示小数。
        
        两者精度上差异不一样，BF16可表示的整数范围更广泛，但是尾数精度较小；FP16表示整数范围较小，但是尾数精度较高。

        FP16的可表示范围较FP32等更小，容易触发上、下溢出问题；BF16则因为阶码同FP32等长，因此并不容易出现上下溢出问题。


### 下周工作

1. 在单卡模型的基础上，进一步考虑DP、MP、PP、VPP、AccNum、Recompute、Sharding等并行模式，将单卡模型扩展到并行训练中。

### 导师点评

单卡建模工作取得较大进展，下一步结合分布式并行策略建立多卡下峰值显存模型，后续该工作将能够真正进行应用在大模型套件之中。
