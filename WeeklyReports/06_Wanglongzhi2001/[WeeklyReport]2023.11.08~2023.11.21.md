### 姓名
王龙志

### 实习项目
量化算子集成

### 本周工作

1. **完善 quant_linear_fuse_pass 和对应单测以及修复 ci**<br>
目前 pass 的编写和单测都已完善， ci 也已经全部通过。
2. **编写 weight_only 的 PIR 的 Pass**
编写 weight_only 的 pass 以及对应单测，目前 pass 和单测已经初步编写完成，还在完善和 debug 中。
3. **学习 PIR 相关的 pass 写法和单测**<br>
学习相关 pass 和单测的写法为后续编写 PIR 的 pass 打基础。

### 下周工作
1. 继续完成 weight_only 的 Pass 与相关单测。
2. 与导师沟通并开发后续工作。

### 导师点评

第一个PR已经顺利合入，补全了paddleslim到paddleinference原生量化推理的关键桥梁；后续quant_linear也需要收敛到PIR当中，所以PIR的掌握和开发至关重要；关于后续工作需要关注具体模型的性能收益，对于PTQ量化我的建议还是以Bert为例子，WINT8量化可以以llama为例，以性能优化为纲领补全或者优化算子。
