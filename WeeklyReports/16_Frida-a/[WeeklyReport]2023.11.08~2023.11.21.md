## Weekly Report 11.08-11.21

### 实现源码推理

- 在aistudio环境中克隆项目源码并配置相关环境
- 下载并运行0.1.0-base，0.1.0-small两种权重

```jsx
(nougat) aistudio@jupyter-4213708-6934893:~/nougat$ nougat /home/aistudio/nougat/pdfs/MPCS55001_Aut23_hw7.pdf -o ./outputs/
downloading nougat checkpoint version 0.1.0-small to path /home/aistudio/.cache/torch/hub/nougat-0.1.0-small

(nougat) aistudio@jupyter-4213708-6934893:~$ nougat /home/aistudio/nougat/pdfs/MPCS55001_Aut23_hw7.pdf -c /home/aistudio/nougat/0.1.0-base/ -o ./outputs/
```

- 将.mmd格式输出转为.md格式
- 图片推理结果：
    - 使用一个3页pdf测试，内容为算法习题
    - base和small推理结果一致
    - 文字和公式基本正确（除了一处公式解译失败）
    
    ```jsx
    $O\big((V + E\big)\log V)$
    ```
    
    - 一处插入图片没有进行解译

        
    - 附原文件和结果文件

### 尝试模型结构对齐

- 网络结构代码转换：
    - backbone对应encoder，head对应decoder
    - 参考NRTR
    
    ```yaml
    Global:
      use_gpu: True
      epoch_num: 21
      log_smooth_window: 20
      print_batch_step: 10
      save_model_dir: ./output/rec/nougat/
      save_epoch_step: 1
      # evaluation is run every 2000 iterations
      eval_batch_step: [0, 2000]
      cal_metric_during_train: True
      pretrained_model: #TODO
      checkpoints:
      save_inference_dir:
      use_visualdl: False
      infer_img: 
      # for data or label process
      character_dict_path: ppocr/utils/EN_symbol_dict.txt
      max_text_length: 25
      infer_mode: False
      use_space_char: False
      save_res_path: ./output/rec/predicts_nougat.txt
    
    Optimizer:
      name: AdamW
      beta1: 0.9
      beta2: 0.99
      lr:
        name: LambdaLR #TODO
        learning_rate: 0.00005
        warmup_epoch: 2
      regularizer:
        name: 'L2'
        factor: 0.
    
    Architecture:
      model_type: rec
      algorithm: NOUGAT
      in_channels: 1
      Transform:
      Backbone:
        name: SwinEncoder
        cnn_num: 2
      Head:
        name: BARTDecoder
        
    Loss:
      name: #TODO
    
    PostProcess:
      name: #TODO
    
    Metric:
      name: #TODO
    
    Train:
      dataset:
      loader:
        
    Eval:
      dataset:
      loader:
    ```
    
- 后续工作：完成代码转换、权重转换、生成tensor验证模型正确性
- https://github.com/WenmuZhou/reprod_log

### 疑惑与解答

- 原仓库并未提供原始训练数据集，但提供了数据处理工具，需要进行数据集准备与迁移吗？可以准备自己的数据集做验证吗？
回答： 原仓库无训练数据，可以优先完成推理对齐（网络结构转换、权重转换），数据部分可以一起讨论如何准备~

### 导师点评
可以参考NRTR结构开始准备迁移了，注意代码结构的细节，遇到diff可以借助工具，或者逐层对齐。期待看到推理对齐的成果。
