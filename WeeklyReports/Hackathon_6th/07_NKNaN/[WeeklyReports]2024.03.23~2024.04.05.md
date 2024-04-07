### 姓名

李睿文

### 实习项目

框架 API 易用性提升

### 本周工作

1. **添加 `paddle.linalg.svd_lowrank` API**

- 新增功能需求：公开已有的 linalg.py 中 `svd_lowrank` 函数计算逻辑。

- 修改点：将原来的 `paddle.linalg.pca_lowrank` 内部定义的 `svd_lowrank` 公开成为 `paddle.linalg.svd_lowrank` 。

- 提交 pr 并合入：https://github.com/PaddlePaddle/Paddle/pull/62876

2. **针对 `paddle.nn.initializer.XavierNormal` 和 `paddle.nn.initializer.XavierUniform` 的功能增强**

- 新增功能需求：添加缩放系数 gain。

- 提交 pr 并合入: https://github.com/PaddlePaddle/Paddle/pull/63134

3. **修复 `paddle.nanmedian` 存在的问题**

- 存在的问题：'min' 模式下 index 分配的内存空间大小等于output的空间大小，'avg' 模式下 index 分配的内存空间大小等于output的空间大小的 2 倍。由于之前修改 cpu kernel 时漏改了一处计算 index 的地方，造成了 cpu kernel 底层运算会出现崩溃。

- 提交 pr: https://github.com/PaddlePaddle/Paddle/pull/63221

4. **针对 `paddle.nn.initializer.KaimingNormal` 和 `paddle.nn.initializer.KaimingUniform` 的功能增强**

- 新增功能需求：添加参数 mode，以支持 'fan_in' 和 'fan_out' 两种模式

- 提交 pr：https://github.com/PaddlePaddle/Paddle/pull/63268

#### 问题疑惑与解答

     暂无

### 下周工作

1. 完善已提交的 pr
2. 继续修改其他框架 API

### 导师点评
