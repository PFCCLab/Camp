### 姓名

黄济懿

### 实习项目

PIR 控制流专项

### 本周工作

- 分析 PaddleDetection 中 ppyoloe_plus_crn_l_80e_coco 模型训练在 PIR 下出现的显存泄露问题并初步解决

#### 复现问题

- 复现脚本：

``` bash
cd /Paddle/build
# 完成 GPU 版本 Paddle 编译
pip install -U python/dist/paddlepaddle_gpu-0.0.0-cp310-cp310-linux_x86_64.whl --force-reinstall

cd /PaddleDetection
export FLAGS_set_to_1d=0;export CUDA_MODULE_LOADING=LAZY;export ENABLE_FALL_BACK=False
# export FLAGS_enable_pir_api=False;export FLAGS_enable_pir_with_pt_in_dy2st=0;FLAGS_enable_pir_in_executor=0  # Old IR
export FLAGS_enable_pir_api=True  # PIR

# export FLAGS_log_memory_stats=True
# export GLOG_vmodule=pir_interpreter=4
python tools/train.py -c configs/ppyoloe/ppyoloe_plus_crn_l_80e_coco.yml -o LearningRate.base_lr=0.0001 log_iter=1 use_gpu=True \
  save_dir=./test_tipc/output/ppyoloe_plus_crn_l_80e_coco/benchmark_train/to_static_train_gpus_0_autocast_fp32 epoch=1 \
  pretrain_weights=https://paddledet.bj.bcebos.com/models/ppyoloe_plus_crn_l_80e_coco.pdparams TrainReader.batch_size=4 \
  filename=ppyoloe_plus_crn_l_80e_coco TrainReader.shuffle=False --enable_ce=True --to_static > oom_log/out.log 2>&1
```

- 复现结果：随着训练过程显存占用不断增加，最后 Out of memory

``` bash
Epoch: [0] [   0/6250] mem_allocated: 1021 MB mem_reserved: 3496 MB
Epoch: [0] [   1/6250] mem_allocated: 1125 MB mem_reserved: 3496 MB
Epoch: [0] [   2/6250] mem_allocated: 1229 MB mem_reserved: 3496 MB
Epoch: [0] [   3/6250] mem_allocated: 1698 MB mem_reserved: 8608 MB
Epoch: [0] [   4/6250] mem_allocated: 1920 MB mem_reserved: 8608 MB
Epoch: [0] [   5/6250] mem_allocated: 2059 MB mem_reserved: 8608 MB
Epoch: [0] [   6/6250] mem_allocated: 2492 MB mem_reserved: 8822 MB
Epoch: [0] [   7/6250] mem_allocated: 2596 MB mem_reserved: 8822 MB
Epoch: [0] [   8/6250] mem_allocated: 2716 MB mem_reserved: 8822 MB
Epoch: [0] [   9/6250] mem_allocated: 2939 MB mem_reserved: 8822 MB
Epoch: [0] [  10/6250] mem_allocated: 3044 MB mem_reserved: 8822 MB
...
Epoch: [0] [  19/6250] mem_allocated: 5268 MB mem_reserved: 10415 MB
----------------------
Error Message Summary:
----------------------
ResourceExhaustedError: 

Out of memory error on GPU 0. Cannot allocate 27.000000MB memory on GPU 0, 10.906372GB memory has been allocated and available memory is only 4.062500MB.
```

- 旧 IR 模式下的训练结果对比：旧 IR 模式下并不存在该问题

``` bash
Epoch: [0] [   0/6250] mem_allocated: 825 MB mem_reserved: 3480 MB
Epoch: [0] [   1/6250] mem_allocated: 825 MB mem_reserved: 3480 MB
Epoch: [0] [   2/6250] mem_allocated: 825 MB mem_reserved: 3480 MB
Epoch: [0] [   3/6250] mem_allocated: 825 MB mem_reserved: 8517 MB
Epoch: [0] [   4/6250] mem_allocated: 825 MB mem_reserved: 8517 MB
Epoch: [0] [   5/6250] mem_allocated: 825 MB mem_reserved: 8517 MB
Epoch: [0] [   6/6250] mem_allocated: 825 MB mem_reserved: 8517 MB
Epoch: [0] [   7/6250] mem_allocated: 825 MB mem_reserved: 8517 MB
Epoch: [0] [   8/6250] mem_allocated: 825 MB mem_reserved: 8517 MB
Epoch: [0] [   9/6250] mem_allocated: 825 MB mem_reserved: 8517 MB
Epoch: [0] [  10/6250] mem_allocated: 825 MB mem_reserved: 8517 MB
```

经初步讨论：导致显存泄露问题的原因是存在变量没有被回收 (GC)，每次迭代都有新的变量没有被 GC 导致显存占用不断增加，最后引发 OOM

#### 验证已知问题是否解决

之前有大佬已经针对这个问题已经提了 2 个 PR：

