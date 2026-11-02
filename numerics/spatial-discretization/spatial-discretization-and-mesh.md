---
title: "空间离散与网格"
nav_order: 3
parent: "空间离散"
layout: default
render_with_liquid: false
---

# 极向网格如何使用贝塞尔有限元
构造网格时使用 [JOREK 中的空间离散引言](introduction.md) 中的表述 $(2)$。  
每个单元须具有特定形状，例如：

<img src="../assets/grids/grid_polar.png">

这意味着必须相应地设定 $\vec{v}^{ivl}$ 与 $h^{ij}$，使 [JOREK 中的空间离散引言](introduction.md) 中的表述 $(2)$ 给出所期望的形状。 

$\vec{v}^{ivl}$ 与 $h^{ij}$ 的设定方式取决于网格类型。 

## 托卡马克中的极向网格
托卡马克是轴对称的，因此对每个 $\phi_p$（$p=1\dots \texttt{n_planes}$）的极向网格相同。
这意味着 `n_coord_tor=1`。 

## 仿星器中的网格
在仿星器中，可能希望设 `n_coord_tor>1`，用傅里叶谐波来刻画网格的非轴对称性。