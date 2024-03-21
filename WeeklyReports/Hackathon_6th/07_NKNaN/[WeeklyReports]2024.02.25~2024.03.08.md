### 姓名

李睿文

### 实习项目

框架 API 易用性提升

### 本周工作

1. **针对 `nn.functional.upsampling` 和 `nn.Upsample` 的功能增强**

- 新增功能需求：据输入维度自动切换默认的 `data_format` 功能，3-D 输入默认 "NCW", 4-D 输入默认 "NCHW", 5-D 输入默认 "NCDHW".

- 修改逻辑：`nn.functional.upsampling`, `nn.Upsample` 的底层实现都是通过 `nn.functional.interpolate`, 所以主要的修改是在 `nn.functional.interpolate` 中。当用户传入 `input` 后，若 `data_format` 是默认值 None，则进行条件判断，为 `data_format` 赋值。

- 提交 pr 并已合入：https://github.com/PaddlePaddle/Paddle/pull/61974

2. **尝试 `nn.functional.ctc_loss` 和 `nn.CTCLoss` 的功能增强**

- 新增功能需求：
     1. 增加 `use_softmax` 参数：torch 的 log_softmax+ctc_loss 相当于 paddle 的 ctc_loss, 所以希望 paddle 的 ctc_loss 输入可以直接是 log_softmax 的输出；用户通过 `use_softmax` 参数来指定是否对输入的 logits 做 softmax 处理。
     2. 增加 `zero_infinity` 参数：当某一个 batch 的 loss 计算结果为无穷时，将计算结果记为 0，且将对应 batch 的梯度值设为 0。

- 修改逻辑： `nn.functional.ctc_loss` 底层的计算逻辑在 `submodule` - `warpctc` 中。
     1. 增加 `use_softmax` 参数：若 `use_softmax == True`，延用原始逻辑；若  `use_softmax == False`，把原本对 input logits 做 softmax 处理的地方替换为对每一个元素取 exponential，（因为此时默认的输入是 logsoftmax 的输出，在此基础上取 exponential 后即可视为是 softmax 的输出）
     2. 增加 `zero_infinity` 参数：目前 `warpctc` 对输入的 `log_prob` 还做了截断处理（为保证 loss 的计算不会出现 infinity），所以需要先去掉截断处理，然后在每一个 batch 计算完 loss 之后做判断，若结果是 `-ctc_helper::neg_inf<ProbT>()` ，则将它和对应输入维度的梯度全部设为 0。

- 提交 pr 至 `warpctc`：https://github.com/baidu-research/warp-ctc/pull/180

3. **针对 `paddle.median` 的功能增强**

- 新增功能需求：
     1. 目前 `paddle.median` 在输入的待计算维度是偶数的情况下求中值的做法是排序后取中间两数的算术平均值，而 torch 则是取最小值，所以希望增加取最小值的功能。
     2. 希望在最小值时同时能够返回最小值对应的 `index`。

- 修改逻辑：增加 `mode` 参数，默认值为 "avg"，可取 "min"；`mode == avg` 保持原逻辑，`mode == min` 时参考 torch 的处理方式取最小值，计算对应的 `index` 并返回中值 tensor 和下标 tensor。

-  提交 pr：https://github.com/PaddlePaddle/Paddle/pull/62407

4. **针对 `paddle.nonzero` 的bug修复**

- bug描述：指定 `as_tuple = True` 时行为与 torch 不一致，假设N为非0个数，C为维度个数，将[N, C]作为tuple返回时，应返回C个[N]。但paddle返回C个[N, 1]，多了一维。

- 修改逻辑：在指定 `as_tuple = True` 时将目前的返回值 reshape([-1])

- 提交 pr：https://github.com/PaddlePaddle/Paddle/pull/62456

#### 问题疑惑与解答

     * submodule 不能直接修改，只有引用的原 repo 发生了更改才可以，能否 fork 引用的仓库然后将引用改为 fork 的仓库？

     答：目前的规范是避免使用私人仓库。

     * paddle.median 的返回值类型 如果 mode == 'min'，是否保持原始逻辑做 cast？
     
     答：mode == 'avg' 时暂时保持原逻辑；mode == 'min' 时不做 cast，输入和输出类型一致。

#### 备注——其他发现的问题

1. `paddle.nn.CrossEntropyLoss`: https://github.com/PaddlePaddle/Paddle/issues/62009

2. `paddle.nanmedian`: 若输入类型为 int 类型，输出在取平均时是按照整数除法，导致输出不是精确的平均值。

3. `paddle.nn.functional.interpolate`: 在 `mode = nearest` 时不支持 3-D tensor 而 torch 是支持的，其他 `mode` 下可能也有兼容的 tensor 维度和 torch 不一致的情况，需要进一步考察。

### 下周工作

1. 完善已提交的 pr
2. 继续修改其他框架 API

### 导师点评

李睿文修改了upsampling、ctc_loss、median、nonzero的API升级，但ctc_loss、nonzero的推进难度较大。在工作中需要注意，结合当前的问题点，分析其对应的工作量、风险等，要把握关键问题点，忽略其他无关问题，保持目标专注不要被无关细节困扰。同时工作前提前评估成本，先易后难的方式开展。对于不兼容升级，应考虑到其成本的倍增。
