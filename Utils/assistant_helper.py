"""
PR 统计助手

- 生成周报统计表
- 生成未提交周报的学员列表
- 生成未点评周报并合入PR的导师列表

新一期的助教需要替换 stu_list 和 teacher_list
后续使用的时候只需要修改 issue_url、start_date 和 end_date 即可
"""


import requests
from collections import OrderedDict

issue_url = "https://api.github.com/repos/PFCCLab/Camp/issues/161"
start_date = "2024.03.09"
end_date = "2024.03.22"

stu_list = [
    "xingmingyyj",
    "huangjiyi",
    "zrr1999",
    "gouzil",
    "zyt1024",
    "zbt78",
    "RedContritio",
    "NKNaN",
    "zeroRains",
    "YibinLiu666",
    "AndSonder",
    "Corle-hyz",
    "xusuyong",
    "zhaojiameng",
    "DUCH714",
    "Yang-Changhui",
    "lshpku",
    "ZelinMa557",
    "Xinyu302",
    "fty1777",
    "yulangz",
    "WintersMontagne10335",
    "unseenme",
    "silverling",
    "Tsaiyue",
    "cocoshe",
    "lishuai-97",
    "yinfan98",
]

stu_to_teacher = {
    "xingmingyyj": ["kangguangli"],
    "huangjiyi": ["winter-wang"],
    "zrr1999": ["YuanRisheng", "0x45f"],
    "gouzil": ["SigureMo"],
    "zyt1024": ["GGBond8488"],
    "zbt78": ["GGBond8488"],
    "RedContritio": ["zhwesky2010"],
    "NKNaN": ["zhwesky2010"],
    "zeroRains": ["cyber-pioneer"],
    "YibinLiu666": ["HydrogenSulfate"],
    "AndSonder": ["From00"],
    "Corle-hyz": ["Caozhou1995"],
    "xusuyong": ["HydrogenSulfate"],
    "zhaojiameng": ["lijialin03"],
    "DUCH714": ["wangguan1995"],
    "Yang-Changhui": ["zhiminzhang0830"],
    "lshpku": ["zyfncg", "jiahy0825"],
    "ZelinMa557": ["zyfncg", "jiahy0825"],
    "Xinyu302": ["zhangbopd"],
    "fty1777": ["zhangbopd"],
    "yulangz": ["feifei-111", "2742195759"],
    "WintersMontagne10335": ["feifei-111", "2742195759"],
    "unseenme": ["zhhsplendid"],
    "silverling": ["risemeup1"],
    "Tsaiyue": ["westfish"],
    "cocoshe": ["LokeZhou"],
    "lishuai-97": ["GuoxiaWang"],
    "yinfan98": ["yuanlehome"],
}

project_to_stu = OrderedDict()
project_to_stu["项目一：PIR 算子补全与兼容机制建设"] = ["xingmingyyj"]
project_to_stu["项目二：PIR 控制流专项"] = ["huangjiyi"]
project_to_stu["项目三：PIR Python API 升级及机制建设"] = ["zrr1999"]
project_to_stu["项目四：动转静 SOT 模块 Python 3.12 支持"] = ["gouzil"]
project_to_stu["项目五：算子支持复数计算专项"] = ["zyt1024", "zbt78"]
project_to_stu["项目六：模型迁移工具建设"] = ["RedContritio"]
project_to_stu["项目七：框架 API 易用性提升"] = ["NKNaN"]
project_to_stu["项目八：组合机制算子专项和机制建设"] = ["zeroRains"]
project_to_stu["项目九：高阶微分的性能分析和优化"] = ["YibinLiu666"]
project_to_stu["项目十：静态图半自动并行训练性能优化"] = ["AndSonder"]
project_to_stu["项目十一：全自动并行架构升级"] = ["Corle-hyz"]
project_to_stu["项目十二：科学计算领域拓展专项（DeePMD-kit、光学案例）"] = ["xusuyong"]
project_to_stu["项目十三：科学计算领域拓展专项（超分重构方向）"] = ["zhaojiameng"]
project_to_stu["项目十四：科学计算领域拓展专项（领域流体方向）"] = ["DUCH714"]
project_to_stu["项目十五：科学计算领域拓展专项（领域气象方向）"] = ["Yang-Changhui"]
project_to_stu["项目十六：CINN 支持动态 Shape 专项（前端方向）"] = ["lshpku", "ZelinMa557"]
project_to_stu["项目十七：CINN 支持动态 Shape 专项（PIR 部分）"] = ["Xinyu302", "fty1777"]
project_to_stu["项目十八：CINN 静态 shape 下鲁棒性和性能优化"] = [
    "yulangz", "WintersMontagne10335"]
project_to_stu["项目二十：CINN 支持动态 Shape 专项 （后端模型扩量）"] = ["unseenme"]
project_to_stu["项目二十一：Paddle CMake 治理和编译优化"] = ["silverling"]
project_to_stu["项目二十二：PaddleMIX 套件能力建设（文图方向）"] = ["Tsaiyue"]
project_to_stu["项目二十三：PaddleMIX 套件能力建设（图文方向）"] = ["cocoshe"]
project_to_stu["项目二十四：大模型训练稳定性和高效低价小模型快速收敛"] = ["lishuai-97"]
project_to_stu["项目二十六：推理 Pass & 融合算子优化"] = ["yinfan98"]


head_part = f"""
# [WeeklyReports] {start_date}~{end_date} 周报汇总

请各位学员在本 issue 下以 comment 的形式填写周报摘要，ddl 本周五晚，格式示例如下：

```
### 姓名

xxx

### 本周工作

1. xxx
2. xxx
 
### 下周工作

1. xxx
2. xxx

### 详细周报链接：

- https://github.com/PFCCLab/Camp/pulls/xxx

```
"""

comments = requests.get(issue_url + "/comments").json()
# convert to a list
comments_stu = [x["user"]["login"]
                for x in comments if x["user"]["login"] in stu_list]
comments_comments = [x["body"]
                     for x in comments if x["user"]["login"] in stu_list]

for project, stus in project_to_stu.items():
    head_part += f"\n#### {project}\n\n"
    for stu in stus:
        teacher = stu_to_teacher[stu]
        teacher = [f"@{t}" for t in teacher]
        if stu in comments_stu:
            head_part += f"- [x] @{stu} ({', '.join(teacher)})\n"
        else:
            head_part += f"- [ ] @{stu} ({', '.join(teacher)})\n"

print(head_part)

# 获取 https://github.com/PFCCLab/Camp 下所有待合入的 pr，且 PR 标题为 start_date~end_date 周报

pr_url = "https://api.github.com/repos/PFCCLab/Camp/pulls"
pr_list = requests.get(pr_url).json()
pr_list = [
    x for x in pr_list if f"{start_date}~{end_date}" in x["title"] and x["state"] == "open"]
pr_author = [x["user"]["login"] for x in pr_list]
# 获取所有 author 的导师
pr_author_teacher = [",".join(stu_to_teacher[x]) for x in pr_author]

print("未提交周报的学员：", list(set(stu_list) - set(comments_stu)))

print("未点评周报并合入PR的导师：", pr_author_teacher)
