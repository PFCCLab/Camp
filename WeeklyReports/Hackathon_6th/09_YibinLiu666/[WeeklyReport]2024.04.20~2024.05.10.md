### 姓名
YibinLiu666

### 实习项目
高阶微分的性能分析和优化

### 本周工作
1. 升级cumprod的功能，支持reverse与exclusive两个参数 https://github.com/PaddlePaddle/Paddle/pull/64022
2. 使用双向cumprod修复 prod_grad 在x有0的时候x_grad出现nan的bug，https://github.com/PaddlePaddle/Paddle/pull/64127

### 下周工作

1. 收尾cumprod升级pr。
2. 修复双向cumprod实现prod_grad的bug
3. 然后支持bmm复数complex类型

### 导师点评
提PR的时候描述可以更完善一些，比如一个问题修复PR，可以按照问题背景、解决方案（简要描述）、最终效果（小的demo代码）。这样review的人能比较直观看到PR的改动目的。
