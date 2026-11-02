---
title: "高能离子"
nav_order: 7
parent: "动理学粒子模块"
layout: default
render_with_liquid: false
---

# 高能离子

通过动理学粒子框架，可在 JOREK 中引入一种超热离子。为模拟高能粒子（EP）与 MHD 模的相互作用，采用混合动理学-MHD 模型 [1]。等离子体被分为主体部分（用 MHD 模型处理）与高能粒子部分（以动理学方式处理）。关于 JOREK 实现与应用的更多细节见 [2]。

## Full-f

JOREK 对 EP 采用 full-f 表述。其分布函数由 $N_\mathrm{p}$ 个标记粒子建模：

$$
    f(\mathbf{r}, \mathbf{v}, t) = \sum_{i=1}^{N_\mathrm{p}} w_i \, \delta(\mathbf{r}-\mathbf{r}_i(t)) \, \delta(\mathbf{v}-\mathbf{v}_i(t))
$$

标记粒子用可用的推进器之一随时间演化，例如 Boris 推进器。

## 耦合方案

EP 与主体 MHD 流体之间的耦合由压力耦合方案提供。EP 压力张量 $\boldsymbol{P}_\mathrm{h}$ 按下式进入动量平衡方程

$$
  \rho \frac{\partial \mathbf{u}}{\partial t}=-\rho \mathbf{u} \cdot \nabla \mathbf{u}+\mathbf{J} \times \mathbf{B}-\nabla p +  \left[ \nabla\cdot\underline{\boldsymbol{P}_\mathrm{h}}\right]_\perp
$$

通常不使用完整张量，而是采用 CGL 形式

$$
  \underline{\boldsymbol{P}}_\mathrm{h} =  \left[  P_{\parallel} \mathbf{b}\mathbf{b} + P_{\perp}\left( \underline{1}-\mathbf{b}\mathbf{b} \right)  \right]
$$

其分量为

$$
  P_\parallel = m \int \mathrm{d}^3 \mathbf{v} \ f(\mathbf{r}, \mathbf{v}, t) v_\parallel^2
$$

$$
  P_\perp = \frac{m}{2} \int \mathrm{d}^3 \mathbf{v} \ f(\mathbf{r}, \mathbf{v}, t) v_\perp^2
$$

在约化 MHD 中，也可以通过设置 `use_pcs_full = .false.` 与 `use_pcs = .true.` 为 EP 改用标量压力。在 full MHD 模型中，只实现了 CGL 形式，并且总是通过 `use_pcs = .true.` 开启。

压力张量由以下六个分量给出

$$
  \boldsymbol{P}_\mathrm{h}^{RR}, \ \boldsymbol{P}_\mathrm{h}^{ZZ}, \ \boldsymbol{P}_\mathrm{h}^{\phi\phi} \ \boldsymbol{P}_\mathrm{h}^{\phi\phi}, \ \boldsymbol{P}_\mathrm{h}^{RZ}, \ \boldsymbol{P}_\mathrm{h}^{R\phi}, \ \boldsymbol{P}_\mathrm{h}^{Z\phi}
$$

这些分量随后用于 `mod_elt_matrix_fft` 中的 MHD 方程组。

## 示例

一个使用示例见 `particles/examples/tae_phase_space_project.f90`，其输入位于 `namelist/model307/itpa(_eq)` 或 `namelist/model710/itpa_full(_eq)`。这是产生 TAE 的 ITPA EP 基准算例的设置 [3]。

在 JOREK 中运行包含 EP 的模拟分两步：

1. 用所需的 jorek 模型（`jorek_modelXXX`）建立 MHD 平衡。运行 0 个时间步。这将生成文件 `jorek_restart.h5`。
2. 运行耦合的粒子模拟。这既可以用专门的粒子可执行程序（如 `tae_phase_space_project`）完成，也可以使用通用程序 `kinetic_main`。



## 诊断

相空间投影为 EP 提供了非常有用且灵活的诊断手段。在文件 `particles/diagnostics/mod_phase_space_project.f90` 中，相空间投影的接口与函数配有详尽注释。

投影的基本思想是把任意粒子物理量计算为任意实空间或速度空间坐标的函数。一个例子是某段特定时间段内的能量交换作为平行速度与磁矩的函数：

$$
  G(v_\parallel, \mu) = \sum_{i=1}^{N_\mathrm{p}} \Delta E_i \ w_i \delta(v_\parallel - v_{\parallel,i}) \delta(\mu - \mu_i)
$$

其中 $\Delta E_i$ 为第 $i$ 个标记粒子的能量变化。

在 JOREK 中，这些投影可以用几种方式完成。可以使用函数 `new_phase_space_projection` 并事先提供投影函数，或者用子程序 `project_single_particle_x` 为每个标记粒子填充一个投影值数组。



## 高能粒子的初始化

### 与 MHD 平衡的一致性

EP 可以贡献总压力的很大一部分。因此，在非线性模拟中重要的是近似满足条件

$$
  p_\mathrm{eq} = p_\mathrm{EP} + p_\mathrm{bulk}
$$

其中 $p_\mathrm{eq}$ 是用于计算 MHD 平衡的压力。这可以通过例如在平衡计算与耦合粒子模拟中使用不同的温度分布和/或密度分布来实现。

### 期望的输入剖面

EP 可以有很大的轨道宽度，不一定停留在某个特定的磁面上。因此，在 full-f 方案中，依据归一化磁通的期望剖面来初始化标记粒子分布并非易事。朴素的初始化会导致剖面弛豫。

### 导入快粒子实验分布

导入快粒子实验分布函数的功能位于文件 `mod_import_experimental_dist.f90` 中。
目前唯一的选择是使用四维分布函数，因为假定另外两个维度（回旋相位与环向角）是均匀分布的。此时维度为 $(R,Z, \lambda,E)$，其中 $\lambda$ 为投掷角，定义为 $\lambda = \frac{v_\parallel}{|\mathbf{v}|}$。该分布函数随后在四维网格上作线性插值并进行四维拒绝采样。回旋相位与环向角则均匀采样，但可以选择把粒子复制 $n_\phi$ 份，使 $\phi$ 以 $\frac{2\pi}{n_\phi}$ 递增（从而消除环向谐波）。这也可以只对一部分粒子进行（以保持噪声扰动足够大）。

期望的 HDF5 结构如下：
   * 4 个一维网格：'E_1D'、'Pitch_1D'、'R_1D' 与 'Z_1D'
   * 1 个四维归一化分布函数 'F0_norm'。其取值不能大于 1。小于 0 的值被忽略（这对拒绝采样没有影响）。

单位为：
   * R [m]
   * Z [m]
   * Pitch {-1.0, ...,1.0}。其符号可能有些令人困惑，因为有时是相对于 J 给出，有时是相对于 B 给出。在当前实现中，用例是 AUG，它相对于 J 给出，而 J 与 B 方向相反，因此 $v_\parallel = - \lambda |\mathbf{v}|$（在 JOREK 中 $v_\parallel$ 是相对于 B 的）。在代码中（或在 HDF5 中）改动这一点很容易。建议用诊断工具确认你所取的符号是否正确。
   * E [eV]


## 参考文献：
[1] W. Park et al., Phys. Fluids B 4, 2033 (1992).

[2] T. Bogaarts et al., Phys. plasmas 29, 122501 (2022).

[3] A. Könies et al., Nucl. Fusion 58, 126027 (2018).
