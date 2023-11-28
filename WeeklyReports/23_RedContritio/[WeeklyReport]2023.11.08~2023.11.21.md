### 姓名

Github ID: [RedContritio](https://github.com/RedContritio)

### 实习项目

模型迁移工具建设


### 本周工作

1. **映射单测调用多样性检测工具维护**
    
    参考 [PaConvert 贡献代码教程中单测部分](https://github.com/PaddlePaddle/PaConvert/blob/master/docs/CONTRIBUTING.md#步骤5编写单元测试)，根据描述，有以下要求：

    > 单测覆盖范围要求为：涉及到多个API形参的，应包含各种参数用法（ 全部指定关键字、全部不指定关键字、改变关键字顺序、默认参数均不指定 四种情况必须考虑），不能只考虑最简单常见的用法，要求至少列举5种不同的使用case（越多越好）。

    但在实际的映射开发过程中，对这些规范的检查往往是人力进行，对于复杂的 api，容易疏忽而导致覆盖不全面。

    为提高单测调用多样性，增加功能覆盖率，考虑对 `APIBase` 进行 patch，在其调用时，记录所有测试的代码，并基于这些测试代码的文本进行分析。

    具体的，本次维护与功能更新包括以下部分：

    - [x] 支持属性映射 `ATTRIBUTE_MAPPING` 跳过检查；
    - [x] 移动了约 20 个 `attribute`` 到对应映射关系文件；
    - [x] 支持可变参数 `*args, **kwargs`；
    - [x] 支持识别 `==`, `lambda` 等运算符、关键字作为参数的识别；
    - [x] 添加了对于抽象方法、可重载方法的标注，当前做跳过处理；
    - [x] 补充约 50 个 api 的映射单元测试用例，以完善覆盖范围。
    
    PR:
    - https://github.com/PaddlePaddle/PaConvert/pull/330

2. **现存 bug 修复**

    由于此前转换工具的开发遗留问题，当前 CI 流程或实际功能存在部分 bug，详情与修复如下：

    - [x] 原计划支持 `torch==1.3.0`，现更新支持计划至 `torch==2.1.0`，部分 api 条件检查更加严格导致单测出错。
          修复了 `tests/test_nn_utils_clip_grad_value_.py` 中出错的两个用例；
    - [x] `Consistency` CI 中，存在 python 版本硬编码与依赖缺失的问题；修复了对应测试脚本；
    - [x] 当类方法调用时，其实例如果存在链式调用，可能导致其正则解析出错；添加了对应的转义规则。

    PR:
    - https://github.com/PaddlePaddle/PaConvert/pull/330
    - https://github.com/PaddlePaddle/PaConvert/pull/334

### 下周工作

1. 继续修复完善单测，提高用例覆盖面；
2. 补充现有映射表 `api_mapping.json`。

### 导师点评

单测数量庞大，亟待全面清理，刘宇博同学思考的自动检测工具极大的提升了效率，期待后续更好的全面摸排并修复庞大且纷繁复杂的单测问题，建设更好的转换工具。
