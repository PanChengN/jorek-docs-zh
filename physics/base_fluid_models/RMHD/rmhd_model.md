---
title: "RMHD 模型"
nav_order: 1
parent: "约化 MHD 模型"
grand_parent: "基础流体模型"
layout: default
render_with_liquid: false
---

# JOREK 约化 MHD 模型

另请参阅 [模型](../base_fluid_models.md)、[坐标](../../coordinates.md)、[符号](../../notation.md) 与 [归一化](../../normalization.md) 页面。

**注意：** 当前的 JOREK 模型假定 $F\equiv F_0$ 在空间与时间上均为常数。此处给出的推导对一般的 $F(R,Z,t)$ 成立，但后者必须与 $\phi$ 无关，以保证 $\nabla\cdot\mathbf{B}=0$。

## 定义

### 磁场

磁场未作归一化。满足 $\nabla\cdot\mathbf{B}=0$ 的 $\mathbf{B}$ 的一般形式为：

$$\begin{align*}
  \mathbf{B} &= \nabla\psi\times \nabla\phi + F~\nabla\phi = \frac{1}{R}(-\partial_1\psi~\mathbf{a}^2 + \partial_2\psi~\mathbf{a}^1)+F\mathbf{a}^3 \\
\end{align*}$$

其中 $F$ 与 $\psi$ 为标量，且 $\partial_3 F=0$ 以保证 $\nabla\cdot\mathbf{B}=0$。相对于归一化基矢的物理分量为：

$$\begin{align*}
  B_R &= +\frac{1}{R}\frac{\partial\psi}{\partial Z} \\
  B_Z &= -\frac{1}{R}\frac{\partial\psi}{\partial R} \\
  B_\phi &= +\frac{F}{R}
\end{align*}$$

极向磁通与矢势的关系为：

$$\begin{equation*}
\psi = R^2\mathbf{A}\cdot\nabla\phi = R A_\phi
\end{equation*}$$

关于[磁矢势的更多说明见此](expressions_and_derivations/mag_vec_pot.md)（与约化 MHD 方程的推导无关）。

### 电流

等离子体电流的[归一化](../../normalization.md)为 $\mathbf{j}_\text{SI}=\mathbf{j}/\mu_0$。环向电流密度 $j$（由于因子 R 的存在，它并非真正的电流密度）定义为

$$\begin{equation*}
  j \equiv - R~\mathbf{j}\cdot\mathbf{e}_\phi = - \mathbf{j}\cdot\mathbf{a}_3 = \Delta^\ast\psi
\end{equation*}$$

[推导概要见此](expressions_and_derivations/j_psi.md)。因此物理分量 $j_\phi$ 为

$$\begin{equation*}
  j_\phi = -\frac{j}{R} = -\frac{\Delta^\ast\psi}{R}
\end{equation*}$$

尽管未用 JOREK 变量表示，电流的 R 分量与 Z 分量同样存在（见[此处](expressions_and_derivations/j_psi.md)）：

$$\begin{align*}
  j_R &= +\frac{1}{R}\partial_2 F+\frac{1}{R^2}\partial_{1,3}\psi \\
  j_Z &= -\frac{1}{R}\partial_1 F+\frac{1}{R^2}\partial_{2,3}\psi
\end{align*}$$

### 速度

归一化（另见[归一化表](../../normalization.md)）：$\mathbf{v}_\text{SI}=\mathbf{v}/\sqrt{\mu_0~\rho_0}$。

##### 标准速度

$$\begin{equation*}
\begin{split}
\mathbf{v} &= -R^2\nabla u \times \mathbf{a}^3 + v_{||}\mathbf{B} \\
&= R(\partial_1 u~\mathbf{a}^2 - \partial_2 u~\mathbf{a}^1) + v_{||}\left[\frac{1}{R}(-\partial_1\psi~\mathbf{a}^2 + \partial_2\psi~\mathbf{a}^1)+F\mathbf{a}^3\right] \\
&= \left(-R\partial_2 u+\frac{v_{||}}{R}\partial_2\psi\right)\mathbf{a}^1 + \left(R\partial_1 u-\frac{v_{||}}{R}\partial_1\psi\right)\mathbf{a}^2+F~v_{||}\mathbf{a}^3
\end{split}
\end{equation*}$$

