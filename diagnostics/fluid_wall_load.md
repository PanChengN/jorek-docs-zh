---
title: "评估三维壁面上的流体负荷"
nav_order: 3
parent: "诊断与后处理"
layout: default
render_with_liquid: false
---

# 如何借助磁力线追踪评估流体壁负荷

计算三维壁面上流体负荷的 Fortran 代码位于

```text
particles/examples/fluid_loads_on_3D_wall.f90
```

## 这段代码做什么？

- 它计算由三角形离散化的三维薄壁上的流体通量（热负荷与电流负荷）。
- 它将这些通量以 VTK 格式导出（`3D_wall_fluid_loads.vtk`）。

## 如何编译与运行

1. 编译该程序，方式与 `jorek2vtk` 类似：

   ```bash
   make -j 8 fluid_loads_on_3D_wall
   ```

2. 将需要计算热流的流体重启文件复制为 `jorek_restart.h5`，例如：

   ```bash
   cp jorek07000.h5 jorek_restart.h5
   ```

3. 使用通常的 JOREK 输入文件执行该程序：

   ```bash
   export OMP_NUM_THREADS=56 # The code only uses OpenMP parallelization (not MPI)
   ./fluid_loads_on_3D_wall < input_file_jorek
   ```

## 必需的输入

必须在算例目录中提供以下两个 HDF5 文件：

- **`wall_to_load.h5`**：将要进行磁力线追踪并计算通量的壁面。
- **`wall.h5`**：磁力线与之相交的壁面。通常，这既包括被加载壁面周围的结构，也包括被加载结构本身。

这些 HDF5 文件的格式见[粒子壁负荷文档](../howto/particles_wall_load.md)。

## 需要了解的重点

- 为使磁力线追踪有效，**壁面三角形必须位于 JOREK 计算域内**。否则这些三角形被视为被遮挡（与等离子体不相连），其上没有负荷。请谨慎选择壁面。
- 注意壁面三角形的排列顺序：代码假定其法向指向等离子体。
- `l_par_min` 是硬编码的。可能需要针对你所用的托卡马克装置加以调整；修改代码后须重新编译。也可检查代码开头附近的其他硬编码参数。
- 代码假定通量平行于磁力线。因此重要的垂直分量贡献未被计入。
- 平行热流的计算依赖于 `jorek2_postproc` 的 `qpar_tot` 表达式，可在 `diagnostics/new_diag/mod_expression.f90` 中查看。它是等离子体离子与电子的动能热流与热传导热流之和，如 [MHD 鞘层热流文档](../howto/physics_options/boundary_conditions/sheath_heatflux_bc.md)所示。

  **应检查网格分辨率对于所选的平行与垂直热扩散系数是否足够。** 否则尖锐的边界梯度——例如平行传导系数过小所导致的梯度——可能无法被分辨，算出的平行热流可能完全错误。

  为验证这一点，可利用[能量守恒诊断](./plot_live_data.sh.md#check-energy-conservation)检查全局能量守恒。使用鞘层边界条件时，通常更方便的做法是把 $q_\parallel$ 替换为所采用的 $q_\parallel$ 公式；这通常效果要好得多。也可以把自定义通量（例如粒子通量或逃逸电子通量）加入代码。

## 有用资源

- [用于时间循环以及用一维方程计算温升的脚本](https://github.com/jorekart/scripts_javier/tree/main/tasks/loads_3d_walls)
