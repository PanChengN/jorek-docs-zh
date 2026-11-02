---
title: "使用非线性时间推进（Newton 迭代）运行"
nav_order: 7
parent: "数值方法与稳定化"
grand_parent: "使用指南"
layout: default
render_with_liquid: false
---

# 非精确 Newton 求解器

## 概述

在 JOREK 中建立并求解物理方程的标准做法是：每个时间步对物理变量线性化一次方程，然后按 [JOREK 求解器](../numerics/solver.html) 所述求解所得的线性系统 $Ax=b$。当时间步较大或处于非线性阶段时，该方法可能不再适用。因此，希望有一种至少在原则上能够非线性求解物理方程的方法。这可以通过非精确 Newton 方法实现，该方法此前已在 JOREK 中部分实现 [参考文献 1](#ref-1)。求解器对当前计算阶段是线性还是非线性的敏感性，也使自适应时间步成为可能。

## 非精确 Newton 方法

### Newton 方法

将时间线性化后的物理方程所构成的非线性系统写为

$$
F(u^{n+1})=F(u^{n+1};u^n,u^{n-1})
=G(u^{n+1})-b(u^n,u^{n-1})=0.
\tag{1}
$$

为符号简洁起见（滥用记号），$F$ 隐含依赖 $u^n,u^{n-1}$，而 $G$ 与 $b$ 通过参数 $\theta$ 与 $\xi$ 依赖于时间积分方法的选取；参见 [时间积分](../numerics/time-integration.html) 以及 [参考文献 1](#ref-1) 第 23 页。标准方法在 $u^n$ 处对式 (1) 线性化并求解

$$
F^{\prime}(u^{n})\delta u^{n+1}
=-F(u^n)
=-G(u^{n})+b(u^n,u^{n-1})=0.
\tag{2}
$$

此处，$\delta u^{n+1}:=u^{n+1}-u^n$ 对应所求的解向量 $x$，且

$$
F^{\prime}(u^n)
=\frac{\partial F(u^{n+1};u^n,u^{n-1})}{\partial u^{n+1}}
\bigg\vert_{u^{n+1}=u^n}
=\frac{\partial G(u^{n+1})}{\partial u^{n+1}}
\bigg\vert_{u^{n+1}=u^n}.
\tag{3}
$$

因此，标准方法只线性化一次，通过求解 $\delta u^{n+1}$ 得到第 $n+1$ 步的物理变量。

Newton 方法迭代求解式 (1)。对给定的时间步 $n\to n+1$，构造序列 $\{u_k\}_{k\in\mathbb{N}}$，使得 $k\to\infty$ 时 $u_k\to u^{n+1}$。以初始估计 $\delta u_0$ 在 $u_{k=0}=u^n+\delta u_0$ 处线性化式 (1)：

$$
F(u_{1})\simeq F(u_0)+(u_{1}-u_0)F^{\prime}(u_0)
\stackrel{!}{=}0
\Rightarrow
F^{\prime}(u_0)\delta u_{1}
=-F(u_0)
=-G(u^{n}+\delta u_0)+b(u^n,u^{n-1}).
\tag{4}
$$

此处，$u_{k=1}=u_{k=0}+\delta u_{k=1}$ 是 $n+1$ 处物理变量的下一次估计。在每次迭代 $k$ 中，线性系统为

$$
F^{\prime}(u_k)\delta u_{k+1}=-F(u_k),
\tag{5}
$$

其中 $F(u_k)=F(u_k;u^n,u^{n+1})$。

雅可比矩阵 $F^{\prime}(u^n)=G^{\prime}(u^n)$ 与式 (2) 的右端项在 `call construct_matrix(...)` 中构造。在式 (4) 中，只需更新 $G(u_k)$。由于代码中无法独立访问 $G$，将式 (5) 的右端项写为

$$
-F(u_k)
=-G(u_k)+b(u^n,u^{n-1})-G(u^n)+G(u^n)
=-F(u^n)-F^{\prime}(u_k)(u_k-u^n),
\tag{6}
$$

因而

$$
F^{\prime}(u_k)\delta u_{k+1}
=-F(u^n)-F^{\prime}(u_k)\delta u_k^n,
\qquad
\delta u_k^n=u_k-u^n
=\delta u_k+\delta u_{k-1}+\dots+\delta u_0.
\tag{7}
$$

对每一步 $k$，雅可比矩阵 $F^{\prime}(u_k)$ 通过 `construct_matrix` 计算。第 $k$ 个右端项由第 $n$ 个右端项减去 $F^{\prime}(u_k)\delta u_k^n$ 得到，随后调用求解器。一旦达到收敛，$u^{n+1}=u_k=u^n+\delta u_k^n$。

### “非精确”的部分

只能使用非精确 Newton 方法，因为式 (7) 中的线性系统 $Ax=b$ 只能求解到有限容差。为保证收敛，式 (7) 各次求解的残差序列必须满足

$$
\frac{\left|F^{\prime}(u_k)\delta u_{k+1}+F(u_k)\right|}
{\left|F(u_k)\right|}
<1
\quad\Leftrightarrow\quad
\epsilon_k<\left|F(u_k)\right|.
\tag{8}
$$

容差 $\{\epsilon_k\}$ 必须据此选取；参见 [参考文献 2](#ref-2)。否则，对所有 $k$ 取 $\delta u_{k+1}=0$ 都会成为可接受的解。类比 [参考文献 1](#ref-1)，令

$$
\epsilon_k
=\min\left(\epsilon_0,\frac{1}{2}\epsilon_{k-1},\eta_k\right),
\qquad
\eta_k
:=\gamma\left(\frac{|F(u_k)|}{|F(u_{k-1})|}\right)^\alpha,
\tag{9}
$$

其中常用取值为 $\gamma=0.5$、$\alpha=2$。只有在式 (8) 得到满足，或式 (7) 右端项下降（$|F(u_k)|<|F(u_{k-1})|$）时，继续迭代才有意义。实际计算中，若连续两次迭代都出现 $|F(u_k)|>|F(u_{k-1})|$，则中止计算。

## 用法

要使用已实现的非精确 Newton 方法，先检出相应的功能分支：

```bash
git checkout feature/nlin_tstep
```

在 `Makefile.inc` 中添加以下行：

```makefile
USE_NEWTON = 1
```

`solvers/mod_inexact_newton.f90` 中的模块在主程序中加载：

```fortran
program JOREK2
...
#ifdef USE_NEWTON
use mod_inexact_newton, only: inexact_newton
#endif
implicit none
...
```

`inexact_newton` 子程序在 `jorek2_main.f90` 的求解器部分被调用：

```fortran
#ifdef USE_NEWTON
      call inexact_newton(...)
#elif USE_BICGSTAB
      call bicgstab_driver(...)
#else
      call gmres_driver(...)
#endif
```

非精确 Newton 方法的行为由输入变量控制：

```fortran
newton_start       = 5.d-1   !< start value, delta_k = deltas*newton_start
newton_gamma       = 5.d-1   !< gamma for computation of eps_k
newton_alpha       = 2.0d0   !< alpha for computation of eps_k
newton_eps_0       = 1.d-4   !< tolerance for initial Newton step
newton_eps_f       = 1.d-6   !< tolerance for final Newton step
newton_max_iter    = 20      !< maximum number of Newton iterations
```

GMRES 迭代上限照常由 `gmres_max_iter` 设定。变量 `newton_alpha` 与 `newton_gamma` 对应式 (9)，可保持不变。式 (4) 中 $k=0$ 步的起始值为 $\delta u_0=\delta u^n\times\mathtt{newton\_start}$。

在多数测试算例中，`newton_eps_0/newton_eps_f = 10..1000` 可带来快速收敛。一般而言要求 `newton_eps_f > gmres_tol`，而 `newton_eps_f/gmres_tol = 10..100` 可得到物理上合理的结果。此处 `gmres_tol = 1.d-5...1.d-8` 是标准情形下会设定的容差。参数 `newton_max_iter` 设定 Newton 迭代的最大次数；达到该次数后计算即停止。

## 自适应时间步

要使用自适应时间步，检出相应的功能分支：

```bash
git checkout feature/nlin_tstep_adaptive
```

同样，在 `Makefile.inc` 中添加该行：

```makefile
USE_NEWTON = 1
```

附加的输入参数为：

```fortran
newton_adapt_time = .false. !< switch for adaptive time stepping
newton_alpha_dt   = 1.05    !< fast convergence: increase tstep
newton_beta_dt    = 0.95    !< slow convergence: decrease tstep
newton_gamma_dt   = 0.75    !< non-convergence: retry with a smaller tstep
```

用以下设置启用该功能：

```fortran
newton_adapt_time = .true.
```

时间步根据收敛情况自适应调整：

- **快速收敛：** 若 $\sum_k \mathtt{iter\_gmres}\leq\mathtt{gmres\_max\_iter}/2$，则对 $n+1\to n+2$ 用 `tstep = tstep*newton_alpha_dt` 增大时间步。
- **收敛缓慢：** 若 $\sum_k \mathtt{iter\_gmres}>\mathtt{gmres\_max\_iter}/2$，则对 $n+1\to n+2$ 用 `tstep = tstep*newton_beta_dt` 减小时间步。
- **不收敛：** 用 `tstep = tstep*newton_gamma_dt` 重新计算第 $n\to n+1$ 步。

此处 $k$ 为 Newton 迭代序号。存在硬编码的最小时同步 `t_min = 0.001`。若以 `tstep = t_min` 仍无法收敛，则中止计算。参数 `newton_alpha_dt`、`newton_beta_dt` 与 `newton_gamma_dt` 应针对具体算例主动调优。

## 限制

目前只纳入并测试了 `jorek_model = 199, 303, 501, 502, 600, 710, 711, 712`。原则上，只要把所有新参数加入相应的 `models/modelXYZ/initialise_parameters.f90`，即可添加新模型。

## 参考文献

1. <a id="ref-1"></a>Franck, E., Hoelzl, M., Lessig, A., & Sonnendrucker, E. (2014). “Energy Conservation and numerical stability for the reduced MHD models of the non-linear JOREK code.” *Mathematical Modelling and Numerical Analysis*, 49, 1331–1365. [arXiv:1408.2099v3](https://arxiv.org/abs/1408.2099)
2. <a id="ref-2"></a>Dembo, R. S., Eisenstat, S. C., & Steihaug, T. (1982). “Inexact Newton Methods.” *SIAM Journal on Numerical Analysis*, 19(2), 400–408. [doi:10.1137/0719025](https://doi.org/10.1137/0719025)
