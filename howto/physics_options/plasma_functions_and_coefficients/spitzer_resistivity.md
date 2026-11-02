---
title: "设置电阻率"
nav_order: 2
parent: "等离子体函数与系数"
grand_parent: "物理选项"
layout: default
render_with_liquid: false
---
# 设置电阻率

输入参数 `eta` 设定平衡等离子体中心（$\psi_n=0$）处的电阻率，单位为 JOREK 单位。等离子体其余位置的电阻率可以是常数，也可以遵循类 Spitzer 的温度依赖。还可以计入库仑对数的变化，以及在杂质模型中计入 $Z_{eff}$ 的变化。

## 简单的类 Spitzer 设置

典型的输入设置为

```fortran
eta                  = 1.d-8 ! Central resistivity in JOREK units
eta_T_dependent      = .true.
eta_coul_log_dep     = .true.
T_max_eta            = 1.d99
```

这里，`eta` 是平衡中心电子温度 $T_{e0}$ 处的值。当 `eta_T_dependent = .true.` 时，JOREK 计算

$$
\eta_T = \eta\left(\frac{T_{e,\mathrm{corr}}}{T_{e0}}\right)^{-3/2}.
$$

对温度分开的模型，使用演化得到的 $T_e$。对单温度模型，JOREK 取 $T_e=T/2$；因子 2 在上式的比值中相消。

若 `eta_coul_log_dep = .true.`，结果还会额外乘以按中心值归一化的局部库仑对数：

$$
\eta_T \longrightarrow \eta_T\frac{\ln\Lambda}{\ln\Lambda_0}.
$$

因此，即使启用了库仑对数依赖，`eta` 仍保持为中心值。该选项目前可用于调用通用电阻率函数的模型，包括模型 600 与 750。

## 选择 `eta`

用作参考的物理 Spitzer 电阻率为

$$
\eta_{\mathrm{Spitzer}}^{SI}
  = 1.65\times10^{-9}\,\ln\Lambda_0
    \left(T_{e0}[\mathrm{keV}]\right)^{-3/2}\;\Omega\,\mathrm{m}.
$$

需要用[归一化](../../../physics/normalization.md)将其换算为 JOREK 单位。为方便起见，日志文件中会给出

```text
eta_Spitzer (not input parameter; printed for reference in JOREK units)
```

`eta_Spitzer` 是诊断参考值，不是输入参数：JOREK **不会**自动把它赋给 `eta`。若要使用标称 Spitzer 值，请从一次较短的初始化运行中读取打印值，并在输入文件中把 `eta` 设为该值。

也可以有意选择不同的 `eta` 以改变电阻时间尺度，前提是已理解其对 Lundquist 数与欧姆加热的影响。

## 可用选项

### 常数电阻率

若要使电阻率在温度与密度上均为常数，请关闭两项依赖：

```fortran
eta                  = 1.d-6
eta_T_dependent      = .false.
eta_coul_log_dep     = .false.
```

当 `eta_coul_log_dep` 仍处于启用状态时，仅关闭 `eta_T_dependent` 不足以得到严格常数的剖面，因为 $\ln\Lambda$ 的局部变化仍会改变 `eta`。

### 温度依赖的电阻率

用以下设置启用类 Spitzer 的 $T_e^{-3/2}$ 标度

```fortran
eta_T_dependent = .true.
```

该函数使用修正后的正温度 $T_{e,\mathrm{corr}}$。该修正避免以负温度计算非整数次幂；参见[修正负密度／温度](/howto/corr_neg.html)。

当原始温度低于 `T_min` 时，电阻率冻结在

$$
\eta_T = \eta\left(\frac{T_{min}}{T_{e0}}\right)^{-3/2}.
$$

这样可避免在极冷或数值上为负温度的区域出现无界电阻率。

### 温度上限截断

`T_max_eta` 限制 Spitzer 标度中所用的温度：

```fortran
T_max_eta = 1.d99 ! Effectively no upper cutoff (default)
```

当 $T_{e,\mathrm{corr}}>T_{max,\eta}$ 时，JOREK 采用

$$
\eta_T = \eta\left(\frac{T_{max,\eta}}{T_{e0}}\right)^{-3/2}.
$$

这在最热的区域内给出了电阻率的下限。`T_max_eta` 采用与演化温度相同的归一化温度单位，只有在特定的数值原因下才应修改。

### 库仑对数依赖

用以下设置启用 $\ln\Lambda$ 中局部密度与温度的影响

```fortran
eta_coul_log_dep = .true.
```

通用等离子体函数实现中，$n_e$ 以 $\mathrm{cm}^{-3}$ 计算，修正后的 $T_e$ 以 eV 计算。它采用

$$
\ln\Lambda =
\begin{cases}
23.0 - \frac{1}{2}\ln n_e + \frac{3}{2}\ln T_e,
  & T_e < 10\;\mathrm{eV}, \\
24.1513 - \frac{1}{2}\ln n_e + \ln T_e,
  & T_e \ge 10\;\mathrm{eV}.
\end{cases}
$$

传入该表达式的密度以 $10^{10}\;\mathrm{cm}^{-3}$ 为下限，以防止对数出现非物理值。

### 杂质修正

当所选模型演化杂质时，温度依赖的电阻率会自动乘以一个 $Z_{eff}$ 修正。通用等离子体函数中实现的因子为

$$
f(Z_{eff}) =
\frac{
  Z_{eff}\left(1+1.198Z_{eff}+0.222Z_{eff}^2\right)
  }{
  1+2.966Z_{eff}+0.753Z_{eff}^2
  }\left[
\frac{1+1.198+0.222}{1+2.966+0.753}
\right]^{-1},
$$

该因子经归一化使 $f(1)=1$。当前实现在 `eta_T_dependent = .true.` 时施加该因子。

## 输入参数一览

| 参数 | 用途 | 默认值 |
|---|---|---:|
| `eta` | JOREK 单位下的中心电阻率 | `1.d-5` |
| `eta_T_dependent` | 是否施加 $T_e^{-3/2}$ 依赖 | `.true.` |
| `eta_coul_log_dep` | 在支持处乘以 $\ln\Lambda/\ln\Lambda_0$ | `.true.` |
| `T_max_eta` | 用于计算 `eta` 的温度上限 | `1.d99` |

## 其他考虑

* 在 RMHD 中形式上不存在极向电阻率
* 新经典效应可能通过俘获粒子增大电阻率

俘获电子不携带电流，因此新经典修正会引入额外的径向依赖：
$$
\eta_{||,neo}=\eta_{||}\;\left(1-\sqrt{r/R_0}\right)^{-2}
$$
对 $r/R=0.3$，修正因子为 $5$，但这还取决于碰撞率与去俘获时间尺度。
