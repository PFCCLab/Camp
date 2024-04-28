### 姓名
马欣楷

### 实习项目
CINN 支持动态 Shape 专项（前端方向）

### 本周工作
本周主要工作如下：
1. 排查paddle.mean接口无法使用cinn编译的原因，进行修复，相关pr: https://github.com/PaddlePaddle/Paddle/pull/63494。目前已修复部分case的编译问题，其它case暂不支持
2. 使用nsys profile对paddle.mean进行分析，发现reduce_sum相关kernel的计算占比较大，无明显优化空间。对不用cinn的情况进行对比测试，发现使用cinn后，性能会下降2个数量级，相关文档：https://docs.qq.com/doc/DRElueFNSdnZRcXNr

### 下周工作
1. 分析paddle.mean编译/性能问题


### 导师点评
欣楷本周在reduce_mean性能分析任务中发现了一些比较关键的性能问题，这对后续优化工作的开展有重要意义，希望继续在相关问题上深入思考，取得突破性进展。
