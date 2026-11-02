---
title: "设置平行热传导（ZKpar）"
nav_order: 3
parent: "等离子体函数与系数"
grand_parent: "物理选项"
layout: default
render_with_liquid: false
---

# 设置平行热传导

`ZKpar` 参数控制 JOREK 单位下的平行热传导系数。可使用常数系数，也可使用类 Spitzer–Härm 的温度依赖 $T^{5/2}$。在离子与电子温度分开演化的模型中，两个系数分别独立配置。

本页介绍模型 600 与 750 所使用的通用 `conductivity_parallel` 实现。

## 单温度设置

对于只演化单一 MHD 温度 $T=T_i+T_e$ 的模型，使用 `ZK_par`：

```fortran
ZK_par             = 1.d0  ! Central parallel heat-conduction coefficient
ZKpar_T_dependent  = .true.
ZK_par_max         = 1.d20
```

这里，`ZK_par` 是平衡中心温度 `T_0` 处的系数。当 `ZKpar_T_dependent = .true.` 时，JOREK 计算

$$
\kappa_{\parallel}(T)
  = \kappa_{\parallel,0}
    \left(\frac{T_{\mathrm{corr}}}{T_0}\right)^{5/2}.
$$

## 离子与电子温度分开

当 $T_i$ 与 $T_e$ 分开演化时，使用 `ZK_i_par` 与 `ZK_e_par`：

```fortran
ZK_i_par            = 1.d0 ! Central ion coefficient
ZK_e_par            = 1.d0 ! Central electron coefficient
ZKpar_T_dependent   = .true.
ZK_par_max          = 1.d20
```

通用子程序分别独立作用于每种粒子：

$$
\begin{aligned}
\kappa_{i,\parallel}(T_i)
  &= \kappa_{i,\parallel,0}
     \left(\frac{T_{i,\mathrm{corr}}}{T_{i0}}\right)^{5/2}, \\
\kappa_{e,\parallel}(T_e)
  &= \kappa_{e,\parallel,0}
     \left(\frac{T_{e,\mathrm{corr}}}{T_{e0}}\right)^{5/2}.
\end{aligned}
$$

`ZK_par_max` 由离子与电子系数共用。

## 选择中心系数

JOREK 根据中心等离子体参数计算标称 Spitzer–Härm 系数，并打印到日志中供参考。对温度分开的模型，请查找

```text
ZK_e_par_SpitzerHaerm (not input parameter; printed for reference in JOREK units)
ZK_i_par_SpitzerHaerm (not input parameter; printed for reference in JOREK units)
```

对单温度模型，请查找

```text
ZK_par_SpitzerHaerm (not input parameter; printed for reference in JOREK units)
```

这些是诊断参考值，不是输入参数。JOREK **不会**自动把它们赋给 `ZK_par`、`ZK_i_par` 或 `ZK_e_par`。若要使用标称 Spitzer–Härm 值，请从一次较短的初始化运行中读取该值，并把它复制到相应的输入参数。

## 可用选项

### 常数平行热传导

用以下设置关闭温度标度

```fortran
ZKpar_T_dependent = .false.
```

此时系数等于 `ZK_par`；在温度分开的模型中等于 `ZK_i_par` 与 `ZK_e_par`。下文描述的负温度覆盖逻辑独立求值，仍可替换该值。

### 最大系数

当 $T^{5/2}$ 标度给出的值大于 `ZK_par_max` 时，系数被截断：

$$
\kappa_{\parallel}=\kappa_{\parallel,max}.
$$

用例如以下设置配置该上限

```fortran
ZK_par_max = 1.d20 ! Default
```

该上限主要是一种数值保护措施，用于防止高温区域出现过大的平行热传导。它同时作用于单温度、离子与电子系数。

### 标度中采用的最低温度

$T^{5/2}$ 表达式使用修正后的正温度。温度修正见 [修正负密度／温度](/howto/corr_neg.html)。

当 `ZKpar_T_dependent = .true.` 时，是否冻结系数依据未经修正的原始温度判断。若 $T_{raw}<T_{min,ZK\parallel}$，JOREK 采用

$$
\kappa_{\parallel}
  = \kappa_{\parallel,0}
    \left(\frac{T_{min,ZK\parallel}}{T_0}\right)^{5/2}.
$$

相应的输入为

```fortran
T_min_ZKpar  = 1.d-6 ! Single-temperature model
Ti_min_ZKpar = 1.d-6 ! Ion temperature
Te_min_ZKpar = 1.d-6 ! Electron temperature
```

所有值均采用 JOREK 温度单位。其预置哨兵值为 `-1.d12`；初始化期间，任何小于 `-1.d10` 的值都会被替换为通用的 `T_min` 设置。因此，若不指定这些参数，其有效值即为 `T_min`。


## 输入参数一览

| 参数 | 用途 | 预置值 |
|---|---|---:|
| `ZK_par` | 单温度模型的中心系数 | `1.d0` |
| `ZK_i_par` | 离子中心系数 | `1.d0` |
| `ZK_e_par` | 电子中心系数 | `1.d0` |
| `ZKpar_T_dependent` | 是否施加 $T^{5/2}$ 依赖 | `.true.` |
| `ZK_par_max` | 温度依赖系数的最大值 | `1.d20` |
| `T_min_ZKpar` | 标度中采用的最低单温度 | `-1.d12`，随后被 `T_min` 替换 |
| `Ti_min_ZKpar` | 标度中采用的最低离子温度 | `-1.d12`，随后被 `T_min` 替换 |
| `Te_min_ZKpar` | 标度中采用的最低电子温度 | `-1.d12`，随后被 `T_min` 替换 |
