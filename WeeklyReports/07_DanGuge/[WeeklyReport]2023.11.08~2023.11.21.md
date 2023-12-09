### 姓名
吴晨灿

### 实习项目
开源模型加速复现

### 本周工作

1. **基于fused VIT完成weight_only_int8/4**

	* 在[PaddleClas](https://github.com/PaddlePaddle/PaddleClas)的fused vit中实现了weight_only_int8的推理
	* weight_only_int8精度符合预期，加速1.4倍左右（batch_size=1/2，硬件原因没法进行更大的测试）
	* 相关PR：https://github.com/PaddlePaddle/PaddleClas/pull/3034
	* 目前，V100无法进行更深入的wint8或者ptq的测试，这部分暂停了


### 下周工作

1. ptq paddlenlp代码学习
2. 静态图trt的推理对比
3. wint性能分析

### 导师点评
1. 吴同学完成了基于融合 kernel 的 VIT 完整实现，并在 wint8/4 下精度和推理速度对齐，在 wint8 下推理加速提升近 40%。
2. 接下来还有 Qwen 大模型需要加速复现工作。
