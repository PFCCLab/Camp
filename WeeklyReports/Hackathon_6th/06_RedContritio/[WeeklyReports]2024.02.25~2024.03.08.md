### 姓名

Github ID: [RedContritio](https://github.com/RedContritio)

### 实习项目

模型迁移工具建设

### 本周工作

1. 对存在于 `paconvert/api_mappings.json` 但缺失的映射文档进行补充，添加对应映射文档。

    - 新增 16 篇映射文档
    - 合并文档检查逻辑，减少检查出现问题的可能性，并参考 [此前意见](https://github.com/PaddlePaddle/docs/pull/6496#discussion_r1493992636)，当类型不符合预设类型时，中断生成。

    - https://github.com/PaddlePaddle/docs/pull/6512

2. 面向更新的 Paddle API 功能，更新映射文档

    基于 [Paddle/#61974](https://github.com/PaddlePaddle/Paddle/pull/61974) 与 [Paddle/#56471](https://github.com/PaddlePaddle/Paddle/pull/56471)，更新映射文档的 paddle 方法签名

    - https://github.com/PaddlePaddle/docs/pull/6513
 
### 下周工作

1. 继续补充完善可映射但缺失的部分映射文档；
2. 添加映射主目录生成时对 `api_aliases` 的处理；
3. 面向更新升级的 Paddle API，更新映射文档、映射方法与测试用例。

### 导师点评

刘宇博近期新增补齐了部分缺失的API映射文档、升级了部分API映射文档。文档的易用性、统一性对用户至关重要，在该项工作中需要 **把握格式规范**、**牢记规范**、**自动化方法**、**手动与自动结合** 等方式，将文档打磨建设得更好。
