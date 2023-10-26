### 姓名

詹荣瑞

Github ID：[zrr1999](https://github.com/zrr1999)

### 实习项目

PIR 核心组件建设与机制完善

### 本周工作

1. **熟悉 PIR 核心组件与机制**
    - 学习[设计文档](https://github.com/PaddlePaddle/community/tree/master/pfcc/paddle-code-reading/IR_Dialect)中相关内容。
2. **迁移部分算子到 PIR**
    - python/paddle/tensor/attribute.py: real, imag
    - python/paddle/tensor/logic.py: logical_and, equal_all
    - python/paddle/tensor/manipulation.py: flip, expand_as
    - python/paddle/tensor/math.py: isnan, logit
    - python/paddle/tensor/search.py: nonzero

相关PR：
- https://github.com/PaddlePaddle/Paddle/pull/58287

### 下周工作

1. 迁移 expand、solve、diag、linspce 等算子到 PIR。

### 导师点评
荣瑞这周完成了多个python api的pir迁移适配工作，对pir有了更多的了解，接下来再接再厉

