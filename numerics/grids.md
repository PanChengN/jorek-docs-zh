---
title: "网格"
nav_order: 2
parent: "数值方法与工具"
layout: default
render_with_liquid: false
---

# 网格

JOREK 中实现了多种有限元网格。其中一些网格仅用于平衡求解，并不与磁面对齐。这些初始网格如下（同时给出子程序名）：

-   `grid_bezier_square`：沿 R 与 Z 方向的矩形网格
-   `grid_polar_bezier`：边界形状可调的极坐标网格。
    参见图 [1](#gridpolar) 与图 [2](#gridxpt)
    （灰色）。这通常是初始网格的默认选择。
-   `grid_bezier_square_polar`：两者的组合，即内部为方形网格、外围为极坐标网格。


[gridpolar]: assets/grids/grid_polar.png "Polar grid"
![极坐标网格][gridpolar]

*图 1：由 `grids/grid_polar_bezier.f90` 生成的极坐标网格示例。图中还示出了单元节点的编号方式：编号从磁轴开始，最初的若干个单元共用磁轴节点。此外，以一个单元为例用红色标出了 `s,t` 方向与顶点次序。*


平衡一旦确定，即可生成与平衡磁面对齐的有限元网格。为此可用的网格生成程序如下（原文称两个，实际列出三个）：

-   `grid_flux_surface`：单元的两条边对齐到无 X 点的托卡马克位形的
    闭合磁面（图 [2](#gridfsxpt) 左侧，红色）。
-   `grid_xpoint`：单元对齐到含单个下 X 点的 X 点位形的
    磁面（图 [2](#gridfsxpt) 右侧，红色）。
-   `grid_double_xpoint`：该程序有多种用途。它既用于上单零
    位形，也用于计算域内包含两个 X 点的位形。这两个 X 点
    可以（但不必）构成对称双零位形。

图 [2](#gridfsxpt) 中给出两套有限元网格。灰色网格为
`grid_polar_bezier` 类型，仅用于平衡求解（初始网格）。红色所示为
X 点位形的磁面对齐网格（`grid_xpoint`），它随后用于
MHD 方程的时间积分。

图中示出了极坐标网格与磁面网格中节点的编号（黑色
数字）、单元内节点的编号（红色数字），以及
单元局部坐标 \$s\$ 与 \$t\$ 的方向。

[gridfsxpt]: assets/grids/grid_fsandxpt.png "Flux-surface grid"
![磁面对齐网格][gridfsxpt]

*图 2：（左）用 `grids/grid_flux_surface.f90` 构造的磁面对齐网格示例。（右）用 `grids/grid_xpoint.f90` 构造的 X 点网格示例。这需要由已有的极坐标网格（灰色）提供极向磁通的映射。__实际应用需要高得多的分辨率__。*


## 教程

以下教程介绍基本 X 点网格、双 X 点网格与壁延伸网格的构造：

-   [Grad-Shafranov 教程](grids/GS_tutorial.md)
-   [X 点网格构造](grids/Xgrid_tutorial.md)
-   [双 X 点网格构造](grids/DXgrid_tutorial.md)
-   [壁延伸网格构造](grids/Wallgrid_tutorial.md)
-   [另一种壁延伸网格构造](grids/Wallgrid_tutorial2.md)
-   [Gn 连续网格构造](grids/Gn_grid_tutorial.md)
