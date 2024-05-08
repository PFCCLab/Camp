### 姓名

卢畅

### 实习项目

静态图半自动并行训练性能优化

### 本周工作

本周工作主要是编写 ZBV 编排代码，并在不同 memory limit 下进行测试以及将编排结果与官方实现对比。还对显存估计工具的问题进行了排查，并在不同配制下进行测试。

#### 1. 解决Backward 阶段峰值显存估计偏差的问题

在将 no_need_buffer 情况的 var 考虑之后，显存估计的结果和实际的峰值显存之间的差距有所缩小

#### 2. 在不同配置下估计显存

pp4, gradient accumulation 8, 开启 recompute,batch1, num_hidden_layers 4

![picture 28](images/70d541a3161c71488e1ebba7d6b87b2c2800dc8f5b8e627ce77eff13856c325d.png)  

pp4, gradient accumulation 8, 不开启 recompute,batch1, num_hidden_layers 4

![picture 29](images/d4008a1e1e2ce3faec71b8de7e121cfd672690d6addd719c2eb37ec5e3c6b3ba.png)  


pp2, mp2, gradient accumulation 8, 不开启 recompute,batch2, num_hidden_layers 4


![picture 30](images/c72cf5e377ec0b339825a0150d86dde2ef94f13cd33072cc2f3e098122ca4c6b.png)


#### 2. 编写 ZBV 编排代码

初步完成 ZBV 编排的代码编写

相关 PR：

- https://github.com/PaddlePaddle/Paddle/pull/63800

#### 3. 编排结果与官方实现对比

**1、vpp2 pp2 无内存限制结果对比**

**官方实现编排结果：**

 
![picture 4](images/13fb10df090c147535928d0e45d31e88d5c2e571211e962e2cac87e576329e69.png)  

**自己实现编排结果：**


![picture 2](images/5122265d16e9f1d5fff93230f9d8809cc007176e689ce1de582d277e69b87a9f.png)  

编排结果一致

**2、vpp2 pp2 内存限制 1p (和1f1b 一样的内存限制) 结果对比**

**官方实现编排结果：**

![picture 5](images/dbf67abd99bffc3d0016eaa3e4a6758f6071377f5f89abe652663aa2a369aaa8.png)  

**自己实现编排结果：**

![picture 6](images/f01272ea79d4bfd53643d873e53f686d67852a6dc7b7e125e3bbf145a1de7f06.png)  

编排结果一致

**3、vpp2 pp2 内存限制 1.5p 结果对比**

**官方实现编排结果：**

![picture 7](images/c1d7bd415cbccc288e2a3fe40d69a3febd550fcb4c66d02650ff9929f356d56e.png)  

**自己实现编排结果：**

![picture 8](images/e2f88a2518aa32db69af49bd642bbc412fd4ae02a832e3b6924caa1dbe64c718.png)  

编排结果一致

**4、vpp2 pp2 内存限制 2p 结果对比**

**官方实现编排结果：**

![picture 9](images/ef8963233f2d5c07302e97c004c096ac5340802234d432cd489b6e5291ff47c9.png)  

**自己实现编排结果：**

![picture 10](images/6eb10ea894e23df378f805443dd868077420e729b1c67ae1a9ae180f7fe8c8aa.png)

**5、vpp2 pp4 无内存限制 结果对比**

**官方实现编排结果：**

![picture 12](images/ebc5f68326269498e5435095909e5d0669bb977e8482f00fd8c9d5d3139f607c.png)  

**自己实现编排结果：**

![picture 13](images/6a5eb94fbb5230470e93b6a33706130efa8f191fd739856f9b11cad1b7af701d.png)  

编排结果一致

**6、vpp2 pp4 1p 内存限制 结果对比**

**官方实现编排结果：**

![picture 14](images/e7b366779487856a43a6f3b3ebb94b08f91e4769a38cbf0da7d7ca8eb7475869.png)  


**自己实现编排结果：**

![picture 15](images/9b086d6450f816993cb2680ecad353b56001cecd4e93a0196fc41d3a45b8c832.png)  

编排结果一致

**7、vpp2 pp4 1.5p 内存限制 结果对比**

**官方实现编排结果：**

![picture 16](images/cd07d134b03bcc7d101423fe5a96eb92e3aa40e016584c1a3a354d4b826b4f54.png)

**自己实现编排结果：**

![picture 17](images/68f0c97ba8e940ee19e9b8f8f1f07fff227494f5e27b74d8f7db82955c71fd16.png)  


**8、vpp2 pp4 2p 内存限制 结果对比**


**官方实现编排结果：**

![picture 11](images/069f287d5163a6ace59f421ae2afb75ea7316c72b8bea94de208cb8021353017.png)  

**自己实现编排结果：**

![picture 18](images/e769db5a02af0a463c5ac964552424e21b834bab8c4db4ebc9dfef7347538911.png)  

编排结果一致

测试结果表明，自己实现的编排结果与官方实现的编排结果一致。由于实现还适配了 vpp_degree > 2 的情况，官方没有实现，所以在这种情况下，只能用自己的实现进行对比。

**9、vpp2 pp8 microbatches 16 无内存限制 结果对比**

**官方实现编排结果：**

![picture 23](images/aab66e7a86a970e797a7c2261861ed0fc9cf146b2ff9653e0847f6239cd9ecfa.png)  


**自己实现编排结果：**

![picture 22](images/059f6d8856a27ff87b366a62e6710f5c0fefa022a9a7f1f3a793e254e1b98182.png)  

编排结果略微有一些不一致，这是由于我们的实现中调整了 backward_b 之前 forward 的插入策略。官方的实现会限制 forward 的数量，但是我们认为只要满足显存限制，forward 的数量可以更多。

官方实现的 bubble rate 为 1.25%，我们的实现的 bubble rate 为 1.15%。

**10、vpp2 pp8 microbatches 16 1p 内存限制 结果对比**

**官方实现编排结果：**

![picture 25](images/1933e990d213324cf58a78bf820633263f889c9ff80885eeff101a666146fe67.png)  


**自己实现编排结果：**

![picture 24](images/416fadf54fb938c1855b93285edba1228ae799a8374f1ca7f9e2f15369eec7e5.png)  

这里编排结果不一致，但是推测是官方实现的 bug，在这样样例里面 max_mem 是 32，每个 forward 的显存是 2，但是官方实现的编排结果中，有 17 个 forward，这样的话显存就超了。我们的实现是 16 个 forward，显存是 32，所以是满足显存限制的。

**11、vpp2 pp8 microbatches 16 1.5p 内存限制 结果对比**

**官方实现编排结果：**

![picture 27](images/12c2128e00c0f54c270e69d034890f12278b595f7b674aa62aa14e1a7ae09e18.png)  

**自己实现编排结果：**

![picture 26](images/e7d1381f0f8d9770044c20a7166007a42266e4244a4a5ae273b757af6bf68b93.png)  

这里编排结果不一致，原因和无内存限制的情况一样，官方实现的 bubble rate 为 1.25%，我们的实现的 bubble rate 为 1.15%。

### 下周工作

适配 vpp_degree > 2 的情况，完成 ZBV 编排代码的编写。修改分布式标记适配 ZBV 的 V 形编排。在 Llama2 上进行初步性能测试。

### 导师点评
