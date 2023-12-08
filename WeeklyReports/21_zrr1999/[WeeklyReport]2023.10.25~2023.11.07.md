### 姓名

詹荣瑞

Github ID：[zrr1999](https://github.com/zrr1999)

### 实习项目

PIR 核心组件建设与机制完善

### 本周工作

1. **迁移部分算子到 PIR**
    - expand/broadcast_to(1/2): 
    - solve(20/20)
    - diag(4/4)
    - linspace(4/4)
    - std(2/2)
    - slogdet/det(6/6)
    - index_add(5/5)
    - inverse(7/7)：

相关PR：
- https://github.com/PaddlePaddle/Paddle/pull/58384

### 下周工作

1. 迁移 print 算子到 PIR。
2. 补全开启 index_put 的单测。
3. 迁移 index_select、index_sample、multiplex、floor_mod、renorm、repeat_interleave、rad2deg 算子到 PIR 。

### 导师点评
荣瑞本周持续参数pir api迁移工作，下周会参与到pir机制修复补全的工作，再接再厉~
