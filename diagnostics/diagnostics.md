---
title: "诊断工具与脚本"
nav_order: 1
render_with_liquid: false
parent: "诊断与后处理"
has_children: true
nav_fold: true
---

本页列出 JOREK 用户可用的一部分诊断工具。这份清单远不完整，欢迎你帮助扩充。

## 诊断工具

JOREK 提供大量诊断工具，其中最重要的几个如下：

| 程序 | 说明 |
| :--- | :--- |
| **[jorek2vtk(_3d)](../howto/introduction_to_jorek_diagnostics.md#jorek2vtk)** | 将 `jorek_restart.h5` 文件转换为 VTK 文件 |
| **[jorek\_read\_h5](jorek_read_h5.html)** | 用于把 HDF5 文件读入 VTK 对象与 VTK 文件的 Python 脚本 |
| **[jorek2vtk\_gaussvortterms](../howto/introduction_to_jorek_diagnostics.md#beyond)** | 在高斯点处积分计算涡量方程的各项，并生成一个 VTK 文件，以便在极向平面上可视化各项。 |
| **[jorek2\_four](jorek2_four.html)** | 对 `jorek_restart.rst` 文件做二维傅里叶分析 |
| **[jorek2\_poincare](../howto/introduction_to_jorek_diagnostics.md#jorek2_poincare)** | 为 JOREK 重启文件绘制庞加莱图 |
| **[jorek2\_postproc](../howto/introduction_to_jorek_diagnostics.md#jorek2_postproc)** | 诊断程序 jorek2_postproc 是一个极为灵活的诊断工具，既可交互使用，也可通过小型脚本调用 |
| **[jorek2\_diagno](../howto/introduction_to_jorek_diagnostics.md#beyond)** | 从 JOREK 重启文件中提取一些有用的数据 |
| **jorek2\_diagno\_spi** | 从 JOREK 重启文件中提取一些有用的数据，包括该重启文件对应时刻 SPI 碎片的位形与半径 |
| **[jorek2\_connection2](../howto/introduction_to_jorek_diagnostics.md#beyond)** | 该诊断给出磁场几何的庞加莱图 |
| **[jorek2\_connection\_flux\_aligned](jorek2_connection_flux_aligned.html)** | 计算到模拟边界的连接长度，以及 n=0 磁面上磁力线对应的打击点 |
| **[jorek2\_fields\_xyz](jorek2_fields_xyz.html)** | 计算给定 (x,y,z) 笛卡尔坐标处的 B_x、B_y、B_z |
| **[jorek2\_wall\_forces](jorek2_wall_forces.html)** | 计算总的壁力（F_x、F_y、F_z）。需要 [JOREK-STARWALL](../howto/running_jorek-starwall_for_the_first_time.md) |
| **[jorek2\_fast\_camera](jorek2_fast_camera.html)** | 该诊断生成可见等离子体（Dalpha）的相机图像 |
| **[rst\_bin2hdf5](rst_bin2hdf5.html)** 与 **[rst\_hdf52bin](rst_bin2hdf5.html#rst_hdf52bin)** | 在 `jorek_restart.rst` 与 `jorek_restart.h5` 之间双向转换。 |
| **[plot\_live\_data.sh](plot_live_data.sh.html)** | 在模拟运行过程中绘制若干 0D 量（gnuplot） |
| **[诊断框架 new\_diag](../howto/introduction_to_jorek_diagnostics.md#new_diag)** | 允许在计算域内的**任意位置计算任意物理表达式（[当前可用的表达式清单](../howto/introduction_to_jorek_diagnostics.md#expressions-available)）**，所用单位既可为 **JOREK 单位，也可为 SI 单位**。该框架支撑了 [jorek2\_postproc](../howto/introduction_to_jorek_diagnostics.md#jorek2_postproc) 诊断的大部分功能，而基于该框架还可以很容易地编写更强大的诊断。 |
| **[radiation\_function\_diagno](../physics/model_extensions/adas.md#checking-the-radiation-power-function-and-its-components)** | 输出硬编码杂质在硬编码参数下的辐射功率函数 |
| **[jorek2\_fieldlines\_vtk\_newdiag](jorek2_fieldlines_vtk_newdiag.html)** | 该诊断沿磁力线计算任意物理表达式（使用 new_diag 框架），并把结果同时写入 vtk 与 txt 文件 |
| **[jorek2\_solcurrent](jorek2_solcurrent.html)** | 该诊断对 `jorek_restart.h5` 做后处理，通过求解 [Stangeby](https://doi.org/10.1201/9780367801489) 式 17.29 来确定刮削层（SOL）电流（靶板之间的热电电流） |
| **[fluid_loads_on_3D_wall](fluid_wall_load.html)** | 计算以三角形离散的三维薄壁上的流体通量（热负荷与电流负荷），方法见 [ArtolaNF2026](https://iopscience.iop.org/article/10.1088/1741-4326/ae80e3)  |
| **[自由边界诊断](../physics/model_extensions/freebound/freebnd_tools.md)** | 这里可以找到与自由边界扩展相关的诊断，例如网格外部 B 场的计算以及壁力的计算 |

诊断工具的编译所用硬编码参数应与 JOREK 一致。

要在 **Marconi 上运行诊断**，可能需要用类似下面的命令申请一个调试节点：

```
salloc --nodes=1 --time=01:00:00 --exclusive --account=FUA36_MHD --partition=skl_fua_dbg
```

要在 **Leonardo DCGP 上运行诊断**，可能需要用类似下面的命令申请一个调试节点：

```
salloc --nodes=1 --time=10:00 --account=FUA38_MHD_0 --partition=dcgp_fua_dbg
```

然后运行：

```
srun jorek2_diagno < jorek_in
```

另一种做法是先在登录节点上把 ulimit 内存限制设为不限定，然后直接运行：

```
ulimit -s unlimited
```

## 脚本

**trunk/util/** 目录下提供了若干脚本：

| 脚本 | 说明 |
| :--- | :--- |
| **[config.sh](hard-coded_parameters.html)** | 列出或修改**硬编码参数** |
| **[plot\_live\_data.sh](plot_live_data.sh.html)** | 在模拟运行期间或运行之后**绘制能量或增长率的时间演化曲线**（以及更多量） |
| **[plot\_grids.sh](plot_grids.sh.html)** | **把网格绘制到文件或屏幕** |
| **[plot\_live\_data.py](plot_live_data.py.html)** | **plot_live_data.sh 的 Python 版本** |
| **[read\_jorek\_logfile.py](read_jorek_logfile.py.html)** | **在 JOREK 日志文件中查找指定变量** |
| **[plot\_mlog.py](plot_mlog.py.html)** | **绘制内存占用** |

## 输出文件

运行过程中会生成一些输出文件，下面简要汇总各类文件。

- [macroscopic\_vars](macroscopic_vars.html) 包含模拟中的能量与增长率清单（以及各种其他量）
- `jorek00XXX.rst` 是快照文件，可用于重启模拟
- `boundary.txt`
- `equilibrium.txt`
- `grid_fluxsurface.dat`
- `grid_initial.dat`
- `jorek2.ps` 在模拟结束时生成，包含能量与磁场的一些图。
- `qprofile.dat`
- `special_equilibrium_points.dat`
- `T_rho_profiles.dat`
