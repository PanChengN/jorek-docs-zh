---
title: "Check Energy Conservation"
nav_order: 2
parent: "诊断与后处理"
layout: default
render_with_liquid: false
---

# 检查能量守恒

实时数据（live-data）诊断可用于监测仿真过程中 JOREK 能量守恒的程度。

> **重要：** 能量守恒诊断必须针对每个模型进行适配。增加物理项可能引入新的能量通道、边界通量、源或汇。为某一模型实现的能量平衡，不可假定对另一模型同样完备。

## 总能量守恒

对于基本的黏性—电阻 MHD 模型，局域总能量平衡可写为

$$
\partial_t w+\nabla\cdot\boldsymbol{\Gamma}=\tau_{\mathrm{nc}},
\tag{1}
$$

其中，略去 $\mu_0$ 因子后，能量密度与能量通量为

$$
\begin{aligned}
w
&\equiv
\frac{\rho}{2}\lvert\boldsymbol{v}\rvert^2
+\frac{p}{\gamma-1}
+\frac{\lvert\boldsymbol{B}\rvert^2}{2}, \\
\boldsymbol{\Gamma}
&\equiv
\left[
\frac{\rho}{2}\lvert\boldsymbol{v}\rvert^2
+\frac{\gamma}{\gamma-1}p
\right]\boldsymbol{v}
+\frac{\boldsymbol{q}}{\gamma-1}
+\boldsymbol{E}\times\boldsymbol{B}.
\end{aligned}
\tag{2}
$$

式 (1) 的右端项 $\tau_{\mathrm{nc}}$ 包含非守恒项，例如加热源与辐射汇。当耗散的磁能或动能被一致地转换为热能时，耗散性的电阻项与黏性项不应出现在 $\tau_{\mathrm{nc}}$ 中。

例如，若 $\eta\neq\eta_{\mathrm{ohmic}}$，则一部分磁能损失不会通过欧姆加热还原为热能。这一不匹配因而计入非守恒平衡。

