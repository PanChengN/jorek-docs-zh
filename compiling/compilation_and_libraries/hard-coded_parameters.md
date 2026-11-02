---
title: "硬编码参数"
nav_order: 3
parent: "编译与依赖库"
grand_parent: "编译与运行"
layout: default
render_with_liquid: false
---

# JOREK 中的硬编码参数

## 物理模型

第一个“硬编码参数”是 **JOREK 物理模型编号**。它在 Makefile.inc 文件中设定。

其余硬编码参数由位于模型目录 models/modelXXX/ 中的 mod_parameters.f90 文件设定：

| 参数 | 说明 |
|----------|--------|
| n_tor | 环向模数个数（cos 与 sin 分别计数） |
| n_period | 周期性（n_period=1 表示完整环） |
| n_plane | 环向平面数；n_plane 必须 >= 2*(n_tor-1) |
| n_vertex_max | 不要修改 |
| n_nodes_max | 网格节点的最大数量 |
| n_elements_max | 网格单元的最大数量（二维 Bezier） |
| n_boundary_max | 边界单元的最大数量（一维 Bezier） |
| n_pieces_max | 磁面表示中的最大分段数 |

修改硬编码参数后，应始终执行：

```bash
make clean
```

更换模型后应执行：

```bash
make cleanall
```

## 脚本 config.sh

脚本

```bash
./util/config.sh
```

在 trunk 目录下调用，可**显示硬编码参数的取值**。将得到类似如下的输出：

```text
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
```

同一脚本也可**修改硬编码参数**：

```bash
./util/config.sh model=303 n_tor=3 n_period=8 n_plane=8
```

**重要：** 用该脚本更换模型时，务必确认其他参数同样正确，因为它们在各模型专属的 mod_parameters.f90 文件中分别设定。
