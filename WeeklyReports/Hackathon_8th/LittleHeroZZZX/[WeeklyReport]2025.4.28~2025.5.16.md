### 姓名

周鑫

### 实习项目

飞桨 3.0 多硬件方向单测/模型验证修复

### 本周工作

1. 修复 NPU Transpose hang
2. 协助修复 XPU OCR3.0 模型推理问题
   1. xpu pool2d 缺少 NHWC 布局支持
   2. conv2d_bn_xpu_fuse_pass 在 xpu 上异常
   3. conv2d_fusion 在特定输入 shape 下报错 XDNN_NOT_IMPLEMENT
   4. einsum xpu & cpu 均不支持 bf16 推理

### 下周工作

1. 修复 MLU 下模型推理错误

### 导师点评
None