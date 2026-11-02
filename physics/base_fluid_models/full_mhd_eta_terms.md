---
title: "全 MHD 中的弱形式电阻项"
nav_order: 16
parent: "基础流体模型"
grand_parent: "物理模型"
layout: default
render_with_liquid: false
---

# 全 MHD 中电阻项的弱形式积分
# 引言

本页说明全 MHD 中电阻项如何通过分部积分处理。这样做的主要原因是避免二阶导数——在全 MHD 中，二阶导数会因快波而既含噪声又数值不稳定。

这样做的主要问题在于：原则上分部积分会带来边界项，这些边界项在 `mod_boundary_matrix_open.f90` 中实现；只要相关变量 `AR`、`AZ` 和 `A3` 在边界上被固定，即采用 Dirichlet 边界条件，这些边界项就可以忽略。然而，在全 MHD 中这样做并不正确，因为 `AR` 和 `AZ` 原则上应保持自由。因此，我们在此尝试给出所有项的推导。

---

# 弱形式下的电阻项

电阻项在感应方程中表示为

$$
\begin{aligned}
\partial_{t} \vec{A} &= \vec{v}\times\vec{B} - \eta\vec{J}, \\
\vec{B} &= B^R\vec{e}_R + B^Z\vec{e}_Z + B^{\phi}\vec{e}_{\phi}, \\
\vec{J} &= \nabla\times\vec{B} \\
&= \vec{e}_R \frac{1}{R} \left(RB^{\phi}_Z - B^Z_{\phi}\right)
+\vec{e}_Z \frac{1}{R} \left(B^R_{\phi} - RB^{\phi}_R - B^{\phi}\right)
+\vec{e}_{\phi} \left(B^Z_R - B^R_Z\right), \\
\vec{A} &= A^R\vec{e}_R + A^Z\vec{e}_Z + A^3\nabla\phi .
\end{aligned}
$$

注意，在 JOREK 中，$\vec{B}$ 与速度 $\vec{u}$ 一样用其物理分量 $B^{\phi}\vec{e}_{\phi}$ 表示，而磁矢势 $\vec{A}$ 则用其几何分量表示

$$
A^3\nabla\phi = \vec{e}_{\phi}\frac{A^3}{R},
$$

因此，全 MHD 的 $A^3$ 与约化 MHD 的 $\psi$ 之间存在对应关系。

上述 $\vec{J}$ 的表达式可以重新整理，用散度项表示，这会使后续的分部积分更清晰。首先注意，对于像 $\vec{B}$ 这样以物理环向分量 $B^{\phi}\vec{e}_{\phi}$ 表示的矢量，有

$$
\nabla\cdot\vec{B}
=
\frac{1}{R}\partial_R \left(RB^R\right)

+ \partial_Z B^Z
+ \frac{1}{R}\partial_{\phi}B^{\phi}.
  $$

因此，

$$
\begin{aligned}
\vec{J} &= \vec{e}_R J^R + \vec{e}_Z J^Z + \vec{e}_{\phi}J^{\phi}, \\
J^R
&= \frac{1}{R} \left(RB^{\phi}_Z - B^Z_{\phi}\right)
= \nabla\cdot\left(B^{\phi}\vec{e}_Z - B^Z\vec{e}_{\phi}\right), \\
J^Z
&= \frac{1}{R} \left(B^R_{\phi} - RB^{\phi}_R - B^{\phi}\right)
= \nabla\cdot\left(B^R\vec{e}_{\phi} - B^{\phi}\vec{e}_R\right), \\
J^{\phi}
&= B^Z_R - B^R_Z
= R \nabla\cdot\left(\frac{1}{R}B^Z\vec{e}_R - \frac{1}{R}B^R\vec{e}_Z\right).
\end{aligned}
$$

因此，在弱形式下，取检验函数 $V$，在由表面 $\xi$ 包围的体积 $\Omega$ 上积分，电阻项给出

