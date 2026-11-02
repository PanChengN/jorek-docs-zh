---
title: "含新经典效应运行"
nav_order: 3
parent: "物理项激活"
grand_parent: "物理选项"
layout: default
render_with_liquid: false
---

# 如何使用新经典系数剖面运行 JOREK

## 1. 计算新经典系数剖面

### 1.1. 获取用于计算系数的 JOREK 数据

以 `neo=.false.` 运行 JOREK 平衡，会生成以下文件：

- `qprofile.dat`，由 `qprofile` 子程序计算，包含归一化极向磁通 $\psi_{N,\mathrm{pol}}$ 与安全因子 $q(\psi_N)$。
- `T_rho_profiles.dat`，由 `equilibrium` 子程序计算，以 JOREK 单位给出 $T(\psi_N)$ 与 $\rho(\psi_N)$。

新经典系数的计算需要：

- 归一化极向磁通 $\psi_N$；
- 安全因子 $q(\psi_N)$；
- 电子温度 $T_e(\psi_N)$；
- 电子密度 $N_e(\psi_N)$。

在 JOREK 中，极向磁通及相应的安全因子剖面由 `qprofile` 子程序计算，该子程序由 `equilibrium` 调用并写出 `qprofile.dat`。依赖 $\psi$ 的温度与密度剖面必须与 $q(\psi_N)$ 具有相同的点数。`equilibrium` 子程序将这些剖面写入 ASCII 文件 `T_rho_profiles.dat`。

为使剖面更干净，请从 `qprofile.dat` 和 `T_rho_profiles.dat` 中删除分界面以外的所有点。

### 1.2. 运行 `neoclassical_program`

该程序及其专用 Makefile 位于 `util/neoclass_program/`。该工具不由 JOREK 顶层 Makefile 构建。

#### 准备输入文件

`neoclassical_program` 的 namelist 输入必须指定：

- 以 $10^{20}\,\mathrm{m}^{-3}$ 为单位的中心密度；
- 以特斯拉为单位的磁场 $B_t$；
- 大半径 $R_0$ 与小半径 $a_\mathrm{min}$；
- 包含安全因子剖面与温度—密度剖面的文件。

例如，对类 ITER 参数：

```fortran
&in1
  central_density  = 1.0                 ! Units: 10^20 m^-3
  Bt               = 5.3d0               ! Magnetic field at the axis
  R0               = 6.19476d0           ! Major radius at the axis
  amin             = 2.d0                ! Minor radius of the equilibrium
  qprofile_file    = 'qprofile_ITER2.dat'
  T_Ne_profile_file = 'Te_ne_profiles_ITER.dat'
/
```

该工具目录中包含示例文件 `qprofile_ITER2.dat` 与 `Te_ne_profiles_ITER.dat`。对新的 JOREK 算例，请把这些文件名替换为相应 `qprofile.dat` 与 `T_rho_profiles.dat` 文件的路径，或将这些文件复制到该工具的工作目录中。两个剖面文件必须具有相同的行数。

#### 编译 `neoclassical_program`

该程序需要 BLAS。其 Makefile 目前默认使用 Intel Fortran 编译器与 Intel MKL，并通过 `MKLROOT` 定位；若系统使用其他编译器或 BLAS 实现，请相应调整 `FC`、`BLAS_HOME` 和 `BLASLIB`。在该工具目录中编译：

```bash
cd util/neoclass_program
make neoclassical_program
```

#### 运行 `neoclassical_program`

```bash
./neoclassical_program < input_neo_ITER
```

该程序生成 `neoclass_coef.dat`，其中以 JOREK 单位给出归一化极向磁通 $\psi_N$、新经典摩擦系数 $\mu_{i,\mathrm{neo}}$ 以及新经典热流系数 $k_i$。

### 1.3. 在 JOREK 中使用系数剖面

在 JOREK 输入文件中添加以下参数：

```fortran
neo      = .t.
neo_file = 'neoclass_coef.dat'
```

## 2. 替代方案：常数新经典系数

也可以不使用剖面，而直接为 $\mu_{i,\mathrm{neo}}$ 与 $k_i$ 取常数值。此时在 JOREK 输入文件中设置典型系数：

```fortran
neo           = .t.
aki_neo_const = -1.
amu_neo_const =  1.e-5
```
