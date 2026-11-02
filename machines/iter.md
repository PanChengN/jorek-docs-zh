---
title: "ITER"
nav_order: 1
parent: "装置配置"
layout: default
render_with_liquid: false
---

# 模拟 ITER 的相关信息

若要通过 IMAS 获取 ITER 平衡、装置描述及其他模拟数据，见 [JOREK-IMAS 文档](../diagnostics/jorek-imas.md)。

## 参考情景

[压缩文件夹](assets/iter/201905_iter_scenarios.zip)，内含 **ITER 参考情景的 CORSICA 模拟**数据。其中包含以下情景的 G 文件（即 eqdsk 文件，可用 [eqdsk2jorek.f90](../howto/eqdsk2jorek) 转换为 JOREK 输入）、P 文件（剖面）和 T 文件（时间轨迹）：

- 15MA/5.3T H 模（D-T 等离子体）
- 15MA/5.3T L 模（H 等离子体）
- 7.5MA/2.65T H 模（He 等离子体）
- 5MA/1.77T H 模（H 等离子体）

**注：** 这些数据也应能通过 **IMAS** 获取，所用名称见上述文件夹中的 Excel 表格，但我（Eric）尚未测试。请第一位尝试者通过邮件向 eric.nardon@cea.fr 确认其是否可用。

[幻灯片](assets/iter/iter_reference_scenario_20190702_v3.pdf)，由 A. Matsuyama 提供，展示了上述情景的部分图，并标出 ITER DMS 任务组为破裂模拟**推荐的时间切片**。

ITER 一方的**联系人**（数据"所有者"）：S.H. Kim [sunhee.kim@iter.org](mailto:sunhee.kim@iter.org)。若对数据有请求或遇到问题，也请告知 Eric [eric.nardon@cea.fr](mailto:eric.nardon@cea.fr)。
