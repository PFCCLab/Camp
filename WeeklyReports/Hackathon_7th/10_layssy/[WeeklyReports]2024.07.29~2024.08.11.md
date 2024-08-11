### 姓名

李伟

### 实习项目

推理Predictor 及 IR Pass建设

### 本周工作

#### paddle架构相关学习

1. 熟悉了Paddle-Inference-Demo  python层面的运用
2. 学习了 paddle 算子层面的转换

#### 算子的 Marker 的开发 和单测的实现

1. 完成Split_with_num 、multiply、 elementwise_max elementwise_min elementwise_pow elementwise_floordiv elementwise_sub elementwise_div elementwise_mod、shape以及greate_equal等算子的 marker 和单测 的开发
2. 补充现在已有marker的算子的单测

#### 模型文档整理

1. 整理了一部分check_infrence.sh中的的模型( Deeplabv3_Plus-R101、 Deeplabv3_Plus-R50、Deeplabv3-R101、Deeplabv3-R50、OCRNet_HRNet-W48、PP-LiteSeg-T、PP-OCRv4_mobile_det、PP-OCRv4_server_det、PP-OCRv4_mobile_rec、PP-OCRv4_server_rec)包含的算子是否具有对应的marker 和converter

### 下周工作

1. 继续完成check_infrence.sh 剩余模型中算子的统计
   1. 统计完成之后，补充缺少marker算子的marker以及单测
   1. 学习如何开发算子的converter
1. 熟悉Paddle-Inference-Demo 的c++端的流程
