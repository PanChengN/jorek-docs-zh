---
title: "JOREK 文档主页"
nav_order: 1
nav_exclude: true
layout: default
render_with_liquid: false
---

- **[JOREK 网站](https://www.jorek.eu)** → 如有遗漏请[发送邮件](mailto:mhoelzl@ipp.mpg.de) \| [添加到图库](https://www.jorek.eu)
- **[JOREK 新用户须知](jorek_access.md)** \| **[代码许可证](code_license.md)**
- **[发表规则](publication_rules.md)** \| **[JOREK 徽标](jorek_logo.md)** \| **[jorek-preprint@jorek.eu](mailto:jorek-preprint@jorek.eu)**
- **[常见问题（FAQ）](faq.md)**
- **[为文档做贡献](contributing.md)**

### [编译与运行](compiling/cat_compiling.md)

- [获取源代码](compiling/get_jorek.md) \| [编译与依赖库](compiling/compilation_and_libraries.md) \| [运行](compiling/running.md)
- **[HPC 与 PC 配置](compiling/compilation_and_libraries/hpc_pc_configurations.md)**
  - [Leonardo-CPU](compiling/compilation_and_libraries/hpc_pc_configurations/leonardo-cpu.md) \| [LUMI-CPU](compiling/compilation_and_libraries/hpc_pc_configurations/lumi-cpu.md) \| [Pitagora-CPU](compiling/compilation_and_libraries/hpc_pc_configurations/pitagora-cpu.md) \| [Pitagora-GPU](compiling/compilation_and_libraries/hpc_pc_configurations/pitagora-gpu.md) \| [IPP Garching](compiling/compilation_and_libraries/hpc_pc_configurations/run_at_ipp_garching.md) \| [ITER 集群](compiling/compilation_and_libraries/hpc_pc_configurations/iter_cluster.md) \| [EUROfusion Gateway](compiling/compilation_and_libraries/hpc_pc_configurations/eurofusion_gateway.md) \| [TGCC-CEA](compiling/compilation_and_libraries/hpc_pc_configurations/tgcc-cea.md) \| [macOS](compiling/compilation_and_libraries/hpc_pc_configurations/macos.md)
- **[输入参数列表](compiling/input.md)**
- **[诊断与后处理](diagnostics/cat_diagnostics.md)**
  - [诊断工具与脚本](diagnostics/diagnostics.md) \| [JOREK-IMAS](diagnostics/jorek-imas.md)

### 代码开发

- **[开发流程](code_development/development_workflow.md)**
- **[回归测试](code_development/nrt.md)**

### 物理模型

- **[符号约定](physics/notation.md)**
- **[归一化](physics/normalization.md)**
- **[矢量恒等式](physics/vector-identities.md)**
- **[坐标系](physics/coordinates.md)**
- **[基础流体模型](physics/base_fluid_models/base_fluid_models.md)**
  - [托卡马克约化 MHD](physics/base_fluid_models/reduced_mhd.md)
  - [托卡马克 full MHD](physics/base_fluid_models/full_mhd.md)
  - [仿星器约化 MHD](physics/base_fluid_models/jorek3d.md)
- **[动理学粒子模块](physics/particles.md)**
- **[模型扩展](physics/model_extensions/model_extensions.md)**
  - [自由边界扩展（STARWALL、CARIDDI）](physics/model_extensions/freebound.md)
  - 杂质：[流体模型](physics/model_extensions/impurities_fluid.md) \| [标记粒子模型](physics/model_extensions/impurities_marker.md) \| [动理学模型](physics/model_extensions/impurities_kinetic.md)
    - [ADAS 原子数据](physics/model_extensions/adas.md)
  - 中性粒子：[流体模型](physics/model_extensions/neutrals_fluid.md) \| [动理学模型](physics/model_extensions/neutrals_kinetic.md)
  - 逃逸电子：[流体模型](physics/model_extensions/runaway_fluid.md) \| [动理学模型](physics/model_extensions/runaway_kinetic.md)

### 数值方法与工具

- [空间离散](numerics/spatial-discretization.md) \| [网格](numerics/grids.md)
- [时间积分](numerics/time-integration.md)
- [单元矩阵 FFT](numerics/element_matrix_fft.md)
- [求解器与预条件器](numerics/solver.md) \| [稀疏矩阵格式](numerics/sparse-matrix.md) 
- [随机数生成器](numerics/rngs.md)
- [HDF5 工具](numerics/hdf5tools.md)

### 操作指南

- 从 **[JOREK](howto/running_jorek_for_the_first_time.md)**、**[JOREK-STARWALL](howto/running_jorek-starwall_for_the_first_time.md)**、**[JOREK-CARIDDI](howto/running_jorek-cariddi_for_the_first_time.md)** 和 **[JOREK 诊断工具](howto/introduction_to_jorek_diagnostics.md)** 入门
- 搭建 **[JOREK 仿真网格](howto/wallgrid_tutorial.md)**
- 使用 **[eqdsk2jorek](howto/eqdsk2jorek.md)** 将 EFIT 平衡数据转换为 JOREK 输入
- 获取 **[稳态剖面所需的 D_perp 与 ZK_perp](howto/physics_options/plasma_functions_and_coefficients/diffusion_coef.md)**
- 检查 **[能量守恒](diagnostics/energy_conservation.md)**
- 运行包含 **[抗磁漂移](howto/physics_options/physical_terms/diamag.md)**、**[新经典效应](howto/physics_options/physical_terms/neo.md)** 以及 **[在黏性项中包含抗磁漂移](howto/physics_options/physical_terms/wdia.md)** 的算例
- 运行包含 **[Taylor-Galerkin 稳定化](howto/tgnum.md)** 与 **[负密度／负温度的修正](howto/corr_neg.md)**（变通方案）的算例
- 运行包含 **[RMP](howto/physics_options/controllers_and_actuators/rmp.md)** 的算例（旧边界条件，不使用 STARWALL）
- 计算 JOREK 网格内部与外部的 **B**（**[jorek2_fields_xyz](howto/jorek2_fields_xyz.md)**）
- 计算 **[壁面总受力](howto/jorek2_wall_forces.md)**（需要 JOREK-STARWALL）
- 运行包含 **[欧姆加热](howto/physics_options/physical_terms/ohmic_heating.md)** 的算例
- 运行使用 **[鞘层热流边界条件](howto/physics_options/boundary_conditions/sheath_heatflux_bc.md)** 的算例
- 运行 **[MGI 仿真](howto/mgi_tutorial.md)** 与 **[SPI 仿真](howto/spi_tutorial.md)**
- 设置 **[Spitzer 电阻率](howto/physics_options/plasma_functions_and_coefficients/spitzer_resistivity.md)** 与各向异性热扩散
- 由 **[限制器等离子体生成 X 点等离子体](howto/x-point_from_limiter.md)**
- 运行使用 **[预条件器中的模式组](howto/mode_groups.md)** 的算例
- **[选择边界条件](howto/physics_options/boundary_conditions/choose_boundary_conditions.md)**
- **[如何使用激波捕捉功能](howto/shock_capturing.md)**
- **[运行仿星器仿真](howto/stellarator_setup.md)**
- **[在 VTK 中绘制方程项](howto/plot_rhs_terms.md)**
- **[使用相空间投影](howto/particles_phase_space.md)**
- **[用粒子追踪器评估粒子壁负载](howto/particles_wall_load.md)**
- **[用磁力线追踪评估三维壁面上的流体负载](howto/fluid_wall_load.md)**
- **[用粒子追踪器生成 Poincaré 图](howto/particles_poincare.md)**
- **[粒子追踪器中的逃逸电子物理](howto/particles_runaways.md)**
- **[使用控制器模块](howto/physics_options/controllers_and_actuators/using_controller_module.md)**
- 运行使用 **[非线性时间推进（Newton 迭代）](howto/inexact_newton_solver.md)** 的算例
- **[重建 namelist 输入参数的修改过程](howto/nml2h5.md)**
- **[在 ParaView 图中显示时间](howto/showing_time_in_paraview.md)**
- **[full MHD 模型 750 中的可变多尺度（VMS）稳定化](howto/vms.md)**
- 编译并运行 **[粒子快速相机](howto/particle_fast_camera.md)**
- **[运行含偏滤器区域的仿星器模型](howto/stellarator_with_divertor.md)**
- **[运行包含动理学中性粒子与杂质的算例](howto/ncs_ics_tutorial.md)**
- 运行包含 **[中性粒子—中性粒子碰撞](howto/neutral_neutral_collisions.md)** 的粒子仿真
- 激活 **[密度方程中的内向箍缩项](howto/physics_options/physical_terms/inward_pinch_term.md)**
- **[在 JOREK 中计算平行电场 $E_{\\vert\\vert}$](physics/base_fluid_models/RMHD/expressions_and_derivations/efield_in_jorek.md)**
- **[螺旋度守恒](physics/base_fluid_models/RMHD/expressions_and_derivations/helicity_conservation.md)**

### 装置、坐标、几何、合成诊断与参考算例

- **[ITER](machines/iter.md)**
- **[JET](machines/jet.md)**
- **[ASDEX Upgrade](machines/asdex_upgrade.md)**
