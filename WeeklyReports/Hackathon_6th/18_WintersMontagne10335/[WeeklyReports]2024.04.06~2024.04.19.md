### 姓名
马贺达

### 实习项目
CINN 静态 shape 下鲁棒性和性能优化

### 本周工作

1. **符号推导机制**

	* 收尾 pd_op.nonzero
（相关PR：https://github.com/PaddlePaddle/Paddle/pull/62987 ）
	* 补全 pd_op.bce_loss, pd_op.sigmoid_cross_entropy_with_logits 的 check 和单测，目前单测存在问题 RuntimeError: Unexpected index，正在解决。
pd_op.distribute_fpn_proposals 存在未能成功注册的问题，正在解决
（相关PR：https://github.com/PaddlePaddle/Paddle/pull/63277 ）

2. **VerticalLoopFusion 阅读笔记**

	* 阅读 HorizontalLoopFusion 的静态实现，并撰写阅读笔记
（相关链接：https://github.com/WintersMontagne10335/Paddle-Code-Camp/blob/master/code%20reading/HorizontalLoopFusion.md）

### 下周工作

1. 收尾 pd_op.bce_loss, pd_op.sigmoid_cross_entropy_with_logits, pd_op.distribute_fpn_proposals
2. 修复计算结果错误相关的 bug
3. VerticalLoopFusion 阅读笔记

### 导师点评
请联系导师填写
