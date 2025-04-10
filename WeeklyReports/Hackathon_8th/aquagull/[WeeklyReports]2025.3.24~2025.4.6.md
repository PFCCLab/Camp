### 姓名
何泓域

### 项目
框架作为array-api-compat后端

### 本周工作

修正prod、eye、expand_dims、vecdot几个array-api-compat后端接口，以让其通过测试。[仓库链接](https://github.com/HydrogenSulfate/array-api-compat/compare/support_paddle...aquagull:array-api-compat:support_paddle)

#### PR：
- 修复paddle.nozero [PR](https://github.com/PaddlePaddle/Paddle/pull/72003)

- 修复paddle.tensordot [PR](https://github.com/PaddlePaddle/Paddle/pull/72139)

- 修复sum [PR](https://github.com/PaddlePaddle/Paddle/pull/72138)

#### 还在开发中：

- 为svdvals支持GPU [PR](https://github.com/PaddlePaddle/Paddle/pull/71930)

### 下周工作

继续完善svdvals，并开始为matmul、index_select、round增加新特性以通过array-api-compat测试。
