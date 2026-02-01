### 姓名

谢润明

### 实习项目

Paddle C++ API生态兼容建设

### 本周工作

1. `TensorBase.h` 下新增 `generic_packed_accessor<T, N>()`  `packed_accessor32<T, N>()` `packed_accessor64<T, N>()` `is_non_overlapping_and_dense()` `has_names()` 兼容接口

   https://github.com/PaddlePaddle/Paddle/pull/77498

   https://github.com/PFCCLab/PaddleCppAPITest/pull/25

2. `TensorBase.h` 下新增 `is_sparse` `is_sparse_csr` 兼容接口，并补充tensor的创建方法，和Pytorch对齐，支持创建稀疏张量

   https://github.com/PaddlePaddle/Paddle/pull/77581

   https://github.com/PFCCLab/PaddleCppAPITest/pull/23

3. `TensorBody.h` 下新增 `flatten` `unflatten` `unflatten_symint` `narrow_copy` `narrow_copy_symint` `narrow` `narrow_symint` 兼容接口，同时规范了`TensorBody.h`下各类ops撰写标准，详见pr

   https://github.com/PaddlePaddle/Paddle/pull/77544

   https://github.com/PFCCLab/PaddleCppAPITest/pull/26

4. `TensorBody.h` 下新增 `is_pinned` `reciprocal` `reciprocal_` `detach` `detach_` `select` `masked_select` `tensor_split` `split` `unsafe_split` `split_with_sizes` `unsafe_split_with_sizes` `hsplit` `vsplit` `dsplit` 兼容接口，使用新的规范

   https://github.com/PaddlePaddle/Paddle/pull/77614

5. `PaddleCppAPITest` 仓库改写测试用例

   https://github.com/PFCCLab/PaddleCppAPITest/pull/24

### 下周工作

1. 继续完善 `TensorBody.h` 头文件
2. 改写 `TensorBody.h` 中的接口，将实现移至ops目录下

### 导师点评