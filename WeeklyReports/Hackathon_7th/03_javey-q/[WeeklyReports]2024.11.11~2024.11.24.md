### 姓名

仇嘉伟

### 实习项目

PaddleMiX 套件能力建设

### 本周工作

#### 1.  StableDiffusion3  Controlnet 完善

- 增加单测

test_controlnet_sd3.py  test_controlnet_inpaint_sd3.py

- 完成 paddle vs torch 精度对比

**相关指标（MAE）**

Controlnet Canny：

step 1:  0.00726168742403388

step 28: 0.004012377467006445

Controlnet Pose：

step 1:  0.01

问题定位：

```python
control_image = self.vae.encode(control_image).latent_dist.sample()
```

相关PR： https://github.com/PaddlePaddle/PaddleMIX/pull/829

#### 2. StableDiffusion3.5 适配

##### 相关代码：

transformer_sd3.py：SD3Transformer2DModel

attention.py：JointTransformerBlock

attention_processor.py： Attention，JointAttnProcessor2_5

normalization.py： SD35AdaLayerNormZeroX

##### 问题：

- SD3Transformer2DModel中 inference_optimize 分支 (TODO)
- Attention 中 qk_norm 

**当前进度：**

代码已完成适配，由于模型下载问题未进行测试。

#### 3. 论文阅读计划：StableDiffusion3

结合代码，对StableDiffusion3论文进行解读。（未完成）

### 导师点评

工作进展总体较好，能够围绕实习项目的核心任务展开，SD3 Controlnet相关PR已顺利合入，任务完成较为扎实，接下来需要进一步推进SD3.5适配合入和论文解读相关工作。
