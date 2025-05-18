### 姓名

秦忠宇

### 实习项目

飞桨PaddlePaddle-PIR适配2ONNX推理转换

### 本周工作

1. 和 mentor商讨后暂定技术路线为 PIR Parser 走单独的逻辑。
2. 修改 CMakeLists，支持 vscode 能够断点调试 Python & C++ 混合项目的 C++ 部分代码。参见 [PR](https://github.com/PaddlePaddle/Paddle2ONNX/pull/1353)。
3. 和 mentor 敲定使用 paddle 中的接口进行 PIR Program recovery，避免重复造轮子。

### 下周工作

3. 完成 PIR Program 的 recover 代码逻辑。
4. 对照学习 PaddleParser 实现的功能模块，新建 PirPaddleParser 实现对应的功能。

### 导师点评