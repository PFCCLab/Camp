### 姓名
马贺达

### 实习项目
CINN 静态 shape 下鲁棒性和性能优化

### 本周工作

1. **test_sub_graph_54.py**

	* 新增 pd_op.meshgrid ，解决 `NotImplementedError: (Unimplemented) pd_op.meshgrid DOES NOT have InferSymbolicShapeInterface!` 的问题
（相关PR：https://github.com/PaddlePaddle/Paddle/pull/62710 ）
	* 修复 ConcatOpInferSymbolicShape 中存在一个小 bug ，解决了 `bad option access` 的问题
（相关PR：https://github.com/PaddlePaddle/Paddle/pull/62992 ）
	* 尝试解决 reshape 未生效的问题，正在推进
（相关issue：https://github.com/PaddlePaddle/Paddle/issues/62976 ）

2. **test_sub_graph_69.py**

	* 新增 pd_op.nonzero ，解决 `NotImplementedError: (Unimplemented) pd_op.nonzero DOES NOT have InferSymbolicShapeInterface!` 的问题
（相关PR：https://github.com/PaddlePaddle/Paddle/pull/62987 ）

### 下周工作

1. 修复编译器子图 CE 建设 Detection 目录下 bug 5-6个

### 导师点评
请联系导师填写
