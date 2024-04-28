### 姓名
YibinLiu666

### 实习项目
高阶微分的性能分析和优化

### 本周工作
1. 分析现有科学计算中性能相比 pytorch 较差的三个模型，发现瓶颈在于矩阵乘法的二阶微分组合实现，但是由于没有发现额外的计算，暂时没有做相关的优化
2. 实现sigmoid的二阶微分组合算子 https://github.com/PaddlePaddle/Paddle/pull/63669
3. 鉴于prod_grad在输入有0的时候梯度会出现nan的情况，参考TensorFlow的实现，评估prod_grad组合实现使用双向cumprod实现的可行性，目前的结论是可行性不高。

### 下周工作

1. 参考torch的prod_grad组合实现，解决prod_grad在输入有0的时候梯度会出现nan的情况。

### 导师点评

