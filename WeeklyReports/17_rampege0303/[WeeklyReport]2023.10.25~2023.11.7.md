### 姓名
罗震宇

### 实习项目
17-大模型复现

### 本周工作

1. **任务1：仿真环境搭建**
* **存在的问题：** 由于本地CUDA版本较高，在安装最新版paddlenlp时出现一系列问题，如：libssl.so.1.1: cannot open shared object file: No such file or directory等
* **解决方法：** 首先在Stack Overflow和Github上寻找了相似问题的解决方法，但是都无法有效解决我所遇到的问题。
* **解决结果：** 在和导师沟通后，选择降低paddlepaddle版本，并且只安装了CPU版本的相关库
* 主要库的版本信息如下：


        conda create -n mypaddle python=3.8
        python -m pip install paddlepaddle==2.5.2 -i https://pypi.tuna.tsinghua.edu.cn/simple
        pip install transformers[torch]
        pip install huggingface-hub==0.17
        pip install --upgrade paddlenlp
  
2. **任务2：权重转换**
* **分析示例模型：** 分析示例中bert-base-uncased模型的模型结构、参数及转换代码
1. 首先，该模型中有bert下共有199（5+12*8*2+2）个权重，分别为
- 其中5层embeding：
    - word_embeddings.weight [do not transpose]
    - position_embeddings.weight [do not transpose]
    - token_type_embeddings.weight [do not transpose]
    - embedding.LayerNorm.（gamma、beta）
- 25层LayerNorm （gamma、beta）
    - attention.output.LayerNorm=norm1
    - output.LayerNorm=norm2
- 24层attention.self.query (weight、bias)
- 24层attention.self.key
- 24层attention.self.value
- 24层attention. output.dense (weight、bias)
- 24层output.dense (weight、bias)= linear2
- 24层intermediate.dense (weight、bias)= linear1
- 8层cls：
    - 一层predictions.decoder
    - 两层predictions.transform.dense (weight、bias) = predictions.transform
    - 两层predictions.transform.LayerNorm (gamma、beta) = predictions.layer_norm

* **分析示例代码：** 分别对应代码中的


        hf_to_paddle = {
            "embeddings.LayerNorm": "embeddings.layer_norm",
            "encoder.layer": "encoder.layers",
            "attention.self.query": "self_attn.q_proj",
            "attention.self.key": "self_attn.k_proj",
            "attention.self.value": "self_attn.v_proj",
            "attention.output.dense": "self_attn.out_proj",
            "intermediate.dense": "linear1",
            "output.dense": "linear2",
            "attention.output.LayerNorm": "norm1",
            "output.LayerNorm": "norm2",
            "predictions.decoder.": "predictions.decoder_",
            "predictions.transform.dense": "predictions.transform",
            "predictions.transform.LayerNorm": "predictions.layer_norm",
        }
        do_not_transpose = []
        if version == "old":
            hf_to_paddle.update({
                "predictions.bias": "predictions.decoder_bias",
                ".gamma": ".weight",
                ".beta": ".bias",
        })
        do_not_transpose = do_not_transpose + ["predictions.decoder.weight"]
  ''' 
* **分析目标模型：** 一共339层：
- transformer.h.N.：
    - ln_1 (weight、bias)
    -     self.ln_1 = nn.LayerNorm(config.n_embd, epsilon=config.layer_norm_epsilon)
    -     self.ln_1 = nn.LayerNorm(config.n_embd, epsilon=config.layer_norm_epsilon)s
    - mlp.fc_out （weight、bias）[do no transpose]
    -     self.fc_out = nn.Linear(intermediate_size, embed_dim)
    -     self.fc_out = nn.Linear(intermediate_size, embed_dim)
    - mlp.fc_in （weight、bias）[do no transpose]
    -     self.fc_in = nn.Linear(embed_dim, intermediate_size)
    -     self.fc_in = nn.Linear(embed_dim, intermediate_size)
    - attn.out_proj （weight）
    - attn.k_proj （weight）
    - attn.v_proj （weight）
    - attn.q_proj （weight）
    -     self.out_proj = nn.Linear(self.embed_dim, self.embed_dim, bias=False)
    -     self.out_proj = nn.Linear(self.embed_dim, self.embed_dim, bias_attr=False)
    - attn.bias
    - attn.masked_bias
- 其他：
    - transformer.wte.weight
    - transformer.ln_f.weight
    - transformer.ln_f.bias
    - lm_head.weight
    - lm_head.bias
    -     self.lm_head = nn.Linear(config.n_embd, config.vocab_size)
* **分析目标代码：** 根据上述分析可得一下转换代码：

      dont_transpose = [
          "wte.weight",
        ]
      for k, v in pytorch_state_dict.items():
        transpose = False
        if k[-7:] == ".weight":
            if not any([w in k for w in dont_transpose]):
                if v.ndim == 2:
                    v = v.transpose(0, 1)
                    transpose = True

3. **问题疑惑与解答**
    1. pytorch版本中register_buffer中的参数persistent设置为False，导致离线模型参数与模型权重不匹配，查阅源码后执行以下更改
 '''
      gptJModel = model.transformer
      gptJBlock_list = gptJModel.h
      for gptJBlock in gptJBlock_list:
            attn = gptJBlock.attn
            tensor_bias = attn._buffers["bias"]
            attn.register_buffer("bias", tensor_bias)
            tensor_masked_bias = attn._buffers['masked_bias']
            attn.register_buffer("masked_bias", tensor_masked_bias)
 '''
     2. 在处理模型输入时，错把模型权重维度当成输入维度，导致缓存溢出，在尝试一系列缓存管理、多卡并行训练后仍未解决，和导师沟通后才找出问题并解决了

### 下周工作

1. 对gpt-j-6B模型依次进行权重转换、前向对齐、评价指标对齐、损失函数对齐
2. 完成数据集处理

### 导师点评

相比以前有进步，复现论文基本是多查API文档，多验证。
