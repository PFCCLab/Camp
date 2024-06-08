### 姓名
YibinLiu666

### 实习项目
高阶微分的性能分析和优化

### 本周工作
1. 收尾cumprod升级pr。
2. 定位到双向cumprod实现prod_grad的bug，静态图机制下cpu cumprod会自动使用inplace，原因未知。
3. 初步支持bmm的复数，complex64还有点问题

### 下周工作

1. 收尾双向cumprod实现prod_grad pr
2. 支持bmm复数类型

高效完成prod_grad并合入PR和bmm复数支持（windows 精度有问题待排查）
