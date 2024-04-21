### 姓名
何咏哲

### 实习项目
全自动并行架构升级

### 本周工作

1. **了解Sharding，阅读ZeRO论文，学习Paddle的Sharding实现**

   * Sharding的原理：Sharding和DeepSpeed的ZeRO类似，都是将训练过程中的参数（Parameter）、梯度（Gradient）和优化器状态（Optimizer State）切开放到不同的设备上，等到需要时再进行通信，从而极大地减少对显存的占用，使得更大规模模型的训练成为可能。
  
   * Sharding的使用：不管是Sharding还是ZeRO都有几个Stage，不同Stage将P、G、OS中的一个或几个切开放置。这是因为Sharding虽然减少了显存占用，但是带来了额外的通信开销，因此在训练时可以通过选择不同的stage来平衡这种开销。
  
   * Sharding和ZeRO的区别：Sharding采用的方法和ZeRO不同，ZeRO是分片，而Sharding是分组。此外，Sharding可以和其他并行模式兼容，而ZeRO不行。但是ZeRO的变种工作可以将P、G、OS给offload到CPU上。
  
   * Sharding需要考虑的其他因素：现在的大模型训练普遍采用自动混合精度（AMP），也存在做量化的（量化到fp16、fp8甚至1 bit），在建模时需要考虑到这个因素。特别是从Nvidia的H100发布后，Hooper架构的Tensor Core增加了对fp8的支持，之后做fp8量化的工作会越来越多。此外，诸如MSRA的BitNet这类“激进”的优化也越来越说明量化是未来的一个趋势，在建模时要充分考虑到它带来的影响。




### 下周工作

1. 学习Recompute

### 导师点评
本周学习了Sharding与ZeRO技术，调研充分翔实，有自己的理解，并提出了一些模型可扩展性方面的思考，为后续建模打下了坚实的理论基础。
