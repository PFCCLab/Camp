### 姓名

方国勇

### 实习项目

PIR 专项

### 本周工作

适配 PIR 单测：

- 修复 [`test_adamw_op_(xpu)`](https://github.com/PaddlePaddle/Paddle/pull/66982) 单测。
    - 旧 IR 下使用 `paddle.static.create_global_var` 来创建 Variable 对象，在 PIR 下使用 `paddle.pir.core.create_persistable_value` 来替代。
    - 在 startup program 中初始化 Value（shadow_output), 在 main_program 中使用 data op 来定义一个 Value，两者在 Scope 中通过 name 来重用，parameter 也是。
    - `clone(for_test=True)`。
- [`test_while_op,test_norm_nn_grad`](https://github.com/PaddlePaddle/Paddle/pull/66785)
    - 打开 `shuffle_batch` pir 下 op 自动生成, 使用 paddle.full([0], 0, "int64") 来创建一个未赋值的 value。

其他相关PR
- https://github.com/PaddlePaddle/Paddle/pull/66785
- https://github.com/PaddlePaddle/Paddle/pull/66959
- https://github.com/PaddlePaddle/Paddle/pull/66816
- https://github.com/PaddlePaddle/Paddle/pull/66757
- https://github.com/PaddlePaddle/Paddle/pull/66734
- https://github.com/PaddlePaddle/Paddle/pull/66709


### 下周工作

1. **继续跟进PIR在基础框架侧的单测修复工作**

### 导师点评

good work
