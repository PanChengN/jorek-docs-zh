---
title: "运行仿星器模拟"
nav_order: 1
parent: "仿星器"
grand_parent: "使用指南"
layout: default
render_with_liquid: false
---

# 搭建一个基本的仿星器模拟

本 wiki 页面介绍如何使用 JOREK 运行 W7-A 仿星器模拟，作为仿星器模型的入门。

搭建仿星器模拟的过程涉及若干步骤，但主要思路可概括如下：

  - 在 VMEC 中计算平衡
  - 在 GVEC 中细化平衡
  - 提取 JOREK 所需的数据：
    - 运行 GVEC 到 JOREK 的转换器，以获得 JOREK 所需的平衡数据。
    - （若使用 Dommaschk 势，则计算真空磁场的这种表示）
  - 使用 model 180 在 JOREK 中重建平衡
  - 使用 model 183 进行时间演化模拟

以下各节以 Wendelstein 7-A 仿星器为例，详细描述每个步骤。

## 1. 在 VMEC 中计算仿星器平衡
与托卡马克模型不同，JOREK 没有内置的仿星器平衡求解器。因此，JOREK 使用具有嵌套的理想 MHD 平衡解作为其初始条件。该解由 VMEC 和 GVEC 计算。将来应可以跳过第一步，直接进行第 (2) 步，在 GVEC 中直接生成平衡。
{: .warning }
译者注：原文此处为"an ideal MHD equilibrium solution with nested as its initial condition"，"nested" 后疑漏 "flux surfaces"，即"具有嵌套磁面"。

