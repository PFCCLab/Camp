### 姓名

冉崇治

Github ID：[ranchongzhi](https://github.com/ranchongzhi)

### 实习项目

[套件压缩能力建设](https://github.com/PaddlePaddle/community/blob/master/hackathon/hackathon_5th/%E3%80%90PaddlePaddle%20Hackathon%205th%E3%80%91%E9%A3%9E%E6%A1%A8%E6%8A%A4%E8%88%AA%E8%AE%A1%E5%88%92%E9%9B%86%E8%AE%AD%E8%90%A5%E9%A1%B9%E7%9B%AE%E5%90%88%E9%9B%86.md#%E9%A1%B9%E7%9B%AE%E5%8D%81%E5%85%AB%E5%A5%97%E4%BB%B6%E5%8E%8B%E7%BC%A9%E8%83%BD%E5%8A%9B%E5%BB%BA%E8%AE%BE)

### 本周工作

1. **熟悉Paddle Inference以及PaddleSlim中的自动压缩功能**
    - 跑通了Paddle Inference的官方的Demo，日志记录在[如下链接](https://www.wolai.com/ranchongzhi/mmsbzC9VsQsHDwasNTNQz7)
    - 跑通了PaddleSeg中自动压缩的示例项目，日志记录在[如下链接](https://www.wolai.com/ranchongzhi/wyMm2rZbjXK79cokPNE4XF)
2. **修复PaddleSeg中模型自动压缩推理遇到的问题**
    - ppliteseg-tiny模型自动压缩之后，CPU端int8推理精度下降，经过排查是在推理过程中量化了多余的`pool2d`算子，导致精度下降。问题已解决，PR地址：[[Fix]modify quantized ops during mkldnn int8 inference](https://github.com/PaddlePaddle/PaddleSeg/pull/3514)
    - 修复其他模型在量化推理过程中的bug，PR地址：[[Bug fixes]: Modify code and setting to run ACT correctly](https://github.com/PaddlePaddle/PaddleSeg/pull/3539/commits/1def3cad964c5605f7af36dbded5bf281e586a34):
        1. ADE20K类似数据集图片大小不一致导致dynamic shape info收集不准确，导致在IR优化过程中TensorRT一直重建子图，最终导致报错，最终通过寻找极端尺寸图像去收集dynamic shape info来解决该问题。
        2. 调整ppmobileseg推理时的验证配置，和训练过程保持一致，利用ACT训练出精度指标更高的量化模型。
        3. 基于aistudio的环境，将全部模型的指标重新测试并更新，并同时更新文档。
3. **问题疑惑与解答**
    - 问题a：[PaddleSlim文档](https://paddleslim.readthedocs.io/zh_CN/latest/deploy/deploy_cls_model_on_x86_cpu.html#id4)里边说，pool2d这种算子不会显著地改变scale，所以不需要在训练过程中进行量化，可以直接从相邻节点获取量化信息，所以在推理的时候可以直接量化它？

        答：
            1. pool2d在压缩时是不支持量化的，在CPU上支持量化是指推理支持量化。
            2. 在压缩时不量化pool2d，推理时量化，那么pool的scale用的是其他已量化op的scale，比如 conv + pool，conv已经通过qat或ptq有scale了，那只需要将反量化过程挪到pool之后，那pool就是int8计算。但是conv之后往往接relu等激活，导致拿到的scale不准确，因此大多数情况下对pool2d的量化都是无效的～ 
            3. 因此最佳实践是推理和量化训练保持量化op的一致，从而推理精度才会和训练精度对齐。

### 下周工作

1. 复现并尝试修复PaddleDetection中ACT相关模型的bug并尝试修复。
2. 整理Paddle Inference的笔记，用于后续的分享。

### 导师点评

请联系导师填写