### 姓名

谢润明

### 实习项目

Paddle C++ API生态兼容建设

### 本周工作

1. `TensorBase.h` 下新增 `sym_size(dim)` `sym_stride(dim)` `sym_sizes()` `sym_strides()` `sym_numel()`  兼容接口

   https://github.com/PaddlePaddle/Paddle/pull/77301

   https://github.com/PFCCLab/PaddleCppAPITest/pull/18

2. `TensorBase.h` 下新增 `is_same(other)` `use_count()` `weak_use_count()` `is_contiguous_or_false()` `toString()`  兼容接口

   https://github.com/PaddlePaddle/Paddle/pull/77388

   https://github.com/PFCCLab/PaddleCppAPITest/pull/21

3. `TensorBase.h` 下新增 `_is_zerotensor` `_set_zero` `is_conj` `_set_conj` `is_neg` `_set_neg` 兼容接口

   https://github.com/PaddlePaddle/Paddle/pull/77399

4. `PaddleCppAPITest` 仓库更新 `TensorBase.h` 文档

   https://github.com/PFCCLab/PaddleCppAPITest/pull/15

### 下周工作

1. 继续完善 `TensorBase.h` 头文件

### 导师点评