相对于归一化基矢的物理分量为：

$$\begin{align*}
  v_R    &= -R\partial_2 u+\frac{v_{||}}{R}\partial_2\psi \\
  v_Z    &= +R\partial_1 u-\frac{v_{||}}{R}\partial_1\psi \\
  v_\phi &= \frac{F~v_{||}}{R}
\end{align*}$$

##### 含抗磁分量的离子速度

$$\begin{equation*}
  \begin{split}
\mathbf{v} &= -R^2\nabla u \times \mathbf{a}^3 - \frac{\tau_{IC} R^2}{\rho}\nabla p_i\times\mathbf{a}^3 + v_{||}\mathbf{B} \\
&= R(\partial_1 u~\mathbf{a}^2 - \partial_2 u~\mathbf{a}^1) + v_{||}\left[\frac{1}{R}(-\partial_1\psi~\mathbf{a}^2 + \partial_2\psi~\mathbf{a}^1)+F\mathbf{a}^3\right] -\frac{\tau_{IC}R}{\rho} \left[ -\partial_1 p_i~\mathbf{a}^2 + \partial_2 p_i~\mathbf{a}^1 \right] \\
&= \left(-R\partial_2 u+\frac{v_{||}}{R}\partial_2\psi - \frac{\tau_{IC}R}{\rho}\partial_2 p_i\right)\mathbf{a}^1 + \left(R\partial_1 u-\frac{v_{||}}{R}\partial_1\psi + \frac{\tau_{IC}R}{\rho}\partial_1 p_i\right)\mathbf{a}^2+F~v_{||}\mathbf{a}^3
\end{split}
\end{equation*}$$

（稍后补充……）

### 涡量

总涡量 $\mathbf{W}$ 的环向分量为：

$$\begin{equation*}\begin{split}
\mathbf{W} \cdot \nabla \phi &= \nabla \cdot \left(\nabla_\text{pol}u +\frac{\tau_{IC}}{\rho} \nabla_\text{pol} p - v_{||} \frac{1}{R^2} \nabla_\text{pol} \psi \right)
\end{split}\end{equation*}$$

（推导见[此处](expressions_and_derivations/omega.md)）。

涡量的归一化为 $\mathbf{W}_\text{SI}=\mathbf{W}/\sqrt{\mu_0~\rho_0}$。

在代码中，编号为 4 的变量（记作 $\omega$）对应于总涡量的以下部分：

$$\begin{equation*}
  \omega \equiv \nabla \cdot \nabla_\text{pol}u = \Delta_\text{pol} u
\end{equation*}$$

### 电势

速度流函数 $u$ 与电势 $\Phi$ 的关系为
$$\begin{equation*}
  u\equiv \Phi/F_0
\end{equation*}$$
当 $F\equiv F_0$ 且电阻项较小时成立。[推导概要见此](expressions_and_derivations/u_phi.md)。

## 常用表达式

