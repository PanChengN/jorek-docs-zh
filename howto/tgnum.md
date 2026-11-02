---
title: "使用 Taylor-Galerkin 稳定化运行"
nav_order: 1
parent: "数值方法与稳定化"
grand_parent: "使用指南"
layout: default
render_with_liquid: false
---

# Taylor–Galerkin 稳定化

Taylor–Galerkin 稳定化在 `model600` 中可用。它针对选定的对流项添加稳定化，每个受支持的方程有各自独立的系数。所有系数默认为零，即关闭相应的稳定化。

当前实现未在 Taylor–Galerkin 项中包含抗磁漂移速度。

## `model600` 的输入参数

与旧模型不同，`model600` **不**使用按方程索引的 `tgnum` 数组。由于 `model600` 是一个模型族，其演化变量取决于编译期扩展，因此改用命名参数：

| 参数 | 方程 | 生效条件 |
|---|---|---|
| `tgnum_u` | 垂直动量 | 始终可用 |
| `tgnum_rho` | 主等离子体密度 | 始终可用 |
| `tgnum_T` | 总温度 | 单温度模型：`with_TiTe=.false.` |
| `tgnum_Ti` | 离子温度 | 双温度模型：`with_TiTe=.true.` |
| `tgnum_Te` | 电子温度 | 双温度模型：`with_TiTe=.true.` |
| `tgnum_vpar` | 平行动量 | `with_vpar=.true.` |
| `tgnum_rhoimp` | 杂质密度 | `with_impurities=.true.` |

通用 namelist 还提供 `tgnum_psi`、`tgnum_zj`、`tgnum_w`、`tgnum_rhon`、`tgnum_nre`、`tgnum_AR`、`tgnum_AZ` 与 `tgnum_A3`。当前 `model600` 的单元矩阵实现不包含由这些参数控制的 Taylor–Galerkin 项，因此在 `model600` 中设置它们没有效果。

## 基本示例

对基础的单温度 `model600` 配置，一个可用的起点是：

```fortran
tgnum_u   = 0.5d0
tgnum_rho = 0.5d0
tgnum_T   = 0.5d0
```

对于含平行速度的双温度配置，使用与已编译方程对应的系数：

```fortran
tgnum_u    = 0.5d0
tgnum_rho  = 0.5d0
tgnum_vpar = 0.5d0
tgnum_Ti   = 0.5d0
tgnum_Te   = 0.5d0
```

若编译了杂质密度扩展，可单独启用其稳定化：

```fortran
tgnum_rhoimp = 0.5d0
```

不要为同一个可执行文件同时设置 `tgnum_T` 与 `tgnum_Ti`／`tgnum_Te`：只有与已编译温度模型对应的那个或那些系数会被使用。

## 系数的选取

`0.5` 是测试时合理的初始值，但并不通用。合适的取值取决于算例、时间步与空间分辨率。

进行包含无稳定化情形的参数扫描，并确认所选系数不会显著改变已解析的物理结果，尤其是线性增长率。只为出现数值不稳定的方程设置系数；各系数不必取相同值。

启动时，JOREK 日志文件会以 `tgnum_u`、`tgnum_rho` 及其他命名参数的形式打印生效值。对编译期已禁用或不受支持的方程，即使打印出非零值，也不代表该稳定化项生效。
