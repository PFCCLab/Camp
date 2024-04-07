### 姓名
朱新明
### 实习项目
PIR 算子补全与兼容机制建设
### 本周工作
#### 解决paddle.bincount API动转静执行失败问题
`paddele.mode`API在静态图组网执行时，后续算子使用`mode`算子输出的`value`报错。主要原因时该tensor持有的数据的类型和期待获取的数据类型不一致。
猜测是`InferMeta`中对输出类型的推导错误导致的。根据`Kernel`中的为输出`value`申请内存的相关代码可以确定是现有的类型推逻辑导致的。结合API的输入限制，修改`InferMeta`中对输出类型推导逻辑。
PR链接：https://github.com/PaddlePaddle/Paddle/pull/62995
#### 解决paddle.mode API动转静精度问题
`paddle.mode`动转静执行时，出现动态图和静态图结果不一致的问题。静态图下输出`indices`的结果全为0.经过分析日志发现kernel选择没有问题，进一步打印kernel内的执行中间结果发现静态图组网时`indices`对应的value，在算子`mode`中的类型和`scale`中的类型式不一致的。具体的在`mode`中的类型是
`int64`而在`scale`中被解释为`int32`。所以定位到是`mode`中的infermeta中dtype的设置问题。
PR链接：https://github.com/PaddlePaddle/Paddle/pull/62995
#### 定位paddle.mean API动转静执行失败问题
`paddle.mean`API在动转静时翻译失败。主要原因是现在的`ProgramTranslator`没有支持`VarDesc*`。以及和导师确定修复方案，计划扩展支持`VarDesc*`，以及`vector<VarDesc>`
#### review PR
Review 分布式算子注册以及单测修复issue相关PR。
   
### 下周工作
1. 完成`paddle.mean` API的动转静执行失败修复
2. Review分布式算子注册以及单测修复相关PR

### 导师点评
