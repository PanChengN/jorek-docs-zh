---
title: "JET"
nav_order: 2
parent: "装置配置"
layout: default
render_with_liquid: false
---

# 模拟 JET 的相关信息

## 等离子体电流与环向场的方向

JET 的标准运行时，从上方俯视 $I_p$ 与 $B_t$ 均沿顺时针方向。在 JOREK 中，由于 $\mathbf{B} = \nabla\psi\times \nabla\phi + F~\nabla\phi$ 且 $\phi$ 同样沿顺时针方向，这意味着应有 $\psi_{axis}>\psi_{bnd}$。


## 从 EFIT 到 JOREK

由 EFIT 重建的平衡数据可用 [eqdsk2jorek.f90](../howto/eqdsk2jorek) 转换为 JOREK 输入数据。

**注：** EFIT 中 $\psi$ 的符号约定（至少对 JET 而言）与 JOREK 相反，即标准 JET 平衡有 $\psi_{axis}^{EFIT}<\psi_{bnd}^{EFIT}$。因此取 $\psi_{JOREK}=-\psi_{EFIT}$，$ff^\prime_{JOREK}=-ff^\prime_{EFIT}$。

## MGI 与 SPI 相关信息

S. Jachmich 的幻灯片（未公开），含 **MGI 实验**信息，并标出各破裂缓解阀（DMV）的位置。

2019 年安装的 **SPI 系统**取代了 DMV1。因此在 JOREK 坐标下其环向位置为 $\phi=6.08$，这里 $\phi=0$ 对应第 1 八分之一扇区的中心。SPI 系统的部分信息见 L. Baylor 的这份[幻灯片](https://tsdw.pppl.gov/Talks/2017/Lexar/Monday%20Session%201/Baylor.pdf)。

## 合成诊断

- [KB5 辐射热计](jet_synthetic_KB5_bolometer)

## JET ELM 教程

- [JET ELM 教程](jet_tutorial)
