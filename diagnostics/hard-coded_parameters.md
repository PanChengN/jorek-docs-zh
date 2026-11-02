---
title: "JOREK 中的硬编码参数"
nav_order: 16
render_with_liquid: false
parent: "Installation & Compilation"
---

## 物理模型

第一个"硬编码参数"是 **JOREK 物理模型编号**。它在 Makefile.inc 文件中设置。

其他硬编码参数由位于模型目录 models/modelXXX/ 中的 mod_parameters.f90 文件设置：

| 参数 | 说明 |
| --- | --- |
| n_tor | 环向模数个数（cos 与 sin 分别计数） |
| n_period | 周期性（n_period=1 表示整个环向） |
| n_plane | 环向平面个数；n_plane 必须 >= 2*(n_tor-1) |
| n_vertex_max | 不要修改 |
| n_nodes_max | 网格节点的最大数目 |
| n_elements_max | 网格单元的最大数目（二维 Bezier） |
| n_boundary_max | 边界单元的最大数目（一维 Bezier） |
| n_pieces_max | 磁面表示中分段的最大数目 |

修改硬编码参数时，应始终执行：
  make clean

更换模型时，应执行：
  make cleanall

## 脚本 config.sh

在 trunk 中调用的脚本
  ./util/config.sh
可用于**显示硬编码参数的取值**。将得到如下输出：
  =======================
  Makefile.inc:
  -----------------------
    model303
    n_tor = 1
    n_period = 1
    n_plane = 8
    n_vertex_max = 4
    n_nodes_max = 60001
    n_elements_max = 60001
    n_boundary_max = 1001
    n_pieces_max = 6001
  =======================

同一脚本也可**修改硬编码参数**：
  ./util/config.sh model=303 n_tor=3 n_period=8 n_plane=8

**重要：** 用该脚本更换模型时，务必确认其他参数也正确，因为它们是分别在各模型专属的 mod_parameters.f90 文件中设置的。
