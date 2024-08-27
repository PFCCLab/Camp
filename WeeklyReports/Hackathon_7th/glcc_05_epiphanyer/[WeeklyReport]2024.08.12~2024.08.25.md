### 姓名

曾志鹏

### 实习项目

飞桨稀疏算子API升级适配PIR

### 本周工作

1. **Sparse算子Python API适配**
  - 对于仅在动态图下有定义的api，需要对python API进行适配升级，并补全静态图下的单测。它们是`paddle/sparse/binary.py`中的二元算子，包括：
     * `paddle.sparse.coalesce`
     * `paddle.sparse.addmm`
     * `paddle.sparse.matmul`
     * `paddle.sparse.masked_matmul`
     * `paddle.sparse.mv`
     * `paddle.sparse.is_same_shape`



### 下周工作

1. 查漏补缺，对一些没有编写PIR分支的算子API继续编写PIR分支代码，并且为没有编写静态图单测的测试代码编写PIR静态图单测。

### 导师点评


