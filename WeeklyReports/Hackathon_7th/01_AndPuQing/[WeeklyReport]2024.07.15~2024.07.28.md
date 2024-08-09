### 姓名

梁嘉铭

### 实习项目

PIR 专项

### 本周工作

本双周工作集中在对于 `PIR mode` 下 `Coverage` 流水线修复工作，主要包括：

1. **Adapt adadelta/adagrad/adam/adamax Unit Test**

    - 修复 `adadelta/adagrad/adam/adamax` 单元测试，使其能够在 `PIR mode` 下正常运行
    - 其中阅读了`paddle.static.amp.decorate`的部分实现。

    相关PR
    - https://github.com/PaddlePaddle/Paddle/pull/66078

2. **Adapt adamw/binary_cross_entropy_with_logits_op/blha_get_max_len_op/assign_pos unit tests**

    - 修复 `adamw/binary_cross_entropy_with_logits_op/blha_get_max_len_op/assign_pos` 单元测试，使其能够在 `PIR mode` 下正常运行
    - 阅读了 `binary_cross_entropy_with_logits_op` 的 `prim op` 实现 

    相关PR
    - https://github.com/PaddlePaddle/Paddle/pull/66114
    - https://github.com/PaddlePaddle/Paddle/pull/66384

3. **Fix pull_box_sparse/asgd unit tests**

    - 修复 `pull_box_sparse/asgd` 单元测试，使其能够在 `PIR mode` 下正常运行
    - 了解了 `_C_ops` 与 `_eager_ops` 的区别。在调试过程中根据报错信息还阅读了`op_gen.py`等部分实现，并为其添加了`Typing`注释，使代码更加清晰。
    - 其中根据错误信息，修复了 `pull_box_sparse` 的 `data_type` 问题

    相关PR
    - https://github.com/PaddlePaddle/Paddle/pull/66364

4. **CINN编译器符号推导**

    - 了解了 `CINN` 编译器的符号推导基本组件，并为其添加了 `Eigh、Eigvalsh、Eigvals` 符号推导支持

    相关PR
    - https://github.com/PaddlePaddle/Paddle/pull/66582
    - https://github.com/PaddlePaddle/Paddle/pull/66637


### 下周工作

1. **继续跟进PIR单测修复工作**

2. **深入阅读PIR相关组件**

### 导师点评


