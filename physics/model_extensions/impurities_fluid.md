---
title: "杂质——流体模型"
nav_order: 1
parent: "杂质"
grand_parent: "模型扩展"
layout: default
render_with_liquid: false
---

# 杂质流体模型

这类模型包含一个对应杂质密度的场（在代码中为变量 8，即 var_rhoimp）。本页适用于专用杂质模型（如模型 501/502），以及它们的模块化通用模型 600。

此类模型可用于例如 [SPI 模拟](spi_tutorial) 或 [MGI 模拟](mgi_tutorial)。

## 模型 501/502

**重要提示：** 目前使用模型 501/502 时应设置 `tau_ic = 0.`，即不应包含抗磁效应（这些效应尚未被正确实现）。

### 变量的定义

**变量 5：** 在模型 501/502 中，$\rho$（变量 5）是**总**质量密度，包含所有组分（但忽略电子质量）。即：

\begin{aligned}
  \rho = \rho_i + \rho_{imp}
\end{aligned}

其中 $\rho_i$ 是主离子密度，$\rho_{imp}$ 是包含所有电荷态的杂质密度。

**压力：** 在模型 501/502 中，能量方程与动量方程中自然出现的压力是包含所有组分的**总**压力 $p$。在模型 501 中，假定所有组分具有共同的温度 $T/2$。因此压力为（此处暂时使用非 JOREK 归一化，以避免混淆）$p=n_{tot}T/2$，其中 $n_{tot}$ 是总粒子密度：$n_{tot}=n_{i}+n_{e}+n_{imp}$。由准中性条件有 $n_e=n_i+\langle Z \rangle_{imp}n_{imp}$。因此，$n_{tot}=2n_i+(\langle Z \rangle_{imp}+1)n_{imp}$。又因 $n_i=\rho_i/m_i$、$n_{imp}=\rho_{imp}/m_{imp}$，故：$n_{tot}=[2\rho_i+\frac{(\langle Z \rangle_{imp}+1)m_i}{m_{imp}}\rho_{imp}]/m_i=[2\rho+(\frac{(\langle Z \rangle_{imp}+1)m_i}{m_{imp}}-2)\rho_{imp}]/m_i$。于是压力可表示为（以下为 JOREK 单位）：

\begin{aligned}
  p=(\rho+\alpha_{imp}\rho_{imp})T/m_{i}
\end{aligned}

其中定义 $\alpha_{imp} \equiv \frac{(\langle Z \rangle_{imp}+1)m_i}{2m_{imp}}-1$。注意我们将假定 $\langle Z \rangle_{imp}=\langle Z \rangle_{imp}(T)$，从而 $\alpha_{imp}=\alpha_{imp}(T)$。

**变量 8：** 在模型 501/502 中，变量 8 是 $\rho_{imp}$，即包含所有电荷态的杂质质量密度。

### 归一化

| SI 单位与归一化单位之间的换算 | | 量的说明／备注 |
|--------------------------------------------|------|----------------------------------------|
| $\rho_\mathrm{SI}~[\mathrm{kg/m^3}]$ | $=\rho\;\rho_0$ | 总质量密度 |
| $\rho_\mathrm{imp,SI}~[\mathrm{kg/m^3}]$ | $=\rho_\mathrm{imp}\;\rho_0$ | 杂质质量密度 |
| $n_\mathrm{i,SI}~[\mathrm{m^{-3}}]$ | $=(\rho - \rho_\mathrm{imp})\;n_0$ | 主离子数密度 |
| $n_\mathrm{imp,SI}~[\mathrm{m^{-3}}]$ | $=\rho_\mathrm{imp}\;n_0\;\mu_{imp}$ | 杂质数密度 |
| $n_\mathrm{e,SI}~[\mathrm{m^{-3}}]$ | $= n_\mathrm{i,SI}\;+\;\langle Z \rangle_{imp}\;n_\mathrm{imp,SI}$ | 电子数密度 |

**其中定义：**

| 符号 | 表达式 | 备注 |
|--------|------------|---------|
| $n_0~[m^{-3}]$ | `central_density` $\cdot 10^{20}$ | `central_density` 在 `preset_parameters.f90` 中有默认值，应在输入文件中指定 |
| $\rho_0~[kg\;m^{-3}]$ | `central_mass` $\cdot n_0 \cdot m_\text{AMU}$ | `central_mass` 在 `preset_parameters.f90` 中有默认值，应在输入文件中指定 |
| $\mu_\mathrm{imp}~[1]$ | `m_i_over_m_imp` $ = m_\mathrm{i}/m_\mathrm{imp}$ | `m_i_over_m_imp` 由杂质种类确定。 |

### 方程

<!--
- [Di 的笔记](note501.pdf)
- [Di 关于模型 502 的笔记](note502.pdf)
- [Boniface 的笔记](mgi_spi_premixed_modelingdiag.pdf)
-->

#### 涡量方程（式 2）

完整的 MHD 动量方程写作：

\begin{aligned}
\rho (\partial_t + \mathbf{v} \cdot \nabla) \mathbf{v}  = \mathbf{j} \times \mathbf{B} - \nabla p + \nu \Delta \mathbf{v} - (\partial_t \rho + \nabla \cdot (\rho \mathbf{v})) \mathbf{v} + S_{\rho_{imp}} \mathbf{v}_{imp}
\end{aligned}

