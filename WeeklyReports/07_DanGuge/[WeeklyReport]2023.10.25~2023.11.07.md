### 姓名
吴晨灿

### 实习项目
开源模型加速复现

### 本周工作

1. **学习PaddleNLP的FusedTransformer**

	* [FusedTransformer](https://github.com/PaddlePaddle/PaddleNLP/blob/develop/paddlenlp/experimental/transformers/fused_transformer_layers.py)
	* 学习和测试PaddleNLP的FusedTransformer中的融合算子
	* 了解如何组合融合算子进行推理加速


2. **完成Fused Vision Transformer**

	* 在[PaddleClas](https://github.com/PaddlePaddle/PaddleClas)的model_zoo中添加fused vit
	* 实现了在fp32上精度和推理速度对齐，在fp16上推理加速1.1～1.3倍的效果
	* 相关PR：https://github.com/PaddlePaddle/PaddleClas/pull/3034

1. **问题疑惑与解答**

	* fused算子是如何做到对原计算的加速的？
	
        答：比如一个linear layer + norm layer，linear layer的bias加操作和norm操作都是element-wise操作，即逐元素操作，如果单独实现这些操作，只会对元素操作一次然后就写回，是访存密集的，容易在cuda kernel计算之间产生空隙，所以我们可以合并多个element wise操作，来减少密集的存储访问和写会，从而提高计算速度。


### 下周工作

1. 使用fused vit测试实际业务场景，看看加速效果

### 导师点评
1. 吴同学在过去两周完成了基于融合 kernel 的 VIT 完整实现，并在 fp32/fp16 下精度和推理速度对齐，在 fp16 下推理加速提升近 30%。
2. 接下来要基于融合 VIT 组网进行 wint8 和 ptq 的支持，继续加油。
