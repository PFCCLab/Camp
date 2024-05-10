### 姓名

蔡越

### 实习项目

PaddleMIX 套件能力建设（文图方向）

### 本周工作

1. **优化AnimateAnyone训练权重保存逻辑以即混合精度控制机制；**
   
   - 根据两阶段权重保存逻辑，重写trainer中_save()函数，实现在training_args参数控制下对模型相关信息进行保存；
   
   - 清除原始精度控制机制，统一改由trainer进行精度策略控制，并在不同精度混合进度策略下进行测试；
   
   - 重构模型相关代码，将其融合进ppdiffusers/models下；
   
   - 关于模型组网denoising_unet()的权重加载方式，由于其包含对motion_module的更新，与ppdiffusers的模型权重统一加载方式难以兼容，考虑先保留现有的权重加载方式；
   
   - 相关PR：https://github.com/PaddlePaddle/PaddleMIX/pull/501 ,  https://github.com/PaddlePaddle/PaddleMIX/pull/510

2. **同步更新AI studio项目**
   
   - 解决由paddle2.5.2升级为2.6.1导致部分算子(transpose)计算行为发生变化的问题，目前已支持paddlepaddle2.6.1；
   
   - 项目链接：https://aistudio.baidu.com/projectdetail/7490749?contributionType=1

### 下周工作

1. 推进AnimateAnyone训练支持相关PR合入；
2. 调研结合transformer和diffusion model的视频生成开源模型，与导师沟通规划下一步工作重点；

### 导师点评

蔡越在本周围完成了AnimateAnyone的结尾工作，完成了相关PR的合入和ai studio项目的更新，并开展了open-sora相关的调研工作，干的不错，继续加油。