### 姓名
陆琦

### 实习项目
新 IR API + 自动微分推全和核心组件完善

### 本周工作

1. xxx

2. xxx

3. **问题疑惑与解答**


	* \_legacy_C_ops.xxx 会调用到 C++ 端的哪个函数？以 `\_legacy_C_ops.fused_attention` 为例

        答：根据 `_legacy_C_ops.py` 文件可知： \_legacy_C_ops.xxx 会调用 `paddle.base.libpaddle.eager.ops.legacy ` 里的 C++ 接口 。这些 legacy 接口由 `BindEagerOpFunctions` 函数调用 `PyModule_AddFunctions(legacy.ptr(), ExtestMethods)` 绑定。即：
        \_legacy_C_ops.fused_attention  -> eager_legacy_api_fused_attention

        目前来看，现存的：

                1.  `eager_api_fused_attention`  : 实际上是 `sparse::eager_api_fused_attention` 对应 python 端的 sparse_fused_attention
                2.  `static_api_fused_attention` : 没有被绑定到 python 端，也没有被利用起来
        

	* \_legacy_C_ops.xxx 需不需要做 pir 的迁移？

        答：需要。以 `\_legacy_C_ops.fused_attention` 为例，其具有 `static_api_fused_attention`，但没有对应的 eager 函数，则需要修改 `paddle/fluid/pir/dialect/op_generator/ops_api_gen.py`，将 `fused_attention` 从 `NO_NEED_GEN_STATIC_ONLY_APIS` 移到 `NEED_GEN_STATIC_ONLY_APIS`，则在编译时，会在 `paddle/fluid/pybind/ops_api.cc` 里生成 C++ 端的接口 `static PyObject *fused_attention(PyObject *self, PyObject *args, PyObject *kwargs)`, 其仅具有 static 分支，并通过 \_C_ops 模块导出。需要注意的是，此时在 pir api 端不能使用 `in_dynamic_or_pir_mode()` 复用原有的 `\_legacy_C_ops.fused_attention` 分支，需要单独用 `in_pir_mode()` 判断分支，添加刚刚生成的 `\_C_ops.fused_attention`

        * `python/paddle/_pir_ops.py` 和 `python/paddle/_C_ops.py` 都导入 `paddle.base.libpaddle.pir.ops`，貌似重复了，两者有何不同？

        答：前者是旧版本的遗留问题，已经废弃。现在都用后者 

        * `python/paddle/_C_ops.py`  导入了 eager 和 pir，`paddle.base.libpaddle.eager.ops` 和 `paddle.base.libpaddle.pir.ops` 有何不同？
        
        答：
                1. 前者是 eager.cc 调用 eager_legacy_op_function.cc 的 BindEagerOpFunctions -> eager_op_function.cc 的 BindFinalStateEagerOpFunctions 绑定的，python method 对应的 cpp 接口为 `eager_api_xxx` (如 eager_api_abs)

                2. 后者是 pir.cc 调用 BindOpsAPI 绑定的，python method 对应的 cpp 接口为 xxx (如 `static PyObject *abs(PyObject *self, PyObject *args, PyObject *kwargs)`) 其在内部做 static 和 eager 的转发，如：
                
                   ```c++
                   static PyObject *abs(PyObject *self, PyObject *args, PyObject *kwargs) {
                     if (egr::Controller::Instance().GetCurrentTracer() == nullptr) {
                       VLOG(6) << "Call static_api_abs";
                       return static_api_abs(self, args, kwargs);
                     } else {
                       VLOG(6) << "Call eager_api_abs";
                       return eager_api_abs(self, args, kwargs);		// <------------- 对应 1. 中的 eager 模式的 cpp 接口
                     }
                   }
                   ```
                
                
                现在再来看 \_C_ops.py 里的操作：
                
                ```python
                for name in dir(core.eager.ops):
                    globals()[name] = getattr(core.eager.ops, name)
                    __all__.append(name)
                
                for name in dir(core.pir.ops):
                    globals()[name] = getattr(core.pir.ops, name)	# <--------------- 把 eager 的接口覆盖掉，这样外部在调用 _C_ops.xxx 时会进入 pir 的 C++ 接口，即上面的 2.
                    if name not in __all__:
                        __all__.append(name)
                
                ```




### 下周工作


### 导师点评