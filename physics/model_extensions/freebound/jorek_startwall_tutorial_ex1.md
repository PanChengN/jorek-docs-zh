---
title: "JOREK-STARWALL 教程：电阻壁撕裂模"
nav_order: 2
parent: "自由边界扩展（STARWALL、CARIDDI）"
grand_parent: "模型扩展"
layout: default
render_with_liquid: false
---

# 首次运行 JOREK-STARWALL

本教程演示如何运行一个与 STARWALL 耦合的小型 JOREK 仿真。它使用 `model600/intear_freebnd` 撕裂模算例，并用一个简单电阻壁的响应取代理想导体边界条件。

开始之前，应已能按[首次运行 JOREK](../../../howto/running_jorek_for_the_first_time.md)所述编译并运行 JOREK。还需要一个已编译的 STARWALL 可执行文件；请按[获取 STARWALL 源代码并编译](running_STARWALL.html#getting-the-source-code)操作，而不要使用从本教程复制来的机器专用配置。

耦合的准备分三个阶段：

1. 以 `freeboundary=.t.` 运行一次 JOREK，写出 `boundary.txt`。
2. 用该边界运行 STARWALL，生成 `starwall-response.dat`。
3. 在算例目录中放有 `starwall-response.dat` 的情况下，运行 JOREK 的时间演化。

只有在生成响应文件时才需要 STARWALL，JOREK 推进时间演化时不需要。

## 1. 准备 JOREK 算例

为 JOREK 源码树和算例目录选择路径。下例将算例放在源码树之外：

```bash
JOREK_DIR=/absolute/path/to/JOREK
RUN_DIR=/absolute/path/to/intear2_reswall

mkdir -p "$RUN_DIR"
cp "$JOREK_DIR/namelist/model600/intear_freebnd" "$RUN_DIR/intear"

cd "$JOREK_DIR"
# choose minimalistic model options for faster runs (no impurities, no vpar, only one T, constant density)
./util/config.sh model=600 n_tor=3 n_period=1 n_plane=4 with_impurities=.false. with_vpar=.false. with_TiTe=.false. with_rho=.false.

make clean
make -j 8
make -j 8 jorek2vtk jorek2_postproc

cp jorek_model600 jorek2vtk jorek2_postproc "$RUN_DIR/"
ln -sfn "$JOREK_DIR/util" "$RUN_DIR/util"
```

按此配置，JOREK 包含轴对称分量以及 $n=1$ 谐波的余弦与正弦分量。下面的 STARWALL 输入只对 $n=1$ 提供自由边界响应；因此 $n=0$ 分量仍为固定边界。

所有使用同一组重启文件的 JOREK 可执行文件，都必须以一致的硬编码参数编译。

## 2. 复制 STARWALL 可执行文件

按 [STARWALL 编译说明](running_STARWALL.html#compiling)操作后，将其可执行文件复制到算例目录：

```bash
STARWALL_DIR=/absolute/path/to/STARWALL
cp "$STARWALL_DIR/o_3d/STARWALL_JOREK_Linux" "$RUN_DIR/"
```

若你的 STARWALL 配置把可执行文件放在机器专用的子目录中，请相应调整源路径。

## 3. 用 JOREK 生成 `boundary.txt`

在输入文件（intear）中设置 `freeboundary = .t.`，然后运行一次 JOREK：

```bash
export OMP_NUM_THREADS=8
mpirun -n 2 ./jorek_model600 < intear | tee logfile_boundary
```

这次调用预期会中止，因为此时还不存在 `starwall-response.dat`。在停止之前，JOREK 应把等离子体耦合面写入 `boundary.txt`。确认该文件存在且非空：

必须用 `freeboundary=.t.` 生成该文件。由固定边界计算导出的边界可能含有不同数量的边界单元，因此不得复用于本步骤。响应文件的通用流程概述于[获取响应文件](jorek_freebnd_params.html#getting-the-response-file)。

 **注意：** JOREK 提供若干输入参数用于配置自由边界扩展，其中包括自由边界平衡（$n=0$ 模式）的计算。详见[自由边界输入参数](jorek_freebnd_params.html)。

## 4. 创建 STARWALL 输入

在算例目录中创建名为 `input_starwall` 的文件：

```fortran
&PARAMS
  ! Calculate the response for a resistive wall.
  ! 0 = no wall, 1 = ideal wall, 2 = resistive wall
  i_response = 2,

  ! Include only the n=1 toroidal harmonic.
  n_harm = 1,
  n_tor  = 1,

  ! Toroidal grid points in the real-space representation.
  nv = 40,

  ! Numerical parameters normally left unchanged.
  delta    = 0.001,
  n_points = 10,
  nwall    = 1,

  ! Represent the wall with a Fourier series.
  iwall = 1,
/

&PARAMS_WALL
  ! Thin-wall resistivity in ohms.
  eta_thin_w = 1.d-4,

  ! Poloidal and toroidal wall-grid points.
  nwu = 32,
  nwv = 32,

  ! R = 10 + 1.10 cos(theta), Z = 1.10 sin(theta).
  mn_w = 2,
  n_w  =  0,    0,
  m_w  =  0,    1,
  rc_w = 10., 1.10,
  rs_w =  0., 0.00,
  zc_w =  0., 0.00,
  zs_w =  0., 1.10,
/
```

该输入描述一个圆心位于 $R=10$、$Z=0$、小半径为 $1.10$ 的圆形壁。有关参数含义、壁电阻率单位、其他壁表示方式以及线圈输入，请查阅维护中的 [STARWALL 参数配置](running_STARWALL.html#parameter-setup)。

`n_harm` 与 `n_tor` 这两个名称容易混淆：在 STARWALL 中，`n_harm` 是响应中包含的环向谐波个数，而 `n_tor` 列出这些谐波的模数。它们与 JOREK 编译期的 `n_tor` 不是一回事。示例见[选择模与谐波](running_STARWALL.html#select-modes-and-harmonics)。

## 5. 生成 `starwall-response.dat`

在同时包含 `boundary.txt` 与 `input_starwall` 的目录中运行 STARWALL：

```bash
cd "$RUN_DIR"
export OMP_NUM_THREADS=1
mpirun -n 16 ./STARWALL_JOREK_Linux ./input_starwall | tee logfile_starwall
```

STARWALL 仅支持 MPI，因此每个 MPI 任务使用一个 OpenMP 线程。对这个小型算例，计算应只需几分钟。在批处理系统上，请按[提交 STARWALL 作业](running_STARWALL.html#submitting-the-job)所述调整资源申请；不要原样复制旧的机器专用作业脚本。

STARWALL 还会写出 `wall.vtk`，其中包含壁的三角形离散，可用 ParaView 或 VisIt 查看。

## 6. 运行耦合的 JOREK 时间演化

此时算例目录中已包含所需的响应文件，且 `intear` 中已设置 `freeboundary=.t.`。按与独立计算相同的方式启动 JOREK：

```bash
cd "$RUN_DIR"
export OMP_NUM_THREADS=8
mpirun -n 2 ./jorek_model600 < intear | tee logfile_jorek
```

正式计算时，请使用适合你的 HPC 系统的批处理提交流程。

## 7. 检查并分析运行结果

在 `logfile_jorek` 开头附近，`STARWALL RESPONSE INFORMATION` 块应给出响应维度、壁电阻率以及所包含的谐波。对本例，谐波列表应包含 $n=1$ 的余弦与正弦分量：

```text
i_tor = 2 (n=1 cos), 3 (n=1 sin)
```

JOREK 按 `nout` 控制的间隔写出 `wallcurr.XXXXXX.vtk`。这些文件包含壁电流流函数，可用 ParaView 或 VisIt 打开。通用诊断与绘图说明见 [JOREK 诊断简介](../../../howto/introduction_to_jorek_diagnostics.md)。

为研究壁的物理效应：

1. 运行其他条件完全相同的固定边界与自由边界算例，比较它们的线性增长率与模结构。
2. 改变 JOREK 输入参数 `wall_resistivity_fact` 以缩放壁电阻率，而无需重新生成 STARWALL 响应。可用它考察从理想壁到高电阻壁的各种极限。见[自由边界输入参数](jorek_freebnd_params.html#main-parameters)。
3. 用 $n=1$ 与 $n=2$ 重复计算。重新配置 JOREK，使两个谐波以及足够的环向平面都存在，然后在 `input_starwall` 中设置 `n_harm=2` 与 `n_tor=1,2`。JOREK 与 STARWALL 的谐波集合必须一致。

## 可选：添加诊断线圈

诊断线圈在生成 STARWALL 响应时定义。在 `input_starwall` 的 `&PARAMS` 块中加入以下条目：

```fortran
diag_coil_file = 'diag_coils.nml',
```

然后在算例目录中创建 `diag_coils.nml`：

```fortran
&coil_set_nml
  description = 'example coil set'
  ncoil       = 1
/

&coils_nml
  coil(1)%name      = 'diag01'
  coil(1)%coil_type = 'general_thin'
  coil(1)%resist    = 1.d0
  coil(1)%n_pts     = 5
  coil(1)%width     = 0.01
  coil(1)%xpts      = 11.,  11., 11.,  11., 11.
  coil(1)%ypts      = -0.5, 0.5, 0.5, -0.5, -0.5
  coil(1)%zpts      = -0.5,-0.5, 0.5,  0.5, -0.5
  coil(1)%nturns    = 1
/
```

再次运行 STARWALL 以重新生成 `starwall-response.dat`，然后重跑 JOREK。用下式绘制诊断线圈信号：

```bash
./util/plot_live_data.sh -q diag_coil_curr
```

支持的线圈类型与全部线圈字段记录于[包含线圈](running_STARWALL.html#include-coils)。

## 后续步骤

更进阶的分析见[自由边界诊断与工具](freebnd_tools.html)，包括壁力与真空场计算。JOREK-STARWALL 工作应引用的论文列于[自由边界参考文献](references.html)。
