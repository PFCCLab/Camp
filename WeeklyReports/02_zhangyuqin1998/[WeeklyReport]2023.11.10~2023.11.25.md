### 姓名
张钰钦

### 实习项目
新IR Pass建设

### 本周工作

1. **完成常量折叠评审**
整理基于执行器和基于kernel的常量折叠方案的文档，完成评审
https://github.com/yuanlehome/Hackathon/wiki/%E5%B8%B8%E9%87%8F%E6%8A%98%E5%8F%A0%E6%96%B9%E6%A1%88%E8%AF%84%E5%AE%A1


2. **重写常量折叠pass**
添加 constant tensor op
添加 tensor name attribute
添加相关UT并跑通
调整常量折叠的逻辑，当full op或full intarray op的use op含有IntArrayAttribute或ScalarAttribute时，full op或full intarray op的输出替换成constant tensor op
提交pr并完成了评审 https://github.com/PaddlePaddle/Paddle/pull/59244

### 下周工作
完善和验证常量折叠

### 导师点评
本周进展符合预期。常量折叠Pass属于逻辑复杂度比较高的组件，开发中会暴露出一些没有提前考虑到的问题，钰钦能够快速理解并做出调整，希望继续保持，这里积累的经验可以进行总结，放在后面的技术分享中。
