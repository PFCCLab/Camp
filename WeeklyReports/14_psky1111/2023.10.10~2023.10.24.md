
### 姓名
宋铠玉
### 实习项目
项目十四：Clas 套件全流程建设

### 本周工作

1. 修复swin transformer 以及 CLIP 的Vision transformer模块无法兼容多分辨率问题.

	* 初步修复多分辨率问题. 核心代码
    ```python
    def pading_for_not_divisible(pixel_values,
                             height,
                             width,
                             patch_size,
                             format="BCHW",
                             function="split"):
    if isinstance(patch_size, int):
        patch_size = (patch_size, patch_size)
    if height // patch_size[0] == 0 and width // patch_size[1] == 0:
        return pixel_values, (0, 0, 0, 0, 0, 0, 0, 0)
    if function == "split":
        pading_width = patch_size[1] - width % patch_size[1]
        pading_height = patch_size[0] - height % patch_size[0]
    elif function == "merge":
        pading_width = width % 2
        pading_height = height % 2
    if format == "BCHW":
        pad_index = (0, 0, 0, 0, 0, pading_height, 0, pading_width)
    elif format == "BHWC":
        pad_index = (0, 0, 0, pading_height, 0, pading_width, 0, 0)
    else:
        assert ("vaild format")

    return F.pad(pixel_values, pad_index), pad_index
    ```
    * 遗留:目前的修复会导致在使用原有224分辨率训练时,产生而外的计算开销以及存储代价,同时由于type问题不支持amp. 需要进一步完善优化


2. 调研视觉模型以及前向对齐.

	* 完成对视觉模型的调研,与导师对齐. 确定前向对齐的工作为:LaCLIP react UNICOM

3. **问题疑惑与解答**

    * 无


### 下周工作

1. 针对阶段1任务, 修复遗留问题.
2. 针对阶段2任务, 完成调研模型并前向对齐.
3. 与导师对齐阶段3所需完成训练对齐的模型

### 导师点评
