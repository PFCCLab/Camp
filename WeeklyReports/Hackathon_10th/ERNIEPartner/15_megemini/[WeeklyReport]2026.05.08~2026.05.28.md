### 认领者 GitHub ID
megemini

### 赛题信息

- **进阶任务序号**：#15
- **赛题名称**：基于天数智芯硬件与文心多模态模型的创新应用
- **关联厂商**：天数

### 本周工作

1. **RFC 文档**

   - 已经完成 RFC 文档
   - AI Studio 地址：https://aistudio.baidu.com/project/edit/10221576

2. **代码实现**

   - 已经完成 AI Studio 项目的 notebook
   - 已经创建了双卡的天数环境
   - 已完成 cli 的脚本，`drug_ocr_cli.py`
   - 已发布 AI Studio notebook 项目：https://aistudio.baidu.com/projectdetail/10413884
   > 注意：因为后面提到的 AI Studio 环境问题，此 notebook 的 ERNIE-4.5-0.3B-Paddle 输出混乱，因此，此 notebook 仅作为参考，可在本地最新的天数环境运行调试。

3. **README**

    - 可以参考 AI Studio 项目的 notebook

4. **演示视频/截图**

    - 待完成

5. **问题与解决**

   - 问题：AI Studio 的 notebook 中无法正常调用 ERNIE-4.5-0.3B-Paddle

   解决：经确认，AI Studio 的 notebook 环境有问题，后续使用 cli 的方式

   ![notebook](images/notebook.png)

   - 问题：天数的双卡框架开发环境中不能编译最新的 FastDeploy 版本 https://github.com/PaddlePaddle/FastDeploy/issues/7948

   ```shell
    /home/aistudio/FastDeploy/custom_ops/build/fastdeploy_ops/temp.linux-x86_64-cpython-310/build/fastdeploy_ops/temp.linux-x86_64-cpython-310/iluvatar_ops/runtime/iluvatar_context.o is compiled
    /home/aistudio/FastDeploy/custom_ops/iluvatar_ops/paged_attn.cu:199:37: error: no matching constructor for initialization of 'PageAttentionWithKVCacheArguments'
    199 |   PageAttentionWithKVCacheArguments args{
        |                                     ^   ~
    200 |       static_cast<float>(scale),
        |       ~~~~~~~~~~~~~~~~~~~~~~~~~~
    201 |       1.0,
        |       ~~~~
    202 |       1.0,
        |       ~~~~
    203 |       static_cast<float>(softcap),
        |       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    204 |       window_left,
        |       ~~~~~~~~~~~~
    205 |       window_right,
        |       ~~~~~~~~~~~~~
    206 |       causal,
        |       ~~~~~~~
    207 |       use_sqrt_alibi,
        |       ~~~~~~~~~~~~~~~
    208 |       enable_cuda_graph,
        |       ~~~~~~~~~~~~~~~~~~
    209 |       false,
        |       ~~~~~~
    210 |       alibi_slopes_ptr,
        |       ~~~~~~~~~~~~~~~~~
    211 |       key_ptr,
        |       ~~~~~~~~
    212 |       value_ptr,
        |       ~~~~~~~~~~
    213 |       workspace_ptr,
        |       ~~~~~~~~~~~~~~
    214 |       merged_qkv,
        |       ~~~~~~~~~~~
    /usr/local/corex-4.3.8/include/ixinfer.h:3699:3: note: candidate constructor not viable: requires at most 27 arguments, but 28 were provided
    3699 |   PageAttentionWithKVCacheArguments(
        |   ^
    3700 |       float scale = 1.f, float k_scale = 1.f, float v_scale = 1.f,
        |       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    3701 |       float softcap = 0.f, int window_size_left = -1,
        |       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    3702 |       int window_size_right = -1, bool is_causal = false,
        |       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    3703 |       bool alibi_sqrt = false, bool enable_cuda_graph = false,
        |       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    3704 |       bool is_bbhh = false, const float *alibi_slopes_ptr = nullptr,
        |       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    3705 |       const void *key = nullptr, const void *value = nullptr,
        |       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    3706 |       void *workspace = nullptr, bool merge_qkv = false,
        |       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    3707 |       const float *rope_sin = nullptr, const float *rope_cos = nullptr,
        |       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    3708 |       const float *qScalePtr = nullptr, const float *kScalePtr = nullptr,
        |       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    3709 |       const float *vScalePtr = nullptr, const float *kScaleVec = nullptr,
        |       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    3710 |       int qLength = 1, int keyStride = 0, int valueStride = 0,
        |       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    3711 |       const void *aux = nullptr, const size_t rope_batch_stride = 0,
        |       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    3712 |       const cuinferAttentionRopeMode_t rope_type = CUINFER_ATTEN_NORMAL)
        |       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    /usr/local/corex-4.3.8/include/ixinfer.h:3666:8: note: candidate constructor (the implicit copy constructor) not viable: requires 1 argument, but 28 were provided
    3666 | struct PageAttentionWithKVCacheArguments {
        |        ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    /usr/local/corex-4.3.8/include/ixinfer.h:3666:8: note: candidate constructor (the implicit move constructor) not viable: requires 1 argument, but 28 were provided
    3666 | struct PageAttentionWithKVCacheArguments {
        |        ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    /home/aistudio/FastDeploy/custom_ops/iluvatar_ops/mixed_fused_attn.cu:269:37: error: no matching constructor for initialization of 'PageAttentionWithKVCacheArguments'
    269 |   PageAttentionWithKVCacheArguments args{
        |                                     ^   ~
    270 |       static_cast<float>(scale),
        |       ~~~~~~~~~~~~~~~~~~~~~~~~~~
    271 |       1.0,
        |       ~~~~
    272 |       1.0,
        |       ~~~~
    273 |       static_cast<float>(softcap),
        |       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    274 |       window_left,
        |       ~~~~~~~~~~~~
    275 |       window_right,
        |       ~~~~~~~~~~~~~
    276 |       causal,
        |       ~~~~~~~
    277 |       use_sqrt_alibi,
        |       ~~~~~~~~~~~~~~~
    278 |       enable_cuda_graph,
        |       ~~~~~~~~~~~~~~~~~~
    279 |       false,
        |       ~~~~~~
    280 |       nullptr,
        |       ~~~~~~~~
    281 |       decode_qkv_ptr,
        |       ~~~~~~~~~~~~~~~
    282 |       decode_qkv_ptr,
        |       ~~~~~~~~~~~~~~~
    283 |       decode_workspace_ptr,
        |       ~~~~~~~~~~~~~~~~~~~~~
    284 |       true,
        |       ~~~~~
    /usr/local/corex-4.3.8/include/ixinfer.h:3699:3: note: candidate constructor not viable: requires at most 27 arguments, but 28 were provided
    3699 |   PageAttentionWithKVCacheArguments(
        |   ^
    3700 |       float scale = 1.f, float k_scale = 1.f, float v_scale = 1.f,
        |       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    3701 |       float softcap = 0.f, int window_size_left = -1,
        |       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    3702 |       int window_size_right = -1, bool is_causal = false,
        |       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    3703 |       bool alibi_sqrt = false, bool enable_cuda_graph = false,
        |       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    3704 |       bool is_bbhh = false, const float *alibi_slopes_ptr = nullptr,
        |       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    3705 |       const void *key = nullptr, const void *value = nullptr,
        |       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    3706 |       void *workspace = nullptr, bool merge_qkv = false,
        |       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    3707 |       const float *rope_sin = nullptr, const float *rope_cos = nullptr,
        |       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    3708 |       const float *qScalePtr = nullptr, const float *kScalePtr = nullptr,
        |       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    3709 |       const float *vScalePtr = nullptr, const float *kScaleVec = nullptr,
        |       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    3710 |       int qLength = 1, int keyStride = 0, int valueStride = 0,
        |       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    3711 |       const void *aux = nullptr, const size_t rope_batch_stride = 0,
        |       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    3712 |       const cuinferAttentionRopeMode_t rope_type = CUINFER_ATTEN_NORMAL)
        |       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    /usr/local/corex-4.3.8/include/ixinfer.h:3666:8: note: candidate constructor (the implicit copy constructor) not viable: requires 1 argument, but 28 were provided
    3666 | struct PageAttentionWithKVCacheArguments {
        |        ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    /usr/local/corex-4.3.8/include/ixinfer.h:3666:8: note: candidate constructor (the implicit move constructor) not viable: requires 1 argument, but 28 were provided
    3666 | struct PageAttentionWithKVCacheArguments {
        |        ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    1 error generated when compiling for ivcore11.
    /home/aistudio/FastDeploy/custom_ops/iluvatar_ops/paged_attn.cu compile failed, command '/usr/local/corex/bin/clang++' failed with exit code 1
    /home/aistudio/FastDeploy/custom_ops/build/fastdeploy_ops/temp.linux-x86_64-cpython-310/build/fastdeploy_ops/temp.linux-x86_64-cpython-310/iluvatar_ops/paged_attn.cu.o is compiled
    1 error generated when compiling for ivcore11.
    /home/aistudio/FastDeploy/custom_ops/iluvatar_ops/mixed_fused_attn.cu compile failed, command '/usr/local/corex/bin/clang++' failed with exit code 1

   ```

   解决：使用 commit： 172ab6020dbe1ccb730f09df74764d6ea388d88f 重新编译

### 下周计划

1. 调试双卡环境

### 当前阻塞（无则填"无"）

- 重新编译 FastDeploy

### 交付物进展

| 交付物 | 状态 | 备注 |
|--------|:----:|------|
| RFC 文档 | ✅ 已完成 | - |
| 代码实现 | 🔄  | |
| README | 🔄  | - |
| 演示视频/截图 |🔄  | - |