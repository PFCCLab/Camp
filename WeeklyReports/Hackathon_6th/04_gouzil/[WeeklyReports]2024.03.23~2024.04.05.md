### 姓名

田川

### 实习项目

PIR 0 维单测适配

### 本周工作

#### **PIR 0 维单测适配**

##### 遇到的一些小问题

* PIR 下已经明确不使用`name`作为`fetch_list`

例子:
```diff
x1 = paddle.static.data(name="x1", shape=[])
prog = paddle.static.default_main_program()
res = self.exe.run(
    prog,
    feed={
        "x1": np.array(1.0, dtype='float32'),
    },
    fetch_list=[
-         x1.name,
+         x1,
    ],
)
```

修复pr：[#62879](https://github.com/PaddlePaddle/Paddle/pull/62879)

* 在 PIR 下错误的生成更多的反向，导致执行期内部检查错误

原:
```bash
{
    (%0) = "pd_op.full" () {dtype:(pd_op.DataType)int64,place:(pd_op.Place)Place(undefined:0),shape:(pd_op.IntArray)[2,2],stop_gradient:[true],value:(Float)0} : () -> builtin.tensor<2x2xi64>
    (%1) = "pd_op.assign_value_" (%0) {dtype:(pd_op.DataType)int64,place:(pd_op.Place)Place(undefined:0),shape:[(Int32)2,(Int32)2],stop_gradient:[true],values:[(Double)3,(Double)3,(Double)3,(Double)3]} : (builtin.tensor<2x2xi64>) -> builtin.tensor<2x2xi64>
    (%2) = "pd_op.cast" (%1) {dtype:(pd_op.DataType)float32,stop_gradient:[false]} : (builtin.tensor<2x2xi64>) -> builtin.tensor<2x2xf32>
    (%3) = "pd_op.full" () {dtype:(pd_op.DataType)float32,place:(pd_op.Place)Place(cpu),shape:(pd_op.IntArray)[1],stop_gradient:[true],value:(Float)1} : () -> builtin.tensor<1xf32>
    (%4) = "pd_op.full_like" (%2, %3) {dtype:(pd_op.DataType)float32,place:(pd_op.Place)Place(undefined:0),stop_gradient:[false]} : (builtin.tensor<2x2xf32>, builtin.tensor<1xf32>) -> builtin.tensor<2x2xf32>
    (%5) = "pd_op.cast" (%4) {dtype:(pd_op.DataType)int64,stop_gradient:[false]} : (builtin.tensor<2x2xf32>) -> <<NULL TYPE>>
}
```
现:
```bash
{
    (%0) = "pd_op.full" () {dtype:(pd_op.DataType)int64,place:(pd_op.Place)Place(undefined:0),shape:(pd_op.IntArray)[2,2],stop_gradient:[true],value:(Float)0} : () -> builtin.tensor<2x2xi64>
    (%1) = "pd_op.assign_value_" (%0) {dtype:(pd_op.DataType)int64,place:(pd_op.Place)Place(undefined:0),shape:[(Int32)2,(Int32)2],stop_gradient:[true],values:[(Double)3,(Double)3,(Double)3,(Double)3]} : (builtin.tensor<2x2xi64>) -> builtin.tensor<2x2xi64>
    (%2) = "pd_op.cast" (%1) {dtype:(pd_op.DataType)float32,stop_gradient:[false]} : (builtin.tensor<2x2xi64>) -> builtin.tensor<2x2xf32>
    (%3) = "pd_op.full" () {dtype:(pd_op.DataType)float32,place:(pd_op.Place)Place(cpu),shape:(pd_op.IntArray)[1],stop_gradient:[true],value:(Float)1} : () -> builtin.tensor<1xf32>
    (%4) = "pd_op.full_like" (%2, %3) {dtype:(pd_op.DataType)float32,place:(pd_op.Place)Place(undefined:0),stop_gradient:[false]} : (builtin.tensor<2x2xf32>, builtin.tensor<1xf32>) -> builtin.tensor<2x2xf32>
}
```
修复 pr: [#63113](https://github.com/PaddlePaddle/Paddle/pull/63113), 在生成反向的时候不要过滤 `inplace` 操作


### 下周工作

1. PIR 0 维单测适配

### 导师点评