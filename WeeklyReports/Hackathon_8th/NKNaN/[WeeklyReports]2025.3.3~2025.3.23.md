### 姓名

李睿文

### 实习项目

混合专家架构自动切分推导优化

### 本周工作

1. **阅读文档学习Paddle自动并行机制**

- 分布式 ml 相关基础概念及框架实现：分布式张量概念、自动并行框架底层执行流程和原理 —— 切分推导和切分转换、自动并行和分布式策略 —— 数据并行，张量并行，流水并行和 3D 混合并行、自动并行相关 API 等 (https://www.paddlepaddle.org.cn/documentation/docs/zh/guides/paddle_v3_features/auto_parallel_cn.html)


2. **阅读文档学习切分推导规则开发流程**

- 切分推导相关概念及开发流程：分布式属性 —— process_mesh 和 dims_mapping、接口定义、计算类 op 及修改形状类 op 的规则开发、注册规则、单测开发 (https://github.com/PaddlePaddle/community/blob/master/pfcc/paddle-code-reading/auto_parallel/spmd_rules.md)


3. **梳理deepseek v3所需算子的切分推导规则配置情况**

- 根据 PaddleNLP 中的 deepseek v3 模型实现 (https://github.com/PaddlePaddle/PaddleNLP/blob/develop/paddlenlp/transformers/deepseek_v3/modeling_auto.py)，梳理出训练推理过程中可能需要用到的所有 API 及相应算子，排查对应算子的切分推导规则配置情况。以下 **API / 算子** 尚未配置切分推导规则：
  - _C_ops.embedding_with_scaled_gradient
  - paddle.expand
  - paddle.tril
  - _C_ops.memory_efficient_attention
  - paddle.incubate.nn.functional.fused_dot_product_attention
  - _C_ops.variable_length_memory_efficient_attention
  - paddle.einsum
  - F.tanh/F.gelu/F.leaky_relu/paddle.tanh/F.mish
  - paddle.log
  - paddle.topk
  - paddle.put_along_axis
  - paddle.gather
  - paddle.cumsum
  - paddle.erf
  - nn.CrossEntropyLoss


#### 问题疑惑与解答

暂无

### 下周工作

1. 确定需要增加切分推导规则的 API / 算子，并进行切分推导规则的开发。


### 导师点评
