### 姓名
陆琦

### 实习项目
新 IR API + 自动微分推全和核心组件完善

### 本周工作

1. **维护第三期的 PIR 迁移的任务**

    * 发布并第三期的 PIR API 迁移任务, 为开发者提供答疑和 pr review, 推进迁移任务进行：
        https://github.com/PaddlePaddle/Paddle/issues/58067
	
    * review PR, 本地复现并解决开发者问题：
        1. https://github.com/PaddlePaddle/Paddle/pull/58676
        2. https://github.com/PaddlePaddle/Paddle/pull/58882
        3. https://github.com/PaddlePaddle/Paddle/pull/58682
        4. https://github.com/PaddlePaddle/Paddle/pull/59042
        5. https://github.com/PaddlePaddle/Paddle/pull/58888
        6. https://github.com/PaddlePaddle/Paddle/pull/58877
        7. https://github.com/PaddlePaddle/Paddle/pull/58833
        8. https://github.com/PaddlePaddle/Paddle/pull/58935
        9. https://github.com/PaddlePaddle/Paddle/pull/58931
        10. https://github.com/PaddlePaddle/Paddle/pull/58740
        11. https://github.com/PaddlePaddle/Paddle/pull/58937
        12. https://github.com/PaddlePaddle/Paddle/pull/58929
        13. https://github.com/PaddlePaddle/Paddle/pull/58927
        14. https://github.com/PaddlePaddle/Paddle/pull/58696
        15. https://github.com/PaddlePaddle/Paddle/pull/58685
        16. https://github.com/PaddlePaddle/Paddle/pull/58690
        17. https://github.com/PaddlePaddle/Paddle/pull/58429
        18. https://github.com/PaddlePaddle/Paddle/pull/58883
        19. https://github.com/PaddlePaddle/Paddle/pull/58781


2. **推进 API PIR 下的推全验证工作**

   * 完成 pr :
        1. cosh: https://github.com/PaddlePaddle/Paddle/pull/58608
        2. group_norm: https://github.com/PaddlePaddle/Paddle/pull/58608
        3. logsumexp: https://github.com/PaddlePaddle/Paddle/pull/58843
        4. lgamma: https://github.com/PaddlePaddle/Paddle/pull/58840
        5. log1p: https://github.com/PaddlePaddle/Paddle/pull/58840

    * 正在推进 pr :
        1. nn.initializer.Uniform: https://github.com/PaddlePaddle/Paddle/pull/58642

3. **完善 PIR API 相关机制**
    1. 代码自动生成触发阶段由 make 编译阶段移至 cmake 构建阶段：https://github.com/PaddlePaddle/Paddle/pull/59129
    2. 为 OpResult 添加 id 属性，以支撑 check_numerics 在 pir 模式下运行：https://github.com/PaddlePaddle/Paddle/pull/59064
    3. 在 Executor 运行前，pop 出 program 中不存在的 feed variable ：https://github.com/PaddlePaddle/Paddle/pull/58984

4. **支持动静半架构升级工作**
    1. eager_properties.cc support auto parallel : https://github.com/PaddlePaddle/Paddle/pull/58746
    2. embedding_grad support AutoParallel : https://github.com/PaddlePaddle/Paddle/pull/58928


### 问题疑惑与解答

1. paddle/fluid/pir/dialect/operator/ir/ops.yaml 与 paddle/phi/api/yaml/ops.yaml 有什么区别？

    答：后者是静态图代码和动态图代码生成公用的 yaml 文件，但是 pir 下有些静态图 op 代码的生成不兼容动态图，所以需要额外写一个 yaml 配置文件。真正在 pir 代码生成时，会将前者和后者合并起来读入

2. 组合算子是什么含义？

    答：一个粒度大的算子可以按一定的规则拆分成更小粒度的算子，这个大粒度的算子就叫组合算子

### 下周工作

1. 与外部开发者协作沟通，管理任务发布, review PR, 答疑和 bug 修复 issue，推进 PIR API 的推全验证工作
2. 继续完善 PIR API 的迁移工作
3. 完成 code reading 笔记

### 导师点评
