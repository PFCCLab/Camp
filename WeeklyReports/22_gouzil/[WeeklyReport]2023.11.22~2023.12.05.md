### 姓名

田川

### 实习项目

PIR 动转静组件建设与单测验证推全

### 本周工作

1. PIR 动转静组件单测问题摸底收尾

接下来几周主要做问题修复部分

相关pr: 

* [#59120](https://github.com/PaddlePaddle/Paddle/pull/59120)
* [#59232](https://github.com/PaddlePaddle/Paddle/pull/59232)
* [#59276](https://github.com/PaddlePaddle/Paddle/pull/59276)
* [#59314](https://github.com/PaddlePaddle/Paddle/pull/59314)
* [#59378](https://github.com/PaddlePaddle/Paddle/pull/59378)
* [#59517](https://github.com/PaddlePaddle/Paddle/pull/59517)
* [#59546](https://github.com/PaddlePaddle/Paddle/pull/59546)
* [#59569](https://github.com/PaddlePaddle/Paddle/pull/59569)

遇到的一些问题:

* `cuda api` 切换不生效

在 [#59300](https://github.com/PaddlePaddle/Paddle/pull/59300) 下适配了 `OpResult.cpu()` 和 `OpResult.cuda()` 方法 (补充说明: 在[#59565](https://github.com/PaddlePaddle/Paddle/pull/59565) pr 中已统一为 `Value`)

但是再 `test_tensor_memcpy_on_cpu` 单测中发现无法从 cpu 切换为 cuda, 下面是精简后的复现单测

```python
def tensor_copy_to_cuda(x):
    x = paddle.to_tensor(x)
    y = x.cuda()
    return y

class TestTensorCopyToCUDAOnDefaultCPU(Dy2StTestBase):
    def _run(self, to_static):
        x1 = paddle.ones([1, 2, 3])
        x2 = paddle.jit.to_static(tensor_copy_to_cuda)(x1)
        return x1.place, x2.place

    @test_pir_only
    @test_sot_only
    def test_tensor_cuda_on_default_cpu(self):
        if not paddle.is_compiled_with_cuda():
            return

        paddle.framework._set_expected_place(paddle.CPUPlace())
        static_x1_place, static_place = self._run()
        self.assertTrue(static_x1_place.is_cpu_place())
        self.assertTrue(static_place.is_gpu_place())
```

分析 GLOG:
```bash
pir_interpreter.cc:1259 New Executor is Running ...
interpreter_util.cc:1262 -----------------------------
interpreter_util.cc:1264  (%0) = "data(phi_kernel)" () {dtype:(pd_op.DataType)float32,kernel_key:<backend:Undefined|layout:Undefined(AnyLayout)|dtype:float32>,kernel_name:"data",name:"_jst.0.args.0",op_name:"pd_op.data",place:(pd_op.Place)Place(undefined:0),shape:(pd_op.IntArray)[1,2,3],stop_gradient:[true]} : () -> undefined_tensor<1x2x3xf32>
ir_context.cc:117 Found a cached OpInfo of: [name=pd_op.data, OpInfo: ptr=0x47f2100].
ir_context.cc:117 Found a cached OpInfo of: [name=pd_op.data, OpInfo: ptr=0x47f2100].
interpreter_util.cc:1370 Value   : (   [0x81e4bf0]) = pd_op.data()
interpreter_util.cc:1371 Variable: (out[0x81e4e00]) = pd_op.data()
interpreter_util.cc:1262 -----------------------------
interpreter_util.cc:1264  (%0) = "memcpy(phi_kernel)" (%1) {dst_place_type:(Int32)1,kernel_key:<backend:GPU|layout:Undefined(AnyLayout)|dtype:float32>,kernel_name:"memcpy",op_name:"pd_op.memcpy",stop_gradient:[true]} : (undefined_tensor<1x2x3xf32>) -> gpu_tensor<1x2x3xf32>
ir_context.cc:117 Found a cached OpInfo of: [name=pd_op.memcpy, OpInfo: ptr=0x7402b60].
ir_context.cc:117 Found a cached OpInfo of: [name=pd_op.memcpy, OpInfo: ptr=0x7402b60].
interpreter_util.cc:1370 Value   : (   [0x4c2ae00]) = pd_op.memcpy( [0x81e4bf0])
interpreter_util.cc:1371 Variable: (out[0x8202a80]) = pd_op.memcpy(x[0x81e4e00])
interpreter_util.cc:1262 -----------------------------
interpreter_util.cc:1264  (%0) = "memcpy_d2h(phi_kernel)" (%1) {dst_place_type:(Int32)0,kernel_key:<backend:GPU|layout:Undefined(AnyLayout)|dtype:float32>,kernel_name:"memcpy_d2h",op_name:"pd_op.memcpy_d2h"} : (gpu_tensor<1x2x3xf32>) -> cpu_tensor<1x2x3xf32>
ir_context.cc:117 Found a cached OpInfo of: [name=pd_op.memcpy_d2h, OpInfo: ptr=0x7402d50].
ir_context.cc:117 Found a cached OpInfo of: [name=pd_op.memcpy_d2h, OpInfo: ptr=0x7402d50].
interpreter_util.cc:1370 Value   : (   [0x81e5660]) = pd_op.memcpy_d2h( [0x4c2ae00])
interpreter_util.cc:1371 Variable: (out[0x8202850]) = pd_op.memcpy_d2h(x[0x8202a80])
interpreter_util.cc:1262 -----------------------------
interpreter_util.cc:1264  () = "builtin.set_parameter" (%0) {parameter_name:"output_0"} : (cpu_tensor<1x2x3xf32>) -> 
ir_context.cc:117 Found a cached OpInfo of: [name=builtin.set_parameter, OpInfo: ptr=0x4b75358].
ir_context.cc:117 Found a cached OpInfo of: [name=builtin.set_parameter, OpInfo: ptr=0x4b75358].
interpreter_util.cc:1370 Value   : () = builtin.set_parameter(        [0x81e5660])
interpreter_util.cc:1371 Variable: () = builtin.set_parameter(output_0[0x8202850])
pir_interpreter.cc:1260 value info of interpretercore 0x81e77a0
```

可以看到执行器执行的op, 观察op可以发现在执行`memcpy`后又执行了`memcpy_d2h`, 而此时`dst_place_type`参数的值为默认的0, 所以又被拷贝回了cpu.

tensot存在设备图:

`undefined(cpu)` -> `GPU` -> `CPU`

对应 op 顺序:

`data` -> `memcpy` -> `memcpy_d2h`


* `paddle.jit.enable_to_static` 泄漏问题

精简复现demo:
```python
def run_lstm():
    paddle.jit.enable_to_static(OFF)
    net = paddle.jit.to_static(Net())

def save_in_eval():
    net = paddle.jit.to_static(Net()) # to_static 不生效

```

由于`enable_to_static`是全局的, 所以当`run_lstm`函数结束了会导致`enable_to_static`泄漏。

修复方案, 相当于给它加了个作用域:
```python
@contextmanager
def enable_to_static_guard(flag: bool):
    program_translator = paddle.jit.api.ProgramTranslator()
    original_flag_value = program_translator.enable_to_static
    program_translator.enable(flag)
    try:
        yield
    finally:
        program_translator.enable(original_flag_value)
```

修复pr:
* [#59670](https://github.com/PaddlePaddle/Paddle/pull/59670)

tracking issue:
* [#59684](https://github.com/PaddlePaddle/Paddle/issues/59684)

1. 适配`OpResult.cpu()` and `OpResult.cuda()` 

pr: [#59300](https://github.com/PaddlePaddle/Paddle/pull/59300)

### 下周工作

1. PIR 动转静组件单测问题修复
2. PIR API 以及动转静最终态适配


### 导师点评
请联系导师填写
