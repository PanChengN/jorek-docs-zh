---
title: "抗磁涡量表达式"
nav_order: 14
parent: "表达式与推导"
grand_parent: "约化 MHD 模型"
layout: default
render_with_liquid: false
---

# 抗磁涡量的推导

在包含抗磁效应的 JOREK 模型中，总涡量 $W$ 定义为离子速度 $\mathbf{v}_i$ 的旋度的环向分量：

$$\begin{equation*}
  W \equiv (\nabla \times \mathbf{v}_i) \cdot \nabla \phi
\end{equation*}$$

离子速度由下式给出：

$$\begin{equation*}
  \mathbf{v}_i = \mathbf{v}_{E \times B} + \mathbf{v}_{dia,i} + v_{||} \mathbf{B}
\end{equation*}$$

代入 $E \times B$ 速度与抗磁速度的表达式：

$$\begin{equation*}
  \mathbf{v}_i = -R^2 \nabla u \times \nabla \phi - \frac{\tau_{IC} R^2}{\rho} \nabla p_i \times \nabla \phi + v_{||} \mathbf{B}
\end{equation*}$$

环向涡量 $W$ 可分为两大部分：

$$\begin{equation*}
  W = \omega + \omega^\ast
\end{equation*}$$

其中 $\omega$ 是与 $E \times B$ 流相关的标准涡量：

$$\begin{equation*}
  \omega = \nabla \cdot \nabla_{pol} u
\end{equation*}$$

而 $\omega^\ast$ 是与抗磁流及平行速度项相关的部分：

$$\begin{equation*}
  \omega^\ast = \nabla \cdot \left( \frac{\tau_{IC}}{\rho} \nabla_{pol} p_i - v_{||} \frac{1}{R^2} \nabla_{pol} \psi \right)
\end{equation*}$$

这些项的完整推导（包括与陀螺黏性张量相关项的抵消）见[涡量推导](omega_deriv.md)页与 [RMHD 模型](../rmhd_model.md)页。
