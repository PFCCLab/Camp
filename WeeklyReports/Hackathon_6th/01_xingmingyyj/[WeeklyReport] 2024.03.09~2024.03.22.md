### 姓名
朱新明
### 实习项目
PIR 算子补全与兼容机制建设
### 本周工作
#### PIR动转静适配op_callstack属性
PIR静态图执行已经适配`op_callstack`属性，进一步的需要为动转静执行适配`op_callstack`。
因为在静态图下已经适配`op_callstack`所以这部分逻辑可以复用。但是动转静采用函数转写实现，静态图下添加的`op_callstack`信息
实际上是转写后的`call_stack`信息。这里需要进行转换。转换逻辑可以参考`update_op_callstack_with_origin_info`的实现。
具体转换时将`op_callstack`信息使用pybind11绑定到`Operator`的属性上，提供`getter`和`setter`方法。


PR链接：https://github.com/PaddlePaddle/Paddle/pull/62536

#### 解决kthvalue API动转静精度问题
`kthvalue`动转静执行时，出现动态图和静态图结果不一致的问题。静态图下输出`indices`的结果全为0.经过分析日志发现kernel选择没有问题，进一步打印kernel内的执行中间结果发现静态图组网时`indices`对应的value，在算子`kthvalue`中的类型和`scale`中的类型式不一致的。具体的在`kthvalue`中的类型是
`int64`而在`scale`中被解释为`int32`。所以定位到是`kthvalue`中的infermeta中dtype的设置问题。

PR链接：https://github.com/PaddlePaddle/Paddle/pull/62801

#### Review分布式算子注册以及单测修复相关PR
1. 定位PR[#62505](https://github.com/PaddlePaddle/Paddle/pull/62505)中`table_id`为非`Int32Attribute`问题。
2. 定位PR[#62836](https://github.com/PaddlePaddle/Paddle/pull/62863)中新旧IR下精度不一致的原因。
   
### 下周工作
1. 分析并修复`paddle.mode`和`paddle.bincount`API新旧IR下精度问题
2. Review分布式算子注册相关PR

### 导师点评
