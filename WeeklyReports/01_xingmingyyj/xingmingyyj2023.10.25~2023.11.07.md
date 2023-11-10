### 姓名
朱新明
### 实习项目
算子规范和ProgramTranslator功能优化
### 本周工作
#### 1.修复exponential算子
遇到的问题及解决方法

**问题一**：exponential op的输出值具有随机性，新Ir下的测试逻辑是在旧Ir下运行一次op，新Ir下运行一次op，比较两者的输出结果。因为exponential op的两次输出不相同所以现有的测试逻辑不适用。解决方法是对对于此类op单独创建一个`new_ir_op_test_no_check_list`不对输出结果做相应的检查

PR链接：https://github.com/PaddlePaddle/Paddle/pull/58029

#### 2.修复randint算子
遇到的问题及解决方法

**问题一**：LOD_TENSOR的dtype类型会出现RAW类型,但是目前不支持RAW类型的翻译，所以这里仿照InferMeta的逻辑，将attribute中的dtype指定给Out<br>**问题二**：randint的输出同样具有随机性，所以这里将其加入`new_ir_op_test_no_check_list`对输出值不做检查

PR链接：https://github.com/PaddlePaddle/Paddle/pull/58295

#### 3.修复seed算子
遇到的问题及解决方法

**问题一**：该错误主要是由新旧ir下的`GetExpectedKernelType`不一致造成的，旧Ir下kerneltype为`INT32`,而新ir下的`GetExpectedKernelType`返回的是Out的dtype,修改新ir下的`GetExpectedKernelType`问题解决

PR链接：https://github.com/PaddlePaddle/Paddle/pull/58552

#### 4.修复sparse_momentum算子
遇到的问题及解决方法

**问题一**：`OpYamlInfoParser`在解析`runtime_info.kernel_param`时会将可变属性放入`kernel_fn_attr_params`这样对于新Ir下定义的sparse_momentum_op(定义了Scalar axis)会造成`AttributeMap`中不存在`axis`属性的问题。所以对于此类`legacy op`暂时将可变属性统一放入`kernel_fn_tensor_params`中。解决方案是需要给`OpYamlInfoParser`多增加一个属性，用来判断当前翻译的Op是非为`legacy op`。

PR链接：https://github.com/PaddlePaddle/Paddle/pull/58536

#### 5.修复repeat_interleave算子
遇到的问题及解决方法

**问题一**：新Ir下需要将repeat_interleave这个op根据输入`RepeatsTensor`翻译成`repeat_interleave_with_tensor_index`或者`repeat_interleave`这里增加RepeatInterLeaveOpTranscriber就可以实现，但是要注意对对应的grad op也要做相同的处理。<br> **问题二**：报错`the type of data we are trying to retrieve (float32) does not match the type of data (flaot64) `这个错误原因主要是组网时声明的tensor的dtype为float32但是测试文件中给出的数据是float64，旧Ir下的GetExpectedKernelType函数可以根据输入的数据的数据类型选择kernel,而新ir下暂不支持，新ir下根据x的dtype选择对应的kernel。所以对于此类问题需要修改单测文件，强制输入的数据类型和声明的dtype一致。

PR链接：https://github.com/PaddlePaddle/Paddle/pull/58379

#### 6.梳理静态图执行流程
结合单测执行时的输出日志，结合文档文档[static_graph_execution/20221230_static_graph_execution.md
](https://github.com/PaddlePaddle/community/blob/master/pfcc/paddle-code-reading/static_graph_execution/20221230_static_graph_execution.md)进一步理解了计算图的执行过程。

#### 7. 添加hook支持为test/white_list/new_ir_op_test_white_list内容自动按字典序排序
PR链接：https://github.com/PaddlePaddle/Paddle/pull/58543
### 下周工作
#### 1.修复下述算子
尝试修复的算子名单中还剩下real_imag,uniform_random_op,unique,uniform_random_bf16_op未修复，计划完成修复
#### 2.编写文档
编写pir算子修复文档，将推全任务发布社区
#### 3.修复推全名单中的部分算子

### 导师点评
新明本周在遗留单测修复上有很多工作，本项工作主要是服务于新IR的完备性和历史兼容性。新明目前阅读代码和调试bug上日渐娴熟，对于整体的执行流程也越来越熟悉，期待后续为飞桨pir的完善做出更大贡献。
