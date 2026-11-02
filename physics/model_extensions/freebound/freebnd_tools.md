---
title: "自由边界诊断与工具"
nav_order: 6
parent: "自由边界扩展（STARWALL、CARIDDI）"
grand_parent: "模型扩展"
layout: default
render_with_liquid: false
---

本页旨在介绍与自由边界扩展相关的工具。你将在此找到

* [在不知道线圈电流的情况下构建自由边界平衡](#construct-a-free-boundary-equilibrium-without-knowing-the-coil-currents)
* [用于垂直稳定的主动控制器模型](#active-controller-model-for-vertical-stabilization)
* [计算壁面受力](#calculate-wall-forces)
* [计算真空中的磁场](#calculate-magnetic-fields-in-vacuum)
* [压缩 STARWALL 响应矩阵](#compress-starwall-response-matrices)


## 在不知道线圈电流的情况下构建自由边界平衡 {#construct-a-free-boundary-equilibrium-without-knowing-the-coil-currents}
上一节假定你已经知道自由边界平衡所需的正确线圈几何与电流。但如果你只是想在 JOREK 中创建新的等离子体，并开展自由边界研究（如破裂或垂直位移事件），该怎么办？又或者，你想通过改变线圈电流来模拟铁磁结构（如 JET 铁芯），又该怎么办？

我们实现了一个例程来简化这一过程，从而无需再手动尝试不同的线圈电流。

### 操作步骤

1. 创建你想转换为自由边界的固定边界平衡。
2. 将 `jorek00000.h5` 文件复制为 `jorek_restart.h5`（以使用该等离子体平衡）。
3. 在 JOREK 代码目录中运行：`make -j 8 jorek2_find_Icoils`
4. 准备一个线圈几何文件。示例文件见：
   - [aug_coils.zip](../assets/freebound/aug_coils.zip)
   - [iter_coils.zip](../assets/freebound/iter_coils.zip)
5. 将你的线圈几何文件命名为 `coils_geo.txt`。
6. 运行程序：`./jorek2_find_Icoils < input_JOREK`
7. 计算得到的线圈电流保存在 `Icoils_found.txt` 中。
8. **重要提示**：所得线圈电流是总电流（已乘以匝数）。若你为 STARWALL 线圈指定了匝数，则在把电流用于 JOREK 输入文件之前，须将所得电流除以 STARWALL 给定的匝数。

### 针对 JET

为预测为 20 个 JET 线圈供电的 10 条 JET 电路中的电流：

1. 在 JOREK 输入文件中设置 `tokamak_device='JET'`。
2. 使用 JET 线圈几何文件：[jet_coils.zip](../assets/freebound/jet_coils.zip)。
3. 要将所得 JET 总电流转换为 STARWALL 格式，需将每个线圈电流除以其匝数。可借助此 [excel 文件](../assets/freebound/turns_cf_star.xlsx) 完成转换。

## 用于垂直稳定的主动控制器模型 {#active-controller-model-for-vertical-stabilization}
为在包含 n=0 的自由边界模拟中实现主动稳定，JOREK 中加入了一个 PID 控制器。

### 基本原理

它依据垂直轴位置及其在模拟中的演化，作用于特定线圈，形式为：

$$\Delta I = K_P \, e(t) + K_D \frac{\mathrm{d} e(t)}{\mathrm{d} t} + K_I \int_{t_0}^{t} e(t)$$

其中 $e=Z(t)-Z_{\text{ref}}(t)$ 是相对参考值的偏差，$K_P$、$K_I$、$K_D$ 分别为比例、积分和微分增益。

### 在 JOREK 中的实现

上述方程经离散化后，在 PF 线圈电流分布插值完成之后，被构建进 vacuum/vacuum_response.dat 中的 coil_current_source 例程。其形式如下：

$$\begin{align}
\mathrm{d}Z_{\text{err}} &= Z_{\text{axis}}(t_n) - Z_{\text{ref}}(t_n)\\
\mathrm{d}Z_{\text{der}} &= \frac{Z_{\text{axis}}(t_n) - Z_{\text{axis}}(t_{n-1})}{\Delta t}\\
\mathrm{d}Z_{\text{integral}} &+= \left(Z_{\text{axis}}(t_n) - Z_{\text{ref}}(t_{n})\right)\Delta t \\
\Delta I &= K_P \, \mathrm{d}Z_{\text{err}} + K_D \, \mathrm{d}Z_{\text{der}} + K_I \, \mathrm{d}Z_{\text{integral}}\\
I(i) &= I(i) + \mathrm{vert\\_FB\\_amp\\_ts}(i) \, \Delta I  
\end{align}$$

它具有以下特性，参数列于下表：
  * 在特定时刻 start_VFB_ts 之后激活控制器
  * 使用恒定参考值或输入分布
  * 指定节拍时间（tact time），即控制器周期性动作的时间间隔
  * 为每个线圈单独设置电流限值
  * 为每个线圈单独设置放大系数以分配动作量

仅当指定了放大系数且已超过起始时间时，控制器才会被激活。

### 参数

| 参数 | 说明 | 典型值 |
|---|---|---|
| vert_FB_gain(1)                 | 比例增益 $K_P$                | 1.e0（视算例而定）  |
| vert_FB_gain(2)                 | **微分**增益 $K_D$              | 1.e0                   |
| vert_FB_gain(3)                 | **积分**增益 $K_I$                | 1.e0                   |
| start_VFB_ts [t<sub>JOREK</sub>]| 垂直反馈的起始时间               | -                      |
| vert_FB_amp_ts                  | 各个线圈的增益放大系数| 上线圈 >0，下线圈 <0    |
| I_coils_max [A]                 | PF 线圈中允许的最大电流        | 视算例而定     |
| vert_FB_tact [t<sub>JOREK</sub>]| 仅周期性施加 VFB                   | 可选          |
| Z_ref_ts(t)                     | 参考轴位置的时间历程         | 视算例而定     | 
| vert_pos_file [t<sub>JOREK</sub> \| m] | 时变轴位置的输入文件   |                   |

### 如何指定输入分布

位置可通过以下任一方式指定
  * 输入分布文件（vert_pos_file）
    * 时间以 [t<sub>JOREK</sub>] 给出
    * 垂直位置以 [m] 给出
    * 当模拟时长超出该分布所指定的范围时，使用该分布的最后一个值作为参考值。  
  * 输入参数 Z_axis_ref，它同样用于自由边界平衡
  * 若以上均未指定，则使用轴的初始值或重启值

### 调参

最优增益因算例而异，取决于平衡参数与使用场景。

通常，在控制器激活后的最初几个时间步内，轴会发生振荡。
可利用该振荡来调整增益。此外，也可利用目标值的突变（阶跃响应）来改进参数设置。

调参可分三步进行：
  - 在其他增益为 0 的情况下增大 $K_P$，直到振荡幅度较小、且在阶跃响应情形下超调较小。若 $K_P$ 过大，响应会超调，系统将变得不稳定。
  - 增大 $K_D$ 以减小振荡
  - 若稳态存在误差，则增大 $K_I$。（迄今我未观察到明显效果，仅用 $K_P$ 与 $K_D$ 增益时误差通常很低）



## 计算壁面受力 {#calculate-wall-forces}
该程序读取 JOREK 重启文件并计算总壁面受力。**你必须在完整自由边界模式（包括 n=0 模式）下运行模拟**。否则无法获知等离子体域之外的真空场。

它涉及等离子体内代价高昂的体积积分，因此对大算例应以多个 MPI 进程并行运行。提交与 JOREK 相同的作业脚本，将 `jorek_modelXXX` 替换为 `jorek2_wall_forces`。编译命令为：

```bash
make -j 8 jorek2_wall_forces
```

要选择 JOREK 重启文件，创建名为 `wall_forces.nml` 的文件，格式如下：

```fortran
&wall_forces
   istart     = 100   ! start index of restart file
   iend       = 1000  ! end index of restart file
   delta_step = 40    ! step interval
   scale_fact = 1.01  ! scaling factor of wall (1.01 default). 
   n_phi_int  = 64    ! number of points for integration in toroidal direction (for B-field)
/
```
受力导出到 `total_wall_forces_istart..iend..scale_fact.dat`。

#### 旧版格式

对于较早的版本，`wall_forces.nml` 只需一行：

```
0 1000 100
```
结果保存在 `total_wall_forces.dat` 中。

### 重要提示

为计算总壁面受力，需对包含 STARWALL 壁面的闭合曲面做积分（[参见本文式 7](https://iopscience.iop.org/article/10.1088/1741-4326/aa8876/meta)）。该例程假定描述此曲面的三角形具有特定排序（该曲面是 STARWALL 壁面的缩放版本）。取决于 STARWALL 中该排序的实现方式，三角形法向可能翻转符号，从而影响所计算受力的符号。**TODO：在例程中强制法向始终朝外，以确保总受力的符号正确。**

## 计算真空中的磁场 {#calculate-magnetic-fields-in-vacuum}
该程序读取 JOREK 重启文件并计算任意 (x,y,z) 点处的磁场。相对于 `jorek2_postroc` 的特殊之处在于，你还可以获得 JOREK 网格之外的场。例如，可用它从 JOREK 重启文件生成 GEQDSK 文件。

要获得完整的场，**你必须在完整自由边界模式（包括 n=0 模式）下运行模拟**。否则无法获知等离子体域之外的真空场。若以 `freeboundary=.false.` 运行，则只能得到等离子体电流产生的场。

它涉及等离子体内代价高昂的体积积分计算，因此对大算例应以多个 MPI 进程并行运行。提交与 JOREK 相同的作业脚本，将 `jorek_modelXXX` 替换为 `jorek2_fields_xyz`。编译命令为：

```bash
make -j 8 jorek2_fields_xyz
```

作为输入，须在文件 `xyz.nml` 中按如下格式给出笛卡尔坐标点：

```
number_of_points
x_1       y_1       z_1  
x_2       y_2       z_2  
 :         :         :   
 :         :         :   
x_n       y_n       z_n  
```

**切勿**把点精确指定在 STARWALL 线圈／壁面三角形上，否则这些点处可能出现奇异性！

要选择给定的 JOREK 重启文件，创建名为 `steps.nml` 的文件，第一行写 3 个整数（`istart`、`iend`、`delta_step`）。例如，要读取第 100 步到 520 步、间隔 10 步的重启文件，在 `steps.nml` 第一行写：

```
100  520  10
```

场导出到文件 `fields_xyz.dat`，并分别给出线圈、壁面与等离子体的贡献。

**注：** 为计算所需的等离子体场，`n_plane` 通常应大于 60（即使是 2D 情形）。

## 压缩 STARWALL 响应矩阵 {#compress-starwall-response-matrices}
> **警告：** 响应矩阵压缩尚未合并到标准 `develop` 分支。当前说明仅适用于未合并的特性分支，集成前可能发生变化。

有一个实验性工具可用奇异值分解压缩 STARWALL 响应矩阵。特性分支的要求、编译说明、参数以及当前限制见[压缩响应矩阵](compress_response_matrices.html)。
