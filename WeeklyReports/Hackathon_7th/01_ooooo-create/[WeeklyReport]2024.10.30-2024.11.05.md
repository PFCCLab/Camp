### 姓名

方国勇

### 实习项目

CINN 符号推导

### 本周工作

#### 合入 pr
- https://github.com/PaddlePaddle/Paddle/pull/68984
- https://github.com/PaddlePaddle/Paddle/pull/68964
- https://github.com/PaddlePaddle/Paddle/pull/68929
- https://github.com/PaddlePaddle/Paddle/pull/68917
- https://github.com/PaddlePaddle/Paddle/pull/68907

#### 完善 pr
- [frame, prune_gate_by_capacity](https://github.com/PaddlePaddle/Paddle/pull/68644)
- [same_operand_with_result.cc](https://github.com/PaddlePaddle/Paddle/pull/68841)
- [assign_ops](https://github.com/PaddlePaddle/Paddle/pull/68947)
- [matrix_rank_tol](https://github.com/PaddlePaddle/Paddle/pull/68975)
- [shuffle_batch](https://github.com/PaddlePaddle/Paddle/pull/68978)
- [weight_{dequantize.quantize}](https://github.com/PaddlePaddle/Paddle/pull/68979)
- [uniform_random_batch_size_like](https://github.com/PaddlePaddle/Paddle/pull/68980)
- [tensor_unfold](https://github.com/PaddlePaddle/Paddle/pull/68981)
- [array_read](https://github.com/PaddlePaddle/Paddle/pull/69017)

#### 新增 PR
- [create_array_like&&has_elements](https://github.com/PaddlePaddle/Paddle/pull/69055) manual op
- [tensor_to_array&&select_output](https://github.com/PaddlePaddle/Paddle/pull/69055) manual op
- [FloorDivide](https://github.com/PaddlePaddle/Paddle/pull/69167) SIR_32

#### Others

- 0D Tensor，在有 data 时，data.size() = 1 ， shape = {}
- data 区数据在 Tensor 作为 shape 的时候，以及可以简单运算或变换得到 1D Tensor 的时候，可以添加 data 区。

### 下周工作

1. 修复 SIR_32 流水线问题
2. 

### 导师点评
