### 姓名
郑天宇

### 实习项目
自动并行在复杂模型结构下的能力摸底和技术储备

### 本周工作

1. **对自动并行及工作相关信息进行学习**

  * 学习了动态图，静态图组网，数据并行，张量并行，流水并行
  * 学习了如何使用docker部署paddle，编译，提交rfc、pr等流程 


2. **开发了load_state_dict_from_url API，并写了多个单测**

    * 为paddle.hub开发了新的加载 Paddle 序列化对象的API
      * 可以通过URL下载并加载 Paddle 序列化对象
      * 可以通过URL下载并解压ZIP格式的模型权重文件，再加载 Paddle 序列化对象
      * 当权重文件存在时，可以直接加载 Paddle 序列化对象


### 下周工作

1. 实现在组网时打印每路dp的loss
2. 离线aadiff检查
3. 在线aadiff检查
4. zero padding check

### 导师点评