其中 $\mathbf{v}_{imp}$ 是由 $S_{\rho_{imp}}$ 源项注入的杂质的速度。注意右端出现了 $-\left(\partial_t \rho + \nabla \cdot (\rho \mathbf{v})\right) \mathbf{v}$ 这一项。该项保证动量守恒，目前（21/08/18）JOREK 的其他模型中尚无此项，但将来可能会加入。

约化 MHD 涡量方程由将算子 $\nabla\phi\cdot\nabla\times(R^2...)$ 作用于动量方程得到。不含 $-\left(\partial_t \rho + \nabla \cdot (\rho \mathbf{v})\right) \mathbf{v}$ 项时的结果见[此处](reduced_mhd)。该项在涡量方程右端给出一个附加项 $-\nabla \cdot \left[ R^2 (\partial_t \rho + \nabla \cdot (\rho \mathbf{v})) \nabla_{pol} u \right] $（我们忽略了 $- (\partial_t \rho + \nabla \cdot (\rho \mathbf{v})) v_{||}\mathbf{B} $ 的贡献）。在弱形式下，该项变为 $ \int - u^* \nabla \cdot \left[ R^2 (\partial_t \rho + \nabla \cdot (\rho \mathbf{v})) \nabla_{pol} u \right] dV$（其中 $u^*$ 为检验函数），分部积分后可化为 $ \int R^2 (\partial_t \rho + \nabla \cdot (\rho \mathbf{v})) (\nabla u^* \cdot \nabla_{pol} u) dV $。为实现该项，需要展开 $\nabla \cdot (\rho \mathbf{v})$，展开过程见[此处](div_rho_v)。

#### 电流的定义（式 3）

该方程与其他 JOREK [约化 MHD 模型](reduced_mhd) 中的相同：
\begin{aligned}
  j = \Delta^*\psi
\end{aligned}

#### 涡量的定义（式 4）

该方程与其他 JOREK [约化 MHD 模型](reduced_mhd) 中的相同：
\begin{aligned}
  \omega = \Delta_\text{pol} u
\end{aligned}

#### 全局连续性方程（式 5）

全局连续性方程，即描述总质量密度演化的方程，写作：

\begin{aligned}
\partial_t \rho = - \nabla \cdot (\rho \mathbf{v}) + \nabla \cdot (D_i \nabla (\rho - \rho_{imp})) + \nabla \cdot (D_{imp} \nabla \rho_{imp}) + S_{\rho_i} + S_{\rho_{imp}}
\end{aligned}

对于例如 [SPI](spi_tutorial) 或 [MGI 模拟](mgi_tutorial) 而言，模型的一个重要方面是杂质藉以注入的体源项 $S_{\rho_{imp}}$。关于该项参数化的一些信息见[此处](particle_source_parameterization)。

#### 压力方程（式 6）

压力方程大致写作：

\begin{aligned}
\partial_t p = - \mathbf{v} \cdot \nabla p - \gamma p \nabla \cdot \mathbf{v} + Conduction + Joule - Radiation - Ionization
\end{aligned}

这里假定所有组分具有相同的热容比 $\gamma$，若考虑单原子杂质与主离子（这正是我们的计划），则该假定成立。注意此处 $p=(\rho+\alpha_{imp}\rho_{imp})T$（见上文）。

#### 平行动量方程（式 7）

将 $\mathbf{B} \cdot (...) $ 作用于完整的 MHD 动量方程（已在上文涡量方程一节写出），即得平行动量方程。不含 $-\left(\partial_t \rho + \nabla \cdot (\rho \mathbf{v})\right) \mathbf{v}$ 项时的结果见[此处](reduced_mhd)。为实现后者，采用近似 $\mathbf{B} \cdot \mathbf{v} \approx B^2 v_{\parallel} \approx \frac{F_0^2}{R^2} v_{\parallel} $，从直觉上看这在约化 MHD 中是合理的。因此在弱形式下，平行动量方程得到右端项 $ \int -(\partial_t \rho + \nabla \cdot (\rho \mathbf{v})) B^2 v_{parallel} $。为实现该项，需要展开 $\nabla \cdot (\rho \mathbf{v})$，展开过程见[此处](div_rho_v)。

#### 杂质连续性方程（式 8）

杂质连续性方程，即描述杂质质量密度（含所有电荷态）演化的方程，写作：

\begin{aligned}
\partial_t \rho_{imp} = - \nabla \cdot (\rho_{imp} \mathbf{v}) + \nabla \cdot (D_{imp} \nabla \rho_{imp}) + S_{\rho_{imp}}
\end{aligned}

如上文所述，对于例如 [SPI](spi_tutorial) 或 [MGI 模拟](mgi_tutorial) 而言，模型的一个重要方面是杂质藉以注入的体源项 $S_{\rho_{imp}}$。关于该项参数化的一些信息见[此处](particle_source_parameterization)。

### 方程的离散实现

- [全局连续性方程](model_501_global_continuity)
- [感应方程](model_501_induction)
- [涡量方程](model_501_vorticity)
- [压力方程](model_501_pressure_eq)
- [平行动量方程](model_501_parallel_momentum)
- [杂质连续性方程](model_501_impurity_continuity)
- **注：** 电流与涡量定义所用的方程与其他模型相同

### 原子系数

原子系数取自 [ADAS 数据库](adas.md)。模型 501/502 的"基线"版本假定体系处于日冕平衡（Coronal Equilibrium），但近期已实现了非平衡情形（见下文）。

### 非平衡杂质

JOREK 中已实现基于粒子的非平衡模型，与 501/502 和 600 兼容。
见[碰撞辐射杂质模型的标记粒子表示](impurities_marker.md)。
