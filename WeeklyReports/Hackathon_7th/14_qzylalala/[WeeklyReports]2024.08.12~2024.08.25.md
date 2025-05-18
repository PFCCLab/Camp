### 姓名

秦忠宇

### 实习项目

飞桨PaddlePaddle-PIR适配2ONNX推理转换

### 本周工作

1. 添加 mentor 的仓库链接到 remote, 拉取未合并的 pr 代码, 保持代码同步开发, 避免重复造轮子
2. 新代码编译遇到问题，找不到 `paddle/fluid/pir/dialect/operator/ir/op_dialect.h` 更新 Paddle 版本至最新解决了该问题
3. 整体工作主要分为两部分 : 
   1. Paddle PIR Parser 的初始化工作 LoadProgram、LoadParameters, 和 mentor 分别自己写了 LoadProgram, 现在把 mentor 的开发仓库添加到 remote 保持代码一致, LoadParameters 暂时使用了 mentor 实现的版本
   2. ModelExporter 进行导出, 这两周梳理了其导出逻辑依赖的 PaddleParser 的接口
      1. register_mapper 逻辑与 PaddleParser 无关，可以直接复用
           - [ ] CreateMapper
      2. data_helper 逻辑与 PaddleParser 无关，可以直接复用
      3. onnx_helper 逻辑与 PaddleParser 无关，可以直接复用
      4. mapper 逻辑与 PaddleParser 相关
           - [ ] GetOpDesc
           - [ ] OpHasInput
           - [ ] OpHasOutput
           - [ ] OpHasAttr
           - [ ] GetOpInput
           - [ ] GetOpOutput
           - [ ] GetOpAttr
           - [ ] GetOpAttrVar
           - [ ] OpIsAttrVar
           - [ ] IsConstantTensor
           - [ ] TryGetTensorValue
       5. export 逻辑与 PaddleParser 相关，主要是在 ModelExporter 类中的方法涉及到
           - [ ] NumOfBlocks
           - [ ] NumOfOps
           - [ ] GetOpDesc
           - [ ] GetOpInput
           - [ ] GetOpOutput
           - [ ] parser.inputs
           - [ ] parser.outputs
           - [ ] parser.params
           - [ ] parser.is_quantized_model
       6. quanize_helper 逻辑与 PaddleParser 相关，涉及到两个接口
           - [ ] NumOfBlocks
           - [ ] TryGetTensorValue

### 下周工作

1. 为 PaddlePirParser 逐步实现梳理出来的 ModelExporter 依赖的 PaddleParser 接口

### 导师点评