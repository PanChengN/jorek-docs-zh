---
title: "连续性方程表达式"
nav_order: 12
parent: "表达式与推导"
grand_parent: "约化 MHD 模型"
layout: default
render_with_liquid: false
---

# 连续性方程的推导

JOREK 中的连续性方程为：

$$\begin{equation}
  \partial_t\rho=-\nabla\cdot(\rho\mathbf{v})+\nabla\cdot(D\nabla\rho) + S_\rho
\end{equation}$$

约化 MHD 模型中速度 $\mathbf{v}$ 的表达式为：

$$\begin{equation*}
\mathbf{v} = -R^2\nabla u \times \nabla\phi + v_{||}\mathbf{B}
\end{equation*}$$

将其代入连续性方程右端的第一项，可得：

$$\begin{equation*}\begin{split}
-\nabla\cdot(\rho\mathbf{v}) &= -\nabla\cdot\left[\rho\left(-R^2\nabla u \times \nabla\phi + v_{||}\mathbf{B}\right)\right] \\
&= \nabla\cdot\left[\rho R^2\nabla u \times \nabla\phi\right] - \nabla\cdot\left(\rho v_{||}\mathbf{B}\right)
\end{split}\end{equation*}$$

利用矢量恒等式 $\nabla\cdot(\mathbf{A}\times\mathbf{C}) = \mathbf{C}\cdot(\nabla\times\mathbf{A}) - \mathbf{A}\cdot(\nabla\times\mathbf{C})$ 以及 $\nabla\times\nabla\phi = 0$，第一项变为：

$$\begin{equation*}\begin{split}
\nabla\cdot\left(\rho R^2\nabla u \times \nabla\phi\right) &= \nabla\phi\cdot\left[\nabla\times\left(\rho R^2\nabla u\right)\right] \\
&= \nabla\phi\cdot\left[\nabla(\rho R^2)\times\nabla u + \rho R^2\underbrace{\nabla\times\nabla u}_{=0}\right] \\
&= \nabla\phi\cdot\left[\nabla(\rho R^2)\times\nabla u\right] \\
&= \frac{1}{R}[\rho R^2, u]
\end{split}\end{equation*}$$

对于第二项，利用 $\nabla\cdot\mathbf{B} = 0$，有：

$$\begin{equation*}\begin{split}
-\nabla\cdot\left(\rho v_{||}\mathbf{B}\right) &= -\mathbf{B}\cdot\nabla(\rho v_{||}) - \rho v_{||}\underbrace{\nabla\cdot\mathbf{B}}_{=0} \\
&= -\mathbf{B}\cdot\nabla(\rho v_{||}) \\
&= -\frac{F}{R^2}\partial_3(\rho v_{||}) - \frac{1}{R}[\rho v_{||}, \psi]
\end{split}\end{equation*}$$

将二者合并，即得约化 MHD 变量下的连续性方程：

$$\begin{equation}
\partial_t\rho = \frac{1}{R}[\rho R^2, u] - \frac{1}{R}[\rho v_{||}, \psi] - \frac{F}{R^2}\partial_3(\rho v_{||}) + \nabla\cdot(D\nabla\rho) + S_\rho
\end{equation}$$
