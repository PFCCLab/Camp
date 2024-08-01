### 姓名

曾志鹏

### 实习项目

飞桨稀疏算子API升级适配PIR

### 本周工作

1. **Sparse算子Python API适配**
  - 对一些动静统一的python api，补全静态图单测的任务
     * `paddle.saprse.reshape`
     * `paddle.sparse.add`
     * `paddle.sparse.nn.functional.softmax`
     * `paddle.sparse.nn.functional.subm_conv2d`
     * `paddle.sparse.nn.functional.subm_conv3d`
  - 对于仅在动态图下有定义的api，需要对python API进行适配升级，并补全在动态图和静态图下的单测
     * `paddle.sparse.subtract`
     * `paddle.sparse.multiply`
     * `paddle.sparse.divide`


### 下周工作

1. 继续完成Sparse算子Python API适配工作，编写PIR模式下静态图下的单元测试。

### 导师点评

积极完成，再接再厉
