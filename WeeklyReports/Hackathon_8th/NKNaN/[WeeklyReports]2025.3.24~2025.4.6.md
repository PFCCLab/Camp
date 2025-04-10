### 姓名

李睿文

### 实习项目

混合专家架构自动切分推导优化

### 本周工作

1. **分析 take_along_axis 算子的切分推导规则**

- 将输入 tensor 的各种可能的切分情况，以及其他输入参数的可能情况进行组合得到不同的 case，再根据不同 case 的切分后输出是否与切分前输出是否一致，判断输入切分状态是否合理以及输出的切分状态。最后总结得到 take_along_axis 算子切分推导的经验性规则：1. x 的 axis 维度不能切分；2. index 的切分要与 x 切分的维度一致，且可以再加上切分 axis 维； 3. out 与 index 切分状态一致。


2. **开发 take_along_axis 算子的切分推导规则**

- 根据分析得到的经验性规则开发 take_along_axis 算子的切分推导规则，将分析时使用的 case 做为单测案例。pr 链接：https://github.com/PaddlePaddle/Paddle/pull/72063


#### 问题疑惑与解答

暂无

### 下周工作

1. 完善 take_along_axis 算子的切分推导规则以及 pr
2. 分析 put_along_axis 算子的切分推导规则

### 导师点评
