### 姓名
王龙志

### 实习项目
量化算子集成

### 本周工作

1. **理清 PaddleSlim 的量化流程现状以及量化后得到的计算图产物**
- 理解了 PaddleSlim 的 PTQ 量化的全流程步骤
- 通过 netron 可视化 PaddleSlim 量化后的计算图，加强了对 PaddleSlim 量化与 TRT 推理之间联系的理解

2. **理清 PaddleSlim 量化后的计算图在 TensorRT backend 下的低精度推理流程**
- 理解了 Paddle TRT 是如何识别到输入的计算图是一个量化后的计算图
- 理解了 Paddle TRT 的算子转换过程
- 理解了 Paddle TRT 的有关 Pass 的执行流程以及几个重要的量化以及子图构建相关的 Pass 的原理，从而理解了从 Paddle TRT 到 TRT 的完整推理流程，为实现原生量化推理提供思路和基础

3. **学习 matmul 算子的 int8 低精度实现**
- 学习 matmul 算子的 int8 低精度实现，为后续补充相关低精度算子提供基础

4. **学习 Paddle IR 的计算图表示和相关 API**
- 学习 Paddle IR 的计算图的相关表示和 API，为编写原生推理相关的 Pass 提供基础

5. **用 TRT API 搭建一个一层的 matmul 层并进行 int8 推理**
- 完成这个任务使得对 TRT 理解更深刻，为后续原生量化推理提供思路和基础

6. **问题疑惑与解答**
- Paddle TRT 是如何识别到输入的计算图是一个量化后的计算图
    答：以 int8 举例，在 ConvertBlockToTRTEngine 函数中会调用 FreezeNetwork 函数，这个函数当识别到 precision_ 为 int8 时，先调用 infer_builder_config_->setFlag(nvinfer1::BuilderFlag::kINT8) 来开启 int8 layer，并且当我们指定了不使用 Int8Calibrator时，会对 netowrk 中的 layer 的输入 tensor 调用 TRT 的 API setDynamicRange 来将 (-InputScale, InputScale) 设置到 DynamicRange（隐式量化），然后后面 TRT 的 engine 就可以调用到 对应的 int8 算子.

### 下周工作

1. 进一步加强对 TRT 低精度推理流程的理解
2. 进一步梳理清楚整个项目的开发步骤和流程
3. 开始编写识别原生量化推理算子的 Pass
4. 参考竞品的原生推理实现的流程以及做了哪些性能优化

### 导师点评
前期工作基本属于代码的阅读理解和量化全流程学习，王龙志同学以极强的学习能力快速厘清了PTQ到量化推理的关系，对其中每一个步骤都有了较为清晰的认识。这里建议可以对这部分工作进行文档整理合入到该仓库中作为本项目的前期成果，也作为黑客松的技术沉淀。下一步将进入到Pass的代码开发阶段，再接再厉
