### 姓名

田川

### 实习项目

动转静 SOT 模块 Python 3.12 支持，PIR 0 维单测适配

### 本周工作

#### **动转静 SOT 模块 Python 3.12 支持总结**

Python 3.12 的更新相较于 Python 3.11 的更新更像是内部优化的一版。

##### SOT 所做的工作

* Eval Frame 适配 3.12

  Eval Frame 作为 SOT 的一个主要入口，我们所生成的新的字节码都会通过 Eval Frame 执行。
  这里需要注意，在适配 3.12 中，`eval_custom_code`不再使用自己手动管理的`shadow`也就是生成的代码 [Fix that frame](https://github.com/PaddlePaddle/Paddle/pull/61703)

* Paddle Jit 适配

  之前因为 3.12 尚未支持 SOT 模式，因此默认情况会 fallback 回 SOT 模式。所以我们在 [[SOT][3.12] Don't fallback to AST mode in 3.12](https://github.com/PaddlePaddle/Paddle/pull/61414) 对 Jit 做了适配。

* CI 打开 3.12 的单测

  需要在不影响现有版本的情况下，增量测试 3.12 的单测。但是目前 3.12 的单测并没有完全支持，所以只能根据文件来进行跳过部分单测。于是就有了现在的 SOT 专属的[单测跳过机制](https://github.com/PaddlePaddle/Paddle/pull/61296): 在 `test/sot` 文件夹下可以通过新建`skip_files_py312` 并在列表中添加文件名进行跳过单测。在适配后进行逐个删除。

* 字节码适配

  官网链接: [What’s New In 3.12](https://docs.python.org/3.12/whatsnew/3.12.html#cpython-bytecode-changes)

  这部分大多是 3.12 删除或者合并的一些字节码，比如 `PRECALL`、`PRECALL__CALL`、`CALL` 统一成 `CALL`。更多详细修改可以查看 [SOT Python3.12 支持任务汇总](https://github.com/PaddlePaddle/Paddle/issues/61173)

  没有写在 Release Note 中的内容:

  3.12 最主要的变动是 Cpython 字节码生成解释器，可以查看：[Python/Cpython/issues/98831](https://github.com/python/cpython/issues/98831) 看到更多内容。

  大致就是 Cpython 定义了自己的 [DSL](https://github.com/faster-cpython/ideas/blob/main/3.12/interpreter_definition.md?rgh-link-date=2024-01-25T08%3A16%3A02Z) 完成了 ceval 的重写，用于实现 3.13 的 [Tier 2 优化器](https://github.com/faster-cpython/ideas/blob/main/3.13/engine.md) 。

* 特化指令适配

  [3.12 中的特化指令适配](https://github.com/PaddlePaddle/Paddle/pull/61305/files#diff-f9342525796497ca5dc0bd20bc9d0d5e3a4498c87d2f1a680af74d09b91bdfa5)。 这里同 Python 3.11 一致，只是指令和大小有所不同，可以查看[大佬的博客](https://nyakku.moe/posts/2023/08/27/python311-instruction-specializing.html#%E6%8C%87%E4%BB%A4%E7%89%B9%E5%8C%96)。

* FOR、IF 适配

  这两部分比较特别，SOT 的 FOR 和 IF 这两个指令，并不会按照原有 Cpython 的逻辑进行跳转，而是会生成一些新的指令重新构建一个 FOR 或者 IF。(在 3.12 中 FOR 多了一个 `END_FOR` 指令，所以需要对其生成新的字节码进行适当的重定位)，老的 FOR 逻辑可以查看: [debug END_FOR #62261](https://github.com/PaddlePaddle/Paddle/pull/62261) 对 `_break_graph_when_for_loop` 函数的注释，可能会有些偏差，以 [#62155](https://github.com/PaddlePaddle/Paddle/pull/62155) 合入的为准。

* Debug Python 版本修复
 
  在开发的过程中可以更多的使用 Debug 版本的 Python 可以提前显现出一些隐性的 BUG。因为 debug 版本的 Python 会在运行时进行一些额外的检查，比如内存分配的边界检查等(并不是所有的问题都需要修复)。虽然用户大概率不会使用 debug 版 Python，但这些问题都是隐患，越早消除越好（不然模型上报出问题就更难调试了）。例如：[#62470](https://github.com/PaddlePaddle/Paddle/pull/62470) 和 [#62424](https://github.com/PaddlePaddle/Paddle/pull/62424) 都是在 debug 版本下发现的 BUG。更多任务信息可以查看：[#61174](https://github.com/PaddlePaddle/Paddle/issues/61174#issuecomment-1978136598)

上述编写顺序也是，推荐的开发流程顺序(仅适用于没啥重大修改的Python版本)，在`Eval Frame`适配并打开相关单测后，优先适配出现概率高的字节码，有助于推进后续任务并行。

##### 总结和思考

* 任务推进方面
  在任务的分配上还是缺乏经验，没能考虑到难易程度，也没有预先查看错误分布。这就导致有部分单测开放不及时，这样的后果就是不同开发者之间适配的部分会冲突，但还好本次参与的人不多，且适配速度较快基本无影响。

* 技术积累方面
  通过学习 Cpython 的源码，查看源码、相关改动 issue 学习背后的原因。可以预见的是 3.13 版本的适配难度将会是前几个版本的总和。 需要补充学习的知识: 编译器原理，VM, Jit 相关知识。

#### **PIR 0 维单测适配**

##### 遇到的一些小问题

* 不应该在`setUp`中加载任何数据，因为在这时还没确定是哪种 IR 模式运行。[#62808](https://github.com/PaddlePaddle/Paddle/pull/62808)
* 尽可能地拆分为更小的单元测试，一是不容易 ci 超时，而是方便上 ci 定位问题。
* 不能在静态图组网期去使用 Value 的 `__bool__`、`__len__`、`__float__`魔法方法，因为这些 Value 的「值」在组网时是不能确定的，但这些方法都会求值，只适合 eager 求值的动态图。[#62794](https://github.com/PaddlePaddle/Paddle/pull/62794)

### 下周工作

1. PIR 0 维单测适配

### 导师点评

不愧是川子，除去 3.12 的适配内容，之后有时间也可以稍微调研下 cpython 社区 3.13 现有的工作进展，看看未来 3.13 适配会有什么可预见的问题

0D Tensor 适配剩余问题可能都是些疑难问题，加油 up!(˘•ω•˘)ง

LGTMeow <img src="https://www.gstatic.com/android/keyboard/emojikitchen/20231113/u1f947/u1f947_u1f43e.png" width="14" alt="🐾"/>