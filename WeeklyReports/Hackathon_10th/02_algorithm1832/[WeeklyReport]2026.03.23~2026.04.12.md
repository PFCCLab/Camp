### 姓名

杨锃砚



### 实习项目

Paddle API兼容性增强



### 本双周工作

1. **`paddle.get_rng_state`添加别名**

- https://github.com/PaddlePaddle/Paddle/pull/78472
- 状态：Paddle已合入
- 所属：兼容性增强任务
- 描述：
  - `paddle.get_rng_state`作为`paddle.device.cpu.get_rng_state`的别名
  - 模型迁移文档内写为`paddle.random.get_rng_state`别名，实际上pytorch中此API的实现是返回CPU的随机生成器状态，因此更改了引用的原API

2. **`paddle.Tensor.numpy()`添加参数支持**

- https://github.com/PaddlePaddle/Paddle/pull/78491
- 状态：Paddle已合入
- 所属：兼容性增强任务
- 描述：
  - 添加了`force`参数，实际逻辑为忽略此参数
  - 在pytorch中，此参数用于限制API的生效条件，对API内部逻辑没有影响，设置`force=True`会让代码更简洁（不需要将tensor先移动到cpu上），paddle默认行为是`force=True`

3. **`paddle.autograd.function.once_differentiable`添加别名**

- https://github.com/PaddlePaddle/Paddle/pull/78539
- 状态：Paddle已合入
- 所属：兼容性增强任务
- 描述：
  - `paddle.autograd.function.once_differentiable`作为`paddle.autograd.py_layer.once_differentiable`的别名

4. **`PyLayerContext.saved_tensors`添加别名**

- https://github.com/PaddlePaddle/Paddle/pull/78589
- 状态：Paddle已合入
- 所属：兼容性增强任务
- 描述：
  -  属性`PyLayerContext.saved_tensors`作为方法`PyLayerContext.saved_tensor()`的别名
  -  之前添加`PyLayerContext`别名的时候，没有注意到这个API的名字不同，而且是属性不是方法，因此进行查漏补缺，添加了别名

5. **`paddle.Tensor.fill_diagonal_`加装饰器**

- https://github.com/PaddlePaddle/Paddle/pull/78615
- 状态：Paddle已合入
- 所属：兼容性增强任务
- 描述：
  - 虽然此API已经有装饰器处理别名，但由于pytorch的参数顺序不同，因此需要使用专用的装饰器来处理参数的顺序
  - 实际处理的是`wrap`参数，在paddle中排名第三，在torch中排名第二

6. **`paddle.optimizer.optimizer.step`添加参数**

- https://github.com/PaddlePaddle/Paddle/pull/78570
- 状态：Paddle已提交PR
- 所属：兼容性增强任务
- 描述：
  - 添加`closure`参数，用于衡量损失并返回，不加此参数情况下返回None
  - 由于Adam和AdamW优化器重写了基类的step方法，因此也在这两个优化器的step中添加了对应参数

7. **`paddle.Tensor.type`支持调用**

- https://github.com/PaddlePaddle/Paddle/pull/78528
- 状态：正在设计方案
- 所属：兼容性增强任务
- 描述：
  - paddle中`Tensor.type`是属性，返回的是VarType
  - torch中没有这个属性，取而代之的是`Tensor.type()`方法，不带参数调用返回VarType，带参数调用相当于转换tensor的类型
  - 若想要兼容原先用法，在C++层需要同时绑定`type`属性和方法，不过经过实验发现似乎方法会覆盖属性
  - 若想要兼容原先用法，在Python层可以设计一个新的类，使其类型为VarType，但也支持调用。不过要直接在Python层修改，则patch会将C++层的定义覆盖，导致原先`type`属性无法获取
  - 目前最兼容的可行方案：C++层将`type`属性绑定到其它的名字如`_type`上，然后Python层使用新的类进行处理，`__new__`返回tensor的`_type`，`__call__`作为转换类型的操作，这样理论上支持原先的所有用法，额外变化是新增了一个`_type`属性

8. **补充英文文档**

- https://github.com/PaddlePaddle/Paddle/pull/78642
- 状态：Paddle已提交PR
- 所属：兼容性增强任务
- 描述：
  - 为部分缺少文档的API添加文档
  - 为进行兼容性的API添加兼容性说明

9. **修复API别名测试**

- https://github.com/PaddlePaddle/Paddle/pull/78649
- 状态：Paddle已提交PR
- 所属：杂项任务
- 描述：
  - #78472中发现的问题
  - 比较别名和本体，直接比较`type`不够充分，修改为用`is`进行比较

### 下双周工作

1. 修改PaConvert和文档
2. 完善`paddle.Tensor.type`的修改方案并实现


