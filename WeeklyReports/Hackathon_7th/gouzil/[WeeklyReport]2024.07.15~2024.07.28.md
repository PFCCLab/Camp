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

1. **在看看还有没有 GetValueName 需要替换的**

### 导师点评
