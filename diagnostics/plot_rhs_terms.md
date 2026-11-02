---
title: "在 VTK 中绘制方程各项"
nav_order: 4
parent: "诊断与后处理"
layout: default
render_with_liquid: false
---

# 在 VTK 中绘制方程的各项

本诊断仅适用于模型 600。

## 概述

该 `jorek2_postproc` 工具读取重启文件，并生成一个 VTK 文件，其中 `elm_matrix` 中各方程的各项被分别列出。它有助于了解主导物理项，并帮助诊断数值问题。

功能包括：

- **避免代码重复：** 各项直接取自 `mod_elm_matrix_fft` 的右端项。
- 用户可用 `only_itor` 选择单个环向谐波。若不指定，则对所有谐波求和。
- 用户可用 `vtk_phi_value` 选择极向平面，并用 `nsub_vtk` 设置 VTK 分辨率。
- 用户可以只计算一个方程的各项。若未选择方程，则生成所有方程的各项。
- 各项按其物理含义标注。每个标签的开头标识方程或变量，末尾标识该方程中的具体项。

**重要：** 经分部积分得到的项需要额外的处理。本诊断调用 `elm_matrix` 时仍缺少边界积分。

## 用法

本工具实现在[交互式诊断工具 `jorek2_postproc`](../howto/introduction_to_jorek_diagnostics.md#jorek2_postproc) 中。编译与一般用法参见该页。

与大多数 `jorek2_postproc` 诊断不同，`RHS_terms_vtk` 不能以交互方式运行。请按以下结构编写后处理脚本：

```text
namelist INPUT_FILE
set nsub_vtk NUMBER_OF_SUBDIVISIONS
set vtk_phi_value TOROIDAL_ANGLE
set only_itor TOROIDAL_HARMONIC
for step FIRST_STEP to LAST_STEP do
  RHS_terms_vtk EQUATION_NUMBER
done
```

参数与命令实参如下：

- `nsub_vtk`：用于 VTK 可视化的 JOREK 单元细分份数。
- `vtk_phi_value`：待计算的极向平面的环向角，单位为弧度。
- `only_itor`：选择单个环向谐波。删除该行则对所有谐波求和。
- `EQUATION_NUMBER`：选择单个方程。在 `RHS_terms_vtk` 中省略该实参，则计算每个方程的各项。

使用一个 MPI 进程运行该脚本：

```bash
export OMP_NUM_THREADS=NUMBER_OF_THREADS
mpirun -n 1 jorek2_postproc < POSTPROCESSING_SCRIPT
```

不要使用多于一个 MPI 进程。大算例可能需要以批处理作业提交，但仍然只用一个 MPI 进程。生成的 VTK 文件写入 `postproc/` 目录。

在某一个特定的 Marconi 配置上，直接调用 `jorek2_postproc`（不经 `mpirun`）解决了该问题。
