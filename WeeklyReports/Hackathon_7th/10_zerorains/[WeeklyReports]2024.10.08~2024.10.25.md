### 卢林军

### 实习项目

推理 Predictor 及 IR Pass 建设

### 本周工作

1. Debug ChatGLM2在开启block_atten的推理场景下精度无法对齐的问题

具体来说这个问题出在了rope计算上，在ChatGLM2模型中rope应该只用了一半的head_dim进行计算，因此需要再rope计算时，将一半的head_dim进行兼容设置，从而保证计算精度。但实际实现后，发现仍然无法对齐精度。

2. 尝试解决现有CI中部分单测挂掉的问题

修复单测tests/llm/test_predictor.py::PredictorTest_1___internal_testing___tiny_fused_bloom::test_wint8，其由于在bloom模型计算alibi的时候，type从float16变成了float32，从而导致了后续计算过程中权重和变量类型不同而产生的计算异常。

- https://github.com/PaddlePaddle/PaddleNLP/pull/9307

3. 学习SageAttention的原理和源码

### 下周工作

1. 调研Huggin Face中AutoModel的实现方式，思考在PaddleNLP中实现类似的模型加载方式
2. 参考append_atten的集成PR，思考SageAttention集成到PaddleNLP中的方式

### 导师点评

