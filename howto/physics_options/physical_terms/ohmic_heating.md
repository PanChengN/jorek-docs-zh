---
title: "含欧姆加热运行"
nav_order: 4
parent: "物理项激活"
grand_parent: "物理选项"
layout: default
render_with_liquid: false
---

## 模型 199/303/333/400/**600**

默认情况下，仿真中欧姆加热项处于关闭状态。**但需注意，这会破坏能量守恒**。开启后，电子能量方程中加入以下项
$$
\eta_{ohm}  \, j_{ohm}^2
$$
其中 $j_{ohm}=j-j_{RE}$ 为欧姆电流密度，$\eta_{ohm}$ 为等离子体电阻率。注意，在方程的电子压力形式中必须补上因子 ($\gamma-1$)。

在输入文件中添加以下参数即可包含欧姆加热项：

```ini
# Setting normal resistivity in electric field equation
eta           = 1.d-7
T_max_eta     = 1.d99

# Setting resistivity for the ohmic heating term
eta_ohmic     = 1.d-7
T_max_eta_ohm = 1.d99
```

`eta_ohmic` 是欧姆加热项中所用的平衡等离子体芯部电阻率值，单位为 JOREK 单位。
电阻率 `eta` 的任何温度依赖都会自动复制到 `eta_ohmic`。用于设置欧姆加热电阻率的参数与[电场方程中的 $\eta$ 项](../plasma_functions_and_coefficients/spitzer_resistivity.md)类似（只是加上后缀 "_ohmic"）。只要 `eta` 与 `eta_ohmic` 不同，就会出现一条警告信息，因为此时磁能未能正确转化为热能。


## 模型 710/711/712

与模型 199/303/333/400/600 类似，full MHD 模型也可以通过输入文件中的 `eta_ohmic` 参数包含欧姆加热项。

full MHD 模型中欧姆加热项的实现与约化 MHD 模型不同。为此需要磁矢量势的二阶导数，这要求扩展 $\phi$ 方向的 Fourier 谱方法，使其包含基函数的二阶导数。

电流矢量 $\boldsymbol{J} = \nabla \times \boldsymbol{B}$ 的各分量为：

$$
\begin{align*}
J_R ={}& \frac{\partial B_\phi}{\partial Z} - \frac{1}{R}\frac{\partial B_Z}{\partial \phi} \\
J_Z ={}& \frac{1}{R} \left(\frac{\partial B_R}{\partial \phi} - \frac{\partial (R B_\phi)}{\partial R} \right) \\
J_\phi ={}& \frac{\partial B_Z}{\partial R} - \frac{\partial B_R}{\partial Z}
\end{align*}
$$

这些分量可以进一步改写为 $\boldsymbol{J} = \nabla \times \nabla \times \boldsymbol{A}$：

$$
\begin{align*}
J_R ={}&
\left(
\frac{\partial^2 A_Z}{\partial Z \partial R}
- \frac{\partial^2 A_R}{\partial Z^2}
+ \frac{1}{R} \frac{\partial F}{\partial \psi} \frac{\partial \psi}{\partial Z}
\right)
- \frac{1}{R^2}
\left(
\frac{\partial^2 A_R}{\partial \phi^2}
- \frac{\partial^2 \psi}{\partial \phi \partial R}
\right)
\\[0.5em]
J_Z ={}&
\frac{1}{R^2}
\left(
\frac{\partial^2 \psi}{\partial \phi \partial Z}
- \frac{\partial^2 A_Z}{\partial \phi^2}
\right)
-
\left(
\frac{\partial^2 A_Z}{\partial R^2}
- \frac{\partial^2 A_R}{\partial R \partial Z}
+ \frac{1}{R} \frac{\partial F}{\partial \psi} \frac{\partial \psi}{\partial R}
- \frac{F}{R^2}
\right)
\\
&-
\frac{1}{R}
\left(
\frac{\partial A_Z}{\partial R}
- \frac{\partial A_R}{\partial Z}
+ \frac{F(\psi)}{R}
\right)
\\[0.5em]
J_\phi ={}&
\frac{1}{R}
\left(
\frac{\partial^2 A_R}{\partial R \partial \phi}
- \frac{\partial^2 \psi}{\partial R^2}
\right)
-
\frac{1}{R^2}
\left(
\frac{\partial A_R}{\partial \phi}
- \frac{\partial \psi}{\partial R}
\right)
-
\frac{1}{R}
\left(
\frac{\partial^2 \psi}{\partial Z^2}
- \frac{\partial^2 A_Z}{\partial Z \partial \phi}
\right)
\end{align*}
$$

关于实现的细节，请见：[ohmic_heating_in_fmhd.pdf](assets/ohmic_heating/ohmic_heating_in_fmhd.pdf)
