# 2023.10.13 meeting

- 主题：可视化流水线并行时序图设计文档讨论

- 时间：2023.10.13 14:40

- 与会人员：
	1. AndSonder
	2. From00

## 主要进展

- 完成了可视化静态图自动并行时序图设计文档的初稿

## 方案设计探讨

1. 如何准确的记录Job开始和结束的时间

由于Run里面的Op是多线程执行的，输出 job 结束时，在 Run 里启动的 op 可能还没有执行完毕。经讨论，决定在 Job 开始执行的时候使用 cudaEventRecord 记录开始时间，而在 Job 结束的时候使用 cudaEventRecord 记录结束时间。由于 cudaEvent 是和流绑定的，所以需要在每个流上都记录开始和结束时间。最后取所有流中最早的开始时间和最晚的结束时间作为 Job 的开始和结束时间。

2. cudaEvent 只能获取到 GPU 的时间，如何获取 CPU 的时间

由于 cudaEvent 只能获取到 GPU 的时间，故在给每个流插入开始的 cudaEvent 的时候，同时也插入一个 CPU 的时间记录。最后用 GPU 上的运行时间加上 CPU 上开始的时间，就可以得到 Job 的运行区间了。

3. 采用离线生成log还是在线生成log

由于在线生成log需要考虑线程通信等问题，故决定采用离线生成log的方式。即生成log文件，然后用python脚本解析log文件，生成时序图。

4. 日志信息设置

日志信息需要包含特殊标记避免在后续解析时错误解析到其他不相关日志。

## 下一步任务

1. 编码实现上述方案
2. 完善文档


