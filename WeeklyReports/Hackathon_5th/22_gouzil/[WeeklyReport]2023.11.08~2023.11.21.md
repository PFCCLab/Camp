### 姓名

田川

### 实习项目

PIR 动转静组件建设与单测验证推全

### 本周工作

1. PIR 动转静组件单测问题排查

接下来几周主要做问题排查部分

相关pr: 

* [#58630](https://github.com/PaddlePaddle/Paddle/pull/58630)
* [#58686](https://github.com/PaddlePaddle/Paddle/pull/58686)
* [#58890](https://github.com/PaddlePaddle/Paddle/pull/58890)
* [#58936](https://github.com/PaddlePaddle/Paddle/pull/58936)
* [#58965](https://github.com/PaddlePaddle/Paddle/pull/58965)
* [#59007](https://github.com/PaddlePaddle/Paddle/pull/59007)
* [#59016](https://github.com/PaddlePaddle/Paddle/pull/59016)

遇到的一些问题:

* `generator`无法切换问题
我们在拿掉`with base.dygraph.guard()`时, 会遇到`name`的`generator`无法切换的问题, 报错信息如下:
```bash
ValueError: parameter name [Base_1_w] have be been used. In dygraph mode, the name of parameter can't be same.Please check the parameter attr value passed to self.create_parameter or constructor of dygraph Layers
```

解决方案:

我们翻一下`guard`api 源码, 发现他其实在切换模式的同时调用了`framework.unique_name.guard`api
```python
def guard(place=None):
    train = framework.Program()
    startup = framework.Program()
    tracer = Tracer()

    if place is not None:
        expected_place = _get_paddle_place(place)
    else:
        expected_place = framework._current_expected_place_()

    with framework.program_guard(train, startup):
        with framework.unique_name.guard():
            with framework._dygraph_guard(tracer):
                with framework._dygraph_place_guard(expected_place):
                    yield
```
这时候我们只需要跟他做一样的操作就可以了`with unique_name.guard()`, 解决pr：[#58936](https://github.com/PaddlePaddle/Paddle/pull/58936/files#diff-97d0698d886bc904d5233448b2de3b1499e78cd1dc68d609b1a00d741ad46a90)


* `device`切换问题

在`setUp`中`paddle.set_device`会导致切换无效

原因:

`dygraph_tracer` 被换掉了，因为 `setUp` 后会走我们的 `to_xxx`，这个时候可能切动态图静态图，会换掉 `dygraph_tracer`，所以 `_expected_place` 就白设置了

可以查看一下`python/paddle/base/framework.py`的写法

```python
def _set_dygraph_tracer_expected_place(place):
    if global_var._dygraph_tracer_ is not None:
        global_var._dygraph_tracer_._expected_place = place


def _set_expected_place(place):
    global _global_expected_place_
    _global_expected_place_ = place
    _set_dygraph_tracer_expected_place(place)
```

修改方案:

将`paddle.set_device`移动到`test_xxx`内部

pr: [#59120](https://github.com/PaddlePaddle/Paddle/pull/59120/files#diff-b71242c321499d35ff39b19d4ee34c05a1168c7eed504bf5f44c9e0fc7dbb3d6)

2. 适配`OpResult.clone()`

pr: [#59115](https://github.com/PaddlePaddle/Paddle/pull/59115)

### 下周工作

1. PIR 动转静组件单测问题排查
2. PIR API 以及动转静最终态适配


### 导师点评

动转静单测推全稳步推进中，接下来在摸底单测问题的同时，如果遇到一些感觉可以修复的可以尝试修复下～LGTMeow 🐾
