### 姓名

李睿文

### 实习项目

混合专家架构自动切分推导优化

### 本周工作

1. **分析并开发 einsum 算子的切分推导规则**

- 将 einsum 算子的功能按照单操作数和双操作数逐一列举，根据对输入 tensor 的各种可能的切分情况进行分析，得到经验性规则：1. 单操作数：若切分维度是输出中被消去的 axis，则该维度切分状态在输出中为 partial；若输出标记有重复的轴(等效计算为 diagonal)，该重复轴不能切分；2. 双操作数：以上规则再加上，等效计算为 outer 的情况中只能切一个维度：对于存在 ... 广播操作的情况，在需要广播的轴上，x 和 y 维数相同时切分状态应相同，x 和 y 维数不同（一个是 n 一个是 1）时只能切维数是 n 的 tensor。

- pr 链接：https://github.com/PaddlePaddle/Paddle/pull/73753

2. **完善 reshard 模拟切分转换功能pr**

- reshard 模拟切分转换功能：添加了 feature _only_reshard_mesh_shape 和 get_local_slice的功能，实现在不进行实际切分张量的情况下，用迭代模拟的方式得到了理论上每张GPU切分后的local_slice，支持shard,replicate和partail三种齐全的placements，并且支持不均匀切分和多重切分的情况。

- pr 链接：https://github.com/PaddlePaddle/Paddle/pull/74248


#### 问题疑惑与解答

暂无

### 下周工作

1. 完成 reshard 模拟切分转换功能pr的修改。

### 导师点评