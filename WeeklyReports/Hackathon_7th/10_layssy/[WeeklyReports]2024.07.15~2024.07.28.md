### 姓名

李伟

### 实习项目

推理Predictor 及 IR Pass建设

### 本周工作

#### paddle架构相关学习

1. 准备好paddle 环境
1. 熟悉paddle的整个流程，以及工作内容

#### 算子的 Marker 的开发 和单测的实现

1. 完成pd_op.index_select Maker的开发和单测
2. 完成了pd_op.cast Maker的开发和单测
3. 整理了需要进行开发的pd_op的算子

### 下周工作

1. 继续完成剩余pd_op.h的算子的Marker开发和实现
   1. 完成Split_with_num 、multiply、 elementwise_max elementwise_min elementwise_pow elementwise_floordiv elementwise_sub elementwise_div elementwise_mod的 marker 的开发
   1. 补充完 已经写好marker 的算子的单测
   1. 整理 Deeplabv3_Plus-R101、 Deeplabv3_Plus-R50、Deeplabv3-R101、Deeplabv3-R50、OCRNet_HRNet-W48、PP-LiteSeg-T

1. 通过Paddle-Inference-Demo 的了解 paddle 整个框架的流程

### 详细链接

[周报pr链接](https://github.com/PFCCLab/Camp/pull/309)

### 导师评价

需要完成哪些op marker / converter的开发，能否梳理一个列表
