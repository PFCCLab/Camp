## 1. 背景

### 当前面临问题

- 开发任务大。新增算子时，需要适配所有硬件平台。同样，当接入新的硬件平台时，需要适配所有算子。

- 后端开发难度大。后端开发时，需要考虑算子的高阶微分，算子并行，算子融合等各种机制。

  

### PyTorch 2.x 中的 `torch.compile`

-  基于四种新技术 - `TorchDynamo`、`AOTAutograd` 、`PrimTorch` 、`TorchInducto`
- **TorchDynamo：快速可靠的获取计算图**
  -   TorchDynamo 使用 Python Frame Evaluation Hooks 安全地捕获 PyTorch 程序，这是一项重大创新，用来快速可靠地获取计算图，是研究团队花费 5 年研发的结果。
- **AOTAutograd：将 Autograd 重用于 ahead-of-time 图**
  -   AOTAutograd 重载 PyTorch 的 autograd 引擎作为一个跟踪 autodiff，用于生成 ahead-of-time 向后跟踪。
- **PrimTorch: 稳定的原始算子集合**
  -   通常情况下，为 PyTorch 编写后端是一件复杂工作。PyTorch 有 1200 多个算子，如果考虑每个算子的各种重载，则有 2000 多个。
  -   将约 2000 多个 PyTorch 算子规范化为一组约 250 个原始算子的闭集，可以将其看作 PyTorch 后端所有算子的子集。使用这种方法，大大降低了编写 PyTorch 特性或后端的障碍。
  - 
  -   在 PrimTorch 项目中，研发团队的目标是构建更小且稳定的算子集，并将 PyTorch 程序基于这个较小的算子集进行构建。目标是定义两个算子集：
  - Prim ops：包含约 250 个相对底层的算子，这些算子底层进行了很多性能优化，同时配合编译器将这些算子进行融合，可以获得良好的性能。
  - ATen ops：包含约 750 个典型算子 (canonical operator)，适合于直接输出。这些算子适用于传统的动态图，不经过编译后端优化的场景。不需要经过编译器恢复性能。
  - 
