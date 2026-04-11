本双周主要完成 PaddleOCR 文档解析方向的部署、benchmark 和文章整理工作：

1. 完成 `PaddleOCR-VL-1.5` 与 `PP-StructureV3` 的本地部署和 smoke test，统一了英文缓存目录，避免 Windows 中文路径导致模型下载或推理异常。
2. 整理并发布 `doc-parsing-benchmark` 仓库，支持 `OmniDocBench`、`MDPBench` 的 lite/resilient/full 三套 benchmark profile，并统一输出 `result.md`、`result.json`、`meta.json`。
3. 在 lite 数据集上完成 `PaddleOCR-VL-1.5`、`PP-StructureV3`、`MinerU`、`HunyuanOCR`、`MonkeyOCR` 的统一评测和对比，初步结论是 `PaddleOCR-VL-1.5` 跨数据集稳定性最好，更适合作为默认主通道候选。
4. 修正 `MonkeyOCR` 早期 text-only 接入导致表格指标被低估的问题，改为完整 parse 输出并重跑 lite benchmark。
5. 围绕 PaddleOCR 相关工作整理了三篇文章，覆盖 `PaddleOCR-VL-1.5` 部署、`PP-StructureV3` 对比、以及主流文档解析模型选型分析。

PR 链接：待提交 PR 后补充。
