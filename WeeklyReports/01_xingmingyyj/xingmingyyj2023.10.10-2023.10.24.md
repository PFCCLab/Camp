
### 姓名
朱新明
### 实习项目
算子规范和ProgramTranslator功能优化
### 本周工作
#### 1.阅读Paddle基于Yaml配置自动生成算子定义逻辑
新Ir下定义的算子定义由框架自动生成，注册算子时只需要将算子的关键信息(attrs,outputs,kernel,infermeta...)等信息配置在对应的yaml文件中即可。代码生成逻辑主要由`paddle/fluid/pir/dialect/operator/ir/CMakeLists.txt`完成。通过阅读上述代码了解算子定义自动生成流程。
#### 2.梳理静态图执行流程
主要通过学习文档[static_graph_execution/20221230_static_graph_execution.md
](https://github.com/PaddlePaddle/community/blob/master/pfcc/paddle-code-reading/static_graph_execution/20221230_static_graph_execution.md
)了解了计算图的组网过程、执行过程、预分析阶段和调度执行阶段所做的主要工作，初步明白了一个算子从python侧到底层的执行过程。
#### 3.学习新Ir计算图翻译机制
新Ir为了支持旧ir计算图提供了translator，该部分相关代码主要在`paddle/fluid/ir_adaptor/translator`文件夹下，通过`op_compat.yaml`文件定义新旧ir下的算子属性映射，该部分定义的信息会被自动解析到`op_compat_info.cc`中，translator执行新旧ir算子翻译时会参考相关信息。通过阅读代码熟悉了一些特殊算子翻译自定义`Transcriber`方法。
#### 4.尝试修复部分算子
尝试修复了test_dpsgd_op、test_exponential_op、test_norm_all等算子，相关进度在[#issue58266](https://github.com/PaddlePaddle/Paddle/issues/58266)中
#### 5.问题疑惑与解答
(1) xpoential op和 randint op测试精度失败问题

解决方法：是使用随机数导致的新旧ir下两次测试不一致。分析op_test.py中_check_ir_output的实现，引入新的flag，执行exponential和randint时打开该flag，执行空的check_method，在cmake中设置flag可以参考pr #55117和#55857

(2) 什么情况下需要将op加入LegacyOpList
解决方法：kernel的注册有两种形式，对应宏，PD_REGISTER_STRUCT_KERNEL和PD_REGISTER_KERNEL。如果是使用PD_REGISTER_STRUCT_KERNEL注册的kernel则需要将opname加入LegacyOpList

(3) 如何确定异常发生的位置？

解决方法: 首先确定是哪个单测错了，然后再确定这个单测在测试什么，这个需要熟悉op_test.py中的_check_ir_output，_check_ir_grad_output测试逻辑以及相关调用。所有日志都打开，确定抛出异常的位置，一般来说报错代码在中断位置附近。

(5) The kernel with key (CPU, Undefined(AnyLayout), int64) of kernel `seed` is not registered. 

解决方法：输出计算图，观察日志，尝试确定原因

(6) 新Ir可变Attribute的处理

解决方法：旧IR下支持可变Attribute的方式有两种。第一种是类似于top_k算子在旧ir下的定义，同时设置Tensor K 和 int k两个参数，但是会出现省略int k或者省略Tensor K的情况，对于省略int k的情况不做特殊处理。对于省略Tensor K的情况，会出现Tensor K未定义的问题，这样可以甄别。第二种是给Attribute添加一个可以为Tensor的属性。

### 下周工作
#### 1.修复下述算子
exponential，randint，real_imag, seed_op, sparse_momentum，repeat_interleave
#### 2.继续熟悉算子执行流程

### 导师点评
请联系导师填写
