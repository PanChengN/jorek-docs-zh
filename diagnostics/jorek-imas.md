---
title: "JOREK-IMAS"
nav_order: 5
parent: "诊断与后处理"
layout: default
render_with_liquid: false
---

# JOREK-IMAS

## IMAS 是什么？

集成建模与分析套件（IMAS）提供统一的数据模型与软件生态，用于在各类聚变程序之间交换实验数据与仿真数据。[IMAS Data Dictionary](https://github.com/iterorganization/IMAS-Data-Dictionary) 以与机器无关的**接口数据结构（IDSs）**实现该模型，其名称与结构均已标准化。

**新用户应先阅读[开源 IMAS 教程](https://github.com/iterorganization/IMAS-tutorial)。** 该教程的 notebook 介绍 IMAS、Data Dictionary、数据访问、IDS 探查与可视化，以及仿真数据库管理。教程是持续更新的文档，并链接到各组件维护中的说明。

## 开源 IMAS 组件

与 JOREK 用户相关的大部分 IMAS 软件都以公开方式开发：

| 组件 | 用途 |
| --- | --- |
| [IMAS Data Dictionary](https://github.com/iterorganization/IMAS-Data-Dictionary) | 定义 IMAS 数据模型，以及实验数据与仿真数据的 IDS 模式。 |
| [IMAS-Python](https://github.com/iterorganization/IMAS-Python) | 用于创建、读取、写入和操作 IDS 的 Python 库。 |
| [IMAS-Fortran](https://github.com/iterorganization/IMAS-Fortran) | Fortran 数据访问库，用于操作 IDS 结构并将其连接到可用的存储后端。 |
| [IMAS-ParaView](https://github.com/iterorganization/IMAS-ParaView) | 用于可视化 GGD 网格及其他 IMAS 数据的 ParaView 插件。它取代了此前的 GGD-VTK 工作流。 |
| [IMAS-MUSCLE3](https://github.com/iterorganization/IMAS-MUSCLE3) | 在 MUSCLE3 工作流中耦合兼容 IMAS 的程序的集成工具。其 actor 在耦合的组件之间交换 IDS 数据。 |
| [SimDB](https://github.com/iterorganization/SimDB) | 用于跟踪、查询、传输和管理仿真及其元数据的命令行工具与客户端—服务器工具。 |
| [SimDB Dashboard](https://github.com/iterorganization/SimDB-Dashboard) | 用于查询和查看远程 SimDB 数据库中仿真的 Web 界面。 |

更多开源聚变与 IMAS 代码仓库可从 [GitHub 上的 ITER Organization](https://github.com/iterorganization)获取。

## JOREK 用户如何从 IMAS 中获益？

- **获取初始平衡：** 由 equilibrium IDS 构建 JOREK 输入文件，包括 $FF'$、线圈电流与极向磁通分布。使用 [SimDB](https://github.com/iterorganization/SimDB) 或 [SimDB Dashboard](https://github.com/iterorganization/SimDB-Dashboard) 查找可用的仿真及其数据库元数据。

- **获取托卡马克部件：** 当真空室几何、第一壁板、诊断与线圈等规格包含在可访问的 IMAS 条目中时，从相应的 IDS 中读取这些规格。

- **归档、共享与引用仿真：** 将 JOREK 结果导出到 IDS，并用 SimDB 管理由此得到的仿真及其元数据。

- **可视化与处理 IMAS 数据：** 用 [IMAS-ParaView](https://github.com/iterorganization/IMAS-ParaView) 处理 GGD 网格、装置描述与诊断几何，或通过 [IMAS-Python](https://github.com/iterorganization/IMAS-Python) 与 [IMAS-Fortran](https://github.com/iterorganization/IMAS-Fortran) 直接操作 IDS。

- **将 JOREK 与其他程序耦合、构建工作流：** MUSCLE3 可将 JOREK 与其他程序耦合，例如由 JOREK 输出计算合成诊断信号。[IMAS-MUSCLE3](https://github.com/iterorganization/IMAS-MUSCLE3) 提供在耦合组件之间交换 IDS 数据的 actor。

## 由 IMAS 条目创建 JOREK 输入文件

1. 按照 [IMAS 教程](https://github.com/iterorganization/IMAS-tutorial)熟悉 IDS 与当前的数据访问工具。
2. 用 [SimDB Dashboard](https://github.com/iterorganization/SimDB-Dashboard) 找到合适的仿真。记录标识该 IMAS 条目的 user、database、pulse 与 run，然后选择包含合适平衡的时间片。
3. 配置本机站点所需的 IMAS 数据访问环境。安装与使用说明在 [IMAS-Python](https://github.com/iterorganization/IMAS-Python) 仓库中维护；模块名与可用的存储后端可能因站点而异。
4. 在 `communication/IMAS` 目录下运行 `imas2jorek.py`，并用所选条目与时间替换全大写的占位符：

```bash
python imas2jorek.py \
    --user USER \
    --database DATABASE \
    --pulse PULSE \
    --run RUN \
    --time TIME
```

用下列命令显示所有参数及其默认值，包括存储后端、Data Dictionary 主版本、IDS occurrence，以及用于构造边界的托卡马克：

```bash
python imas2jorek.py -h
```

该脚本的用法与 `eqdsk2jorek` 类似。`--tokamak`（`-tk`）选项指定用于构造初始 $R$-$Z$ 边界的托卡马克；请按需检查并调整生成的网格边界。

`imas2jorek.py` 运行结束后会生成：

- `jorek_namelist`，包含极向磁通边界条件与线圈电流。
- `jorek_density`、`jorek_temperature` 与 `jorek_ffprime`，包含剖面。

## 将 JOREK 数据导出到 IMAS

加载 IMAS 模块。在 ITER 集群上：

```bash
module load IMAS
```

`jorek2_IDS` 工具将 JOREK 的 HDF5 重启文件转换为 IMAS 数据。在 `Makefile.inc` 中启用 IMAS 接口，并给出 Access Layer 的编译与链接标志：

```makefile
USE_IMAS = 1

IMASINCLUDE=`pkg-config --cflags-only-I al-fortran`
IMASLIB=`pkg-config --libs-only-L --libs-only-l al-fortran`

# For the old Access Layer 4, use these lines instead:
# IMASINCLUDE=`pkg-config --cflags-only-I imas-ifort`
# IMASLIB=`pkg-config --libs-only-L --libs-only-l imas-ifort`
```

按仿真所用的模型与环向分辨率一致地配置 `jorek2_IDS`，然后编译。例如：

```bash
util/config.sh n_tor=1 n_period=1 n_plane=1 with_TiTe=.false. with_vpar=.false. with_impurities=.true.
make -j 8 jorek2_IDS
```

在包含重启文件的算例目录中创建 `imas.nml`。下面的注释说明了各参数的含义：

```fortran
&imas_params

  ! --- Where is this simulation going to be stored?
  user        = 'artolaj'           ! your username
  database    = 'test_database'     ! your local database, if it does not exist it will create a new one
  shot_number = 111111              ! choose a shot or reference number
  run_number  = 1                   ! choose a run number
  overwrite_entry = .false.         ! If true:  it will overwrite pre-existing entries in the database (CAREFUL!!)
                                    ! If false: it will append the data to existing IDSs

  ! --- Which restart files are going to be exported?
  i_begin     = 700           ! Do not consider restart files before 700
  i_end       = 5000          ! Do not consider restart files after 5000
  i_jump_steps= 100           ! jump restart files by this step

  ! --- Which IDSs are going to be exported?
  export_JOREK_variables  = .true.     ! --- Exports JOREK raw variables to occurrence 1 of plasma_profiles
  export_1d_profiles      = .false.    ! --- Exports 1D flux-averaged profiles to occurrence 0 of plasma_profiles
  export_equilibrium      = .false.
  export_summary          = .false.
  export_disruption       = .false.
  export_wall             = .false.    ! --- Needs free-boundary mode
  export_pf_passive       = .false.    ! --- Needs free-boundary mode
  export_pf_active        = .false.    ! --- Needs free-boundary mode
  export_radiation        = .false.    ! --- Only working with SPI simulations with marker model
  export_spi              = .false.    ! --- Needs SPI simulation
  export_field_extension  = .false.    ! --- Export psi(n=0) and B(3D) to a rectangular grid that goes beyond
                                       ! ---    the JOREK grid. The n=0 components are stored in
                                       ! ---    equilibrium/profiles_2D and the 3D fields in plasma_profiles
                                       ! ---    occurrence 2.

  ! --- Geometry of coils and passive components (as in STARWALL input)
  ! --- These are needed to export the coil geometries in the IDSs pf_active & pf_passive
  passive_coil_geo_file = 'passive_components.nml'
  active_coil_geo_file  = 'polcoils_iter.nml'

  ! --- If true, read only radiation projections for the non-coronal equilibrium model
  rad_only_projections_h5 = .false.

  ! --- Brief description of the simulation
  simulation_description = 'JOREK 2D disruption simulation.'

  ! --- Parameters defining the rectangular grid used in equilibrium and plasma_profiles occurrence 2.
  rect_grid_params%nR    = 100
  rect_grid_params%nZ    = 200
  rect_grid_params%R_min = 3.d0
  rect_grid_params%R_max = 10.d0
  rect_grid_params%Z_min = -6.d0
  rect_grid_params%Z_max = 6.d0

/
```

用单个 MPI 进程运行该转换器：

```bash
mpirun -n 1 ./jorek2_IDS < jorek_input_file
```

导出成功时会打印形如 `XXXXX IDS exported` 的消息。随后可用 [IMAS-ParaView](https://github.com/iterorganization/IMAS-ParaView) 查看所存数据，或用 [IMAS-Python](https://github.com/iterorganization/IMAS-Python) 与 [IMAS-Fortran](https://github.com/iterorganization/IMAS-Fortran) 直接处理。

## 可用的 IDS 节点

下面列出目前可填充的 IDS 与变量。

### `summary`

```text
summary_ids.ids_properties.homogeneous_time
summary_ids.ids_properties.comment
summary_ids.time
summary_ids.global_quantities.r0.value
summary_ids.global_quantities.b0.value
summary_ids.global_quantities.beta_pol.value
summary_ids.global_quantities.beta_tor.value
summary_ids.global_quantities.beta_tor_norm.value
summary_ids.global_quantities.ip.value
summary_ids.global_quantities.li_3.value
summary_ids.global_quantities.volume.value
summary_ids.global_quantities.q_95.value
summary_ids.global_quantities.energy_thermal.value
summary_ids.global_quantities.energy_b_field_pol.value
summary_ids.global_quantities.power_ohm.value
summary_ids.global_quantities.power_radiated.value
summary_ids.heating_current_drive.power_additional.value
summary_ids.local.magnetic_axis.position.r
summary_ids.local.magnetic_axis.position.z
summary_ids.local.magnetic_axis.position.psi
summary_ids.boundary.type.value
summary_ids.boundary.minor_radius.value
summary_ids.boundary.elongation.value
summary_ids.boundary.triangularity_upper.value
summary_ids.boundary.triangularity_lower.value
summary_ids.boundary.geometric_axis_r.value
summary_ids.boundary.geometric_axis_z.value
```

### `plasma_profiles`（occurrence 0）

使用 $n=0$ 的极向磁通，给出按极向磁通平均的剖面。

```text
plasma_profiles_ids.profiles_1d.grid.psi_magnetic_axis
plasma_profiles_ids.profiles_1d.grid.psi_boundary
plasma_profiles_ids.profiles_1d.grid.rho_pol_norm
plasma_profiles_ids.profiles_1d.grid.psi

plasma_profiles_ids.profiles_1d.t_i_average
plasma_profiles_ids.profiles_1d.electrons.temperature
plasma_profiles_ids.profiles_1d.electrons.density
plasma_profiles_ids.profiles_1d.pressure_thermal
plasma_profiles_ids.profiles_1d.phi_potential
plasma_profiles_ids.profiles_1d.conductivity_parallel
plasma_profiles_ids.profiles_1d.j_total
plasma_profiles_ids.profiles_1d.e_field.parallel
plasma_profiles_ids.profiles_1d.e_field.radial
plasma_profiles_ids.profiles_1d.ion.velocity.parallel
plasma_profiles_ids.profiles_1d.ion.velocity.poloidal
plasma_profiles_ids.profiles_1d.ion.velocity.diamagnetic
plasma_profiles_ids.profiles_1d.zeff
plasma_profiles_ids.profiles_1d.ion.density
plasma_profiles_ids.profiles_1d.ion.element.a
plasma_profiles_ids.profiles_1d.neutral.density
plasma_profiles_ids.profiles_1d.neutral.element.a
plasma_profiles_ids.profiles_1d.ion.element.z_n
plasma_profiles_ids.profiles_1d.q
plasma_profiles_ids.profiles_1d.grid.rho_tor_norm
```

### `plasma_profiles`（occurrence 1）

包含高精度的 JOREK 原始变量。该 IDS 可用于准确计算电流密度与磁场。它还包含电子与离子温度、质量密度、静电势以及环向涡量。有限元系数与傅里叶级数系数以 GGD 格式存储，可用 [IMAS-ParaView](https://github.com/iterorganization/IMAS-ParaView) 可视化。

```text
plasma_profiles_ids.ids_properties.homogeneous_time
plasma_profiles_ids.time

plasma_profiles_ids.ggd.time
plasma_profiles_ids.ggd.psi
plasma_profiles_ids.ggd.phi_potential
plasma_profiles_ids.ggd.r_j_total_phi
plasma_profiles_ids.ggd.vorticity_over_r
plasma_profiles_ids.ggd.mass_density
plasma_profiles_ids.ggd.electrons.temperature
plasma_profiles_ids.ggd.t_i_average
plasma_profiles_ids.ggd.velocity_parallel_over_b_field
plasma_profiles_ids.ggd.ion.element.a
plasma_profiles_ids.ggd.ion.element.z_n
plasma_profiles_ids.ggd.ion.density
plasma_profiles_ids.ggd.neutral.element.a
plasma_profiles_ids.ggd.neutral.element.z_n
plasma_profiles_ids.ggd.neutral.density

##Grid
plasma_profiles.grid_ggd[0].identifier.description
plasma_profiles.grid_ggd[0].identifier.name
plasma_profiles.grid_ggd[0].identifier.index

plasma_profiles.grid_ggd[0].grid_subset[0].identifier.name
plasma_profiles.grid_ggd[0].grid_subset[0].identifier.index
plasma_profiles.grid_ggd[0].grid_subset[0].identifier.description
plasma_profiles.grid_ggd[0].grid_subset[0].dimension

plasma_profiles.grid_ggd[0].space[0].geometry_type.index
plasma_profiles.grid_ggd[0].space[0].coordinates_type
plasma_profiles.grid_ggd[0].space[0].objects_per_dimension[0].object[:].geometry
plasma_profiles.grid_ggd[0].space[0].objects_per_dimension[0].object[:].geometry_2d
plasma_profiles.grid_ggd[0].space[0].objects_per_dimension[2].object[:].nodes
plasma_profiles.grid_ggd[0].space[0].objects_per_dimension[2].object[:].geometry_2d

plasma_profiles.grid_ggd[0].space[1].coordinates_type
plasma_profiles.grid_ggd[0].space[1].geometry_type.index
plasma_profiles.grid_ggd[0].space[1].identifier.description
plasma_profiles.grid_ggd[0].space[1].objects_per_dimension[0].object[:].geometry
```

### `plasma_profiles`（occurrence 2）

在超出 JOREK 网格的矩形网格上给出 $B_R$ 与 $B_Z$ 磁场分量。仅当 `export_field_extension = .true.` 的完整自由边界仿真才可用。$(R,Z)$ 空间是规则二维网格，节点上存的是数值而非贝塞尔系数，而环向方向仍保留傅里叶表示。该 occurrence 面向 SMITER 之类的磁力线追踪程序。

```text
plasma_profiles_ids.ids_properties.homogeneous_time
plasma_profiles_ids.time
plasma_profiles_ids.ggd.b_field

##Grid
plasma_profiles.grid_ggd[0].identifier.description
plasma_profiles.grid_ggd[0].identifier.name
plasma_profiles.grid_ggd[0].identifier.index

plasma_profiles.grid_ggd[0].grid_subset[0].identifier.name
plasma_profiles.grid_ggd[0].grid_subset[0].identifier.index
plasma_profiles.grid_ggd[0].grid_subset[0].identifier.description
plasma_profiles.grid_ggd[0].grid_subset[0].dimension

plasma_profiles.grid_ggd[0].space[0].geometry_type.index
plasma_profiles.grid_ggd[0].space[0].coordinates_type
plasma_profiles.grid_ggd[0].space[0].objects_per_dimension[0].object[:].geometry
plasma_profiles.grid_ggd[0].space[0].objects_per_dimension[2].object[:].nodes

plasma_profiles.grid_ggd[0].space[1].coordinates_type
plasma_profiles.grid_ggd[0].space[1].geometry_type.index
plasma_profiles.grid_ggd[0].space[1].identifier.description
plasma_profiles.grid_ggd[0].space[1].objects_per_dimension[0].object[:].geometry
```

### `wall`

`wall` IDS 包含两种壁描述：

- ITER 真空室内层，表示为用线性三角形单元离散的薄壁。每个三角形都给出电流密度矢量、有效厚度与电阻率。
- ITER 第一壁的轴对称表示。入射垂直热流、用于晕电流（halo current）计算的电流密度矢量以及极向磁通存储在三角形网格的节点上。

这些量可用 [IMAS-ParaView](https://github.com/iterorganization/IMAS-ParaView) 可视化。

```text
wall_ids.ids_properties.homogeneous_time
wall_ids.time

# Vacuum vessel inner layer
wall_ids.description_ggd[0].ggd[:].j_total
wall_ids.description_ggd[0].ggd[:].resistivity

# First wall surface
wall_ids.description_ggd[1].ggd[:].j_total
wall_ids.description_ggd[1].ggd[:].power_density
wall_ids.description_ggd[1].ggd[:].psi

# Grid
wall_ids.description_ggd[:].type.index
wall_ids.description_ggd[:].grid_ggd[0]identifier.index
wall_ids.description_ggd[:].grid_ggd[0]identifier.description
wall_ids.description_ggd[:].grid_ggd[0]grid_subset[0].identifier.index
wall_ids.description_ggd[:].grid_ggd[0]grid_subset[0].dimension
wall_ids.description_ggd[:].grid_ggd[0]space[0].identifier.index
wall_ids.description_ggd[:].grid_ggd[0]space[0].geometry_type.index
wall_ids.description_ggd[:].grid_ggd[0]space[0].coordinates_type
wall_ids.description_ggd[:].grid_ggd[0]space[0].objects_per_dimension[0].geometry_content.index
wall_ids.description_ggd[:].grid_ggd[0]space[0].objects_per_dimension[0].object[:].geometry
wall_ids.description_ggd[:].grid_ggd[0]space[0].objects_per_dimension[2].object[:].nodes

wall_ids.description_ggd[:].thickness[0].grid_subset[0].grid_index
wall_ids.description_ggd[:].thickness[0].grid_subset[0].grid_subset_index
wall_ids.description_ggd[:].thickness[0].grid_subset[0].values

wall_ids.description_ggd[:].component[0].type[0].grid_index
wall_ids.description_ggd[:].component[0].type[0].grid_subset_index
wall_ids.description_ggd[:].component[0].type[0].identifier.index
wall_ids.description_ggd[:].component[0].type[0].identifier.name
wall_ids.description_ggd[:].component[0].type[0].identifier.description
```

### `pf_passive`

`pf_passive` IDS 包含可在其中感应出电流的附加无源导体：真空室外层、外部三角形支撑以及偏滤器内侧导轨。它们按环向回路离散。

```text
pf_passive.ids_properties.homogeneous_time
pf_passive.time
pf_passive.loop.name
pf_passive.loop.resistance
pf_passive.loop.element.turns_with_sign
pf_passive.loop.element.geometry.geometry_type
pf_passive.loop.element.geometry.rectangle.r
pf_passive.loop.element.geometry.rectangle.z
pf_passive.loop.element.geometry.rectangle.width
pf_passive.loop.element.geometry.rectangle.height
pf_passive.loop.current
```

### `pf_active`

```text
pf_active.ids_properties.homogeneous_time
pf_active.time
pf_active.coil.name
pf_active.coil.resistance
pf_active.coil.element.turns_with_sign
pf_active.coil.element.geometry.geometry_type
pf_active.coil.element.geometry.rectangle.r
pf_active.coil.element.geometry.rectangle.z
pf_active.coil.element.geometry.rectangle.width
pf_active.coil.element.geometry.rectangle.height
pf_active.coil.current.data
```

### `disruption`

```text
disruption_ids.ids_properties.homogeneous_time
disruption_ids.time
disruption_ids.global_quantities.current_halo_pol
disruption_ids.global_quantities.current_halo_phi
disruption_ids.global_quantities.power_ohm
disruption_ids.global_quantities.power_ohm_halo
disruption_ids.global_quantities.power_parallel_halo
disruption_ids.global_quantities.power_radiated_electrons_impurities
```

### `spi`

```text
spi.ids_properties.homogeneous_time
spi.time
spi.injector.pellet.core.atoms_n
spi.injector.pellet.core.species.a
spi.injector.pellet.core.species.z_n
spi.injector.pellet.core.species.density
spi.injector.velocity_mass_centre_fragments_r
spi.injector.velocity_mass_centre_fragments_z
spi.injector.velocity_mass_centre_fragments_tor
spi.injector.fragment.position.r
spi.injector.fragment.position.z
spi.injector.fragment.position.phi
spi.injector.fragment.velocity_r
spi.injector.fragment.velocity_z
spi.injector.fragment.velocity_tor
spi.injector.fragment.volume
```

### `equilibrium`

```text
equilibrium_ids.ids_properties.homogeneous_time
equilibrium_ids.time

equilibrium_ids.time_slice.profiles_1d.psi
equilibrium_ids.time_slice.profiles_1d.pressure
equilibrium_ids.time_slice.profiles_1d.dpressure_dpsi
equilibrium_ids.time_slice.profiles_1d.f_df_dpsi
equilibrium_ids.time_slice.profiles_1d.j_parallel
equilibrium_ids.time_slice.profiles_1d.q
equilibrium_ids.time_slice.profiles_1d.rho_tor_norm

equilibrium_ids.vacuum_toroidal_field.r0
equilibrium_ids.vacuum_toroidal_field.b0

equilibrium_ids.time_slice.global_quantities.psi_axis
equilibrium_ids.time_slice.global_quantities.psi_boundary
equilibrium_ids.time_slice.global_quantities.magnetic_axis.r
equilibrium_ids.time_slice.global_quantities.magnetic_axis.z
equilibrium_ids.time_slice.global_quantities.beta_pol
equilibrium_ids.time_slice.global_quantities.beta_tor
equilibrium_ids.time_slice.global_quantities.beta_tor_norm
equilibrium_ids.time_slice.global_quantities.ip
equilibrium_ids.time_slice.global_quantities.li_3
equilibrium_ids.time_slice.global_quantities.volume
equilibrium_ids.time_slice.global_quantities.area
equilibrium_ids.time_slice.global_quantities.current_centre.r
equilibrium_ids.time_slice.global_quantities.current_centre.z
equilibrium_ids.time_slice.global_quantities.q_axis
equilibrium_ids.time_slice.global_quantities.q_95
equilibrium_ids.time_slice.global_quantities.energy_mhd
equilibrium_ids.time_slice.boundary.type
equilibrium_ids.time_slice.boundary.psi
equilibrium_ids.time_slice.boundary.minor_radius
equilibrium_ids.time_slice.boundary.elongation
equilibrium_ids.time_slice.boundary.triangularity_upper
equilibrium_ids.time_slice.boundary.triangularity_lower
equilibrium_ids.time_slice.boundary.geometric_axis.r
equilibrium_ids.time_slice.boundary.geometric_axis.z
equilibrium_ids.time_slice.boundary.closest_wall_point.r
equilibrium_ids.time_slice.boundary.closest_wall_point.z
equilibrium_ids.time_slice.boundary.closest_wall_point.distance
equilibrium_ids.time_slice.contour_tree.node.critical_type
equilibrium_ids.time_slice.contour_tree.node.r
equilibrium_ids.time_slice.contour_tree.node.z
equilibrium_ids.time_slice.contour_tree.node.psi

equilibrium_ids.time_slice.boundary.outline.r
equilibrium_ids.time_slice.boundary.outline.z

equilibrium_ids.time_slice.profiles_2d.type.index
equilibrium_ids.time_slice.profiles_2d.grid_type.index
equilibrium_ids.time_slice.profiles_2d.grid.dim1
equilibrium_ids.time_slice.profiles_2d.grid.dim2
equilibrium_ids.time_slice.profiles_2d.r
equilibrium_ids.time_slice.profiles_2d.z
equilibrium_ids.time_slice.profiles_2d.psi         #extended to vacuum if using export_field_extension
equilibrium_ids.time_slice.profiles_2d.j_phi
equilibrium_ids.time_slice.profiles_2d.b_field_r   #extended to vacuum if using export_field_extension
equilibrium_ids.time_slice.profiles_2d.b_field_z   #extended to vacuum if using export_field_extension
equilibrium_ids.time_slice.profiles_2d.b_field_phi
```

### `radiation`

仅在使用标记粒子的 SPI 仿真中可用。

```text
The GGD structures are identical to those of plasma_profiles/1, otherwise

radiation_ids.time
radiation_ids.process.ggd.time

radiation_ids.process.identifier.name
radiation_ids.process.identifier%description
radiation_ids.process.identifier%index
radiation.process[0].ggd.ion[0].emissivity.coefficients
```
