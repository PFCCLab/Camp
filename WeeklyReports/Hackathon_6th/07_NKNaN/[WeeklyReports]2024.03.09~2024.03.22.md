### 姓名

李睿文

### 实习项目

框架 API 易用性提升

### 本周工作

1. **针对 `paddle.nanmedian` 的功能增强**

- 新增功能需求：
     1. 目前 `paddle.nanmedian` 在输入的待计算维度是偶数的情况下求中值的做法是排序后取中间两数的算术平均值，而 torch 则是取最小值，所以希望增加取最小值的功能。
     2. 希望在最小值时同时能够返回最小值对应的 `index`。

- 修改点：增加 `mode` 参数，默认值为 "avg"，可取 "min"；`mode == avg` 保持原逻辑，`mode == min` 时在 kernel 中偶数情况计算的地方将原逻辑替换取最小值，对应的梯度则取 d_output 的值即可。当 `mode == avg` 且 `axis` 为 int 类型时返回非 NaN 中值和对应下标。

- 提交 pr 并已合入：https://github.com/PaddlePaddle/Paddle/pull/62624

2. **针对 `paddle.nn.TransformerEncoderLayer` 的功能增强**

- 新增功能需求：与 `paddle.nn.TransformerDecoderLayer` 一样需添加支持 `layer_norm_eps` 参数。

- 修改点： 添加 `layer_norm_eps` 参数，并传入 `LayerNorm` 层。

- 提交 pr 并已合入：https://github.com/PaddlePaddle/Paddle/pull/62788

3. **添加 `paddle.nn.functional.group_norm` API**

- 新增功能需求：paddle 目前只有 `paddle.nn.GroupNorm`，需添加对应的 `paddle.nn.functional.group_norm` 。

- 修改点：将原来的 `paddle.nn.GroupNorm` forward 方法移植到 `paddle.nn.functional.group_norm` 中。

-  提交 pr：https://github.com/PaddlePaddle/Paddle/pull/62672

4. **添加 `paddle.linalg.svd_lowrank` API**

- 新增功能需求：公开已有的 linalg.py 中 `svd_lowrank` 函数计算逻辑。

- 修改点：将原来的 `paddle.linalg.pca_lowrank` 内部定义的 `svd_lowrank` 公开成为 `paddle.linalg.svd_lowrank` 。（还需添加单测）

- 提交 pr：https://github.com/PaddlePaddle/Paddle/pull/62876

#### 问题疑惑与解答

     暂无

### 下周工作

1. 完善已提交的 pr
2. 继续修改其他框架 API

### 导师点评
