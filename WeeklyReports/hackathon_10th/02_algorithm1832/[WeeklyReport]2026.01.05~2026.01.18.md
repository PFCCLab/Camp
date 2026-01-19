### 姓名

杨锃砚



### 实习项目

Paddle API兼容性增强



### 本双周工作

1. **修复eager_api从kwarg获取内容的逻辑**

- https://github.com/PaddlePaddle/Paddle/pull/77234
- 状态：已合入
- 所属：衍生的杂项任务
- 描述：
  - 修改了`op_function_common.cc`中的方法`GetItemFromArgsOrKWArgs`，使得PyObject能够从kwargs中多次获取。
  - 原先此函数的逻辑为解析输入、将PyObject从args和kwargs取出，每次从kwargs取走一个对象，计数减一，为后续kwargs数量校验服务。然而kwargs数量校验完毕后，仍会存在从kwargs中取PyObject的需求，此时计数没有意义，因而移除了对于计数的判断。

2. **torch.std对齐**

- https://github.com/PaddlePaddle/Paddle/pull/77006
- 状态：Paddle仓库已合入，PaConvert和中文文档修改进行中
- 所属：API兼容性增强任务
- 描述：
  - 使用参数转发的方式，为`std`添加了torch形式的参数别名和其它缺少的参数。
  - `std`实际上是依次执行`var`和`sqrt`，而这两个API兼容性适配已经完成。因此经过讨论决定不使用别名装饰器，减小性能的损耗。直接进行参数转发，将参数转发给`var`，通过overload和处理签名的装饰器来为方法添加签名。同时补充了兼容性的单测，顺便修了单测所属文件内的typo。

3. **abs_下沉**

- https://github.com/PaddlePaddle/Paddle/pull/77294
- 状态：Paddle仓库Review进行中
- 所属：API兼容性增强任务、inplace API下沉系列任务
- 描述：
  - See Also: https://github.com/PaddlePaddle/Paddle/pull/76994
  - See Also: https://github.com/PaddlePaddle/Paddle/pull/76431
  - 为inplace api的eager_api增加了从kwarg取结果的逻辑、增加了inplace api的kwarg数量检查逻辑、下沉了`abs_`，补充了下沉后的相关单测。
  - 第一版方案：增加从kwarg取结果的逻辑，修改`ToPyObject`方法。
  - 第二版方案：尽可能复用已有代码，从kwarg取内容的逻辑可以使用`GetItemFromArgsOrKWArgs`，这样只需要一个map（输出位置 - PyObject）。
  - 后来决定使用第一版方案，因为第二版过于复杂。由于涉及到代码生成逻辑，对于返回PyTuple类型的处理等，因此整个过程花费了较多时间。

4. **`ChainDataset`, `ConcatDataset`, `Dataset`, `IterableDataset`对齐**

- 状态：正在实现和测试当前方案
- 所属：API兼容性增强任务
- 描述：
  - See Also: https://github.com/PaddlePaddle/Paddle/pull/77334
  - See Also: https://github.com/PaddlePaddle/Paddle/pull/77212
  - 在`paddle.utils`新增对应类的导入，但不在`__init__.py`注册，补充单测。
  - 第一版方案：在`paddle.utils`新增对应类的代码（从`paddle.io`复制过来）。
  - 第二版方案：整理`paddle.utils`，将有问题的全部迁入另一个文件夹，不对外暴露，仅内部使用。
  - 第三版方案：先新增导入不注册，后续再根据导入情况选择性注册。
  - 目前用的是第三版方案。直接导入`paddle.io`内的类会导致循环依赖，前两个方案涉及到的修改比较复杂。所以把整个任务分成两部分：先新增别名（通过`paddle.utils.data`访问），再考察如何绕开循环依赖，使得从`paddle`就能够访问对应的类。



### 下双周工作

1. **torch.std对齐**的PaConvert和中文文档修改
2. **abs_下沉**的PaConvert和中文文档修改
3. **`ChainDataset`, `ConcatDataset`, `Dataset`, `IterableDataset`对齐**的选择性注册方法，PaConvert和英文&中文文档修改
4. 如有时间剩余，继续认领完成其它任务



### 导师点评

杨锃砚同学近期完成了`torch.std`下沉和两个较为复杂的共性问题调研开发：inplace下沉机制调研 +  paddle.utils.data.*模块迁移。针对这两个共性问题调研了多种可行方案，在此过程中主动学习相关技术，对飞桨框架相关的代码也有了更多理解。后续继续保持学习和探索的势头，为飞桨贡献更多代码。