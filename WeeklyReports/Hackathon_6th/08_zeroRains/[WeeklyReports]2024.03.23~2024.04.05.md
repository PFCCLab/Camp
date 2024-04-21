### 姓名

卢林军

### 实习项目

组合机制算子专项和机制建设

### 本周工作

本项目的主要工作是对尚未支持组合机制的算子添加组合机制并完善机制，本周主要工作如下：

1. 新增`sum_as` op

在`broadcast`类算子的反向拆解，动态shape的输入在编译器无法拿到reduce_dim，没法正常执行。因此需要`sum_as` op解决这一场景，具体实现与描述见PR。

相关 PR:

- https://github.com/PaddlePaddle/Paddle/pull/63064

2. 解决`test_sub_graph_73`中，开启`with_prim=True`会导致单测报错的BUG。

出问题的地方在于gather_nd_grad的反向拆解使用了prim op scatter_nd_add, 在scatter_nd_add的infershape中有涉及到对tensor shape具体数值的断言，但输入的tensor是dynamic shape，从而导致断言触发。现在我在infershape里加了一个dynamic shape的判断，只有不是动态shape的时候才执行那个断言。

相关 PR:

- https://github.com/PaddlePaddle/Paddle/pull/63276


### 下周工作

1. 尝试修复`test_sub_graph_46, 65, 66, 78`开启`with_prim=True`会导致单测报错的BUG。
2. 完善之前尚未merge的PR。

### 导师点评
能高效开发飞桨算子；初步解决组合机制遇到的问题，建议将问题调试的经验总结成文档，便于社区开发者参考学习。
