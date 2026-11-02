---
title: "电流表达式"
nav_order: 7
parent: "表达式与推导"
grand_parent: "约化 MHD 模型"
layout: default
render_with_liquid: false
---

# 电流表达式的推导

下面概述表达式 $j=\Delta^\ast\psi$ 的推导。出发点是磁场的定义

$$\begin{equation}
  \mathbf{B} = F\nabla\phi+\nabla\psi\times\nabla\phi
\end{equation}$$

等离子体电流由下式给出

$$\begin{equation}
  \mathbf{j} = \nabla\times\mathbf{B}.
\end{equation}$$

因此，

$$\begin{equation}\begin{split}
  \mathbf{j}
   &= \nabla\times(F\nabla\phi)+\nabla\times(\nabla\psi\times\nabla\phi) \\
   &= \nabla F\times\nabla\phi + F\underbrace{\nabla\times\nabla\phi}_{\equiv 0} + \nabla\times\left[\left(\partial_1\psi~\mathbf{a}^1+\partial_2\psi~\mathbf{a}^2+\partial_3\psi~\mathbf{a}^3 \right)\times\mathbf{a}^3 \right] \\
   &= \nabla F\times\nabla\phi + \nabla\times\left[-\frac{1}{R}\partial_1\psi~\mathbf{a}^2+\frac{1}{R}\partial_2\psi~\mathbf{a}^1 \right] \\
   &= \nabla F\times\nabla\phi + \frac{1}{R^2}\partial_{1,3}\psi~\mathbf{a}_1+\frac{1}{R^2}\partial_{2,3}\psi~\mathbf{a}_2-\frac{1}{R}\left[\partial_1\left(\frac{1}{R}\partial_1\Psi\right)+\frac{1}{R}\partial_{2,2}\psi\right]\mathbf{a}_3 \\
   &= \nabla F\times\nabla\phi + \frac{1}{R^2}\partial_{1,3}\psi~\mathbf{a}_1+\frac{1}{R^2}\partial_{2,3}\psi~\mathbf{a}_2-\frac{1}{R^2}\Delta^\ast\psi~\mathbf{a}_3 \\
   &= \nabla F\times\nabla\phi + \frac{1}{R^2}\partial_3(\nabla_\text{pol}\psi)-\Delta^\ast\psi~\nabla\phi \\
   &= \left(\frac{1}{R}\partial_2 F+\frac{1}{R^2}\partial_{1,3}\psi\right)\mathbf{a}^1+\left(-\frac{1}{R}\partial_1 F+\frac{1}{R^2}\partial_{2,3}\psi\right)\mathbf{a}^2-\Delta^\ast\psi~\mathbf{a}^3
\end{split}\end{equation}$$

电流的物理环向分量由下式给出

$$\begin{equation}
j_\phi
  = \mathbf{j}\cdot\mathbf{e}_\phi
  = -\partial_1\left(\frac{1}{R}\partial_1\psi\right)-\frac{1}{R}\partial_{2,2}\psi
  = -\frac{1}{R}\Delta^\ast\psi
\end{equation}$$

而 JOREK 变量 $j$ 由下式给出

$$\begin{equation}
  j = -R~j_\phi = \Delta^\ast\psi
\end{equation}$$
