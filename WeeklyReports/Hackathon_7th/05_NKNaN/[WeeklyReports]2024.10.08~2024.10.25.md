### 姓名

李睿文

### 实习项目

框架 API 易用性提升

### 本周工作

1. **`paddle.linalg.slogdet` 支持复数**

- 增加前向和反向 kernel 的复数类型支持

- pr 链接：https://github.com/PaddlePaddle/Paddle/pull/68772

2. **支持整数类型输入的数学计算类API**

- 梳理需要支持的API，并整理数学计算类API的中英文文档中对支持数据类型的描述

- pr 链接：https://github.com/PaddlePaddle/Paddle/pull/68866， https://github.com/PaddlePaddle/docs/pull/6916

3. **修复 `paddle.distribution.StudentT`**

- 支持输入参数 df, loc, scale 的类型可以是 float 和 Tensor 的混合。修复：输入参数全为 float 或 0-D Tensor 时，每个方法应该返回 0-D Tensor 而不是 1-D Tensor

- pr 链接：https://github.com/PaddlePaddle/Paddle/pull/68895

4. **修复 `paddle.distribution.LKJCholesky`**

- 修复 concentration  是 1-D tensor 时 sample 方法返回值的维度问题

- pr 链接：https://github.com/PaddlePaddle/Paddle/pull/68922

5. **修复 `paddle.distribution.Constraint`**

- 将 paddle.distribution.constraint.Constraint 的回调方法由 `__call__` 改为 `check`，与 pytorch 对齐

- pr 链接：https://github.com/PaddlePaddle/Paddle/pull/68996

6. **排查 distribution API 的 0D 输入问题**

- 排查并修复 distribution API 的 0D 参数输入问题，并给 sample/rsample 方法增加默认值

- pr 链接：https://github.com/PaddlePaddle/Paddle/pull/69090

#### 问题疑惑与解答

暂无

### 下周工作

1. 完善已修改 API 的映射文档以及 PaConvert 中的 json 映射规则/mathcer/单测
1. 继续排查 distribution API 的 0D 输入问题
1. 完成数学计算类API对整数类型输入的支持

### 导师点评
李睿文近期完成了多个API的修改，注意对每一个API的修改，需要完善json 映射规则/mathcer/单测。按上面的下周工作整体开展即可。
