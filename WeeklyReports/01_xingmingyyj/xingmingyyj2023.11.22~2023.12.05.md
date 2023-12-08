### 姓名
朱新明
### 实习项目
算子规范和ProgramTranslator功能优化
### 本周工作
#### 1.将算子单测修复issue发布社区
将算子单测修复issue发布社区，并认领任务
#### 2.修复 test_decayed_adagrad_op 单测
该单测是因为算子`decayed_adagrad`未注册导致的，注册后成功修复，PR已合入。
#### 3.修复 test_fake_quantize_op
该单测涉及多个op，目前已经注册`fake_channel_wise_quantize_abs_max`,`fake_channel_wise_quantize_dequantize_abs_max`,`fake_quantize_abs_max`,`fake_quantize_dequantize_abs_max`,`fake_quantize_moving_average_abs_max`,`fake_quantize_range_abs_max`,`quantize_linear`等多个Op.主要遇到问题如下：
1. moving_rate can not found in AttributeMap
已经在新Ir下的算子定义中额外补充moving_rate
2. tensor holder_ is null
具体报错位置还在定位
3. 翻译op fetch_v2时找不到输入[x]
具体原因还在定位
#### 4.修复 test_matrix_rank_op
已定位问题，原因该是op根据`ctx`中是否存在`TolTensor`选择`kernel`，还未修复。
#### 5.修复 test_sgd_op_bf16
已定位问题，该op的情况和`test_unique`类似，参考PR59124适配`GetSgdExpectedKernelType`，还未修复。
#### 6.修复 test_tdm_sampler_op
本地注册`tdm_sampler`之后，单测执行成功，但是PR CI-Coverage覆盖率未通过，目前确定是FLAG设定存在问题。
#### 7.修复 test_activation_op
注册`soft_relu`后，执行成功，PR已合入
#### 8.修复 test_shuffle_batch_op
注册`shuffle_batch`后本地执行成功，PR遇到了和test_tdm_sampler_op一样的问题
#### 9.修复 test_row_conv_op 
注册`row_conv`后执行成功，已提交PR
#### 10.修复 test_tril_triu_op
注册`tril_triu`后执行成功，已提交PR

### 下周工作
#### 1.根据推全名单继续修复Op单测
#### 2.修复分布式算子c_softmax_with_cross_entropy相关单测
#### 3.统计需要修复的分布式算子单测并区分修复难度
### 导师点评
新明本周积极推进算子推全工作，认真负责，对于发现的问题能认真展开分析，确认问题原因，希望继续保持这种积极的态度，期待未来取得更多成果。
