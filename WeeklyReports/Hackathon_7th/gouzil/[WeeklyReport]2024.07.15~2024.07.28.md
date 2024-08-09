### 姓名

田川

### 实习项目

PIR 专项

### 本周工作

1. **对于 name 获取的统一**
  - 优化 GetValueName 相关签名
     * `IsUsedByShadowOutput` -> x
     * `HasValueName` -> x (使用`TryGetValueFirstName`能覆盖现有场景)
     * `SetValueName` -> `SetValueAllNamesWith`
     * `GetValueName` -> `GetValueAllNames`
     * `GetValueOutputName` -> `GetValueOutputNames`
     * 增加`GetValueFirstName`（获取第一个名字）、`TryGetValueFirstName` (optional 用于不需要报错和`HasValueName`的场景)
  - GetValueName 相关签名下沉至 PIR utils
  - 在 run_program_op_node 中替换原有的 name 查找逻辑


### 下周工作

1. **再看看还有没有 `GetValueName` 需要替换的**

### 导师点评

川子推动了动转静散落在多处的 name 获取逻辑的统一，避免了不同逻辑带来的潜在隐患和额外维护成本，而且新的逻辑不需要遍历整个 Program，为性能带来了一些固有提升，这对未来极致性能优化是有帮助的

一些 TODO 可以在接下来的时间做一下：

- `pir.cc` 中 `GetNameMap` 的清理
- `run_program_op_node.h` 中考虑下加 assert，确保一个 Value 只有一个 name（或者在 Python 端做也可以）
