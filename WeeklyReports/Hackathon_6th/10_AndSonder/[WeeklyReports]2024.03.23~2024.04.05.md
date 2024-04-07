### 姓名

卢畅

### 实习项目

静态图半自动并行训练性能优化

### 本周工作

本周主要任务是对 ZB H1 的编排结果进行测试以及设计 ZB VPP 的编排实现方案。

#### 对 ZB H1 进行性能测试并验证模型是否能正常收敛



Llama2 4卡实际调度结果如下：

![d378681e1c2a9cdb1d47f971c9836ea7](https://github.com/PaddlePaddle/Paddle/assets/55493212/5c9a9c52-6ea8-4c21-85fc-c02e7ca36f52)


在 PaddleNLP Llama2 模型上进行测试结果如下（pp4, batch 1, hidden_layer=4）：

**精度**

 精度可以对齐，有时候小数点后3位以后会有误查（符合论文的描述）

Llama2 下 10000 步 Loss 对比：

- ZBH1: 2.6
- 1F1B: 2.6

以下为前1000步，loss 曲线图

<img width="1144" alt="image" src="https://github.com/PaddlePaddle/Paddle/assets/55493212/61f24b15-4fea-4e6f-a852-9996a547019a">




**速度测试**

测试机器： 4卡 3090

| 调度方案 | interval_runtime | interval_samples_per_second | interval_steps_per_second |
| - | - | - | - |
| 1F1B | 3.17 | 5.1 | 0.3 |
| ZBH1 | 2.75 | 5.8 | 0.4 |


**显存占用**

| 调度方案 | 卡号 | max_memory_allocated | max_memory_reserved |
| - | - | - | - |
| 1F1B | 0 | 12605.69 MB | 13405.76 MB |
| 1F1B | 1 | 8809.68 MB | 9611.76 MB |
| 1F1B | 2 | 7013.66 MB | 7785.76 MB |
| 1F1B | 3 | 7806.72 MB | 8561.76 MB |
| ZBH1 | 0 | 12921.69 MB (↑ 316 )| 13831.76 MB (↑ 426 )|
| ZBH1 | 1 | 9639.7 MB (↑ 830 )| 10463.76 MB (↑ 852 )|
| ZBH1 | 2 | 8357.72 MB (↑ 1344 )| 9149.76 MB (↑ 1364 )|
| ZBH1 | 3 | 10597.38 MB (↑ 1790 )| 11219.76 MB (↑ 1658 )|


- 1F1B 总 max_memory_allocated: 36035.75 MB
- ZBH1 总 max_memory_allocated: 41516.49 MB
- 1F1B 总 max_memory_reserved: 35064.04 MB
- ZBH1 总 max_memory_reserved: 44650.04 MB


测试脚本如下：

```
set -x
unset CUDA_VISIBLE_DEVICES

task_name="llama_auto_static_dp2sharding2mp2pp2_vpp2"
# rm -rf output/$task_name/  # ckpt is saved in 'output/''
rm -rf "output/$task_name""_log"

# export PARALLEL_CROSS_ENTROPY=true
export FLAGS_call_stack_level=4
export PYTHONPATH=../../../:$PYTHONPATH
export GLOG_v=0

python -u -m paddle.distributed.launch \
    --gpus "0,1,2,3" \
    --log_dir "output/$task_name""_log" \
    run_pretrain_auto_static.py \
    --model_type "llama" \
    --model_name_or_path "facebook/llama-7b" \
    --tokenizer_name_or_path "facebook/llama-7b" \
    --input_dir "../data" \
    --output_dir "output/$task_name" \
    --split 949,50,1 \
    --max_seq_length 2048 \
    --per_device_train_batch_size 1 \
    --per_device_eval_batch_size 1 \
    --gradient_accumulation_steps 16 \
    --use_flash_attention 0 \
    --use_fused_rms_norm 0 \
    --fp16 0 \
    --fp16_opt_level "O2"  \
    --scale_loss 1024 \
    --pipeline_parallel_degree  4 \
    --tensor_parallel_degree 1 \
    --pipeline_schedule_mode "ZBH1" \
    --learning_rate 0.0001 \
    --min_learning_rate 0.00001 \
    --max_steps 20 \
    --save_steps 5000 \
    --weight_decay 0.01 \
    --warmup_ratio 0.01 \
    --max_grad_norm 1.0 \
    --logging_steps 1 \
    --dataloader_num_workers 1 \
    --eval_steps 1000 \
    --report_to "visualdl" \
    --disable_tqdm true \
    --continue_training 0 \
    --recompute 0 \
    --recompute_granularity full \
    --do_train \
    --do_eval \
    --device "gpu" \
    --data_impl "mmap" \
    --enable_auto_parallel 1 \
    --sharding_parallel_degree 1 \
    --sharding "stage1" \
```

相关 PR：

- https://github.com/PaddlePaddle/Paddle/pull/62865

#### 设计 ZB VPP 的编排实现方案

ZB VPP 是一种根据计算图自动调度任务的并行训练方案，反向计算分为两部分 b 和 w。w 可以用于填充计算图中的空洞，以此来降低 Bubble 率。ZB VPP 会把 Forward 和 Backward 拆分为多个 chunk，然后根据显存占用情况来进行任务调度。

想要实现自动调度任务，需要解决以下问题：

1. 如何将计算图分为两部分 b 和 w
2. 如何获得计算图的显存占用情况
3. 如何进行任务调度

详细设计文档：

- https://github.com/PFCCLab/Camp/pull/194

### 下周工作

1. 与导师讨论 ZB VPP 的设计方案是否合理
2. 初步实现 ZB VPP 的编排方案


### 导师点评