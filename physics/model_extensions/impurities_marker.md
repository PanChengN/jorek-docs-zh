---
title: "杂质——标记粒子模型"
nav_order: 2
parent: "杂质"
grand_parent: "模型扩展"
layout: default
render_with_liquid: false
---

## 使用标记粒子进行混合杂质 SPI 建模

本页说明在混合弹丸模拟中使用基于标记粒子的碰撞辐射非平衡杂质处理时的一些基本步骤与技巧。该方法的实现发表于 [D Hu et al 2021 Plasma Phys. Control. Fusion 63 125003](https://iopscience.iop.org/article/10.1088/1741-4326/acc8e9/meta)。

### 1. 代码版本（待更新）

截至 2024.11，建议使用分支 [IMAS-4606](https://git.iter.org/projects/STAB/repos/jorek/commits?until=refs%2Fheads%2FIMAS-4606-add-non-equilibrium-radiation-terms-in-model600-mod_elt_matrix_fft.f90-but-based-on-the&merges=include#) 的模型 600，而分支 [feature/SPImodel502_w_marker](https://git.iter.org/projects/STAB/repos/jorek/commits?until=refs%2Fheads%2Ffeature%2FSPImodel502_w_marker&merges=include#) 的模型 502 也被大量使用。

**注：** IMAS-4606 分支模型 600 的 `with_impurities=.t.` 与 `with_neutrals=.t.` 选项目前尚不应使用——调试仍在进行。详见该 [pull request](https://git.iter.org/projects/STAB/repos/jorek/pull-requests/891/overview)。

注意必须启用 `with_vpar` 选项。  

### 2. 编译（两步）

- 按通常不使用标记粒子的模拟的方式编译 JOREK。
- 编译标记粒子程序：`marker_spi_source.f90`，存放在 `/particles/examples`。注意编译前应在 Makefile.inc 中将 `USE -MUMPS` 设为 1，因为标记粒子投影需要 MUMPS。（不要与 JOREK namelist 中的相关项混淆：JOREK 输入文件中的 `use_mumps`、`use_pastix` 与 `use_strumpack` 指的是流体时间推进所用的求解器，与标记粒子设置无关）。

### 3. 运行模拟

注意使用标记粒子时需将 `EXPORT OMP_STACKSIZE` 设为更大的值（例如 50M），以避免（重启时）出现内存问题。 

**警告**：某些 Intel 编译器版本（例如 2021.10.0）存在会阻塞标记粒子模拟的缺陷！其成因是在 omp 循环中使用了 select type。据称该问题已在新版本编译器中修复……

#### JOREK namelist 中的新参数：

- `use_marker`：是否使用标记粒子
- `restart_particles`：类似 `restart`，但针对标记粒子 
- `n_particles`：模拟中使用的标记粒子（最大）数量。如上述 Di 的 PPCF 论文所述，一条经验法则是：一个标记粒子代表 10^{14} 个真实粒子。
- `tstep_particles`：推进标记粒子所用的时间步（SI 单位），应显著小于流体时间步，参见 Di 的论文。
- 需要施加滤波器以平滑粒子投影并保证数值稳定性。一个不错的初始设置可以是：

    - filter_perp = 1.d-4
    - filter_hyper = 1.d-8
    - filter_par = 5.d-1
    - filter_perp_n0 = 1.d-4
    - filter_hyper_n0 = 1.d-8
    - filter_par_n0 = 5.d-1


- `diff_diffusive_flux`：若设为 `.true.`，该选项会在标记粒子推进器中启用一个与 rho_imp 梯度成正比的附加项，从而模拟密度扩散，并有助于 aux05 与 rho_imp 的一致演化。

#### 使用标记粒子运行模拟的步骤：

- 关闭上述参数，先运行一段（例如约 50 个）时间步的标准 JOREK 模拟，不使用标记粒子（在作业脚本中使用常规的 `srun jorek_modelxxx`）
- 以 `use_marker = .t.` 但 `restart_particles = .f.` 重启模拟，因为此时模拟中还没有粒子。不要忘记在作业脚本中使用 `srun marker_spi_source`。 
- 达到设定的运行时间后再次重启模拟，这次同时设置 `restart_particles = .t.`，以便加载已保存的粒子信息。不要忘记把最新的粒子重启文件复制为 `part_restart.h5`（类似于 jorek 重启文件）

### 4. 诊断

使用分支 [IMAS-4606](https://git.iter.org/projects/STAB/repos/jorek/commits?until=refs%2Fheads%2FIMAS-4606-add-non-equilibrium-radiation-terms-in-model600-mod_elt_matrix_fft.f90-but-based-on-the&merges=include#) 时，多数标准 JOREK 诊断应可适用于标记粒子模拟。 

一些提示：
- 对于 `jorek2vtk` 或 `convert2vtk.sh`，使用命令时需包含选项 `-proj projections`。所得到的 vtk 文件中会生成 `aux01`、`aux05` 等额外场，例如用 Paraview 查看时即可看到。这些场分别对应电离功率密度（`aux01`）、辐射功率密度（`aux02`）、杂质有效电荷（`aux03`）、杂质组分的平均电荷（`aux04`）与杂质数密度（`aux05`），如 Di 的论文所述。 
- 合理性检查以确认参数设置合理：比较投影场与流体场，二者结构应非常相似。Weikang 提供的有用 Python 脚本（待补充）。
- 补充的合理性检查：将硬编码的 `CE_marker` 标志设为 true 后运行标记粒子程序。这样对标记粒子采用 CE 近似而非 CR 处理。结果应与使用 CE 近似的流体模拟相当，如 Di 的论文所讨论。
- `aux01`–`aux05` 变量也可作为 `jorek2_postproc` 的表达式使用。
- 将 aux 变量换算为物理单位需乘以归一化因子（例如为了与其流体对应量作定量比较）。归一化因子在 `marker_spi_source` 日志开头打印。特别地，辐射功率密度（`aux02`）的归一化因子为 `E_norm / t_norm`，杂质数密度（`aux05`）的归一化因子为 `N_norm`。
*本页为占位页——内容待补充。*
