---
title: "Jorek2_fieldlines_vtk_newdiag"
nav_order: 26
render_with_liquid: false
parent: "General"
---

## Jorek2_fieldlines_vtk_newdiag

该诊断沿磁力线计算任意物理表达式（使用 new_diag 框架），并将这些信息同时写入 vtk 与 txt 文件。运行方式为
   jorek2_fieldlines_vtk_newdiag < jorek.in

它使用文件 jorek_restart.h5 载入模拟状态，并使用名为 stpts 的文本文件，其中包含待求值物理表达式所在磁力线的必要信息，以及待求值的物理表达式（见下文）。 
输出生成于以下文件 
- field_lines.vtk 是二进制文件，包含沿磁力线的表达式值（使用与 jorek2vtk 一致的坐标系），可用 Paraview 等可视化工具读取
- field_lines.txt 是 ASCII 文件，包含相同的数据（使用 https://www.jorek.eu/wiki/doku.php?id=coordinates 中的坐标系）

### 程序设置
若存在文件 stpts，则读入该文件以设定所需参数。stpts 文件必须采用以下格式：
  # n_scalars
  3
  # expr  name
  Te    Te_eV
  ne    ne_m-3
  nimp  nimp_m-3
  # n_lines
  100
  # nr    R_start   Z_start   phi_start   n_turns
  1    3.003     1.606     6.0900      1
  2    2.988     1.558     6.0900      1
  3    2.990     1.560     6.0900      1
  4    2.946     1.576     6.0900      1
  5    2.989     1.571     6.0900      1
  ...
  100  2.997     1.620     6.0900      1
此处，n_scalars 为待求值的标量表达式个数，expr 与 name 分别为表达式（按 new_diag 框架中的定义）及其名称，n_lines 为待求值的磁力线条数（沿正向与反向两个方向追踪，因此最终计算的磁力线数目为该值的两倍）。此外，nr 为磁力线编号，R_start、Z_start 与 phi_start 为其起始坐标，n_turns 为追踪该磁力线所沿的环向圈数。与 jorek2_poincare 诊断相同，用户可以给出全部磁力线的起始坐标，也可以指定若干组磁力线、只显式给出每组的第一条与最后一条，其起始坐标假定在首条与末条之间均匀分布。

### 输出文件
field_lines.txt 包含沿磁力线求值的表达式结果，使用的坐标系见 https://www.jorek.eu/wiki/doku.php?id=coordinates
该文件的格式如下：
            line               x               y               z             Phi    Te_eV           ne_m-3          nimp_m-3
               1  0.29471371E+01  0.57653373E+00  0.16059999E+01  0.60900002E+01  0.32168159E+01  0.25254070E+21  0.11506390E+21
               1  0.29454236E+01  0.59543729E+00  0.16052808E+01  0.60837169E+01  0.32214899E+01  0.25050444E+21  0.11412951E+21
               1  0.29435921E+01  0.61434269E+00  0.16045547E+01  0.60774336E+01  0.32317951E+01  0.24841616E+21  0.11315785E+21
               1  0.29416425E+01  0.63324934E+00  0.16038219E+01  0.60711503E+01  0.32482059E+01  0.24628058E+21  0.11214984E+21
               1  0.29395747E+01  0.65215647E+00  0.16030822E+01  0.60648675E+01  0.32712436E+01  0.24410277E+21  0.11110648E+21

field_lines.vtk 是二进制文件，可在 Paraview 中读取。它包含与 field_line.txt 相同的数据，但坐标系与 jorek2vtk 一致。原站此处附有一个用该诊断绘制的图形示例（图片在上游已缺失）。
<!-- 原站引用的图/附件已缺失：上游仓库与旧 wiki 均无此文件，故移除引用 -->
