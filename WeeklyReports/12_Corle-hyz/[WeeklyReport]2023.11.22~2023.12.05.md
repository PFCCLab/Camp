### 姓名

何咏哲

Github ID：[Corle-hyz](https://github.com/Corle-hyz)

### 实习项目

[全自动并行架构升级](https://github.com/PaddlePaddle/community/blob/master/hackathon/hackathon_5th/%E3%80%90PaddlePaddle%20Hackathon%205th%E3%80%91%E9%A3%9E%E6%A1%A8%E6%8A%A4%E8%88%AA%E8%AE%A1%E5%88%92%E9%9B%86%E8%AE%AD%E8%90%A5%E9%A1%B9%E7%9B%AE%E5%90%88%E9%9B%86.md#%E9%A1%B9%E7%9B%AE%E5%8D%81%E4%BA%8C%E5%85%A8%E8%87%AA%E5%8A%A8%E5%B9%B6%E8%A1%8C%E6%9E%B6%E6%9E%84%E5%8D%87%E7%BA%A7)

### 本周工作

1. **Llama显存模型代码实现**
    - 将上周建立的Llama模型使用Python进行代码实现，定义函数的接口以及功能，并对代码进行测试

2. **在已有数据集上验证模型的准确性**
    - 借助已经实现的Llama显存模型预估公式，添加文件读写模块，根据已有测试数据的格式进行自动化对比验证

3. **修正模型公式**
    - 在代码实现以及结果验证的过程中发现之前建模中出现的纰漏，已对这一部分进行了修改
    - 进一步发现预估结果与实测结果差距较大，分析发现是原本对于梯度、参数和优化器状态的建模只考虑了Sharding的影响，除此之外PP、TP等并行模式也会对这一部分的显存占用带来影响。而对于大模型来说，由于梯度、参数和优化器状态占据了显存的绝大部分，因此这部分考虑的欠缺对结果造成了比较大的影响。目前还在修改中


3. **问题疑惑与解答**
    - 问题a：Paddle有没有考虑过使用[Chimera(SC'21)](https://dl.acm.org/doi/10.1145/3458817.3476145)或者[Hanayo(SC'23)](http://arxiv.org/abs/2308.15762)的方式来实现流水线并行（Pipeline Parallelism）？

        答：Chimera增加一条流水线的操作确实减少了Bubble，但是代价是参数、梯度和优化器状态的显存占用翻倍了，这对于大模型训练来说是不可接受的。Hanayo的做法和Interleaved PP（或者叫VPP）没有太大区别。
    
    - 问题b：paddle在训练大模型的时候会开量化吗？[有的项目在训练llama的时候会量化到8 bit甚至4 bit](https://github.com/ggerganov/llama.cpp)，并且paddle里面好像也给了量化的接口。

        答：训练的时候不开，训练对大厂而言，可能更追求的是模型效果，量化的话一般用8bit，一般会掉精度

### 下周工作

1. 继续考虑PP、TP等并行模式对梯度、参数和优化器状态的显存占用的影响，完善Llama显存模型。

### 导师点评

对显存模型有了正确的认识并开始提升了显存模型的正确性，下周正式完成代码开发并验证。
