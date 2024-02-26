### 姓名
杨国浩

### 实习项目
子图验证&核心机制完善

### 本周工作

1. **修复动转静测试**
    * 在新 IR 下增加 FusedElemwiseAddActivationOp 修复相关测试 test_build_strategy。
    * 反复测试，并尝试修复的某些问题，没有彻底解决：
        1. 在 windows-inference 下 backend 错误。
        2. test_fuse_elewise_add_act_pass_pir 的精度无法对齐。在不开启 fuse 的情况下新单测也没办法通过，可能原因是 pir 下 start_up program 的参数权重初始化的随机种子无法固定。

2. **代码串讲**
    * 与导师讨论，完善补充代码串讲内容
    * 对 PIR 执行器部分的代码进行进一步学习理解。

### 下周工作

1. 解决新 IR 下 fused_elemwise_add_activation OP 的相关问题
2. 撰写社区发布的相关内容，将动转静单测修复任务发布。
3. 完成其他单测的修复

### 导师点评
国浩本周继续动转静单测的修复工作，本项工作主要是IR升级体系的功能测试的一部分。本周在修复 test_fuse_elewise_add_act_pass_pir 这个单测时遇到了很多困难，国浩在面对复杂问题时能耐心冷静的分析，仔细的寻找突破口，展现出了良好的素质，期待国浩的后续发挥。
