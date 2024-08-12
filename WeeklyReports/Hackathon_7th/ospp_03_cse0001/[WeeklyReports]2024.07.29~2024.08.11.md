### 姓名

谢一帆

### 实习项目

飞桨 PaddlePaddle-PIR 适配 VisualDL 模型可视化

### 本周工作

1. **测试目前 Visualdl 对于控制结构可视化的支持能力**

- 静态方式组建六种包含控制结构的网络，包含循环结构和分支结构，以及多层嵌套控制等
- 利用现有 pir 可视化方法进行可视化发现不支持包含多层 Block 网络的可视化

2. **开发 Visualdl 多层 Block 解析功能**

- 修改 visualdl#analyse_pir()，支持获取子 Block 中的全部变量
- 修改 visualdl#analyse_pir()，支持获取子 Block 中的全部算子
- 增加控制流算子识别功能
- 完善模型分析代码，实现 visualdl 对 pir 中 yield 等新算子的表示
- 完善模型分析代码，实现多层 Block 嵌套模型的全部变量和算子解析
- 完善模型分析代码，实现 Block 内外算子参数传递关系的正确表示

3. **完善 visualdl 对控制流算子的可视化**

- 将控制流算子构建为 visualdl 中的 layer，可以收缩或展开表示

### 下周工作

1. **完善 visualdl 对控制流算子的可视化**

- 修改 visualdl 后端，完善对控制流算子传入变量和传出变量的处理
- 修改 visualdl 前端，提升控制流算子 layer 的可视化美观程度，并支持对 layer 的参数传入和传出

### 导师点评
