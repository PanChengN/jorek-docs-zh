---
title: "运行与配置 STARWALL"
nav_order: 4
parent: "自由边界扩展（STARWALL、CARIDDI）"
grand_parent: "模型扩展"
layout: default
render_with_liquid: false
---

本页旨在说明如何编译、配置并运行 STARWALL 代码，以用于 JOREK 的自由边界仿真。

## 获取源代码 {#getting-the-source-code}
克隆代码，目前位于 ITER 的 bitbucket 服务器

```bash
git clone --branch develop ssh://git@git.iter.org/stab/starwall.git starwall/
```

## 编译 {#compiling}
编译需要一个带 MPI 的 FORTRAN 编译器，还需要包含 SCaLAPACK 的 [**MKL**](https://en.wikipedia.org/wiki/Math_Kernel_Library) 依赖库。首先需要为自己的机器准备一个配置文件，并在主目录中将其命名为 `config.in`。例如对 ITER，进入 STARWALL 文件夹并执行

```bash
cp configs/config.iter config.in
```
并确保 MKL 模块已正确链接

```bash
MKL_HOME=$(MKLROOT)
LAPACK_LIB = $(MKL_HOME)/lib/intel64/libmkl_sequential.a -Wl,--start-group  $(MKL_HOME)/lib/intel64/libmkl_intel_lp64.a $(MKL_HOME)/lib/intel64/libmkl_sequential.a $(MKL_HOME)/lib/intel64/libmkl_core.a $(MKL_HOME)/lib/intel64/libmkl_scalapack_lp64.a   $(MKL_HOME)/lib/intel64/libmkl_blacs_intelmpi_lp64.a    -Wl,--end-group -lpthread

LIB = $(LAPACK_LIB)
```
编译只需执行

```bash
make clean 
make
```
要运行的可执行文件是
```bash
./starwall/o_3d/STARWALL_JOREK_Linux
```

## 运行

在任意方便的位置为 STARWALL 创建一个运行文件夹（例如 `run_starwall`）

### 获取 boundary.txt 文件
1. 在输入文件中设置 `freeboundary=.t.` 运行 JOREK。JOREK 会停止，并在文件夹中出现含耦合面几何的 **boundary.txt** 文件。
2. 把 **boundary.txt** 复制到 `run_starwall` 文件夹。

### 创建 STARWALL 输入文件
文件名可任意选择（例如 `input_starwall`）。以 ITER 的下例为参照，**输入参数**在[此处](#parameter-overview)说明
```bash
&PARAMS
  ! Calculate response matrix for:
  !   0=no wall, 1=ideal wall, 2=resistive wall
  i_response = 2,
  
  ! Number of toroidal modes
  n_harm     = 1,

  ! Toroidal mode numbers n_tor(i) for i=1...n_harm
  n_tor      = 0
  
  ! Number of toroidal grid points for real space representation
  nv         = 32,
  
  ! B_par is computed on a surface shifted by delta into the vacuum domain
  ! (numerical parameter: leave unchanged)
  delta      = 0.001,
  
  ! Number of grid points per boundary element
  n_points   = 10,
  
  ! Number of unconnected wall components
  ! (CURRENTLY UNUSED)
  nwall      = 1,
  
  ! Representation of the wall:
  !   1=Fourier series, 2=triangles, 3=triangles+index fu.
  iwall      = 1,

  ! PF coils file
  pol_coil_file  = 'polcoils_iter.nml'
    
  ! Passive components file
  diag_coil_file = 'passive_components.nml'
  
/

&PARAMS_WALL
  ! eta_thin,wall in SI units [Ohm]
  eta_thin_w = 1.33e-05
  
  ! Wall grid points in poloidal direction
  nwu        = 60,
  
  ! Wall grid points in toroidal direction
  nwv        = 60,
  
  ! Number of Fourier harmonics
  mn_w       = 8,
  
  ! Modes characterizing the wall shape (data taken from ../wall/descur/input/out_vmec_test)
  n_w  =          0,         0,         0,         0,         0,         0,         0,         0,
  m_w  =          0,         1,         2,         3,         4,         5,         6,         7,
  rc_w =  5.7387E+0, 2.8230E+0, 4.3479E-1,-1.0796E-1, 8.9448E-2, 1.2628E-2, 1.2445E-3, 2.9309E-2,
  rs_w =  0.0000E+0, 3.6590E-2, 5.1754E-2, 6.4473E-2, 5.7993E-2, 1.8204E-2,-1.4235E-2,-1.4031E-2,
  zc_w =  7.9184E-2, 3.6590E-2, 7.4851E-2, 3.4342E-2, 1.2247E-2,-1.2918E-2,-2.1155E-2,-7.0774E-3,
  zs_w =  0.0000E+0, 5.1906E+0,-2.2917E-1, 7.2744E-3,-2.3149E-2,-3.0743E-3, 1.6155E-4,-7.0349E-3,
/
```

### 提交作业 {#submitting-the-job}
**STARWALL 是仅 MPI 的代码**，不使用 OpenMP。因此在作业文件中，运行前必须设置以下参数
```bash
  #SBATCH --ntasks-per-node= Number of cpus per node of your machine
  #SBATCH --cpus-per-task  =1
  
  export OMP_NUM_THREADS=1
```
随后运行 STARWALL 的命令很简单

```bash
  mpirun STARWALL_JOREK_Linux input_starwall > output_starwall
```
视问题规模与所用 CPU 数量，耗时从几分钟到数小时不等。对 ITER 的高要求仿真，用 4–8 个计算节点约需 8 小时。

运行一开始，STARWALL 就会生成“wall.vtk”，可用 visit 或 paraview 绘制，以可视化你在输入文件中指定的壁几何。STARWALL 的输出信息可在 output_starwall 中查看。

最后，运行文件夹中应出现响应文件

```bash
  ./starwall-response.dat
```
你需要把它复制或链接到 JOREK 目录。

## 参数配置 {#parameter-setup}
### 参数总览 {#parameter-overview}
| 输入参数 | 说明 |
|---|---|
| `n_harm` | 环向谐波个数，见[选择模与谐波](#select-modes-and-harmonics) |
| `n_tor` | 要包含的环向模数，见[选择模与谐波](#select-modes-and-harmonics) |
| `nv` | 在 STARWALL 中表示等离子体的环向网格点数 |

以下参数通常无需改动：

| 输入参数 | 说明 |
|---|---|
| `i_response` | 2 —— 不要改动 |
| `delta` | 0.001 —— 不要改动 |
| `n_points` | 10 —— 不要改动 |
| `nwall` | 1 —— 简单壁不要改动 |

此外，对由傅里叶谐波表示的**简单闭合壁**（详见[配置简单壁](#setting-up-a-simple-wall)）：

| 输入参数 | 说明 |
|---|---|
| `eta_thin_w` | 薄壁电阻率，见[壁与线圈电阻率](#wall-and-coil-resistivities) |
| `nwu` | 表示简单壁的极向点数 |
| `nwv` | 表示简单壁的环向点数 |
| `mn_w` | 描述简单壁几何的谐波个数 |
| `n_w(*)` | 描述简单壁几何的各谐波的环向模数 |
| `m_w(*)` | 描述简单壁几何的各谐波的极向模数 |
| `rc_w(*)` | 描述简单壁几何的 R 的余弦谐波 |
| `rs_w(*)` | 描述简单壁几何的 R 的正弦谐波 |
| `zc_w(*)` | 描述简单壁几何的 Z 的余弦谐波 |
| `zs_w(*)` | 描述简单壁几何的 Z 的正弦谐波 |

此外，在包含**线圈**时（详见[包含线圈](#include-coils)）：

| 输入参数 | 说明 |
|---|---|
| `pol_coil_file` | 文件名，用于自由边界平衡、垂直反馈等的轴对称线圈 |
| `rmp_coil_file` | 文件名，非轴对称主动线圈 |
| `diag_coil_file` | 文件名，用作虚拟诊断的任意几何线圈 |
| `voltage_coil_file` | 文件名（尚未可用） |



### 配置简单壁 {#setting-up-a-simple-wall}
下例配置一个几何为 $R=10+1.2\cos(\theta)$、$Z=1.2\sin(\theta)$ 的壁，它由 32 个极向点和 32 个环向点表示（即 2×32×32=2048 个三角形）：

```fortran
&PARAMS_WALL
  nwu        = 32,
  nwv        = 32,
  mn_w       = 2,
  eta_thin_w = 1.e-6,
  n_w(1)=0, m_w(1)=0, rc_w(1)=10.0, rs_w(1)=0., zc_w(1)=0., zs_w(1)=0.0,
  n_w(2)=0, m_w(2)=1, rc_w(2)= 1.2, rs_w(2)=0., zc_w(2)=0., zs_w(2)=1.2,
/
```

关于参数 `eta_thin_w`，参见[如何设置壁与线圈电阻率？](#how-to-set-up-wall-and-coil-resistivities)。

### 选择模与谐波 {#select-modes-and-harmonics}
`n_harm` 表示谐波个数，`n_tor` 列出相应的环向模数。几个例子：

| 环向模数 | `n_harm` | `n_tor` |
|---|---|---|
| 0 | 1 | 0 |
| 0,1,2 | 3 | 0,1,2 |
| 4,8 | 2 | 4,8 |

在 JOREK 日志文件中搜索下面这段，它报告响应中计入的谐波：

```
-----------------------------------------------------------------------------
STARWALL RESPONSE INFORMATION:
-----------------------------------------------------------------------------
...
i_tor                   = 2 (n=1 cos), 3 (n=1 sin)
-----------------------------------------------------------------------------
```

**注意：**
* 存在于 JOREK 但不在 STARWALL 响应中的模，将按理想壁边界条件处理。
* 存在于 STARWALL 但未包含在 JOREK 中的模，其真空响应将被忽略。

### 如何设置壁与线圈电阻率？ {#how-to-set-up-wall-and-coil-resistivities}
壁与线圈电阻率**在 STARWALL 中**设置，方法如下。JOREK 参数 `wall_resistivity_fact` 可同时缩放壁与线圈的电阻率。

#### 壁

壁电阻率由 STARWALL 中的参数 `eta_thin_w` 设置。由材料属性 $\eta_{wall,SI}$ [Ω·m] 与壁厚 $d_{wall}$ [m]，可按下式计算“薄壁电阻率”：

$$\eta_{thin,SI}=\frac{\eta_{wall,SI}}{d_{wall}} \text{ [Ω]}$$

把 `eta_thin_w` 设为此 SI 值。

#### 线圈

对线圈，输入参数 `resist` 指线圈的电阻，单位为欧姆（若线圈多于 1 匝，该值指所有匝合计）。相应的 $\eta_{thin,norm}$ 由它自动算出。

### 包含线圈 {#include-coils}
线圈需通过额外的线圈文件添加到 STARWALL 中。这些文件的名称在主 STARWALL 输入文件中由以下参数指定：

| 输入参数 | 说明 |
|---|---|
| `pol_coil_file` | 文件名，用于自由边界平衡、垂直反馈等的轴对称线圈 |
| `rmp_coil_file` | 文件名，非轴对称主动线圈 |
| `diag_coil_file` | 文件名，用作虚拟诊断的任意几何线圈 |
| `voltage_coil_file` | 文件名（尚未可用） |

一些示例线圈文件可在 STARWALL 仓库的 `coil_inputs/` 文件夹中找到。每个线圈文件包含两段。

**第一段**只包含线圈组的一般信息：

```fortran
&coil_set_nml
  description = 'short plain text description of this coil set'
  ncoil       = 1  ! number of coils in the set
/
```

**第二段**包含线圈属性的细节：

```fortran
&coils_nml
  ...
/
```

这里按以下各节所述指定每个线圈的属性。

#### 与类型无关的每个线圈的通用字段

```fortran
coil(1)%name            ! name of the coil
coil(1)%coil_type       ! can be axisym_thick, axisym_fila, general_thin (see below)
coil(1)%resist          ! resistance of the coil in Ohm
```

视 `coil_type` 而定，还需按下文所述提供额外信息。

#### 具有 dR 与 dZ 范围的轴对称线圈（`coil_type=axisym_thick`）

```fortran
coil(1)%R               ! Position in R (center of coil)
coil(1)%Z               ! Position in Z (center of coil)
coil(1)%dR              ! Full width in R
coil(1)%dZ              ! Full width in Z
coil(1)%nbands_R        ! Discretize coil by triangle bands in R direction
coil(1)%nbands_Z        ! Discretize coil by triangle bands in Z direction
coil(1)%ntorpts         ! Number of toroidal points
coil(1)%nturns          ! Number of turns for the coil
```

**更新（25.04.2022）：** 现在可以在不同的径向与垂直位置指定线圈带，例如用以表示同一电路中的电流回路。分部数由 `nparts_coil` 给出。每一部分都有 R、Z、dR 与 dZ 的取值。每一部分都可像以前那样在 R 与 Z 方向细分为若干带。旧输入文件向后兼容。

**使用新选项的输入：**

```fortran
coil(1)%nparts_coil      ! Number of coil parts N
coil(1)%R(N)             ! Position in R (center of coil)
coil(1)%Z(N)             ! Position in Z (center of coil)
coil(1)%dR(N)            ! Full width in R
coil(1)%dZ(N)            ! Full width in Z
coil(1)%nbands_R         ! Discretize coil by triangle bands in R direction
coil(1)%nbands_Z         ! Discretize coil by triangle bands in Z direction
coil(1)%ntorpts          ! Number of toroidal points
coil(1)%n_thick_turns(N) ! Number of turns per coil part
```

#### 由细丝指定的轴对称线圈（`coil_type=axisym_fila`）

```fortran
coil(1)%n_fila          ! Number of filaments for the coil
coil(1)%n_fila_turns    ! Number of turns in each filament
coil(1)%width           ! "Width" of the coil
coil(1)%R_fila          ! R-position of each filament
coil(1)%Z_fila          ! Z-position of each filament
coil(1)%ntorpts         ! Number of toroidal points
```

#### 由点列指定的 3D 线圈（`coil_type=general_thin`）

```fortran
coil(1)%n_pts           ! Number of points along the coil
coil(1)%width           ! "Width" of the coil
coil(1)%xpts            ! x-Position of each point along the coil
coil(1)%ypts            ! y-Position of each point along the coil
coil(1)%zpts            ! z-Position of each point along the coil
coil(1)%nturns          ! Number of turns for the coil
coil(1)%dir3d(n_pts*3)  ! OPTIONAL: for each point, give the direction of the band.
                        ! The norm corresponds to the coil width.
                        ! The order is dx1, dy1, dz1, ..., dxN, dyN, dzN
```
