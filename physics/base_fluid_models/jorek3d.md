---
title: "仿星器约化 MHD"
nav_order: 3
parent: "基础流体模型"
grand_parent: "物理模型"
layout: default
render_with_liquid: false
---

# 仿星器约化 MHD 模型

JOREK 仿星器模型（约化 MHD）包含两个不同的模型：

1. **Model 180** 不对等离子体作时间演化，只根据 VMEC/GVEC 计算**初始条件**。
2. **Model 183** 真正**对等离子体作时间演化**（沿用与 model 180 相同的硬编码编译参数）。

这些模型包含若干硬编码开关，例如是否包含平行速度 $v_{\parallel}$。

关于 JOREK 原始仿星器模型实现的详细描述可参见以下文献：

1. N. Nikulsin. [Models and methods for nonlinear magnetohydrodynamic simulations of stellarators](https://mediatum.ub.tum.de/?id=1624218) (2021), PhD thesis, TUM.
2. R. Ramasamy [Equilibrium and initial value problem simulation studies of nonlinear magnetohydrodynamics in stellarators](https://mediatum.ub.tum.de/?id=1686004) (2022), PhD thesis, TUM. 此处尤其重要的是第 7 章。 
3. N. Nikulsin et al. [JOREK3D: An extension of the JOREK nonlinear MHD code to stellarators](https://doi.org/10.1063/5.0087104), Physics of Plasmas 29.6 (2022). 
4. R. Ramasamy et al. [Nonlinear MHD modeling of soft beta limits in W7-AS](https://doi.org/10.1088/1741-4326/ad56a1), Nucl. Fusion 64 086030 (2024).

## 仿星器模型方程

我们把磁场拆分为真空部分 $\nabla\chi$ 与由等离子体中电流产生的部分 $\vec B_p$：
$$\vec B = \nabla\chi + \vec B_p.$$
于是可以为真空场构造 Clebsch 坐标 $(\psi_v,\beta_v,\chi)$，按定义它必须满足
$$\nabla\chi = \nabla\psi_v\times\nabla\beta_v.$$
现在，若只考虑等离子体感应场 $\vec B_p$，则其矢势可写为：
$$\vec A_p = A_\chi\nabla\chi + A_{\psi_v}\nabla\psi_v,$$
其中已利用规范自由度消去 $\nabla\beta_v$ 分量。于是令 $A_\chi = \Psi$、$A_{\psi_v} = \Omega$，总磁场为
$$\vec B = \nabla\chi + \nabla\Psi\times\nabla\chi + \nabla\Omega\times\nabla\psi_v.$$

如文献 [1] 所示，任意速度场均可写为：
$$
\newcommand{\vpar}{v_\parallel}
\newcommand{\pgrad}{\nabla^\perp}
\vec v = \frac{\nabla\Phi\times\nabla\chi}{B_v^2} + \vpar\vec B + \pgrad\zeta,
$$
其中 $B_v = \Vert\nabla\chi\Vert$，$\nabla^\perp = \nabla - B_v^{-2}\nabla\chi\nabla\chi\cdot\nabla$。

将这些假设代入电阻 MHD 方程（如[基础流体模型](base_fluid_models.md)页面所示）后，我们把法拉第定律投影到 $\nabla\psi_v$ 与 $\nabla\chi$ 上，并对动量方程施加如下投影算符：
$$
\begin{gathered}
\nabla\chi\cdot\nabla\times(B_v^{-2} \\
\vec B\cdot \\
\nabla\chi\cdot\nabla\times(B_v^{-2}\nabla\times
\end{gathered}
$$
由此得到以下**全 MHD** 方程：
$$
\newcommand{\tderiv}[1]{\frac{\partial#1}{\partial t}}
\newcommand{\llderiv}{\partial^\parallel}
\newcommand{\psderiv}{\partial_{\psi_v}}
\newcommand{\pLap}{\Delta^\perp}
\begin{aligned}
&\left[\psi_v,\tderiv{\Psi}\right] = \left[\frac{[\Psi,\Phi]-\llderiv\Phi}{B_v},\psi_v\right] - \frac{F_v}{B_v}\left[\Omega,\frac{[\psi_v,\Phi]}{B_v}\right]_{\psi_v} + \llderiv(F_v\psderiv\zeta) + \left[(\zeta,\Psi),\psi_v\right] - \frac{F_v}{B_v}\left[\Omega,(\zeta,\psi_v)\right]_{\psi_v} + \frac{1}{B_v}\nabla\cdot(\eta\nabla\psi_v\times\vec j), \\
\\
&\left[\tderiv{\Omega},\psi_v\right] = -\left[\Omega,\frac{[\psi_v,\Phi]}{B_v}\right] + \left[\psi_v,\frac{[\Omega,\Phi]}{B_v}\right] - 2(B_v,\zeta) - B_v\pLap\zeta - \left[\Omega,(\zeta,\psi_v)\right] + \left[\psi_v,(\zeta,\Omega)\right] + \frac{1}{B_v}\nabla\cdot(\eta\nabla\chi\times\vec j), \\
\\
&\nabla\cdot\left[\frac{\rho}{B_v^2}\pgrad\tderiv{\Phi} + \rho\tderiv{}(\vpar\pgrad\Psi) - \frac{\rho}{B_v}\tderiv{}(\vpar\llderiv\Omega)\nabla\psi_v\right] - B_v\left[\frac{\rho}{B_v^2},\tderiv{\zeta}\right] = \frac{B_v}{2}\left[\frac{\rho}{B_v^2},v^2\right] + B_v\left[\frac{\rho\omega^\chi}{B_v^4},\Phi\right] \\
&- \nabla\cdot(\rho \vpar\vec\omega^\perp) + B_v\left[\frac{\rho \vpar\omega^\chi}{B_v^2},\Psi\right] + B_v\left[\frac{\rho \vpar\omega^{\psi_v}}{B_v^2},\Omega\right] + \nabla\cdot\left(\frac{\rho\omega^\chi}{B_v^2}\pgrad\zeta - \frac{P}{B_v^2}\pgrad\Phi - P\vpar\pgrad\Psi + \frac{P\vpar\llderiv\Omega}{B_v}\nabla\psi_v\right) \\
&- B_v\left[\frac{\rho\vpar\vec\omega\cdot\nabla\Omega}{B_v^2},\psi_v\right] + B_v\left[\frac{P}{B_v^2},\zeta\right] + \nabla\cdot\left(\frac{B^\chi}{B_v^2}\vec j - \frac{j^\chi}{B_v^2}\vec B\right) + B_v\left[\frac{1}{B_v^2},p\right] + \nabla\cdot(\mu_\perp\pgrad\pLap\Phi), \\
\\
&\rho\left(\tderiv{\Phi},\Psi\right) - \rho\frac{F_v}{B_v}\llderiv\Omega\psderiv\tderiv{\Phi} + \rho B^2\tderiv{\vpar} + \frac{\rho\vpar}{2}\tderiv{B^2} + \rho B_v\left[\tderiv{\zeta},\Psi\right] + \rho F_v\left[\tderiv{\zeta},\Omega\right]_{\psi_v} = -\frac{\rho B_v}{2}\llderiv v^2 \\
&- \frac{\rho B_v}{2}\left[v^2,\Psi\right] - \frac{\rho F_v}{2}\left[v^2,\Omega\right]_{\psi_v} - \frac{\rho\omega^\chi}{B_v}\llderiv\Phi - \frac{\rho\omega^\chi}{B_v}\left[\Phi,\Psi\right] - \frac{\rho\omega^\chi F_v}{B_v^2}\left[\Phi,\Omega\right]_{\psi_v} + \frac{\rho B^\chi}{B_v^2}\vec\omega\cdot\nabla\Phi - \rho\vec\omega\cdot(\nabla\zeta\times\nabla\chi) \\
&+ \rho\omega^\chi(\Psi,\zeta) - \rho\vec\omega\cdot\nabla\Omega F_v\psderiv\zeta + \rho\omega^{\psi_v}(\Omega,\zeta) - \vec v\cdot\vec B~P - B_v\llderiv p - B_v\left[p,\Psi\right] - F_v\left[p,\Omega\right]_{\psi_v} + \nabla\cdot(\mu_\parallel\nabla_\perp\vpar + \mu_{\parallel,\parallel}\nabla_\parallel\vpar), \\
\\
&B_v\left[\frac{\rho}{B_v^2},\tderiv{\Phi}\right] + B_v\left[\rho\tderiv{\vpar},\Psi\right] + B_v\left[\rho \vpar,\tderiv{\Psi}\right] - B_v\left[\frac{\rho}{B_v}\tderiv{}(\vpar\llderiv\Omega),\psi_v\right] + \nabla\cdot\left(\rho\pgrad\tderiv{\zeta}\right) \\
&= -\nabla\cdot\left(\frac{\rho}{2}\pgrad v^2 + \frac{\rho\omega^\chi}{B_v^2}\pgrad\Phi - \frac{\rho \vpar B^\chi}{B_v^2}\nabla\chi\times\vec\omega + \frac{\rho \vpar\omega^\chi}{B_v^2}\nabla\chi\times\vec B\right) + B_v\left[\frac{\rho\omega^\chi}{B_v^2},\zeta\right] - B_v\left[\frac{P}{B_v^2},\Phi\right] \\
&- B_v\left[P\vpar,\Psi\right] + B_v\left[\frac{P\vpar\llderiv\Omega}{B_v},\psi_v\right] - \nabla\cdot\left(P\pgrad\zeta + \frac{B^\chi}{B_v^2}\nabla\chi\times\vec j - \frac{j^\chi}{B_v^2}\nabla\chi\times\vec B\right) - \pLap p + \nabla\cdot(\mu_\zeta\pgrad\pLap\zeta), \\
\\
&\tderiv{\rho} = - B_v\left[\frac{\rho}{B_v^2},\Phi\right] - B_v\llderiv(\rho \vpar) - B_v[\rho \vpar,\Psi] - F_v[\rho \vpar,\Omega]_{\psi_v} - \nabla\cdot(\rho\pgrad\zeta) + P, \\
\\
&\tderiv{p} = - \frac{1}{B_v}\left[p,\Phi\right] - \vpar B_v\llderiv p - \vpar B_v\left[p,\Psi\right] - \vpar F_v \left[p,\Omega\right]_{\psi_v} - (\zeta,p) - \gamma p B_v\left[\frac{1}{B_v^2},\Phi\right] - \gamma p B_v\llderiv \vpar - \gamma p B_v\left[\vpar,\Psi\right] \\
&- \gamma p F_v\left[\vpar,\Omega\right]_{\psi_v} - \gamma p\pLap\zeta + \nabla\cdot\vec q + (\gamma-1)(S_e + \eta j^2),
\end{aligned}
$$
其中 $[f,g] = \nabla\chi\cdot(\nabla f\times\nabla g)/B_v$ 与 $[f,g]_{\psi_v} = \nabla\psi_v\cdot(\nabla f\times\nabla g)/\Vert\nabla\psi_v\Vert$ 为泊松括号，$(f,g) = \pgrad f\cdot\pgrad g$ 为内积，$\nabla_\parallel = B^{-2}\vec B\vec B\cdot\nabla$，$\nabla_\perp = \nabla - \nabla_\parallel$。本推导除假定电阻 MHD 成立之外未作任何进一步假设，但我们向投影后的动量方程加入了通用黏性项。这些通用黏性项并不能准确刻画等离子体中的黏性效应，但在避免数值不稳定时往往很有用。

### 约化 MHD

JOREK 中实际实现的方程是**约化 MHD** 方程，要由上述**全 MHD** 方程得到它们还需再走一步：令 $\Omega = 0$、$\zeta = 0$，并从上述完整方程组中去掉 $\Omega$ 与 $\zeta$ 的演化方程。为守恒能量，还必须从 $\Psi$ 演化方程中去掉 $\vec j$ 垂直于 $\nabla\chi$ 的分量。得到的**约化 MHD** 方程如下：
$$
\newcommand{\red}[1]{{\color{red}#1}}
\newcommand{\blue}[1]{{\color{blue}#1}}
\begin{aligned}
B_v\tderiv{\Psi} &= \llderiv\Phi - \left[\Psi,\Phi\right] - \eta\frac{j^\chi}{B_v} \blue{+ \eta^{(h)} B_v\pLap\left(\frac{j^\chi}{B_v^2}\right)}, \\
\nabla\cdot\left[\frac{\rho}{B_v^2}\pgrad\tderiv{\Phi} \red{+ \rho\tderiv{}(\vpar\pgrad\Psi)}\right] &= \frac{B_v}{2}\left[\frac{\rho}{B_v^2},v^2\right] + B_v\left[\frac{\rho\omega^\chi}{B_v^4},\Phi\right] - \nabla\cdot(\rho \vpar\vec\omega^\perp) + B_v\left[\frac{\rho \vpar\omega^\chi}{B_v^2},\Psi\right] \\
&- \nabla\cdot\left(\frac{P}{B_v^2}\pgrad\Phi \red{+ P\vpar\pgrad\Psi}\right) - \nabla\cdot\left(\frac{j^\chi}{B_v^2}\vec B\right) + B_v\left[\frac{1}{B_v^2},p\right] + \nabla\cdot(\mu_\perp\pgrad\pLap\Phi) \blue{- \mu_\perp^{(h)}\Delta^2\pLap\Phi}, \\
\red{\rho\left(\tderiv{\Phi},\Psi\right)} + \rho B^2\tderiv{\vpar} + \frac{\rho\vpar}{2}\tderiv{B^2} &= -\frac{\rho B_v}{2}\llderiv v^2 - \frac{\rho B_v}{2}\left[v^2,\Psi\right] \red{- \frac{\rho\omega^\chi}{B_v}\llderiv\Phi - \frac{\rho\omega^\chi}{B_v}\left[\Phi,\Psi\right] + \rho\vec\omega\cdot\nabla\Phi} - (\red{(\Phi,\Psi)} + \vpar B^2)P \\
&- B_v\llderiv p - B_v\left[p,\Psi\right] + \nabla\cdot(\mu_\parallel\nabla_\perp\vpar + \mu_{\parallel,\parallel}\nabla_\parallel\vpar) \blue{- \mu_\parallel^{(h)}\Delta^2\vpar}, \\
\tderiv{\rho} &= - B_v\left[\frac{\rho}{B_v^2},\Phi\right] - B_v\llderiv(\rho \vpar) - B_v[\rho \vpar,\Psi] + P, \\
\tderiv{p} &= - \frac{1}{B_v}\left[p,\Phi\right] - \vpar B_v\llderiv p - \vpar B_v\left[p,\Psi\right] - \gamma p B_v\left[\frac{1}{B_v^2},\Phi\right] - \gamma p B_v\llderiv \vpar - \gamma p B_v\left[\vpar,\Psi\right] \\
&+ \nabla\cdot\vec q + (\gamma-1)(S_e + \eta j^2) \blue{- \kappa_\perp^{(h)}\Delta^2 T},
\end{aligned}
$$
其中 $j^\chi = \nabla\chi\cdot\vec j = -\nabla\cdot(B_v^2\pgrad\Psi)/\mu_0$，$\omega^\chi = \nabla\chi\cdot\vec\omega = -\pLap\Phi \red{- \nabla\cdot(B_v^2\vpar\pgrad\Psi)}$。

这些方程（不含标红的项）在 **model 183** 中实现。还可以进一步约化：令 $\vpar = 0$，并从上述方程组中去掉 $\vpar$ 的演化方程。这通过在编译 JOREK 之前于硬编码参数中设置 `with_vpar = .false.` 实现。反之，当 `with_vpar = .true.` 时会求解上述全部方程，且不对 $\vpar$ 作任何假设。请注意，若 `with_vpar = .false.`，所有标红项本来也不会产生贡献。

我们还向原始方程加入了超电阻率、超黏性与超导率项（标蓝）。这些项不刻画任何物理效应，但有时是抑制数值不稳定的必要手段。若使用这些项，应确保其足够小，以免影响物理结果。

## 真空场

### Dommaschk 势

*待补充*

### 有限元 Laplace 求解

*待补充*

## GVEC 导入

*待补充*