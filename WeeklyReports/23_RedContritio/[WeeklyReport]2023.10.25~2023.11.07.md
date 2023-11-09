### 姓名

Github ID: [RedContritio](https://github.com/RedContritio)

### 实习项目

模型迁移工具建设


### 本周工作

1. **添加部分缺失的 api 映射文档**

    对于映射主目录文件中，存在部分 api 尚未开发映射文档。为实现映射主目录的自动生成，需要先对缺失的 api 映射文档进行补充并对存量的不符合规范 api 进行修复。
    对于相关的 16 个 api，新增/修复了映射文档。

    PR (merged): https://github.com/PaddlePaddle/docs/pull/6252

2. **映射主目录自动生成**

    对于[映射主目录文档](https://github.com/PaddlePaddle/docs/blob/develop/docs/guides/model_convert/convert_from_pytorch/pytorch_api_mapping_cn.md)，
    当前目录以手动维护为主，存在大量的失去同步的表单项，且不同条目使用的规范不同。

    为提高可维护性，映射主目录文档拟参考 `COPY-FROM` 的动态生成方法，对表单项进行自动生成，需完成的工作包括：

    - [x] 对 `api_difference` 目录下的映射文档进行自动检查，以确保格式合法；
    - [x] 手动修复不符合规范的映射文档；
    - [ ] 在 ci 流程中触发对映射文档的检查；
    - [x] 从 `api_difference` 目录中获取映射文档集合的元信息，并基于此生成映射主目录文档；
    - [x] 对非预期缺失的文档，手动予以补充；
    - [x] 将映射主目录文档的生成添加到构建流程中。

    PR (merged): https://github.com/PaddlePaddle/docs/pull/6256


3. **映射单测调用多样性检测工具**
    
    参考 [PaConvert 贡献代码教程中单测部分](https://github.com/PaddlePaddle/PaConvert/blob/master/docs/CONTRIBUTING.md#步骤5编写单元测试)，根据描述，有以下要求：

    > 单测覆盖范围要求为：涉及到多个API形参的，应包含各种参数用法（ 全部指定关键字、全部不指定关键字、改变关键字顺序、默认参数均不指定 四种情况必须考虑），不能只考虑最简单常见的用法，要求至少列举5种不同的使用case（越多越好）。

    但在实际的映射开发过程中，对这些规范的检查往往是人力进行，对于复杂的 api，容易疏忽而导致覆盖不全面。

    为提高单测调用多样性，增加功能覆盖率，考虑对 `APIBase` 进行 patch，在其调用时，记录所有测试的代码，并基于这些测试代码的文本进行分析。

    具体的，包含以下标准：

    1. 对于单测中出现的每个 api，其必须在 api_mapping.json 中出现，或配置了别名 api_alias。
    2. 对于每个 api （如 `torch.a.b.c`）的测试代码，其必须包含该 api 的一个全字匹配非空后缀，如 `torch.a.b.c`、`a.b.c`、`b.c`、`c`，否则报 `ValueError`。
    3. 当前假设所有 api 均为函数调用（包括类、方法等），匹配其第一个匹配后的括号内内容作为参数，如果匹配失败则报 `ValueError`。
    4. 验证时读入所有的 `args` 和 `kwargs`，并基于其 api_mapping 数据，进行以上四种测试。特别的，目前支持了 `*` 置入参数列表，其表明后面的参数不可作为位置参数。尚无支持 `/`，`*args`，`**kwargs` 这三种参数。

    目前已初步完成工具的开发，并基于该工具进行验证，修复 53 个不符合规范的单元测试与约 10 项 `api_mapping` 映射数据。

    PR: https://github.com/PaddlePaddle/PaConvert/pull/328


### 下周工作

1. 完善 PaConvert 单测检查工具；
2. 基于单测检查工具，继续修复完善单测；
3. 修复现有的映射表 api_mapping.json；
4. 参考现有 ci 流程，将映射文档检查流程加入到 ci 流程中；

### 导师点评
