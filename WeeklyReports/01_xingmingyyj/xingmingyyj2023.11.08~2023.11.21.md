### 姓名
朱新明
### 实习项目
算子规范和ProgramTranslator功能优化
### 本周工作
#### 1.整理待修复Op单测名单
由于之前的推全名单中的op单测测试的op没有对应的API调用同时也没有对应的PASS规则使用到对应的Op,这种Op在后续是不会被使用到的,
所以目前没有必要进行修复.将这些Op对应的单测剔除推全名单.

#### 2.编写op单测修复issue
编写了op单测推全issue,在issue中对需求背景,单测修复流程,op单测执行流程,之前遇到的一些问题进行介绍.并且与导师进行讨论,
完成了修改.计划将issue发布社区.

#### 3.编写Parser实现分享文档
本周计划参加codereading活动，分享之前实现的`Parser`,所以重新编写了文档.文档主要分析了在实现`Parser`时是怎样的一个设计思路,以及
遇到了那些比较困难的问题是怎样解决的,并且思考了`Parser`另一种实现方案.

#### 4.修复test_unique单测
遇到的问题如下:<br>
1. test_unique在新Ir下执行报错为PreconditionNotMetError: Tensor holds no memory. Call Tensor::mutable_data firstly..这里的问题是由新Ir下默认将旧Ir下的unique只翻译成新Ir下的unique导致的.在旧Ir下unique会根据属性`is_sorted`的值选择unique或者unique_raw两个`kernel`执行.在新Ir下不存在这样的机制，所以需要根据is_sorted的值将旧Ir下的unique翻译为新Ir下的unique或者unique_raw两个OP.这里在新Ir下补充了unique_raw的定义.<br>
2. 修复问题1后在GPU环境上运行，在GPU版本的`kernel`中发生空指针异常，这是选`kernel`的逻辑存在问题，旧Ir下通过`GetReduceGradExpectedKernelType`在GPU环境下选择CPU中的`kernel`,新IR下不适配`GetReduceGradExpectedKernelType`导致在GPU环境下`kernel`选择出现问题,暂时尚未处理,已记录在issue.

#### 5.修复单测test_uniform_random_bf16_op
遇到的问题如下:<br>
`input`对应的`Variable`在构建`PhiContext`时`holder_`为空。在python侧`_StandaloneExecutor`执行run函数时传入的`feed_names`为空，在旧IR中会在`program_interpreter`中执行run函数,对于`program_interpreter`初始化`Variable`的机制,他会在构建`Varibale`时就将其初始化.而`pir_interpreter`不会先初始化`Variable`,它根据feed_names为输入变量初始化,所以如果feed_names为空,会导致input不会被初始化,导致后面运行报错.解决方案是在exe.run()中加入`feed`.
### 下周工作
#### 1.根据推全名单继续修复Op单测
#### 2.将issue发布社区

### 导师点评
新明积极参与分享，对过去的工作做了相对完善和系统的总结，同时也能比较深入的思考遇到的问题，为下一步工作的开展做了很好的准备。
