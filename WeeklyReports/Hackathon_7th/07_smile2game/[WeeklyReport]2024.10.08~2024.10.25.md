### 姓名
刘卉杰

### 实习项目
自动并行张量切分机制预研&建设

### 本周工作

1. 开发 `p_to_s_reshard_func.py`
        创建了静态图下的p_to_s_reshard_func.py,并在其中参考着s_to_r_reshard_func.py编写了逻辑为
        if balanced:
                reduce_scatter
        else:
                padding
                reduce_scatter
                split
        
        目前存在的问题：
        (1) reduce_scatter返回尺寸不对，如 我希望4 x 7的partial张量，在 0维度，变成 2 x 7 - 2 x 7 的shard张量(global shape还是4 x 7)，但是目前返回 global shape是 2 x 7的张量

2. 参考s_to_r的单测，编写p_to_s单测`p_to_s_unittest.py`和`reshard_p_to_s.py`并能够跑通

代码暂时都存放在我fork下的github仓库，链接为[个人fork下仓库](https://github.com/smile2game/Paddle/tree/note/unittest)


### 存在的问题
reduce_scatter返回尺寸不对，如 我希望4 x 7的partial张量，在 0维度，变成 2 x 7 - 2 x 7 的shard张量(global shape还是4 x 7)，但是目前返回 global shape是 2 x 7的张量

### 下周工作

1. 修复目前 p_to_s_reshard_func.py存在的问题
2. 开始 r_to_s_reshard_func.py实现



### 导师点评
通过
