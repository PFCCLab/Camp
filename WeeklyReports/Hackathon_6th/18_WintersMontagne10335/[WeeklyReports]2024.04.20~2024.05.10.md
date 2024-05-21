### 姓名
马贺达

### 实习项目
CINN 静态 shape 下鲁棒性和性能优化

### 本周工作

1. **符号推导机制**

	* 添加 cinn_op.reshape 到 pd_op.reshape 的转换规则
（相关PR：https://github.com/PaddlePaddle/Paddle/pull/64303 ）
	* 将 "pd_op.add" 添加至 ALLOW_DYNAMIC_SHAPE_VJP_OPS；补充全局推导时带有外部输入时的处理逻辑
（相关PR：https://github.com/PaddlePaddle/Paddle/pull/64342 ）

2. **代码串讲**

	* 调研动态 shape 支持相关的内容，并以《浅析 cinn 中的符号推导机制》为题做分享
（相关链接：https://github.com/WintersMontagne10335/Paddle-Code-Camp/blob/master/code%20reading/%E6%B5%85%E6%9E%90%20cinn%20%E4%B8%AD%E7%9A%84%E7%AC%A6%E5%8F%B7%E6%8E%A8%E5%AF%BC%E6%9C%BA%E5%88%B6.md ）

### 下周工作

1. 继续修 bug
2. 完善《浅析 cinn 中的符号推导机制》
3. VerticalLoopFusion 阅读笔记

### 导师点评
请联系导师填写
