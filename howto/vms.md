---
title: "变分多尺度（VMS）稳定化"
nav_order: 6
parent: "数值方法与稳定化"
grand_parent: "使用指南"
layout: default
render_with_liquid: false
---

# 变分多尺度（VMS）稳定化

VMS 稳定化目前已在 full MHD 模型 750 中实现。

## 用法

在 JOREK 输入文件中设置 `use_vms = .true.`，并为各演化变量的系数赋予合适的值：

```fortran
use_vms = .true.

vms_coeff_AR     = 1.d-3
vms_coeff_AZ     = 1.d-3
vms_coeff_A3     = 1.d-3
vms_coeff_UR     = 1.d-3
vms_coeff_UZ     = 1.d-3
vms_coeff_Up     = 1.d-3
vms_coeff_rho    = 1.d-3
vms_coeff_T      = 1.d-3
vms_coeff_Ti     = 1.d-3
vms_coeff_Te     = 1.d-3
vms_coeff_rhon   = 1.d-3
vms_coeff_rhoimp = 1.d-3
```

预设值为 `use_vms = .false.`，因此 VMS 稳定化默认关闭。对 `n_order = 3`，建议每个生效变量的起始取值为 `0.001`。

## 推导与实现

设 $\mathcal{R}(\boldsymbol{w})$ 为残差

$$
\begin{aligned}
\mathcal{R}(\boldsymbol{w})
&:=\mathbb{M}(\boldsymbol{w})\partial_t\boldsymbol{w}
  +\mathcal{L}(\boldsymbol{w}) \\
&=\mathbb{M}(\boldsymbol{w})\partial_t\boldsymbol{w}
  +\mathbb{C}\nabla\boldsymbol{w}
  -\nabla\cdot(\mathbb{D}\nabla\boldsymbol{w})
  -\mathbb{S}(\boldsymbol{w})
=0.
\end{aligned}
$$

此处 $\boldsymbol{w}\subset\boldsymbol{W}$ 构成一个定义良好的 MHD 方程组，且

$$
\boldsymbol{W}
=\left(
A_R,\,A_Z,\,\psi,\,u_R,\,u_Z,\,u_\phi,\,
\rho,\,T,\,T_i,\,T_e,\,\rho_n,\,\rho_f
\right)^\mathrm{T}.
$$

该偏微分方程组的 Galerkin 有限元方法（FEM）为

$$
\int \boldsymbol{w}^\ast\cdot\mathcal{R}(\boldsymbol{w})\,d\Omega=0.
$$

VMS 稳定化的有限元表述为

$$
\int \boldsymbol{w}^\ast\cdot\mathcal{R}(\boldsymbol{w})\,d\Omega
-\int
\mathcal{L}^\mathrm{T}\boldsymbol{w}^\ast
\cdot\mathbb{T}\mathcal{R}(\boldsymbol{w})\,d\Omega'
=0.
$$

第一项为有限元弱形式，第二项为 VMS 稳定化。

> **实现说明：** 在隐式方法中，假定 $\mathcal{L}^\mathrm{T}\boldsymbol{w}^\ast$ 取上一时间步的值，因此不计入其雅可比矩阵。

## 残差与实际困难

VMS 稳定化项中出现的残差近似为

$$
\mathcal{R}
\approx\widetilde{\mathcal{R}}
=\mathbb{C}\nabla\boldsymbol{w}
-\nabla\cdot(\mathbb{D}\nabla\boldsymbol{w})
-\mathbb{S}(\boldsymbol{w}).
$$

作了如下简化：

- 忽略瞬态（时间导数）项。
- 为简化起见，忽略 $\boldsymbol{J}\times\boldsymbol{B}$ 项。若要包含该项，需要扩展 Fourier 方法。
- 为简化起见，忽略平行于磁场的扩散系数。

## 稳定化算子

考虑含杂质的双温度 full MHD 模型，其偏微分方程算子为

$$
\mathcal{L}=
\begin{bmatrix}
-(\boldsymbol{v}\times\nabla\times)+\nabla^2
  & \boldsymbol{0} & 0 & 0 & 0 & 0 \\
\boldsymbol{0}
  & \rho\boldsymbol{v}\cdot\nabla-\nabla^2
  & (T_i+T_e)\nabla & \rho\nabla & \rho\nabla & 0 \\
\boldsymbol{0}
  & \rho\nabla\cdot
  & \boldsymbol{v}\cdot\nabla-\nabla^2 & 0 & 0 & 0 \\
\boldsymbol{0}
  & \gamma\rho T_i\nabla\cdot
  & T_i\boldsymbol{v}\cdot\nabla
  & \rho_{\mathrm{eff}}^i\boldsymbol{v}\cdot\nabla
    -\nabla\cdot(\boldsymbol{\kappa}_i\nabla)
  & 0
  & T_{\mathrm{eff}}^i\boldsymbol{v}\cdot\nabla \\
\boldsymbol{0}
  & \gamma\rho T_e\nabla\cdot
  & 0
  & T_e\boldsymbol{v}\cdot\nabla
  & \rho_{\mathrm{eff}}^i\boldsymbol{v}\cdot\nabla
    -\nabla\cdot(\boldsymbol{\kappa}_e\nabla)
  & T_{\mathrm{eff}}^e\boldsymbol{v}\cdot\nabla \\
\boldsymbol{0}
  & \rho_f\nabla\cdot
  & 0 & 0 & 0
  & \boldsymbol{v}\cdot\nabla-\nabla\cdot(\mathbb{D}_f\nabla)
\end{bmatrix}.
$$

## 稳定化矩阵

最简单的选择是对角稳定化矩阵：

$$
\mathbb{T}
=\frac{h_e}{\max(\lambda_e)}
\begin{bmatrix}
C_{A_R} & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
0 & C_{A_Z} & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & C_{A_3} & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & C_{v_R} & 0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & C_{v_Z} & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & C_{v_\phi} & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & C_{\rho} & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & C_{T_i} & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & C_{T_e} & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & C_{\rho_f}
\end{bmatrix}.
$$

其中 $h_e$ 为单元特征尺寸，$\lambda_e$ 为逐单元计算的 Alfvén 波速。实数参数 $C_{A_R}$ 等对应 `vms_coeff_AR` 之类的输入参数。

原则上，稳定化矩阵应为

$$
\mathbb{T}
=\mathcal{L}^{-1}
=\left(
\mathbb{M}\partial_t
+\mathbb{A}\nabla
+\nabla\cdot(\mathbb{D}\nabla)
\right)^{-1}.
$$

然而，计算该表达式比求解原问题更困难。

## 补充说明

- 残差的不同表述与近似会产生一个 VMS 稳定化方法系列。
- 稳定化算子的不同选择同样会产生一个方法系列。例如，最简单的选择是只取 $\mathcal{L}$ 的对角部分而不含扩散项。
- 细节与演示见 [Computers & Mathematics with Applications (2023)](https://doi.org/10.1016/j.camwa.2023.04.034)。
