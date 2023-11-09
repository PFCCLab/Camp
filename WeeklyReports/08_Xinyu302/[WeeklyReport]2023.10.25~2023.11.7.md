### 姓名
杨新宇

### 实习项目
CPU 融合算子 / GPU 算子融合 pass

### 本周工作

详见 https://github.com/yuanlehome/Hackathon/wiki/%E6%B7%B7%E5%90%88%E7%B2%BE%E5%BA%A6pass%E6%A2%B3%E7%90%86


1. **梳理混合精度pass实现**
分析了旧IR下自动混合精度pass的实现，整理成文档。

2. **思考混合精度pass在新ir下的实现**
与导师讨论了混合精度pass使用新ir下match and rewrite方式的实现, 已经搭建框架，实现了一版，但还存在一些问题。

### 下周工作

1. 完善对输入输出op的处理
2. 完善对算子输入精度的处理，例如fp16精度下的batch_norm算子仍然需要float32的输出

### 导师点评

