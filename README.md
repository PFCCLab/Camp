# 【PaddlePaddle Hackathon】飞桨护航计划集训营周报 & 资料管理

**[🚀 飞桨开源框架](https://github.com/PaddlePaddle/Paddle) | [🧰 飞桨开发套件](https://github.com/PaddlePaddle/PaddleOCR) | [⛵ 飞桨护航计划集训营](https://github.com/PaddlePaddle/Paddle/issues/57264)**

☘️ **我们为什么需要这个 repo ？**

- 本 repo 用于「飞桨护航计划集训营」的学员周报提交、资料管理、会议记录保存和技术方案探讨（使用方法详见本文档的 [护航计划规则](https://github.com/PFCCLab/Camp/tree/main/README.md#%E6%8A%A4%E8%88%AA%E8%AE%A1%E5%88%92%E8%A7%84%E5%88%99)）。希望这个 repo 能记录你乘风破浪解决各种难题的印记，或是留下你由浅入深不断成长的足迹， enjoy it 😄

🏡 **请问这个 repo 的文件夹都有什么内容？**

- `Docs/` : 存放各学员参与「飞桨护航计划集训营」项目时的过程文档。包括但不限于**学习资料**、**代码阅读笔记**和**设计文档**等
- `Meetup/` : 存放各学员参与「飞桨护航计划集训营」项目时的会议纪要、与导师的沟通记录等
- `WeeklyReports/` : 存放各学员参与「飞桨护航计划集训营」项目时的详细周报

## 飞桨护航计划简介

【飞桨护航计划】是【百度飞桨社区】发起的远程项目，也是飞桨黑客松非常重要的一个赛道（不了解飞桨黑客松戳这里 ➡️ [PaddlePaddle Hackathon 说明](https://github.com/PaddlePaddle/docs/blob/develop/docs/guides/10_contribution/hackathon_cn.md)），旨在鼓励在校学生积极参与开源社区，提升实践能力，在社区中获得更良好、全面的成长 💪。

学生通过申请后，将由专属的百度资深工程师带教进行**为期 3 个月**的开源项目开发。顺利结项后，会获得百度的技术认证证书 📄 和丰厚的奖励 🎁。

随时随地都能使用 🔧 的线上 V100 开发环境（申请方式看这里 ➡️ [飞桨线上开发环境——AI Studio](https://github.com/PaddlePaddle/community/tree/master/pfcc/call-for-contributions#%E9%A3%9E%E6%A1%A8%E7%BA%BF%E4%B8%8A%E5%BC%80%E5%8F%91%E7%8E%AF%E5%A2%83ai-studio)），可以灵活安排的日常工作时间 ⌚️，正式实习和就业的绿色通道 🚥，耐心专业技术力超强的研发导师 🧑🏻‍💻……你，心动了吗？💓 心动的话快来加入我们吧～～

## 报名参与流程

**飞桨护航计划集训营**的**任务**发布在这个 [issue](https://github.com/PaddlePaddle/Paddle/issues/61006) 里面，开发者提交简历 & 通过面试后，以远程的方式深度参与飞桨重要开源项目开发实践，成果以 PR（Pull Requests）的形式贡献到指定代码仓库，实训期 3 个月（每周开发时间至少 25h），奖金 3-5 🌟。

详细说明请戳这里 👉 [报名链接](https://github.com/PaddlePaddle/docs/blob/develop/docs/guides/10_contribution/hackathon_cn.md#2-飞桨护航计划集训营)

### 护航计划规则

**整体流程**

进入护航计划的学员需在导师的指导下完成指定项目。为了更好地推进项目顺利进行，下面是我们为大家安排的一些例常任务：

- 按照要求**提交周报** 📄（两周一次）
- 根据自身情况自愿报名参加**代码串讲**活动
- 完成课题答辩，**评分标准**详见下文
- 使用 wiki 完成**协同编辑**，学员和导师更好地协同交流 💬

**周报提交**

周报是每一段时间工作的总结提炼，用于更好地反映过去两周的工作成果。提交周报的流程如下：

- 学员在 [./WeeklyReports](https://github.com/PFCCLab/Camp/tree/main/WeeklyReports) 目录下提交 PR，PR 里面是详细的周报内容，戳这里看 [Weekly Report PR Demo](https://github.com/PFCCLab/Camp/pull/7)
- 导师在 PR 中填写周报评价，以 commit 的形式添加在文档中，确认周报信息完整后由导师合入 PR，便于全体成员了解推进情况，必要时可为学员调整方向和计划
- 学员在 PR 合入后，抽取关键信息，按格式回复周报 issue。这个相当于 PR 的摘要版，便于读者快速了解项目进展和关键信息。戳这里看 [Weekly Report issues Demo](https://github.com/PFCCLab/Camp/issues/3)

详细的周报提交指南可参考：[周报提交指南](https://github.com/PFCCLab/Camp/issues/2)

**评分标准**

在进行答辩后，导师会针对学员的表现给出反馈和评价，分为四个等级：

- **不及格**：未完成导师布置的课题任务
- **及格**（🌟🌟🌟）：保质保量完成导师布置的课题任务
- **良好**（🌟🌟🌟🌟）：保质保量完成导师布置的课题任务，对项目有一定的思考和总结能力
- **优秀**（🌟🌟🌟🌟🌟）：保质保量完成导师布置的课题任务，对项目有深入的见解并提出可行性建议
- **特别优秀**（🌟🌟🌟🌟🌟🌟）：保质保量完成导师布置的课题，对项目课题贡献了可感知的创新点、或显著的额外工作量。

这个评级会直接与活动奖金挂钩，请务必重视噢～

**代码串讲**

这是一个自愿自发的分享活动，任何集训营开发项目相关的进度和成果都可以分享，导师会提供指导。代码串讲有助于知识的流动与沉淀，并锻炼学员自身演讲能力。该活动两周举行一次，面向全体训练营成员，有助于成员之间的共享互助。

**协同文档**

如果学员在项目过程中有任何尚未成熟的 idea，欢迎在 **[wiki](https://github.com/PFCCLab/Camp/wiki)** 里面写下自己的想法 💡，wiki 编辑权限对全体成员开放，在这里你可以和导师 🧑‍🏫 友好协作，共同讨论沉淀。wiki 就像你的专属「草稿箱」，你也可以在里面起草周报，甚至来一场酣畅淋漓的 brainstorm 🧠

等到 idea 在 wiki 里面打磨成熟以后，你可把它提到 **[issues](https://github.com/PFCCLab/Camp/issues)** 里面，或沉淀为分享材料提交到 [./Docs](https://github.com/PFCCLab/Camp/tree/main/Docs) 目录，期待有越来越多的 idea 帮助我们一同建设飞桨大家庭 🏠！

### 护航计划时间安排

这是我们为训练营制定的详细日程和计划 ⬇️ （重要的会议记录会被更新到 [./Meetup](https://github.com/PFCCLab/Camp/tree/main/Meetup) 目录）

| **时间** | **日程**                   |
| -------- | -------------------------- |
| **待定** | 发布集训项目，启动营员招募 |
| **待定** | 公开接收简历，安排面试     |
| **待定** | 营员招募截止，公布招募名单 |
| **待定** | 开营仪式，集训营正式启动   |
| **待定** | 营员集中答辩               |
| **待定** | 集训营结营，公布考核结果   |

**开营仪式**

我们会在训练营正式开始时为成员们举办的一个线上见面会，在这里可以认识班主任、助教、导师和其他学员，结交到志同道合的好友 👯

**集中答辩**

配合整体飞桨黑客松活动节点，学员们需要在集训结束前参与集中答辩，考核集训项目完成度与研发质量，**只有通过考核的学员才能获得对应的活动奖金
🎁 与证书 🏅️**

**结营评估**

依据营员开启集训的日期，在完成 3 个月集训后进行结营评估，评估结果分为 4 档，对应不同星级（及格：🌟🌟🌟；良好：🌟🌟🌟🌟；优秀：🌟🌟🌟🌟🌟；特别优秀：🌟🌟🌟🌟🌟🌟），**一颗 🌟 对应￥ 2,000 奖金**

## 学习资料共享

### 资料共建邀请

在项目开发过程中，你一定有许多对于技术的思考和积累，沉淀成文档一方面有助于你梳理思路、提升个人技术能力，另一方面可以分享给其他人，或许会对他人的工作有所帮助和启发。飞桨团队十分欢迎这样的行为，也邀请每一位学员共同参与资料共建。你可以在 wiki 中记录草稿，整理成系统资料后提交 markdown 文档到 [./Docs](https://github.com/PFCCLab/Camp/tree/main/Docs) 目录，优秀的分享材料可以通过**代码串讲活动**进行传播，更有机会在 PFCC 技术分享会、飞桨多平台直播活动、飞桨公众号、AIStudio 精品项目等多渠道进行宣推！

往期代码串讲活动材料戳这里 ➡️[代码串讲 & 技术分享会](https://github.com/PFCCLab/Camp/issues/14)、[飞桨源码读书会](https://github.com/PaddlePaddle/community/tree/master/pfcc/paddle-code-reading)

### 代码串讲活动

本期飞桨护航集训营固定两周举行一次代码串讲活动，每期邀请 1-2 位学员，就课题任务和其熟悉的领域进行分享，包括但不限于：基础知识、代码研读、学习心得、踩坑经验、~~同性交友~~......

护航计划发布的每个课题所属领域各不相同，你的每一次分享一定会有别人没有听过的新东西，也会收获新启发，这既是知识的流动，也是灵感的碰撞 💥！

欢迎大家踊跃参与，欢迎讨论交流 👏

### Contributors

<a href="https://github.com/PFCCLab/Camp/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=PFCCLab/Camp&max=200&columns=10&anon=1" />
</a>
