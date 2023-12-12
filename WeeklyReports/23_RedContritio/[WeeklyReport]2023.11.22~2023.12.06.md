### 姓名

Github ID: [RedContritio](https://github.com/RedContritio)

### 实习项目

模型迁移工具建设

### 本周工作

1. **api 单测补充与完善**

    由于转换工具开发过程中，对 api 转换的单测最初设计时存在检查不严格、覆盖率不够等问题。为提高转换工具可维护性，根据更新后的单测规范，主要进行以下几方面工作：

    1. 完善单测用例，争取 api 不同用法完全覆盖；
    2. 检查 `api_mapping.json` 数据是否符合实际情况，是否有少标、错标的现象；
    3. 检查 `api_matcher.py` 能否正确匹配与转换。

    PR:
    - https://github.com/PaddlePaddle/PaConvert/pull/335
    - https://github.com/PaddlePaddle/PaConvert/pull/338
    - https://github.com/PaddlePaddle/PaConvert/pull/339
    - https://github.com/PaddlePaddle/PaConvert/pull/342
    - https://github.com/PaddlePaddle/PaConvert/pull/343
    - https://github.com/PaddlePaddle/PaConvert/pull/344
    - https://github.com/PaddlePaddle/PaConvert/pull/345

### 下周工作

1. 继续修复完善单测，提高用例覆盖面；
2. 继续补充映射表 `api_mapping.json`；
3. 维护设计不合理的 `Matcher`。

### 导师点评

刘宇博同学在单测和Matcher的维护下，设计了良好可用的单测检查工具，很好减少了人工排查的工作量，同时对于各种corner case分析细致。后续将基于已检查出的各种单测问题，全面地毯式的提升单测质量，从而进一步提升Matcher的质量。期待工作成果的落地。
