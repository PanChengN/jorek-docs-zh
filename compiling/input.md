---
title: "输入参数列表"
nav_order: 4
parent: "编译与运行"
layout: default
render_with_liquid: false
---

<!--
  AUTO-GENERATED FILE - DO NOT EDIT BY HAND.
  Regenerate by running ./util/parameter-overview.py from the repo root.
-->

<style>
  /* Target the tables directly rather than a `.params-table` class: kramdown's
     `{: .params-table}` IAL does not reliably attach to very large tables.
     All column widths use `em` (no percentages): mixing `%` text columns with
     `em` numeric columns under `table-layout: fixed` + `min-width: 100%` makes
     Firefox resolve the percentages against the wrong basis and collapse the
     text columns. With uniform `em` widths both engines distribute leftover
     space proportionally, keeping the description column widest. Scoped to
     .main-content so it only affects this page's parameter tables. */
  .main-content table { table-layout: fixed; width: 100%; font-size: 0.9em; }
  .main-content table th, .main-content table td {
      word-wrap: break-word; overflow-wrap: break-word; vertical-align: top; padding: 4px 6px;
  }
  .main-content table th:nth-child(1), .main-content table td:nth-child(1) { width: 10em; }
  .main-content table th:nth-child(2), .main-content table td:nth-child(2) { width: 8em; }
  .main-content table th:nth-child(3), .main-content table td:nth-child(3) { width: 30em; }
  .main-content table th:nth-child(n+4), .main-content table td:nth-child(n+4) {
      width: 2.2em; text-align: center;
  }
</style>

# 输入参数列表

> **⚠️ 自动生成的文件——请勿手工编辑。**
> 本页由 Fortran 源码生成。任何手工修改都会在下次运行生成器时
> 被覆盖。如需更新，请在仓库根目录运行
> `./util/parameter-overview.py` 并提交结果。

## phys_module

