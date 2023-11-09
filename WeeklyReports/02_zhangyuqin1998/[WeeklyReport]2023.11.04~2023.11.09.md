### 姓名
张钰钦

### 实习项目
新IR Pass建设

### 本周工作

1. **跑通 基于 kernel info 的 constant folding pass**
```c++
void Rewrite(pir::Operation* op,
               pir::PatternRewriter& rewriter) const override {  // NOLINT
    pir::IrContext* ctx = pir::IrContext::Instance();
    ctx->GetOrRegisterDialect<paddle::dialect::OperatorDialect>();
    ctx->GetOrRegisterDialect<paddle::dialect::KernelDialect>();
    
    // 0 设置 output name, build value
    std::string op_name = op_item->name();

    std::string output_name = "@constant_folding_pass@_" + std::to_string(suffix_++);
    paddle::framework::Variable* var = exec_info_->GetScope()->Var(output_name);
    phi::DenseTensor * ts = var->GetMutable<phi::DenseTensor>();
    exec_info_->Add(op_item->result(0), output_name);

    // 1 获取 op_info_parser
    paddle::dialect::OpYamlInfoParser op_info_parser(op_item->
        dyn_cast<paddle::dialect::OpYamlInfoInterface>().
        GetOpInfo());
    // 2 获取 kernel name
    auto kernel_fn_str = op_info_parser.OpRuntimeInfo().kernel_func;
    auto& data_type_info = op_info_parser.OpRuntimeInfo().kernel_key_dtype;

    // 3 获取 data type
    phi::DataType kernel_data_type = phi::DataType::FLOAT32;//phi::DataType::UNDEFINED;

    // 4 设置其它 kernel 信息
    phi::Backend kernel_backend = phi::Backend::CPU;
    phi::DataLayout kernel_layout = phi::DataLayout::UNDEFINED;

    // 5 获取 kernel fn
    phi::KernelKey kernel_key = phi::KernelKey(kernel_backend, kernel_layout, kernel_data_type);
    auto kernel_fn = phi::KernelFactory::Instance().SelectKernelOrThrowError(
       kernel_fn_str, kernel_key).kernel;
    
    // 6 build ctx
    pir::OpInfo op_info = ctx->GetRegisteredOpInfo(op_name);
    auto* infer_meta_interface =
        op_info.GetInterfaceImpl<paddle::dialect::InferMetaInterface>();

    phi::InferMetaContext infer_meta_context;
    phi::KernelContext kernel_context;
    {
          // EmplaceBackInputs
          // EmplaceBackAttributes
          // EmplaceBackOutputs
          // ... 代码先省略了
    }

    // 7. 设置device ctx
    kernel_context.SetDeviceContext(phi::DeviceContextPool::Instance().Get(
        phi::TransToPhiPlace(kernel_key.backend())));

    // 8 执行
    infer_meta_interface->infer_meta_(&infer_meta_context); // 填充 tensor 的 meta 信息
    kernel_fn(&kernel_context);

    // 9 获取结果
    auto out_tensor = exec_info_->GetScope()->
            FindVar(output_name)->Get<phi::DenseTensor>();

    // 10 替换结果
    std::unique_ptr<pir::Parameter> parameter =
          std::make_unique<pir::Parameter>(
              reinterpret_cast<void*>(out_tensor.data()),
              out_tensor.numel() * phi::SizeOf(out_tensor.dtype()),
              op_item->result(0).type());
    std::cout << "4" << std::endl;
    op_item->GetParentProgram()->SetParameter(output_name, std::move(parameter));
    auto get_parameter_op =
          rewriter.Build<pir::GetParameterOp>(output_name, op_item->result(0).type());
    rewriter.ReplaceAllUsesWith(op_item->result(0), get_parameter_op->result(0));
    rewriter.EraseOp(op_item);
}
```

2. **验证 constant folding pass 在 fuse attention 上的单元测试**
进度：代码已经写好，但是存在一些编译问题，准备从ninja换成make再试试。但make编译比较慢，还没有编译完。
仔细看了 combine 的代码，传入scope的话，我感觉不用跳过 combine 也能跑通。

### 下周工作

### 导师点评
