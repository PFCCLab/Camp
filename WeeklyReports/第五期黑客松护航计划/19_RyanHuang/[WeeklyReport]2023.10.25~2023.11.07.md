### 姓名

黄子豪

### 实习项目

PIR 适配 AI 编译器 CINN

### 本周工作


#### 1. [遗留工作] matmul 转写PR的合入&&优化完成

- https://github.com/PaddlePaddle/Paddle/pull/56550
- https://github.com/PaddlePaddle/Paddle/pull/58517

#### 2. [遗留工作] build cinn pass test 代码 case 添加

- https://github.com/PaddlePaddle/Paddle/pull/58620


#### 3. [遗留工作] 修改 pir.cc 部分文档使其通过 xdoctest 检查 

- https://github.com/PaddlePaddle/Paddle/pull/58177


#### 4. 一些编译 Paddle 的 tricks

```shell

# cmake 指令
cmake .. -DPY_VERSION=3.8 -DWITH_GPU=ON -DWITH_TESTING=ON               -DCINN_ONLY=OFF -DWITH_CINN=ON

# 添加 PYTHONPATH 避免 wheel 安装 Paddle
export PYTHONPATH=/home/aistudio/lbwnb/Paddle/build/python

# 可以进行 Paddle 的增量修改的编译
make copy_libpaddle -j$(nproc)

# 修改单测可以只 make 相应的 target
make {单测 targe}  -j$(nproc)


# 改 pip 源, pre-commit 安装速度提升
echo -e '[global]\nindex-url=http://mirrors.aliyun.com/pypi/simple/\ntrusted-host=mirrors.aliyun.com' >> ~/.pip/pip.conf
python -mpip install httpx --upgrade pip

# 运行单测 demo
FLAGS_NEW_IR_OPTEST_WHITE_LIST=1 FLAGS_NEW_IR_OPTEST=1 GLOG_v=10 python test/legacy_test/test_mul_op.py  >err.log 2>&1

ctest -VV -R test_pir_build_cinn_pass
```

#### 5. 新IR Python API适配升级

新IR Python API适配升级
- https://github.com/PaddlePaddle/Paddle/pull/58394
- https://github.com/PaddlePaddle/Paddle/pull/58445
- https://github.com/PaddlePaddle/Paddle/pull/58629
- https://github.com/PaddlePaddle/Paddle/pull/58670
- https://github.com/PaddlePaddle/Paddle/pull/58675
- https://github.com/PaddlePaddle/Paddle/pull/58683
- https://github.com/PaddlePaddle/Paddle/pull/58693
- https://github.com/PaddlePaddle/Paddle/pull/58699


#### 6. 阅读 cinn 相关源码

- [cinn_source_code_reading_guide](https://github.com/DrRyanHuang/community/blob/master/pfcc/paddle-code-reading/IR_Dialect/)

### 下周工作

1. 新IR Python API适配升级

160、204、216、23、27、102、140-142

2. 继续进行 cinn 相关源码阅读


### 导师点评
总结：优秀。子豪本周参与了非常多的 API PIR 迁移的工作，积极主动，遇到问题及时沟通和同步，进展较快。
建议：在迁移过程中，可以多发现和多思考遇到的功能问题，反馈给内部同学支持。
