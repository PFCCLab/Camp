### 姓名
杨新宇

### 实习项目
CPU 融合算子 / GPU 算子融合 pass

### 本周工作

详见 https://github.com/yuanlehome/Hackathon/wiki/%E6%96%B0IR-Pass-%E6%8E%A8%E7%90%86%E5%8D%95%E6%B5%8B%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD%E6%90%AD%E5%BB%BA


1. **新IR-Pass-推理单测基础设施搭建**

尝试两种方式搭建新IR下的Conv2d和BN组成的网络，但是遇到问题，暂时搁置。

2. **完成fuse_conv pass的迁移**

参见PR https://github.com/PaddlePaddle/Paddle/pull/58252.

将 pattern_rewrite_test.cc 中实现的 Conv2dFusePass 迁移到了 paddle/fluid/pir/transforms/fusion 目录下，并完成了 CMakeLists.txt 的更新。

3. **自动混合精度pass迁移工作的准备**

学习旧IR下自动混合精度pass的实现，准备基于新IR实现自动混合精度pass。

### 下周工作

1. 撰写自动混合精度pass的实现方案

### 导师点评
前两项工作暂时搁置，后续全人力投入新IR下自动混合精度pass的实现上，多沟通多交流，预祝如期完成工作。
