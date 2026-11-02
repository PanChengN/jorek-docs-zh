---
title: "动理学逃逸电子"
nav_order: 7
parent: "动理学粒子模块"
layout: default
render_with_liquid: false
---

# 逃逸电子
逃逸电子的入门指引请参见[在 JOREK 中运行逃逸电子](./)。
# 耦合方案 
JOREK 中采用的耦合方案是压力耦合方案。然而，该方案还需要逃逸电子产生的电流。因此共有 3 个耦合参数：逃逸电子的平行与垂直压力，以及逃逸电子电流。

$$
\mathbf{J}_{\text{r}} = q\int \mathbf{v}f_{\text{r}} d^3\mathbf{v}
$$

$$
\mathcal{P}_{\text{r},\perp} = \frac{m}{2}\int \gamma_{\text{L}}v^2_{\perp}f_{\text{r}}d^3\mathbf{v}
$$

$$
\mathcal{P}_{\text{r},\parallel} = m \int \gamma_{\text{L}}v^2_{\parallel}f_{\text{r}}d^3\mathbf{v}
$$

下标 r 指逃逸电子，$$q$$ 为电子电荷，$m$ 为电子质量，$\mathbf{v}$ 为电子速度，$f_{\text{r}}$ 为逃逸电子分布函数，$v_{\perp}$ 与 $v_{\parallel}$ 分别为电子速度的垂直与平行分量，$\gamma_{\text{L}}$ 为洛伦兹因子。模拟中先计算这些量，再将其投影到 JOREK 有限元网格上，供相关的 MHD 方程使用。逃逸电子对 MHD 方程的影响体现在动量方程和电流中（$\mathbf{J}\rightarrow(\mathbf{J}-\mathbf{J}_{\text{r}})$，其中 $\mathbf{J}$ 指体 MHD 电流）。动量方程修改如下：

$$
\rho\left(\frac{\partial \mathbf{V}}{\partial t} + \mathbf{V}\cdot\nabla\mathbf{V}\right) = -\nabla p + \mathbf{J}\times\mathbf{B} -\left(\mathcal{P}_{\text{r},\parallel}-\mathcal{P}_{\text{r},\perp} \right)\boldsymbol{\kappa} - \nabla\mathcal{P}_{\text{r},\perp} + \nabla \cdot \boldsymbol{\tau}
$$

注意该方程中的 $\mathbf{J}$ 不包含逃逸电子电流。这是因为与压力相关的各项是由 $\mathbf{J}_{\text{r}}\times\mathbf{B}$ 导出的。更多细节见下文所列文献。

逃逸电子耦合方案的推导可参见 *V. Bandaru et al. Phys. Plasmas 2023*（https://doi.org/10.1063/5.0165240）。

该模型在 JOREK 中的实现以及 JET 中逃逸电子束终止的模拟可参见 *H. Bergström et al. Plasma Phys. Control. Fusion 2025*（https://doi.org/10.1088/1361-6587/adaee7） 

# 未纳入 kinetic_main 的实现 
JOREK 中还实现了若干其他与逃逸电子相关的物理（例如辐射力和碰撞），但尚未纳入 kinetic_main。详见[逃逸电子推进器](./runaway_electron_pushers.md)及其提到的示例可执行程序。注意使用这些示例可执行程序时须谨慎（尤其是在 kinetic_develop 分支中），因为部分功能可能与更新的 kinetic_main 框架不兼容。
