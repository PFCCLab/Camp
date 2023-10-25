### 姓名
张钰钦

### 实习项目
新IR Pass建设

### 本周工作

详见 https://github.com/yuanlehome/Hackathon/wiki/%E6%96%B0IR%E5%B8%B8%E9%87%8F%E6%8A%98%E5%8F%A0#%E6%8E%A8%E7%90%86%E6%B5%81%E7%A8%8B%E6%A2%B3%E7%90%86

1. **梳理飞桨目前执行器的流程**

#### 0. 训练阶段参数初始化与 scope 构建
1. paddle.nn 中的函数会将参数初始化的 op 追加到 start program 中
2. 执行器执行 start program
3. 在 NewIRInterpreter 阶段 build scope，把 op 用到的输入输出 var 都构造出来并放到 global scope 里
4. NewIRInterpreter 按序执行 op kernel。之后，初始化后的参数就在 global scope 里了
5. 执行器执行 main program，可以从 global scope 里拿到参数
6. ...

#### 1. 执行器python前端
网络和参数都就绪之后，调用 Executor 的 run() 方法执行，这里以新执行器为例。新执行器会：
1. 创建 StandaloneExecutor实例
2. feed data
3. 调用 StandaloneExecutor::run
#### 2. 执行器c++后端
StandaloneExecutor 的构造函数依次做了几件重要的事情：
1. TranslateLegacyProgramToProgram，旧 IR 被翻译成新 IR
2. 常规 pass，如常量折叠、算子融合、死代码消除等
3. PdOpLowerToKernelPass，新 IR 绑定到 kernel
4. inplace pass
5. 创建 InterpreterCore，将 impl 构造为 NewIRInterpreter	**（直到这一步才用到 scope_，之前都没用到）**

其中真正负责执行的是 NewIRInterpreter。

2. **新IR常量折叠问题分析**
#### 1. 新 IR 常量折叠的主要改写逻辑
1. 根据 op 创建 temp_program
2. PdOpLowerToKernelPass，根据 temp_program 构造 kernel_program
3. 创建 InterpreterCore 并执行
4. 根据 fetch_list 取出 out_tensor
5. 根据 out_tensor 构造 pir::Parameter
6. 在 scope_ 中创建新 param_var，并把 out_tensor 赋值给 param_var
7. 在原 program 中 SetParameter
8. 插入 get_parameter_op 并替换子图

#### 2. 问题分析
可以看到，新IR常量折叠里主要存在两个问题：

问题一：需要从原 program 中获取 Parameter，但我们在 TranslateLegacyProgramToProgram 时，只记录了 param_name，并没有创建 Parameter 对象（见上面流程梳理3.1）。目前我们仍然是把 param 以 var 的形式存储在 scope 里了。而在 pass 阶段，并没有传入 scope，也就没法获得原 program 的参数。

问题二：需要单独构造出 temp program，并构造 InterpreterCore。其实可以直接调用 op 的 kernel。

3. **梳理 codegen 流程**

一个很自然的想法是，能不能通过 codegen 的方式为每个 op 生成 fold 方法？为此，我们梳理一下 op codegen 的大概流程
在 gen.py 的 OpGenerator 里：

1. 根据 op_yaml_files 和 op_compat_yaml_file 解析生成 op_compat_item
2. 构造 OpInfoParser(op, op_compat_item)
3. 根据上面解析出的结果，格式化 OP_INFO_TEMPLATE，用于生成算子的 GetOpInfo() 方法。这东西很重要。**OpInfoTuple 把所有元信息和 op 打包在一起**
4. 根据模板生成头文件
5. 根据模板 CC_FILE_TEMPLATE 生成源文件

理论上拿到 OpInfoTuple 就可以找到 kernel 并构建 InferMetaContext 和 KernelContext 了。只要把 KernelContext 传给 kernel 就能执行了。（需要先 BuildScope，为 kernel 的 output 在 scope 里申请出空间）
所以我们可以看出，并不需要额外的 codegen 了。想运行指定的 op，只要拿到它的 OpInfoTuple，然后传入 scope 就可以。

4. **调研**
调研 tvm、mlir、oneflow 中常量折叠的实现方案



### 下周工作

1. 搭建 新 ir 常量折叠的 demo 并跑动

### 导师点评
对飞桨框架新IR的执行流程学习比较细致，本周工作按照预期推进，继续保持！
