---
title: "运行"
nav_order: 3
parent: "编译与运行"
layout: default
render_with_liquid: false
---

# 运行 JOREK

## 运行代码

- 将 namelist 输入文件作为可执行文件的标准输入：

```bash
./jorek_model303 < ./input
```

- 使用 OpenMP 时（例如 16 个线程），在运行代码前设置：

```bash
export OMP_NUM_THREADS=16
```

- 使用 MPI 并行运行时（例如 4 个进程）：
  - MPI 进程数必须是 `(n_tor+1)/2` 的整数倍[参见硬编码参数](compilation_and_libraries/hard-coded_parameters.md)

```bash
mpirun -n 4 ./jorek_model303 < input
```

## Namelist 输入文件

- JOREK 仿真由输入参数控制，这些参数在如下形式的 namelist 输入文件中设置：

```fortran
&in1
  restart=.false.
  nstep_n=0
  tstep_n=1.e3
  ...
/
```

- **部分输入参数与具体模型相关。** 详见 `models/modelXXX/initialise_parameters.f90`。
- **输入参数的默认值**由 `models/preset_parameters.f90` 赋予。
- 输入参数由 MPI 线程 0 读取，并通过 `trunk/communication/broadcast_phys.f90` 发送给所有其他 MPI 线程。
- **示例输入文件**可在仓库的 `trunk/namelist/modelXXX/` 目录中找到。
- 仿真开始时，所有输入参数会自动写出。这样可核对所用参数是否正确，在使用默认值时尤其有用。

### 通用参数

| 输入参数 | 说明 | 备注 |
|----------|--------|--------|
| `restart` | 重启被中断的仿真 | 允许从 `jorek_restart.rst` 文件重启 JOREK 仿真。默认：`.false.` |
| `rst_format` | 重启文件采用的格式编号。有效选项：0、1、>1 | 参见 `export_restart.f90` |
| `regrid` | 在磁面上重新对齐网格 | 从未使用 |
| `nout` | 每 `nout` 步输出一个重启文件 | |

### 物理参数

| 输入参数 | 说明 | 备注 |
|----------|--------|--------|
| `tauIC` | 归一化回旋频率的倒数（扩展 MHD） | |
| `eta` | 电阻率 | |
| `visco(_par)` | 垂直（平行）速度的黏性 | |
| `D_par` | 平行粒子扩散 | = zero |
| `D_perp(i)` | 垂直粒子扩散 $D_{base} = D_1 \left(( 1 - D_2) + \frac{D_2}{2} \left(1 - \tanh \left(\frac{\psi - D_5}{D_4} \right) \right)\right)$ 若 model < 300 则 $D = D_{base}$，否则 $D = D_{base} + \frac{D_6 D_2}{2} \left(1 - \tanh \left( \frac{D_5 + D_3 -\psi}{D_4}  \right) \right)$ | 依次为（1-6）：芯部取值、台基区取值 (1-D(2))、台基区宽度、过渡层宽度、台基起始位置、台基外侧的扩散系数 |
| `ZK_par` | 平行热扩散 | |
| `ZK_perp(i)` | 垂直热扩散 | 参见粒子扩散 |
| `F0` | R*B_phi | |
| `FF_0` | 等离子体芯部的 FF' | |
| `FF_1` | 等离子体边界的 FF' | |
| `FF_coef(i)` | `FF'(psi) = [(FF_0 - FF_1)*(1 + coef(1) * psi + coef(2)*psi**2 + coef(3)*psi**3) + coef(6)/cosh((psi - coef(7))/coef(8))**2 / (2.d0 * coef(8)) / (psi_1-psi_0) ]*0.5*(1- tanh((psi-coef(5))/coef(4)))  +  FF_1` | |
| `heatsource` | 能量源幅度 | 加热，采用归一化单位 |
| `particlesource` | 粒子源幅度 | |
| `T_0, T_1` | 初始温度剖面，分别取轴心（0）处与边界处 | |
| `T_coef(i)` | `T(psi) = (T_0 - T_1)*(1 + coef(1) * psi + coef(2)*psi**2 + coef(3)*psi**3)  *0.5*(1- tanh((psi-coef(5))/coef(4)))  +  T_1` | |
| `rho_(0,1,coef(i))` | 初始密度剖面（参见温度） | |
| `V_(0,1,coef(i))` | 初始环向速度剖面（若 `normalized_velocity_profile = .t.` 则为旋转频率）（参见温度） | |
| `central_density` | 中心数密度 | 用于其他量的归一化 |
| `central_mass` | 中心平均离子质量 | 未指定时取氘质量 |

