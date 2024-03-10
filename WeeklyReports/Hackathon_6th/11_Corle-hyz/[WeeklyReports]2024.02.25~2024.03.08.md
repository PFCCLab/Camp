### 姓名
何咏哲

### 实习项目
全自动并行架构升级

### 本周工作

1. **调研vPipe工作**

	《[vPipe: A Virtualized Acceleration System for Achieving Efficient and Scalable Pipeline Parallel DNN Training](https://ieeexplore.ieee.org/document/9472938/)》是一个使用动态训练策略进行神经网络搜索的系统。

  * 神经结构搜索(Neural architecture search, NAS)是一种自动化设计人工神经网络(artificial Neural network, ANN)的技术，是机器学习领域中广泛使用的模型。NAS与超参数优化和元学习密切相关，是自动化机器学习(AutoML)的一个子领域。
    
  * 两个目标
    1. G1：管理显存防止OOM；
    2. G2：balanced partition。
       
  * 这篇文章提出来的方法是
    1. 对于G1：swap和recompute。swap指offload到CPU显存；
    2. 对于G2：使用online generated partition plan，将layer从intense的stage迁移到临近stage。
       
  * 该方法面临两个挑战
    1. 对swap、recompute、repartition(SRP)空间的搜索；
    2. 在迁移层的同时保持对一般上层PP系统透明，即不会向上层系统增加或减少参数过时性。
       
  * 相应的解决办法
    1. 通过两个observation构建了一个快速收敛的接近最优的算法：迭代地将layer迁移到相邻阶段；典型的复杂神经网络通常是重复子图组成的；
    2. 激活生成(在向前传递中)与其最终使用(在相应的向后传递中)之间的时间窗口允许VPIPE在不改变上层系统参数的情况下透明地实时迁移层的微妙交错。


2. **讨论异构环境下的全自动并行方案**

  延续第五期飞桨护航计划集训营的工作，将之前建立的显存模型和全自动并行系统应用到异构环境下。
  * 需要在原有并行模式的基础上，完善对Recompute、Sharding搜索空间的支持。
  * 需要提出一些经验策略进行启发式搜索，进一步缩小搜索空间。

3. **问题疑惑与解答**


	* 异构和同构除了显存的区别外还有什么不同？

        答：异构资源的算力甚至算子的实现方式也存在显著差异。异构资源的算力与显存并不存在一个直接的比例关系，因此将原有的并行模式部署到异构环境下时，除了需要保证显存不OOM，还需要尽可能地使负载均衡，达到一个比较理想的训练效率。同构其实可以说是异构的一种特例。



### 下周工作

1. 继续思考原本的全自动并行方案在异构环境下需要改进的地方。
2. 提出一些经验策略进行启发式搜索，进一步缩小搜索空间。

### 导师点评

