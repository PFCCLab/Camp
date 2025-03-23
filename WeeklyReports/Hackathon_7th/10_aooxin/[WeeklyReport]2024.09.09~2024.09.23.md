### 姓名
马奥欣

### 实习项目
推理Predictor 及 IR Pass建设

### 本周工作

1. **对周中拿到的测试报告中提到的问题进行定位已经修改**
  * 定位并解决amp pass的cast缓存问题导致的pass 顺序不同会导致的报错问题，修改后的 pass 在不同顺序下不会受到影响
  * 定位出在 C++推理正常情况下python推理会报错的问题
  
  https://github.com/PaddlePaddle/Paddle/pull/67822

2. 学习使用 paddle profile，并完成相关 python 测试脚本


### 下周工作

1. 解决C++推理正常情况下python推理会报错的问题
2. 解决amp pass之前存在 cast op 重复的问题
3. 检查相关 op 是否正确设置了推理前的输入输出精度并改进
4. 对典型模型进行性能分析，查看是否还有改进的点

### 导师点评
点评
