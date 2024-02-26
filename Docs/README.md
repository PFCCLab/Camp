## 📖 本目录用于存放各学员参与「飞桨护航计划集训营」项目时的学习文档

### 子文件夹命名规则
`Docs` 下各子文件夹的命名规则为：
```
项目序号_项目英文名称
```

比如 MarioLulab 同学参与的是 ["项目三：新 IR API + 自动微分推全和核心组件完善"](https://github.com/PaddlePaddle/community/blob/master/hackathon/hackathon_5th/%E3%80%90PaddlePaddle%20Hackathon%205th%E3%80%91%E9%A3%9E%E6%A1%A8%E6%8A%A4%E8%88%AA%E8%AE%A1%E5%88%92%E9%9B%86%E8%AE%AD%E8%90%A5%E9%A1%B9%E7%9B%AE%E5%90%88%E9%9B%86.md#%E9%A1%B9%E7%9B%AE%E4%B8%89%E6%96%B0-ir-api--%E8%87%AA%E5%8A%A8%E5%BE%AE%E5%88%86%E6%8E%A8%E5%85%A8%E5%92%8C%E6%A0%B8%E5%BF%83%E7%BB%84%E4%BB%B6%E5%AE%8C%E5%96%84)，则文件夹命名为
```
03_NewIRAPI_AutoDiffAndCoreComponentRefinement
```

### 子文件夹内存放的文件
子文件夹内部可存放各学员参与项目时形成的一系列过程文档，包括但不限于**学习资料**、**代码阅读笔记**和**设计文档**等。如果学员在项目过程中有任何尚未成熟的 idea，欢迎先在 wiki 或者 issue 里面写下自己的想法 💡，在这里你可以和导师 🧑‍🏫 友好协作，共同讨论沉淀。等到 idea 在 wiki 或者 issue 里面打磨成熟以后，你可把其沉淀为分享材料通过 **PR** 的方式提交到该文件夹下对应项目的子文件夹内，期待有越来越多的 idea 帮助我们一同建设飞桨大家庭 🏠～

原则上不对各学员子文件夹内的文件组织方式做要求。**但请注意：请保证提交的文件名中不包含空格**。如有需要，`03_NewIRAPI_AutoDiffAndCoreComponentRefinement` 下的文件夹结构可作为参考：
```
Camp/
├── ...
├── Docs/
│   ├── 第五期黑客松护航计划
│   │   ├── xx_xxxxx/
│   │   ├── ...
│   │   ├── 03_NewIRAPI_AutoDiffAndCoreComponentRefinement/
│   │   │   ├── imgs/
│   │   │   │   ├── xx.png
│   │   │   │   └── ...
│   │   │   ├── CodeReading/
│   │   │   ├── DesignDocs/
│   │   │   ├── ...
│   │   │   └── README.md
│   │   └── ...
│   ├── 第六期黑客松护航计划
│   │   ├── ...
└── ...
```

#### 格式规范
为了更好的阅读体验，我们为大家提供了书写文档时的参考范式，希望大家按照下面的模板创建并维护自己的技术资料 💗

**README**

请在这里面介绍你的技术文档仓库，突出一下它的亮点和特色，方便读者快速了解和阅读 📖～

**设计文档**

建议存放路径：

```
./DesignDocs/
```


参考链接：[api_design_template.md](https://github.com/PaddlePaddle/community/blob/master/rfcs/APIs/api_design_template.md)

具体案例：[20200301_api_design_for_quantile.md](https://github.com/PaddlePaddle/community/blob/master/rfcs/APIs/20200301_api_design_for_quantile.md)

**代码阅读笔记**

建议存放路径：

```
./CodeReading/
```

如果你对于代码阅读并不熟悉，或许可以在这里获得灵感 🔮：

🌟 往期代码串讲活动材料 ➡️ [飞桨源码读书会](https://github.com/PaddlePaddle/community/tree/master/pfcc/paddle-code-reading)

### 代码串讲&技术分享会

我们将在每周三举办一个技术分享会，只要是和所作课题相关的技术分享都可以来讲（如代码串讲、基础技术分享、问题总结与方案拆解、踩坑经验分享等），欢迎大家前来分享 or 听取别人的心得和经验 👏！在技术分享会上，你有机会与小伙伴交流自己沉淀的文档，也能够得到其他导师的指导和建议 😊

#### 技术分享会报名与审批说明

1️⃣ 将待分享的内容（通常是 md 格式）以 PR 的形式提交到 [./Docs](https://github.com/PFCCLab/Camp/tree/main/Docs) 目录下你的个人文件夹中

2️⃣ 带教导师审核串讲内容 📄，通过后 ✅，在 https://github.com/PFCCLab/Camp/issues/14 下面回复报名信息，报名格式如下：
```
【代码串讲报名】
日期：xxx（2023.10.16）
分享主题：xxx（面壁人调研分享）
分享人：@xxx（@艾AA）
分享材料：([文档链接🔗](https://github.com/PFCCLab/Camp/tree/main/Docs/xx/xx.md))
```

3️⃣ PaddlePaddle 团队审核，审核通过后沟通分享会排期 ✅

4️⃣ 若多人报名，则按报名先后顺序进行筛选，一期最多不超过两个主讲人

5️⃣ 技术分享会包含：学员分享、导师点评、自由讨论环节，为全体参会人提供技术交流平台

