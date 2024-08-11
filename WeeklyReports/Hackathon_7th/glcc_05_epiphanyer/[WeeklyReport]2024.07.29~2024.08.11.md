### 姓名

曾志鹏

### 实习项目

飞桨稀疏算子API升级适配PIR

### 本周工作

1. **Sparse算子Python API适配**
  - 对一些动静统一的python api，补全静态图单测的任务
     * `paddle.sparse.nn.functional.max_pool3d`
  - 对于仅在动态图下有定义的api，需要对python API进行适配升级，并补全静态图下的单测。它们是`paddle/sparse/unary.py`中的算子，包括：
     * `paddle.sparse.sin`
     * `paddle.sparse.tan`
     * `paddle.sparse.asin`
     * `paddle.sparse.transpose`
     * `paddle.sparse.atan`
     * `paddle.sparse.sinh`
     * `paddle.sparse.asinh`
     * `paddle.sparse.atanh`
     * `paddle.sparse.tanh`
     * `paddle.sparse.square`
     * `paddle.sparse.sqrt`
     * `paddle.sparse.log1p`
     * `paddle.sparse.pow`
     * `paddle.sparse.neg`
     * `paddle.sparse.abs`
     * `paddle.sparse.cast`
     * `paddle.sparse.rad2deg`
     * `paddle.sparse.deg2rad`
     * `paddle.sparse.expm1`
     * `paddle.sparse.relu6`
     * `paddle.sparse.leaky_relu`


### 下周工作

1. 完成剩下的所有的Sparse算子Python API适配工作，编写PIR模式下静态图下的单元测试。

### 导师点评


