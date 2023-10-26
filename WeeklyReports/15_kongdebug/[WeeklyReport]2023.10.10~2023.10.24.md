### 姓名

孔远杭

Github ID：[kongdebug](https://github.com/kongdebug)

### 实习项目

[3D方向模型全流程建设](https://github.com/PaddlePaddle/community/blob/master/hackathon/hackathon_5th/%E3%80%90PaddlePaddle%20Hackathon%205th%E3%80%91%E9%A3%9E%E6%A1%A8%E6%8A%A4%E8%88%AA%E8%AE%A1%E5%88%92%E9%9B%86%E8%AE%AD%E8%90%A5%E9%A1%B9%E7%9B%AE%E5%90%88%E9%9B%86.md#%E9%A1%B9%E7%9B%AE%E5%8D%81%E4%BA%943d%E6%96%B9%E5%90%91%E6%A8%A1%E5%9E%8B%E5%85%A8%E6%B5%81%E7%A8%8B%E5%BB%BA%E8%AE%BE)

### 本周工作

1. **阅读与理解实习项目需要复现的论文Fast-BEV**
    - 了解了Fast-BEV的快速射线变换、多尺度图像编码、高效BEV编码、数据增强、时间融合五个关键部分
    - 学习Fast-BEV所用数据集nuScenes, 将在本周末之前整理出学习笔记发布在AI Studio星河社区以及Camp项目中

2. **为Paddle3D添加Fast-BEV对NuScenes数据预处理的代码**
    - 相较BEVFormer模型，Fast-BEV为了加速训练过程中NuScenes数据集的加载和解析，除了添加标注信息还需要建立与时间戳相关的序列索引。同时考虑到平常学习一般使用数据量少的`NuScenes-mini`版本，增加预处理脚本对该版本数据的支持，相关预处理代码地址[create_fastbev_nus_infos_seq_converter](https://github.com/kongdebug/Fast-BEV-Paddle/blob/main/tools/create_fastbev_nus_infos_seq_converter.py)
    - 由于论文复现是一个整体性的工程，因此该代码暂未合入Paddle3D中，而是在基于Paddle3D的个人项目[Fast-BEV-Paddle](https://github.com/kongdebug/Fast-BEV-Paddle)中，完成论文复现之后再整体合入

3. **问题疑惑与解答**
    - 问题a: NuScenes完整数据集接近500G大小，目前推进该项目是使用mini版的NuScenes数据进行代码测试，而之后训练复现需要使用完整数据，已经超过AI Studio的磁盘大小，该如何进行训练？
      答：


### 下周工作

1. 完成Fast-BEV模型组网复现，并前向对齐
2. 完成Fast-BEV的NuScenes数据集类的定义

### 导师点评

