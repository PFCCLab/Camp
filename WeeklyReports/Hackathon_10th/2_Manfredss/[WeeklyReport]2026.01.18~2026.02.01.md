### 姓名
戚文斐

### 实习项目
Paddle API 兼容性增强

### 本周工作
1. [PR #77300](https://github.com/PaddlePaddle/Paddle/pull/77300)
paddle.nn.funtional.relu / paddle.nn.functional.leaky_relu / paddle.nn.functional.relu_ / paddle.nn.functional.leaky_relu_ 以及 paddle.relu 对齐, 使用装饰器。PR 已合入
2. [PR #77194](https://github.com/PaddlePaddle/Paddle/pull/77194) paddle.randint 对齐, 使用装饰器。PR 已合入
3. [PR #77078](https://github.com/PaddlePaddle/Paddle/pull/77078) paddle.inverse 对齐, 采用 cpp 下称机制。在对齐过程中发现现有的 api patch 机制存在缺陷，表现为 CI/CE-Framework 测试不通过, 经本地测试确认此缺陷：
```bash
pytest paddletest/framework/api/linalg/test_inv.py # Test Fail
```
通过调研发现缺陷存在于代码生成器。改进措施：生成器增强，扩展 monkey_patch_gen.py 以支持通用模块路径。
- 新增 `generic_funcs_map` 储存 (`module_path`, `method_name`, `method`) 元组
- 修改 `ClassifyAPIByPrefix` 函数将未匹配的 `paddle.*` 前缀纳入通用映射表
- 在运行时通过 `getattr()` 动态调用目标模块并设置属性

修改文件：`paddle/fluid/eager/auto_code_generator/generator/monkey_patch_gen.py`
结论：未来添加类似路径的 API，如 paddle.fft.* 等时，只要在 yaml 文件中配置即可
PR 已合入
4. [PR #77168](https://github.com/PaddlePaddle/Paddle/pull/77168) paddle.deg2rad 对齐，使用装饰器。PR 已合入
5. [PR #77333](https://github.com/PaddlePaddle/Paddle/pull/77333) 新增 paddle.addcmul api，对齐 pytorch 别名，但是现有测试的 coverage test 依然不够标准，有待后续跟进。整体实现已完成，已被 Approved。待 coverage test 完善后最终 review。
6. [PR #77170](https://github.com/PaddlePaddle/Paddle/pull/77170) paddle.lerp 对齐，实验了能否将 `weight` 参数的值的类型改为 `Scalar` 然后采用 cpp 下沉。结论是不可以，因为 `weight` 需要接受多元素，而 `Scalar` 只能接受标量。现在尝试采用 mapper 的方式进行cpp 下沉。在 `paddle/fluid/pybind/args_mapper.cc` 中添加辅助函数 `LerpMapper` 和 `LerpInplaceMapper` 并在 `python_api_info.yaml` 中添加 `Lerp` 和 `LerpInplace` 的参数映射关系。目前在研究 inplace 版本和不是 inplace 版本能否共用一个 Mapper，解决后再进行 review。

### 下周工作
1. 继续 paddle.addcmul 和 paddle.lerp 的收尾工作，争取合并 PR
2. 检查上述所有 api 的 paconvert 是否正常，并修改对应的中文文档
3. 有时间认领 paddle.nn.ParameterDict, paddle.nn.functional.pixel_shuffle, paddle.mm 和 paddle.Tensor.tile 这几个 api 的对齐工作。

### 导师点评
