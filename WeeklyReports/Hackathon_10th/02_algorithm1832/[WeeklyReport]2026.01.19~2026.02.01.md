### 姓名

杨锃砚



### 实习项目

Paddle API兼容性增强



### 本双周工作

1. **torch.std对齐**

- https://github.com/PaddlePaddle/Paddle/pull/77006
- https://github.com/PaddlePaddle/PaConvert/pull/804
- https://github.com/PaddlePaddle/PaConvert/pull/813
- https://github.com/PaddlePaddle/docs/pull/7680
- 状态：CI通过，等待合入
- 所属：API兼容性增强任务
- 描述：
  - 在PaConvert增强对应的测试用例，补充中文文档修改
  - 内容详情详见上次双周周报

2. **abs_下沉**

- https://github.com/PaddlePaddle/Paddle/pull/77294
- https://github.com/PaddlePaddle/PaConvert/pull/811
- https://github.com/PaddlePaddle/docs/pull/7697
- 状态：全部已合入
- 所属：API兼容性增强任务、inplace API下沉系列任务
- 描述：
  - 在PaConvert增强对应的测试用例，补充中文文档修改
  - 内容详情详见上次双周周报

3. **`paddle.utils.data.*`对齐**

- https://github.com/PaddlePaddle/Paddle/pull/77391
- https://github.com/PaddlePaddle/Paddle/pull/77446
- https://github.com/PaddlePaddle/Paddle/pull/77451
- https://github.com/PaddlePaddle/Paddle/pull/77591
- https://github.com/PaddlePaddle/PaConvert/pull/817
- 状态：CI通过，等待合入
- 所属：API兼容性增强任务
- 描述：
  - 实现了上个双周的方案，通过`paddle.utils`的按需导入，延后了对应类和方法的导入时机，不会触发循环依赖，同时补充了对应的单测
  - PaConvert测试过程中发现存在`torch.utils.data.dataloader.default_collate`这个用法，在torch文档里没有写，paddle的API差异文档也没写，但PaConvert做了测试，所以后来加了一下别名
  - 目前处理了"仅API调用方式不一致"的所有API（10个API）

4. **装饰器优化**

- https://github.com/PaddlePaddle/Paddle/pull/77497
- https://github.com/PaddlePaddle/Paddle/pull/77561
- 状态：全部已合入，系列任务进行中
- 所属：API兼容性增强任务、衍生的杂项任务
- 描述：
  - 有些API为了实现兼容性，使用了自己定义的装饰器，后来定义了通用的别名装饰器，自定义装饰器性能会比通用装饰器差一点，所以尽量替换为通用装饰器
  - 通用装饰器`ParamAliasDecorator`可以处理任意别名情况，但性能较差，将单参数别名和双参数别名的替换为`param_one_alias` 和`param_two_alias`提高性能



### 下双周工作

1. **`paddle.utils.data.*`对齐**的中文文档修改
2. **装饰器优化**进行下一子任务：自定义装饰器代码可读性差，通过overload维护方法签名增强可读性
3. **inplace API下沉系列任务**进行下一子任务：inplace API的`python_api_info.yaml`解析处理（原先逻辑似乎是直接用非inplace版本的配置，不够灵活）
4. 继续认领完成其它任务



### 导师点评

杨锃砚同学半个月来积极开展工作，顺利完成了多个API的兼容性增强，同时完成3个API机制优化的工作：

1. inplace下沉机制优化
2. `torch.utils.data.*`批量对齐与导入路径设计
3. 装饰器性能与可读性优化

API机制优化的工作，相比单个API更有难度，体现出对Paddle代码有了较好理解。后续将上述工作继续收尾，由于机制优化工作更为重要，在日常工作中需优先开展，然后再开展剩余API的对齐。