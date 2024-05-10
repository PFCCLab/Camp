### 姓名
马欣楷

### 实习项目
CINN 支持动态 Shape 专项（前端方向）

### 本周工作
1. 与导师讨论并敲定reduce_mean api性能优化方案，需要完成generate shape op的中端代码生成，最终消除reduce_mean产生的第一个kernel，目前已提交pr https://github.com/PaddlePaddle/Paddle/pull/64167, 争取下周合入
2. 修复部分inferSymbolicShape和inferMeta推导结果不一致的问题，包括：
    * 部分算子inferMeta未考虑输入张量部分dim为-1的情况 pr: https://github.com/PaddlePaddle/Paddle/pull/63961
    * 符号推导机制缺少对max/min符号的常量折叠，造成结果不一致 pr: https://github.com/PaddlePaddle/Paddle/pull/63978

### 下周工作
1. 收尾generate shape的相关问题，与reduce_mean其它相关优化联调测试
2. 收尾inferSymbolicShape和inferMeta推导结果不一致的问题，使pr https://github.com/PaddlePaddle/Paddle/pull/63784 可以合入
3. 开始测试if\else分支在计算图中与在cuda kernel中的性能差异