### 姓名
马贺达

### 实习项目
CINN 静态 shape 下鲁棒性和性能优化

### 本周工作

1. **阅读 CINN 相关笔记、源码，并产出流程图**

	* 阅读留杰老师的 [CINN 阅读笔记](https://github.com/PaddlePaddle/community/tree/master/pfcc/paddle-code-reading/CINN) ， 熊昆老师的 《CINN Static Group Schedule 分享》 ，
和自己搜集的一些相关博客（如：[深度学习框架（三）：底层运行机制](https://zhuanlan.zhihu.com/p/435024770)），对 CINN 的基本结构有了初步了解
	* 阅读 cinn/frontend 与 cinn/hlir 源码，重点阅读 cinn/hlir/framework ，基本熟悉了CINN前端后端流程（CodeGen之前）
	* 产出相关内容的流程图

2. **复习 CUDA 基础知识**

	* 复习 CUDA ，主要依据 [paddle 的 CUDA 教程](https://github.com/PaddleJitLab/CUDATutorial) 与整理的资料

3. **尝试修复CINN的框架 bug**

	* 暂无进展。编译 CINN 时报错(https://github.com/PaddlePaddle/Paddle/issues/62546) ，正在寻找原因并解决

3. **问题疑惑与解答**

	* ISL 是什么？

        答：xxx

	* 《CINN Static Group Schedule 分享》中的链接没有权限访问？

        答：xxx
   
	* 这里注释有点小问题：[CINN/cinn/hlir/framework/op_lowering.h](https://github.com/PaddlePaddle/CINN/blob/develop/cinn/hlir/framework/op_lowering.h#L82)

        答：xxx

### 下周工作

1. 修复CINN的框架子图 bug 5-6个
2. 继续熟悉 CINN 源码，重点阅读 static group schedule 相关内容

### 导师点评
请联系导师填写