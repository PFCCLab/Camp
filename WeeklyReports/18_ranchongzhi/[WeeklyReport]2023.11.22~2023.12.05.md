### 姓名

冉崇治

Github ID：[ranchongzhi](https://github.com/ranchongzhi)

### 实习项目

[套件压缩能力建设](https://github.com/PaddlePaddle/community/blob/master/hackathon/hackathon_5th/%E3%80%90PaddlePaddle%20Hackathon%205th%E3%80%91%E9%A3%9E%E6%A1%A8%E6%8A%A4%E8%88%AA%E8%AE%A1%E5%88%92%E9%9B%86%E8%AE%AD%E8%90%A5%E9%A1%B9%E7%9B%AE%E5%90%88%E9%9B%86.md#%E9%A1%B9%E7%9B%AE%E5%8D%81%E5%85%AB%E5%A5%97%E4%BB%B6%E5%8E%8B%E7%BC%A9%E8%83%BD%E5%8A%9B%E5%BB%BA%E8%AE%BE)

### 本周工作

为PaddleOCR套件接入自动化压缩功能，主要完成以下PPOCRV4检测模型的压缩与推理，并尝试解决其中的报错。


原始情况如下：

![](./imgs/ocr_det_goal.png)

目前的结果：

Nvidia GPU测试环境：

- 硬件：NVIDIA RTX 3090ti 单卡
- 软件：CUDA 11.7, cudnn 8.1.0, TensorRT-8.4.2.4
- 测试配置：batch_size: 1

|模型|模型精度(%,gpu上)||GPU+TRT推理延时(ms)||备注|
|-|-|-|-|-|-|
||量化前|量化后|量化前|量化后||
|ch_PP-OCRv4_det_mobile|72.71|71.10|5.7|2.3|仅量化conv2d|
|ch_PP-OCRv4_det_server|79.82|79.27|32.6|12.3|仅量化conv2d|


CPU测试环境：

- Intel(R) Xeon(R) Gold 6226R CPU @ 2.90GHz
- cpu thread: 12

|模型|cpu精度||CPU推理延时(ms)||备注|
|-|-|-|-|-|-|
||量化前|量化后|量化前|量化后||
|ch_PP-OCRv4_det_mobile|72.71|72.94|92.0|94.1|仅量化conv2d|
|ch_PP-OCRv4_det_server|79.77|79.66|844.7|635.0|仅量化conv2d|

#### ch_PP-OCRv4_det_server

- 官方仓库里给定的推理模型是使用paddle2.3导出的，在paddle2.5的环境下推理会报错，所以我使用导出推理模型的脚本到出了新的推理模型，使用新的推理模型进行推理，解决了报错问题。

- 由于给定的测试集中存在一些长宽比例很大的图像，在预处理之后图像变得很大，导致在ir优化构建TensorRT子图的过程中会爆显存，为了测试加速效果，所以我写了一个脚本对数据集进行筛选，筛选出长宽比例小于2的图像，使用筛选后的数据集进行测试，解决了爆显存的问题。

相关PR
- https://github.com/PaddlePaddle/PaddleOCR/pull/11345

### 下周计划

完善PaddleClas中两个模型的ACT功能，提交PaddleDetection和PaddleClas对应的PR。

### 导师点评
实现了OCR全部模型和Det部分模型的调通，量化效果优秀，成果突出。
