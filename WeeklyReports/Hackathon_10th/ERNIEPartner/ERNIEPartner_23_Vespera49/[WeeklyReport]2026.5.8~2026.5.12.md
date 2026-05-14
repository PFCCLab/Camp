Vespera49

赛题信息
进阶任务序号：23
赛题名称：在天玑9500 手机上运行 OpenClaw —— 移动端个人 AI 助手
关联厂商：联发科技、百度
本周工作

1. RFC 方案提交并通过
    已完成 OpenClaw 移动端适配 RFC 文档，提交至 PaddlePaddle/community 仓库 rfcs/hardware 目录
    方案涵盖 Termux + Node.js 运行环境、文心大模型 API 接入、资源限制应对等

2. Windows 本地环境搭建与部分功能验证
    在 Windows 上成功运行 OpenClaw Gateway，接入千帆平台 ERNIE-4.5-turbo-8k 模型
    Crestodian 管家代理可正常对话，Gateway 端口统一为 18789
    解决 Gateway 服务安装、gateway.mode 配置缺失等问题
    修正配置文件中多处残留的错误模型 ID（如 `openai/qianfan`、`openai/gpt-5.5`），统一替换为 `qianfan:ernie-4.5-turbo-8k`

3. 问题与解决
     问题：Gateway 与 Agent 端口不一致  
     解决：通过 `config set gateway.port 18789` 统一
     问题：模型报错 `Unknown model: openai/qianfan:ernie-4.5-turbo-8k`  
     解决：逐文件清理用户全局配置和项目源码中的错误前缀
     问题：pnpm 缺失导致构建失败  
     解决：通过 `npm install -g pnpm` 安装，或创建临时 pnpm.cmd 调用 npx pnpm
     问题：main agent 启动后报 `unsafe native hook relay bridge directory permissions`，且模型残留为 `openai/gpt-5.5`  
     解决：该问题仍在解决中。已尝试重置目录权限、删除运行时缓存（dist/dist-runtime）、重建用户配置目录、强制重装 Gateway，但仍在部分启动中出现

下周计划

1. 彻底解决 Windows 端 main agent 权限及模型残留问题，确保稳定启动
2. 完成至少三类实际任务验证（信息查询、文件操作、日程提醒）并记录性能指标
3. 等待天玑9500 工程设备，开始搭建 Termux + Node.js 环境，将已验证的配置移植过去
4. 准备部署文档（README）框架

当前阻塞

    Windows 端 main agent 启动时偶发 `unsafe native hook relay bridge directory permissions` 权限错误，且模型配置有时仍读取到 `openai/gpt-5.5`，尚未完全清除默认模型来源


交付物进展

| 交付物 | 状态 | 备注 |
|--------|:----:|------|
| RFC 文档 |  ✅ 已完成 | - |
| 代码实现 | 🔄  |
| README | 🔄 | - |
| 演示视频/截图 |  🔄| - |