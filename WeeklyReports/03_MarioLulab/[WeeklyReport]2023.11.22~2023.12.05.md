### 姓名
陆琦

### 实习项目
新 IR API + 自动微分推全和核心组件完善

### 本周工作

1. **维护第三期的 PIR 迁移的任务**

    * 维护第三期的 PIR API 迁移任务, 为开发者提供答疑和 pr review, 推进迁移任务进行：
        https://github.com/PaddlePaddle/Paddle/issues/58067
	
    * review PR, 本地复现并解决开发者问题：
        1. https://github.com/PaddlePaddle/Paddle/pull/59313
        2. https://github.com/PaddlePaddle/Paddle/pull/59387
        3. https://github.com/PaddlePaddle/Paddle/pull/59459
        4. https://github.com/PaddlePaddle/Paddle/pull/59469
        5. https://github.com/PaddlePaddle/Paddle/pull/59481
        6. https://github.com/PaddlePaddle/Paddle/pull/59572

    * 为第三期 PIR API 迁移任务增添新的子任务，添加了 253-315 号任务，并更新 hackathon bot 的配置文件


2. **推进 API PIR 下的推全验证工作**

   * 推进 pr :
        1. fused_layer_norm and FusedDropoutAdd: https://github.com/PaddlePaddle/Paddle/pull/59420

    * 完成 pr :
        1. nn.initializer.Uniform：https://github.com/PaddlePaddle/Paddle/pull/58642
        2. nn.initializer.XavierInitializer, nn.initializer.MSRAInitializer：https://github.com/PaddlePaddle/Paddle/pull/59419
        3. instance_norm: https://github.com/PaddlePaddle/Paddle/pull/59371

3. **完善 PIR API 相关机制**
    1. 代码自动生成触发阶段由 make 编译阶段移至 cmake 构建阶段, 补充 PR：https://github.com/PaddlePaddle/Paddle/pull/59222
    2. Fix bug: Operation pybind 绑定的 get_input_names 在无 OpYamlInterface 时 (比如 set_parameter op) 会段错误: 可以在pir.cc里那个get_input_names里完善一下，通过operation的HasInterface判断一下有没有OpYamlInterface，没有的话报一个 warning 返回空list

4. **迁移 PyLayer API 和 Op 至 PIR 体系下**
    开发中

5. **支持动静半架构升级工作**
    1. expand_v2 spmd 规则推导: https://github.com/PaddlePaddle/Paddle/pull/59432


### 问题疑惑与解答

1. 当前 OpResult 是否支持设置 use_cudnn 属性
    答：暂不支持

2. pir 下 fetch 未初始化的变量，会报错，为什么？应该如何适配相关单测
    答：PIR fetch 的逻辑和老静态图有 diff，所以在 PIR 下 fetch 未初始化的 var 会报错。当单测出现该类问题时，先修改单测的 fetch list ，只把想要测试的结果 fetch 出来，暂时规避掉这个问题


### 下周工作

1. 与外部开发者协作沟通，管理任务发布, review PR, 答疑和 bug 修复 issue，推进 PIR API 的推全验证工作
2. 加速推进 PIR API 的迁移工作
3. 编写 code reading 笔记 (ddl with 2023.12.13)
4. 推进迁移 PyLayer API 和 Op 至 PIR 体系下
5. 完成 expand_v2 spmd 规则推导 

### 导师点评
整体：工作有序推进，深入问题细节，主动广泛参与框架各层的工作，非常出色！

建议：API推全的事情，我们计划在元旦节前后能进入「收尾状态」，期望任务认领率达到95%+、PR提交率达到95%+，合入率达到90%+，还有1个月左右时间。目前任务认领率为86.3%，PR 提交率80%，合入率64.76%。可以定期在微信群里同步关键进展，鼓励外部开发者。等到12月25日左右，我们可能要根据情况来内外协同，冲刺一波。
