---
title: "使用鞘层热流边界条件运行"
nav_order: 2
parent: "边界条件"
grand_parent: "物理选项"
layout: default
render_with_liquid: false
---

# 鞘层热流边界条件

本页涵盖：

- [选择在何处施加鞘层边界条件](#choosing-the-boundaries)；
- [单温度鞘层条件及其实现](#one-temperature-models)；
- [双温度模型中的电子与离子鞘层条件](#two-temperature-models)；
- [掠入射磁力线的处理](#treatment-at-grazing-angles)。

相关的 [$v_\parallel$ 边界条件平滑](./vpar_smooth.md)可用于平滑掠射角附近的 Mach=1 平行速度条件。

## 选择边界 {#choosing-the-boundaries}
借助 `bcs` 结构，可以在任意网格中对选定的边界类型施加鞘层边界条件。边界类型索引与完整的选择规则见[选择边界条件](./choose_boundary_conditions.md)。

例如，要在边界类型 `i` 上施加单温度鞘层热流条件，可使用：

```fortran
bc_natural_open      = .true. ! Enable boundary-integral calls
bcs(i)%dirichlet%T   = .false.
bcs(i)%natural%T     = .true.
gamma_stangeby       = 8.d0
```

把 `i` 替换为需要施加该条件的每个边界类型索引。对每个选定的边界类型都必须单独写出这些设置；不能使用 `bcs(:)`。若离子与电子温度分开演化，则应按[下文](#two-temperature-models)所述改用 `bcs(i)%natural%Ti` 与 `bcs(i)%natural%Te`。

## 单温度模型 {#one-temperature-models}
本节适用于模型 303、333 和 500，以及以单温度运行的模型 600。

在大多数边界类型中，温度默认在边界上固定（Dirichlet 边界条件）。也可以改为把（流向边界的）法向热流设为

$$
\begin{align*}
  \mathbf{Q}\cdot\mathbf{n} &= \gamma_{sh} n_e k_B T_e \mathbf{v}_\parallel\cdot\mathbf{n} \\
\end{align*}
$$

该式见 P. Stangeby，*The Plasma Boundary of Magnetic Fusion Devices*（2000），第 2 章式 2.94。当 $T_e=T_i$ 时，$\gamma_{sh}$ 的典型值为 7–8。

### 该条件的实现方式

用户设置的 `gamma_stangeby` 在内部被转换为 Natural 边界条件中使用的系数 $\gamma_{sh}^{JOREK}$。该转换由 JOREK 能量方程所代表的热流与 Stangeby 热流的匹配得到。

在 JOREK 中，实现的 Natural 边界条件为

$$
\begin{align*}
  -\kappa\nabla T \cdot\mathbf{n} &= (\gamma_{sh}^{JOREK}-1) n_e k_B T \mathbf{v}_\parallel\cdot\mathbf{n} \\
\end{align*}
$$

其中 $T=T_i+T_e$。总的动能与热能 MHD 热流（见 Ideal MHD 或 Goedbloed 的著作）为

$$
\begin{align*}
  \mathbf{Q}\cdot\mathbf{n} &= -\frac{\kappa}{\gamma-1}\nabla T \cdot\mathbf{n} + \frac{\gamma}{\gamma-1}n_e k_B T \mathbf{v}_\parallel\cdot\mathbf{n} + \frac{\rho}{2}v^2 \mathbf{v}_\parallel\cdot\mathbf{n} \\
\end{align*}
$$

当 $T_i=T_e$ 时有 $T=2T_e$。在鞘层入口处，$v^2=c_s^2=\gamma k_BT/m_i$，因此

$$
\begin{align*}
  \frac{\rho}{2}v^2 &= \frac{\gamma}{2}n_e k_BT .
\end{align*}
$$

将代码中实现的边界条件代入 MHD 热流，得到

$$
\begin{align*}
  \mathbf{Q}\cdot\mathbf{n}
  &= \left[
       \frac{\gamma_{sh}^{JOREK}-1+\gamma}{\gamma-1}
       + \frac{\gamma}{2}
     \right]
     n_e k_BT\,\mathbf{v}_\parallel\cdot\mathbf{n} .
\end{align*}
$$

用 JOREK 温度写出的 Stangeby 表达式为

$$
\begin{align*}
  \mathbf{Q}\cdot\mathbf{n}
  &= \frac{\gamma_{sh}}{2}
     n_e k_BT\,\mathbf{v}_\parallel\cdot\mathbf{n} .
\end{align*}
$$

令两式相等，即得代码中实现的转换：

$$
\begin{align*}
  \gamma_{sh}^{JOREK} &= (\gamma-1) \left(\frac{\gamma_{sh}}{2}-1 -\frac{\gamma}{2} \right) \\
\end{align*}
$$

例如，$\gamma=5/3$ 与 `gamma_stangeby = 8.d0` 给出 $\gamma_{sh}^{JOREK}=1.44$。也可以直接通过 `gamma_sheath` 给出内部系数，但 `gamma_stangeby` 表示的是物理上的鞘层传输系数，通常更便于理解。

## 双温度模型 {#two-temperature-models}
本节适用于分别演化离子与电子温度的模型 600。

按[选择边界条件](./choose_boundary_conditions.md)所述，在每个所需的边界类型上分别对每种温度选择 Natural 边界条件。例如：

```fortran
bc_natural_open      = .true.
bcs(i)%dirichlet%Te  = .false.
bcs(i)%natural%Te    = .true.
bcs(i)%dirichlet%Ti  = .false.
bcs(i)%natural%Ti    = .true.
gamma_e_stangeby     = 5.d0  ! Stangeby book end of section 2.8
gamma_i_stangeby     = 3.d0  ! Stangeby book end of section 2.8
```

物理的电子与离子鞘层热流分别写为

$$
\begin{align*}
  \mathbf{Q}_e\cdot\mathbf{n}
    &= \gamma_{sh,e} n_e k_BT_e\,\mathbf{v}_\parallel\cdot\mathbf{n}, \\
  \mathbf{Q}_i\cdot\mathbf{n}
    &= \gamma_{sh,i} n_i k_BT_i\,\mathbf{v}_\parallel\cdot\mathbf{n}.
\end{align*}
$$

JOREK 通过下式实现其传导部分

$$
\begin{align*}
  -\kappa_e\nabla T_e\cdot\mathbf{n}
    &= (\gamma_{sh,e}^{JOREK}-1)n_e k_BT_e\,\mathbf{v}_\parallel\cdot\mathbf{n}, \\
  -\kappa_i\nabla T_i\cdot\mathbf{n}
    &= (\gamma_{sh,i}^{JOREK}-1)n_i k_BT_i\,\mathbf{v}_\parallel\cdot\mathbf{n}.
\end{align*}
$$

### 电子系数

电子能流包含传导与对流两部分的贡献，

$$
\begin{align*}
  \mathbf{Q}_e\cdot\mathbf{n}
  &= -\frac{\kappa_e}{\gamma-1}\nabla T_e\cdot\mathbf{n}
     + \frac{\gamma}{\gamma-1}n_e k_BT_e\,
       \mathbf{v}_\parallel\cdot\mathbf{n} \\
  &= \frac{\gamma_{sh,e}^{JOREK}-1+\gamma}{\gamma-1}
     n_e k_BT_e\,\mathbf{v}_\parallel\cdot\mathbf{n}.
\end{align*}
$$

将该式与 $\gamma_{sh,e}n_e k_BT_e\mathbf{v}_\parallel\cdot\mathbf{n}$ 匹配，得到


$$
\begin{align*}
  \gamma_{sh,e}^{JOREK} &= (\gamma-1) \left(\gamma_{sh,e}-1 \right) \\
\end{align*}
$$

这就是从 `gamma_e_stangeby` 到内部 `gamma_sheath_e` 的转换。

### 离子系数

离子能流还携带整体动能：

$$
\begin{align*}
  \mathbf{Q}_i\cdot\mathbf{n}
  &= -\frac{\kappa_i}{\gamma-1}\nabla T_i\cdot\mathbf{n}
     + \frac{\gamma}{\gamma-1}n_i k_BT_i\,
       \mathbf{v}_\parallel\cdot\mathbf{n}
     + \frac{\rho}{2}v^2\mathbf{v}_\parallel\cdot\mathbf{n}.
\end{align*}
$$

在同样的 $T_i=T_e$ 鞘层假定下，$v^2=c_s^2=\gamma k_B(T_i+T_e)/m_i=2\gamma k_BT_i/m_i$。因此

$$
\begin{align*}
  \frac{\rho}{2}v^2 &= \gamma n_i k_BT_i,
\end{align*}
$$

代入代码中实现的边界条件得到

$$
\begin{align*}
  \mathbf{Q}_i\cdot\mathbf{n}
  &= \left[
       \frac{\gamma_{sh,i}^{JOREK}-1+\gamma}{\gamma-1}
       + \gamma
     \right]
     n_i k_BT_i\,\mathbf{v}_\parallel\cdot\mathbf{n}.
\end{align*}
$$

将该式与物理的离子鞘层热流匹配，得到

$$
\begin{align*}
  \gamma_{sh,i}^{JOREK} &= (\gamma-1) \left(\gamma_{sh,i}-1 - \gamma\right) \\
\end{align*}
$$

这就是从 `gamma_i_stangeby` 到内部 `gamma_sheath_i` 的转换。与电子表达式相比多出的 $\gamma$ 项来自离子动能流。

## 掠射角处的处理 {#treatment-at-grazing-angles}
如本页开头的 Stangeby 公式所示，当 $v_\parallel=0$ 时热流为零。当磁力线完全平行于壁面（掠射角）时可能出现这种情况。此时可能发生人为的能量堆积，这是非物理的。为此可以使用一个最小热流，它完全是扩散性的，取为

$$
\begin{align*}
  \left.\mathbf{Q}\cdot\mathbf{n}\right|_{min} &= \gamma_{sh} n_e k_B T_e c_s \sin (\theta_{min}) = -\frac{\kappa}{\gamma-1}\nabla T \cdot\mathbf{n} \\
\end{align*}
$$

其中声速 $c_s$ 直接由温度计算（而非由 $v_\parallel$）。注意此时总热流因该最小热流而多出一项贡献：

$$
\begin{align*}
  \mathbf{Q}\cdot\mathbf{n} &= \gamma_{sh} n_e k_B T_e \mathbf{v}_\parallel\cdot\mathbf{n} + \left.\mathbf{Q}\cdot\mathbf{n}\right|_{min} \\
\end{align*}
$$

可以在 JOREK 输入文件中通过以下设置选择 $\theta_{min}$ 的取值

```fortran
min_sheath_angle = 1 ! Example of 1 degree (not in radians!)
```

**重要：** 为计算这些通量，网格分辨率或 $\kappa_\perp$ 必须足够大，以分辨边界条件所施加的数值梯度。另请注意，默认情况下该处理也施加于粒子通量：

$$
\begin{align*}
  \mathbf{\Gamma}\cdot\mathbf{n} &= n_i \mathbf{v}_\parallel\cdot\mathbf{n} + \left.\mathbf{\Gamma}\cdot\mathbf{n}\right|_{min} \\
\end{align*}
$$

其中

$$
\begin{align*}
  \left.\mathbf{\Gamma}\cdot\mathbf{n}\right|_{min} &= n_i c_s \sin (\theta_{min}) = -D \nabla n_i\cdot\mathbf{n} \\
\end{align*}
$$

该方法曾用于以下论文：

1. [F. J. Artola et al., 2021, *Plasma Physics and Controlled Fusion* **63**, 064004](https://iopscience.iop.org/article/10.1088/1361-6587/abf620)
