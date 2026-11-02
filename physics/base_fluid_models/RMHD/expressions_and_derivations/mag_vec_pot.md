---
title: "磁矢势"
nav_order: 6
parent: "表达式与推导"
grand_parent: "约化 MHD 模型"
layout: default
render_with_liquid: false
---

# 磁矢势

磁矢势的拟设（ansatz）为***（该拟设与 JOREK 方程的推导无关；关于规范（Gauge）的细节缺失）***：

$$\begin{equation*}
\mathbf{A}=\nabla\alpha\times\nabla\phi+\psi\nabla\phi
\end{equation*}$$

其中假定 $\partial_3\alpha\equiv 0$。$\mathbf{A}$ 的旋度由下式给出

$$\begin{equation*}\begin{split}
\nabla\times\mathbf{A}
 &= \nabla\times(\nabla\alpha\times\nabla\phi)+\nabla\times(\psi\nabla\phi) \\
 &= -\Delta^\ast\alpha\nabla\phi+\frac{1}{R^2}\nabla_\text{pol}\underbrace{\partial_3\alpha}_{\equiv 0} + \nabla\psi\times\nabla\phi + \psi\underbrace{\nabla\times\nabla\phi}_{\equiv 0} \\
 &= -\Delta^\ast\alpha\nabla\phi+\nabla\psi\times\nabla\phi
\end{split}\end{equation*}$$

由于该式必须与磁场表达式 $\mathbf{B}=F\nabla\phi+\nabla\psi\times\nabla\phi$ 一致，可导出如下条件：

$$\begin{equation*}
  F\equiv-\Delta^\ast\alpha
\end{equation*}$$
