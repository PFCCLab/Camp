### 姓名

黄济懿

### 实习项目

PIR 控制流专项

### 本周工作

1. **修复 PIR 控制流模型测试 BUG**

- https://github.com/PaddlePaddle/PaddleDetection/pull/8822
  - 第一个报错修复：增加 PaddleDetection 中 `prior_box` api 对 PIR 模式的支持
  - 遇到的第二个报错：下面的 if 控制流在转化为静态图后会出现 UndefinedVar 相关的报错，经讨论后目前无法支持
    ``` python
    # Compute regression loss.
    # Select positive samples.
    bbox_mask = paddle.tile(targets_label != bg_index, [1, 1, 4])
    if bbox_mask.astype(boxes.dtype).sum() > 0:
        location = paddle.masked_select(boxes, bbox_mask)
        targets_bbox = paddle.masked_select(targets_bbox, bbox_mask)
        loc_loss = F.smooth_l1_loss(location, targets_bbox, reduction='sum')
        loc_loss = loc_loss * self.loc_loss_weight
    else:
        loc_loss = paddle.zeros([1])
    ```
  - PR 提交后 CI 无法通过，后与负责 CI 的同学讨论确定不是该 PR 导致的，目前该 PR 等待 PaddleDetection 修复后可以合入

- https://github.com/PaddlePaddle/PaddleDetection/pull/8840
  - 修复在 PIR 模式下推理 `PPYOLOFPN` 时出现的 channel 为 -1 的报错
  - 通过 debug 问题定位到了 `paddle.expand` 算子在接收的 shape 参数包含 Value 时会出现返回 Value 的 shape 均为 -1 的情况
  - 该 PR 通过避免 expand 算子接收的 shape 参数包含 Value 解决了这个 BUG，后经过讨论近期已经有 PR 解决了 expand 算子返回 Value shape 异常的问题，故关闭该 PR

2. **将 pir::DenseTensorType 从 OperatorDialect 下沉到 BuiltinDialect**

- https://github.com/PaddlePaddle/Paddle/pull/62491
  - 将 `OperatorDialect` 下注册的 `DenseTensorType` 移动到 `BuiltinDialect`
  - 将 `DenseTensorType` 相关的 `ParseType` 和 `PrintType` 实现移动到 `BuiltinDialect`
  - 将 `pd_op.tensor` 的用法替换为 `builtin.tensor`

### 下周工作

1. PIR 控制流模型测试 BUG 修复
2. 其他 PIR 控制流相关工作
