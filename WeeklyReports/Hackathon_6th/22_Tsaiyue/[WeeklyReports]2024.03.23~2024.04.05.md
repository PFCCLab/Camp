### 姓名

蔡越

### 实习项目

PaddleMIX 套件能力建设（文图方向）

### 本周工作

1. **完成对paddle实现下AnimateAnyone stage2微调的有效性验证；**
   
   - 在自定义数据集(ubc_fashion + bili_dance)对stage2的motion_module基于animatediff进行微调，相较于Moore权重、animatediff初始化权重以及仅使用ubc_fashion训练得到的权重，在生成视觉效果以及量化指标上更优，具体体现为动画背景闪动得到一定程度抑制、时间一致性保持更优、测试样例下PSNR值更高。

2. **提供ppdiffusers/example/AnimateAnyone训练支持，实现基于paddlenlp.trainer实现对stage1 & stage2在自定义数据集(ubc_fashion + bili_dance)下的微调。**
   
   - 调试解决基于paddlenlp.trainer训练过程出现NAN问题，问题为计算snr loss时由于随机timesteps导致计算过程出现溢出，通过修改noise_scheduler的prediction_type属性解决；
   
   - 相关PR：[[ppdiffusers] AnimateAnyone Training Support by Tsaiyue · Pull Request #501 · PaddlePaddle/PaddleMIX · GitHub](https://github.com/PaddlePaddle/PaddleMIX/pull/501)

### 下周工作

1. 推进AnimateAnyone训练支持PR合入；
2. 尝试对组网部分的denoising_unet进行权重加载逻辑升级，以提升开发者体验以及该示例与ppdiffusers的耦合度；
3. 完善对应ai studio项目，提供训练支持。 

### 导师点评