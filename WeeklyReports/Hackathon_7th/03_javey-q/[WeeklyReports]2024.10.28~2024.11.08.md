### 姓名

仇嘉伟

### 实习项目

PaddleMiX 套件能力建设

### 本周工作

##### 1. ppdiffusers  支持 StableDiffusion3  Controlnet, 完成推理流程初步搭建

- controlnet_sd3模型实现， 结构参照transformer_sd3;
- transformer_sd3 模型修改，添加controlnet residual;
- stable_diffusion_3_controlnet  pipeline实现;
- stable_diffusion_3_controlnet_inpainting  pipeline实现.

相关PR：https://github.com/PaddlePaddle/PaddleMIX/pull/789

##### 2. StableDiffusion3  Controlnet 完善

- 增加推理：ppdiffusers/examples/inference/text_to_image_generation-stable_diffusion_3_controlnet.py;
- 增加Dummy Classes：ppdiffusers/ppdiffusers/utils/dummy_paddle_and_paddlenlp_objects.py;

- 调研  StableDiffusion3.5 。

##### 3. 实习收获

本周主要学到了一些torch2paddle 转换时一些要注意的点

- 算子名称差异, 如 cat -> concat, to->cast
- 算子参数名称差异, 如 axis->dim
- 类名称差异:  如Modoulelist -> LayerList
- 数据类型差异:  paddle中只有paddle.Tensor
- 其他: paddle 没有 device

### 下周工作

1. 对 StableDiffusion3  Controlnet 进行精度验证;
2. 增加单测。

### 导师点评
工作进展清晰且高效，学习态度良好。
