### 姓名
杨国浩

### 实习项目
子图验证&核心机制完善

### 本周工作

1. **修复动转静测试**
    * 在新 IR 下增加 memcpyOp 修复相关测试 test_tensor_memcpy_to_cpu 和 test_tensor_memcpy_to_gpu。

2. **修复了新 IR 下 memcpyOp 选 kernel 的相关问题。**
    1. 测试的过程中发现了 memcpyOp 在新 IR 下 GPU 到 CPU 的拷贝出现错误。最后成功定位解决问题。过程中与导师反复讨论，并且学习到了很多调试技巧，对整体流程梳理更加清晰。

3. **撰写代码串讲的相关内容**
    1. 初稿完成并与导师沟通，还需补充内容打磨完善。
### 下周工作

1. 完成在新 IR 下添加 fused_elemwise_add_activation OP
2. 完成串讲材料的补充，和导师进行第二次讨论
3. 对 test_len、test_seq2seq 单测错误的分析定位。
4. 对某部分代码的深入学习和进一步理解，体现为学习笔记等

### 导师点评