# 可视化静态图自动并行时序图工具使用手册

由于当下大模型的训练时间较长，分布式训练时序图的可视化对于调试和分析模型的训练过程非常重要。当下没有工具能够直接给出各个GPU设备上不同Job的运行区间，本可视化工具用来实现这个功能。

本工具使用分为两步，第一步为生成时序图数据，第二步为使用python脚本可视化时序图。

## 1. 生成时序图数据

本工具将可视化功能集成到了命令行参数中，以下以 PaddleNLP 中 LLama 训练脚本为例：

```bash
task_name="llama_7b_pp2_mp4_st"
rm -rf output/$task_name/
rm -rf "output/$task_name""_log"

export SOT_LOG_LEVEL=4
export PYTHONPATH=../../:$PYTHONPATH

export FLAGS_embedding_deterministic=1
export FLAGS_cudnn_deterministic=1

export CUDA_DEVICE_MAX_CONNECTIONS=1

python -u  -m paddle.distributed.launch \
     --gpus "0,1,2,3" \
     --log_dir "output/$task_name""_log" \
     run_pretrain_auto.py \
     --model_type "llama" \
     --model_name_or_path "meta-llama/Llama-2-7b" \
     --tokenizer_name_or_path "meta-llama/Llama-2-7b" \
     --input_dir "./data" \
     --output_dir "output/$task_name" \
     --split 949,50,1 \
     --max_seq_length 2048 \
     --per_device_train_batch_size 1 \
     --per_device_eval_batch_size 1 \
     --gradient_accumulation_steps 4 \
     --use_flash_attention 0 \
     --use_fused_rms_norm 0 \
     --fp16 0 \
     --fp16_opt_level "O2"  \
     --scale_loss 1024 \
     --pipeline_parallel_degree 4 \
     --tensor_parallel_degree 1 \
     --sharding_parallel_degree 1 \
     --sharding "stage1" \
     --learning_rate 0.0001 \
     --min_learning_rate 0.00001 \
     --max_steps 10 \
     --save_steps 5000 \
     --weight_decay 0.01 \
     --warmup_ratio 0.01 \
     --max_grad_norm 1.0 \
     --logging_steps 1\
     --dataloader_num_workers 1 \
     --sharding "" \
     --eval_steps 1000 \
     --report_to "visualdl" \
     --disable_tqdm true \
     --continue_training 0\
     --recompute 1 \
     --do_train \
     --do_eval 0 \
     --device "gpu" \
     --data_impl "mmap" \
     --parallel_mode "auto" \
     --job_schedule_profiler_start 0 \
     --job_schedule_profiler_end 5 \
```

其中 `--job_schedule_profiler_start 0` 和 `--job_schedule_profiler_end 5` 为控制可视化的时间区间。

在训练结束后，会在 `log_dir` 目录下生成每个设备的时序图数据，存储在 workerlog.0, workerlog.1, workerlog.2, workerlog.3 中。

## 2. 可视化时序图

在 Paddle 目录下有一个 `python/paddle/distributed/auto_parallel/static/profiler_helper_static.py` 脚本，用来可视化时序图。使用方法如下：

```bash
python python/paddle/distributed/auto_parallel/static/profiler_helper_static.py --devices 0,1,2,3 --log_dir /home/workspace/PaddleNLP/llm/llama/output/llama_7b_pp2_mp4_st_log
```

其中 `--devices` 为需要可视化的设备，`--log_dir` 为时序图数据所在的目录。

![picture 4](images/c9bbd2b9f69872e3f761841eaedf18a5f4d35488c78412e9651f666fdadec11e.png)  


脚本会生成 `Chrome tracing` 格式的文件，可以使用 Chrome 浏览器打开，也可以使用 [perfetto](https://ui.perfetto.dev/) 打开 `pipeline_profile_perfetto.json`。perfetto 提供了更好看的界面以及更流畅的体验，更推荐使用。

perfetto 可视化效果如下：

![picture 6](images/db4df88460aee707421616b99587554314637ddd0fc2541f1a4a6174aac4b29d.png)  


Chrome Tracing 可视化效果如下：

![picture 7](images/7524f138147dab43c170668eb555c767c8e2c65750fae6d7d22332d43abb39b2.png)  



## 3. 多机环境下的可视化

由于多机环境下，每个设备的时序图数据会分别存储在不同的机器上，因此需要将时序图数据收集到一台机器上，再进行可视化。请用户在每台机器上运行训练命令，然后将每台机器上的时序图数据按照如下方式放在一台机器上：

```
multi_machine_logs
├── machine0
│   ├── workerlog.0
│   └── workerlog.1
├── machine1
│   ├── workerlog.0
│   └── workerlog.1
```

然后在任意一台机器上运行可视化脚本并指定 `--log_dir` 参数为 `log_dir` 目录以及开启 `--multi_machine` 参数即可。

```bash
python python/paddle/distributed/auto_parallel/static/profiler_helper_static.py --devices 0,1 --log_dir /home/workspace/PaddleNLP/llm/llama/output/llama_7b_pp2_mp4_st_log/multi_machine_logs --multi_machine
```