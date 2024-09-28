### 姓名

吕东翼

### 实习项目

PaddleNLP 套件能力建设

### 本周工作

本项目的主要工作是tokenizer对齐，本周主要工作如下：

1. 优化add_special_token函数，允许replace_additional_special_tokens

相关 PR:

- https://github.com/PaddlePaddle/PaddleNLP/pull/9144 (Merged)

2. 允许padding_side做为调用时参数

相关 PR:

- https://github.com/PaddlePaddle/PaddleNLP/pull/9161 (Merged)

3. 支持Tokenizer读取Tiktoken tokenizer.model

同时对部分代码进行了重构，将 `PretrainedTokenizerBase.from_pretrained` 拆分为两个单独的方法：`from_pretrained` 和 `_from_pretrained` ，当 `FastTokenizer` 可用时优先使用 ，使用 LazyMapping 来在访问时动态加载键和值，整理了部分常量。

相关 PR：

- https://github.com/PaddlePaddle/PaddleNLP/pull/9215 (Opened)

### 下周工作

1. 完善工作3，加入更多测试

2. 继续tokenizer对齐

### 导师点评

