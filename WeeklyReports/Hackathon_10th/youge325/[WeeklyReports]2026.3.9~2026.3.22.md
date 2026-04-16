### 姓名

谢润明

### 实习项目

Paddle C++ API生态兼容建设

### 本周工作

1. 修复接入 FlashMLA 时发现的多重定义错误，将实现移至 Utils.cpp 文件下

   https://github.com/PaddlePaddle/Paddle/pull/78244

2. 对齐 pin_memory 相关接口，并将 tensor 创建方法统一委托给含 TensorOptions的重载

   https://github.com/PaddlePaddle/Paddle/pull/78255

3. 新增 TypeMeta 类，用于替换暂代功能的 ScalarType 类

   https://github.com/PaddlePaddle/Paddle/pull/78257

4. 重命名不规范的单测文件，方便回归测试

   https://github.com/PaddlePaddle/Paddle/pull/78266

5. PaddleCppAPITest 仓库下新增部分文档与对齐测试

   https://github.com/PFCCLab/PaddleCppAPITest/pull/49

   https://github.com/PFCCLab/PaddleCppAPITest/pull/56

6. 使用已合入 Paddle 仓库的兼容接口，消除 DeepEP 中的部分 diff 

   https://github.com/PFCCLab/DeepEP/pull/10


### 下周工作

1. 继续消除 DeepEP 中的 diff
2. 为 Allocator、Storage 等涉及到底层指针引用计数的接口添加详细的兼容架构文档
3. 补充已合入的 Generator、Stream 等相关接口的对齐测试
4. 对齐已经发现的接口差异点，并再次排查是否有遗漏的差异点，同时为无法对齐的接口添加详细的文档

### 导师点评