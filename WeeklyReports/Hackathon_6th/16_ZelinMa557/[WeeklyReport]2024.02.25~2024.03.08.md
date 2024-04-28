### 姓名
马欣楷

### 实习项目
CINN 支持动态 Shape 专项（前端方向）

### 本周工作
本周主要工作如下：
1. 阅读cinn部分前端pass，理清前端执行流程
2. 将`lower_cinn_fusion_op_pass`中用到的`group`结构体重新抽出，替换成新的结构体，与其它用到`group`的部分解耦。由于这部分涉及文件较多，且相关文件改动较频繁，需要解决合并冲突，pr暂未合入  
相关pr:
- https://github.com/PaddlePaddle/Paddle/pull/62339



### 下周工作

1. 尽早将pr [62339](https://github.com/PaddlePaddle/Paddle/pull/62339) 合入
2. 尝试解决cinn某些单测[（complex symbol shape）](https://github.com/PaddlePaddle/Paddle/blob/develop/test/ir/pir/cinn/symbolic/test_complex_symbol_subgraph.py)无法通过的问题

### 导师点评
欣楷当前的工作以熟悉流程为主，CINN前端近期代码更新比较频繁，上手会有一些难度，目前进度基本符合预期。