### 数值参数

| 输入参数 | 说明 | 备注 |
|----------|--------|--------|
| `tstep_n` | 时间步长 $\Delta t$ 的大小 | 最多可给七个值（与多个 `nstep_n` 值对应） |
| `nstep_n` | 时间步数 | 最多可给七个值（与多个 `tstep_n` 值对应） |
| `tstep` | 不使用 `nstep_n` 时的时间步长 | |
| `nstep` | 要执行的 `tstep` 步数 | |
| `eta_num` | 数值超电阻率 | 建议取较小值，满足 `eta_num \lesssim eta^2`，并对 `eta_num` 做扫描以确保其结果不受影响。 |
| `visco(_par)_num` | 数值超黏性 | 建议取较小值，满足 `visco_num \lesssim visco^2`，并对 `visco_num` 做扫描以确保其结果不受影响。 |
| `D_perp_num` | 超扩散（粒子，数值稳定化） | |
| `ZK_perp_num` | 超扩散（热，数值稳定化） | |
| `tgnum(i)` | 方程 i 中 Taylor-Galerkin 稳定化的系数 | 参见有关使用稳定化的说明。 |
| `iter_precon` | 若 gmres 迭代次数 > `iter_precon`，则重做分解 | GMRES 参数 |
| `gmres_m` | gmres 维度 | |
| `gmres_4` | 误差的缩放 | 参见源代码 |
| `gmres_max_iter` | gmres 迭代的最大次数 | |
| `gmres_tol` | 误差 < `gmres_tol` 时视为收敛 | |

### 几何参数

| 输入参数 | 说明 | 备注 |
|----------|--------|--------|
| `mf` | `fbnd` 中的谐波数 | 若 `mf=0` 则改用椭率等参数 |
| `fbnd(i)` | 等离子体边界半径（Fourier 级数）随极向角的变化 | 共 `mf` 项 |
| `ellip` | 初始极向网格的椭率 | |
| `tria_u/l` | 上／下三角形变 | |
| `quad_u/l` | 上／下四边形变 | |
| `xampl` | 边界上 `psi(theta)` 的解析定义 | 幅度 |
| `xsig` | | |
| `xwidth` | 扰动 `psi(theta)` 在 `theta` 方向的宽度 | |
| `xtheta` | X 点所在的角度位置 | |
| `xleft` | 平移等离子体的径向位置 | |
| `xshift` | 平移等离子体的垂直位置 | |
| `xpoint` | 等离子体带 X 点 | |
| `R_begin` | 方形 Bezier 网格的最小 R | |
| `R_end` | 方形 Bezier 网格的最大 R | |
| `Z_begin` | 方形 Bezier 网格的最小 Z | |
| `Z_end` | 方形 Bezier 网格的最大 Z | |
| `R_geo` | 极向网格中心的 R 坐标 | |
| `Z_geo` | 极向网格中心的 Z 坐标 | |
| `amin` | 极向网格的小半径 | |
| `n_R` | 方形 Bezier 网格中水平方向的节点数 | 该方向由此得到 `n_R-1` 个单元 |
| `n_Z` | 方形 Bezier 网格中垂直方向的节点数 | 由此得到 `n_Z-1` 个单元 |
| `n_radial` | 极向 Bezier 网格（网格 1）中的径向节点数 | |
| `n_pol` | 极向 Bezier 网格（网格 1）中的极向节点数 | |
| `n_flux` | 等离子体边界内侧磁面对齐网格（网格 2）上的径向节点数 | |
| `n_tht` | 极向节点数（网格 2） | |
| `n_open` | 从磁轴到分界面的径向节点数（网格 2） | |
| `n_leg` | 沿分界面支腿、从 X 点到偏滤器壁的节点数（网格 2） | |
| `n_private` | 私有区（分界面支腿下方区域）的径向节点数（网格 2） | |