$$
\begin{aligned}
\int_{\Omega} - V\eta\vec{J} d\Omega
&=
\int_{\Omega} - V\eta
\left(
J^R\vec{e}_R
+ J^Z\vec{e}_Z
+ J^{\phi}\vec{e}_{\phi}
\right)
d\Omega .
\end{aligned}
$$

---

# 分部积分

下面我们对沿 $\vec{e}_R$、$\vec{e}_Z$ 和 $\vec{e}_{\phi}$ 三个矢量投影得到的每一项分别作分部积分。在区域边界 $\xi$ 上，定义法向量为

$$
\vec{n} = n^R\vec{e}_R + n^Z\vec{e}_Z .
$$

在 JOREK 中，由于我们的区域边界是环向轴对称的（尽管对仿星器情形未必如此），因此有

$$
\vec{n}\cdot\vec{e}_{\phi} = 0 .
$$

---

## $\vec{e}_R$ 项的积分

$$
\begin{aligned}
&\int_{\Omega} - V\eta J^R d\Omega\\
&=
\int_{\Omega}

- V\eta
  \nabla\cdot
  \left(
  B^{\phi}\vec{e}_Z - B^Z\vec{e}_{\phi}
  \right)
  d\Omega \\
  &=
  \int_{\Omega}
- \nabla\cdot
  \left[
  V\eta
  \left(
  B^{\phi}\vec{e}_Z - B^Z\vec{e}_{\phi}
  \right)
  \right]
  d\Omega \\
  &\quad

+ \int_{\Omega}
  \nabla(V\eta)
  \cdot
  \left(
  B^{\phi}\vec{e}_Z - B^Z\vec{e}_{\phi}
  \right)
  d\Omega \\
  &=
  \int_{\xi}

- V\eta
  \left(
  B^{\phi}\vec{e}_Z - B^Z\vec{e}_{\phi}
  \right)
  \cdot \vec{n} d\xi \\
  &\quad

+ \int_{\Omega}
  \left[
  B^{\phi} \left(V_Z\eta + V\eta_Z\right)

  - \frac{1}{R} B^Z \left(V_{\phi}\eta + V\eta_{\phi}\right)
    \right]
    d\Omega \\
    &=
    \int_{\xi}

- V\eta B^{\phi}n^Z
  d\xi \\
  &\quad

+ \int_{\Omega}
  \left[
  B^{\phi} \left(V_Z\eta + V\eta_Z\right)

  - \frac{1}{R} B^Z \left(V_{\phi}\eta + V\eta_{\phi}\right)
    \right]
    d\Omega .
    \end{aligned}
    $$

因此，在 `mod_elt_matrix_fft.f90` 中所需的右端项为

```fortran
+ v * (eta_Z*Bp - eta_p*BZ/R)
+ eta * (v_Z*Bp - v_p*BZ/R)
```

而在 `mod_boundary_matrix_open.f90` 中所需的右端项为

```fortran
- v * eta * Bp * normal(2)
```

---

## $\vec{e}_Z$ 项的积分

$$
\begin{aligned}
&\int_{\Omega} - V\eta J^Z d\Omega\\
&=
\int_{\Omega}

- V\eta
  \nabla\cdot
  \left(
  B^R\vec{e}_{\phi} - B^{\phi}\vec{e}_R
  \right)
  d\Omega \\
  &=
  \int_{\Omega}
- \nabla\cdot
  \left[
  V\eta
  \left(
  B^R\vec{e}_{\phi} - B^{\phi}\vec{e}_R
  \right)
  \right]
  d\Omega \\
  &\quad

+ \int_{\Omega}
  \nabla(V\eta)
  \cdot
  \left(
  B^R\vec{e}_{\phi} - B^{\phi}\vec{e}_R
  \right)
  d\Omega \\
  &=
  \int_{\xi}

- V\eta
  \left(
  B^R\vec{e}_{\phi} - B^{\phi}\vec{e}_R
  \right)
  \cdot \vec{n}
   d\xi \\
  &\quad

