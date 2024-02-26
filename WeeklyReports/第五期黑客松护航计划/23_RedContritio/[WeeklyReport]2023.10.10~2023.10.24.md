### 姓名

Github ID: [RedContritio](https://github.com/RedContritio)

### 实习项目

模型迁移工具建设


### 本周工作

1. **更新部分 Tensor inplace method api 的映射规则**

    由于 `paddlepaddle` 主框架的升级，部分 inplace method api 已绑定到 `paddle.Tensor`，原有的过渡期映射方式需要更新。
    因此，本周对这部分 api 的映射规则进行了更新。

    PR (merged): https://github.com/PaddlePaddle/PaConvert/pull/315

2. **添加部分 Tensor inplace method api 的映射文档**

    前期开发过程中，对于比较简单的 Tensor inplace method api 采用先开发映射，后补充文档的方式进行开发。
    对于这 26 个 api，本周补全了映射文档。

    PR (merged): https://github.com/PaddlePaddle/docs/pull/6228

3. **修复部分不符合规范的映射文档**

    由于映射文档开发过程缺少自动化工具检查，因此对于相同表意的项，存在多种不同的表达风格，且文档内存在一些错误的写法。
    为实现后续映射文档撰写后的检查工作自动化，对部分显著错误进行了修复。

    PR (merged): https://github.com/PaddlePaddle/docs/pull/6249

4. **映射主目录自动生成**

    对于[映射主目录文档](https://github.com/PaddlePaddle/docs/blob/develop/docs/guides/model_convert/convert_from_pytorch/pytorch_api_mapping_cn.md)，
    当前目录以手动维护为主，存在大量的失去同步的表单项，且不同条目使用的规范不同。

    为提高可维护性，映射主目录文档拟参考 `COPY-FROM` 的动态生成方法，对表单项进行自动生成，需完成的工作包括：

    - [x] 对 `api_difference` 目录下的映射文档进行自动检查，以确保格式合法；
    - [x] 手动修复不符合规范的映射文档；
    - [ ] 在 ci 流程中触发对映射文档的检查；
    - [ ] 从 `api_difference` 目录中获取映射文档集合的元信息，并基于此生成映射主目录文档；
    - [ ] 对非预期缺失的文档，手动予以补充；
    - [ ] 将映射主目录文档的生成添加到构建流程中。


### 下周工作

1. 添加目录中存在，但内容缺失的映射文档；
2. 参考现有构建流程，将映射目录生成流程加入到文档构建过程中；
3. 参考现有 ci 流程，将映射文档检查流程加入到 ci 流程中；
4. 在 PaConvert 中添加检查工具，用于验证映射文档与映射规则 （`api_aliases` 和 `api_mapping`）的一致性，并兼顾检查缺失文档、未添加映射功能。

### 导师点评
宇博近期完成了inplace的文档补充与部分文档bug的修复，针对文档的各种问题，主动思考，构思了一系列自动化方案降低人工成本，接下来继续努力，将映射文档这一大体系建设得更好，质量更优。
