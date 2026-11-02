---
title: "plot_live_data.sh 脚本"
nav_order: 16
render_with_liquid: false
parent: "Running JOREK"
---

- 在算例目录中运行该脚本，即可绘制例如模拟期间或模拟之后的**能量时间曲线**。
- 例如（点击可放大）：![](energies.png?400)
- 该脚本需要较新版本的 gnuplot（在许多机器上可直接使用，或通过 'module' 命令加载）
- 还可以绘制**增长率**（`plot_live_data.sh -q g`）、与**时间步**对应的模拟时间（`plot_live_data.sh -q t`）以及**输入剖面**（`plot_live_data.sh -q i`），今后也很容易继续扩展
- **用 `plot_live_data.sh -l` 列出所有可绘制的量**

## 用法说明（plot_live_data.sh -h）

  ```
  Usage: plot_live_data.sh [-h -f <file> -l -q <qtty> -ps -(no)log]

    -h         Print this usage information
    -f <file>  Take data from <file> instead of 'macroscopic_vars.dat'
    -l         List plottable quantities
    -q <qtty>  Plot the given quantity (default: '-q energies')
    -ps        Plot to .ps files (default: plot to screen)
    -(no)log   (Non-)Logarithmic y-axis (default: '-log')

  Remarks:
  - The beginning of a quantity name is sufficient, e.g., the command
      'plot_live_data.sh -q gr' will plot growth_rates.

  ```
## 检查能量守恒 {#check-energy-conservation}
### 总能量守恒

实时数据可以让你实时检查 JOREK 如何守恒能量（或不守恒）。**能量守恒诊断必须针对每个模型单独适配**，因为新增物理项会带来新的能量通道。考虑一个基本的黏性—电阻 MHD 模型，总能量密度的演化方程为

\begin{equation}
\label{eq:energy_density}
\partial_t w + \nabla\cdot\mathbf{\Gamma}=\tau_{nc} 
\end{equation}

其中能量密度与能量通量（略去 $\mu_0$ 因子）分别为

\begin{align}
w &\equiv \frac{\rho}{2}|\mathbf{v}|^2 + \frac{p}{\gamma-1}+\frac{|\mathbf{B}|^2}{2}   
 \mathbf{\Gamma} &\equiv \left[ \frac{\rho}{2}|\mathbf{v}|^2  + \frac{\gamma}{\gamma-1}p \right]\mathbf{v} + \frac{\mathbf{q}}{\gamma-1} + \mathbf{E}\times\mathbf{B} 
\end{align}

式 \eqref{eq:energy_density} 的右端项（$\tau_{nc}$）表示非守恒项，例如源项（如加热源）与汇项（如辐射）。耗散项（如电阻项与黏性项）原则上不应出现在（$\tau_{nc}$）中。不过，例如当 $\eta \neq \eta_{ohmic}$ 时，一部分损失的磁能不会通过欧姆加热项转化为热能，从而产生一个非守恒项。式 \eqref{eq:energy_density} 的推导概述见下面的 ![slides ](artola_energy_conservation_diagnostics.pdf)。能量守恒诊断基于式 \eqref{eq:energy_density} 在 JOREK 计算域上的体积分，即

\begin{equation}
\label{eq:total_energy_ev}
\partial_t E_{tot} = \textrm{Boundary fluxes} + \textrm{Non-conservative/source terms}  
\end{equation}

以及

\begin{align}
E_{tot} &\equiv \int_V w dV   
 \textrm{Boundary fluxes} &\equiv -\oint_S \mathbf{\Gamma}\cdot\mathbf{n}dS  
\textrm{Non-conservative/source terms} &\equiv \int_V \tau_{nc} dV
\end{align}

用下面的命令检查 LFS（原文如此，应为 LHS）与 RHS 两项，即可确认式 \eqref{eq:total_energy_ev} 是否得到满足

  jorek_folder/util/plot_live_data.sh -q energy_conservation

