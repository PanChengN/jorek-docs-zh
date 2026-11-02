---
title: "RMHD 中的平行电场"
nav_order: 16
parent: "表达式与推导"
grand_parent: "约化 MHD 模型"
layout: default
render_with_liquid: false
---

# JOREK 中的电场

在实际放电中，等离子体的完整形状与尺寸并非一次性形成。

先开启环向场，充入气体，随后施加“变压器电压”。这会在内侧附近产生一小块等离子体“斑点”（之所以在内侧，是因为该处环向路径最短，因而伏特/米最大）。随后该“斑点”与等离子体电流一起迅速增长到完整尺寸。

之所以采用这种方式，是因为在增长过程中等离子体温度尚不高，不存在电场/磁场向等离子体内扩散的问题。然而一旦达到具有完整 $I_p$ 的热等离子体状态，磁扩散时间尺度就过长，任何外部电磁变化都无法引起等离子体芯部的快速变化。

因此，在所关注的时间尺度上，一旦达到具有完整 $I_p$ 的热等离子体状态，变压器的 $\partial\mathbf{A}/\partial t$ 就不再进入等离子体芯部（尽管边界区域可能感受到它）。

因此，在具有完整 $I_p$ 的热等离子体状态下，我们拥有的是等离子体电流 $J_0$ 及其相伴的无旋环向电场 $\mathbf{E}_0$（因处于稳态而无旋）。容易证明，无旋条件导致如下形式的平衡环向电场

$$
E_0 = \frac{C_0}{R},
$$

其中 $C_0$ 为常数。

上述讨论的要点在于：等离子体中的平衡环向电场 $\mathbf{E}_0$ 不能与等离子体空间内的局域 $\partial\mathbf{A}/\partial t$ 相关联或相等同。

此外，JOREK 并不追踪/包含由变压器作用引起的边界磁通的时间导数。那么，“电流源”项究竟以什么前提进入法拉第定律？如果把法拉第定律反旋（uncurl）以适配等离子体初始的无流动二维平衡态，这一点就相当清楚。

在等离子体的严格内部对法拉第定律反旋，可以写出

$$
\frac{\partial \mathbf{A}}{\partial t}
=
-\mathbf{E}
-
F_0\nabla u
-
\nabla v_l,
$$

而不失一般性。

附加项 $\nabla v_l$ 是必需的，因为 JOREK 对电势 $F_0u$ 的使用与解释并不完整——它不包含/不容纳环向上的初始电势梯度。

上式应满足我们模拟中的初始条件，即无流动的稳态二维平衡，也就是说

$$
\frac{\partial}{\partial t}(\ldots)=0,
\qquad
\nabla u = 0.
$$

由此得到

$$
-\nabla v_l
=
\mathbf{E}_{t=0}
=
E_0\hat{\mathbf e}_{\phi}
=
\eta_0\left(J_0-J_{b0}\right)\hat{\mathbf e}_{\phi}.
$$

最后一个等号来自将作用在电子上的电场力与碰撞阻力相等同，因为电子惯性可忽略。

其中

$$
\eta_0 = \eta(T_0,Z_{\mathrm{eff},0})
$$

是在平衡/初始状态下计算的电阻率（我们的模拟中通常取 $Z_{\mathrm{eff},0}=1$），$J_0$ 为总的平衡等离子体电流密度，$J_{b0}$ 为平衡自举电流密度。

由于自举电流是“由输运产生”的，不能像 JOREK 中那样对其施加电阻率。否则我们还须计入最初产生自举电流的通行粒子与捕获粒子之间的碰撞力。因此我们不同时计入碰撞成因与碰撞阻力，而是采用一个经验模型（ad-hoc model）来简单估算自举电流。

将 $\nabla v_l$ 的上述表达式代入反旋后的法拉第定律，得到

$$
\frac{\partial\mathbf{A}}{\partial t}
=
-\mathbf{E}
-
F_0\nabla u
+
\eta_0\left(J_0-J_{b0}\right)\hat{\mathbf e}_{\phi}.
\tag{18.1}
$$

以这种方式得到上式，就避免了把环电压项当作一个凭空出现（out-of-the-blue）的项引入，并附上“为在模拟中维持恒定电流而人为加入该项，因为现实如此”之类的临时理由。

因此，上式中最后一项应简单解释为我们的模拟中等离子体区域在初始时刻（$t=0$）的平衡电场。

在一般情况下，电场随后可由下式经必要的投影直接算出

$$
\boxed{
\mathbf{E}
=
-\frac{\partial\mathbf{A}}{\partial t}
-
F_0\nabla u
+
\eta_0\left(J_0-J_{b0}\right)\hat{\mathbf e}_{\phi}
}
\tag{18.2}
$$

因此，在计算电场 $\mathbf{E}$ 时，背景环电压项始终被包含在内。


## 平行电场的表达式

JOREK 中实现的极向磁通 $\psi$ 方程（归一化形式）为

