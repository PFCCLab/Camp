### 姓名

冉崇治

Github ID：[ranchongzhi](https://github.com/ranchongzhi)

### 实习项目

[套件压缩能力建设](https://github.com/PaddlePaddle/community/blob/master/hackathon/hackathon_5th/%E3%80%90PaddlePaddle%20Hackathon%205th%E3%80%91%E9%A3%9E%E6%A1%A8%E6%8A%A4%E8%88%AA%E8%AE%A1%E5%88%92%E9%9B%86%E8%AE%AD%E8%90%A5%E9%A1%B9%E7%9B%AE%E5%90%88%E9%9B%86.md#%E9%A1%B9%E7%9B%AE%E5%8D%81%E5%85%AB%E5%A5%97%E4%BB%B6%E5%8E%8B%E7%BC%A9%E8%83%BD%E5%8A%9B%E5%BB%BA%E8%AE%BE)

### 本周工作

为PaddleOCR套件接入自动化压缩功能，主要完成以下PPOCRV4识别模型的压缩与推理，并尝试解决其中的报错。


原始情况如下，主要是在ACT压缩的时候会出现loss为nan的情况：

![](./imgs/ocr_rec_goal.png)

目前的结果：

Nvidia GPU测试环境：

- 硬件：NVIDIA Tesla V100 单卡
- 软件：CUDA 11.2, cudnn 8.1.0, TensorRT-8.0.3.4
- 测试配置：batch_size: 1

|模型|cpu精度(%)||CPU推理延时(ms)||备注|
|-|-|-|-|-|-|
||量化前|量化后|量化前|量化后||
|ch_PP-OCRv4_rec_mobile|78.92|78.41|1.7|1.4|仅量化conv2d|
|ch_PP-OCRv4_rec_server|81.62|81.03|4.0|2.0|仅量化conv2d|

CPU测试环境：

- Intel(R) Xeon(R) Gold 6148 CPU @ 2.40GHz
- cpu thread: 12

|模型|模型精度(%,gpu上)||GPU+TRT推理延时(ms)||备注|
|-|-|-|-|-|-|
||量化前|量化后|量化前|量化后||
|ch_PP-OCRv4_rec_mobile|78.92|78.44|33.3|34.0|仅量化conv2d|
|ch_PP-OCRv4_rec_server|81.62|81.00|62.5|64.4|仅量化conv2d|



1. **ch_PP-OCRv4_rec_server**
  loss为nan是蒸馏损失skd的bug，更换蒸馏节点或者将该loss去掉，仅使用l2蒸馏损失，可以解决该问题。在实践过程中发现，仅使用l2蒸馏损失，精度下降最少，故最终使用了仅使用l2蒸馏损失的方式。
2. **ch_PP-OCRv4_rec_mobile**
   loss为nan是蒸馏损失skd的bug，更换蒸馏节点或者将该loss去掉，仅使用l2蒸馏损失，可以解决该问题。在实践过程中发现，将skdloss的蒸馏节点从linear_170.tmp_1更换为softmax_11.tmp_0这种方式，精度下降最少，故最终使用了该种方式。

### 下周工作

1. 由于数据集保密的原因，需要在公开数据集上从头训练模型，然后再进行压缩，所以下周主要是在公开数据集上训练文本检测模型，然后再进行跑通一遍act的流程。

### 导师点评



