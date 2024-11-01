### 姓名

方国勇

### 实习项目

PIR 专项

### 本周工作

- 学习 [CINN 动态 shape 符号推导](https://github.com/PaddlePaddle/Paddle/issues/66444)
- 本地完成 Linux 下 CINN 的编译
- 尝试完成 `det`, `is_empty`, `eye` 的符号推导接口
- `pd_op.h`, `pd_op.cc` 是在 cmake 阶段自动生成的，`pd_op.h` 都会自动生成*声明代码*，.cc 文件根据 ops.yaml 进行生成*实现代码*，所以需要重新 cmake
- 发现 ci 上单测通过，但是新增代码覆盖率为 0
### 下周工作

- 继续完成符号推导工作
- 分析 ci 原因

### 导师点评
