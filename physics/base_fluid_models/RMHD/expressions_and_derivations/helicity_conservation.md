---
title: "螺旋度守恒"
nav_order: 17
parent: "表达式与推导"
grand_parent: "约化 MHD 模型"
layout: default
render_with_liquid: false
---

# JOREK 中的螺旋度守恒

磁螺旋度定义为：

$$
\begin{equation*}
H=\mathbf{A}\cdot\mathbf{B}.
\end{equation*}
$$

可以证明，在理想 MHD 中，若 $\mathbf{B}$ 与 $\mathbf{v}$ 垂直于边界的分量均为零，则 $H$ 的体积积分为守恒量（例如参见 D. Biskamp 所著 *Nonlinear Magnetohydrodynamics* 一书第 2.2 节）。

在电阻 MHD 中，$H$ 并不精确守恒，而是以正比于等离子体电阻的速率耗散（参见 Biskamp 第 7.3.1 节）。在快速的 MHD 弛豫过程中（例如破裂的热淬灭阶段），预期 $H$ 的耗散远慢于磁能，从而对全局动力学施加约束（例如参见 A. Boozer 的[这篇 2019 年 PPCF 论文](https://iopscience.iop.org/article/10.1088/1361-6587/aaf293)）。

在 JOREK 的约化 MHD 版本中，矢势可采用如下可接受的表达式：

$$
\begin{equation*}
\mathbf{A} = \psi \nabla \phi - F_0 \frac{Z}{R} \nabla R.
\end{equation*}
$$

确实，

$$
\begin{equation*}
\nabla \times \mathbf{A} = \nabla\psi\times \nabla\phi + F_0 \nabla\phi
\end{equation*}
$$

这与 $\mathbf{B}$ 的表达式相对应（见 [JOREK 约化 MHD 模型](../rmhd_model.md)），并且

$$
\begin{equation*}
\partial_t \mathbf{A} = \partial_t \psi \nabla\phi
\end{equation*}
$$

这与电场的感应部分相对应。

相应的螺旋度表达式为：

$$
\begin{equation*}
  \begin{split}
H &= \mathbf{A} \cdot \mathbf{B} \\
  &= (\psi \nabla \phi - F_0 \frac{Z}{R} \nabla R) \cdot (\nabla\psi\times \nabla\phi + F_0 \nabla\phi) \\
  &= F_0 \frac{\psi}{R^2} - F_0 \frac{Z}{R^2} \partial_Z \psi \\
  &= F_0 \frac{\psi}{R^2} - \frac{F_0}{R^2} [\partial_Z (Z \psi) - \psi] \\
  &= 2 F_0 \frac{\psi}{R^2} - \frac{F_0}{R^2} \partial_Z (Z \psi).
  \end{split}
\end{equation*}
$$

现在考虑 $\frac{d}{dt}\int H dV$，其中积分是计算域（该域在时间上固定）上的体积积分：

$$
\begin{equation*}
  \begin{split}
\frac{d}{dt}\int H dV &= \int \partial_t H dV \\
  &= \int [2 F_0 \frac{\partial_t \psi}{R^2} - \frac{F_0}{R^2} \partial_Z (Z \partial_t \psi)] dV \\
  &= \int [2 F_0 \frac{\partial_t \psi}{R} - \frac{F_0}{R} \partial_Z (Z \partial_t \psi)] d\phi dS \\
  \end{split}
\end{equation*}
$$

其中 $dS$ 是极向平面内的面元。

第二项可沿 $Z$ 直接积分，得到边界项；若边界上 $\partial_t \psi = 0$（固定边界模拟即属此情形），这些边界项为零。

为计算第一项，利用极向磁通方程：

$$
\begin{equation*}
  \partial_t\psi = R[\psi,u] - F_0 \partial_\phi u + \eta j - R^2 \nabla \cdot \left( \frac{\eta_{num}}{R} \nabla_{\text{pol}} j \right)
\end{equation*}
$$

$\partial_\phi u$ 项在沿 $\phi$ 积分时为零。至于泊松括号：

$$
\begin{equation*}
  \begin{split}
  [\psi,u] &= \partial_R \psi \partial_Z u - \partial_Z \psi \partial_R u \\
           &= \partial_Z (u \partial_R \psi) - \partial_R (u \partial_Z \psi)
  \end{split}
\end{equation*}
$$

而若边界上 $u=0$（固定边界模拟即属此情形，即电势在理想导壁上为常数，对应流入壁的法向速度分量为零），这两项在沿 $R$ 或 $Z$ 积分时均为零。

由散度定理，超电阻项化为边界积分：

$$
\begin{equation*}
 \int - \nabla \cdot \left( \frac{\eta_{num}}{R} \nabla_{\text{pol}} j \right)dV = -\oint \frac{\eta_{num}}{R} \mathbf{n}\cdot\nabla_{\text{pol}} j dS_{bnd}
\end{equation*}
$$

其中 $\mathbf{n}$ 是 JOREK 边界的单位法向量（指向域外）。最后，总螺旋度的时间导数为

$$
\begin{equation*}
  \begin{split}
\frac{d}{dt}\int H dV &= 2 F_0 \int \frac{\eta j}{R} d\phi dS -2F_0\oint \frac{\eta_{num}}{R} \mathbf{n}\cdot\nabla_{\text{pol}} j dS_{bnd} \\
  \end{split}
\end{equation*}
$$

由此重新得到经典结论：螺旋度以电阻速率耗散。
