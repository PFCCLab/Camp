### 姓名
冯潇

### 实习项目
动静统一自动并行支持MoE专家并行策略

### 本周工作

1. 构建了一个等效qwen2moe SparseMoEBlock的模型
2. 将该模型改成自动并行版本并且验证其与单节点结果的一致性

  * 相关pr: https://github.com/PaddlePaddle/Paddle/pull/67594

### 下周工作

1. 将qwen2moe SparseMoEBlock改成自动并行版本
2. 编写单元测试

### 导师点评
尽量在不改动源代码逻辑下实现自动并行版本