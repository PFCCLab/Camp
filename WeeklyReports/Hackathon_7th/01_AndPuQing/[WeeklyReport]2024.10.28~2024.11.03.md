### 姓名

梁嘉铭

### 实习项目

PIR 专项

### 本周工作

本周工作完成对：

- `DepthwiseConv2dTranspose&&LogSoftmax`: https://github.com/PaddlePaddle/Paddle/pull/69133

CINN InferSymbolShape支持。

以及在 `strided_slice` 添加 `InferShape` 支持中发现 `stride_slice` 在 PIR 下 python 前端适配不完全，导致部分测试用例失败；另外 `stride_slice` 在 ops yaml 中定义参数缺少 `infer_flags`，导致在`InferShape`中无法获取到参数，导致shape推理失败。

### 下周工作

继续完成对其他Op的InferSymbolShape支持。

### 导师点评
