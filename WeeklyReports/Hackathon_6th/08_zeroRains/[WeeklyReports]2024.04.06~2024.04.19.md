### 姓名

卢林军

### 实习项目

组合机制算子专项和机制建设

### 本周工作

本项目的主要工作是对尚未支持组合机制的算子添加组合机制并完善机制，本周主要工作如下：

1. 新增`reduce_as` op并修复其BUG

算子的新增，引起了`test_assign_pos_op`单测的错误，在本地cuda 11.2和cuda 12.0的环境下，均无法复现其错误。最后，是导师及其同事在CI环境中，发现`test_assign_pos_op`的动态图测试出现了问题，估计是和单测执行模式有关，最后将动态图测试从`test_assign_pos_op`拆解出来，并写入新的单测文件中，问题得以解决。

相关 PR:

- https://github.com/PaddlePaddle/Paddle/pull/63064

2. 解决`test_sub_graph_78`中，开启`with_prim=True`会导致单测报错的BUG。

`test_sub_graph_78`的单测是因为在使用`multiply_grad`的反向拆解时，调用反向拆解中的函数`get_reduce_dims_from_out(out_grad_dims, x_dims)`有问题。具体是说，在检测reduce的dim时，使用的索引错误，现已修改成正确的索引。

相关 PR:

- https://github.com/PaddlePaddle/Paddle/pull/63251

3. 补充组合机制开发文档中的动态图支持部分


### 下周工作

1. 尝试对`reduce_as`完成`complex64/128`和`int8`的支持
2. 补充`reduce_as`的中文文档
3. 完善之前尚未merge的PR。

### 导师点评
开发能力强，积极性高：可以独立修复机制相关错误；可以开发独立算子
