### 姓名
李帅

### 实习项目
大模型训练稳定性和高效低价小模型快速收敛

### 本周工作

1. **开源模型框架学习**

    * 学习LLaMA、LLaMA-2、DiT、CLIP论文，了解其网络结构、训练策略以及优化器等相关技术原理。
    * 熟悉Megatron-LLaMA、Open-CLIP以及Large-DiT训练框架代码结构，掌握其优化器、分布式训练、梯度裁剪等相关代码实现。


2. **XXX梯度裁剪算法**

	* 基于Megatron-LM框架的GPT-2 345M模型上C4-en数据集的XXX梯度裁剪算法tensor-wise实验以及baseline实验，验证了XXX梯度裁剪算法的有效性，并进行了超参的搜索调整实验。
	* XXX梯度裁剪算法tensor-wise的代码在Megatron-LLaMA框架的实现，并在小规模数据集上对LLaMA-245M、LLaMA-1.2B规模的loss spike进行了复现。
	* 基于初始化方法的竞品算法在Megatron-LLaMA框架的实现以及基于AdamW优化器方法的竞品在Open-CLIP上的实现。


3. **大模型训练稳定性探索**

	* 阅读了从初始化以及网络结构角度进行大模型稳定性训练相关论文，拓展了相关工作内容。
	* VLM、MLLM两大类预训练任务中出现loss spike模型的调研，并对其解决方案的相关论文进行了阅读学习。


4. **问题疑惑与解答** 无


### 下周工作

1. LLaMA-13B模型fine-tune实验中出现loss spike情况的调研，并对其进行复现实验，验证XXX梯度裁剪算法在LLM的fine-tune任务中的有效性。
2. LLaMA-7B模型的XXX梯度裁剪算法实验以及VLM、MLLM两大类预训练任务中出现loss spike的baseline实验。
3. XXX梯度裁剪算法在VLM、MLLM两大类预训练任务中的实验验证，对比不同任务的效果。
4. 继续阅读梯度裁剪、大模型稳定性训练以及优化器的相关论文，为我们的优化算法提供理论支持，并开始着手构建论文框架。


### 导师点评