VMEC2000 与 GVEC 兼容。VMEC2000/STELLOPT VMEC 中所有参数的说明见[此处](https://princetonuniversity.github.io/STELLOPT/VMEC%20Input%20Namelist%20(v8.47))，此外还有更详细的运行代码教程。

为了运行 VMEC，需要在 namelist 文件中指定一些输入参数，该文件随后被传给 VMEC。下面给出一个低比压（轴心处 1 Pa）Wendelstein 7-A 平衡的示例 namelist 文件：

```fortran
&INDATA
lfreeb        = .false.
MGRID_FILE    = 'none'
NFP           = 5,
mpol          = 12,
ntor          = 10,
ntheta        = 60,
nzeta         = 50,
NS_ARRAY      = 12, 47, 133, 201, 501, 1001, 3001 
FTOL_ARRAY    = 1.e-06, 1.e-09, 5.e-10, 1.e-12, 1e-12, 1e-12, 1e-12
DELT          = 0.2,
NITER         = 100000,
NSTEP         = 100,
AM            = 1.0, -0.99
AC            = 3.0 -6.0 3.0 0.0 
NCURR         = 1,
CURTOR        = -17500.0
GAMMA         = 0.0,
PHIEDGE       = 0.08,
raxis      = 1.99,
zaxis      = 0.,
rbc(0,0)=1.99090000E+00,zbs(0,0)=0.00000000E+00,
rbc(1,0)=5.17790000E-04,zbs(1,0)=-5.12860000E-04,
rbc(-2,1)=-1.20200000E-04,zbs(-2,1)=-1.15270000E-04,
rbc(-1,1)=-5.25220000E-04,zbs(-1,1)=-5.75380000E-04,
rbc(0,1)=1.05000000E-01,zbs(0,1)=1.04000000E-01,
rbc(1,1)=-1.3239E-02,    zbs(1,1)=1.388E-02,
rbc(2,1)=1.13000000E-05,zbs(2,1)=2.31320000E-04,
rbc(1,3)=5.61690000E-05,zbs(1,3)=1.04540000E-04,
rbc(2,3)=3.35470000E-04,zbs(2,3)=-3.36410000E-04,
rbc(1,4)=-1.38590000E-04,zbs(1,4)=-1.35450000E-04,
rbc(3,5)=-1.74710000E-04,zbs(3,5)=1.71180000E-04,
/
&end
```

压力，以及环向电流或旋转变换二者之一，必须指定。参数 `NCURR` 指示将提供哪个剖面：若 `NCURR = 1` 则指定环向电流，若 `NCURR = 0` 则指定旋转变换。默认情况下，剖面以多项式给出：
$$f(s) = \sum_n a_n s^n,$$
其中 $f$ 是所讨论的剖面，$s$ 是归一化环向磁通，系数 $a_n$ 由数组 `AM`（压力）、`AC`（环向电流）和 `AI`（iota，此处未使用）给出。总环向电流由 `CURTOR` 给出。

参数 `raxis` 和 `zaxis` 分别指定磁轴 $R$ 坐标的余弦模和磁轴 $z$ 坐标的正弦模（两者均为环向角的函数）。

上面用到但尚未提及的最重要参数可概括如下。参数 `lfreeb` 设为 false，表示将计算固定边界平衡，因此不需要 `MGRID_FILE`。参数 `NFP` 设定周期数，而 `mpol` 和 `ntor` 分别指定一个周期内的极向与环向 Fourier 模数，`ntheta` 和 `nzeta` 分别设定极向与环向分辨率。径向分辨率由数组 `NS_ARRAY` 给出。VMEC 先计算低径向分辨率的平衡，增加更多磁面，通过最小化能量得到更高分辨率的平衡，然后再增加更多磁面，依此类推。`NS_ARRAY` 中元素的个数指定径向分辨率被细化的次数，每个元素给出对应细化步中磁面的总数。此外，每次细化可按不同的容差计算；`FTOL_ARRAY` 的每个元素给出对应细化的容差。最后，对于给定的环向角 $\zeta$ 和极向角 $\theta$，边界的 $(R,z)$ 坐标以一系列模的形式指定：
$$R = \sum_{m,n} a_{mn}\cos(m\theta - n\zeta),\quad z = \sum_{m,n} b_{mn}\sin(m\theta - n\zeta).$$
数组 `rbc(n,m)` 和 `zbs(n,m)` 分别指定系数 $a_{mn}$ 和 $b_{mn}$。

在 namelist 文件中设定好参数后，可按如下方式运行 VMEC：
```bash
./xvmec < input.l2stel_w7a_like
```
其中 `input.l2stel_w7a_like` 是上述 namelist 文件的名称。
## 2. 在 GVEC 中细化平衡

### 一般信息
目前 GVEC 是一个固定边界的 3D 平衡代码，采用与 VMEC 相同的策略寻找平衡。单独运行时，可给定边界形状以及以多项式展开给出的 iota 和压力剖面。以指定环向电流剖面代替 iota 的选项尚不可用。

另一种做法是，它可以使用给定的 VMEC 文件来提取这些信息（iota、压力、总环向磁通以及边界的 Fourier 模）。Wendelstein 7-A 的平衡就是这样做的，因为这些平衡是按给定的环向电流剖面计算的。

VMEC 中求解的未知量是标记为 $s$ 的磁面几何 $R(s,\theta,\zeta),Z(s,\theta,\zeta)$ 以及势 $\lambda(s,\theta,\zeta)$，由此得到 PEST 直线磁力线极向角 $\theta^*=\theta+\lambda$。

在 GVEC 中，未知量为 $(X_1,X_2,\lambda)$。这是因为环向映射 $(R,Z,\phi)->(x,y,z)$ 被推广到了任意的其他解析映射。在环向映射的默认情形下，未知量与 VMEC 中相同，因此 $R=X_1,Z=X_2$ 以及 $\lambda$。

结合环向磁通 $\Phi$ 与极向磁通 $\chi$，磁场定义为
$$ B = \Phi'(s)\nabla s \times \nabla(\theta+\lambda) - \chi'(s)\nabla s \times \nabla \zeta 
     = \Phi'(s)(1+\partial_\theta(\lambda)) \nabla s \times \nabla \theta + (\chi'(s)-\Phi'(s)\partial_\zeta(\lambda)) \nabla \zeta \times \nabla s$$
其中通常以环向磁通作为径向变量（在 VMEC 中为归一化环向磁通，在 GVEC 中为归一化环向磁通的平方根）。于是极向磁通的导数由 iota 剖面给出，$\chi'(s) = \iota(s)\Phi'(s)$。

### 输入参数

此处给出 Wendelstein 7-A 算例的示例参数文件：
```ini
!===================================================!
! initial solution from existing equilibrium
!===================================================!
  whichInitEquilibrium = 1 ! 0: only from input parameters, 1: from VMEC file

  ProjectName = GVEC_W7A_UNSTABLE_1PA_mpol12_ntor10_r41_vmecBC_accGD
    vmecwoutFile=wout_l2stel_w7a_like.nc
    VMECwoutfile_format = 0 !0: netcdf, 1: nemec

  init_fromBConly =F   ! true: only use axis and boundary for X1,X2 (True is default) 
                       ! false: only needed if VMEC data is used, interpolate on full mesh s=0...
  reinit_BC       = -1 ! =-1, keep vmec axis and boundary,
                       ! = 0: keep vmec boundary, overwrite axis (from parameterfile)
                       ! = 1: keep vmec axis, overwrite boundary
                       ! = 2: overwrite axis and boundary 
  init_LA         = F  ! = T: compute lambda from initial mapping (default)
                       ! = F: lambda=0 / from VMEC at initialization 
!===================================================!
! discretization parameters
!===================================================!
  sgrid_nElems=41          ! grid in radial direction (for B-splines)
  sgrid_grid_type=4        ! spacing: 0: uniform, 1: sqrt (finer at edge), 2: s^2 (finer at axis), 
                           ! 3: bump (fine at edge and center), 4: uniform at axis, finer at edge
  degGP  = 7               ! number of gauss points per radial element
  fac_nyq = 4              ! factor to compute the number of fourier interpolation points: 
                           ! (m_nyq,n_nyq) = fac_nyq * (m_max,n_max)
  X1X2_deg  = 5            ! polynomial degree in radial discretization for X1 and X2 variable
  LA_deg    = 4            ! polynomial degree in radial discretization for Lambda variable
  LA_continuity = 3        ! set to LA_deg-1, so that a spline in radial direction is used
  
!!!these parameters can be set, but they are commented out, so they are taken from the vmec file! 
!!!  X1_mn_max = (/ 12, 10/)   ! maximum mumber of fourier modes (mmax,nmax)
!!!  X2_mn_max = (/ 12, 10/)   ! 
!!!  X1_sin_cos = _cos_        ! which fourier modes: can be either _SIN_,_COS_, or _sin_cos_, 
!!!  X2_sin_cos = _sin_        !
!!!  LA_mn_max = (/ 12, 10/)   ! maximum mumber of fourier modes (mmax,nmax)
!!!  LA_sin_cos = _sin_        !
!===================================================!
! Minimization parameters
!===================================================!
  MaxIter =100000             ! maximum number of iterations
  outputIter = 10000          ! number of iterations after which a state & visu is written
  logIter = 1000              ! write log of iterations to screen 
  start_dt=0.5                ! step length of gradient descent (can be reduced by the algorithm)
  minimize_tol=1.0e-12        ! absolute tolerance |Force|<abstol
  PrecondType = 1             ! -1: off(default), 1: on
  MinimizerType = 10          ! 0: gradient descent(default), 10:  new accelerated gradient descent
```
参数 `vmecwoutFile` 给出上一步 VMEC 输出文件的路径，该文件必须由 GVEC 读取。参数 `ProjectName` 给出 GVEC 输出文件名的前缀，在其后追加 `_State_0000_<stepnumber>.dat` 即构成输出文件名。原则上后续只需最后一个状态文件。

梯度下降/加速梯度下降（`MinimizerType=0/10`）在给定约束下最小化总 MHD 能量。梯度下降仍是更稳健（但更慢）的选项。预条件器（`PrecondType=1`）极大地有助于收敛，并允许量级为 1 的步长（`start_dt`）。使用容差 `minimize_tol` 的终止判据取梯度下降中所用梯度向量的范数。但这并不严格对应于强力平衡，因为它依赖于分辨率。由于不清楚什么值算"足够小"，此处将其设为非常小的值，使 GVEC 永远无法达到，而只是一直运行 `MaxIter` 次迭代。

对于离散化，可以指定径向单元数（`sgrid_nElems`），它随后用于特定次数的 B 样条（$X_1,X_2$ 变量用 `X1X2_deg`，$\lambda$ 变量用 `LA_deg`）。如果 Fourier 基的设置被注释掉，则使用来自 VMEC 文件的信息。

### 运行 GVEC
运行该示例，保存参数文件并将其传给 GVEC 可执行文件：

```bash
  gvec_path/build/bin/gvec parameter.ini
```
  
程序将按每个 `outputIter` 生成一个状态文件，最后一个可用于 `convert_gvec_to_jorek` 工具（该工具也属于 GVEC 仓库）。

## 3. 为 JOREK 模拟做准备

### 运行 GVEC 到 JOREK 的转换器

在计算初始条件之前，应将 GVEC 的输出转换为 JOREK 能读取的格式。这通过 `convert_gvec_to_jorek` 工具完成：

```bash
gvec_path/build/bin/convert_gvec_to_jorek -r 41 -p 48 GVEC_W7A_UNSTABLE_1PA_mpol12_ntor10_r41_vmecBC_accGD_State_0000_00100000.dat gvec2jorek.dat
```

该工具构建一个非轴对称的磁面对齐网格，径向分辨率由 `-r` 参数给出，极向分辨率由 `-p` 参数给出，然后在该网格上计算来自 GVEC 平衡的磁场与压力的有限元表示。输出文件必须始终命名为 `gvec2jorek.dat`，因为这是 JOREK 在查找来自 GVEC 的输入时会尝试打开的文件名。

`gvec2jorek.dat` 文件包含在 JOREK 中重建平衡所需的全部信息，唯独缺少线圈真空磁场的表示 $\nabla \chi$。真空场可用以下两种方式之一计算：
  - 在 JOREK 外部，使用 Dommaschk 势计算器。
  - 在 JOREK 内部，使用有限元基和 Poisson 求解。

接下来的各节描述如何计算 Dommaschk 势。若无意使用它们，可跳至第 (4) 步。

### 用 EXTENDER_P 提取线圈场

JOREK 模型中所用的磁场表示要求把由线圈产生的那部分磁场与其余由等离子体电流产生的磁场分开。由于固定边界平衡计算只给出总磁场，因此需要一个中间步骤来提取线圈场。此目的将使用 [EXTENDER_P](https://dx.doi.org/10.1088/0029-5515/45/7/022) 代码。

第一步是把 GVEC 的输出转换为 NetCDF 格式，以便 EXTENDER_P 读取。可使用随 GVEC 代码提供的 `convert_gvec_to_vmec` 工具：
```bash
gvec_path/build/bin/convert_gvec_to_vmec -r 101 GVEC_W7A_UNSTABLE_1PA_mpol12_ntor10_r41_vmecBC_accGD_State_0000_00100000.dat wout_gvec_w7a_unst_1Pa.nc
```
其中 `-r` 参数指定 NetCDF 文件中要包含的磁面数，其后的第一个参数是 GVEC 输出状态文件的名称，最后一个参数是要创建的 NetCDF 文件的期望名称。

EXTENDER_P 将在均匀间隔的 $(R,z,\phi)$ 网格上以 MGRID 格式输出线圈场的 $R$、$z$ 和 $\phi$ 分量。运行该代码之前，应创建一个名为 `suin` 的文本文件，内容如下：
```
nr 101
nz 101
nphi 91
```
该文件指定输出网格的分辨率。之后可按如下方式运行 EXTENDER_P：
```bash
EXTENDER_P -vmec_nyquist wout_gvec_w7a_unst_1Pa.nc -i suin -NU 150 -NV 150 -NI 7 -vacuumfield -write-mgrid -s gvec_w7a_unst_1Pa
```
这里，`-vmec_nyquist` 选项指定上一步得到的 NetCDF 文件名，`-NU` 和 `-NV` 给出要计算镜像电流的边界面的分辨率，`-NI` 是 Newton-Cotes 积分区间数。最后，`-vacuumfield` 指定要计算由线圈产生的磁场（真空场，即若把等离子体替换为真空时存在的场），`-write-mgrid` 表示输出以 MGRID 格式写出，`-s` 给出输出文件的后缀（在此情形下，输出文件将名为 `extended_field.gvec_w7a_unst_1Pa.nc`）。

注意 EXTENDER_P 是纯 MPI 代码，因此给每个 MPI 任务分配多于一个核不会有任何好处。

### 计算 Dommaschk 势系数

EXTENDER_P 运行结束后，可用 JOREK 仓库中附带的 `compute_dcoef_lsq.py` 脚本计算实际的 Dommaschk 势系数。该脚本可按如下方式运行：
```bash
jorek_path/util/compute_dcoef_lsq.py -R 1.99 -m 10 -l 9 -p 5 -o coef_1Pa_R1p99_l9.npy extended_field.gvec_w7a_unst_1Pa.nc
```
该脚本将对来自 EXTENDER_P 的真空磁场与 Dommaschk 基做最小二乘拟合。应指定 Dommaschk 势中 $R_0$ 的值，即真空场磁轴的环向平均 $R$ 坐标。不过，与其寻找真空磁轴，通常更简单的做法是用总场轴的 $n=0$ Fourier 模（`raxis` 中的第一个数）作为初猜，然后从该处开始尽量减小误差。`-m` 参数给出环向模数，并且由于 Dommaschk 势在 JOREK 中的实现方式，它必须与 VMEC 输入 namelist 中的参数 `ntor` 一致。`-l` 参数给出极向模数，应接近 `mpol`，但不必完全一致。`-p` 参数是装置的周期性，必须与 VMEC 中的 `NFP` 参数一致。`-o` 参数指定保存 Dommaschk 势系数的文件名，最后一个参数是上一步 EXTENDER_P 的输出文件。有关该计算的更多细节见[此处](assets/stellarator_setup/dommaschk_computation.pdf)。

为了将 Dommaschk 势给出的磁场与 EXTENDER_P 的输出进行比较，可使用 `compfld.py` 脚本：
```bash
jorek_path/util/compfld.py -R 1.9905208396958163 -F 4.720778214636723 -p 5 -o compare_1Pa_r50_l9.nc coef_1Pa_r50_l9.npy extended_field.gvec_w7a_unst_1Pa.nc
```
注意该脚本依赖 [Zoidberg 项目](https://github.com/boutproject/zoidberg/tree/master/zoidberg)中的 `field.py`、`boundary.py` 和 `progress.py` 模块。在 `field.py` 中，`boundary` 和 `update_progress` 的 import 语句应替换为以下内容：
```python
import boundary
from progress import update_progress
```

`compfld.py` 脚本将计算绝对误差的体积平均平方 $\langle |\vec B_2 - \vec B_1|^2\rangle$，以及相对于 EXTENDER_P 场 $\vec B_1$ 和 Dommaschk 势场 $\vec B_2$ 的误差的体积平均平方 $\langle |\vec B_2 - \vec B_1|^2/|\vec B_{1,2}|^2\rangle$。`-R` 和 `-F` 参数必须分别与 `compute_dcoef_lsq.py` 脚本打印出的 $R_0$ 和 $F_0$ 值一致，而 `-p` 是周期性。最后，使用 `-o` 选项并给出所需的文件名，可以创建一个 NetCDF 文件，其中同时包含 EXTENDER_P 场和 Dommaschk 场，便于在 Paraview 或 Visit 中做可视化比较。最后两个参数是分别包含 Dommaschk 势系数和 EXTENDER_P 输出的文件名，它们都在前面的步骤中创建。

Dommaschk 势系数的最后一步是将其保存为 JOREK 可读取的格式。做法是把系数保存在一个特殊的 namelist 文件中，与标准 JOREK 输入文件分开。系数存放在 Fortran 数组 `dcoef` 中，但其索引顺序与 NumPy 数组不同，而且 Fortran 数组还会跳过未使用的系数（即环向模数不是装置周期性整数倍的那些）。可用以下简单脚本写出该 namelist 文件的内容：
```python
import numpy as np

Nt = 10
Mp = 9
P = 5
coef = np.load("coef_1Pa_r50_l9.npy")
for i in range(Nt+1):
  for l in range(Mp+1):
    for j in range(4):
      if (coef[P*i,l,j] != 0.0):
        print(" dcoef(" + str(j+1) + "," + str(l) + "," + str(i) + ") = " + str(coef[P*i,l,j]))
```
变量 `Nt` 和 `Mp` 应分别设为传给 `compute_dcoef_lsq.py` 脚本 `-m` 和 `-l` 参数的值。`P` 变量就是周期性。该脚本的输出随后应复制到 namelist 文件中。此外，namelist 中应包含 `R_domm` 变量，其值应设为 `compute_dcoef_lsq.py` 打印出的 $R_0$ 值。Dommaschk 势 namelist 文件应为何种样式的示例见此处：[dc_W7A_unst_1Pa](assets/stellarator_setup/dc_W7A_unst_1Pa)。

## 4. 使用 model 180 在 JOREK 中重建平衡

下一步是用 model 180 编译 JOREK，这是一个"假"模型，不对等离子体做时间演化，只计算初始条件。硬编码选项应按如下设置：`n_period` 和 `n_coord_period` 都应与 VMEC namelist 中的 `NFP` 一致，`n_coord_tor` 应为 `2*ntor + 1`，其中 `ntor` 是传给 VMEC 的相应参数的值。

若使用 Dommaschk 系数，`l_pol_domm` 应设为上一步 `compute_dcoef_lsq.py` 中传给 `-l` 参数的那个数。若在不使用 Dommaschk 势的情况下运行代码，必须设置 jorek/defaults.mk 中的 `USE_DOMM=0` 以及 `l_pol_domm=0`。这意味着作为 model 180 的一部分将执行一次 Poisson 求解以计算 $\chi$。注意这虽然可能耗时，但会使后续计算显著加快，因为 Dommaschk 势的计算在计算上很昂贵。

若使用 32 位整数，对于更复杂的设置，由于矩阵求解器中自由度很多，可能会触及矩阵数组索引的整数溢出。如何切换到 64 位整数见此处：[使用长整数编译 JOREK 和求解器](../compiling/compilation_and_libraries/compiling_int64.md)

对于此处考虑的 W7-A 示例（使用 Dommaschk 势），硬编码参数取以下值：

```
model180
n_tor = 5
n_period = 5
n_coord_tor = 21
n_coord_period = 5
l_pol_domm = 9
n_plane = 40
n_vertex_max = 4
n_nodes_max = 15001
n_elements_max = 15001
n_boundary_max = 1001
n_pieces_max = 10001
```

编译之后，JOREK 需要配合输入 namelist 运行。下面给出 1Pa 示例的示例 namelist：
```fortran
&in1
 restart = .f.
 regrid  = .f.
 refinement=.false.
 tstep   = 1.
 nstep   = 1
 nout = 1

 freeboundary = .f.
 gvec_grid_import = .true.
 keep_current_prof = .f.
 fix_axis_nodes = .t.
 bc_natural_open = .t.

 F0    = 4.720778214636723

 rho_0 = 1.0
 rho_1 = 1.0
 rho_coef(1)  =  0.0
 rho_coef(2)  =  0.0
 rho_coef(3)  =  0.0
 rho_coef(4)  =  1.d0
 rho_coef(5)  =  5.d0
 T_0 = 1.d-6

 n_flux   = 41
 n_tht    = 48

 m_pol_bc = 24

 domm_file = "dc_W7A_unst_1Pa"

 iter_precon = 22
 gmres_m = 20
 gmres_4 = 1.d0
 gmres_max_iter = 200
 gmres_tol = 1.d-8
/
```

这里，`nstep` 必须始终为 1，因为没有实际的时间推进，初始条件只需计算一次，而 `tstep` 的值无关紧要，不会影响结果。`gvec_grid_import` 参数告知 JOREK 查找 `gvec2jorek.dat` 文件（该文件必须存在于工作目录中）并从其中导入，而 `bc_natural_open` 允许边界上的电流非零。此外，`F0` 应设为 `compute_dcoef_lsq.py` 打印出的值。若在不使用 Dommaschk 势的情况下运行，`F0` 由 VMEC 生成的 NetCDF 文件中的 `rbtor` 变量给出。

重要：在不使用 Dommaschk 势运行时，还必须提供密度剖面。否则密度和温度将返回 NaN 值。

`n_flux` 和 `n_tht` 必须分别与传给 `convert_gvec_to_jorek` 的 `-r` 和 `-p` 参数的值一致，`domm_file` 给出存放上一步 Dommaschk 势系数的 namelist 的路径。本教程所用的文件见此处：[dc_W7A_unst_1Pa](assets/stellarator_setup/dc_W7A_unst_1Pa)。

随后可按如下方式运行 JOREK：
```bash
mpirun -n 3 ./jorek_model180 < intear
```
其中传给 `-n` 参数的数字必须是 `(n_tor+1)/2` 的整数倍，`intear` 是上面给出的 namelist 文件名。该次运行将产生一个名为 `jorek_restart.h5` 的输出文件（以及其它文件），其中包含约化 MHD 变量的初始条件。下一步将需要该文件。

## 5. 使用 model 183 在 JOREK 中进行时间演化模拟

实际的时间推进在 model 183 中完成。保持与之前相同的硬编码参数，用 model 183 重新编译 JOREK。在此考虑的示例中，将模拟一个撕裂模。模拟的第一部分将以五重周期性进行，以便在小残余力被阻尼掉的过程中让等离子体重新达到平衡。可向 JOREK 提供以下 namelist 文件：
```fortran
&in1
 restart = .t.
 regrid  = .f.
 refinement=.false.
 tstep_n = 1. 10. 100.
 nstep_n = 20 20  5
 nout = 1

 freeboundary = .f.
 keep_current_prof = .t.
 init_current_prof = .t.
 time_evol_scheme = "implicit Euler"
 fix_axis_nodes = .t.
 bc_natural_open = .f.
 eta_T_dependent = .f.
 visco_T_dependent = .f.
 zkpar_T_dependent = .f.

 F0    = 4.720778214636723

 rho_0 = 1.0
 rho_1 = 1.0
 rho_coef(1)  =  0.0
 rho_coef(2)  =  0.0
 rho_coef(3)  =  0.0
 rho_coef(4)  =  1.d0
 rho_coef(5)  =  5.d0
 T_0 = 1.256637061435917E-006

 n_flux   = 41
 n_tht    = 48

 eta   = 1.d-6
 visco = 0.d-9

 eta_num = 0.d-19
 visco_num = 1.d-15

 D_par  = 0.d0
 D_perp = 0.d-7

 ZK_par  = 0.d0
 ZK_perp = 0.d-7

 domm_file = "dc_W7A_unst_1Pa"

 heatsource     = 0.d0
 particlesource = 0.d0

 iter_precon = 22
 gmres_m = 1000
 gmres_4 = 1.d0
 gmres_max_iter = 400
 gmres_tol = 1.d-8
/
```
这里，`restart` 为 true，指定模拟要从上一次 JOREK 运行（初始条件步）产生的 `jorek_restart.h5` 文件初始化。此外，`init_current_prof` 必须设为 true，以便把电流源设为电流的初始条件。最后，时间离散应使用隐式 Euler 方法（`time_evol_scheme`），因为它比 Crank-Nicolson 方法更具耗散性，能相对较快地阻尼掉由残余力引起的振荡。也可以使用 Gears 方法。

JOREK 可按如下方式运行：
```bash
mpirun -n 3 ./jorek_model183 < intear
```
其中，与之前一样，传给 `-n` 参数的数字必须是 `(n_tor+1)/2` 的整数倍，`intear` 是上面给出的 namelist 文件名。同样，该次运行将产生一个名为 `jorek_restart.h5` 的文件，用于初始化下一次 JOREK 运行。

最后一步是把模拟区域扩展到整个环面，以便撕裂模得以发展。这需要把硬编码参数 `n_tor` 设为 21、`n_period` 设为 1，然后重新编译 JOREK。重新编译后，最后一步可使用以下 namelist 文件：
```fortran
&in1
 restart = .t.
 regrid  = .f.
 refinement=.false.
 tstep   = 25.
 nstep   = 160
 nout = 1

 freeboundary = .f.
 keep_current_prof = .t.
 init_current_prof = .f.
 fix_axis_nodes = .t.
 bc_natural_open = .f.
 eta_T_dependent = .f.
 visco_T_dependent = .f.
 zkpar_T_dependent = .f.

 F0    = 4.720778214636723

 rho_0 = 1.0
 rho_1 = 1.0
 rho_coef(1)  =  0.0
 rho_coef(2)  =  0.0
 rho_coef(3)  =  0.0
 rho_coef(4)  =  1.d0
 rho_coef(5)  =  5.d0
 T_0 = 1.256637061435917E-006

 n_flux   = 41
 n_tht    = 48

 eta   = 1.d-6
 visco = 0.d-9

 eta_num = 0.d-19
 visco_num = 1.d-15

 D_par  = 0.d0
 D_perp = 0.d-7

 ZK_par  = 0.d0
 ZK_perp = 0.d-7

 domm_file = "dc_W7A_unst_1Pa"

 heatsource     = 0.d0
 particlesource = 0.d0

 iter_precon = 22
 gmres_m = 1000
 gmres_4 = 1.d0
 gmres_max_iter = 400
 gmres_tol = 1.d-8
/
```
该文件与上一步几乎相同，只是步长（`tstep`）和步数（`nstep`）不同，并且 `init_current_prof` 设为 false（电流源将设为 `jorek_restart.h5` 中存储的电流源值，而不是电流的值），且未指定 `time_evol_scheme`（默认是 Crank-Nicolson 方法）。

随后可按如下方式运行 JOREK：
```bash
mpirun -n 11 ./jorek_model183 < intear
```
其中，与之前一样，`intear` 是上面给出的 namelist 文件名。
