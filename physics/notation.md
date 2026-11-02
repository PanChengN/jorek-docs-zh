---
title: "记号约定"
nav_order: 1
parent: "物理模型"
layout: default
render_with_liquid: false
---

# 记号约定

## 一般约定

| 符号 | 说明 |
| --- | --- |
| S   | 标量以常规字体排印 | 
| $\mathbf{V}$ | 矢量以粗体排印 |
| $V_1, V_2, V_3$ | 矢量 $\mathbf{V}$ 的协变分量（除特别说明外，均指柱坐标） |
| $V^1, V^2, V^3$ | 矢量 $\mathbf{V}$ 的逆变分量（除特别说明外，均指柱坐标） |
| $V_R, V_Z, V_\phi$ | 物理柱坐标分量（即对应于归一化基矢量的分量） | 
| $\mathbf{T}, T_{\alpha \beta}, T^{\alpha \beta}$ | 张量以粗体排印，张量分量以常规字体排印 | 

适用爱因斯坦求和约定，即 $a_i b^i \equiv \sum_i a_i b^i$。

## 坐标相关符号

| 符号 | 说明 |
| --- | --- |
| $x, y, z$ | 笛卡尔坐标 [(1)](#footnotes) |
| $R, Z, \phi$ | 柱坐标 |
| $u^1\equiv R, u^2\equiv Z, u^3\equiv\phi$ | 柱坐标 |
| $\mathbf{a}_1, \mathbf{a}_2, \mathbf{a}_3$ | 协变基矢量（非单位矢量；除特别说明外，均指柱坐标） |
| $\mathbf{a}^1, \mathbf{a}^2, \mathbf{a}^3$ | 逆变基矢量（非单位矢量；除特别说明外，均指柱坐标） |
| $\mathbf{e}_1, \mathbf{e}_2, \mathbf{e}_3$ | 归一化协变基矢量（除特别说明外，均指柱坐标） [(2)](#footnotes) |
| $\mathbf{e}^1, \mathbf{e}^2, \mathbf{e}^3$ | 归一化逆变基矢量（除特别说明外，均指柱坐标） [(2)](#footnotes) |
| $g_{ij}, g^{ij}$ | 协变与逆变度规张量分量 |
| $g$ | 协变度规张量的行列式 $g=\textrm{det}(\mathbf{g}_{ij})$ |
| $J$ | 雅可比（$J^2=g$） |
| $\partial_\alpha U\equiv\partial U / \partial u^\alpha$ | 导数的简写（例如 $\partial_1 U\equiv\partial U/\partial R$） |

另请参阅[坐标系](coordinates)页面。

## 物理量

| 符号 | 说明 |
| --- | --- |
| $\psi$ | 极向磁通 |
| $\psi_N$ | 归一化极向磁通 $\psi_N=(\psi - \psi_\text{axis})/(\psi_\text{bnd}-\psi_\text{axis})$ |
| $\mathbf{B}$ | 磁场矢量 |
| $\mathbf{b}$ | 归一化磁场矢量 $\mathbf{b}=\mathbf{B}/\vert B\vert$ |
| ... | ... |

另请参阅[模型](base_fluid_models/base_fluid_models.md)页面。

## 脚注
  - 在 element_matrix 例程中，x 与 y 常被用作 R 与 Z 的同义词，切勿与笛卡尔坐标混淆。 
  - 在柱坐标系中，归一化协变基矢量与归一化逆变基矢量自然是相同的。
