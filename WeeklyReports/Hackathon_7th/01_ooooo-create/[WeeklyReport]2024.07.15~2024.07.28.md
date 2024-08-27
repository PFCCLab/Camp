### 姓名
方国勇

### 实习项目
PIR 专项

### 本周工作

1. **熟悉 Paddle 仓库和 cmake**
    * 在仅仅修改 FLAGS_enable_pir_api 默认为 True 时，设置了环境变量 FLAGS_enable_pir_api=0，在 import paddle 时并没有同步 FLAGS_enable_pir_api 的值 0,导致 in_pir_mode 函数，判断结果还在旧 IR mode 下，（待阅读相关实现进行分析

2. **修复 PIR 下 PR-CE-Framework 测试流水线**

3. **修复 PIR 单测**

	* 修复大多数使用 static.nn 下不会支持 PIR 的API导致单测失败的这类问题，使用更加具体的 API 来替换。
	* 修复了一些 amp 单测，阅读 PIR 适配 AMP 的方案


### 下周工作

1. 继续完成单测中 static.nn.* 下的 API 替换，整理替换方法
2. 继续修复 PIR 单测
3. 整理遇到的问题到 [PIR 单测推全交流平台](https://github.com/PaddlePaddle/Paddle/issues/66134) 上

### 导师点评
@ooooo-create 重点参与了static.nn的API替换工作，这是一个相对独立且对飞桨未来API动静统一有重要价值的工作。需要注意，有一些API如果已有动静统一的非static.nn的API，则可以考虑标记退场，仅需要适配静态图独有的API即可。
