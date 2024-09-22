### 姓名

田川

### 实习项目

PIR 专项

### 本周工作

1. 修复动转静下解析 `x.to(device=y.place)` device 参数异常的问题，动转静下 `y.place` 会是 None. PR: [#68030](https://github.com/PaddlePaddle/Paddle/pull/68030)
2. 修复 https://www.paddlepaddle.org.cn/documentation/docs/zh/guides/paddle_v3_features/sot_cn.html#id2 示例代码报错不一样的问题，本质上是 ipython 的问题，jupyter 同样可以复现. PR: [#67893](https://github.com/PaddlePaddle/Paddle/pull/67893)
3. 了解动转静体验优化现阶段已有的任务，对部分场景报错进行优化. PR: [#68078](https://github.com/PaddlePaddle/Paddle/pull/68078)


### 下周工作

1. 继续进行部分动转静体验优化任务

### 导师点评

解决了遗留的问题，接下来可以继续对体验持续进行优化～