> **推导参考：** 标准总能量方程可由 MHD 的质量、动量、内能与感应方程组合得到。关于底层 MHD 守恒律的一般性推导与讨论，见 J. P. Goedbloed 与 S. Poedts，[*Principles of Magnetohydrodynamics: With Applications to Laboratory and Astrophysical Plasmas*](https://www.cambridge.org/core/books/principles-of-magnetohydrodynamics/847AF12C94451B41D8F71C1F11EB308A)，Cambridge University Press（2004）。本页侧重 JOREK 诊断及其依赖模型的能量核算，而不重复一般性推导。

将式 (1) 在 JOREK 计算域上积分，得

$$
\partial_t E_{\mathrm{tot}}
=\text{boundary fluxes}
+\text{non-conservative/source terms},
\tag{3}
$$

其中

$$
\begin{aligned}
E_{\mathrm{tot}}
&\equiv \int_V w\,dV, \\
\text{boundary fluxes}
&\equiv
-\oint_S\boldsymbol{\Gamma}\cdot\boldsymbol{n}\,dS, \\
\text{non-conservative/source terms}
&\equiv
\int_V\tau_{\mathrm{nc}}\,dV.
\end{aligned}
\tag{4}
$$

### 绘制总能量平衡

用下列命令绘制式 (3) 的左端与右端：

```bash
jorek_folder/util/plot_live_data.sh -q energy_conservation
```

若能量守恒良好，两条曲线应在预期的数值精度内重合。持续存在的偏差表示存在未计入的能量通道，或存在数值守恒误差。

### 积分能量与时间导数

用下列命令绘制各能量分量及其时间导数：

```bash
jorek_folder/util/plot_live_data.sh -q integrated_energies
jorek_folder/util/plot_live_data.sh -q dEdt
```

图中标签对应于

$$
\begin{aligned}
\text{Total energy}
&\equiv E_{\mathrm{tot}}, \\
\text{Magnetic}
&\equiv
\int_V\frac{\lvert\boldsymbol{B}\rvert^2}{2}\,dV, \\
\text{Thermal energy}
&\equiv
\int_V\frac{p}{\gamma-1}\,dV, \\
\text{Kinetic parallel}
&\equiv
\int_V\frac{\rho}{2}
\lvert\boldsymbol{v}_{\parallel}\rvert^2\,dV, \\
\text{Kinetic perpendicular}
&\equiv
\int_V\frac{\rho}{2}
\lvert\boldsymbol{v}_u\rvert^2\,dV,
\end{aligned}
\tag{5}
$$

其中

$$
\boldsymbol{v}_u=-R^2\nabla u\times\nabla\phi.
$$

### 边界通量

用下列命令绘制各边界通量贡献：

```bash
jorek_folder/util/plot_live_data.sh -q bnd_fluxes
```

各标签对应于

$$
\begin{aligned}
\text{p vn}
&\equiv
\int_S\frac{\gamma}{\gamma-1}
p\,\boldsymbol{v}\cdot\boldsymbol{n}\,dS, \\
\text{kinpar-flux}
&\equiv
\int_S\frac{\rho}{2}\lvert\boldsymbol{v}\rvert^2
\boldsymbol{v}\cdot\boldsymbol{n}\,dS, \\
\text{qn-par}
&\equiv
\int_S
\frac{\boldsymbol{q}_{\parallel}\cdot\boldsymbol{n}}
{\gamma-1}\,dS, \\
\text{qn-perp}
&\equiv
\int_S
\frac{\boldsymbol{q}_{\perp}\cdot\boldsymbol{n}}
{\gamma-1}\,dS.
\end{aligned}
\tag{6}
$$

若在整个计算域边界（而不仅在偏滤器上）施加鞘层边界条件，则这四项通量之和对应于按 Stangeby 表达式给出的流过鞘层的能量。参见[在热流计算中使用鞘层边界条件](../howto/physics_options/boundary_conditions/sheath_heatflux_bc.html)。

在固定边界仿真中，坡印廷通量通常为零。其贡献可通过下文所述的磁能平衡来检查。

### 非守恒项与源项

对于此处所述的 RMHD 诊断，非守恒项与源项为

$$
\text{non-conservative/source terms}
=\int_V
\left[
\frac{S_T}{\gamma-1}
+S_{\mathrm{mag}}
+(\eta_{\mathrm{ohmic}}-\eta)
\lvert\boldsymbol{J}\rvert^2
-\boldsymbol{\nu}_{\parallel}
\cdot\boldsymbol{v}_{\parallel}
\right]\,dV.
\tag{7}
$$

其中：

- $S_T=S_{T_i}+S_{T_e}$ 是温度方程中所用的离子与电子加热源之和。
- $S_{\mathrm{mag}}$ 是与电流源相关的磁能源。
- $(\eta_{\mathrm{ohmic}}-\eta)\lvert\boldsymbol{J}\rvert^2$ 表示电阻性磁能耗散与欧姆加热之间的不匹配。
- 最后一项表示通过平行黏性耗散的能量。

用下列命令绘制这些贡献：

```bash
jorek_folder/util/plot_live_data.sh -q dissipative_terms
```

所有这些量也可通过 [`jorek2_postproc`](../howto/introduction_to_jorek_diagnostics.html#jorek2_postproc) 用 `expressions_int` 命令获取。在 `jorek2_postproc` 中：

```text
help expressions_int
expressions_int
```

第一条命令显示用法信息，第二条列出可用的积分表达式。用 `zeroD_quantities` 命令可获取这些量乃至更多。

## 磁能守恒

记 $W\equiv E_{\mathrm{mag}}$ 为式 (5) 已定义的总能量中的磁能分量。本节为简洁起见取 $\mu_0=1$。

> **模型依赖性：** 以下推导给出的是该诊断所实现的约化 MHD 平衡。各项须与所选模型中启用的方程及物理效应逐一对核。

### 一般平衡

磁能的时间演化为

$$
\partial_t W
=
\int
\mathbf{B}\cdot\partial_t\mathbf{B}
\,dV
=
\int
\mathbf{B}\cdot\nabla\times\partial_t\mathbf{A}
\,dV.
\tag{8}
$$

利用下述恒等式，并取 $\boldsymbol{C}=\partial_t\boldsymbol{A}$，

$$
\mathbf{B}\cdot\nabla\times\mathbf{C}
=
\nabla\cdot(\mathbf{C}\times\mathbf{B})
+
\mathbf{C}\cdot\nabla\times\mathbf{B},
$$

结合安培定律，可得

$$
\partial_t W
=
\int
\partial_t\mathbf{A}\cdot\mathbf{J}
\,dV
+
\int
\nabla\cdot
\left(
\partial_t\mathbf{A}\times\mathbf{B}
\right)
\,dV.
\tag{9}
$$

应用高斯散度定理，

$$
\partial_t W
=
\int
\partial_t\mathbf{A}\cdot\mathbf{J}
\,dV
+
\oint
\partial_t\mathbf{A}\times\mathbf{B}
\cdot d\mathbf{S}.
\tag{10}
$$

对于有限的 JOREK 计算域，必须保留该面积分项。只有当所施加的边界条件使其为零，或边界取得足够远时，它才消失。

将后一形式用电场表示，

$$
\mathbf{E}
=
-\partial_t\mathbf{A}
-
\nabla\Phi,
$$

得到

$$
\partial_t W
=
-
\int
\mathbf{E}\cdot\mathbf{J}
\,dV
-
\oint
\mathbf{E}\times\mathbf{B}
\cdot d\mathbf{S}
-
\int
\nabla\Phi\cdot\mathbf{J}
\,dV
-
\oint
\nabla\Phi\times\mathbf{B}
\cdot d\mathbf{S}.
\tag{11}
$$

最后两项相互抵消。这可通过对体积分项作分部积分并利用下式得到：

$$
\nabla\Phi\cdot\nabla\times\mathbf{B}
=
-\nabla\cdot
\left(
\nabla\Phi\times\mathbf{B}
\right).
$$

由此得到标准形式

$$
\boxed{
\partial_t W
=
-
\int
\mathbf{E}\cdot\mathbf{J}
\,dV
-
\oint
\mathbf{E}\times\mathbf{B}
\cdot d\mathbf{S}
}
\tag{12}
$$

式 (12) 的第一项描述磁能通过 $\boldsymbol{E}\cdot\boldsymbol{J}$ 与等离子体的交换。第二项是穿过边界向外的坡印廷通量。

### 约化 MHD 特化形式

在约化 MHD 中，

$$
\partial_t\mathbf{A}
=
\partial_t A_\phi\,\hat{\mathbf e}_\phi
=
\partial_t\left(\frac{\psi}{R}\right)
\hat{\mathbf e}_\phi.
$$

并利用 JOREK 变量

$$
j = -J_\phi R,
$$

式 (10) 的体积分项变为

$$
\mathcal{V}_{\mathrm{mag}}
\equiv
\int
\partial_t\mathbf{A}\cdot\mathbf{J}
\,dV
=
-
\int
\frac{1}{R^2}
j\,\partial_t\psi
\,dV.
\tag{13}
$$

利用约化 MHD 的极向磁通方程，可将被积函数用演化变量表示，

$$
j\,\partial_t\psi
=
j
\left(
R[\psi,u]
+
\eta(j-j_S)
-
F\frac{\partial u}{\partial\phi}
\right).
\tag{14}
$$

此处 $j_S$ 为电流源，$F=RB_\phi$。符号与变量约定的说明见[极向磁通方程的推导](../physics/base_fluid_models/RMHD/expressions_and_derivations/psi_eq.html)。

由此得到

$$
\mathcal{V}_{\mathrm{mag}}
=
\int
\partial_t\mathbf{A}\cdot\mathbf{J}
\,dV
=
-
\int
[\psi,u]
\frac{j}{R}
\,dV
-
\int
\eta
\left(
\frac{j}{R}
\right)^2
\,dV
+
\int
\eta
\frac{jj_S}{R^2}
\,dV
+
\int
\frac{Fj}{R^2}
\frac{\partial u}{\partial\phi}
\,dV.
\tag{15}
$$

边界通量为

$$
\partial_t\mathbf{A}\times\mathbf{B}
=
\partial_t\psi
\nabla\phi
\times
\left(
\nabla\psi\times\nabla\phi
\right)
=
\frac{\partial_t\psi}{R^2}
\nabla_{\mathrm{pol}}\psi.
\tag{16}
$$

利用磁通方程，边界通量变为

$$
\partial_t\mathbf{A}\times\mathbf{B}
=
\frac{1}{R}
[\psi,u]
\nabla_{\mathrm{pol}}\psi
+
\frac{1}{R^2}
\left(
\eta(j-j_S)
-
F\frac{\partial u}{\partial\phi}
\right)
\nabla_{\mathrm{pol}}\psi.
\tag{17}
$$

可以证明，第一项为

$$
-\mathbf{v}_{\perp}^{\mathrm{pol}}
B_{\mathrm{pol}}^2.
$$

将式 (15) 的体积贡献 $\mathcal{V}_{\mathrm{mag}}$ 与式 (16) 的边界贡献合并，即得磁能平衡（不再重复展开后的体积分项）：

$$
\boxed{
\partial_t W
=
\mathcal{V}_{\mathrm{mag}}
+
\oint
\frac{\partial_t\psi}{R^2}
\nabla_{\mathrm{pol}}\psi
\cdot\mathbf{n}
\,dS
}
\tag{18}
$$

### 诊断标签

运行

```bash
jorek_folder/util/plot_live_data.sh -q mag_energy_balance
```

即可比较式 (18) 中各项随时间的变化。

诊断名称与推导的对应关系如下：

| 实时数据标签 | 磁能平衡中的项 |
|:---|:---|
| `magSource` | 式 (15) 的第三项，表示电流源 $j_S$ 输入的磁能。 |
| `Ohmic` | 式 (15) 的第二项，表示磁能的电阻性损失。 |
| `JxB.v` | 式 (15) 中第一项与第四项之和，表示磁能向动能的转移。 |
| `Poynting` | 式 (18) 中的面积分，表示穿过计算域边界的磁能。 |
| `dWmagdt` | 式 (18) 的左端，$\partial_t W$。 |
| `sum all...` | `magSource + Ohmic + JxB.v + Poynting` 之和，即式 (18) 完整的右端。 |

若平衡闭合，`dWmagdt` 与 `sum all...` 应在时间、空间与诊断积分精度内一致。系统性偏差表明缺少某个物理项、系数不一致、存在未计入的边界贡献，或数值精度不足。