- **TorchInductor: 使用 define-by-run** **IR** **快速生成代码 [** **对应 paddle 中的 cinn** **]** **[Paddle cinn 传送门](https://github.com/PaddlePaddle/CINN)**
  -   TorchInductor 是一种深度学习编译器，可为多个加速器和后端生成快速代码。对于 NVIDIA GPU，它使用 OpenAI Triton 作为关键构建块。



![img](https://github.com/kevincheng2/Camp/blob/kevincheng2/WeeklyReport/Docs/04_TheUnityOfOperatorForwardAndBackwardInCombinationFeatures/imgs/pytorch_compilation_process.png)

​												The PyTorch compilation process

### 图算融合技术  --  静态图框架

以 MindSpore 的图算融合技术为例，图算融合通过 **算子拆解、算子聚合、算子重建** 三个主要阶段让计算图中的计算更密集，并进一步减少低效的内存访问。

![img](https://github.com/kevincheng2/Camp/blob/kevincheng2/WeeklyReport/Docs/04_TheUnityOfOperatorForwardAndBackwardInCombinationFeatures/imgs/aggregation_compute.png)



## 2. 组合机制

### softmax 算子 - 前向拆解

- 计算公式

​  $$Softmax(x)_{i} = \frac{e^{x_{i}}}{\sum_{j=1}^{N}e^{x_{j}}}, j=1,2,...,n$$

- 上溢出(overflow)和下溢出(underflow)

​	计算机中使用二进制表示数值，当某个 $$x_{i}$$ 数值过小时，被四舍五入表示为0，这就是下溢出。

​	同理，当 $$x_{i}$$ 数值过大时，会出现上溢出。

- 解决方法

​	$$ Softmax(x)_{i} = \frac{e^{x_{i}} / e^{x_{max}} }{(\sum_{j=1}^{N}e^{x_{j}})/e^{x_{max}}} = \frac{e^{x_{i}-x_{max}}}{\sum_{j=1}^{N}e^{x_{j}-x_{max}}} , j=1,2,...,n $$

​	对于任何一个 $$x_{i}$$ ，减去 $$x_{max}$$ 之后，$$e$$的指数最大值为 `0` ，所以不会出现上溢出情况。同时，分母中至少包含一个值为 1 的项，所以不会下溢出。

### 代码实现

```C++
template <typename T>
Tensor softmax_decomp(const Tensor& x, const int& axis) {
  auto org_dtype = x.dtype();
  auto x_tmp = x;
  auto axis_tmp = IntArray({axis});

  bool need_cast = is_half_dtype(org_dtype);
  if (need_cast) {
    x_tmp = cast<T>(x, phi::DataType::FLOAT32);
  }

  auto max_tmp = max<T>(x_tmp, axis_tmp, true);
  auto molecular = exp<T>(x_tmp - max_tmp);
  auto res = molecular / sum<T>(molecular, axis_tmp, molecular.dtype(), true);

  if (need_cast) {
    return cast<T>(res, org_dtype);
  } else {
    return res;
  }
}
```

![img](https://github.com/kevincheng2/Camp/blob/kevincheng2/WeeklyReport/Docs/04_TheUnityOfOperatorForwardAndBackwardInCombinationFeatures/imgs/operator_prim.png)

### sqrt 算子 - 反向拆解

​										$$(\sqrt{x})' = 1/（2*\sqrt{x}）$$

```C++
template <typename T>
void sqrt_grad(const Tensor& out, const Tensor& out_grad, Tensor* x_grad) {
  if (x_grad) {
    // This calculation is important for resnet.
    auto x_grad_tmp = (0.5 / out) * out_grad;
    set_output<T>(x_grad_tmp, x_grad);
  }
}
```

## 3. 组合机制在 paddle 中的实现

### 算子前向拆解

![img](https://github.com/kevincheng2/Camp/blob/kevincheng2/WeeklyReport/Docs/04_TheUnityOfOperatorForwardAndBackwardInCombinationFeatures/imgs/forward_prim.png)

```C++
// /home/aistudio/Paddle/paddle/fluid/pybind/pybind.cc

void BindDecomp(pybind11::module *m) {
  m->def("call_decomp", [](pir::Operation &fwd_op) {
    py::list res;
    paddle::dialect::DecompInterface decomp_interface =
        fwd_op.dyn_cast<paddle::dialect::DecompInterface>();
    PADDLE_ENFORCE(
        decomp_interface,
        phi::errors::InvalidArgument(
            "The decomp function is not registered in %s op ", fwd_op.name()));
    std::vector<std::vector<pir::OpResult>> decomp_res =
        decomp_interface.Decomp(&fwd_op);
```
```c++
// /home/aistudio/Paddle/paddle/fluid/pir/dialect/operator/interface/decomp.h

class DecompInterface : public pir::OpInterfaceBase<DecompInterface> {
 public:
  struct Concept {
    explicit Concept(
        std::vector<std::vector<pir::OpResult>> (*decomp)(pir::Operation* op))
        : decomp_(decomp) {}
    std::vector<std::vector<pir::OpResult>> (*decomp_)(pir::Operation* op);
  };
  
  std::vector<std::vector<pir::OpResult>> Decomp(pir::Operation* op) {
    return impl_->decomp_(op);
  }

 private:
  Concept* impl_;
};
```
```c++
// /home/aistudio/Paddle/paddle/fluid/pir/dialect/operator/ir/pd_op.h

class ReluOp : public pir::Op<ReluOp, ... ,paddle::dialect::DecompInterface,paddle::dialect::VjpInterface,paddle::dialect::CustomVjpTrait> {
 public:
  using Op::Op;
  static const char *name() { return "pd_op.relu"; }
  static constexpr const char **attributes_name = nullptr;
  static constexpr uint32_t attributes_num = 0;
  static OpInfoTuple GetOpInfo();
  static void Build(pir::Builder &builder, pir::OperationArgument &argument, pir::Value x_);
  
  static std::vector<std::vector<pir::OpResult>> Vjp(pir::Operation* op, const std::vector<std::vector<pir::Value>>& inputs_, const std::vector<std::vector<pir::OpResult>>& outputs, const std::vector<std::vector<pir::Value>>& out_grads, const std::vector<std::vector<bool>>& stop_gradients);
  static std::vector<std::vector<pir::OpResult>> Decomp(pir::Operation* op);
 }
```
```c++
// /home/aistudio/Paddle/paddle/fluid/pir/dialect/operator/ir/op_decomp.cc

std::vector<std::vector<pir::OpResult>> ReluOp::Decomp(pir::Operation* op) {
  VLOG(4) << "Decomp call relu's decomp interface begin";
  ReluOp op_obj = op->dyn_cast<ReluOp>();
  (void)op_obj;
  FLAGS_tensor_operants_mode = "static";
  VLOG(6) << "Decomp Prepare inputs of relu";
  Tensor x(std::make_shared<primitive::LazyTensor>(op_obj.x()));
  VLOG(6) << "Decomp prepare attributes of relu";
  VLOG(6) << "Decomp call relu's forward composite rule prepare";
  auto org_res = op->results();
  std::vector<std::vector<pir::OpResult>> res(org_res.size());

  VLOG(6) << "Decomp call relu's forward composite rule begin";
  Tensor op_res = paddle::primitive::details::relu_decomp<primitive::LazyTensor>(x);
  VLOG(6) << "Decomp call relu's forward composite rule end";

  res[0].push_back(
    std::static_pointer_cast<primitive::LazyTensor>(op_res.impl())
        ->value()
        .dyn_cast<pir::OpResult>());
  VLOG(4) << "Decomp call relu's decomp interface end";
  return res;
}
```
```c++
// /home/aistudio/Paddle/paddle/fluid/pir/dialect/operator/ir/op_decomp.cc

template <typename T>
Tensor relu_decomp(const Tensor& x) {
  return maximum<T>(x, full<T>(phi::vectorize(x.dims()), 0.0, x.dtype()));
}
```

### 算子反向拆解

![img](https://github.com/kevincheng2/Camp/blob/kevincheng2/WeeklyReport/Docs/04_TheUnityOfOperatorForwardAndBackwardInCombinationFeatures/imgs/backward_prim.png)

```C++
// /home/aistudio/Paddle/paddle/fluid/pybind/pybind.cc

void BindVjp(pybind11::module *m) {
  m->def(
      "call_vjp",
      [](pir::Operation &fwd_op,
         const std::vector<std::vector<pir::Value>> &inputs,
         const std::vector<std::vector<pir::OpResult>> &outputs,
         const std::vector<std::vector<pir::OpResult>> &out_grads,
         const std::vector<std::vector<bool>> &stop_gradients) {
        py::list res;
        paddle::dialect::VjpInterface vjp_interface =
            fwd_op.dyn_cast<paddle::dialect::VjpInterface>();
        PADDLE_ENFORCE(
            vjp_interface,
            phi::errors::InvalidArgument(
                "The vjp function is not registered in %s op ", fwd_op.name()));
        std::vector<std::vector<pir::OpResult>> vjp_res = vjp_interface.Vjp(
            &fwd_op, inputs, outputs, out_grads, stop_gradients);
......     
```
```c++
// /home/aistudio/Paddle/paddle/fluid/pir/dialect/operator/interface/vjp.h

class VjpInterface : public pir::OpInterfaceBase<VjpInterface> {
 public:
  struct Concept {
    explicit Concept(std::vector<std::vector<pir::OpResult>> (*vjp)(
        pir::Operation* op,
        const std::vector<std::vector<pir::Value>>& inputs,
        const std::vector<std::vector<pir::OpResult>>& outputs,
        const std::vector<std::vector<pir::Value>>& out_grads,
        const std::vector<std::vector<bool>>& stop_gradients))
        : vjp_(vjp) {}
    std::vector<std::vector<pir::OpResult>> (*vjp_)(
        pir::Operation* op,
        const std::vector<std::vector<pir::Value>>& inputs,
        const std::vector<std::vector<pir::OpResult>>& outputs,
        const std::vector<std::vector<pir::Value>>& out_grads,
        const std::vector<std::vector<bool>>& stop_gradients);
  };
    std::vector<std::vector<pir::OpResult>> Vjp(
      pir::Operation* op,
      const std::vector<std::vector<pir::Value>>& inputs,
      const std::vector<std::vector<pir::OpResult>>& outputs,
      const std::vector<std::vector<pir::Value>>& out_grads,
      const std::vector<std::vector<bool>>& stop_gradients) {
    return impl_->vjp_(op, inputs, outputs, out_grads, stop_gradients);
  }
 }
```
```c++
// /home/aistudio/Paddle/paddle/fluid/pir/dialect/operator/ir/pd_op_vjp.cc

std::vector<std::vector<pir::OpResult>> SumOp::Vjp(pir::Operation* op, const std::vector<std::vector<pir::Value>>& inputs_, const std::vector<std::vector<pir::OpResult>>& outputs, const std::vector<std::vector<pir::Value>>& out_grads, const std::vector<std::vector<bool>>& stop_gradients){
......
    VLOG(6) << "Prepare inputs of sum_grad";
    Tensor x(std::make_shared<primitive::LazyTensor>(inputs_[0][0]));
    Tensor out_grad(std::make_shared<primitive::LazyTensor>(out_grads[0][0]));
    VLOG(6) << "Vjp prepare Prepare attributes of sum_grad";
    Tensor axis(std::make_shared<primitive::LazyTensor>(inputs_[1][0]));
    bool keepdim = op->attribute("keepdim").dyn_cast<pir::BoolAttribute>().data();
    bool reduce_all = false;

    VLOG(6) << "Vjp prepare call sum's vjp inteface";
    std::vector<std::vector<Tensor>> tensor_res =
        primitive::sum_vjp(
        x, out_grad, axis, keepdim, reduce_all, stop_gradients);
    VLOG(6) << "Vjp prepare stop gradient of sum_grad";

    std::vector<std::vector<pir::OpResult>> res(tensor_res.size());
    for (size_t i = 0; i < tensor_res.size(); ++i) {
        res[i].resize(tensor_res[i].size());
        for (size_t j = 0; j < tensor_res[i].size(); ++j) {
            if(tensor_res[i][j].defined()){
                res[i][j] = std::static_pointer_cast<primitive::LazyTensor>(tensor_res[i][j].impl())->value().dyn_cast<pir::OpResult>();
            }
        }
    }
    return res;
}
```
```c++
// /home/aistudio/Paddle/paddle/fluid/primitive/rule/vjp/generated/generated_vjp.cc

std::vector<std::vector<paddle::Tensor>> sum_vjp(const Tensor& x, const Tensor& out_grad, const Tensor& axis_, bool keepdim, bool reduce_all, const std::vector<std::vector<bool>>& stop_gradients) {
  std::vector<std::vector<paddle::Tensor>> vjp_res;
  for (auto arg: stop_gradients) {
    vjp_res.push_back(std::vector<paddle::Tensor>(arg.size()));
  }
  std::string op_name = "sum_grad";
  auto need_skip = paddle::prim::StaticCompositeContext::Instance().CheckSkipCompOps(op_name);
  if (paddle::prim::StaticCompositeContext::Instance().IsBwdPrimEnabled() && !need_skip) {
    FLAGS_tensor_operants_mode = "static";
    VLOG(4) << "Call Pir Decomposed backward op sum_grad";
    paddle::Tensor* x_grad = !stop_gradients[0][0] ? &vjp_res[0][0] : nullptr; 
    auto* axis_define_op = std::static_pointer_cast<primitive::LazyTensor>(axis_.impl())->value().dyn_cast<pir::OpResult>().owner();
    if(axis_define_op->name() != "pd_op.full_int_array"){
      PADDLE_THROW(platform::errors::Unimplemented(
          "We don't support dynamic tensors attribute axis for sum_grad composite "
          "for now. "));
    }
    auto axis = phi::IntArray(paddle::dialect::GetInt64Vector(axis_define_op->attribute("value")));

    details::sum_grad<LazyTensor>(x, out_grad, axis, keepdim, reduce_all, x_grad);
  } else {
    auto op_res = backend::sum_grad<LazyTensor>(x, out_grad, axis_, keepdim, reduce_all);
    vjp_res[0][0] = op_res;
    vjp_res = ConstructVjpResultByStopGradients(vjp_res, stop_gradients);
  }
  return vjp_res;
}
```
```c++
// /home/aistudio/Paddle/paddle/fluid/primitive/rule/vjp/details.h

template <typename T>
void sum_grad(const Tensor& x,
              const Tensor& out_grad,
              const IntArray& axis,
              bool keepdim,
              bool reduce_all,
              Tensor* x_grad) {
......             
}
```
