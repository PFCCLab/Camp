### 姓名
陆琦

### 实习项目
新 IR API + 自动微分推全和核心组件完善

### 本周工作

1. **整理统计第三期的 PIR 待迁移的API**

    * 负责统计使用频次 < 40 次的待迁移 paddle API，目前已经完成初步统计，包括但不限于 activation.py, math.py, manupulation.py, logic.py, distribution.py 文件内的 API。对于 quant 层，sparse 算子，分布式算子，与 paddle 内部研发人员讨论后，决定放在以后的专项任务中去推全验证，第三期 PIR 迁移工作暂不迁移这部分 API
	
    * 正式发布第三期的 PIR API 迁移任务：
        https://github.com/PaddlePaddle/Paddle/issues/58067
    
    * 维护 PIR 迁移任务的 bug 修复手册：
        https://github.com/PaddlePaddle/Paddle/issues/58259


2. **推进 API PIR 下的推全验证工作**

	* 完成 pr:
        1. round: https://github.com/PaddlePaddle/Paddle/pull/58005
        2. sin: https://github.com/PaddlePaddle/Paddle/pull/58094
        3. cos: https://github.com/PaddlePaddle/Paddle/pull/58137
        4. dot: https://github.com/PaddlePaddle/Paddle/pull/57990 和 https://github.com/PaddlePaddle/Paddle/pull/58081
        5. floor: https://github.com/PaddlePaddle/Paddle/pull/58093
        6. nn.Sigmoid: https://github.com/PaddlePaddle/Paddle/pull/58144
        7. nn.LeakyReLU: https://github.com/PaddlePaddle/Paddle/pull/58340
        8. nn.MSELoss: https://github.com/PaddlePaddle/Paddle/pull/58352
        9. log10: https://github.com/PaddlePaddle/Paddle/pull/58363

3. **问题疑惑与解答**


	* 当前 pir 体系暂不兼容 `gradient_checker.double_grad_check` 和 静态图的 `base.backward.append_backward` 等与自动微分和梯度检查相关函数，需要在第三期任务中让开发者进行适配吗？

        答：不需要让外部开发者进行适配，该任务已在 paddle 内部进行排期推进。第三期任务开发者遇到自动微分推全的问题时可以在 PR 里记录 TODO

	* 在旧 IR 体系下 VarDesc 会有 Variable 作为 Python Class 进行封装。但 PIR 体系下 OpResult 目前缺失对应的 Python Class？

        答：该工作后续会有推进，复用当前 Variable 的全部接口

### 下周工作

1. 与外部开发者协作沟通，管理任务发布和 bug 修复 issue，推进 API PIR 下的推全验证工作
2. 继续完善 API PIR 下的迁移工作

### 导师点评
整体评价：推进有力，非常优秀！

后续建议：
1. 可以定期在微信群里向开发者更新「三期API」的进展，多正向鼓励和宣发任务
2. 思考确定自己的串讲议题，尽快发起技术分享日程
3. 可以负责迁移一批「三期API」，给开发者提供「样板间PR」的参考