- https://github.com/PaddlePaddle/Paddle/pull/63395
- https://github.com/PaddlePaddle/Paddle/pull/63408

但目前问题依旧存在，因此需要验证这 2 个 PR 是否达到预期目标

结果：经过 log 验证分析，这 2 个 PR 实现了预期的目标，因此在其他地方还存在没有被 GC 的变量

#### 问题分析过程

1. 逐个 OP 对比 PIR 和旧 IR 之间显存变化的区别

   由于整个 Program 的前反向共有 6000 个左右的 OP，并且由于 PIR 和旧 IR 的执行过程的区别导致显存变化很难对齐，通过逐个 OP 对比的方式没办法对问题进行定位

2. 不断削减模型组件分析是哪个组件引发的问题

   通过不断修改模型结构，最后发现是模型中的 if 控制流导致的显存泄露问题，当把模型中所有的 if 控制流都移除时，显存泄露的问题就消失了，但却不清楚为什么 if 控制流会导致显存泄露

3. 缩小问题规模分析问题

   由于原模型的 if 控制流比较复杂，涉及的变量较多，不方便分析，我通过将原模型的 if 控制流全部移除，然后通过修改模型代码增加了一个非常简单的 if 控制流：

   ``` bash
   (%578) = pd_op.if (%577) {} -> gpu_tensor<8x64x256x256xf32>{
   	(%579) = "multiply(phi_kernel)" (%576, %542) {kernel_key:<backend:GPU|layout:NCHW|dtype:float32>,kernel_name:"multiply",op_name:"pd_op.multiply",stop_gradient:[false]} : (gpu_tensor<8x64x256x256xf32>, gpu_tensor<1xf32>) -> gpu_tensor<8x64x256x256xf32>
   	() = "cf.yield" (%579) {} : (gpu_tensor<8x64x256x256xf32>) -> 
   } else {
   	() = "cf.yield" (%576) {} : (gpu_tensor<8x64x256x256xf32>) -> 
   }
   ```

   该控制流也能复现显存泄露的问题，通过对模型前反向各执行一次后的日志进行分析，发现了最终的问题所在：

   在执行 if_instruction 时，true 或 false 分支里的计算结果 (inner outputs) 会以共享内存的的方法拷贝给其他 Variable 作为 if_instruction 的输出 (if outputs)，但是这些 inner outputs 没有被 GC，而当 if outputs 被 GC 时，由于 inner outputs 也持有了相同的内存，最终导致这个内存没能正确回收。

   另外 ppyoloe_plus_crn_l_80e_coco 对于 Program 中的同一个 if 控制流，每次迭代执行时都会定义新的 inner outputs，导致随着训练没有被回收的显存越来越多，最后报了 OOM 的错误

#### 初步解决问题

- https://github.com/PaddlePaddle/Paddle/pull/64130

- 修复后 ppyoloe_plus_crn_l_80e_coco 在 PIR 下的训练过程：显存占用与旧 IR 保持一致

  ```bash
  Epoch: [0] [   0/6250] mem_allocated: 825 MB mem_reserved: 3497 MB
  Epoch: [0] [   1/6250] mem_allocated: 825 MB mem_reserved: 3497 MB
  Epoch: [0] [   2/6250] mem_allocated: 825 MB mem_reserved: 3497 MB
  Epoch: [0] [   3/6250] mem_allocated: 825 MB mem_reserved: 8529 MB
  Epoch: [0] [   4/6250] mem_allocated: 825 MB mem_reserved: 8529 MB
  Epoch: [0] [   5/6250] mem_allocated: 825 MB mem_reserved: 8529 MB
  Epoch: [0] [   6/6250] mem_allocated: 825 MB mem_reserved: 8529 MB
  Epoch: [0] [   7/6250] mem_allocated: 825 MB mem_reserved: 8529 MB
  Epoch: [0] [   8/6250] mem_allocated: 825 MB mem_reserved: 8529 MB
  Epoch: [0] [   9/6250] mem_allocated: 825 MB mem_reserved: 8529 MB
  Epoch: [0] [  10/6250] mem_allocated: 825 MB mem_reserved: 8529 MB
  ```


- 目前通过手动添加 inner outputs 的 GC 虽然能够解决问题，但是可能存在 inner outputs 后续需要被使用的风险，针对该问题，经讨论后认为应该为 yield op 实现一个 instruction，从而直接复用 pir_interpreter 的 GC 逻辑。

  因为当前 inner outputs 不被 GC 的原因是 yield op 的实际执行只是一个拷贝函数，而不是一个 instruction，因此 interpreter 在默认情况下会认为 inner outputs 是不被后续算子需要的，导致 inner outputs 在拷贝之前就被 GC 掉了，所以目前将 inner outputs 跳过了 GC，但是会引发内存泄露问题，而为 yield op 实现 instruction 后旧不用跳过 inner outputs 的 GC，直接服用 pir_interpreter 的 GC 逻辑就能解决目前的问题。

### 下周工作

- 为 yield op 实现 instruction

