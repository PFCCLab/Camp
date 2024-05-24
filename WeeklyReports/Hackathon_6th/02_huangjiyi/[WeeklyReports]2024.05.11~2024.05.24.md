### 姓名

黄济懿

### 实习项目

PIR 控制流专项，PIR 算子 yaml 定义规范

### 本周工作

1. 实现 YieldInstruction 以解决 YieldOp 的输入变量需要跳过 GC 所引发的内存泄露问题
   - https://github.com/PaddlePaddle/Paddle/pull/64234
2. 增加 WhileOp 中的 loop_vars 对 -1 shape 的支持
   - https://github.com/PaddlePaddle/Paddle/pull/64272
3. 规范用于自动生成算子定义的 yaml 文件路径
   - https://github.com/PaddlePaddle/Paddle/pull/64446
4. 将新 IR 下动静定义一致的算子迁移至 ops.yaml 和 backward.yaml
   - https://github.com/PaddlePaddle/Paddle/pull/64536

### 下周工作

- 推进 PIR 算子 yaml 定义规范化

