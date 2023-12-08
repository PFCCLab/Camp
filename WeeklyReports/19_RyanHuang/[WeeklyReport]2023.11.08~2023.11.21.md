### 姓名

黄子豪

### 实习项目

PIR 适配 AI 编译器 CINN

### 本周工作

将相关 API 迁移升级至 pir，并更新单测, 共24个

```
bmm / broadcast_tensors / histogram
lstsq / lu / lu_unpack
matrix_rank / mv / matrix_power / qr / multi_dot
is_empty / isfinite / isinf
PairwiseDistance / take_along_axis
unique_consecutive / moveaxis
roi_align / roi_pool
pinv / svd
diff / conj
```

pr链接

- https://github.com/PaddlePaddle/Paddle/pull/58833
- https://github.com/PaddlePaddle/Paddle/pull/58815
- https://github.com/PaddlePaddle/Paddle/pull/58740
- https://github.com/PaddlePaddle/Paddle/pull/58696
- https://github.com/PaddlePaddle/Paddle/pull/58689
- https://github.com/PaddlePaddle/Paddle/pull/58688
- https://github.com/PaddlePaddle/Paddle/pull/58685
- https://github.com/PaddlePaddle/Paddle/pull/58446
- https://github.com/PaddlePaddle/Paddle/pull/58676


### 下周工作

1. 新IR Python API适配升级收尾工作

- https://github.com/PaddlePaddle/Paddle/pull/58832
- https://github.com/PaddlePaddle/Paddle/pull/58708
- https://github.com/PaddlePaddle/Paddle/pull/58700
- https://github.com/PaddlePaddle/Paddle/pull/58678
- https://github.com/PaddlePaddle/Paddle/pull/58661


2. PIR 动转静理想态单测推全验证

- https://github.com/PaddlePaddle/Paddle/issues/58633


3. 继续进行 cinn 相关源码阅读


### 导师点评
整体：非常优秀！子豪本周参与了非常多的API迁移工作，自驱主动，迁移工作认真。

建议：下周可以将工作重心转移至动转静理想态推全验证上，从子图验证角度思考PIR的工作，并可以实时抛出自己的问题和思考。

