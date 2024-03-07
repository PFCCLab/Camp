### 姓名
朱新明
### 实习项目
PIR 算子补全与兼容机制建设
### 本周工作
#### 统计新旧IR下算子签名差异
1. 统计旧IR下算子全集
   
   旧IR下算子通过`REGISTER_OPERATOR`和`REGISTER_OP_WITHOUT_GRADIENT`注册，使用正则表达式匹配所有的代码段，得到旧IR下注册算子全集。与excel中给出的旧IR算子全集做比较，互相补充。对于框架中注册的旧算子可以通过`op_proto`获取除`inplace`以外的所有信息。`inplace`信息可以通过在C++侧使用`OpInfoMap`获取。使用脚本将上述信息写入yaml中。对于框架中未注册的算子需要手动补充。
2. 统计新IR下算子全集
   
   新IR下算子签名通过yaml可以直接拿到，但是需要进行格式变换，新IR下的算子签名将`Attribute`和`Input`合并在一个key中，为了方便对比需要将其拆分。

3. 将`op_compat.yaml`信息应用于旧IR算子签名中

   `op_compat.yaml`中记录了新旧IR下签名之间的映射关系，需要先将这部分信息同步到旧IR算子签名中，方便后续对比。

4. 比较新旧IR下算子签名差异
   
   主要统计新旧IR下算子签名的如下差异：
   - 新增算子：PIR中存在但是旧IR不存在的算子
   - 缺失算子：旧IR存在但是PIR中不存在
   - 算子签名变更，主要包括新增/删除参数，参数类型，参数属性变更

#### PIR静态图适配op_callstack属性
Pir静态图适配`op_callstack`属性，对齐旧IR下的报错机制。主要实现思路是在静态图组网时为op插入`op_callstack`属性，该属性记录了python侧的调用栈，在执行器遇到异常时，解析op中的`op_callstack`属性，将python调用栈信息抛出。由于，Paddle dialect层未引入python库依赖，所以考虑在其上层`PyObject->Cpp object`实现python调用栈的获得与`op_callstack`属性的插入。

PR链接：https://github.com/PaddlePaddle/Paddle/pull/62139

#### Review分布式算子注册相关PR

PR链接：
- https://github.com/PaddlePaddle/Paddle/pull/62270
- https://github.com/PaddlePaddle/Paddle/pull/62369
- https://github.com/PaddlePaddle/Paddle/pull/62443
- https://github.com/PaddlePaddle/Paddle/pull/62416
- https://github.com/PaddlePaddle/Paddle/pull/62412

### 下周工作
1. PIR动转静适配op_callstack属性
2. Review分布式算子注册相关PR

### 导师点评


