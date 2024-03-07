### 姓名

Github ID: [yulangz](https://github.com/yulangz)

### 实习项目

CINN子图鲁棒性和性能优化

### 本周工作

1. **大模型子图导出**

    CINN 编译器用于将动态图转为静态图，对提升 Paddle 性能表现具有重要作用。为了确保 CINN 的鲁棒性，需要对目标大模型进行子图导出，摸底模型结构，生成 CINN 测试，主要进行以下几方面工作：

    1. 走通大模型动转静以及 SOT 子图导出流程
    2. 导出 QWen 子图，并对照子图与原模型结构
    3. 导出 Stable Diffusion 子图，并对照子图与原模型结构

    PR:
    - [https://github.com/PaddlePaddle/Paddle/pull/62382](https://github.com/PaddlePaddle/Paddle/pull/62382)
    - [https://github.com/PaddlePaddle/Paddle/pull/62405](https://github.com/PaddlePaddle/Paddle/pull/62405)

### 下周工作

1. 继续大模型子图导出
2. 熟悉 CINN 的设计与实现

### 导师评语
海涛在本周协助开展 ”大模型子图抽取“ 任务，独立完成了Stable Diffusion、Qwen 两个大模型的子图导出工作，并且已经提了两个PR，做的很好