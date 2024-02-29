### 姓名
张钰钦

### 实习项目
新IR Pass建设

### 本周工作

1. **重新适配constant folding pass**
#### 方法1 引入 InterpreterCore 进行常量折叠计算
在原来代码的基础上重新适配（原来的代码没跑通），并给 pass 传入 scope。InterpreterCore 从 scope 中可以拿到常量参数，并进行计算，将计算结果再存回 scope。最后进行子图替换。
核心代码如下：
```C++
void Rewrite(pir::Operation* op_item,
            pir::PatternRewriter& rewriter) const override {
  std::string out_name = "@constant_folding_pass@_" + std::to_string(suffix_++);

  auto temp_program = BuildProgramFromOperation(op_item, out_name);

  auto kernel_program =
        paddle::dialect::PdOpLowerToKernelPass(temp_program.get());

  auto place = phi::CPUPlace();
  exe_config_.create_local_scope = false;

  paddle::framework::InterpreterCore core(place, {}, kernel_program->block(), scope_, exe_config_);

  core.SetSkipGcVars({out_name});
  core.Run({});

  paddle::framework::Variable * out_var = scope_->FindVar(out_name);
  auto out_tensor = out_var->Get<phi::DenseTensor>();

  std::unique_ptr<pir::Parameter> parameter =
        std::make_unique<pir::Parameter>(
            reinterpret_cast<void*>(out_tensor.data()),
            out_tensor.numel() * phi::SizeOf(out_tensor.dtype()),
            op_item->result(0).type());
  op_item->GetParentProgram()->SetParameter(out_name, std::move(parameter));

  auto get_parameter_op =
        rewriter.Build<pir::GetParameterOp>(out_name, op_item->result(0).type());

  rewriter.ReplaceAllUsesWith(op_item->result(0), get_parameter_op->result(0));
  rewriter.EraseOp(op_item);
}
```

#### 方法2 不引入 InterpreterCore，而是根据 OpInfoTuple 直接找到 kernel 进行计算
代码编写已经完成，但调试时遇到一些问题。目前在 kernel 中为 output tensot 申请内存时会 core，具体原因尚未找出。
core发生在 return static_cast<T*>(this->Alloc(tensor, dtype, requested_size, pinned))，并且检查过 this 非空：
```C++
template <typename T>
T* DeviceContext::Alloc(TensorBase* tensor,
                        size_t requested_size,
                        bool pinned) const {
  DataType dtype = phi::CppTypeToDataType<T>::Type();
  return static_cast<T*>(this->Alloc(tensor, dtype, requested_size, pinned));
}
```

2. **搭建constant folding pass单元测试**
搭建了简单的 UT，测试常量折叠的方法，并成功跑通

### 下周工作
1. **找到代码中的问题**
找到 DeviceContext 为什么会发生这个问题

### 导师点评
11-03：本周开发工作有一定难度，钰钦能够很快解决遇到的各种问题，点赞！