| 参数 | 默认值 | 说明 | 180 | 183 | 199 | 600 | 710 | 711 | 712 | 750 |
|---|---|---|---|---|---|---|---|---|---|---|
| **eta** | 1.d-5 | 等离子体中心处的电阻率（归一化） | x | x | x | x | x | x | x | x |
| **eta_ohmic** | 0. | 用于欧姆加热项的芯部电阻率 | x | x | x | x | x | x | x | x |
| **eta_T_dependent** | .true. | 电阻率是否依赖温度？否则为常数 | x | x | x | x | x | x | x | x |
| **eta_coul_log_dep** | .true. | 电阻率是否依赖库仑对数的变化？ |  |  |  | x |  |  |  | x |
| **T_max_eta** | 1.d99 | 电阻率被截断的温度上限（谨慎使用；仅出于数值原因） |  |  |  | x |  |  |  |  |
| **T_max_eta_ohm** | 1.d99 | 欧姆加热项中所用电阻率被截断的温度上限（谨慎使用；仅出于数值原因） |  |  |  | x |  |  |  |  |
| **T_max_visco** | 1.d99 | 黏性被截断的温度上限；其目的是在启用 T_max_eta 时保持普朗特数不变。 |  |  |  | x |  |  |  |  |
| **visco** | 1.d-5 | 等离子体中心处的黏性（归一化） | x | x | x | x | x | x | x | x |
| **visco_heating** | 0. | 垂直黏性加热项中所用的黏性 |  |  |  | x |  |  |  |  |
| **visco_T_dependent** | .true. | 黏性是否依赖温度？否则为常数。 | x | x | x | x | x | x | x | x |
| **visco_old_setup** | .false. | 若为 true，则为保持兼容而采用旧的垂直黏性处理方式（旧 visco 依赖 R^2） |  |  |  | x |  |  |  |  |
| **visco_par** | 1.d-5 | 作用于平行流的跨磁场黏性（归一化） | x | x | x | x | x | x | x | x |
| **visco_par_par** | 0. | 作用于平行流的沿磁场平行黏性（归一化） |  | x |  | x |  |  |  |  |
| **visco_par_heating** | 0. | 平行黏性加热项中所用的平行黏性（归一化） |  |  |  | x |  |  |  |  |
| **TiTe_ratio** | 0.5 | 由 T 设定离子与电子温度的比例（在模型 180 中）：Ti=TiTe_ratio*T；Te=(1.0-TiTe_ratio)*T | x |  |  |  |  |  |  |  |
| **F0** | 10. | 决定固定的环向磁场：$ B_\phi = F_0/R $ | x | x | x | x | x | x | x | x |
| **central_density** | 1. | 磁轴处的粒子密度（单位为 $10^{20} m^{-3}$） | x | x | x | x | x | x | x | x |
| **central_mass** | 2.01410177811 | 平均离子质量，单位为原子质量单位（在时间和空间上为常数，含电子质量） | x | x | x | x | x | x | x | x |
| **gamma** | 5. / 3. | 比热比（通常为 5/3） |  |  |  |  | x | x | x | x |
| **tauIC** | 0. | 抗磁项的缩放因子（见 [[diamag\|diamagnetic]]） | x | x | x | x | x | x | x | x |
| **Wdia** | .false. | 是否在黏性项中计入抗磁流？（见 [[wdia\|here]]） |  |  |  | x |  |  |  |  |
| **gamma_sheath** | 4.5 | 开放磁力线上的鞘层边界条件（JOREK 单位）；也可改用常规单位给出 gamma_stangeby！ | x | x | x | x | x | x | x | x |
| **gamma_stangeby** | -1.d99 | P. Stangeby 在（The plasma boundary of magnetic fusion devices）中给出的鞘层透射系数 |  |  |  | x | x | x | x | x |
| **gamma_sheath_e** | 3.00 | 开放磁力线上的鞘层边界条件（JOREK 单位）；也可改用常规单位给出 gamma_stangeby！ |  |  |  | x |  | x | x | x |
| **gamma_e_stangeby** | -1.d99 | P. Stangeby 在（The plasma boundary of magnetic fusion devices）中给出的鞘层透射系数 |  |  |  | x |  |  |  |  |
| **gamma_sheath_i** | -1.11d-1 | 开放磁力线上的鞘层边界条件（JOREK 单位）；也可改用常规单位给出 gamma_stangeby！ |  |  |  | x |  | x | x | x |
| **gamma_i_stangeby** | -1.d99 | P. Stangeby 在（The plasma boundary of magnetic fusion devices）中给出的鞘层透射系数 |  |  |  | x |  |  |  |  |
| **density_reflection** | 0. | 开放磁力线上的密度反射系数 | x | x | x | x |  |  |  |  |
| **neutral_reflection** | 0. | 离子反射为中性粒子的反射系数（model500） |  |  |  | x |  |  | x | x |
| **loop_voltage** | 0. | 在计算域边界施加回路电压（单位 V；仅适用于固定边界） |  |  |  | x |  |  |  |  |
| **old_deuterium_atomic** | .false. | 使用旧的拟合公式计算氘的原子系数（电离、复合、辐射），否则使用更好的拟合 |  |  |  | x |  |  |  |  |
| **deuterium_adas** | .false. | 使用 OPEN ADAS 计算氘的电离、复合与辐射系数 |  |  |  | x |  |  |  |  |
| **deuterium_adas_1e20** | .false. | 使用密度固定为 1e20 的 OPEN ADAS 计算氘的电离、复合与辐射系数 |  |  |  | x |  |  |  |  |
| **mach_one_bnd_integral** | .false. |  |  |  |  | x |  |  |  |  |
| **vpar_smoothing** | .false. | 对 B.n=0 处 Vpar 的跳变施加平滑函数 |  |  |  | x |  |  |  |  |
| **vpar_smoothing_coef** | 0.01, 0., 0. | 平行速度平滑剖面的系数 |  |  |  | x |  |  |  |  |
| **min_sheath_angle** | 1. | 对鞘层边界条件：热流与粒子流的最小入射角（单位为度） |  |  |  | x |  |  |  |  |
| **mode** |  | 与 JOREK 模式对应的环向模数，例如对于 n_period=8 和 n_tor=3，mode(:)=0,8,8 | x | x | x | x | x | x | x | x |
| **nout** | 9999999 | 每 nout 个时间步输出一个重启文件 | x | x | x | x | x | x | x | x |
| **nout_projection** | -1 | 每 nout_projection 个时间步输出一次粒子投影（仅用于诊断） |  |  |  | x | x | x | x | x |
| **xcase** | LOWER_XPOINT | 1->下 X 点。2->上 X 点。3->双零点 | x | x | x | x | x | x | x | x |
| **forceSDN** | .false. | 在 SDN_threshold 的精度范围内强制形成对称双零点 |  |  | x | x | x | x | x | x |
| **SDN_threshold** | 1.d-4 | 对称双零点网格构造的阈值，以绝对 psi 计 | x | x | x | x | x | x | x | x |
| **rst_format** | 0 | 重启文件格式：0 == 旧格式，1 == 新格式 | x | x | x | x |  |  |  |  |
| **restart** | .false. | 是否从重启文件 jorek_restart.h5 重新开始计算？ | x | x | x | x | x | x | x | x |
| **regrid** | .false. | 重新生成磁面对齐网格（目前不可用）？ | x | x | x | x | x | x | x | x |
| **regrid_from_rz** | .false. | 由 rz 平衡重新生成磁面对齐网格 | x | x | x | x | x | x | x | x |
| **xpoint** | .false. | 是否为 X 点等离子体？另见 xcase | x | x | x | x | x | x | x | x |
| **Z_xpoint_limit** | -0.4 0.4 | 将下 X 点限制在 Z < Z_xpoint_limit(1)、上 X 点限制在 Z > Z_xpoint_limit(2) 的区域中搜索 |  |  |  | x | x | x | x | x |
| **xpoint_search_tries** | 500 | 用于检查是否为含上 X 点或下 X 点的单元的候选单元数量。 |  |  | x | x | x | x | x | x |
| **bootstrap** | .false. | 是否随时间一致地演化自举电流？ | x | x | x | x |  |  |  |  |
| **bootstrap_psin_cutoff** | 0.9995 |  | x | x | x | x |  |  |  |  |
| **refinement** | .false. | 是否使用网格加密？（目前不可用） | x | x | x | x | x | x | x | x |
| **force_central_node** | .true. | 在磁面对齐网格中，强制中心处所有节点取相同值，还是各自取独立值？ | x | x | x | x | x |  |  | x |
| **fix_axis_nodes** | .false. | 固定轴上的 t 导数与交叉 st 导数以避免噪声 | x | x | x | x | x | x | x | x |
| **treat_axis** | .false. | > 用于选择网格轴处理方式的开关（见 grids/mod_axis_treatment.f90） | x | x | x | x | x | x | x | x |
| **bc_natural_flux** | .false. | 磁面边界（2 和 3）的边界条件 |  |  |  |  | x | x | x | x |
| **bc_natural_open** | .false. | 在开放磁力线上使用自然边界条件 | x | x | x | x | x | x | x | x |
| **produce_live_data** | .true. | 是否在计算过程中写出数据文件 'macroscopic_vars.dat' 以便使用 plot_live_data.sh？ | x | x | x | x | x | x | x | x |
| **grid_to_wall** | .false. | 将网格延伸到物理壁 | x | x | x | x | x | x | x | x |
| **RZ_grid_inside_wall** | .false. | 在第一壁内侧构建矩形网格 |  |  |  | x | x | x | x | x |
| **RZ_grid_jump_thres** | 0.85 | 当 RZ 网格被限制器轮廓挤压时改变 R 分辨率的阈值 |  |  |  | x | x | x | x | x |
| **manipulate_psi_map** | 0. 99. 99. 0.1 0.1 | 用于初始网格的 Psi_boundary 操控选项 | x | x | x | x | x | x | x | x |
| **adaptive_time** | .false. | （目前无用） | x | x | x | x | x | x | x | x |
| **equil** | .true. | 计算平衡 | x | x | x | x | x | x | x | x |
| **no_mach1_bc** | .false. | 从不施加 Mach-1 边界条件 |  |  |  | x | x | x | x | x |
| **Mach1_openBC** | .true. | Full-MHD：在 mod_boundary_matrix_open.f90（或 mod_boundary_conditions.f90）内部施加 Mach-1 边界条件 |  |  |  |  | x | x | x | x |
| **Mach1_fix_B** | .true. | Full-MHD：靶板上的 Mach1 边界条件使用初始磁场，即不含 AR 与 AZ 的变化 |  |  |  |  | x |  |  | x |
| **export_polar_boundary** | .false. | 即使在极向边界情形下也导出 boundary.txt 的选项。 |  |  |  | x |  |  |  |  |
| **eta_ARAZ_const** | 0. | 对 AR 与 AZ 方程使用均匀电阻率，仅在 eta_ARAZ_on=.false. 时使用 |  |  |  |  | x | x | x | x |
| **eta_ARAZ_on** | .true. | Full-MHD：开启/关闭 AR 与 AZ 方程的电阻项 |  |  |  |  | x | x | x | x |
| **eta_ARAZ_simple** | .false. | Full-MHD：在 AR 与 AZ 的电阻项中移除 Bphi 对 Fprof 的依赖（反正应由电流源补偿） |  |  |  |  | x | x | x | x |
| **tauIC_ARAZ_on** | .true. | Full-MHD：开启/关闭 AR 与 AZ 方程的抗磁项 |  |  |  |  | x | x | x | x |
| **bench_without_plot** | .false. | 若为 .true.，则不生成某些输出图（例如用于基准测试） | x | x | x | x | x | x | x | x |
| **gmres** |  | 使用迭代 GMRES 求解器 | x | x | x | x | x | x | x | x |
| **gmres_max_iter** | 200 | GMRES 迭代的最大次数 | x | x | x | x | x | x | x | x |
| **keep_n0_const** | .false. | 是否执行平衡量（i_tor=1）不随时间变化的线性运行？ |  |  | x | x | x | x | x | x |
| **linear_run** | .false. | 与 keep_n0_const 相同，即将被各模式相互独立的真正线性运行取代 |  |  | x | x | x | x | x | x |
| **export_for_nemec** | .false. | 是否为 NEMEC 程序导出平衡信息？ | x | x | x | x | x | x | x | x |
| **export_aux_node_list** | .true. | 是否在重启文件中包含用于粒子投影的 aux_node_list |  |  | x | x | x | x | x | x |
| **use_murge** | .false. | （已弃用，无法再使用） | x | x | x | x | x | x | x | x |
| **use_murge_element** | .false. | （已弃用，无法再使用） | x | x | x | x | x | x | x | x |
| **use_BLR_compression** | .false. | 在 MUMPS / PaStiX 6 求解器中使用块低秩（BLR）压缩 | x | x | x | x | x | x | x | x |
| **epsilon_BLR** | 0. | BLR 压缩的精度 | x | x | x | x | x | x | x | x |
| **just_in_time_BLR** | .true. | 对 BLR 压缩使用即时（just-in-time）策略（速度优化） | x | x | x | x | x | x | x | x |
| **write_ps** | .true. | 在运行结束时写出 postscript 文件 | x | x | x | x | x | x | x | x |
| **use_mumps** | .false. | 使用 Mumps 求解器 | x | x | x | x | x | x | x | x |
| **use_pastix** | .false. | 使用 Pastix 求解器 | x | x | x | x | x | x | x | x |
| **use_strumpack** | .true. | 使用 Strumpack 求解器 | x | x | x | x | x | x | x | x |
| **use_mumps_eq** | .false. | 使用 Mumps 平衡求解器 | x | x | x | x | x | x | x | x |
| **use_pastix_eq** | .false. | 使用 Pastix 平衡求解器 | x | x | x | x | x | x | x | x |
| **use_strumpack_eq** | .false. | 使用 Strumpack 平衡求解器 | x | x | x | x | x | x | x | x |
| **use_mumps_prj** | .true. | 使用 Mumps 投影求解器 | x | x | x | x | x | x | x | x |
| **use_pastix_prj** | .false. | 使用 Pastix 投影求解器 | x | x | x | x | x | x | x | x |
| **use_strumpack_prj** | .false. | 使用 Strumpack 投影求解器 | x | x | x | x | x | x | x | x |
| **use_wsmp** | .false. | 使用 WSMP 求解器 | x | x | x | x |  |  |  |  |
| **centralize_harm_mat** | .true. | 在环向主进程上集中谐波矩阵；STRUMPACK 求解器的开关 | x | x | x | x | x | x | x | x |
| **mumps_ordering** | 7 | MUMPS 排序选项（7:自动，3:Scotch，4:PORD，5:METIS），默认：7 | x | x | x | x | x | x | x | x |
| **pastix_maxthrd** | 1024 | pastix 求解器使用的最大线程数（改用较小的数值可能更有利） | x | x | x | x | x | x | x | x |
| **pastix_pivot** |  | 用于量级控制的 Pastix epsilon（主元阈值） | x | x | x | x |  |  |  |  |
| **use_newton** | .false. | 使用非精确 Newton 方法 |  |  | x | x | x | x | x |  |
| **maxNewton** | 20 | Newton 迭代的最大次数 |  |  | x | x | x | x | x |  |
| **gamma_Newton** | 0.5 | Newton gamma 参数：gmres_tol = gamma_Newton*(normRHScurrent/normRHSprevious)**alpha_Newton |  |  | x | x | x | x | x |  |
| **alpha_Newton** | 2. | Newton gamma 参数：gmres_tol = gamma_Newton*(normRHScurrent/normRHSprevious)**alpha_Newton |  |  | x | x | x | x | x |  |
| **strumpack_matching** | .false. | 在 STRUMPACK 求解器中执行最大对角积重排序算法（可改进直接求解器，但需使用矩阵集中化） |  |  | x | x | x | x | x | x |
| **bcs** | see [its documentation page](../howto/physics_options/boundary_conditions/choose_boundary_conditions.md) |  |  |  |  |  |  |  |  |  |
| **n_limiter** | 0 | 限制器点数量 | x | x | x | x | x | x | x | x |
| **R_limiter** | 0. | 限制器点的 R 坐标 | x | x | x | x | x | x | x | x |
| **Z_limiter** | 0. | 限制器点的 Z 坐标 | x | x | x | x | x | x | x | x |
| **first_target_point** |  |  | x | x | x | x | x | x | x | x |
| **last_target_point** |  |  | x | x | x | x | x | x | x | x |
| **gvec_grid_import** | .false. | 使用 GVEC 生成网格的傅里叶表示 | x | x | x |  |  |  |  |  |
| **extended_boundary** | .false. | 选择是否使用扩展边界条件（Biot-Savart 版本），默认（false）为使用 Dommaschk 势的 grad_chi | x |  |  |  |  |  |  |  |
| **j_cutoff_rcoord** | 99.0 | 电流在趋近边界时被置零的径向位置——rcoord 对应归一化环向磁通 | x |  |  |  |  |  |  |  |
| **j_cutoff_sig** | 0.025 | 电流朝边界逐渐降至零所经过的径向宽度 | x |  |  |  |  |  |  |  |
| **eqdsk_psi_fact** | 1. | 针对 grid_inside_wall 将 eqdsk 的 psi 乘以该因子 |  |  |  | x | x | x | x | x |
| **extend_existing_grid** | .false. | 从重启文件向已有网格添加补片 |  |  |  | x | x | x | x | x |
| **n_wall_blocks** | 0 | 块数量 |  |  |  | x | x | x | x | x |
| **corner_block** | 0 | 角块取 =1（"left"侧也将与壁对齐） |  |  |  | x | x | x | x | x |
| **n_ext_block** | 0 | 从最外磁面到壁的"径向"网格点数） |  |  |  | x | x | x | x | x |
| **n_ext_equidistant** | .false. | 若为 true，网格点的径向间距将等距（不做自适应） |  |  |  | x | x | x | x | x |
| **n_block_points_left** | 0 | 块左侧的点数 |  |  |  | x | x | x | x | x |
| **R_block_points_left** | 0. | 块左侧点的 R 坐标 |  |  |  | x | x | x | x | x |
| **Z_block_points_left** | 0. | 块左侧点的 Z 坐标 |  |  |  | x | x | x | x | x |
| **n_block_points_right** | 0 | 块左侧的点数 |  |  |  | x | x | x | x | x |
| **R_block_points_right** | 0. | 块左侧点的 R 坐标 |  |  |  | x | x | x | x | x |
| **Z_block_points_right** | 0. | 块左侧点的 Z 坐标 |  |  |  | x | x | x | x | x |
| **use_simple_bnd_types** | .false. | 将 Stan 的 bnd_types 转换为 Guido 的 bnd_types |  |  |  | x | x | x | x | x |
| **xampl** | 0. | 允许通过系数构造简单的 X 点算例（修改 Psi 边界条件） | x | x | x | x | x | x | x | x |
| **xwidth** | 0. | 允许通过系数构造简单的 X 点算例（修改 Psi 边界条件） | x | x | x | x | x | x | x | x |
| **xsig** | 1. | 允许通过系数构造简单的 X 点算例（修改 Psi 边界条件） | x | x | x | x | x | x | x | x |
| **xtheta** | 0. | 允许通过系数构造简单的 X 点算例（修改 Psi 边界条件） | x | x | x | x | x | x | x | x |
| **xshift** | 0. | 允许通过系数构造简单的 X 点算例（修改 Psi 边界条件） | x | x | x | x | x | x | x | x |
| **xleft** | 0. | 允许通过系数构造简单的 X 点算例（修改 Psi 边界条件） | x | x | x | x | x | x | x | x |
| **particlesource** | 1.e-5 | 粒子源幅度 | x | x | x | x | x | x | x | x |
| **particlesource_psin** | 1.0 | 源逐渐减弱的中心位置 | x | x | x | x | x | x | x | x |
| **particlesource_sig** | 0.1 | 源逐渐减弱的宽度 | x | x | x | x | x | x | x | x |
| **particlesource_gauss** | 0. | 附加高斯粒子源幅度 | x | x | x | x | x | x | x | x |
| **particlesource_gauss_psin** | 0.9 | 高斯源设定的中心位置 | x | x | x | x | x | x | x | x |
| **particlesource_gauss_sig** | 0.1 | 高斯源设定的宽度 | x | x | x | x | x | x | x | x |
| **edgeparticlesource** | 0. | 边缘粒子源幅度 | x | x | x | x | x | x | x | x |
| **edgeparticlesource_psin** | 0.98 | 边缘粒子源所在的中心位置 | x | x | x | x | x | x | x | x |
| **edgeparticlesource_sig** | 0.01 | 边缘粒子源延伸的宽度 | x | x | x | x | x | x | x | x |
| **neutral_line_source** | 0. | 中性粒子入流源 |  |  |  | x |  |  | x | x |
| **neutral_line_R_start** | 1.d20 | 中性粒子入流源（线源的起点） |  |  |  | x |  |  | x | x |
| **neutral_line_Z_start** | 1.d20 | 中性粒子入流源 |  |  |  | x |  |  | x | x |
| **neutral_line_R_end** | 2.d20 | 中性粒子入流源（线源的终点） |  |  |  | x |  |  | x | x |
| **neutral_line_Z_end** | 2.d20 | 中性粒子入流源 |  |  |  | x |  |  | x | x |
| **heatsource** | 1.e-7 | 热源幅度 | x | x | x | x | x | x | x | x |
| **heatsource_e** | 0.5e-7 | 电子热源幅度 | x | x |  | x |  | x | x | x |
| **heatsource_i** | 0.5e-7 | 离子热源幅度 | x | x |  | x |  | x | x | x |
| **heatsource_psin** | 1.0 | 源逐渐减弱的中心位置 | x | x | x | x | x | x | x | x |
| **heatsource_sig** | 0.1 | 源逐渐减弱的宽度 | x | x | x | x | x | x | x | x |
| **heatsource_e_psin** | 1.0 | 电子源逐渐减弱的中心位置 | x |  |  | x |  |  |  |  |
| **heatsource_e_sig** | 0.1 | 电子源逐渐减弱的宽度 | x |  |  | x |  |  |  |  |
| **heatsource_i_psin** | 1.0 | 离子源逐渐减弱的中心位置 | x |  |  | x |  |  |  |  |
| **heatsource_i_sig** | 0.1 | 离子源逐渐减弱的宽度 | x |  |  | x |  |  |  |  |
| **heatsource_gauss** | 0. | 附加高斯热源幅度 | x | x | x | x | x | x | x | x |
| **heatsource_gauss_psin** | 0.9 | 高斯源所在的中心位置 | x | x | x | x | x | x | x | x |
| **heatsource_gauss_sig** | 0.1 | 高斯源延伸的宽度 | x | x | x | x | x | x | x | x |
| **heatsource_gauss_e** | 0. | 电子高斯热源 | x | x |  | x |  | x | x | x |
| **heatsource_gauss_i** | 0. | 离子高斯热源 | x | x |  | x |  | x | x | x |
| **heatsource_gauss_e_psin** | 0.9 | 电子高斯源所在的中心位置 | x | x |  | x |  |  |  |  |
| **heatsource_gauss_e_sig** | 0.1 | 电子高斯源延伸的宽度 | x | x |  | x |  |  |  |  |
| **heatsource_gauss_i_psin** | 0.9 | 离子高斯源所在的中心位置 | x | x |  | x |  |  |  |  |
| **heatsource_gauss_i_sig** | 0.1 | 离子高斯源延伸的宽度 | x | x |  | x |  |  |  |  |
| **constant_imp_source** | 0. | 添加一个恒定杂质源 |  |  |  | x |  |  |  |  |
| **eta_num** | 0. |  | x | x | x | x | x | x | x | x |
| **visco_num** | 0. |  | x | x | x | x | x | x | x | x |
| **visco_par_num** | 0. |  | x | x | x | x | x | x | x | x |
| **Dn_perp_num** | 0. |  |  |  |  | x |  |  | x | x |
| **maintain_profiles** | .false. | 添加人工源以维持初始的 rho 与 T 剖面 |  | x |  |  |  |  |  |  |
| **use_sc** | .false. | 使用激波捕捉稳定化 |  |  |  | x |  |  |  | x |
| **D_perp_sc_num** | 0. |  |  |  |  | x |  |  |  | x |
| **D_par_sc_num** | 0. |  |  |  |  | x |  |  |  | x |
| **Dn_pol_sc_num** | 0. |  |  |  |  | x |  |  |  | x |
| **Dn_p_sc_num** | 0. |  |  |  |  | x |  |  |  | x |
| **D_perp_imp_sc_num** | 0. |  |  |  |  | x |  |  |  | x |
| **D_par_imp_sc_num** | 0. |  |  |  |  | x |  |  |  | x |
| **ZK_perp_sc_num** | 0. |  |  |  |  | x |  |  |  | x |
| **ZK_par_sc_num** | 0. |  |  |  |  | x |  |  |  | x |
| **ZK_i_perp_sc_num** | 0. |  |  |  |  | x |  |  |  | x |
| **ZK_i_par_sc_num** | 0. |  |  |  |  | x |  |  |  | x |
| **ZK_e_perp_sc_num** | 0. |  |  |  |  | x |  |  |  | x |
| **ZK_e_par_sc_num** | 0. |  |  |  |  | x |  |  |  | x |
| **visco_sc_num** | 0. |  |  |  |  | x |  |  |  | x |
| **visco_par_sc_num** | 0. |  |  |  |  | x |  |  |  | x |
| **eta_num_T_dependent** | .false. | 超电阻率是否依赖温度？否则为常数。 |  |  |  | x |  |  |  |  |
| **eta_num_psin_dependent** | .false. | 是否将超电阻率给出为 \psi_N 的函数剖面？可用于二维电流展平 |  |  |  | x |  |  |  |  |
| **eta_num_prof** | 0. 0.8 0.03 | 用于指定超电阻率 \psi_N 剖面的系数 |  |  |  | x |  |  |  |  |
| **visco_num_T_dependent** | .false. |  |  |  |  | x |  |  |  |  |
| **add_sources_in_sc** | .false. | 是否在激波捕捉稳定化中计入源项效应 |  |  |  | x |  |  |  | x |
| **use_vms** | .false. | 仅在模型 750 中使用 VMS 稳定化 |  |  |  |  |  |  |  | x |
| **vms_coeff_AR** | 0. |  |  |  |  |  |  |  |  | x |
| **vms_coeff_AZ** | 0. |  |  |  |  |  |  |  |  | x |
| **vms_coeff_A3** | 0. |  |  |  |  |  |  |  |  | x |
| **vms_coeff_UR** | 0. |  |  |  |  |  |  |  |  | x |
| **vms_coeff_UZ** | 0. |  |  |  |  |  |  |  |  | x |
| **vms_coeff_Up** | 0. |  |  |  |  |  |  |  |  | x |
| **vms_coeff_T** | 0. |  |  |  |  |  |  |  |  | x |
| **vms_coeff_Te** | 0. |  |  |  |  |  |  |  |  | x |
| **vms_coeff_Ti** | 0. |  |  |  |  |  |  |  |  | x |
| **vms_coeff_rho** | 0. |  |  |  |  |  |  |  |  | x |
| **vms_coeff_rhon** | 0. |  |  |  |  |  |  |  |  | x |
| **vms_coeff_rhoimp** | 0. |  |  |  |  |  |  |  |  | x |
| **tstep** | 1. | 时间步长（$ \Delta t $） | x | x | x | x | x | x | x | x |
| **tstep_n** | 1. | tstep 的替代方式：最多可给出十个数值 | x | x | x | x | x | x | x | x |
| **nstep** | 0 | 要执行的时间步数 | x | x | x | x | x | x | x | x |
| **nstep_n** | 0 | nstep 的替代方式：最多可给出十个数值 | x | x | x | x | x | x | x | x |
| **time_evol_scheme** | 'Crank-Nicholson' | 采用的时间演化格式（见 [[time-integration\|time_integration]]） | x | x | x | x | x | x | x | x |
| **time_evol_theta** |  | 时间演化参数 theta（见 [[time-integration\|time_integration]]） |  |  |  |  | x | x | x | x |
| **time_evol_zeta** |  | 时间演化参数 zeta（见 [[time-integration\|time_integration]]） |  |  |  |  | x | x | x | x |
| **rst_hdf5** | 1 | 若设为 1 则写出 hdf5 重启文件 | x | x | x | x | x | x | x | x |
| **rst_hdf5_version** |  | 写出哪一版本的 hdf5 文件？ | x | x | x | x | x | x | x | x |
| **tokamak_device** | 'none' | 所模拟的托卡马克装置名称 | x | x | x | x | x | x | x | x |
| **amin** | 1. | 极向网格构造用的小半径；若边界以 R,Z 点给出则设为 1 | x | x | x | x | x | x | x | x |
| **ellip** | 1. | 极向网格的椭圆度（解析定义见 phys_module.f90） | x | x | x | x | x | x | x | x |
| **tria_u** | 0. | 极向网格的上三角形度（解析定义见 phys_module.f90） | x | x | x | x | x | x | x | x |
| **tria_l** | 0. | 极向网格的下三角形度（解析定义见 phys_module.f90） | x | x | x | x | x | x | x | x |
| **quad_u** | 0. | 极向网格的上四边形度（解析定义见 phys_module.f90） | x | x | x | x | x | x | x | x |
| **quad_l** | 0. | 极向网格的下四边形度（解析定义见 phys_module.f90） | x | x | x | x | x | x | x | x |
| **mf** | 2 | fbnd 与 fpsi 中的条目数 | x | x | x | x | x | x | x | x |
| **fbnd** | 0.;   fbnd(1)  = 2. | 边界的傅里叶展开 | x | x | x | x | x | x | x | x |
| **fpsi** |  | 边界处极向磁通的傅里叶展开 | x | x | x | x | x | x | x | x |
| **n_boundary** | 0 | R_boundary、Z_boundary、psi_boundary 中的点数。 | x | x | x | x | x | x | x | x |
| **R_boundary** | 0. | 定义边界的 R 数值 | x | x | x | x | x | x | x | x |
| **Z_boundary** | 0. | 定义边界的 Z 数值 | x | x | x | x | x | x | x | x |
| **psi_boundary** | 0. | 给出边界处极向磁通的数值 | x | x | x | x | x | x | x | x |
| **n_pfc** | 0 | 线圈数量，（MAST 用的旧功能……）线圈请改用 JOREK-STARWALL [[jorek-starwall\|JOREK-STARWALL]] | x | x | x | x |  |  |  |  |
| **Rmin_pfc** | 0. | 线圈的最小 R，（MAST 用的旧功能……）线圈请改用 JOREK-STARWALL [[jorek-starwall\|JOREK-STARWALL]] | x | x | x | x |  |  |  |  |
| **Rmax_pfc** | 0. | 线圈的最大 R，（MAST 用的旧功能……）线圈请改用 JOREK-STARWALL [[jorek-starwall\|JOREK-STARWALL]] | x | x | x | x |  |  |  |  |
| **Zmin_pfc** | 0. | 线圈的最小 Z，（MAST 用的旧功能……）线圈请改用 JOREK-STARWALL [[jorek-starwall\|JOREK-STARWALL]] | x | x | x | x |  |  |  |  |
| **Zmax_pfc** | 0. | 线圈的最大 Z，（MAST 用的旧功能……）线圈请改用 JOREK-STARWALL [[jorek-starwall\|JOREK-STARWALL]] | x | x | x | x |  |  |  |  |
| **current_pfc** | 0. | 线圈中的电流密度，（MAST 用的旧功能……）线圈请改用 JOREK-STARWALL [[jorek-starwall\|JOREK-STARWALL]] | x | x | x | x |  |  |  |  |
| **n_jropes** | 0 | 电流绳的数量， |  |  |  | x |  |  |  |  |
| **R_jropes** | 0. | 电流绳中心的 R 坐标 |  |  |  | x |  |  |  |  |
| **Z_jropes** | 0. | 电流绳中心的 Z 坐标 |  |  |  | x |  |  |  |  |
| **w_jropes** | 0. | 电流绳的宽度 |  |  |  | x |  |  |  |  |
| **current_jropes** | 0. | 电流绳内的电流 |  |  |  | x |  |  |  |  |
| **pellet_amplitude** | 0. | 密度源幅度（当弹丸被建模为密度源时） | x | x | x | x | x | x | x | x |
| **pellet_R** | 3.8 | 弹丸的大半径位置 | x | x | x | x | x | x | x | x |
| **pellet_Z** | 0.0 | 弹丸的 Z 位置 | x | x | x | x | x | x | x | x |
| **pellet_phi** | 1.57 | 弹丸云（密度源）在环向角上的宽度 | x | x | x | x | x | x | x | x |
| **pellet_ellipse** | 5. | 弹丸源的椭率 | x | x | x | x |  |  |  |  |
| **pellet_radius** | 0.08 | 模拟弹丸的半径 | x | x | x | x | x | x | x | x |
| **pellet_sig** | 0.02 | 密度源平滑的宽度（arctan( (r-pellet_radius)/pellet_sig) ） | x | x | x | x | x | x | x | x |
| **pellet_length** | 0.785 | 密度源在环向角上的平滑宽度 | x | x | x | x | x | x | x | x |
| **pellet_theta** | 0. | 弹丸椭圆的取向 | x | x | x | x |  |  |  |  |
| **pellet_psi** | 1.0 | 弹丸在极向磁通中的宽度 | x | x | x | x | x | x | x | x |
| **pellet_delta_psi** | 999. | 极向磁通中平滑的宽度 | x | x | x | x | x | x | x | x |
| **pellet_velocity_R** | 0. | 弹丸速度的径向分量 | x | x | x | x |  |  |  |  |
| **pellet_velocity_Z** | 0. | 弹丸速度的 Z 方向分量 | x | x | x | x |  |  |  |  |
| **pellet_density** | 5.985d8 | 弹丸原子数密度（单位为 $10^{20} m^{-3}$） | x | x | x | x |  |  |  | x |
| **pellet_density_bg** | 5.958d8 | 背景粒子种的弹丸原子数密度（单位为 $10^{20} m^{-3}$） |  |  |  | x |  |  |  | x |
| **pellet_particles** | 0. | 弹丸中的粒子数（以 $10^{20}$ 为单位） | x | x | x | x |  |  | x | x |
| **use_pellet** | .false. |  | x | x | x | x |  |  | x | x |
| **t_ns** | 2.d3 | MGI 起始时间（JOREK 单位） |  |  |  | x |  |  | x | x |
| **ns_amplitude** | 0. | 气体源幅度 |  |  |  | x |  |  | x | x |
| **ns_R** | 3.2 | 气体源的 R 位置 |  |  |  | x |  |  | x | x |
| **ns_Z** | 1.5 | 气体源的 Z 位置 |  |  |  | x |  |  | x | x |
| **ns_phi** | 1.57 | 气体源的 Phi 位置 |  |  |  | x |  |  | x | x |
| **ns_radius** | 0.08 | 气体源的极向半径 |  |  |  | x |  |  | x | x |
| **ns_deltaphi** | 0.5 | 气体源的环向延伸 |  |  |  | x |  |  | x | x |
| **ns_delta_minor_rad** | 0. | 气体源在小半径方向上的延伸（若大于 0.） |  |  |  | x |  |  | x | x |
| **drift_distance** | 0. | 为模拟等离子体团漂移，将中性粒子沉积的 R 位置向外平移 drift_distance（单位 m） |  |  |  | x |  |  | x | x |
| **energy_teleported** | 0. | 为计入等离子体团漂移效应而每个原子迁移的能量（单位 eV） |  |  |  | x |  |  | x | x |
| **imp_type** | ' ' | 注入材料或背景杂质种的类型：Argon、neon、…… |  |  |  | x |  |  |  | x |
| **use_imp_adas** | .true. | 使用 open adas 计算杂质的电离、复合与辐射系数 |  |  |  | x |  |  |  |  |
| **JET_MGI** | .false. | 切换到类似 JET 的 MGI |  |  |  | x |  |  | x | x |
| **ASDEX_MGI** | .false. | 切换到类似 ASDEX 的 MGI |  |  |  | x |  |  | x | x |
| **V_Dmv** | 9.75d-4 | DMV 储气罐的体积 |  |  |  | x |  |  | x | x |
| **P_Dmv** |  | DMV 储气罐中的压强（bar） |  |  |  | x |  |  | x | x |
| **A_Dmv** | 1.77d-2 | DMV（破裂缓解阀）管道的横截面积 |  |  |  | x |  |  | x | x |
| **K_Dmv** | 4.d-2 | 描述管口附近气体膨胀的修正参数 |  |  |  | x |  |  | x | x |
| **L_tube** | 0. | 管道长度 |  |  |  | x |  |  | x | x |
| **ksi_ion** | 1.84d-24 | 每次电离的能量代价，ksi_ion / mu_0 / (gamma-1) / e = 13.7 eV |  |  |  | x |  |  | x | x |
| **delta_n_convection** | 0 | 激活中性粒子对流项（以等离子体速度）的开关 |  |  |  | x |  |  | x | x |
| **nimp_bg** | 0. | 背景杂质密度（单位 $m^{-3}$） |  |  |  | x |  |  | x | x |
| **index_main_imp** | 0 | 用连续性方程求解的主杂质种（位于 imp_type 与 nimp_bg 中）的索引 |  |  |  | x |  |  |  | x |
| **using_spi** | .false. | 决定使用 SPI 还是传统 MGI；见 [[spi_tutorial\|SPI Tutorial]] |  |  |  | x |  |  | x | x |
| **spi_Vel_Rref** | 0.0 | 注入时弹丸中心沿 R 方向的参考速度 |  |  |  | x |  |  | x | x |
| **spi_Vel_Zref** | 0.0 | 注入时弹丸中心沿 Z 方向的参考速度 |  |  |  | x |  |  | x | x |
| **spi_Vel_RxZref** | 0.0 | 注入时弹丸中心沿 RxZ 方向的参考速度 |  |  |  | x |  |  | x | x |
| **spi_quantity** | 0.0 | 杂质 SPI 注入的原子总数 |  |  |  | x |  |  | x | x |
| **spi_quantity_bg** | 0.0 | 背景粒子种 SPI 注入的原子总数 |  |  |  | x |  |  |  | x |
| **ns_radius_ratio** | 1.4 | 假定各 NG 云半径之间保持恒定比值 |  |  |  | x |  |  | x | x |
| **spi_Vel_diff** | 0.0 | 相对参考速度的速度差 |  |  |  | x |  |  | x | x |
| **spi_angle** | 0.0 | SPI 扩散的顶角，以 rad 计 |  |  |  | x |  |  | x | x |
| **spi_L_inj** | 0.25 | SPI 喷嘴与 ns_R、ns_Z、ns_phi 之间的距离 |  |  |  | x |  |  | x | x |
| **spi_L_inj_diff** | 0.0 | 相对点 (ns_R, ns_Z, ns_phi) 的位置差 |  |  |  | x |  |  | x | x |
| **tor_frequency** | 0.0 | 刚体旋转频率 |  |  |  | x |  |  | x | x |
| **ns_radius_min** | 8.d-2 | 出于数值原因定义中性粒子云的最小半径（单位 m） |  |  |  | x |  |  | x | x |
| **spi_abl_history_old** | .false. | 若为 .t.，重启时将旧的 spi_abl_history 格式转换为新格式。 |  |  |  | x |  |  |  |  |
| **n_spi** | 0 1 | 每次注入的碎裂碎片数量 |  |  |  | x |  |  | x | x |
| **n_inj** | 1 | 注入次数 |  |  |  | x |  |  | x | x |
| **spi_abl_model** | -1 | 决定采用哪种烧蚀模型。 |  |  |  | x |  |  | x | x |
| **spi_rnd_seed** | 0 | 用于生成 SPI 速度散布的随机种子数组 |  |  |  | x |  |  | x | x |
| **spi_shard_file** | 'none' | 碎片尺寸文件的名称 |  |  |  | x |  |  |  | x |
| **spi_plume_file** | 'none' | 碎片信息数据文件（数组）的名称 |  |  |  | x |  |  |  | x |
| **spi_plume_hdf5** | .false. | 'spi_plume_file' 是否为 HDF5 格式？ |  |  |  | x |  |  |  |  |
| **spi_abl_mag_reduction** | .false. | 是否使用 Nucl. Fusion 60 066027 中公式 (27) 所述的磁致减弱效应 |  |  |  | x |  |  |  |  |
| **n_adas** | 1 | 由 ADAS 追踪的粒子种数量 |  |  |  | x |  |  |  | x |
| **spi_tor_rot** | .false. | 为 SPI 开启刚体环向等离子体旋转的开关 |  |  |  | x |  |  | x | x |
| **spi_num_vol** | .true. | 开启对 SPI 气体源体积进行数值积分的开关 |  |  |  | x |  |  | x | x |
| **adas_dir** | ' ' | 要读取的 ADAS 数据文件所在目录 |  |  |  | x |  |  |  | x |
| **output_prad_phi** | .false. | 使用 integrals_3D 将 Prad(phi) 输出到文件 |  |  |  | x |  |  |  | x |
| **amix** | 0. | 以给定的因子将 Poisson 解与前一次解混合 | x | x | x | x | x | x | x | x |
| **equil_accuracy** | 1.d-6 | 固定边界平衡收敛的容差 | x | x | x | x | x | x | x | x |
| **axis_srch_radius** | 99. | 磁轴将在具有该半径的圆内搜索 | x | x | x | x | x | x | x | x |
| **delta_psi_GS** | 10000. | 最终平衡预期的 psi_bnd - psi_axis |  |  | x | x | x | x | x | x |
| **newton_GS_fixbnd** | .false. | 固定边界平衡是否用 Newton 迭代代替 Picard 迭代？ |  |  | x | x | x | x | x | x |
| **newton_GS_freebnd** | .true. | 自由边界平衡是否用 Newton 迭代代替 Picard 迭代？ |  |  | x | x | x | x | x | x |
| **freeboundary_equil** | .false. | 使用自由边界还是固定边界平衡？（[[jorek-starwall\|JOREK-STARWALL]]） | x | x | x | x | x | x | x | x |
| **freeboundary** | .false. | 时间演化中使用自由边界还是固定边界条件？（[[jorek-starwall\|JOREK-STARWALL]]） | x | x | x | x | x | x | x | x |
| **resistive_wall** | .false. | 使用电阻壁还是理想壁？（[[jorek-starwall\|JOREK-STARWALL]]） | x | x | x | x | x | x | x | x |
| **freeb_equil_iterate_area** | .false. | 在自由边界平衡限制器算例中迭代至目标面积 [[jorek-starwall-faqs\|jorek_starwall]] | x | x | x | x | x | x | x | x |
| **amix_freeb** | 0.85 | 为自由边界平衡选择 amix | x | x | x | x | x | x | x | x |
| **equil_accuracy_freeb** | 1.d-6 | 自由边界平衡收敛的容差 | x | x | x | x | x | x | x | x |
| **freeb_change_indices** | .true. | 交换网格节点索引以并行化边界积分 | x | x | x | x | x | x | x | x |
| **n_R** | 0 | R 方向网格点数（用于矩形网格）（另见 [[grids#tutorials\|here]]） | x | x | x | x | x | x | x | x |
| **n_Z** | 0 | Z 方向网格点数（用于矩形网格） | x | x | x | x | x | x | x | x |
| **R_begin** | -0.1 | 网格在 R 方向的左边界（用于矩形网格） | x | x | x | x | x | x | x | x |
| **R_end** | 0.1 | 网格在 R 方向的右边界（用于矩形网格） | x | x | x | x | x | x | x | x |
| **Z_begin** | -0.1 | 网格在 Z 方向的下边界（用于矩形网格） | x | x | x | x | x | x | x | x |
| **Z_end** | 0.1 | 网格在 Z 方向的上边界（用于矩形网格） | x | x | x | x | x | x | x | x |
| **rect_grid_vac_psi** | 0. | 对矩形网格使用真空 psi 边界条件，即 (rect_grid_vac_psi * R**2) |  |  |  | x |  |  |  |  |
| **force_horizontal_Xline** | .false. | 强制穿过 X 点的网格线保持水平（而非垂直于 X 点与磁轴连线） | x | x | x | x | x | x | x | x |
| **n_radial** | 11 | 径向网格点数（用于极向网格）（另见 [[grids\|here]]） | x | x | x | x | x | x | x | x |
| **n_pol** | 16 | 极向网格点数（用于极向网格） | x | x | x | x | x | x | x | x |
| **R_geo** | 10. | 网格中心（用于极向网格） | x | x | x | x | x | x | x | x |
| **Z_geo** | 0. | 网格中心（用于极向网格） | x | x | x | x | x | x | x | x |
| **psi_axis_init** | -0.1 | 磁轴处 Psi 的初始猜测（用于极向网格） | x | x | x | x | x | x | x | x |
| **XR_r** | 999. | 径向网格聚集的 Psi_N 位置（两个位置）（用于极向网格）（也用作矩形网格中的 R 位置） | x | x | x | x | x | x | x | x |
| **SIG_r** | 999. | 网格聚集的宽度（两个位置）（用于极向网格）（也用作矩形网格中的 R 宽度） | x | x | x | x | x | x | x | x |
| **XR_tht** | 999. | 极向网格聚集的位置（0...1，两个位置）（用于极向网格） | x | x | x | x | x | x | x | x |
| **SIG_tht** | 999. | 网格聚集的宽度（两个位置）（用于极向网格） | x | x | x | x | x | x | x | x |
| **XR_z** | 999. | 矩形网格聚集的 Z 位置（两个位置）（用于矩形网格） |  |  |  | x |  |  |  |  |
| **SIG_z** | 999. | 网格聚集的 Z 宽度（两个位置）（用于矩形网格） |  |  |  | x |  |  |  |  |
| **bgf_r** | 0.7 |  |  |  |  | x |  |  |  |  |
| **bgf_z** | 0.7 | R-Z 聚集的 meshac 分布背景 |  |  |  | x |  |  |  |  |
| **bgf_rpolar** | 0.6 |  |  |  | x | x | x | x | x | x |
| **bgf_tht** | 0.6 | R-theta 聚集的 meshac 分布背景 |  |  | x | x | x | x | x | x |
| **n_flux** | 11 | 径向网格点数（用于磁面对齐网格）（另见 [[grids#tutorials\|here]]） | x | x | x | x | x | x | x | x |
| **n_tht** | 16 | 极向网格点数（用于磁面对齐网格） | x | x | x | x | x | x | x | x |
| **xr1** | 9999. | 网格聚集参数（用于磁面对齐网格） | x | x | x | x | x | x | x | x |
| **xr2** | 99999. | 网格聚集参数（用于磁面对齐网格） | x | x | x | x | x | x | x | x |
| **sig1** | 9999. | 网格聚集参数（用于磁面对齐网格） | x | x | x | x | x | x | x | x |
| **sig2** | 99999. | 网格聚集参数（用于磁面对齐网格） | x | x | x | x | x | x | x | x |
| **m_pol_bc** | 1 | 仿星器中用于 Psi 边界条件的极向模数 | x |  |  |  |  |  |  |  |
| **i_plane_rtree** | 1 | 仿星器中构建 RTree 所在的极向平面（RZ_minmax 指该平面） | x | x |  |  |  |  |  |  |
| **n_open** | 5 | 开放磁通区（若为双零点，则位于两条分界面之间）的"径向"网格点数 | x | x | x | x | x | x | x | x |
| **n_outer** | 0 | 若为双零点，外侧（LFS）开放磁通区的"径向"网格点数 | x | x | x | x | x | x | x | x |
| **n_inner** | 0 | 若为双零点，内侧（HFS）开放磁通区的"径向"网格点数 | x | x | x | x | x | x | x | x |
| **n_private** | 5 | 底部私有磁通区的"径向"网格点数 | x | x | x | x | x | x | x | x |
| **n_leg** | 5 | 底部沿偏滤器腿的"极向"网格点数 | x | x | x | x | x | x | x | x |
| **n_leg_out** | 0 | 底部 LFS 侧沿偏滤器腿的"极向"网格点数 |  |  |  | x | x | x | x | x |
| **n_up_priv** | 0 | 顶部（上 X 点或双零点）私有磁通区的"径向"网格点数 | x | x | x | x | x | x | x | x |
| **n_up_leg** | 0 | 顶部（上 X 点或双零点）沿偏滤器腿的"极向"网格点数 | x | x | x | x | x | x | x | x |
| **n_up_leg_out** | 0 | 顶部 LFS 侧沿偏滤器腿的"极向"网格点数（上 X 点或双零点） |  |  |  | x | x | x | x | x |
| **n_ext** | 0 | 从最外磁面到壁的"径向"网格点数） | x | x | x | x | x | x | x | x |
| **n_tht_equidistant** | .false. | 开启后在网格芯部（psi<0.5）得到等距的极向单元分布 |  |  |  | x | x | x | x | x |
| **xr_closed** | 1.0, 9999., 9999. | 网格聚集的位置（用于磁面对齐网格） | x | x | x | x | x | x | x | x |
| **SIG_closed** | 0.1, 9999., 0.1 | 网格聚集的宽度（用于磁面对齐网格） | x | x | x | x | x | x | x | x |
| **SIG_open** | 0.1 | 网格聚集的宽度（用于磁面对齐网格） | x | x | x | x | x | x | x | x |
| **SIG_outer** | 0.1 | 网格聚集的宽度（用于磁面对齐网格） | x | x | x | x | x | x | x | x |
| **SIG_inner** | 0.1 | 网格聚集的宽度（用于磁面对齐网格） | x | x | x | x | x | x | x | x |
| **SIG_private** | 0.1 | 网格聚集的宽度（用于磁面对齐网格） | x | x | x | x | x | x | x | x |
| **SIG_up_priv** | 0.1 | 网格聚集的宽度（用于磁面对齐网格） | x | x | x | x | x | x | x | x |
| **SIG_theta** | 0.03 | 网格聚集的宽度（用于磁面对齐网格） | x | x | x | x | x | x | x | x |
| **SIG_theta_up** | 999. | 网格聚集的宽度（用于磁面对齐网格；仅对双零点有效） |  |  | x | x | x | x | x | x |
| **SIG_leg_0** | 0.05 | 网格聚集的宽度（用于磁面对齐网格） | x | x | x | x | x | x | x | x |
| **SIG_leg_1** | 0.2 | 网格聚集的宽度（用于磁面对齐网格） | x | x | x | x | x | x | x | x |
| **SIG_up_leg_0** | 0.05 | 网格聚集的宽度（用于磁面对齐网格） | x | x | x | x | x | x | x | x |
| **SIG_up_leg_1** | 0.2 | 网格聚集的宽度（用于磁面对齐网格） | x | x | x | x | x | x | x | x |
| **dPSI_open** | 0.11 | 网格延伸进入开放磁通区的 Delta Psi（用于磁面对齐网格） | x | x | x | x | x | x | x | x |
| **dPSI_outer** | 0.11 | 网格延伸进入开放磁通区的 Delta Psi（用于磁面对齐网格） | x | x | x | x | x | x | x | x |
| **dPSI_inner** | 0.11 | 网格延伸进入开放磁通区的 Delta Psi（用于磁面对齐网格） | x | x | x | x | x | x | x | x |
| **dPSI_private** | 0.03 | 网格延伸进入私有磁通区的 Delta Psi（用于磁面对齐网格） | x | x | x | x | x | x | x | x |
| **dPSI_up_priv** | 0.03 | 网格延伸进入私有磁通区的 Delta Psi（用于磁面对齐网格） | x | x | x | x | x | x | x | x |
| **D_perp** | 1.d-5, 0., 0., 99., 99. | 垂直粒子扩散剖面的系数 | x | x | x | x | x | x | x | x |
| **D_par** | 0. | 平行粒子扩散（通常无用） | x | x | x | x | x | x | x | x |
| **V_pinch_gauss** | 0. | 背景流体（仅 rho）高斯向内收缩速度剖面的幅度。 |  |  |  | x |  |  |  |  |
| **V_pinch_psin** | 0. | V_pinch 高斯在归一化极向磁通（psin）中的中心。 |  |  |  | x |  |  |  |  |
| **V_pinch_sig** | 1. | V_pinch 高斯在 psin 单位下的宽度（sigma）。 |  |  |  | x |  |  |  |  |
| **D_perp_imp** | 1.d-5, 0., 0., 99., 99. | 垂直杂质粒子扩散剖面的系数 |  |  |  | x |  |  |  | x |
| **D_par_imp** | 0. | 平行杂质粒子扩散（通常无用） |  |  |  | x |  |  |  | x |
| **ZK_perp** | 1.d-5, 0., 0., 99., 99. | 垂直热扩散剖面的系数 | x | x | x | x | x | x | x | x |
| **ZK_par** | 1. | 等离子体中心处的平行热扩散值 | x | x | x | x | x | x | x | x |
| **ZK_par_max** | 1.d20 | 出于数值原因不使用更大的平行热扩散值 | x | x | x | x | x | x | x | x |
| **T_min_ZKpar** | -1.d12 | 低于该 MHD 温度（Ti+Te）时不使用更小的平行热扩散值；JOREK 单位 |  |  |  | x |  |  |  |  |
| **Ti_min_ZKpar** | -1.d12 | 低于 Ti 时不使用更小的平行热扩散值；JOREK 单位 |  |  |  | x |  |  |  |  |
| **Te_min_ZKpar** | -1.d12 | 低于 Te 时不使用更小的平行热扩散值；JOREK 单位 |  |  |  | x |  |  |  |  |
| **ZK_i_perp** | 1.d-5, 0., 0., 99., 99. | 垂直离子热扩散剖面的系数 |  | x |  | x |  | x | x | x |
| **ZK_e_perp** | 1.d-5, 0., 0., 99., 99. | 垂直电子热扩散剖面的系数 |  | x |  | x |  | x | x | x |
| **ZK_i_par** | 1. | 等离子体中心处的离子平行热扩散系数 |  | x |  | x |  | x | x | x |
| **ZK_e_par** | 1. | 等离子体中心处的电子平行热扩散系数 |  | x |  | x |  | x | x | x |
| **D_neutral_x** | 1.d-5 | 中性粒子在 R 方向的扩散系数 |  |  |  | x |  |  | x | x |
| **D_neutral_y** | 1.d-5 | 中性粒子在 Z 方向的扩散系数 |  |  |  | x |  |  | x | x |
| **D_neutral_p** | 1.d-5 | 中性粒子在 phi 方向的扩散系数 |  |  |  | x |  |  | x | x |
| **ZKpar_T_dependent** | .true. | 使用依赖温度的平行热扩散系数 | x | x | x | x | x | x | x | x |
| **d_perp_file** | 'none' | 含垂直粒子扩散剖面的 ASCII 文件 | x | x | x | x |  |  |  |  |
| **zk_perp_file** | 'none' | 含垂直热扩散剖面的 ASCII 文件 | x | x | x | x |  |  |  |  |
| **zk_e_perp_file** | 'none' | 含垂直电子热扩散剖面的 ASCII 文件 |  |  |  | x |  |  |  |  |
| **zk_i_perp_file** | 'none' | 含垂直离子热扩散剖面的 ASCII 文件 |  |  |  | x |  |  |  |  |
| **v_pinch_file** | 'none' | 含向内收缩速度剖面的 ASCII 文件（psin、V_pinch 列） |  |  |  | x |  |  |  |  |
| **rho_0** | 1. | 中心归一化密度（通常为 1） | x | x | x | x | x | x | x | x |
| **rho_1** | 1. | SOL 归一化密度 | x | x | x | x | x | x | x | x |
| **rho_coef** | 0.;  rho_coef(1) =  0. | 密度剖面系数 | x | x | x | x | x | x | x | x |
| **rho_file** | 'none' | 读取密度剖面所用的 ASCII 文件。 | x | x | x | x | x | x | x | x |
| **T_0** | 1.d-6 | 中心归一化温度 | x | x | x | x | x | x | x | x |
| **T_1** | 1.d-8 | SOL 归一化温度 | x | x | x | x | x | x | x | x |
| **T_coef** | 0.;  T_coef(1)   = -1. | 温度剖面系数 | x | x | x | x | x | x | x | x |
| **Ti_0** | 5.d-7 | 中心离子归一化温度 | x | x |  | x |  | x | x | x |
| **Ti_1** | 5.d-9 | SOL 离子归一化温度 | x | x |  | x |  | x | x | x |
| **Ti_coef** | 0.;  Ti_coef(1)  = -1. | 离子温度剖面系数 | x | x |  | x |  | x | x | x |
| **Te_0** | 5.d-7 | 中心离子归一化温度 | x | x |  | x |  | x | x | x |
| **Te_1** | 5.d-9 | SOL 离子归一化温度 | x | x |  | x |  | x | x | x |
| **Te_coef** | 0.;  Te_coef(1)  = -1. | 离子温度剖面系数 | x | x |  | x |  | x | x | x |
| **T_file** | 'none' | 读取温度剖面所用的 ASCII 文件。 | x | x | x | x | x | x | x | x |
| **Ti_file** | 'none' | 读取离子温度剖面所用的 ASCII 文件。 |  |  |  | x |  | x | x | x |
| **Te_file** | 'none' | 读取电子温度剖面所用的 ASCII 文件。 |  |  |  | x |  | x | x | x |
| **rhon_0** | 0. | 初始归一化中性粒子密度的中心值 |  |  |  | x |  |  |  |  |
| **rhon_1** | 0. | 初始归一化中性粒子密度的 SOL 值 |  |  |  | x |  |  |  |  |
| **rhon_coef** | 0. 0.01 0.01 | 初始中性粒子密度剖面的系数 |  |  |  | x |  |  |  |  |
| **Fprofile_file** | 'none' | 读取 Fprofile 所用的 ASCII 文件。 |  |  |  |  | x | x | x | x |
| **phi_0** | 0. | 中心背景电势；（通常为 1） | x | x |  |  |  |  |  |  |
| **phi_1** | 0. | 边缘背景电势 | x | x |  |  |  |  |  |  |
| **phi_coef** | 0.;  phi_coef(1) =  0.; phi_coef(4) = 1. | 电势剖面系数 | x | x |  |  |  |  |  |  |
| **phi_file** | 'none' | 读取电势剖面所用的 ASCII 文件。 | x | x |  |  |  |  |  |  |
| **nu_phi_source** | 0. | n=0 背景电势剖面源项的摩擦系数（>~ visco） |  | x |  |  |  |  |  |  |
| **FF_0** | 1. | 等离子体中心处的 FF' 值 | x | x | x | x | x | x | x | x |
| **FF_1** | 0. | SOL 中的 FF' 值 | x | x | x | x | x | x | x | x |
| **FF_coef** | 0.;  FF_coef(1)  = -1. | FF' 剖面的系数 | x | x | x | x | x | x | x | x |
| **ffprime_file** | 'none' | 读取 FF' 剖面所用的 ASCII 文件。 | x | x | x | x | x | x | x | x |
| **NEO** | .false. | 若为 .true. 则计入新经典效应（见 [[neo\|here]]） | x | x | x | x | x | x | x | x |
| **neo_file** | 'none' | 读取 aki 与 amu 剖面所用的 ASCII 文件。 | x | x | x | x | x | x | x | x |
| **aki_neo_const** | 0. | 若 ( (NEO) .and. (neo_file=='none') )，则 aki_neo 取该常数值 | x | x | x | x | x | x | x | x |
| **amu_neo_const** | 0. | 若 ( (NEO) .and. (neo_file=='none') )，则 amu_neo 取该常数值 | x | x | x | x | x | x | x | x |
| **output_bnd_elements** | .false. | 若为 .true.，则将边界节点与边界单元写入文件 'boundary_nodes.dat' 与 'boundary_elements.dat' | x | x | x | x | x | x | x | x |
| **RMP_on** | .false. | 若为 .true. 则在边界上激活 RMP（不含 STARWALL 的旧版本） | x | x | x | x |  |  |  |  |
| **RMP_psi_cos_file** | 'none' | 读取 psi_RMP_cos 及其导数剖面所用的 ASCII 文件 | x | x | x | x |  |  |  |  |
| **RMP_psi_sin_file** | 'none' | 读取 psi_RMP_sin 及其导数剖面所用的 ASCII 文件 | x | x | x | x |  |  |  |  |
| **RMP_growth_rate** | 0.011 |  | x | x | x | x |  |  |  |  |
| **RMP_ramp_up_time** | 1000 | psi_RMP 的时间依赖参数：Sigmoid 函数 f(t)= 1/ (1 + exp(-RMP_growth_rate*(t-RMP_ramp_up_time/2) )) | x | x | x | x |  |  |  |  |
| **RMP_har_cos** | 2 |  | x | x | x | x |  |  |  |  |
| **RMP_har_sin** | 3 |  | x | x | x | x |  |  |  |  |
| **Number_RMP_harmonics** | 1 | Number_RMP_harmonics < N_RMP_max。若只有一个谐波，则 Number_RMP_harmonics=1；默认在 models/preset_parameters.f90 中为 1 |  |  |  | x |  |  |  |  |
| **RMP_har_cos_spectrum** | RMP_har_cos | 若只有一个谐波，默认 RMP_har_cos_spectrum(1)=RMP_har_cos； |  |  |  | x |  |  |  |  |
| **RMP_har_sin_spectrum** | RMP_har_sin | 若只有一个谐波，默认 RMP_har_sin_spectrum(1)=RMP_har_sin |  |  |  | x |  |  |  |  |
| **V_0** | 0. | 解析平行旋转剖面——中心值 | x | x | x | x | x | x | x | x |
| **V_1** | 0. | 解析平行旋转剖面——SOL 值 | x | x | x | x | x | x | x | x |
| **V_coef** | 0., 0., 0., 0.1, 1.0 | 解析平行旋转剖面——系数 | x | x | x | x | x | x | x | x |
| **R_Z_psi_bnd_file** | 'none' | 用于 R_boundary、Z_boundary、psi_boundary 的 ASCII 文件，大小为 n_boundary。 | x | x | x | x | x | x | x | x |
| **wall_file** | 'wall.txt' | 外部壁几何的 ASCII 文件，若 n_ext 大于零时使用。 | x | x | x | x | x | x | x | x |
| **rot_file** | 'none' | 读取平行旋转剖面所用的 ASCII 文件（见 normalized_velocity_profile） | x | x | x | x |  |  |  |  |
| **normalized_velocity_profile** | .true. | 若为 true，则将归一化速度剖面作为磁通函数读取，否则将 Omega_tor 作为磁通函数读取。 | x | x | x | x |  |  |  |  |
| **domm_file** | 'none' | 含 Dommaschk 势系数的 namelist 文件 | x | x |  |  |  |  |  |  |
| **iter_precon** | 10 | 每当 gmres 迭代次数超过 iter_precon 时，更新预条件矩阵 | x | x | x | x | x | x | x | x |
| **max_steps_noUpdate** | 10000000 | 每当未更新预条件矩阵的步数超过 max_steps_noUpdate 时，更新预条件矩阵 | x | x | x | x | x | x | x | x |
| **gmres_m** | 20 | gmres 重启参数（维数） | x | x | x | x | x | x | x | x |
| **gmres_4** | 1.d3 | 见 gmres 手册（预条件误差与非预条件误差之比） | x | x | x | x | x | x | x | x |
| **gmres_tol** | 1.d-8 | gmres 迭代被视为收敛所用的容差 | x | x | x | x | x | x | x | x |
| **tgnum** | 0. | 各方程分别的 Taylor Galerkin 稳定化系数 | x | x | x |  |  |  |  |  |
| **tgnum_psi** | 0. | 同上，但避免了模型族的方程索引 |  |  |  | x |  |  |  |  |
| **tgnum_u** | 0. |  |  |  |  | x |  |  |  |  |
| **tgnum_zj** | 0. |  |  |  |  | x |  |  |  |  |
| **tgnum_w** | 0. |  |  |  |  | x |  |  |  |  |
| **tgnum_rho** | 0. |  |  |  |  | x |  |  |  |  |
| **tgnum_T** | 0. |  |  |  |  | x |  |  |  |  |
| **tgnum_Ti** | 0. |  |  |  |  | x |  |  |  |  |
| **tgnum_Te** | 0. |  |  |  |  | x |  |  |  |  |
| **tgnum_vpar** | 0. |  |  |  |  | x |  |  |  |  |
| **tgnum_rhon** | 0. |  |  |  |  | x |  |  |  |  |
| **tgnum_rhoimp** | 0. |  |  |  |  | x |  |  |  |  |
| **tgnum_nre** | 0. |  |  |  |  | x |  |  |  |  |
| **tgnum_AR** | 0. |  |  |  |  | x |  |  |  |  |
| **tgnum_AZ** | 0. |  |  |  |  | x |  |  |  |  |
| **tgnum_A3** | 0. |  |  |  |  | x |  |  |  |  |
| **keep_current_prof** | .true. | 用于近似维持初始电流剖面的人工电流源，即 $\eta(j-j0)$？ | x | x | x | x | x | x | x | x |
| **init_current_prof** | .false. | 由当前存在的电流剖面初始化电流源 | x | x |  |  |  |  |  |  |
| **D_prof_neg** | 1.d-5 | 背景粒子种密度为负的区域中的粒子扩散系数 | x | x | x | x |  |  |  |  |
| **D_prof_neg_thresh** | 0. | 若 r0-rimp0 < D_prof_neg_thresh，则 D_prof_neg 生效 | x | x | x | x |  |  |  |  |
| **D_prof_imp_neg_thresh** | -1.d3 | 若 rimp0 < D_prof_imp_neg_thresh，则 D_prof_neg 生效 |  |  |  | x |  |  |  |  |
| **D_prof_tot_neg_thresh** | 0. | 若 r0 < D_prof_tot_neg_thresh，则 D_prof_neg 生效 |  |  |  | x |  |  |  |  |
| **ZK_prof_neg** | 1.d-5 | 温度为负的区域中的垂直热扩散系数 | x | x | x | x |  |  |  |  |
| **ZK_par_neg** | 1.d-3 | 温度为负的区域中的平行扩散系数 |  |  |  | x |  |  |  |  |
| **ZK_prof_neg_thresh** | 0. | 若 T < ZK_prof_neg_thresh，则 ZK_prof_neg 生效 | x | x | x | x |  |  |  |  |
| **ZK_par_neg_thresh** | 0. | 若 T < ZK_par_neg_thresh，则 ZK_par_neg 生效 |  |  |  | x |  |  |  |  |
| **ZK_e_prof_neg** | 1.d-5 | 温度为负的区域中的垂直热扩散系数 |  |  |  | x |  |  |  |  |
| **ZK_e_par_neg** | 1.d-3 | 温度为负的区域中的平行扩散系数 |  |  |  | x |  |  |  |  |
| **ZK_e_prof_neg_thresh** | 0. | 若 T < ZK_e_prof_neg_thresh，则 ZK_e_prof_neg 生效 |  |  |  | x |  |  |  |  |
| **ZK_e_par_neg_thresh** | 0. | 若 T < ZK_e_par_neg_thresh，则 ZK_e_par_neg 生效 |  |  |  | x |  |  |  |  |
| **ZK_i_prof_neg** | 1.d-5 | 温度为负的区域中的垂直热扩散系数 |  |  |  | x |  |  |  |  |
| **ZK_i_par_neg** | 1.d-3 | 温度为负的区域中的平行扩散系数 |  |  |  | x |  |  |  |  |
| **ZK_i_prof_neg_thresh** | 0. | 若 T < ZK_i_prof_neg_thresh，则 ZK_i_prof_neg 生效 |  |  |  | x |  |  |  |  |
| **ZK_i_par_neg_thresh** | 0. | 若 T < ZK_i_par_neg_thresh，则 ZK_i_par_neg 生效 |  |  |  | x |  |  |  |  |
| **D_imp_extra_neg_thresh** | -1.d3 | 若 rho_imp < D_imp_extra_neg_thresh，则 D_imp_extra_neg 生效 |  |  |  | x |  |  |  |  |
| **T_min** | 1.0d-20 | 最低温度（用于限制电阻率等的温度依赖），取值以 jorek 单位计：2.01d-5*central_density*Tmin_ev（预设 central_density = 1，20 eV） | x | x | x | x | x | x | x | x |
| **rho_min** | 1.0d-20 | 最低密度 |  |  | x | x | x | x | x | x |
| **ne_SI_min** | 1.d18 | 最低电子密度（SI 单位），低于此值则截断辐射损失 |  |  |  | x |  |  |  |  |
| **Te_eV_min** | 5. | 最低温度（单位 eV），低于此值则截断辐射损失 |  |  |  | x |  |  |  | x |
| **rn0_min** | 1.d-8 | 辐射损失截断所用的最低杂质密度（JOREK 单位） |  |  |  | x |  |  |  |  |
| **T_min_neg** | -1.d12 | 最低温度，用于修正负值，以 jorek 单位计：2.01d-5*central_density*Tmin_ev（预设 central_density = 1，20 eV） |  |  | x | x | x | x | x | x |
| **rho_min_neg** | -1.d12 | 最低密度，用于修正负值 |  |  | x | x | x | x | x | x |
| **implicit_heat_source** | 0. | 取 = 1.d0 以完全启用以数值稳定为目的的隐式热源 |  |  |  | x |  |  |  |  |
| **n_tor_fft_thresh** | 2 | 若 n_tor >= n_tor_fft_thresh，则使用 element_matrix_fft | x | x | x | x | x | x | x | x |
| **corr_neg_temp_coef** | 0.5, 0.5 | models/corr_neg.f90 中使用的参数 | x | x | x | x | x | x | x | x |
| **corr_neg_dens_coef** | 0.5, 0.5 | models/corr_neg.f90 中使用的参数 | x | x | x | x | x | x | x | x |
| **thermalization** | .true. | 若为 true 则开启离子—电子热化项 |  |  |  | x |  | x | x | x |
| **zjz_0** | 0.1173 |  | x | x | x | x | x | x | x | x |
| **zjz_1** | 0.0 |  | x | x | x | x | x | x | x | x |
| **zj_coef** | 0.;  zj_coef(1)  = -1. |  | x | x | x | x | x | x | x | x |
{: .params-table}

## vacuum

| 参数 | 默认值 | 说明 | 180 | 183 | 199 | 600 | 710 | 711 | 712 | 750 |
|---|---|---|---|---|---|---|---|---|---|---|
| **CARIDDI_mode** | .false. | CARIDDI 或 STARWALL；若使用 CARIDDI 输入文件则为 True |  |  | x | x | x | x | x | x |
| **vacuum_min** | .false. | 最小化内存占用的模式 |  |  | x | x | x | x | x | x |
| **wall_resistivity_fact** | 1. | STARWALL 中指定的壁与线圈电阻率的缩放因子 | x | x | x | x |  |  |  |  |
| **wall_resistivity** | 0. | 外部壁的电阻率 | x | x | x | x |  |  |  |  |
| **n_pf_coils** | 0 | 极向场线圈数量 | x | x | x | x | x | x | x | x |
| **starwall_equil_coils** | .false. | 指定平衡 PF 线圈是否由 STARWALL 给出 | x | x | x | x | x | x | x | x |
| **find_pf_coil_currents** | .false. | 搜索最优的 pf_coil 电流以构建自由边界平衡？ [[jorek-starwall-faqs\|fbnd_eq_FAQs]] | x | x | x | x | x | x | x | x |
| **psi_offset_freeb** | 0. | 允许对 freeb_equil 的 psi 值加上一个全局常数平移（可改善收敛） | x | x | x | x | x | x | x | x |
| **current_ref** | 1.d22 | 反馈（FB）的目标总等离子体电流 Ip [[jorek-starwall-faqs\|fbnd_eq_FAQs]] | x | x | x | x | x | x | x | x |
| **FB_Ip_position** | 0.2 | Ip 反馈的放大因子（见 [[jorek-starwall-faqs\|fbnd_eq_FAQs]]） | x | x | x | x | x | x | x | x |
| **FB_Ip_integral** | 0.01 | Ip 反馈的放大因子（见 [[jorek-starwall-faqs\|fbnd_eq_FAQs]]） | x | x | x | x | x | x | x | x |
| **Z_axis_ref** | 1.d22 | 目标磁轴垂直位置（见 [[jorek-starwall-faqs\|fbnd_eq_FAQs]]） | x | x | x | x | x | x | x | x |
| **R_axis_ref** | -99. | 可选的目标磁轴径向位置（见 [[jorek-starwall-faqs\|fbnd_eq_FAQs]]） |  |  | x | x | x | x | x | x |
| **FB_Zaxis_position** | 1. | Zaxis 反馈的放大因子（见 [[jorek-starwall-faqs\|fbnd_eq_FAQs]]） | x | x | x | x | x | x | x | x |
| **FB_Zaxis_derivative** | 0. | Zaxis 反馈的放大因子（见 [[jorek-starwall-faqs\|fbnd_eq_FAQs]]） | x | x | x | x | x | x | x | x |
| **FB_Zaxis_integral** | 0. | Zaxis 反馈的放大因子（见 [[jorek-starwall-faqs\|fbnd_eq_FAQs]]） | x | x | x | x | x | x | x | x |
| **cte_current_FB_fact** | -1d99 | 在自由边界 GS 迭代之前缩放 FF' 与 T 剖面的常数因子（关闭电流反馈） |  |  | x | x | x | x | x | x |
| **start_VFB** | 10 | 开始垂直反馈的迭代步（见 [[jorek-starwall-faqs\|fbnd_eq_FAQs]]） | x | x | x | x | x | x | x | x |
| **n_feedback_current** | 2 | 每隔 n_... 次迭代执行一次反馈（见 [[jorek-starwall-faqs\|fbnd_eq_FAQs]]） | x | x | x | x | x | x | x | x |
| **n_feedback_vertical** | 1 | 每隔 n_... 次迭代执行一次反馈（见 [[jorek-starwall-faqs\|fbnd_eq_FAQs]]） | x | x | x | x | x | x | x | x |
| **n_iter_freeb** | 900 | 自由边界平衡的迭代次数（见 [[jorek-starwall-faqs\|fbnd_eq_FAQs]]） | x | x | x | x | x | x | x | x |
| **diag_coils** |  | 见 [[jorek-starwall-faqs\|jorek_starwall_FAQs]] | x | x | x | x | x | x | x | x |
| **rmp_coils** |  | 见 [[jorek-starwall-faqs\|jorek_starwall_FAQs]] | x | x | x | x | x | x | x | x |
| **voltage_coils** |  | 尚未就绪（见 [[jorek-starwall-faqs\|jorek_starwall_FAQs]]） | x | x | x | x | x | x | x | x |
| **pf_coils** | 0 | 见 [[jorek-starwall-faqs\|jorek_starwall_FAQs]] | x | x | x | x | x | x | x | x |
| **vert_FB_amp** |  | 为每个极向场线圈调节垂直反馈的方向与幅度（[[jorek-starwall-faqs\|eq_FAQs]]） | x | x | x | x | x | x | x | x |
| **rad_FB_amp** |  | 为每个极向场线圈调节垂直反馈的方向与幅度（[[jorek-starwall-faqs\|eq_FAQs]]） |  |  | x | x | x | x | x | x |
| **vert_pos_file** |  |  | x | x | x | x | x |  |  |  |
| **start_VFB_ts** | 0. | 模拟过程中主动 VFB 的起始时间（[JOREK 单位]） | x | x | x | x | x |  |  |  |
| **vert_FB_amp_ts** | 0. | 各线圈垂直反馈的幅度与符号（[[jorek-starwall-faqs\|eq_FAQs]]）；放大因子（相对于 PF 线圈） | x | x | x | x | x |  |  |  |
| **I_coils_max** | 1.d99 | 各线圈的电流限值（[安培]）；线圈电流的最大绝对值 | x | x | x | x | x |  |  |  |
| **vert_FB_gain** | 0. | 垂直反馈控制器的增益参数；VFB 控制器的比例、微分、积分增益 | x | x | x | x | x |  |  |  |
| **vert_FB_tact** | 1.d-9 | 两次控制器动作之间的时间间隔（[JOREK 单位]）；VFB 控制器的节拍 | x | x | x | x | x |  |  |  |
{: .params-table}