若能量守恒良好，两条曲线应当重合，如下例所示。

![](example_energy_conservation1.png?nolink)

也可以用下面的命令绘制各类能量及其时间导数

  ```
  jorek_folder/util/plot_live_data.sh -q integrated_energies
  jorek_folder/util/plot_live_data.sh -q dEdt

  ```
它们的标签命名如下

\begin{align}
\textrm{Total energy} &\equiv E_{tot}   
\textrm{Magnetic} &\equiv \int_V \frac{|\mathbf{B}|^2}{2} dV   
\textrm{Thermal energy} &\equiv \int_V \frac{p}{\gamma-1} dV   
\textrm{Kinetic parallel} &\equiv \int_V\frac{\rho}{2}|\mathbf{v}_\parallel|^2 dV   
\textrm{Kinetic perpendicular} &\equiv \int_V\frac{\rho}{2}|\mathbf{v}_u|^2 dV 
\end{align}
其中 $\mathbf{v}_u=-R^2\nabla u\times \nabla\phi$。

也可以用下面的命令绘制不同的边界通量

  jorek_folder/util/plot_live_data.sh -q bnd_fluxes

它们的标签为

\begin{align}
\textrm{"p vn"} &\equiv \int_S \frac{\gamma}{\gamma-1}p \mathbf{v}\cdot\mathbf{n}dS   
\textrm{"kinpar-flux"} &\equiv \int_S \frac{\rho}{2}|\mathbf{v}|^2 \mathbf{v}\cdot\mathbf{n}dS    
\textrm{"qn-par"} &\equiv  \int_S  \frac{\mathbf{q}_{\parallel}\cdot\mathbf{n}}{\gamma-1}dS   
\textrm{"qn-perp"} &\equiv  \int_S  \frac{\mathbf{q}_{\perp}\cdot\mathbf{n}}{\gamma-1}dS   
\end{align}

注意，如果在计算域的整个边界上（**不只是偏滤器**）都设置鞘层边界条件，那么上面 4 项通量之和就对应于穿过鞘层流走的能量，以及 Stangeby 给出的公式（见[带鞘层边界条件运行热流计算](../howto/physics_options/boundary_conditions/sheath_heatflux_bc.md)）。

在固定边界模拟中，坡印廷通量通常为 0（如何绘制见下一节关于磁能守恒的内容。）

在当前 JOREK 版本（已适配 RMHD）中，诊断把下列各项视为非守恒项

\begin{equation}
\textrm{Non-conservative/source terms} = \int_V \left( \frac{S_T}{\gamma-1} + S_{mag} + (\eta_{ohmic}-\eta) |\mathbf{J}|^2  -\boldsymbol{\nu}_\parallel\cdot\mathbf{v}_\parallel  \right) dV
\end{equation}

其中 $S_T = S_{T_i}+S_{T_e}$ 是离子与电子合起来的加热源（用于温度方程），$S_{mag}$ 是由电流源项提供的磁能源（见下一节），最后一项是通过平行黏性耗散掉的能量。这些项可以用下面的命令绘制

  jorek_folder/util/plot_live_data.sh -q dissipative_terms

注意，以上所有量都可以用 [jorek2_postproc](jorek2_postproc.md) 的 "expressions_int" 命令**通过后处理重新获得**。用法见 "help expressions_int"，在 jorek2_postproc 中输入 "expressions_int" 即可列出所有可用量（约 67 个）。



### 磁能守恒

与总能量方程类似，磁能方程的各个图可以用下面的命令绘制

  ```
  jorek_folder/util/plot_live_data.sh -q mag_energy_balance

  ```
![](screenshot_from_2020-04-19_13-20-17.png?800)

磁能方程及所绘制的各项可在文档 ![](mag_energy_evolution.pdf) 中找到（也可以查看对应的 ![ pull request](https://git.iter.org/projects/STAB/repos/jorek/pull-requests/376/overview) ）
