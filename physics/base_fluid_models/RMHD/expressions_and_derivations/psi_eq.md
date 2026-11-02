---
title: "极向磁通方程表达式"
nav_order: 13
parent: "表达式与推导"
grand_parent: "约化 MHD 模型"
layout: default
render_with_liquid: false
---

# 极向磁通方程的推导

极向磁通方程的出发点是感应方程：

$$\begin{equation}
  \partial_t\mathbf{B} = -\nabla\times\mathbf{E}
\end{equation}$$

将磁场表示为 $\mathbf{B}=\nabla\times\mathbf{A}$ 并消去旋度，可得：

$$\begin{equation}\label{dAdt}
  \partial_t\mathbf{A} = -\mathbf{E} - \nabla\Phi + \alpha_L\nabla\phi
\end{equation}$$

其中 $\Phi$ 为电势，$\alpha_L$ 表示环电压。将该方程乘以 $R^2\nabla\phi$，得到：

$$\begin{equation*}
  R^2\nabla\phi\cdot\partial_t\mathbf{A} = -R^2\nabla\phi\cdot\mathbf{E} - R^2\nabla\phi\cdot\nabla\Phi + R^2\nabla\phi\cdot\alpha_L\nabla\phi
\end{equation*}$$

利用极向磁通的定义 $\psi = R^2\mathbf{A}\cdot\nabla\phi = RA_\phi$ 以及电势关系 $F_0 u \equiv \Phi$，各项为：

$$\begin{align*}
  R^2\nabla\phi\cdot\partial_t\mathbf{A} &= \partial_t\psi \\
  -R^2\nabla\phi\cdot\nabla\Phi &= -R^2\frac{1}{R^2}\partial_3\Phi = -\partial_3\Phi = -F_0\partial_\phi u \\
  R^2\nabla\phi\cdot\alpha_L\nabla\phi &= \alpha_L
\end{align*}$$

电场项 $-R^2\nabla\phi\cdot\mathbf{E}$ 利用欧姆定律 $\mathbf{E} = -\mathbf{v}\times\mathbf{B} + \eta\mathbf{j}$ 计算：

$$\begin{equation*}\begin{split}
  -R^2\nabla\phi\cdot\mathbf{E} &= R^2\nabla\phi\cdot(\mathbf{v}\times\mathbf{B}) - R^2\nabla\phi\cdot\eta\mathbf{j} \\
  &= R^2\frac{1}{R}[\psi, u] - R^2\eta\frac{1}{R^2}(j - j_0) \\
  &= R[\psi, u] - \eta(j - j_0)
\end{split}\end{equation*}$$

其中 $j_0$ 是通过 $\eta j_0 = \alpha_L$ 与环电压 $\alpha_L$ 相关联的电流源。

将各项合并，即得 JOREK 中所用的极向磁通方程：

$$\begin{equation}
  \partial_t\psi = R[\psi, u] + \eta(j - j_0) - F_0\partial_\phi u
\end{equation}$$
