### 姓名
杨国浩

### 实习项目
子图验证&核心机制完善

### 本周工作

1. **修复动转静测试**
    * 修复新 IR 下遗留的 pd_op.fused_elemwise_add_activation 的相关问题。
    * 定位 test_len/test_slice/test_list 的问题，与 mentor 沟通关于 Lod Array Length 的相关问题。
    * 修复新 IR 下 test_len 中 len_with_selected_rows 测试， 主要是 ShapeSR 和 PhiRuntimeContext 中对 SelectedRows 数据类型的支持。
    * 修复 batch_norm_grad_grad 在新 IR 下的适配

2. **撰写算子修复任务的社区发布的相关内容并进行讨论**

### 下周工作

1. 完成 PyLayer Op 在新 IR 下的适配
2. 完成 Sequence_mask Op 在新 IR 下的适配
3. 定位剩余几个动转静测试的问题

### 导师点评
