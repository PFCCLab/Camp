### 姓名

周鑫

### 实习项目

飞桨 3.0 多硬件方向单测/模型验证修复

### 本周工作

1. 修复 SLANet 推理报错
2. 为 NPU & MLU 添加 full_with_tensor kernel
3. 修复 NPU 流水线新检出异常单测
4. 修复 NPU get_device 时 context 为 NULL
5. 为 memcpy 选 device和根据 operand 选 Kernel backend 添加input 为 TensorArray 的支持
6. 部分修复 pd_op.if 异常

### 下周工作

1. 继续排查 MLU 下 pd_op.if 和 单测异常
2. 修复新 MLU 模型推理错误
3. 整理精度报错

### 导师点评
None