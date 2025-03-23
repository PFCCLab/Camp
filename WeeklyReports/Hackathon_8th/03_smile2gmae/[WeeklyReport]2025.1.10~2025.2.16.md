### 姓名

刘卉杰

### 实习项目

自动并行切分转换和专家并行机制完善

### 本周工作



1. 扩展了 _reshard_mesh_shape对Partial的测试(原有Replicate)
2. 扩展了 _reshard_mesh_shape对Shard的部分_local_value不变的情况的测试，改进了_only_reshard_mesh_shape判断函数

代码对Paddle的修改部分和实验测试在我的github托管仓库 [Moe/pd-dist at main · smile2game/Moe。](https://github.com/smile2game/Moe/tree/main/pd-dist)



针对Shard的_only_reshard_mesh_shape具体修改和原理：

- 属于only_reshard_mesh_shape

1.   

   1. src_mesh的切分，实际上第二刀没有切出来，因为2x1的1切了和没切是一样的，dst_mesh是[2]。我所补充在_only_reshard_mesh_shape中补充的也是针对这种的情况


<br/>

- 不属于的情况

1. [[0], [1]] Shard(0),Shard(1) --> [[0,1]] Shard(0) Shard(1) 

   1. 按行切分变成按列切分了


<br/>

- 未覆盖的情况

1. [[0], [1]] Shard(0),Shard(0) --> [0,1] Shard(0)

   1. 目前这种mesh在dim_0同时切两刀，会报warning： not supported


```python
src_len = len(src_placements)
dst_len = len(placements)
print(f"src_mesh.shape[1] is {src_mesh.shape[1]}")
if src_len >= dst_len:
    print(f"src_len is {src_len},dst_len is {dst_len}")
    for i in range(dst_len):
        if src_mesh.shape[i] != mesh.shape[i]:
            return False
    for i in range(dst_len,src_len):
        if src_mesh.shape[i] != 1:
            return False
else:
    for i in range(src_len):
        if src_mesh.shape[i] != mesh.shape[i]:
            return False
    for i in range(src_len,dst_len):
        if dst_mesh.shape[i] != 1:
            return False
```





### 存在的问题

_only_reshard_mesh_shape的完备性还需要和老师继续确认

### 下周工作

1. 继续完善 _reshard_mesh_shape的情况



### 导师点评

通过

