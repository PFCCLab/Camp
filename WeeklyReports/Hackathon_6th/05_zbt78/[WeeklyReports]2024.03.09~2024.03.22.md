### 姓名

周波涛

### 实习项目

算子支持复数计算专项

### 本周工作

1. 完成pow复数支持中的 pow部分和elementwish_pow部分
2. 为allgather,diag,eye,gather,lookup_table_v2 支持复数
3. 阅读test过程中对grad进行测试时的numerical_grad部分，是因为在测试pow时，如果输入数据的size为1测试正确，当size不为1时numerical_grad计算得到的结果为（正确结果）/ size。可能是pow的问题。

相关pr：

https://github.com/PaddlePaddle/Paddle/pull/62764

https://github.com/PaddlePaddle/Paddle/pull/62959

### 下周工作

1. 完善已提交pr
2. 开展新的算子，要加快进度了

### 导师点评
稳步按照规划推进，再接再励