| 表达式 | 说明 |
|---|---|
| $\nabla\times\nabla\phi\equiv 0$ | |
| $\nabla\cdot\nabla\phi\equiv 0$ | |
| $\nabla a\cdot\nabla\phi=\frac{1}{R^2}\partial_3 a$ | 对任意标量 $a$、$b$ |
| $\Delta_\text{pol} u=\Delta^\ast u+\frac{2}{R}\partial_1 u$ | |
| $\nabla a\times\nabla\phi = \frac{1}{R}(\partial_2 a\mathbf{a}_1 - \partial_1 a\mathbf{a}_2)$ | |
| $\nabla\phi\times(\nabla a\times\nabla\phi)=\frac{1}{R^2}\nabla_\text{pol}a$ | |
| $(\nabla a\times\nabla\phi)\times(\nabla b\times\nabla\phi) = \frac{1}{R}[a,b]\nabla\phi$ | |
| $\nabla\times(\nabla a\times\nabla\phi)=-\Delta^\ast a\nabla\phi + \frac{1}{R^2}\nabla_\text{pol}\partial_3 a$ | |
| $\mathbf{B}\cdot\nabla a=\frac{F}{R^2}\partial_3 a+\frac{1}{R}[a,\psi]$ | |
| $\nabla a\cdot\nabla b = \nabla_\text{pol}a\cdot\nabla_\text{pol}b+\frac{1}{R^2}\partial_3 a\partial_3 b$ | |
| $\nabla\phi\cdot(\nabla C\times \nabla D)=\frac{1}{R}[C,D]$ | 对任意矢量 $\mathbf{C}$、$\mathbf{D}$ |
| $\mathbf{B}\cdot(\mathbf{C}\times\mathbf{D})=\frac{F}{R}[C,D]-\frac{C}{R}[\nabla\psi,D]+\frac{D}{R}[\nabla\psi,C]$ | |
| $\mathbf{j} \equiv \nabla F\times\nabla\phi + \frac{1}{R^2}\partial_3(\nabla_\text{pol}\psi)-\Delta^\ast\psi~\nabla\phi$ | [见此处](expressions_and_derivations/j_psi.md) |
| $j \equiv -\mathbf{j}\cdot\mathbf{a}_3=\Delta^\ast\psi$ | [见此处](expressions_and_derivations/j_psi.md) |
| $\mathbf{j}\times\mathbf{B}= -\frac{F}{R^2}\nabla_\text{pol}F+\frac{1}{R}\nabla\phi[F,\psi]-\frac{\Delta^\ast\psi}{R^2}\nabla_\text{pol}\psi+\frac{1}{R^2}\nabla_\text{pol}\partial_3\psi\times\mathbf{B}$ | [见此处](expressions_and_derivations/j_cross_b.md) |
| $\mathbf{v}\times\mathbf{B} = \frac{1}{R}\mathbf{a}_3 [\psi,u]+F\nabla_\text{pol} u$ | [见此处](expressions_and_derivations/v_cross_b.md) |

## 方程

### 连续性方程

$$\begin{equation}
  \partial_t\rho=-\nabla\cdot(\rho\mathbf{v})+\nabla\cdot(D\nabla\rho) + S_\rho
\end{equation}$$

[约化 MHD 形式的推导见此](expressions_and_derivations/continuity_eq.md)。

### 极向磁通方程

$$\begin{equation}
  \partial_t\psi=R[\psi,u]+\eta(T)(j-j_0)-F_0\partial_\phi u
\end{equation}$$

其中 $j_0$ 以电流源的方式实现。[推导概要见此](expressions_and_derivations/psi_eq.md)。

### 垂直动量方程

动量方程的垂直投影通过将算符 $\nabla\phi\cdot\nabla\times(R^2...)$ 作用于动量方程得到。

##### 标准方程

$$\begin{equation*}\begin{split}
\nabla\cdot\left[R^2\rho\nabla_{pol}\left(\frac{\partial U}{\partial t}\right)\right] = 
  &   \frac{1}{R} \left[R^4\rho\omega,U\right]
    - \frac{1}{2R} \left[R^2\rho,R^2\left|\nabla_{pol}U\right|^2\right] \\ 
  & - \frac{1}{R} \left[R^2,p\right] + \frac{1}{R} \left[\psi,j\right]
    - \frac{F_{o}}{R^2}\frac{\partial j}{\partial\phi} + \mu \nabla^2\omega
\end{split}\end{equation*}$$

##### 含抗磁分量的方程

本方程通过把 $\mathbf{v}_{pol} = R^2 \nabla\phi\times\nabla U$ 替换为
$$\mathbf{v}_{pol} = R^2\nabla\phi\times\nabla U + \frac{\tau_{IC}R^2}{\rho}\nabla\phi\times\nabla P_i$$
并去掉与陀螺黏性张量相消的项得到（见陀螺黏性相消，[Schnack, Phys. Plasmas 13, 058103, 2006]）。

