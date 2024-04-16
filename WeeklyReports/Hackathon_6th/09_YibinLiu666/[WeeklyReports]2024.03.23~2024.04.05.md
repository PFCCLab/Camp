### 姓名
YibinLiu666

### 实习项目
高阶微分的性能分析和优化

### 本周工作
1. 收尾DivideDoubleGrad算子.
2. 阅读fft算子的相关文档，优化FFTC2RGradKernel，去除其额外的循环与内存占用。 https://github.com/PaddlePaddle/Paddle/pull/63137
3. 优化FFTC2RKernel，其在计算时候长时间同步的问题。 https://github.com/PaddlePaddle/Paddle/pull/63249

### 下周工作

1. 分析现有科学计算中性能相比 pytorch 较差的三个模型，尝试发现其瓶颈并优化对应的算子。

### 导师点评
Yibin同学基于结合nsight和实现代码，对FFTC2RGradKernel、FFTC2RGradKernel进行了较为细致的分析，对两个算子实现进行了优化 👍 
