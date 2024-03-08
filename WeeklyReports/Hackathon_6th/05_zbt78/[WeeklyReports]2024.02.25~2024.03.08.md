### 姓名

周波涛

### 实习项目

算子支持复数计算专项

### 本周工作

1. 学习静态图中attrs为scalar的实现原理。目前根据op.yaml自动生成代码时Scalar类型被转换成了float，但是为了支持complex，此处感觉应该为[Scalar](https://github.com/PaddlePaddle/Paddle/blob/1208cd3345113b21821accef9d31acd636b0f74a/paddle/fluid/operators/generator/generate_op.py#L93)

2. log、log2、log10、log1p的复数支持进行中

3. pow复数支持中的 pow部分，elementwish_pow还在完善中

相关pr：https://github.com/PaddlePaddle/Paddle/pull/62448

### 下周工作

1. 完成pow复数支持

2. 继续阅读源码，弄懂算子输出类型和梯度类型从何而来，具体由什么确定；为什么有的算子的op.yaml中推导过程为UnchangedInferMeta，但输出类型和输入类型却不一样；而有的算子用自定义的InferMeta，但输入类型和输出类型却一样。

3. 修复log、log2、log10、log1p中输入类型为int时的backward

	![](https://blog-img-zbt.oss-cn-beijing.aliyuncs.com/picture/wuyang/202403062138642.png)
    

### 导师点评
pow 的支持可能会有一些难度，因为elementwise_pow 也需要支持指数为复数的场景，源码中遇到的问题可以多多和@zyt1024, 解决不了的我们可以一起看看
再接再厉！
