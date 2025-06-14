### 姓名
何泓域

### 项目
框架作为array-api-compat后端

### 本周工作

paddle.where、paddle.nonzero、paddle.matrix_power支持complex：
- https://github.com/PaddlePaddle/Paddle/pull/72247
- https://github.com/PaddlePaddle/Paddle/pull/72279
- https://github.com/PaddlePaddle/Paddle/pull/72308

paddle.inv支持0-size：
- https://github.com/PaddlePaddle/Paddle/pull/72262

paddle.slogdet算子重构：
- 目前已跑通dtype=float下的单测，dtype=complex的情况仍在调试。

### 下周工作
继续完善slogdet，并开始着手pow、pinv、matrix_norm。
