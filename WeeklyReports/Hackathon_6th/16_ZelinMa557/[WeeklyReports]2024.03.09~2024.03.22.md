### 姓名
马欣楷

### 实习项目
CINN 支持动态 Shape 专项（前端方向）

### 本周工作
本周主要工作如下：
1. 熟悉cinn前端动态shape符号推理相关代码，理清operation, value, dim_expr等数据结构之间的关系
2. 与导师讨论当前group lower过程中符号传递的问题，单纯通过输入张量的符号做替换不一定完备，需要在group中重新进行一次符号推导，大致工作流程如下  
    * 获取group所有输入value的shape expr
    * 对shape expr中外部传入的符号进行重新赋值
    * 对剩余value重新执行符号推导  

相关pr:
* https://github.com/PaddlePaddle/Paddle/pull/62951

### 下周工作

1. 继续优化动态shape符号推导流程
2. 完善 https://github.com/PaddlePaddle/Paddle/pull/62951 ,添加单元测试，验证流程效果

### 导师点评
欣楷学习能力很棒，能够很快熟悉相关设计并进行代码开发，当前任务进度符合预期，相关代码的学习可以整理成文档给大家分享下~
