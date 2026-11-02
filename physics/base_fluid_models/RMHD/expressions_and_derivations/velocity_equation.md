---
title: "平行动量方程推导"
nav_order: 15
parent: "表达式与推导"
grand_parent: "约化 MHD 模型"
layout: default
render_with_liquid: false
---

# 附录：平行动量方程的推导

动量方程的平行投影通过将算子 $\nabla\phi \cdot (\dots)$ 作用于动量方程得到。

出发点是动量方程：

$$\begin{equation}
\rho \left( \frac{\partial \mathbf{v}}{\partial t} + \mathbf{v} \cdot \nabla \mathbf{v} \right) = \mathbf{j} \times \mathbf{B} - \nabla p + \mu \nabla^2 \mathbf{v}
\end{equation}$$

将其乘以 $F_0 \nabla\phi$ 沿平行方向投影，并假定 $F \approx F_0$（常数），下面逐项分析。

### 时间导数项

速度 $\mathbf{v} = \mathbf{v}_{pol} + v_{||} \mathbf{B}$ 的时间导数投影到 $F_0 \nabla\phi$ 上给出：

$$\begin{equation*}
F_0 \nabla\phi \cdot \rho \frac{\partial \mathbf{v}}{\partial t} \approx \rho \frac{\partial v_{||}}{\partial t}
\end{equation*}$$

### 对流项

对流项 $\rho (\mathbf{v} \cdot \nabla \mathbf{v})$ 投影到 $F_0 \nabla\phi$ 上展开为：

$$\begin{equation*}
F_0 \nabla\phi \cdot \rho (\mathbf{v} \cdot \nabla \mathbf{v}) = - R \rho \left[ u, v_{||} \right] + \frac{1}{R} \rho v_{||} \left[ \psi, v_{||} \right] - \frac{F_0}{R^2} \rho v_{||} \partial_3 v_{||}
\end{equation*}$$

### 力项

$\mathbf{j} \times \mathbf{B}$ 项与压强梯度 $\nabla p$ 项的投影为：

$$\begin{align*}
F_0 \nabla\phi \cdot (\mathbf{j} \times \mathbf{B}) &= - \frac{1}{2R^2} \frac{\partial}{\partial \phi} \left| \nabla \psi \right|^2 \\
- F_0 \nabla\phi \cdot \nabla p &= - \frac{\partial p}{\partial \phi}
\end{align*}$$

### 合并后的方程

将上述各部分合并，即得 JOREK 中所用的平行动量方程形式：

$$\begin{equation*}\begin{split}
\rho \frac{\partial v_{\parallel}}{\partial t} = 
  & - R \rho \left[ u, v_{\parallel}\right] + \frac{1}{R} \rho v_{\parallel} \left[ \psi, v_{\parallel}\right] 
    - \frac{F_0}{R^2} \rho v_{\parallel} \partial_3 v_{\parallel}  \\
  & - \frac{1}{2R^2} \frac{1}{F_0} \frac{\partial}{\partial \phi} \left| \nabla \psi\right|^2 - \frac{1}{F_0} \frac{\partial p}{\partial \phi}
\end{split}\end{equation*}$$

该方程描述约化 MHD 极限下平行速度分量的演化。
