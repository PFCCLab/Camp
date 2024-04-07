### 姓名

蔡越

### 实习项目

PaddleMIX 套件能力建设（文图方向）

### 本周工作

1. **完成AnimateAnyone stage1训练steploss对齐**
   
   * 按照no_trainer->trainer的顺序进行代码转写、权重转换以及训练steploss对齐。steploss对比图如下：
     
     <img title="" src="https://github.com/PFCCLab/Camp/assets/46399096/649c4380-1e71-4955-91a6-dfe9b6b6dd82" alt="" width="400">

2. **基于paddlenlp.trainer完成AnimateAnyone stage2训练steploss对齐 **
   
   * 完成代码转写、权重转换以及解决显存递增问题。steploss对比图如下：
     
     <img title="" src="https://github.com/PFCCLab/Camp/assets/46399096/d59b16fb-d86b-4d04-8a1c-91c11c21f432" alt="" width="400">

3. **构建爬取2000条高质量人体动作数据集，用于后续微调训练。并与导师沟通确立仅对stage2进行训练的微调策略。**

### 下周工作

1. 基于构建的数据集对AnimateAnyone stage2进行微调，预期为在相关量化指标和生成视觉效果上相较于源库有一定的提升，以验证方案的有效性;
2. 完善训练功能，包括对fp16训练精度, recompute, xformer的支持。

### 导师点评

蔡越在本周围绕着AnimateAnyone的训练开展了一系列的对齐和实验，工作扎实，能力强，继续加油。