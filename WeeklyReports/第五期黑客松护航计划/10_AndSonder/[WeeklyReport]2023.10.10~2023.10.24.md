### 姓名

卢畅

### 实习项目

静态图半自动并行执行架构升级

### 本周工作

本项目第一个功能为可视化静态图自动并行时序图。由于当下大模型的训练时间较长，分布式训练时序图的可视化对于调试和分析模型的训练过程非常重要。当下没有工具能够直接给出各个GPU设备上不同Job的运行区间，因此我们需要设计一个可视化工具来实现这个功能。

本周工作如下：

1. **设计静态图自动并行可视化时序图**

####  Step1: FLAGS控制可视化开关

首先添加一个FLAGS `FLAGS_auto_parallel_profiler` 用于控制可视化时序图的开关。

后期，改成解析命令行参数，如 `python -m paddle.distributed.launch --visualize_pipline=True train.py`。

#### Step2: C++端添加相关VLOG信息

静态图模式下自动并行的运行将调用C++端 `StandaloneExecutor::Run` ，该方法中将顺序执行提前拆分好的Job，相关代码如下：

```c++
paddle::framework::FetchList StandaloneExecutor::Run(
    const std::vector<std::string>& feed_names) {
  platform::RecordEvent record_event(
      "StandaloneExecutor::run", platform::TracerEventType::UserDefined, 1);

  const auto& jobs = plan_.JobList();
  ...
  for (size_t job_idx = 0; job_idx < jobs.size(); ++job_idx) {
    const auto& job = jobs[job_idx];
    const std::string& job_type = job->Type();
    ...
    if (jobs.size() 1 && job_type != "forward") {
      const std::vector<std::stringtmp_feed_names = {};
      interpretercores_[job_idx]->Run(tmp_feed_names, /*need_fetch = */ false);
    } else {
      interpretercores_[job_idx]->Run(feed_names, /*need_fetch = */ false);
    }
  }
  ...
}
```

其中 `job_type` 包含 `forward`、`backward` 、`lr`、`optimizer`、`default`。

由于Run里面的Op是多线程执行的，输出 job 结束时，在 Run 里启动的 op 可能还没有执行完毕。因此我们在每个 Job 开始和结束的时候插入一个 `cudaEventRecord` ，这样就能保证每个 Job 的开始和结束时间都是准确的。并通过 `cudaEventSynchronize` 等待所有的 Job 结束后，再通过 `cudaEventElapsedTime` 计算出每个 Job 的运行时间。

 `FLAGS_auto_parallel_profiler` 为 True 时，在所有Job运行结束后遍历所有的Job，输出每个Job的开始和结束时间，以及Job的类型。

```c++
// record each job's run time
  if (FLAGS_auto_parallel_profiler) {
    for (size_t job_idx = 0; job_idx < jobs.size(); ++job_idx) {
      const auto& job = jobs[job_idx];
      const std::string& job_type = job->Type();
      double start_time, end_time;
      std::tie(start_time, end_time) =
          interpretercores_[job_idx]->InterpreterRunTime();
      VLOG(0) << "Profiler Info: Job (" << job_idx << "), type = " << job_type
              << ", micro_batch_id = " << job->MicroBatchId()
              << ", job_start_time = " << std::to_string(start_time)
              << ", job_end_time = " << std::to_string(end_time);
    }
```

#### Step3: Python 端解析输出的log日志

在自动并行模式下，log目录下会输出n个日志文件（n=设备数）。在训练结束后通过独立脚本解析这些日志文件，得到每个Job的开始和结束时间，以及Job的类型。

#####  正则匹配日志

在 C++ 端输出的日志格式如下：

```
I1020 09:15:07.265326 22317 standalone_executor.cc:217] Profiler Info: Job (3), type = forward, micro_batch_id = 2, job_start_time = 1697793307213.760986, job_end_time = 1697793307254.006104
I1020 09:15:07.265338 22317 standalone_executor.cc:217] Profiler Info: Job (4), type = forward, micro_batch_id = 3, job_start_time = 1697793307214.742920, job_end_time = 1697793307219.168945
```

我们可以通过如下正则表达式解析出所有类似的日志，并获取到时间、job_id、job_type、起始信息等。

##### 整合日志格式为json

在解析出所有的日志信息后，我们需要将其整合为json格式，方便后续使用Chrome tracing进行可视化。

详细设计文件见项目Doc目录

2. **编码实现讨论后的方案**

依据上述设计，编码实现了可视化时序图的功能。

以下以使用 `test_pipeline_scheduler` 单侧生成日志文件并生成可视化时序图为例进行说明：

由于单侧默认会清空掉生成的日志文件，我们需要先将清空日志的逻辑删除并指定log文件夹：

```python
class TestFThenBPass(unittest.TestCase):
    def test_pp2(self):
        file_dir = os.path.dirname(os.path.abspath(__file__))
        launch_model_path = os.path.join(
            file_dir, "pipeline_scheduler_unittest.py"
        )

        if os.environ.get("WITH_COVERAGE", "OFF") == "ON":
            coverage_args = ["-m", "coverage", "run", "--branch", "-p"]
        else:
            coverage_args = []

        # tmp_dir = tempfile.TemporaryDirectory()
        cmd = (
            [sys.executable, "-u"]
            + coverage_args
            + [
                "-m",
                "paddle.distributed.launch",
                "--devices",
                "0,1",
                "--log_dir",
                "/home/root/Paddle/build/Testing/Temporary",
                launch_model_path,
            ]
        )

        process = subprocess.Popen(cmd)
        process.wait()
        self.assertEqual(process.returncode, 0)

        # tmp_dir.cleanup()
```

1、在开启FLAG的前提下，运行训练过程并生成log

```
FLAGS_auto_parallel_profiler=1 GLOG_v=0 ctest -R test_pipeline_scheduler $VV
```

`GLOG_v=0` 的目的是产生尽可能少的日志，降低正则匹配的时间

2、运行 profiler_helper_static.py 生成json文件

![image](https://user-images.githubusercontent.com/55493212/277252471-f8cb7ac9-4b39-4a75-a21b-dc1af5a25564.png)

3、使用 Chrome Tracing 打开json文件

![image](https://user-images.githubusercontent.com/55493212/277252880-5bf6e483-4633-413b-9828-b7e078b4157d.png)

也可以使用 [perfetto](https://ui.perfetto.dev/) 打开 `pipeline_profile_perfetto.json`

![image](https://user-images.githubusercontent.com/55493212/277253525-1b6d1261-fa70-4dac-8f89-d5452d4d995c.png)

相关PR:

- https://github.com/PaddlePaddle/Paddle/pull/58313

### 下周工作

1、将 flag 修改为命令行参数

2、完善可视化时序图的功能、在多机环境下测试

3、完善设计文档和使用文档


### 导师点评
夏令营第一周能快速掌握分布式流水并行相关基础知识，准确理解项目开发需求，细致地设计实现方案并编码验证，总体表现不错。
后续工作按计划推进，以下几点建议可以关注：
1. 命令行参数开关实现可以参考[auto_config](https://github.com/PaddlePaddle/PaddleNLP/blob/develop/model_zoo/gpt-3/ppfleetx/utils/auto_config.py)和[auto_parallel.strategy](https://github.com/PaddlePaddle/Paddle/blob/develop/python/paddle/distributed/auto_parallel/strategy.py)
2. 可以考虑不同job执行时间有交集的情况