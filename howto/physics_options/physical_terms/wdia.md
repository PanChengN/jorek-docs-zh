---
title: "在黏性项中计入抗磁漂移"
nav_order: 2
parent: "物理项激活"
grand_parent: "物理选项"
layout: default
render_with_liquid: false
---

# 如何在黏性项中计入抗磁漂移

- **何时有用？** 在低电阻率条件下使用抗磁项时。
- **已实现于：** 模型 303、307、333、500 和 600。
- **如何激活？** 在 namelist 输入文件中设置 `Wdia = .true.`。该贡献还要求 `tauIC` 与 `visco` 取非零值。


# 黏性抗磁项的推导

在当前的方程中，黏性项写为

$$
-\int \mu \nabla v \cdot \nabla W \, dV,
$$

因此在分部积分之前，实际的物理项为

$$
+\int v \, \nabla \cdot \left(\mu \nabla W\right)\, dV.
$$

也就是说，黏性位于散度算子内部。

对黏性抗磁项，在弱形式下，出发点为

$$
\int v \, \nabla \cdot \left(\mu \nabla W_{\mathrm{dia}}\right)\, dV.
$$

分部积分给出

$$
-\int \mu \nabla v \cdot \nabla W_{\mathrm{dia}}\, dV
+
\int \nabla \cdot
\left(
\mu v \nabla W_{\mathrm{dia}}
\right)\, dV.
$$

假定边界项为零，

$$
-\int \mu \nabla v \cdot \nabla W_{\mathrm{dia}}\, dV.
$$

再次分部积分给出

$$
+\int
\left[
\nabla \cdot \left(\mu \nabla v\right)
\right]
W_{\mathrm{dia}}\, dV
-
\int
\nabla \cdot
\left(
\mu \nabla v \, W_{\mathrm{dia}}
\right)\, dV.
$$

再次假定边界项为零，最终形式为

$$
+\int
W_{\mathrm{dia}}
\left[
\nabla \cdot \left(\mu \nabla v\right)
\right]
\, dV.
$$

展开散度，

$$
+\int
W_{\mathrm{dia}}
\nabla\mu \cdot \nabla v
\, dV
+
\int
\mu W_{\mathrm{dia}}
\nabla^2 v
\, dV.
$$

若 $\mu$ 依赖于温度，

$$
\nabla \mu
=
\frac{\partial \mu}{\partial T}\nabla T,
$$

因而

$$
+\int
W_{\mathrm{dia}}
\frac{\partial\mu}{\partial T}
\nabla T \cdot \nabla v
\, dV
+
\int
\mu W_{\mathrm{dia}}
\nabla^2 v
\, dV.
$$

## JOREK 中的实现

在 JOREK 中，取

$$
dV = R\,\mathrm{xjac},
$$

相应的项为

$$
+
R
\frac{\partial\mu}{\partial T}
W_{\mathrm{dia}}
\left(
v_x T_x + v_y T_y
\right)
\mathrm{xjac},
$$

以及

$$
+
R \mu W_{\mathrm{dia}}
\left(
v_{xx}
+
\frac{v_x}{R}
+
v_{yy}
\right)
\mathrm{xjac}.
$$

其中，

$$
W_{\mathrm{dia}}
=
\frac{\tau}{\rho}
\left(
p_{xx}
+
\frac{p_x}{R}
+
p_{yy}
\right)
-
\frac{\tau}{\rho^2}
\left(
\rho_x p_x
+
\rho_y p_y
\right).
$$
