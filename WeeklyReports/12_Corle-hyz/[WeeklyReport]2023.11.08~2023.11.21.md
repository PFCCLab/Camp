### 姓名

何咏哲

Github ID：[Corle-hyz](https://github.com/Corle-hyz)

### 实习项目

[全自动并行架构升级](https://github.com/PaddlePaddle/community/blob/master/hackathon/hackathon_5th/%E3%80%90PaddlePaddle%20Hackathon%205th%E3%80%91%E9%A3%9E%E6%A1%A8%E6%8A%A4%E8%88%AA%E8%AE%A1%E5%88%92%E9%9B%86%E8%AE%AD%E8%90%A5%E9%A1%B9%E7%9B%AE%E5%90%88%E9%9B%86.md#%E9%A1%B9%E7%9B%AE%E5%8D%81%E4%BA%8C%E5%85%A8%E8%87%AA%E5%8A%A8%E5%B9%B6%E8%A1%8C%E6%9E%B6%E6%9E%84%E5%8D%87%E7%BA%A7)

### 本周工作

**建立了分布式训练的Llama-1显存模型，包括以下几个部分**

#### 1. 张量并行（Tensor Parallelism）
##### How TP
![image.png](https://cdn.nlark.com/yuque/0/2023/png/22927810/1700355323987-c08e97b0-0b18-40e1-87b4-445ba1decae9.png#averageHue=%23f5f5f4&clientId=udb044a1c-b187-4&from=paste&height=412&id=u162928e4&originHeight=824&originWidth=2182&originalType=binary&ratio=2&rotation=0&showTitle=false&size=296078&status=done&style=none&taskId=u57aa953d-a053-449c-a9f4-13df52fc721&title=&width=1091)<br />张量并行引入了两个新的算子，其中![](https://cdn.nlark.com/yuque/__latex/18f3c2855f0e85a1ac2257f64d917144.svg#card=math&code=f&id=n5MYz)算子在前向没有操作、在反向All-Reduce；![](https://cdn.nlark.com/yuque/__latex/39014b9c76fb5402749c3fff8a571744.svg#card=math&code=%5Coverline%7Bf%7D&id=IFja6)算子在前向All-Reduce、在反向没有操作<br />下面这些块的输入激活(例如输入到Q、K和V矩阵的乘法或输入到h→4h线性层)没有并行化，并且只有每个块内的激活在张量并行组中被划分<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/22927810/1700356239223-dcc5f2d0-8892-4585-9af5-e37342296c3f.png#averageHue=%23f7f6f6&clientId=udb044a1c-b187-4&from=paste&height=575&id=uc54e8b6d&originHeight=1149&originWidth=1500&originalType=binary&ratio=2&rotation=0&showTitle=false&size=267637&status=done&style=none&taskId=ucac36cfd-a106-4e82-9698-28b0872c335&title=&width=750)
##### Summary TP
在Transformer中，上面这几项的激活内存是没有被Tensor Parallelism切分的，共10sbh，所以Transformer考虑了Tensor Parallelism的激活内存为![](https://cdn.nlark.com/yuque/__latex/8c8d7c8f2848fdae1499184adbf9b704.svg#card=math&code=10sbh%2B%5Cfrac%7B24sbh%7D%7Bt%7D%2B%5Cfrac%7B5as%5E2b%7D%7Bt%7D&id=XaLF1)<br />那么对应到Llama中的话：

- Normalize的变化不影响
- ReLU替换成SwiGLU，影响MLP模块中的ReLU（GeLU）及其后面的Linear层，都在Tensor Parallelism的作用范围之内
- RoPE的变化不影响

所以考虑了Tensor Parallelism后Llama单个Transformer Layer的激活内存为<br />![](https://cdn.nlark.com/yuque/__latex/103eda16016e1e923f62072880cefb22.svg#card=math&code=10sbh%2B%5Cfrac%7B56sbh%7D%7B3t%7D%20%2B%20%5Cfrac%7B5as%5E2b%7D%7Bt%7D&id=P3MsU)


#### 2. 序列并行（Sequence Parallelism）
##### Why SP
TP并行化了在训练过程中花费最多时间的那部分Transformer Layer，因此它的计算效率很高。然而LayerNorm以及Attention和MLP块之后的dropout仍然在张量并行组中被复制。这些元素不需要大量的计算，但需要相当数量的激活内存。定量地说，10sbh部分是由于这些复制操作，因此它们没有被张量并行大小t所除。
##### How SP
在Transformer Layer的非TP区域，操作沿sequence维度是独立的。这个特性允许我们沿着序列维度s划分这些区域。这种额外的Parallel在![](https://cdn.nlark.com/yuque/__latex/e06d4f3372b4dde4686df5b2e5f5ea00.svg#card=math&code=%7Bf%7D&id=ZCmfG)之前和![](https://cdn.nlark.com/yuque/__latex/39014b9c76fb5402749c3fff8a571744.svg#card=math&code=%5Coverline%7Bf%7D&id=qf6gc)之后引入了新的通信集体，它们将作为序列和张量并行区域之间的转换器。例如，在Forward中，我们需要在![](https://cdn.nlark.com/yuque/__latex/e06d4f3372b4dde4686df5b2e5f5ea00.svg#card=math&code=%7Bf%7D&id=wj0ma)之前进行额外的All-Gather。这些额外的交流带来了额外的开销，并且会减慢训练的速度。<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/22927810/1700358442365-51d34961-7d0a-4a98-8fe8-5b601f14b13b.png#averageHue=%23e8deb6&clientId=u2638a3ab-7b46-4&from=paste&height=400&id=u86ecbcd2&originHeight=800&originWidth=2182&originalType=binary&ratio=2&rotation=0&showTitle=false&size=391349&status=done&style=none&taskId=u24ba0285-ee91-4068-8ac0-89afc2ada31&title=&width=1091)<br />将这些操作与![](https://cdn.nlark.com/yuque/__latex/e06d4f3372b4dde4686df5b2e5f5ea00.svg#card=math&code=%7Bf%7D&id=fGY9m)和![](https://cdn.nlark.com/yuque/__latex/39014b9c76fb5402749c3fff8a571744.svg#card=math&code=%5Coverline%7Bf%7D&id=YbMrt)结合得到了新的操作![](https://cdn.nlark.com/yuque/__latex/62c47f7701a93a31d03688893e810324.svg#card=math&code=%7Bg%7D&id=z7QbA)和![](https://cdn.nlark.com/yuque/__latex/1804bf77948962d571e65beefb8f2308.svg#card=math&code=%5Coverline%7Bg%7D&id=vCtxJ)。<br />![下标表示沿着加速器的切分，上标表示这个切分的维度（sequence、batch、hidden、column、row）](https://cdn.nlark.com/yuque/0/2023/png/22927810/1700359139824-0f0dfbae-2335-48c6-92f5-d0795160b9f3.png#averageHue=%23eae0c4&clientId=u2638a3ab-7b46-4&from=paste&height=446&id=ue1eda9b1&originHeight=1036&originWidth=2516&originalType=binary&ratio=2&rotation=0&showTitle=true&size=356149&status=done&style=none&taskId=u4031c71a-5f5d-4405-9f74-5d1b2b4c982&title=%E4%B8%8B%E6%A0%87%E8%A1%A8%E7%A4%BA%E6%B2%BF%E7%9D%80%E5%8A%A0%E9%80%9F%E5%99%A8%E7%9A%84%E5%88%87%E5%88%86%EF%BC%8C%E4%B8%8A%E6%A0%87%E8%A1%A8%E7%A4%BA%E8%BF%99%E4%B8%AA%E5%88%87%E5%88%86%E7%9A%84%E7%BB%B4%E5%BA%A6%EF%BC%88sequence%E3%80%81batch%E3%80%81hidden%E3%80%81column%E3%80%81row%EF%BC%89&width=1084 "下标表示沿着加速器的切分，上标表示这个切分的维度（sequence、batch、hidden、column、row）")<br />layer-norm的输入沿sequence并行，因此layer-norm的输出也将沿sequence维度并行。具有GeLU的linear层需要整个输入Y，因此我们需要执行all-gather。这意味着g是Forward中沿序列维度的all-gather操作。<br />通过将A沿着它的列(![](https://cdn.nlark.com/yuque/__latex/8709564dbc6ed6cfd0995e4abc12bfdd.svg#card=math&code=A_1%5Ec&id=BxA7r)和![](https://cdn.nlark.com/yuque/__latex/437c5f4be1b0973445300d8623e09315.svg#card=math&code=A_2%5Ec&id=Uam6B))、B沿着它的行(![](https://cdn.nlark.com/yuque/__latex/e0cd882ef401a698c514d131b3ff4c85.svg#card=math&code=B_1%5Er&id=CvhYW)和![](https://cdn.nlark.com/yuque/__latex/dcc0c69897a54626e90f69b8a1af91de.svg#card=math&code=B_2%5Er&id=CInOp))分开，我们避免了通信就得到了W1和W2。这两个张量不再是并行的，在它们被输入到dropout层之前需要求和为W=W1+W2。然而，dropout需要其输入在序列维度s上是并行的。我们将这两个操作组合成一个reduce-scatter操作，而不是在序列维度上求和然后并行化。因此，在前向通道中，![](https://cdn.nlark.com/yuque/__latex/1804bf77948962d571e65beefb8f2308.svg#card=math&code=%5Coverline%7Bg%7D&id=oQTra)可以是一个单一的reduce-scatter操作。<br />上述过程可以写作公式<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/22927810/1700360783936-658e3134-f323-47b8-81c9-013de452501b.png#averageHue=%23f3f3f3&clientId=ud0d5e619-936b-4&from=paste&height=238&id=u964439ca&originHeight=476&originWidth=1022&originalType=binary&ratio=2&rotation=0&showTitle=false&size=84107&status=done&style=none&taskId=u95b02f7c-e2cd-4df5-aff0-770ceb82d56&title=&width=511)<br />如果我们对Backward进行类似的分解，我们会发现![](https://cdn.nlark.com/yuque/__latex/62c47f7701a93a31d03688893e810324.svg#card=math&code=%7Bg%7D&id=ZuMYO)和![](https://cdn.nlark.com/yuque/__latex/1804bf77948962d571e65beefb8f2308.svg#card=math&code=%5Coverline%7Bg%7D&id=hQ82E)是彼此共轭的。![](https://cdn.nlark.com/yuque/__latex/62c47f7701a93a31d03688893e810324.svg#card=math&code=%7Bg%7D&id=JUNLA)为Forward的All-Gather，Backward的Reduce-Scatter，而![](https://cdn.nlark.com/yuque/__latex/1804bf77948962d571e65beefb8f2308.svg#card=math&code=%5Coverline%7Bg%7D&id=NVxSp)为Forward的Reduce-Scatter，Backward的All-Gather。<br />对 Transformer中Attention前面的layer-norm进行类似的分解。<br />张量并行需要在单个Forward和Backward中进行4次All-Reduce，而张量+序列并行需要在单个Forward和Backward中进行4次All-Gather和4次Reduce-Scatter。而All-Reduce=Reduce-Scatter+All-Gather，因此通信总量是一样的。
##### Summary SP
从上面的方程中，TP+SP除第一个linear操作所需的张量![](https://cdn.nlark.com/yuque/__latex/6204886f5cc39a4b860ea98a7e95af1d.svg#card=math&code=Y&id=cQGA3)外，将其他所有的激活分开。为了缓解这个问题，我们不存储向后传递的完整张量![](https://cdn.nlark.com/yuque/__latex/6204886f5cc39a4b860ea98a7e95af1d.svg#card=math&code=Y&id=EAtW7)。相反，我们只将![](https://cdn.nlark.com/yuque/__latex/4b54267f270653504ddc065d775e1eeb.svg#card=math&code=Y_i%5Es&id=MsOMi)部分存储在第i个TP rank中，并在Backward时执行额外的all-gather。为了消除这种额外的all-gather带来的延迟，我们将这种通信与计算相对于Y的梯度所需的计算重叠，从而减少了开销。<br />所以考虑了TP+SP后，Transformer的激活内存为![](https://cdn.nlark.com/yuque/__latex/d9c4770a79a0d8bed8be67f67d65522b.svg#card=math&code=%5Cfrac%7B10sbh%7D%7Bt%7D%2B%5Cfrac%7B24sbh%7D%7Bt%7D%2B%5Cfrac%7B5as%5E2b%7D%7Bt%7D%20%3D%20%5Cfrac%7B34sbh%7D%7Bt%7D%2B%5Cfrac%7B5as%5E2b%7D%7Bt%7D&id=obFUs)<br />同理，因为TP+SP将所有的层都沿着TP组切分了（如果![](https://cdn.nlark.com/yuque/__latex/6204886f5cc39a4b860ea98a7e95af1d.svg#card=math&code=Y&id=RoOqk)也按照上述方法切分的话），那么

考虑了Tensor Parallelism + Sequence Parallelism的Llama单个Transformer Layer的激活内存为<br />![](https://cdn.nlark.com/yuque/__latex/d49216b130965649683f71137f174e8f.svg#card=math&code=%5Cfrac%7B1%7D%7Bt%7D%28%5Cfrac%7B86sbh%7D%7B3%7D%2B5as%5E2b%29&id=tTaHA)<br />如果使用![](https://cdn.nlark.com/yuque/__latex/788df1ba344b3092def7590d1be6b4d4.svg#card=math&code=%5Csigma&id=GTIdY)来表示是否开启Sequence Parallelism的话（使用Sequence Parallelism则![](https://cdn.nlark.com/yuque/__latex/a24acba0a780556cd21fad4a7b5ad9ac.svg#card=math&code=%5Csigma%3D1%0A&id=jnFFt)，不使用Sequence Parallelism则![](https://cdn.nlark.com/yuque/__latex/7254509f0e5ec75d00dd174887e2e6c0.svg#card=math&code=%5Csigma%3D0&id=e7ZZp)），那么公式可以写作<br />![](https://cdn.nlark.com/yuque/__latex/38f3e4c6b8d05a6dc186fe70d3d282db.svg#card=math&code=10sbh%5Cfrac%7B%5Csigma-%5Csigma%20t%2Bt%7D%7Bt%7D%2B%5Cfrac%7B56sbh%7D%7B3t%7D%20%2B%20%5Cfrac%7B5as%5E2b%7D%7Bt%7D%0A%3D%5Cfrac%7B1%7D%7Bt%7D%5C%7B%5B10%28%5Csigma-%5Csigma%20t%2Bt%29%2B%5Cfrac%7B56%7D%7B3%7D%5Dsbh%2B5as%5E2b%5C%7D&id=XH3AR)


#### 3. 流水线并行（Pipeline Parallelism）
##### 1F1B Pipeline Parallelism
Pipeline Parallelism意味着每个device需要存储L/p层Transformer Layer，L表示模型中总的Transformer层数，p表示Pipeline Parallelism degree。<br />在PipeDream提出的1F1B中，第1个stage需要承担最大的内存压力，为了减少idle时间、充分发挥流水线的性能，第1个stage需要存储p个microbatch的激活内存。所以对于stage 1所在的device来说，需要存储的激活内存为![](https://cdn.nlark.com/yuque/__latex/682976e588e6ed00fc0d2abeb6d352ae.svg#card=math&code=%5Cfrac%7BL%7D%7Bp%7D%5Ctimes%20p%20%3D%20L&id=XAOYp)层的激活内存，从结果上来看并没有减少峰值激活内存。所以即使考虑1F1B也不会对上一节的公式造成影响。
##### Interleaved 1F1B Pipeline Parallelism / VPP
用m表示interleaving stage/vpp stage的话，stage 1只需要存储![](https://cdn.nlark.com/yuque/__latex/c453845b5b41a652ffd647e659f773d1.svg#card=math&code=L%281%2B%5Cfrac%7Bp-1%7D%7Bpm%7D%29&id=xtSjp)层的激活内存
##### Summary PP
把1F1B看作是m=1的Interleaved 1F1B，不使用流水线并行时p=1，那么stage 1需要存储的层数为![](https://cdn.nlark.com/yuque/__latex/4fccba2e472d03e6e2a0e0d4a2ea97f0.svg#card=math&code=L%281%2B%5Cdelta_%7Bm%5Cneq1%7D%5Cfrac%7Bp-1%7D%7Bpm%7D%29&id=y4d5s)，其中![](https://cdn.nlark.com/yuque/__latex/c68b07a61417c32e359c58767101129d.svg#card=math&code=m%5Cneq1&id=UExUR)时![](https://cdn.nlark.com/yuque/__latex/0cf79ec7192d3798bd99aa1dc4d343b5.svg#card=math&code=%5Cdelta_%7Bm%5Cneq1%7D&id=SXSRU)为1，否则为0

考虑了Pipeline Parallelism的Llama激活内存为<br />![](https://cdn.nlark.com/yuque/__latex/395183bbbcddb4d7f0ae0f6b45de09ed.svg#card=math&code=%281%2B%5Cdelta_%7Bm%5Cneq1%7D%5Cfrac%7Bp-1%7D%7Bpm%7D%29%5Cfrac%7BL%7D%7Bt%7D%5C%7B%5B10%28%5Csigma-%5Csigma%20t%2Bt%29%2B%5Cfrac%7B56%7D%7B3%7D%5Dsbh%2B5as%5E2b%5C%7D&id=EmVSS)<br />![](https://cdn.nlark.com/yuque/__latex/788df1ba344b3092def7590d1be6b4d4.svg#card=math&code=%5Csigma&id=UY65p)表示是否开启Sequence Parallelism


#### 4. 切片（Sharding）
Sharding类似于DeepSpeed的ZeRO，不同点在于DeepSpeed的ZeRO和Data Parallelism其实是一个维度，叫做ZeRO-DP，而Paddle的Sharding则可以和DP分别配置。相当于在内层先做一次ZeRO-DP，外层再做一次DP。
##### Sharding Degree
Paddle的Sharding并不是将所有的GPU都用于放置参数切片的，因为节点间的通信非常花时间。假设我们有4个8卡V100的节点，如果全部放在同一sharding 的parallelism里的话，那就需要在32个设备间进行broadcast和All-Reduce，且为跨节点通信，开销巨大。<br />如果开启Sharding-hybrid-dp的话，这时候我们可以设置sharding_group_size = 8，即节点内的8卡组成一个完整的sharding，之需要在节点内broadcast就行，然后再在四个节点之间对rank相同的gpu进行All-Reduce，这样做可以有效减少跨节点通信。<br />hybrid dp 是因为 Sharding parallelism 本身内含一层 data parallelism 逻辑， hybrid dp 是在 Sharding parallelism之上再增加新的一层 data parallelism 逻辑。关系式为<br />![](https://cdn.nlark.com/yuque/__latex/2e27f51ebebf77779f70c6f39150e023.svg#card=math&code=DP.degree%5Ctimes%20TP.degree%5Ctimes%20PP.degree%5Ctimes%20Sharding.degree%20%3D%20%5C%23GPUs&id=yCfEh)<br />参考资料：[Paddle 的混合并行 / Sharding / DP策略笔记](https://zhuanlan.zhihu.com/p/371566942)
##### Sharding Stage
Sharding可以切片放置的有三种内存数据：

- 优化器状态（Optimizer State）
- 梯度（Gradient）
- 参数（Parameter）

Sharding给的三个选Stage分别对应：

- Stage 1: os
- Stage 2: os_g
- Stage 3: os_g_p

Ref:[Paddle/python/paddle/distributed/sharding/group_sharded.py at develop · PaddlePaddle/Paddle](https://github.com/PaddlePaddle/Paddle/blob/develop/python/paddle/distributed/sharding/group_sharded.py#L40)
#####  Summary Sharding
用![](https://cdn.nlark.com/yuque/__latex/72cb3a229067770aeb6caa625a65a1a1.svg#card=math&code=r&id=EenhI)表示Sharding Degree（不使用Sharding时![](https://cdn.nlark.com/yuque/__latex/72cb3a229067770aeb6caa625a65a1a1.svg#card=math&code=r&id=B0fJc)为1），![](https://cdn.nlark.com/yuque/__latex/5e7878d8d49827cf3f546e2cc28769e3.svg#card=math&code=D_s&id=Dilgd)表示Sharding Stage（不使用Sharding时![](https://cdn.nlark.com/yuque/__latex/5e7878d8d49827cf3f546e2cc28769e3.svg#card=math&code=D_s&id=JWt3W)为0）。那么参数、梯度、优化器状态部分的内存公式为：

![](https://cdn.nlark.com/yuque/__latex/4791cd1ae18f4cc971aaf5d9aa899d5c.svg#card=math&code=%28%20K%5Ccdot%28%5Cfrac%7BD_s%7D%7Br%7D%2B1-D_s%29%2B2%5Ccdot%28%5Cfrac%7BD_s-1%7D%7Br%7D%2B3-D_s%29%20%29%5Ccdot%5CPhi&id=Fw4lU)<br />其中![](https://cdn.nlark.com/yuque/__latex/7856fad79bb68a940c6d5bd9658335f2.svg#card=math&code=K%3D4%5C%20for%5C%20SGD%5C%20and%5C%20K%3D12%5C%20for%5C%20Adam&id=HpWQ0)

#### 5. 重计算（Recompute）
#####  Recompute Granularity
recompute_granularity = 
- core_attn
- full_attn
- full (default)
##### Information
core_attn其实就是Self-Attention层（对照代码和结构可以得出这个结论），在完整的Attention层中后面还有个Linear，Linear是实现在Multi-Head Attention里的，Dropout使用在TransformerDecoder中<br />TransformerDecoder is a stack of N decoder layers.<br />The transformer decoder layer contains multiheadattention and some linear layers.
##### Summary Recompute

- 如果是core_attn模式，那么就重计算self.core_attn，否则将self.core_attn的算子从重计算中剔除
- 如果是full_attn模式，就重计算整个MultiHeadAttention，否则正常计算
- 如果是full模式，就重计算整个TransformerDecoder

下图是TP不能切分的层，可以得到结论<br />**core_attn重计算**

- 非TP而是由SP决定的：![](https://cdn.nlark.com/yuque/__latex/c5e6e178485c23fe369e35bb41ffb797.svg#card=math&code=2%5Ccdot%20sbh&id=zIKeA)
- TP决定的：![](https://cdn.nlark.com/yuque/__latex/97d4dbc5ee368ac05948264386931a9f.svg#card=math&code=%284%2B2%29%5Ccdot%20sbh%20%2B%20%282%2B1%2B2%29%20%5Ccdot%20as%5E2b%20%3D%206%5Ccdot%20sbh%20%2B%205as%5E2b&id=WbINA)

**full_attn重计算**

- 除了core_attn的之外，额外多了一层Linear，是![](https://cdn.nlark.com/yuque/__latex/c5e6e178485c23fe369e35bb41ffb797.svg#card=math&code=2%5Ccdot%20sbh&id=hqgQv)的TP

**full重计算**

- 只剩下![](https://cdn.nlark.com/yuque/__latex/c5e6e178485c23fe369e35bb41ffb797.svg#card=math&code=2%5Ccdot%20sbh&id=u7NHE)的输入，其他全没了

![image.png](https://cdn.nlark.com/yuque/0/2023/png/22927810/1700356239223-dcc5f2d0-8892-4585-9af5-e37342296c3f.png#averageHue=%23f7f6f6&clientId=udb044a1c-b187-4&from=paste&height=575&id=jhvnW&originHeight=1149&originWidth=1500&originalType=binary&ratio=2&rotation=0&showTitle=false&size=267637&status=done&style=none&taskId=ucac36cfd-a106-4e82-9698-28b0872c335&title=&width=750)

## Llama显存公式
> ![](https://cdn.nlark.com/yuque/__latex/15288aa2308892b2cf8e1fe68a0fc93c.svg#card=math&code=M_%7Btotal%7D%20%3D%20M_%7Bp%5C_g%5C_os%7D%20%2B%20M_%7Ba%7D%2C%5C%20where&id=LJNjV)
> ![](https://cdn.nlark.com/yuque/__latex/9a6a6bafeadad0e90e29e415d5f1ceb1.svg#card=math&code=M_%7Bp%5C_g%5C_os%7D%20%3D%20%28%20K%5Ccdot%28%5Cfrac%7BD_s%7D%7Br%7D%2B1-D_s%29%20%2B%202%5Ccdot%28%5Cfrac%7BD_s-1%7D%7Br%7D%2B3-D_s%29%20%29%5Ccdot%5CPhi&id=Tue6Q)
> ![](https://cdn.nlark.com/yuque/__latex/63a017a47c28f1c261bf086fd6226583.svg#card=math&code=M_%7Ba%7D%5C%20%3D%20%5Cleft%5C%7B%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%5Cbegin%7Barray%7D%7B%2A%2Alr%2A%2A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%281%2B%5Cdelta_%7Bm%5Cneq1%7D%5Cfrac%7Bp-1%7D%7Bpm%7D%29%5Cfrac%7BL%7D%7Bt%7D%5C%7B%5B10%28%5Csigma-%5Csigma%20t%2Bt%29%2B%5Cfrac%7B56%7D%7B3%7D%5Dsbh%2B5as%5E2b%5C%7D%2C%20%26%20%5Ctext%7Bno%20recompute%7D%5C%5C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%281%2B%5Cdelta_%7Bm%5Cneq1%7D%5Cfrac%7Bp-1%7D%7Bpm%7D%29%5Cfrac%7BL%7D%7Bt%7D%5C%7B%5B8%28%5Csigma-%5Csigma%20t%2Bt%29%2B%5Cfrac%7B38%7D%7B3%7D%5Dsbh%5C%7D%2C%20%26%20%5Ctext%7Bcore_attn%20recompute%7D%20%5C%5C%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%281%2B%5Cdelta_%7Bm%5Cneq1%7D%5Cfrac%7Bp-1%7D%7Bpm%7D%29%5Cfrac%7BL%7D%7Bt%7D%5C%7B%5B8%28%5Csigma-%5Csigma%20t%2Bt%29%2B%5Cfrac%7B32%7D%7B3%7D%5Dsbh%5C%7D%2C%20%26%20%5Ctext%7Bfull_attn%20recompute%7D%20%5C%5C%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%281%2B%5Cdelta_%7Bm%5Cneq1%7D%5Cfrac%7Bp-1%7D%7Bpm%7D%29%5Cfrac%7B2sbhL%7D%7Bt%7D%2C%20%26%20%5Ctext%7Bfull%20recompute%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%5Cend%7Barray%7D%20%20%0A%5Cright.%20&id=thD2Y)


![](https://cdn.nlark.com/yuque/__latex/7856fad79bb68a940c6d5bd9658335f2.svg#card=math&code=K%3D4%5C%20for%5C%20SGD%5C%20and%5C%20K%3D12%5C%20for%5C%20Adam&id=MrHFI)<br />![](https://cdn.nlark.com/yuque/__latex/72cb3a229067770aeb6caa625a65a1a1.svg#card=math&code=r&id=A2ZfR)表示Sharding Degree（不使用Sharding时![](https://cdn.nlark.com/yuque/__latex/72cb3a229067770aeb6caa625a65a1a1.svg#card=math&code=r&id=VVzgV)为1）<br />![](https://cdn.nlark.com/yuque/__latex/5e7878d8d49827cf3f546e2cc28769e3.svg#card=math&code=D_s&id=JFVpF)表示Sharding Stage（不使用Sharding时![](https://cdn.nlark.com/yuque/__latex/5e7878d8d49827cf3f546e2cc28769e3.svg#card=math&code=D_s&id=NNCxw)为0）<br />![](https://cdn.nlark.com/yuque/__latex/8456c30c0d08ea621bbda08077638dd7.svg#card=math&code=%5CPhi&id=VIYtg)表示参数量<br />![](https://cdn.nlark.com/yuque/__latex/4760e2f007e23d820825ba241c47ce3b.svg#card=math&code=m&id=vbINr)表示Interleaving stage/vpp degree（把1F1B看作是![](https://cdn.nlark.com/yuque/__latex/f0c8366376d0dc59475bc516b9982ed0.svg#card=math&code=m%3D1&id=DnkTz)的Interleaved 1F1B）<br />![](https://cdn.nlark.com/yuque/__latex/d4cd21d60552e207f237e82def9029b6.svg#card=math&code=p&id=gmwbE)表示Pipeline Parallelism Degree，不使用流水线并行时![](https://cdn.nlark.com/yuque/__latex/9af3acf106aaeba29d00cd5d581c26a0.svg#card=math&code=p%3D1&id=v3cHG)<br />![](https://cdn.nlark.com/yuque/__latex/0cf79ec7192d3798bd99aa1dc4d343b5.svg#card=math&code=%5Cdelta_%7Bm%5Cneq1%7D&id=sg4Ue)当![](https://cdn.nlark.com/yuque/__latex/c68b07a61417c32e359c58767101129d.svg#card=math&code=m%5Cneq1&id=iMiLx)时为1，否则为0<br />![](https://cdn.nlark.com/yuque/__latex/c895173d3be4872abf206be4268a58cb.svg#card=math&code=L&id=Fftpp)表示模型中Transformer Layer数量<br />![](https://cdn.nlark.com/yuque/__latex/cead1760d9d5723460c4b8d4028f113a.svg#card=math&code=t&id=JCEXJ)表示Tensor Parallelism Degree<br />![](https://cdn.nlark.com/yuque/__latex/788df1ba344b3092def7590d1be6b4d4.svg#card=math&code=%5Csigma&id=aA2qX)表示是否开启Sequence Parallelism（使用SP则![](https://cdn.nlark.com/yuque/__latex/a24acba0a780556cd21fad4a7b5ad9ac.svg#card=math&code=%5Csigma%3D1%0A&id=kIefu)，不使用则![](https://cdn.nlark.com/yuque/__latex/7254509f0e5ec75d00dd174887e2e6c0.svg#card=math&code=%5Csigma%3D0&id=HREKF)）<br />![](https://cdn.nlark.com/yuque/__latex/79ce3c7a71877c2ff01695e38ade43ca.svg#card=math&code=s&id=K1qAb)是sequence length<br />![](https://cdn.nlark.com/yuque/__latex/d29c2e5f4926e5b0e9a95305650f6e54.svg#card=math&code=b&id=ZTe9F)是micro batch size<br />![](https://cdn.nlark.com/yuque/__latex/67df0f404d0960fadcc99f6258733f22.svg#card=math&code=h&id=DsNtL)是hidden dimension size<br />![](https://cdn.nlark.com/yuque/__latex/26fdbf8e53cb0e48da5f4ddd4aaf5a5c.svg#card=math&code=a&id=st7Hi)是attention heads



#### 7. **问题疑惑与解答**

   - 问题a：阅读代码时发现，如果重计算的粒度不是core_attn，就将self.core_attn的算子从重计算中剔除，这是为什么？self atten就不参与重计算了吗？
     
     答：如果是最后一层的话不用参与重计算，因为算完前向之后马上就计算反向了。但是attention并不是最后一层，这部分代码等待后续再确认一下。

### 下周工作

1. 在真机分布式环境下验证Llama显存模型的准确度
2. 为Llama显存模型编写函数，并提交PR到PaddleNLP中

### 导师点评


