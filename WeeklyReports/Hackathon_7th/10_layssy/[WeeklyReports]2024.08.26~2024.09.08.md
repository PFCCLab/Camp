### 姓名

李伟

### 实习项目

推理Predictor 及 IR Pass建设



### 本周工作

#### paddle架构相关学习

1. 熟悉了Paddle-Inference-Demo  python层面的运用
2. 学习了 paddle 算子层面的转换

#### 算子的 Marker、converter 的开发 和单测的实现

1. 完成了 divide、multiply、substract的converter的开发和单测实现
2. 完成了max的marker和converter的开发和单测的测试
3. 排查了pd_op.bilinear_interp在旧ir下为什么没有进入tensorrt
4. 提交了split算子在进行converter的时候出现的bug



### 下周工作

1. 继续完成分配算子的converter的实现
1. 重新全部理解一下converter.py全部的实现

### 导师评价

