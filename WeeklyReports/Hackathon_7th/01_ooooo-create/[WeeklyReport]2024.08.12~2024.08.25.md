### 姓名

方国勇

### 实习项目

PIR 专项

### 本周工作

适配 PIR 单测：

- **修改单测写法**
    - https://github.com/PaddlePaddle/Paddle/pull/67230
        - test_slice_scatter，包含 pir mode 判断的方法，需要在 test_with_pir_api 下运行。
    - https://github.com/PaddlePaddle/Paddle/pull/67399
        - 完善 Optest `check_inplace_output_with_place` 中 PIR 跳过的判断逻辑，os.envs，加上 FLAGS 判断 
    - https://github.com/PaddlePaddle/Paddle/pull/67403
        - test_elementwise_nn_grad，`triple_grad_check` 属于单op的梯度检查，PIR下使用多 op 组合实现，加上 OldIRGuard

- **适配 API**
    - https://github.com/PaddlePaddle/Paddle/pull/67230
        - test_multiplex_op, 添加 api 下的类型检查
    - https://github.com/PaddlePaddle/Paddle/pull/67389
        - 适配 python/paddle/signal.py 中的 API
        - 同步 binary_cross_entropy_with_logits 旧 IR 下的 typeerror
        - 适配 paddle.view
    - https://github.com/PaddlePaddle/Paddle/pull/67452
        - 因为 PIR 下不支持 stride api，添加在动转静下 view tensor 被 inplace 使用导致行为不一致的报错
    - https://github.com/PaddlePaddle/Paddle/pull/67619
        - base.Dataloader, PyReader，在 iterable 为 True 时 create_py_reader，和静态图下没有差异，PIR 下减少相关 LOD 的检查，可以正常运行。
        - iterable 为 False 会在 Program 插入算子，因为被标记废弃，没有进行适配

### 下周工作

1. **PIR在分布式下的单测修复工作**

### 导师点评

good work
