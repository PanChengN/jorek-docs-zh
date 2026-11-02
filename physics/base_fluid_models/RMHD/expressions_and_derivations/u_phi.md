---
title: "流函数与电势表达式"
nav_order: 9
parent: "表达式与推导"
grand_parent: "约化 MHD 模型"
layout: default
render_with_liquid: false
---

# 流函数与电势的推导

下面推导 $u$ 与 $\Phi$ 之间的联系。出发点是法拉第定律

$$\begin{equation}
  \partial_t\mathbf{B}=-\nabla\times\mathbf{E},
\end{equation}$$

该式也可用磁矢势表示：

$$\begin{equation}\label{dAdt}
  \partial_t\mathbf{A}=-\mathbf{E}-\nabla\Phi+\alpha_L\nabla\phi.
\end{equation}$$

这里，环电压 $\alpha_L$ 与电势 $\Phi$ 是消去旋度后作为积分常数引入的。由 $\nabla\times(\alpha_L\nabla\phi)=0$ 的要求可知，$\nabla_\text{pol}\alpha_L$ 必须为零。电场由下式给出

$$\begin{equation}\label{E}
  \mathbf{E}=-\mathbf{v}\times\mathbf{B}+\eta\mathbf{j}=-F\nabla_\text{pol}u - [\Psi,u]\mathbf{e}_\phi + \eta\mathbf{j},
\end{equation}$$

将式 $\eqref{E}$ 代入式 $\eqref{dAdt}$，可得

$$\begin{equation}
  \partial_t\mathbf{A}=F\nabla_\text{pol}u + [\Psi,u]\mathbf{e}_\phi - \eta\mathbf{j} - \nabla\Phi + \alpha_L\nabla\phi.
\end{equation}$$

在 JOREK 中，通过引入 $\mathbf{j}_0$ 把环电压项与电流合并：

$$\begin{equation}\label{dAdt9}
  \partial_t\mathbf{A}=F\nabla_\text{pol}u + [\Psi,u]\mathbf{e}_\phi - \eta(\mathbf{j}-\mathbf{j}_0) - \nabla\Phi.
\end{equation}$$

为完全自洽，$j_0$ 需取为 $\frac{\alpha_L}{\eta}\nabla\phi$，其中 $\alpha_L$ 在空间上为常数。

## 当取 $F\equiv F_0$ 并忽略 $\eta(\mathbf{j}-\mathbf{j}_0)$ 时：

可得 $\partial_t\mathbf{A}=\partial_t\psi\nabla\phi$。对式 $\eqref{dAdt9}$ 作用 $\nabla\phi\times(\dots)$，得到

$$\begin{equation}
  F_0\nabla\phi\times\nabla_\text{pol}u=\nabla\phi\times\nabla_\text{pol}\Phi
\end{equation}$$

这意味着电势 $\Phi$ 与速度流函数 $u$ 通过下式相联系

$$\begin{equation}
  F_0 u \equiv \Phi.
\end{equation}$$

（原则上该式中还有一个积分常数 $c\phi$，此处取为零）

随后可由 $E = -\nabla \Phi - \partial_t A$ 计算局域电场。

$$\begin{equation}
  \mathbf{E} = \left(- F_0 u_R, - F_0 u_Z, - F_0 u_\phi/R - \partial_t \psi/R\right),
\end{equation}$$

其中下标表示求导，矢量分量 $(R,Z,\phi)$ 分别写出。
