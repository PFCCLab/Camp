### 姓名
刘卉杰

### 实习项目
自动并行张量切分机制预研&建设

### 本周工作

1. 开发 `p_to_s_reshard_func.py`,代码全局尺寸修正：

reduce_scatter:
```python
dst_value = paddle._C_ops.reduce_scatter(
            src_value, group.id, len(src_dist_attr.process_mesh.process_ids)
        )
        out_global_shape = dst_value.shape
        out_global_shape[split_axis] = (
            padding_num + out_global_shape[split_axis]
        )
        out_global_shape[split_axis] = (
            padding_num + out_global_shape[split_axis]
        )
        dst_tmp_type = paddle.pir.create_shaped_type(
            dst_value.type(), out_global_shape
        )
        dst_tmp_type = paddle.base.libpaddle.pir.cvt_to_dist_type(
            dst_tmp_type, dst_dist_attr
        )
```
split:
```python
dst_value = paddle._C_ops.split(
                    dst_value,
                    [
                        dst_value.shape[split_axis] - padding_num,
                        padding_num,
                    ],
                    0,
                )[0]
```

2. pr描述修正

代码暂时都存放在我fork下的github仓库，链接为[个人fork下仓库](https://github.com/smile2game/Paddle/tree/note/unittest)

3. 代码风格修正

```
pip isntall pre-commit
pre-commit run --files python/paddle/distributed/auto_parallel/static/reshard_funcs/p_to_s_reshard_func.py \
                    test/auto_parallel/pir/pir_reshard_p_to_s.py \
                    test/auto_parallel/pir/test_pir_reshard_p_to_s.py
```
4.提交pr
```
git add .
git commit --amend --no-edit 
git push --force
```
pr链接:https://github.com/PaddlePaddle/Paddle/pull/69265



### 下周工作

1. 确保 p_to_s的pr能成功合入
2. 开始 r_to_s_reshard_func.py实现
3. 找老师咨询多重切分相关pr进行学习和开发



### 导师点评
通过
