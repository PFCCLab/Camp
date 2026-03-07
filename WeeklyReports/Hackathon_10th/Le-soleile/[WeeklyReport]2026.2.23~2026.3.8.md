### 姓名

杨晓春

### 实习项目

Paddle C++ API生态兼容建设

### 本周工作

1. 新增若干兼容 `Pytorch` 的 `C++` 接口以及单测
  - 接口概览：register_hook、any、chunk、rename、new_empty、new_full、new_zeros、new_ones、resize_、expand、expand_as等
2. 补全针对新增接口各项参数、输出是否与 `Pytorch` 完全对齐的测试，增加`torch`兼容层该测试覆盖率到60%以上、记录行为差异
 
### 下周计划

1. 修改需要对齐的相关兼容接口
2. 进一步添加接口兼容性测试、提升覆盖率到95%
