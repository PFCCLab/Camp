### 姓名

谢一帆

### 实习项目

飞桨PaddlePaddle-PIR适配VisualDL模型可视化

### 本周工作

1. **配置开发环境，熟悉Paddle和VisualDL**
  - 本地源码编译安装Paddle和VisualDL的develop分支
2. **熟悉VisualDL进行计算图可视化的设计**
  - 阅读visualdl#Model()类存储计算图的设计逻辑
  - 阅读visualdl#analyse_model()函数从**.pdmodel*文件获取计算图数据的逻辑
  - 阅读visualdl#analyse_pir()函数从PIR表示的模型获取计算图数据的逻辑
3. **熟悉PIR进行计算图存储的设计**
  - 阅读pir#program.cc, operation.cc, block.cc, region.cc等文件，熟悉PIR进行模型存储的设计
  - 阅读fluid#pir.cc中和获取Program数据有关接口API
4. **完成Visual现有PIR计算图可视化方法适配Paddle3.0版本**
  - 修改visualdl#analyse_pir()等函数，并成功可视化原有测试demo#pir_translate.py
5. **尝试可视化具有分支结构模型**
  - 实现了具有if分支结构的简单模型并进行可视化

### 下周工作

1. **继续尝试可视化具有分支结构的模型，探索如何利用PIR新特性进行可视化**
  - 从Paddle的分支结构算子ifop和whileop的测试文件中获取静态组网的简单模型，验证现有visualdl对于分支结构可视化的支持能力，探索优化方法

### 导师点评

按计划进度完成任务
