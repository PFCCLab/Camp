### 姓名
王豪

### 实习项目
GraphNet 计算子图构建与推广

### 本周工作

1. 修复dtype_generalizer.py的bug：在判断计算图need_rewrite之前， parse_immutable_model_path_into_sole_graph_module()返回的trace_model不包含tensor_meta导致dtype_pass.need_rewrite(traced_model)返回总是false，在need_rewrite之前为trace_model加入tensor_meta，因此调用ShapeProp(traced_model).propagate(*inputs)

2. 将dtype_gen_test.sh改为标准脚本格式并对samll100_samples.txt的进行dtype generalizaion pass测试，并用 graph_net.torch.validate 验证生成的 samples of dtype generalization pass

3. 把dtype_generalizer.py做成了SamplePass的子类并放到torch/sample_pass目录下。


### 下周工作

1. 调试分析未通过的sample的原因
2. 开一个关于数据类型泛化的讨论区，并讨论如何集成进加工流程。

### 导师点评
true
