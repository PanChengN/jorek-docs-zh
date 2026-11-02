---
title: "电流表达式"
nav_order: 7
parent: "表达式与推导"
grand_parent: "约化 MHD 模型"
layout: default
render_with_liquid: false
---

<!-- untranslated-notice -->
<div class="warning" markdown="1">
**本页尚未翻译**，以下为 JOREK 官方英文原文。

原文页面：[Current Expression](https://iterorganization.github.io/JOREK/physics/base_fluid_models/RMHD/expressions_and_derivations/j_psi.html)　·　源文件：`physics/base_fluid_models/RMHD/expressions_and_derivations/j_psi.md`
</div>

# Derivation of the Current Expression

The derivation of the expression $j=\Delta^*\psi$ is sketched in the following. Starting point is the definition of the magnetic field

$$\begin{equation}
  \mathbf{B} = F\nabla\phi+\nabla\psi\times\nabla\phi
\end{equation}$$

The plasma current is given by

$$\begin{equation}
  \mathbf{j} = \nabla\times\mathbf{B}.
\end{equation}$$

So,

$$\begin{equation}\begin{split}
  \mathbf{j}
   &= \nabla\times(F\nabla\phi)+\nabla\times(\nabla\psi\times\nabla\phi) \\
   &= \nabla F\times\nabla\phi + F\underbrace{\nabla\times\nabla\phi}_{\equiv 0} + \nabla\times\left[\left(\partial_1\psi~\mathbf{a}^1+\partial_2\psi~\mathbf{a}^2+\partial_3\psi~\mathbf{a}^3 \right)\times\mathbf{a}^3 \right] \\
   &= \nabla F\times\nabla\phi + \nabla\times\left[-\frac{1}{R}\partial_1\psi~\mathbf{a}^2+\frac{1}{R}\partial_2\psi~\mathbf{a}^1 \right] \\
   &= \nabla F\times\nabla\phi + \frac{1}{R^2}\partial_{1,3}\psi~\mathbf{a}_1+\frac{1}{R^2}\partial_{2,3}\psi~\mathbf{a}_2-\frac{1}{R}\left[\partial_1\left(\frac{1}{R}\partial_1\Psi\right)+\frac{1}{R}\partial_{2,2}\psi\right]\mathbf{a}_3 \\
   &= \nabla F\times\nabla\phi + \frac{1}{R^2}\partial_{1,3}\psi~\mathbf{a}_1+\frac{1}{R^2}\partial_{2,3}\psi~\mathbf{a}_2-\frac{1}{R^2}\Delta^*\psi~\mathbf{a}_3 \\
   &= \nabla F\times\nabla\phi + \frac{1}{R^2}\partial_3(\nabla_\text{pol}\psi)-\Delta^*\psi~\nabla\phi \\
   &= \left(\frac{1}{R}\partial_2 F+\frac{1}{R^2}\partial_{1,3}\psi\right)\mathbf{a}^1+\left(-\frac{1}{R}\partial_1 F+\frac{1}{R^2}\partial_{2,3}\psi\right)\mathbf{a}^2-\Delta^*\psi~\mathbf{a}^3
\end{split}\end{equation}$$

The physical toroidal component of the current is given by

$$\begin{equation}
j_\phi
  = \mathbf{j}\cdot\mathbf{e}_\phi
  = -\partial_1\left(\frac{1}{R}\partial_1\psi\right)-\frac{1}{R}\partial_{2,2}\psi
  = -\frac{1}{R}\Delta^*\psi
\end{equation}$$

and the JOREK variable $j$ is given by

$$\begin{equation}
  j = -R~j_\phi = \Delta^*\psi
\end{equation}$$
