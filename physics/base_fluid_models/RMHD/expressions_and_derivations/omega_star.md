---
title: "抗磁涡量表达式"
nav_order: 14
parent: "表达式与推导"
grand_parent: "约化 MHD 模型"
layout: default
render_with_liquid: false
---

<!-- untranslated-notice -->
<div class="warning" markdown="1">
**本页尚未翻译**，以下为 JOREK 官方英文原文。

原文页面：[The Diamagnetic Vorticity Expression](https://iterorganization.github.io/JOREK/physics/base_fluid_models/RMHD/expressions_and_derivations/omega_star.html)　·　源文件：`physics/base_fluid_models/RMHD/expressions_and_derivations/omega_star.md`
</div>

# Derivation of the Diamagnetic Vorticity

In JOREK models that include diamagnetic effects, the total vorticity $W$ is defined as the toroidal component of the curl of the ion velocity $\mathbf{v}_i$:

$$\begin{equation*}
  W \equiv (\nabla \times \mathbf{v}_i) \cdot \nabla \phi
\end{equation*}$$

The ion velocity is given by:

$$\begin{equation*}
  \mathbf{v}_i = \mathbf{v}_{E \times B} + \mathbf{v}_{dia,i} + v_{||} \mathbf{B}
\end{equation*}$$

Substituting the expressions for the $E \times B$ and diamagnetic velocities:

$$\begin{equation*}
  \mathbf{v}_i = -R^2 \nabla u \times \nabla \phi - \frac{\tau_{IC} R^2}{\rho} \nabla p_i \times \nabla \phi + v_{||} \mathbf{B}
\end{equation*}$$

The toroidal vorticity $W$ can be split into two main parts:

$$\begin{equation*}
  W = \omega + \omega^*
\end{equation*}$$

where $\omega$ is the standard vorticity related to the $E \times B$ flow:

$$\begin{equation*}
  \omega = \nabla \cdot \nabla_{pol} u
\end{equation*}$$

and $\omega^*$ is the part related to the diamagnetic flow and the parallel velocity term:

$$\begin{equation*}
  \omega^* = \nabla \cdot \left( \frac{\tau_{IC}}{\rho} \nabla_{pol} p_i - v_{||} \frac{1}{R^2} \nabla_{pol} \psi \right)
\end{equation*}$$

The full derivation of these terms, including the cancellation of terms with the gyro-viscous tensor, can be found in the [Vorticity Derivation](omega_deriv.md) and [RMHD Model](../rmhd_model.md) pages.