$$\begin{equation*}\begin{split}
\nabla\cdot\left[R^2\rho\nabla_{pol}\left(\frac{\partial U}{\partial t}\right)\right] = 
  &   \frac{1}{R} \left[R^4\rho W,U\right]
    - \frac{1}{2R} \left[R^2\rho,R^2\left|\nabla_{pol}U\right|^2\right] \\ 
  & - \frac{1}{R} \left[R^4\tau_{IC}\nabla^{2}_{pol}P_{i},U\right]
    + \frac{1}{R} \left[R^4\frac{\tau_{IC}}{\rho}\nabla_{pol}\rho\cdot\nabla_{pol}P_{i},U\right] \\
  & + \tau_{IC}R^3\left[W,P_i\right]
    + \tau_{IC}R^2 \nabla\cdot\left(\frac{\partial P_i}{\partial Z}\nabla_{pol}U\right) \\ 
  & - \tau_{IC}R^3 \left[\partial_{xy}U  \left(\partial_{xx}P_i-\partial_{yy}P_i\right)
                        -\partial_{xy}P_i\left(\partial_{xx}U  -\partial_{yy}U  \right)\right] \\
  & - \frac{1}{R} \left[R^{2},p\right] + \frac{1}{R} \left[\psi,j\right]
    - \frac{F_{o}}{R^2}\frac{\partial j}{\partial\phi}
    + \mu \nabla^{2}\left(\omega + \omega^\ast\right)
\end{split}\end{equation*}$$

其中 $\omega^\ast$ 是涡量的抗磁部分（[定义见此](expressions_and_derivations/omega_star.md)）。
注意，在方程中包含 $\omega^\ast$ 非常重要。在代码中，我们把总涡量定义为

$$\begin{equation*}
  W = \omega + \omega^\ast
\end{equation*}$$

注意，在上述方程中引入这一新变量意味着必须从项 $\left[R^4\rho\omega,U\right]$ 中分离出 $\omega^\ast$。
理想情况下还需从项 $\tau_{IC}R^4[\omega,P_i]$ 中分离出 $\omega^\ast$，但这会产生 $\tau_{IC}^2$ 量级的项，该量级被认为足够小而可以忽略。所得方程为（采用总涡量 $W$ 的新定义）：

$$\begin{equation*}\begin{split}
\nabla\cdot\left[R^2\rho\nabla_{pol}\left(\frac{\partial U}{\partial t}\right)\right] = 
  &   \frac{1}{R} \left[R^4\rho W,U\right]
    - \frac{1}{2R} \left[R^2\rho,R^2\left|\nabla_{pol}U\right|^2\right] \\ 
  & - \frac{1}{R} \left[R^4\tau_{IC}\nabla^{2}_{pol}P_{i},U\right]
    + \frac{1}{R} \left[R^4\frac{\tau_{IC}}{\rho}\nabla_{pol}\rho\cdot\nabla_{pol}P_{i},U\right] \\
  & + \tau_{IC}R^3\left[W,P_i\right]
    + \tau_{IC}R^2 \nabla\cdot\left(\frac{\partial P_i}{\partial Z}\nabla_{pol}U\right) \\ 
  & - \tau_{IC}R^3 \left[\partial_{xy}U  \left(\partial_{xx}P_i-\partial_{yy}P_i\right)
                        -\partial_{xy}P_i\left(\partial_{xx}U  -\partial_{yy}U  \right)\right] \\
  & - \frac{1}{R} \left[R^{2},p\right] + \frac{1}{R} \left[\psi,j\right]
    - \frac{F_{o}}{R^2}\frac{\partial j}{\partial\phi}
    + \mu \nabla^{2}W
\end{split}\end{equation*}$$

### 平行动量方程

动量方程的平行投影通过将算符 $\nabla\phi\cdot (...)$ 作用于动量方程得到。

[推导见此。](expressions_and_derivations/velocity_equation.md)

##### 标准方程

$$\begin{equation*}\begin{split}
\rho \frac{\partial v_{\parallel}}{\partial t} = 
  & - R \rho \left[ u, v_{\parallel}\right] + \frac{1}{R} \rho v_{\parallel} \left[ \psi, v_{\parallel}\right] 
    - \frac{F_0}{R^2} \rho v_{\parallel} \partial_3 v_{\parallel}  \\
  & - \frac{1}{2R^2} \frac{1}{F_0} \frac{\partial}{\partial \phi} \left| \nabla \psi\right|^2 - \frac{1}{F_0} \frac{\partial p}{\partial \phi}
\end{split}\end{equation*}$$

### 能量方程
*(稍后补充……)*

### 电流定义方程
*(稍后补充……)*

### 涡量定义方程
*(稍后补充……)*
