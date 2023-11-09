### 姓名
陆琦

### 实习项目
新 IR API + 自动微分推全和核心组件完善

### 本周工作

1. **维护第三期的 PIR 迁移的任务**

    * 发布并第三期的 PIR API 迁移任务, 为开发者提供答疑和 pr review, 推进迁移任务进行：
        https://github.com/PaddlePaddle/Paddle/issues/58067
	
    * review PR, 并解决开发者问题, 总结共性问题至 「PIR 迁移任务的 bug 修复手册」：
        1. https://github.com/PaddlePaddle/Paddle/pull/58699
        2. https://github.com/PaddlePaddle/Paddle/pull/58699
        3. https://github.com/PaddlePaddle/Paddle/pull/58683
        4. https://github.com/PaddlePaddle/Paddle/pull/58675
        5. https://github.com/PaddlePaddle/Paddle/pull/58670
        6. https://github.com/PaddlePaddle/Paddle/pull/58634
        7. https://github.com/PaddlePaddle/Paddle/pull/58629
        8. https://github.com/PaddlePaddle/Paddle/pull/58605
        9. https://github.com/PaddlePaddle/Paddle/pull/58605
        10. https://github.com/PaddlePaddle/Paddle/pull/58604
        11. https://github.com/PaddlePaddle/Paddle/pull/58603
        12. https://github.com/PaddlePaddle/Paddle/pull/58596
        13. https://github.com/PaddlePaddle/Paddle/pull/58593
        14. https://github.com/PaddlePaddle/Paddle/pull/58546
        15. https://github.com/PaddlePaddle/Paddle/pull/58541
        16. https://github.com/PaddlePaddle/Paddle/pull/58491
        17. https://github.com/PaddlePaddle/Paddle/pull/58453
        18. https://github.com/PaddlePaddle/Paddle/pull/58394
    
    * 维护 PIR 迁移任务的 bug 修复手册：
        https://github.com/PaddlePaddle/Paddle/issues/58259


2. **推进 API PIR 下的推全验证工作**

   * 完成 pr :
        1. atan, atanh: https://github.com/PaddlePaddle/Paddle/pull/58473
        2. asin, asinh: https://github.com/PaddlePaddle/Paddle/pull/58470
        3. FusedMultiHeadAttention, FusedFeedForward: https://github.com/PaddlePaddle/Paddle/pull/58453
        4. acosh: https://github.com/PaddlePaddle/Paddle/pull/58450
        5. acos: https://github.com/PaddlePaddle/Paddle/pull/58317

    * 正在推进 pr :
        1. nn.initializer.Uniform: https://github.com/PaddlePaddle/Paddle/pull/58642
        2. cosh: https://github.com/PaddlePaddle/Paddle/pull/58608
        3. group_norm: https://github.com/PaddlePaddle/Paddle/pull/58608
        4. logsumexp: https://github.com/PaddlePaddle/Paddle/pull/58843
        5. lgamma: https://github.com/PaddlePaddle/Paddle/pull/58840
        6. log1p: https://github.com/PaddlePaddle/Paddle/pull/58840

