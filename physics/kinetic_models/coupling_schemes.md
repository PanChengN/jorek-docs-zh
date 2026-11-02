---
title: "耦合方案"
---

# 粒子耦合方案

如动理学[简介](./particle_introductions,md)中所述，每个 part_group_config 都需要一个 3 字母代码 %coupling_scheme。本页进一步说明各种耦合方案的区别。

在后端，所有使用的 part_group_config 所选耦合方案的组合，会自动创建一定数量的变量，这些变量将被投影到有限元网格上，作为源/汇送入流体方程（mod_elt_matrix_fft）。这量化了动理学粒子对等离子体的反馈。所需的耦合变量在 particles/mod_coupling_settings.f90（assess_and_accumulate_variables）中确定，而耦合变量本身定义在 particles/coupling_variables.f90 中

目前 kinetic_main 假定存在某种与等离子体的耦合，也就是说，无法在使用静态背景等离子体或用于示踪目的时使用 kinetic_main。要做这类事，需要使用专门的程序脚本，而不是 kinetic_main。

目前已实现的耦合方案有：

| coupling_scheme | 说明 |
|-----------------|-------------|
| ncs | 中性粒子耦合方案，见[中性粒子与杂质耦合方案](./neutrals_and_impurities.md) |
| ics | 杂质耦合方案，见[中性粒子与杂质耦合方案](./neutrals_and_impurities.md) |
| rep | 逃逸电子的压力耦合方案，见[逃逸电子](./runaways_electrons.md) |
| ccs | 快粒子的电流耦合方案，见[高能离子](./energetic_ions.md) |
| pcs | 快粒子的压力耦合方案，见[高能离子](./energetic_ions.md) |
| pcf | 快粒子的压力耦合方案（完整张量），见[高能离子](./energetic_ions.md) |

*为每种类型分别建立耦合方案页面，并在那里详细说明！*
