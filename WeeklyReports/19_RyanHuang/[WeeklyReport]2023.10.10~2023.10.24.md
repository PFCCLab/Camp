### 姓名

黄子豪

### 实习项目

PIR 适配 AI 编译器 CINN

### 本周工作

1. **理清 mul 映射为 matmul 算子的过程**

```python
# 测试代码
import paddle
from paddle.common_ops_import import LayerHelper
    
def mul(x, y, x_num_col_dims, y_num_col_dims=1):
    
    helper = LayerHelper("mul", **locals())
    dtype = helper.input_dtype()
    tmp = helper.create_variable_for_type_inference(dtype)
    helper.append_op(
        type="mul",
        inputs={"X": x, "Y": y},
        outputs={"Out": tmp},
        attrs={"x_num_col_dims": x_num_col_dims, "y_num_col_dims": y_num_col_dims},
    )
    
    return tmp


paddle.enable_static()
x = paddle.randn([3, 4, 2, 3, 4])
y = paddle.randn([4, 6, 5, 7])

out = mul(x, y, 2, 2)
# (3, 4, 5, 7)

print(out.shape)

x = paddle.randn([12, 24])
y = paddle.randn([24, 35])

out2 = paddle.matmul(x, y)
print(out2.shape)
# (12, 35)
```

#### MulOpTranscriber

##### `mul` 算子的**输入**映射:

`x` `[3, 4, 2, 3, 4]` `reshape` => `[3x4, 2x3x4]`

`y` `[4, 6, 5, 7]` `reshape` => `[4x6, 5x7]`

将 `x` 和 `y` 映射为 `mul` 的输入


##### `mul` 算子的**输出**映射:

`x` 的输入 `[3x4, 2x3x4]` 和 `y` 的输出 `[4x6, 5x7]`, 通过 `matmul` 算子计算为 `out` `[3x4, 5x7]`

所以需要将 `out` `[3x4, 5x7]` 再 `reshape` 为 `[3, 4, 5, 7]`


##### `mul` 算子要拿到自己的 `Attribute`:

`x_num_col_dims` 和 `y_num_col_dims`


#### MulGradOpTranscriber


##### `mul` 算子的**输入**映射:

与 `MulOpTranscriber` 相同, 也要将输入 `x` 和 `y` 进行 `reshape`

`x` `[3, 4, 2, 3, 4]` `reshape` => `[3x4, 2x3x4]`

`y` `[4, 6, 5, 7]` `reshape` => `[4x6, 5x7]`

`out@GRAD` `[3, 4, 5, 7]` `reshape` 为 `[3x4, 5x7]`


##### `mul` 算子的**输出**映射:

由于 `matmul` 输出的 `Y@GRAD` 和 `X@GRAD` 的 shape 分别是 `[3x4, 2x3x4]` 和 `[4x6, 5x7]`

所以需要将 `X@GRAD` 和 `Y@GRAD` 分别 `reshape` 为 `[3, 4, 2, 3, 4]` 和 `[4, 6, 5, 7]`



##### `mul` 算子要拿到自己的 `Attribute`:

`x_num_col_dims` 和 `y_num_col_dims` 



2. **阅读 build_cinn_pass_test 源码**

`fluid/framework/paddle2cinn/build_cinn_pass_test.cc` 单测中建立了以下几个图

- NoCinnSubgraph

```c++
  // var1 --
  //        | --> fake1 --> var3 --> fake2 --> var4
  // var2 --
```

- AllOpSupportCinn

```c++
  // v0 --|
  // v1 --|                  
  // v2 --| --> mul  --> v3 --|
  //                 --> v4 --| --> add  --> v5 --> relu  --> v6
  //                                                      --> v7
``` 
构建 pass 之后, 将几个算子整合为 `kCinnLaunchOp`

```c++
  // v0 --|
  // v1 --|                   |--> v6
  // v2 --| --> kCinnLaunchOp |--> v7
  // v4 --|
```

- OneCinnSubgraph

```c++
  // fake1 --> v1 --
  //                | --> mul --> v3 --> relu --> v4 --> fake2
  //           v2 --
```

构建 pass 之后, 将几个算子整合为 `kCinnLaunchOp`

```c++
  // fake1 --> v1 --
  //                | --> kCinnLaunchOp --> v4 --> fake2
  //           v2 --
```

- MultiCinnSubgraph

```c++
  // fake1 --> v1 --
  //                | --> mul --> v3 --> fake2 --> v4 --> relu --> v5 --> fake3
  //           v2 --
```

构建 pass 之后, 将几个算子整合为 `kCinnLaunchOp`, 构建了两个 `CinnOp`

```c++
  // fake1 -> v1 -
  //              | -> CinnOp -> v3 -> fake2 -> v4 -> CinnOp ->v5 -> fake3
  //          v2 -
```


- NoNeedBufferInput

```c++
  // fake1 --> v1 --                 --> v4 --> relu_grad --> v6
  //           v2 -- | --> add_grad |
  //           v3 --                 --> v5 --> fake2
```

构建 pass 之后的图:

```c++
  // fake1 --> v1 --                     --> v6
  //           v2 -- | -->kCinnLaunchOp |
  //           v3 --                     --> v5 --> fake2
```

`test/cpp/pir/cinn/build_cinn_pass_test.cc` 目录下只有一个单测 `Program` 构建 pass 之后, 查看其 `block` 下算子名字是否对的上:

```c++
paddle::dialect::FullOp::name()
paddle::dialect::TanOp::name()
paddle::dialect::ReluOp::name()
paddle::dialect::TanOp::name()
paddle::dialect::ReluOp::name()
pir::YieldOp::name()
```

3. 完成 `LeakyReLU` 和 `swish` 的 PIR Python API适配升级

- https://github.com/PaddlePaddle/Paddle/pull/58394


### 下周工作

1. 新IR Python API适配升级：178, 169, 137, 34, 129, 152, 187, 197, 219-221, 225, 227

2. 完成新IR build_cinn_pass_test



### 导师点评

请联系导师填写