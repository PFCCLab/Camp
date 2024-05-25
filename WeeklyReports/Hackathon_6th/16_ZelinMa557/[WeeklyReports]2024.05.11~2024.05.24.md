### 姓名
马欣楷

### 实习项目
CINN 支持动态 Shape 专项（前端方向）

### 本周工作
1. 完成单个generate shape的lower工作，在reduce mean和group norm上取得性能增益
2. 与导师讨论，探索generate shape op具有多输出情况的lower机制。目前暂定split+concat方案。期间提出了一个生成局部数组的方案，对现有机制改动较大，暂时废弃。
3. 修复部分inferSymbolicShape和inferMeta推导结果不一致的问题，包括：
    * 修复unique算子部分返回值不对齐的问题
    * 修复argmax\slice推导出shape为[1]的问题

### 下周工作
1. 实验generate shape多输出lower

### 导师点评
generate shape的lower工作在近两周取得重要突破，完成了核心代码的开发和PR合入，希望再接再厉，将generate shape lower的工作做到足够完备。