3. **问题疑惑与解答**

	* \_legacy_C_ops.xxx 需不需要做 pir 的迁移？

        答：需要。以 `\_legacy_C_ops.fused_attention` 为例，其具有 `static_api_fused_attention`，但没有对应的 eager 函数，则需要修改 `paddle/fluid/pir/dialect/op_generator/ops_api_gen.py`，将 `fused_attention` 从 `NO_NEED_GEN_STATIC_ONLY_APIS` 移到 `NEED_GEN_STATIC_ONLY_APIS`，则在编译时，会在 `paddle/fluid/pybind/ops_api.cc` 里生成 C++ 端的接口 `static PyObject *fused_attention(PyObject *self, PyObject *args, PyObject *kwargs)`, 其仅具有 static 分支，并通过 \_C_ops 模块导出。需要注意的是，此时在 pir api 端不能使用 `in_dynamic_or_pir_mode()` 复用原有的 `_legacy_C_ops.fused_attention` 分支，需要单独用 `in_pir_mode()` 判断分支，添加刚刚生成的 `_C_ops.fused_attention`

    * `python/paddle/_pir_ops.py` 和 `python/paddle/_C_ops.py` 都导入 `paddle.base.libpaddle.pir.ops`，貌似重复了，两者有何不同？

        答：前者是旧版本的遗留问题，已经废弃。现在都用后者 


	*  pir 体系的 Block 与 Program 存在方法缺失, 如何解决？
        
        答：可以采用 monkey patch 的方法对 pir 体系下的 Block 和 Program 做方法补全。比如这个 PR https://github.com/PaddlePaddle/Paddle/pull/58660 , 补全了 Program 的 global_seed 方法

     * 为什么 `Attribute` 和 `OpInfo` 都会在 `IrContext` ，不独立拆开来写？

        答：...

     * 为何区分 OpOutlineResultImpl 和 OpInlineResultImpl ？即为啥 Value 里不直接存储一个 long 或 int ，表示 OpResult 的 index，还需要用 first_use_offseted_by_kind_  的低三位？

        答：...

     * `build/python/paddle/_C_ops.py`  导入了 eager 和 pir，`paddle.base.libpaddle.eager.ops` 和 `paddle.base.libpaddle.pir.ops` 有何不同？

        答：
        >
        > 1. 前者是 eager.cc 调用 eager_legacy_op_function.cc 的 BindEagerOpFunctions -> eager_op_function.cc 的 BindFinalStateEagerOpFunctions 绑定的，python method 对应的 cpp 接口为 `eager_api_xxx` (如 eager_api_abs)
        >
        > 2. 后者是 pir.cc 调用 BindOpsAPI，python method 对应的 cpp 接口为 xxx (如 `static PyObject *abs(PyObject *self, PyObject *args, PyObject *kwargs)`) 其在内部做 static 和 eager 的转发，如：
        >
        > ```c++
        > static PyObject *abs(PyObject *self, PyObject *args, PyObject *kwargs) {
        >       if (egr::Controller::Instance().GetCurrentTracer() == nullptr) {
        >       VLOG(6) << "Call static_api_abs";
        >       return static_api_abs(self, args, kwargs);
        >       } else {
        >       VLOG(6) << "Call eager_api_abs";
        >       return eager_api_abs(self, args, kwargs);		// <------------- 对应 1. 中的 eager 模式的 cpp 接口
        >       }
        >}
        > ```
        >
        >
        > 现在再来看 \_C_ops.py 里的操作：
        >
        > ```python
        > for name in dir(core.eager.ops):
        >     globals()[name] = getattr(core.eager.ops, name)
        >     __all__.append(name)
        > 
        > for name in dir(core.pir.ops):
        >     globals()[name] = getattr(core.pir.ops, name)	# <------------------- 把 eager 的接口覆盖掉，这样外部在调用 _C_ops.xxx 时会进入 pir 的 C++ 接口，及上面的 2.
        >     if name not in __all__:
        >         __all__.append(name)
        > 
        > ```

        \_legacy_C_ops 和 \_C_ops, 前者老动态图，后者新动态图。老动态图里有些代码和逻辑依然在用，所以保留了 \_legacy_C_ops 下来

	* paddle/phi/api/yaml/op_compat.yaml 的具体作用, 为什么在 op_compat.yaml 里存在如下用括号起来的 "别名":
        > \- op : bilinear (bilinear_tensor_product)
        
        在哪里完成了具体的算子映射?

        答：paddle 的静态图 op 定义简单分为两种体系，一种是旧体系，手动编写 OpMaker 等函数并调用 REGISTER_OPERATOR 手动注册；一种是新体系，使用 yaml 来定义。所以 op_compat.yaml 的主要功能是在代码自动生成时，完成参数名字映射和增加一些原始 ops.yaml 中没有的信息，确保生成的Op和原始手写的文件一致。具体来说 generate_op.py 的 add_compat_name::get_phi_and_fluid_op_name 完成了这种别名的映射


    * kernel_sig 的作用是什么？

        答：首先明确源码中的两种 kernel_signature:
        1. C++ class `KernelSignature`: 在静态图和旧动态图下，用于拿到 kernel 的输入，输出，属性信息，也就是所谓的签名，辅助 kernel 分发。查找对应的 kernel signature 的方法是：`paddle/phi/ops/compat/generated_static_sig.cc` 会注册诸如 `MatmulV2OpArgumentMapping` 的 mapping function，然后在需要的时候通过 `GetExpectedPhiKernelArgs` 查表找到对应的 mapping function，然后构造得到 `KernelSignature`
        
        2. 新动态图下的函数指针类型 `kernel_signature`: 在新动态图下，该函数指针类型是通过 api_gen.py 读取 ops.yaml 和 legacy_ops.yaml 自动生成的。比如 paddle/phi/api/lib/api.cc::matmul 函数里:

        ```c++
        using kernel_signature = void(*)(const phi::DeviceContext&, const phi::DenseTensor&, const phi::DenseTensor&, bool, bool, phi::DenseTensor*);
        ```
        该行代码指定的函数指针类型是 api_gen.py 读取里 legacy_ops.yaml 对应的 matmul 定义生成的

### 下周工作

1. 与外部开发者协作沟通，管理任务发布, review PR, 答疑和 bug 修复 issue，推进 API PIR 下的推全验证工作
2. 继续完善 API PIR 下的迁移工作
3. 阅读 PIR 源码

### 导师点评