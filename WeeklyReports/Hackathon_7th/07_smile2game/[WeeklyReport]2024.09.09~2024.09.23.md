### 姓名
刘卉杰

### 实习项目
自动并行张量切分机制预研&建设

### 本周工作

1. 学习jeff提交的 s_to_r case下的不均匀切分的pr，并调研其余cases

参考链接 [67756pr](https://github.com/PaddlePaddle/Paddle/pull/67756)

        * 阅读 base_reshard_func.py,了解ReshardFunction基本类,需要我们实现is_suitable和reshard的
        * 阅读 s_to_r_reshard_func.py:
                1. SToRReshardFunction.reshard()
                  1.1. padding 不均匀需要先padding
                  1.2. reshard_s_to_r_with_padding 具体怎么通信得到复制，并去除padding
                2. SToRReshardFunctionCrossMesh.reshard()
                  1.1 先用 SameStatusReshardFunction() 
                  1.2 在用 SToRReshardFunction.reshard()
        * 源码编译之后，跑一下test


2. 进行code-reading和学习，参考链接 [code-reading](https://github.com/PaddlePaddle/community/tree/master/pfcc/paddle-code-reading)

        * 学习PIR机制的概念
            * 了解多层级Dialect
            * 了解Pass体系 
        * 学习自动并行机制
            * 了解动手、静手、自动并行方式（切分推导-切分转换）
            * 了解分布式张量的三种 placements 和 ProcessMesh
            * 了解了reshard的含义和多种case
            * 了解了自动并行和分布式策略：数据并行，张量并行，流水线并行，3D混合并行

      

3. **问题疑惑与解答**

        * s-to-r的情况,是说shard状态是被不均匀切分了吗？这里的s-to-r的src value本身就是不均匀的,那这是哪里来的？
        答：xxx
        * 目前s-to-r的不均匀切分,Processmesh的dimNum还是1，多重切分指的是后面的 crossmesh吗？
        答：xxx
        * 目前是不是只有 s-to-r实现了这个不均匀切分，其余情况p-r,p-s,r-p,r-s,是否也需要实现不均匀切分？
        答：xxx
        * tmp_src_type = paddle.base.libpaddle.pir.cvt_to_dist_type不太明白为什么需要这样做？
        答：好像是为了解决静态图的问题，以及后面的op_dist_attribute。还需要再学一下pir以及get_defining_op()
        * 这些程序，执行时候就和cuda并行一样，每个device上获得相同的代码，根据rank来实现不同的操作吗？
        答：xxx
        * 问题出现的动机是，不均匀时候没法直接用all_gather吗？
        答：xxx




### 下周工作

1. 尝试 r-to-s的不均匀切分实现
2. 尝试 s-to-r的多重切分实现


### 导师点评
请联系导师填写
