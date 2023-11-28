### 姓名
陆琦

### 实习项目
新 IR API + 自动微分推全和核心组件完善

### 本周工作

1. **维护第三期的 PIR 迁移的任务**

    * 维护第三期的 PIR API 迁移任务, 为开发者提供答疑和 pr review, 推进迁移任务进行：
        https://github.com/PaddlePaddle/Paddle/issues/58067
	
    * review PR, 本地复现并解决开发者问题：

    * 为第三期 PIR API 迁移任务增添新的子任务


2. **推进 API PIR 下的推全验证工作**

   * 推进 pr :
        1. instance_norm: https://github.com/PaddlePaddle/Paddle/pull/59371
        2. nn.initializer.XavierInitializer, nn.initializer.MSRAInitializer：https://github.com/PaddlePaddle/Paddle/pull/59419
        3. fused_layer_norm and FusedDropoutAdd: https://github.com/PaddlePaddle/Paddle/pull/59420

    * 完成 pr :
        1. https://github.com/PaddlePaddle/Paddle/pull/58642

3. **完善 PIR API 相关机制**
    1. 代码自动生成触发阶段由 make 编译阶段移至 cmake 构建阶段, 补充 PR：https://github.com/PaddlePaddle/Paddle/pull/59222
    2. Fix bug: Operation pybind 绑定的 get_input_names 在无 OpYamlInterface 时 (比如 set_parameter op) 会段错误: 可以在pir.cc里那个get_input_names里完善一下，通过operation的HasInterface判断一下有没有OpYamlInterface，没有的话报一个 warning 返回空list

4. **迁移 PyLayer API 和 Op 至 PIR 体系下**
    1. 阅读源码中...

5. **支持动静半架构升级工作**
    1. expand_v2 spmd 规则推导: https://github.com/PaddlePaddle/Paddle/pull/59432


### 问题疑惑与解答



### 下周工作

1. 与外部开发者协作沟通，管理任务发布, review PR, 答疑和 bug 修复 issue，推进 PIR API 的推全验证工作
2. 继续完善 PIR API 的迁移工作
3. 编写 code reading 笔记 (ddl with 2023.12.13)
4. 推进迁移 PyLayer API 和 Op 至 PIR 体系下
5. 完成 expand_v2 spmd 规则推导 

### 导师点评
