### 姓名
王龙志

### 实习项目
量化算子集成

### 本周工作

1. **编写将  matmul_v2 和 quant dequant op 融合替换成 quant_linear 的 pass**<br>
该 pass 将 quant dequant dequant_weight 以及 matmul_v2 以及后面的 elementwise_add op 替换成 quant_linear op<br>
相关 PR: https://github.com/PaddlePaddle/Paddle/pull/58637<br>
![结果展示1](./images/quant_linear_fuse.png)
2. **完成 bert 模型的导出和量化**
完成 bert 模型的量化，为后面原生推理与 TRT 推理在语言大模型上进行对比分析打下基础
![结果展示2](./images/bert_quantinized.png)

3. **修复 paddle trt 在 int8 模式下的推理 bug**<br>
相关 issue: https://github.com/PaddlePaddle/Paddle/issues/58674<br>
相关 PR: https://github.com/PaddlePaddle/Paddle/pull/58672

4. **学习 paddle trt 相关的 pass**<br>
继续学习 paddle trt 的有关 pass 的实现，为后续继续编写 pass 增加熟练度

### 下周工作
1. 该pass目前只完成了基本功能，可能还有不完善的地方, 待与导师沟通之后再进行完善
2. 编写其他算子融合的 pass
3. 学习其他竞品的相关优化思路

### 导师点评
