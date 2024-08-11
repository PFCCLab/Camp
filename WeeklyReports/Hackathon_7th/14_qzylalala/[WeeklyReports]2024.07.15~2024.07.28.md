### 姓名

秦忠宇

### 实习项目

飞桨PaddlePaddle-PIR适配2ONNX推理转换

### 本周工作

1. 梳理 Paddle PIR save/load 的逻辑，对照着 PIR Schema 学习生成的 json 文件格式。
2. 梳理 Paddle2ONNX 项目代码，主要从 `paddle2onnx.export` 接口学习 PaddleParser 的实现逻辑，思考针对 PIR 进行新的方案设计。
3. 输出[技术文档](https://iqf3tuixgs.feishu.cn/docx/NcXWdfPfmovFd7xLsQycrTPjnTf)，和 mentor 讨论技术选型，之前通过 `framework.proto` 对 `pdmodel` 进行解析。现在如何解析生成的 json 文件，并且尽可能的少造轮子。

### 下周工作

1. 针对 Paddle2ONNX 如何对 PIR save 生成的 json 文件进行解析进行技术选型。

### 导师点评
忠宇本周做了大量调研和方案设计的相关工作，产出了设计文档，和组内同事也进行了一些讨论，基本方案已经确定，再接再厉~
