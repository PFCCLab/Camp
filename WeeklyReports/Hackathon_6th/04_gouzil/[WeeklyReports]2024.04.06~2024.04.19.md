### 姓名

田川

### 实习项目

PIR 动转静理想态单测推全验证任务（二期）

### 本周工作

#### **PIR 0 维单测适配结项**

任务issue: [#62652](https://github.com/PaddlePaddle/Paddle/issues/62652)

#### **PIR 动转静理想态单测推全验证任务（二期）**

##### 遇到的一些小问题

* 在动转静跑反向的时候 hold 不住反向 Program 导致跑反向时 Program 不存在的问题，整体上参考了[PR#63216](https://github.com/PaddlePaddle/Paddle/pull/63216) 和 [PR#59764](https://github.com/PaddlePaddle/Paddle/pull/59764) 思路，修复 PR [#63694](https://github.com/PaddlePaddle/Paddle/pull/63694) (下周修复)

```python
def static_func(x, no_grad_x):
    tx = 2 * no_grad_x
    tx.stop_gradient = True
    return 2 * x


def main_func(x, index):
    tmp = paddle.gather(x, index)
    out = paddle.jit.to_static(static_func)(x, tmp) # program 被意外释放, 导致反向时找不到对应的 program
    return out


class TestNoGradientCase(Dy2StTestBase):
    @test_ast_only
    @test_pir_only
    def test_no_gradient(self):
        paddle.disable_static()
        x = paddle.randn([10, 3])
        index = paddle.arange(0, 10, 1, dtype='int32')
        x.stop_gradient = False
        index.stop_gradient = True

        func = main_func
        output = func(x, index).mean()
        output.backward() # 这里会报错
```

### 下周工作

1. PIR 动转静理想态单测推全验证任务（二期）

### 导师点评

加油加油，下周继续 :doge:

LGTMeow <img src="https://www.gstatic.com/android/keyboard/emojikitchen/20220506/u1f381/u1f381_u1f43e.png" width="14" alt="🐾"/>