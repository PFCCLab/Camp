### 姓名
何泓域

### 项目
框架作为array-api-compat后端

### 本周工作

1.为paddle.less_than、paddle.less_equal、paddle.greater_than、paddle.greater_equal添加复数类型支持：
- https://github.com/PaddlePaddle/Paddle/pull/72619

2.paddle.slogdet 返回值规范化:
- https://github.com/PaddlePaddle/Paddle/pull/72505
 
3.为paddle.max、paddle.min支持 指定axis为非零轴的0-size tensor输入，还在调试：
- https://github.com/PaddlePaddle/Paddle/pull/72565

4.paddle.cumsum算子接口重构，目前仍在调试：
- https://github.com/PaddlePaddle/Paddle/pull/72532

5.paddle.martix_norm修复，支持0-size并支持复数，需要等待`3`合入：
- https://github.com/PaddlePaddle/Paddle/pull/72577

### 下周工作
继续完成上述pr，并合入paddle主分支。
