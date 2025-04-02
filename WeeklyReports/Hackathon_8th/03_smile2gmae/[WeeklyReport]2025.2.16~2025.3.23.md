### 姓名

刘卉杰

### 实习项目

自动并行切分转换和专家并行机制完善

### 本周工作



1. 完成了 only_reshard_mesh的所有情况的判断，使用模拟法，逐个mesh_dim切分，最终得到所有rank上的tensor_indices，覆盖了之前的 shard切同一个tensor_dim，以及replicate和partial



### 存在的问题

还需要和老师一起确认下正确性 

### 下周工作

1. 确认完正确性之后提一个pr
2. 开始做 MoE Block部分自动并行的任务



### 导师点评

通过