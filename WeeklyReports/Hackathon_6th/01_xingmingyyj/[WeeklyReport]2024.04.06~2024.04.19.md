### 姓名
朱新明
### 实习项目
PIR 算子补全与兼容机制建设
### 本周工作
#### 分析mean API动转静执行的问题
`paddle.mean`API在动转静时翻译失败。主要原因是现在的ProgramTranslato没有支持`VarDesc*`。在OpTranslator中适配从`mutable_attributes`中
得到`VarDesc*`,进而得到VarName，从`param_map`得到对应的`value`。这里从`param_map`中的到`value`的前提是该`VarDesc*`已经被前述Op定义。但是在
动转静时没有插入对应的data_op。尝试进行插入，在实际执行时发现在`scope`中的Tensor对应的`holder_`为空，所以动转静时在新IR和就IR下都会失败。
ProgramTranslator对`VarDesc*`的支持已经进行了适配。
#### 分析fake_quantize_range_abs_max执行时OutScale的holder_为null问题
在`fake_quantize_range_abs_max`的参数`is_test`为`True`时，`OutScale`的`holder_`为`null`。因为当输入`x`的dtype为`float16`时，会选择在GPU上的Kernel执行。中间框架会插入`memcpy_d2h`算子，该算子负责将数据从GPU拷贝会主机。但是当`is_test`为`True`时，Kernel中并没有为`OutScale`中分配显存，所以会执行失败。
目前的解决方法是当`is_test`为`True`时，将输出`OutScale`和`OutScales`加入到no_check_set中，在no_check_set中的属性不会通过`fetch`算子取出，所以一九不会
涉及插入`memcpy_d2h`算子。
#### review分布式算子注册issue相关PR
在review `pull_gpups_sparse`算子注册时发现TestOpWithBackwardTranslator中并不会成功插入反向算子，原因是out的`stop_gradient`的属性值默认为`True`。
现在已经修正。

### 下周工作
1. 推进分布式算子注册issue的合入，完成该issue中的内容
2. review算子单测任务相关PR

### 导师点评
