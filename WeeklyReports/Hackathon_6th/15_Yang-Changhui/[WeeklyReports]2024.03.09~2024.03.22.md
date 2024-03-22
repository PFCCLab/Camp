### 姓名

杨昌辉

### 实习项目

科学计算领域拓展专项（领域气象方向）

### 本周工作

1. **复现Earthformer，支持ICAR ENSO数据集**
 
	- 完成了earthformer对ICAR ENSO数据集的推理对齐
	
	- 完成了earthformer对ICAR ENSO数据集的训练，由于参数问题，训练后的模型，在测试集上指标超过官方的
	
	- 完成导出模型和静态推理代码


2. **支持SEVIR数据集**

  - 由于SEVIR数据集过大，因此只完成了训练和验证过程，并未对齐精度
  
  - 完成导出模型和静态推理代码，并可对输出进行可视化
  

3. **问题疑惑与解答**
  * 上周训练的时候出现以下错误:
      
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

  - 解决问题：paddle中需要对标量进行数据类型转后，才能进行masked_fill操作，否则会报以上错误
   	
  
### 下周工作

1. 提交了PR，根据导师意见进行代码细节的修改

2. 编写相关技术文档

### 导师点评
昌辉在复现过程中积极沟通、思考解决遇到的问题，同时对套件代码理解比较好，提交的代码质量较好，后续需要完善代码质量、相关技术文档对该篇论文复现工作收尾，并准备下一篇的论文复现工作。再接再厉！
