### 姓名

李伟

### 实习项目

推理Predictor 及 IR Pass建设

### 本周工作

#### paddle架构相关学习

1. 熟悉了Paddle-Inference-Demo  python层面的运用
2. 学习了 paddle 算子层面的转换

#### 算子的 Marker 的开发 和单测的实现

1. 完成一系列算子的 marker和单测的开发
   1. Split_with_num 
   2. multiply
   3.  elementwise_max、 elementwise_min 、elementwise_pow 、elementwise_floordiv 、elementwise_sub 、elementwise_div 、elementwise_mod
   4. shape
   5. greate_equal

2. 补充现在已有marker的算子的单测

#### 模型文档整理

1. 整理了一部分check_infrence.sh中的的模型包含的算子是否具有对应的marker 和converter
   1. Deeplabv3_Plus-R101、 Deeplabv3_Plus-R50、Deeplabv3-R101、Deeplabv3-R50
   2. OCRNet_HRNet-W48
   3. PP-LiteSeg-T
   4. PP-OCRv4_mobile_det、PP-OCRv4_server_det、PP-OCRv4_mobile_rec、PP-OCRv4_server_rec


### 下周工作

1. 继续完成check_infrence.sh 剩余模型中算子的统计
   1. 统计完成之后，补充缺少marker算子的marker以及单测
   1. 学习如何开发算子的converter
1. 熟悉Paddle-Inference-Demo 的c++端的流程

### 导师评价

本周李伟已经统计完成check_inference.sh模型中全部算子的统计，并提交了elementwise_max、 elementwise_min 、elementwise_pow 、elementwise_floordiv 、elementwise_sub 、elementwise_div 、elementwise_mod、shape、greate_equal 的Marker到develop分支上