$$
\frac{1}{R^2}\frac{\partial\psi}{\partial t}
=
\frac{\eta}{R^2}
\left[
j-j_0-(j_b-j_{b0})
\right]
-
\frac{1}{R}[u,\psi]
-
\frac{F_0}{R^2}\frac{\partial u}{\partial\phi}
+
\frac{F_0^2}{R^2B^2}
\frac{\tau_{\mathrm{IC}}}{\rho}
\left[
\frac{1}{R}[p,\psi]
+
\frac{F_0}{R^2}\frac{\partial p}{\partial\phi}
\right].
\tag{18.3}
$$

此处已略去超电阻项，它对当前讨论并不重要。

然而，如上述讨论所示，物理上自洽、应当实现的形式是

$$
\frac{1}{R^2}\frac{\partial\psi}{\partial t}
=
\frac{\eta}{R^2}
\left(j-j_b\right)
-
\frac{\eta_0}{R^2}
\left(j_0-j_{b0}\right)
-
\frac{1}{R}[u,\psi]
-
\frac{F_0}{R^2}\frac{\partial u}{\partial\phi}
+
\frac{F_0^2}{R^2B^2}
\frac{\tau_{\mathrm{IC}}}{\rho}
\left[
\frac{1}{R}[p,\psi]
+
\frac{F_0}{R^2}\frac{\partial p}{\partial\phi}
\right].
\tag{18.4}
$$

对法拉第定律反旋，得到如下电场表达式：

$$
\mathbf{E}
=
-\frac{1}{R}
\frac{\partial\psi}{\partial t}
\hat{\mathbf e}_{\phi}
-
F_0\nabla u
+
\eta_0
\left(J_0-J_{b0}\right)
\hat{\mathbf e}_{\phi}.
$$

再做平行投影 $\hat{\mathbf b}\cdot(\ldots)$，即容易得到归一化形式的

$$
E_{\parallel}
=
-\frac{F_0}{B}
\left[
\frac{1}{R^2}\frac{\partial\psi}{\partial t}
+
\frac{1}{R}[u,\psi]
+
\frac{F_0}{R^2}\frac{\partial u}{\partial\phi}
+
\frac{\eta_0}{R^2}(j_0-j_{b0})
\right].
\tag{18.5}
$$

利用式 (18.4)，可将式 (18.5) 右端括号内的各项改写为另一种形式，由此得到如下归一化形式的平行电场表达式：

$$
E_{\parallel}
=
-\frac{F_0}{B}
\left[
\frac{\eta}{R^2}(j-j_b)
+
\frac{F_0^2}{R^2B^2}
\frac{\tau_{\mathrm{IC}}}{\rho}
\left(
\frac{1}{R}[p,\psi]
+
\frac{F_0}{R^2}\frac{\partial p}{\partial\phi}
\right)
\right].
\tag{18.6}
$$

或者，也可直接利用广义欧姆定律得到平行电场的表达式：

$$
\mathbf{E}
=
-\mathbf{v}\times\mathbf{B}
+
\eta(\mathbf{J}-\mathbf{J}_b)
+
\frac{\mathbf{J}\times\mathbf{B}-\nabla p_e}{ne}.
$$

因此，

$$
E_{\parallel}
=
\frac{\mathbf{E}\cdot\mathbf{B}}{B}
=
\frac{\eta(\mathbf{J}-\mathbf{J}_b)\cdot\mathbf{B}}{B}
-
\frac{\mathbf{B}\cdot\nabla p_e}{Bne}.
$$

其中

$$
\mathbf{B}\cdot\nabla p_e
=
\frac{1}{R}[p_e,\psi]
+
\frac{F_0}{R^2}\frac{\partial p_e}{\partial\phi},
$$

而取下述近似是稳妥的

$$
(\mathbf{J}-\mathbf{J}_b)\cdot\mathbf{B}
\approx
(J_\phi-J_{\phi,b})B_\phi
\approx
(J_\phi-J_{\phi,b})\frac{F_0}{R}.
$$

由此得到

$$
E_{\parallel}
=
\eta(J_\phi-J_{\phi,b})\frac{F_0}{BR}
-
\frac{1}{enB}
\left(
\frac{1}{R}[p_e,\psi]
+
\frac{F_0}{R^2}\frac{\partial p_e}{\partial\phi}
\right).
$$

对上述结果归一化，得到

$$
E_{\parallel}
=
-\frac{F_0}{B}
\left[
\frac{\eta}{R^2}(j-j_b)
+
\frac{\tau_{\mathrm{IC}}}{\rho}
\left(
\frac{1}{R}[p,\psi]
+
\frac{F_0}{R^2}\frac{\partial p}{\partial\phi}
\right)
\right].
\tag{18.7}
$$

因此，式 (18.5)、式 (18.6) 或式 (18.7) 均可用于在 JOREK 中计算 $E_{\parallel}$。

式 (18.6) 与式 (18.7) 的唯一差别在于一个并不太显著的因子

$$
\frac{F_0^2}{R^2B^2}.
$$
