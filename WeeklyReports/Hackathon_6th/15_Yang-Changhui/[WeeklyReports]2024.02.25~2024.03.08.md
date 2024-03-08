### 姓名

杨昌辉

### 实习项目

科学计算领域拓展专项（领域气象方向）

### 本周工作

1. **阅读earthformer论文**

2. **复现earthformer**

  - 下载ICAR-ENSO数据集，并完成该数据集的读取与加载
  
  - 使用PaConvert完成了网络的转换，并修改其中的一些错误
  
  - 完成了学习率、优化器、loss、metric相关代码的编写，并实现了训练的过程

3. **问题疑惑与解答**
  * 训练的时候出现以下错误:
      
```

    W0307 19:58:24.192648  9727 gpu_resources.cc:119] Please NOTE: device: 0, GPU Compute Capability: 7.0, Driver API Version: 12.0, Runtime API Version: 11.8

    W0307 19:58:24.194325  9727 gpu_resources.cc:164] device: 0, cuDNN Version: 8.9.

    [2024/03/07 19:58:45] ppsci WARNING: The argument: 'lr_scheduler' now automatically retrieves from 'optimizer._learning_rate' when 'optimizer' is given, so it is recommended to remove it from the Solver's initialization arguments.

    [2024/03/07 19:58:45] ppsci INFO: Using paddlepaddle 2.6.0 on device Place(gpu:0)

    [2024/03/07 19:58:45] ppsci INFO: Set to_static=False for computational optimization.

    W0307 19:58:47.696384  9727 dygraph_functions.cc:52641] got different data type, run type protmotion automatically, this may cause data type been changed.

    W0307 19:58:47.696985  9727 dygraph_functions.cc:52641] got different data type, run type protmotion automatically, this may cause data type been changed.

    W0307 19:58:47.697081  9727 dygraph_functions.cc:52641] got different data type, run type protmotion automatically, this may cause data type been changed.
```

  - 考虑是PaConvert转换时，网络的数据类型转换方式并没有完全对齐
  
### 下周工作

1. 完成earthformer的推理对齐，并修复以上问题

2. 完成整个训练过程，并查看精度对齐

### 导师点评

该论文代码基于pytorch lightning，封装程度较高，转换工作量多、难度大，昌辉同学目前已完成数据集、学习率、优化器等模块的编写转换，并实现了训练过程，高效率地完成了本周工作，点赞。