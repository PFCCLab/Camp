### 姓名

谢润明

### 实习项目

Paddle C++ API生态兼容建设

### 本周工作

1. 回滚 DeepGEMM 当中的部分修改以减少 diff

   https://github.com/PFCCLab/DeepGEMM/pull/9

2. 新增 torch.h 头文件

   https://github.com/PaddlePaddle/Paddle/pull/77854

3. 在 Paddle 仓库中移除 DeepEP 已经不再使用的旧接口

   https://github.com/PaddlePaddle/Paddle/pull/78549

4. 对齐 Device 相关接口

   https://github.com/PaddlePaddle/Paddle/pull/78551

5. 修复 is_available() 接口命名空间冲突

   https://github.com/PaddlePaddle/Paddle/pull/78550

6. 修复 arange 接口

   https://github.com/PaddlePaddle/Paddle/pull/78552

7. 对齐 Event 相关接口

   https://github.com/PaddlePaddle/Paddle/pull/78553

8. 对齐 resize_ 接口，支持可变大小

   https://github.com/PaddlePaddle/Paddle/pull/78554

9. 对齐若干接口

   https://github.com/PaddlePaddle/Paddle/pull/78555

10. 完善 ScalarType 相关宏，提供占位符

    https://github.com/PaddlePaddle/Paddle/pull/78581

11. 修复 CUDAContext.h 头文件导入

    https://github.com/PaddlePaddle/Paddle/pull/78584

12. 新增 TORCH_WARN 宏，并修复 resize_ 接口以解决 DeepEP 编译错误

    https://github.com/PaddlePaddle/Paddle/pull/78576

13. 重命名测试文件以 ATen|c10|torch 开头，便于回归测试

    https://github.com/PaddlePaddle/Paddle/pull/78580

14. 在 PaddleFleet 仓库中更新 DeepGEMM，实际上应该更新 DeepEP

    https://github.com/PaddlePaddle/PaddleFleet/pull/712

15. 为 DCU 设备添加测试

    https://github.com/PaddlePaddle/Paddle/pull/78595

16. 通过同步 Storage 对齐 resize_ 接口

    https://github.com/PaddlePaddle/Paddle/pull/78609

    https://github.com/PaddlePaddle/Paddle/pull/78633

17. 消除 DeepEP 引入 std::optional 带来的 diff

    https://github.com/PFCCLab/DeepEP/pull/11

18. 新增 STD_CHECK 宏

    https://github.com/PaddlePaddle/Paddle/pull/78641

19. 更新 PaddleCppAPITest 仓库下的文档及测试

    https://github.com/PFCCLab/PaddleCppAPITest/pull/58

    https://github.com/PFCCLab/PaddleCppAPITest/pull/59

20. 新增 XPU 设备相关测试用例

    https://github.com/PaddlePaddle/Paddle/pull/78647

21. 在 PaddleCodec 中新增 ARM 设备 CI

    https://github.com/PFCCLab/paddlecodec/pull/4
    
22. 在 PaddleFleet 仓库中更新 DeepEP

    https://github.com/PaddlePaddle/PaddleFleet/pull/762


### 下周工作

1. 跟进未合入的 pr
2. 尝试新增 paddlecodec 上游缺失的兼容接口，进行排查后发现，目前缺失较多

### 导师点评