+ \int_{\Omega}
  \left[
  \frac{1}{R} B^R \left(V_{\phi}\eta + V\eta_{\phi}\right)

  - B^{\phi} \left(V_R\eta + V\eta_R\right)
    \right]
    d\Omega \\
    &=
    \int_{\xi}
+ V\eta B^{\phi}n^R
  d\xi \\
  &\quad
+ \int_{\Omega}
  \left[
  \frac{1}{R} B^R \left(V_{\phi}\eta + V\eta_{\phi}\right)

  - B^{\phi} \left(V_R\eta + V\eta_R\right)
    \right]
    d\Omega .
    \end{aligned}
    $$

因此，在 `mod_elt_matrix_fft.f90` 中所需的右端项为

```fortran
+ v * (eta_p*BR/R - eta_R*Bp)
+ eta * (v_p*BR/R - v_R*Bp)
```

而在 `mod_boundary_matrix_open.f90` 中所需的右端项为

```fortran
+ v * eta * Bp * normal(1)
```

---

## $R\vec{e}_{\phi}$ 项的积分

请记住，环向方程的投影含有因子 $R$，因此 $A^3$（即 $\psi$）的时间导数项在代码中写作 $\partial_t A^3$，而不是 $\frac{1}{R}\partial_t A^3$，因为

$$
\begin{aligned}
&\int_{\Omega} - V\eta J^{\phi} d\Omega\\
&=
\int_{\Omega}

- V\eta R^2
  \nabla\cdot
  \left(
  \frac{1}{R}B^Z\vec{e}_R

  - \frac{1}{R}B^R\vec{e}_Z
    \right)
    d\Omega \\
    &=
    \int_{\Omega}
- \nabla\cdot
  \left[
  V\eta R^2
  \left(
  \frac{1}{R}B^Z\vec{e}_R

  - \frac{1}{R}B^R\vec{e}_Z
    \right)
    \right]
    d\Omega \\
    &\quad

+ \int_{\Omega}
  \nabla(V\eta R^2)
  \cdot
  \left(
  \frac{1}{R}B^Z\vec{e}_R

  - \frac{1}{R}B^R\vec{e}_Z
    \right)
    d\Omega \\
    &=
    \int_{\xi}

- V\eta R
  \left(
  B^Z\vec{e}_R - B^R\vec{e}_Z
  \right)
  \cdot \vec{n}
   d\xi \\
  &\quad

+ \int_{\Omega}
  \left[
  B^Z
  \left(
  V_R\eta R + V\eta_R R + 2V\eta
  \right)

  - RB^R
    \left(
    V_Z\eta + V\eta_Z
    \right)
    \right]
    d\Omega \\
    &=
    \int_{\xi}
+ V\eta R
  \left(
  B^Z n^R - B^R n^Z
  \right)
   d\xi \\
  &\quad
+ \int_{\Omega}
  \left[
  B^Z
  \left(
  V_R\eta R + V\eta_R R + 2V\eta
  \right)

  - RB^R
    \left(
    V_Z\eta + V\eta_Z
    \right)
    \right]
    d\Omega .
    \end{aligned}
    $$

最后，为清晰起见，我们给出 JOREK 中所需的右端项，同时记住 $d\Omega$ 体积被积函数中含有因子 $R$。

因此，在 `mod_elt_matrix_fft.f90` 中所需的右端项为

```fortran
+ v * R * (eta_R*BZ - eta_Z*BR)
+ eta * (2*v + R*v_R)*BZ
- eta * R * v_Z*BR
```

而在 `mod_boundary_matrix_open.f90` 中所需的右端项为

```fortran
+ v * eta * R * BZ * normal(1)
- v * eta * R * BR * normal(2)
```

实际上，该项可以忽略，因为 $A^3$ 在边界上是固定的。不过，对于自由边界情形，这些项或许需要保留。
