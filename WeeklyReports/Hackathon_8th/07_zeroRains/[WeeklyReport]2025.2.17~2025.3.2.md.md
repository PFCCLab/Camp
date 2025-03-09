### 姓名

卢林军

### 实习项目

大语言模型推理&服务化易用性提升专项

### 本周工作

本项目的主要工作是优化当前PaddleNLP大模型推理服务调用，本周主要工作如下：


1. 自定义算子二次封装与自动编译

收集PaddleNLP中使用的自定义算子(csrc文件夹中)，构建二次封装接口

继续更新自定义算子的调用参数，添加新增算子的二次封装。

CI已过

相关 PR：

- https://github.com/PaddlePaddle/PaddleNLP/pull/9794

2. 分析Append Attention使用的Kernel结构，尝试解耦其实例化方式

编译失败：指符号链接超出能够索引的范围

尝试将现有Dispatch宏展开替换成递归模板调用的形式，但本质上仍然要对Append Attention Kernel进行很多的实例化。编译时间仍然很长，最后也会编译失败。

通过编写脚本，将Append Attention的CascadeAppendAttentionKernel的实例化过程写在不同的文件，最后大概生成了9000多个实例化函数，最后仍然编译失败。

最后远乐老师从代码结构分析，将适配MLA所需要的head_dim与原本的GQA所需要的head_dim分成两个不同的宏定义进行Dispatch，解决了编译失败的问题。


### 下周工作

1. 推进当前自定义算子PR合入
2. 讨论自定义算子的多设备适配和自定义算子的默认参数设置问题

### 导师点评



