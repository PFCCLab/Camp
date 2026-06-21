### 姓名

杨锃砚



### 实习项目

Paddle API兼容性增强



### 本双周工作

1. **新增属性`paddle.Tensor.is_cpu`**

- https://github.com/PaddlePaddle/Paddle/pull/78224
- 状态：Paddle已合入，PaConvert和文档施工中
- 所属：兼容性增强任务
- 描述：
  - 增加动态图和静态图tensor的is_cpu属性，和torch对应API对齐

2. **新增方法`paddle.Tensor.nelement()`**

- https://github.com/PaddlePaddle/Paddle/pull/78264
- 状态：Paddle已合入，PaConvert和文档施工中
- 所属：兼容性增强任务
- 描述：
  - 增加动态图和静态图tensor的nelement方法，实际返回元素数量
  - 最初将其定义为`size`属性的别名，不过`size`本身还有方法的用法，因此后来进行了简化

3. **`paddle.io.RandomSampler`处理generator逻辑追加**

- https://github.com/PaddlePaddle/Paddle/pull/78401
- 状态：Paddle已合入，PaConvert施工中
- 所属：兼容性增强任务
- 描述：
  - torch签名和paddle签名中，`RandomSampler`都包含generator参数，但两者代表的含义不同。paddle的generator参数需要能够iter，直接得到元素，torch的generator参数控制的是随机数生成器，不需要能够iter。若直接转换签名，将会导致错误
  - 因此增加了处理逻辑，如果传入的generator非Iterable，则忽略此参数并向用户抛出警告

4. **`paddle.io.BatchSampler`支持torch参数用法**

- https://github.com/PaddlePaddle/Paddle/pull/78382
- 状态：Paddle已合入，PaConvert施工中
- 所属：兼容性增强任务
- 描述：
  - `BatchSampler`的torch和paddle签名不同，torch的首个参数为sampler，paddle的首个参数为dataset，如果直接按照位置参数传入，则无法正确识别，从而导致报错
  - 因此添加了装饰器，对首个位置参数的类型进行检查，如果是sampler或者Iterable，则使用torch签名，若参数过多则抛出异常，如果不是则按照paddle签名处理

5. **`paddle.Tensor.cuda()`支持更多参数类型**

- https://github.com/PaddlePaddle/Paddle/pull/78294
- 状态：Paddle已合入，PaConvert施工中
- 所属：兼容性增强任务
- 描述：
  - `cuda`方法原先支持的参数类型较少（int, None），无法覆盖从torch直接转换的需求，因此添加了处理逻辑，针对不同的参数类型进行处理，另外添加了参数别名
  - 目前`cuda`方法支持的参数类型为None, paddle.device.Device, int, str, CUDAPlace/CustomPlace/XPUPlace

### 下双周工作

1. 对于已完成的兼容性增强任务，继续修改PaConvert和文档
2. `torch.random.get_rng_state`对齐
3. `torch.Tensor.type`对齐
4. `torch.Tensor.numpy`对齐
5. `torch.optim.Optimizer.step`对齐


