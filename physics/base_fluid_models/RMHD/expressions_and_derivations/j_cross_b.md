---
title: "j×B 项表达式"
nav_order: 10
parent: "表达式与推导"
grand_parent: "约化 MHD 模型"
layout: default
render_with_liquid: false
---

# j×B 项的推导

$$\begin{equation*}\begin{split}
\mathbf{j}\times\mathbf{B} 
=& \left(\nabla F\times\nabla\phi+\frac{1}{R^2}\nabla_\text{pol}\partial_3\psi-\Delta^\ast\psi\nabla\phi\right)\times(F\nabla\phi+\nabla\psi\times\nabla\phi) \\
=& -F\nabla\phi\times(\nabla F\times\nabla\phi) + (\nabla F\times\nabla\phi)\times(\nabla\psi\times\nabla\phi) + \frac{F}{R^2}\nabla_\text{pol}\partial_3\psi\times\nabla\phi \\
 & +\frac{1}{R^2}\nabla_\text{pol}\partial_3\psi\times(\nabla_\text{pol}\psi\times\nabla\phi)-F\Delta^\ast\psi\underbrace{\nabla\phi\times\nabla\phi}_{\equiv 0}-\Delta^\ast\psi\nabla\phi\times(\nabla\psi\times\nabla\phi) \\
=&-\frac{F}{R^2}\nabla_\text{pol}F+\frac{1}{R}\nabla\phi[F,\psi]-\frac{\Delta^\ast\psi}{R^2}\nabla_\text{pol}\psi+\frac{1}{R^2}\nabla_\text{pol}\partial_3\psi\times\mathbf{B}
\end{split}\end{equation*}$$
