### 姓名

杨锃砚



### 实习项目

Paddle API兼容性增强



### 本双周工作

1. **兼容性装饰器的报错提示信息优化**

- https://github.com/PaddlePaddle/Paddle/pull/77916
- 状态：已合入
- 所属：衍生的杂项任务
- 描述：
  - 更新参数别名装饰器的报错提示，新的提示内容为"无法同时指定原参数和别名"

2. **文档中添加参数别名说明**

- https://github.com/PaddlePaddle/Paddle/pull/77935
- https://github.com/PaddlePaddle/docs/pull/7675
- 状态：已合入
- 所属：兼容性增强任务
- 描述：
  - 向中英文文档补充了参数别名的说明
  - 此工作属于重复性高的工作，或可使用agent完成

3. **`paddle.autograd.PyLayerContext`添加别名**

- https://github.com/PaddlePaddle/Paddle/pull/78114
- 状态：Paddle仓库审阅中
- 所属：兼容性增强任务
- 描述：
  - 涉及到文档中五个API别名
  - 通过在对应的包添加导入来实现API别名

4. **`paddle.utils.data`添加别名**

- https://github.com/PaddlePaddle/Paddle/pull/78204
- 状态：已提交PR
- 所属：兼容性增强任务
- 描述：
  - 原先`paddle.utils.data`中的API已经通过添加导入的方式添加别名，然而在后续的PaConvert检查中，发现其中方法还存在一些文档内没写的别名（如`paddle.utils.data._utils.default_collate`），这些调用方式是随着PyTorch的演化产生的，此PR添加了这一部分的别名
  - 整理了paddle.utils.data文件夹的结构，使别名能够被正确调用

**[*] 本周有其它事务处理，时间受限**

### 下双周工作

1. 对于已完成的兼容性增强任务，修改PaConvert和文档
2. 如有时间剩余，继续认领完成其它任务（预计开展以下API的兼容性工作：`paddle.Tensor.cuda`, `paddle.Tensor.is_cpu`, `paddle.Tensor.nelement`、`torch.nn.ReLU`）


