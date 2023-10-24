### 姓名

田川

### 实习项目

动转静问题验证

### 本周工作

1. **cityscapes 模型问题复现**

#### 分析问题

报错环境：

```bash
platform: Linux-5.10.0-1.0.0.26-x86_64-with-glibc2.31
Python: 3.11.3 (main, Apr  5 2023, 14:15:06) [GCC 9.4.0]
Paddle compiled with cuda: True
NVCC: Build cuda_12.0.r12.0/compiler.32267302_0
cudnn: 8.9
GPUs used: 1
CUDA_VISIBLE_DEVICES: 0,1
GPU: ['GPU 0: Tesla V100-SXM2-16GB', 'GPU 1: Tesla V100-SXM2-16GB']
GCC: gcc (GCC) 12.2.0
PaddleSeg: 0.0.0.dev0
PaddlePaddle: 0.0.0
OpenCV: 4.5.5
```

错误信息:

```bash
---------------- PaddleSOT graph info ----------------
Traceback (most recent call last):
  File "/workspace/PaddleSeg/tools/train.py", line 207, in <module>
    main(args)
  File "/workspace/PaddleSeg/tools/train.py", line 182, in main
    train(
  File "/workspace/PaddleSeg/paddleseg/core/train.py", line 238, in train
    loss_list = loss_computation(
                ^^^^^^^^^^^^^^^^^
  File "/workspace/PaddleSeg/paddleseg/core/train.py", line 50, in loss_computation
    mixed_loss_list = loss_i(logits, labels)
                      ^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/paddle/nn/layer/layers.py", line 1343, in __call__
    return self.forward(*inputs, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/PaddleSeg/paddleseg/models/losses/mixed_loss.py", line 55, in forward
    output = loss(logits, labels)
             ^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/paddle/nn/layer/layers.py", line 1343, in __call__
    return self.forward(*inputs, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/PaddleSeg/paddleseg/models/losses/rmi_loss.py", line 82, in forward
    loss = self.forward_sigmoid(logits_4D, labels_4D, do_rmi=do_rmi)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/PaddleSeg/paddleseg/models/losses/rmi_loss.py", line 113, in forward_sigmoid
    rmi_loss = self.rmi_lower_bound(valid_onehot_labels_4D, probs_4D)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/PaddleSeg/paddleseg/models/losses/rmi_loss.py", line 191, in rmi_lower_bound
    pr_cov_inv = self.inverse(pr_cov + paddle.cast(
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/PaddleSeg/paddleseg/models/losses/rmi_loss.py", line 118, in inverse
    return paddle.inverse(x)
           ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/paddle/tensor/math.py", line 2670, in inverse
    return _C_ops.inverse(x)
           ^^^^^^^^^^^^^^^^^
RuntimeError: (PreconditionNotMet) For batch [0]: U(2, 2) is zero, singular U. Please check the matrix value and change it to a non-singular matrix
  [Hint: Expected info[i] == 0, but received info[i]:2 != 0:0.] (at ../paddle/phi/kernels/funcs/matrix_inverse.cu:117)

```


#### 验证步骤:

* 准备复现环境

```bash
platform: Linux-5.15.0-72-generic-x86_64-with-glibc2.27
Python: 3.11.2 (main, Feb  8 2023, 14:49:29) [GCC 7.5.0]
Paddle compiled with cuda: True
NVCC: Build cuda_11.8.r11.8/compiler.31833905_0
cudnn: 8.6
GPUs used: 1
CUDA_VISIBLE_DEVICES: None
GPU: ['GPU 0: Tesla V100-SXM2-16GB']
GCC: gcc (GCC) 8.2.0
PaddleSeg: 0.0.0.dev0
PaddlePaddle: 0.0.0
OpenCV: 4.5.5
```

* 准备数据集

[aistudio](https://aistudio.baidu.com/datasetdetail/48855)

[CityScapes官网](https://www.cityscapes-dataset.com/)

* 配置目录

```
PaddleSeg
├── data
│   ├── cityscapes
│   │   ├── leftImg8bit
│   │   │   ├── train
│   │   │   ├── val
│   │   ├── gtFine
│   │   │   ├── train
│   │   │   ├── val
```

* 尝试复现

```bash
export STRICT_MODE=0
export COST_MODEL=False
export MIN_GRAPH_SIZE=0
export SOT_LOG_LEVEL=3
export ENABLE_FALL_BACK=True

python3.11 tools/train.py \
    --config configs/deeplabv3p/deeplabv3p_resnet50_os8_cityscapes_1024x512_80k_rmiloss.yml \
    --iters 10 \
    --save_interval 100 \
    --batch_size 1 \
    --num_workers 4 \
    --save_dir output/deeplabv3p_resnet50_os8_cityscapes_1024x512_80k_rmiloss \
    --opts to_static_training=true
```

* 总结

复现失败, 暂时归类为 cuda12 问题 (手里没 cuda12 环境可以复现).

查看报错源码, 为自定义 eq: 
```c++
    PADDLE_ENFORCE_EQ(info[i],
                      0,
                      phi::errors::PreconditionNotMet(
                          "For batch [%d]: U(%d, %d) is zero, singular U. "
                          "Please check the matrix value and change it to a "
                          "non-singular matrix",
                          i,
                          info[i],
                          info[i]));
```


### 下周工作

1. 动转静单测机制推全

### 导师点评


请联系导师填写

