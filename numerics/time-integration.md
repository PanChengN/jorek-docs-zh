---
title: "时间积分"
nav_order: 3
parent: "数值方法与工具"
layout: default
render_with_liquid: false
---

# 时间积分 

对形如

$$
\frac{\partial \mathbf{A(u)}}{\partial t} = \mathbf{B}(\mathbf{u},t) \tag{1}
$$

的方程组，其时间积分可用如下一般形式离散（参见 Beam80 与 Hirsch91 第 11.1 章）

$$
(1+\xi) \, \mathbf{A}^{n+1} - (1+2\xi) \, \mathbf{A}^{n} + \xi \, \mathbf{A}^{n-1}
= \Delta t \left[
\theta \, \mathbf{B}^{n+1}
+ (1 - \theta - \phi) \, \mathbf{B}^{n}
- \phi \, \mathbf{B}^{n-1}
\right] \tag{2}
$$

当 $\phi+\theta-\xi = 1/2$ 时，该形式保证二阶精度。形如 $\mathbf{B}^n$ 的上标表示相应表达式是在哪个时间步上求值的。

线性化

$$
\mathbf{H}^{n+1} \approx \mathbf{H}^n + \left[ \frac{\partial \mathbf{H}}{\partial \mathbf{u}} \right]^n \cdot \delta \mathbf{u}^n \tag{3}
$$

其中 $\mathbf{H} = \mathbf{A}$ 或 $\mathbf{H} = \mathbf{B}$。该线性化见参考文献 Hirsch91 第 11.3 章，它允许把式 (2) 改写为如下形式，其中取 $\phi = 0$。

$$
\begin{split}
  (1+\xi)\left[\mathbf{A}^n+\left(\frac{\partial \mathbf{A}}{\partial \mathbf{u}}\right)^n\delta\mathbf{u}^n\right]
    -(1+\xi)\mathbf{A}^n-\xi\mathbf{A}^n+\xi\mathbf{A}^{n-1} \\
    =\Delta t\left[\theta\left(\mathbf{B}^n+\left(\frac{\partial \mathbf{B}}{\partial \mathbf{u}}\right)^n\delta\mathbf{u}^n\right)
      +(1-\theta)\mathbf{B}^n\right] 
\end{split} \tag{4}
$$

此处，

$$
  \delta\mathbf{u}^n \equiv \mathbf{u}^{n+1}-\mathbf{u}^n \tag{5}
$$

经若干化简，并使用后向线性化

$$
  \mathbf{H}^{n-1}\approx \mathbf{H}^n-\left[\frac{\partial \mathbf{H}}{\partial \mathbf{u}}\right]^n\cdot\delta\mathbf{u}^{n-1}, \tag{6}
$$

可得

$$
  \boxed{
    \left[(1+\xi)\left(\frac {\partial \mathbf{A}}{\partial \mathbf{u}}\right)^n-\Delta t\theta\left(\frac{\partial \mathbf{B}}{\partial \mathbf{u}}\right)^n\right]\delta\mathbf{u}^n
      =\Delta t\mathbf{B}^n+\xi\left(\frac{\partial \mathbf{A}}{\partial \mathbf{u}}\right)^n\delta\mathbf{u}^{n-1}
  }, \tag{7}
$$

这就是 JOREK 中实现的时间积分格式。某些参数取值对应众所周知的时间积分方法，如表 1 所列。参数 $\xi$ 在代码中记作 ''zeta''。

| $\theta$ | $\xi$ | 方法 | 输入参数 `time_evol_scheme` |
|----------|------|--------|------------------------------------|
| 1/2 | 0 | **Crank-Nicolson 格式（默认）** | `"Crank-Nicholson"` |
| 1 | 1/2 | **BDF2（Gears）格式** | `"Gears"` |
| 1 | 0 | 隐式 Euler 格式（通常不使用） | `"implicit Euler"` |

具体而言，项 $(\partial\mathbf{A}/\partial{\mathbf{u}})\cdot\delta\mathbf{u}$ 与 $(\partial\mathbf{B}/\partial{\mathbf{u}})\cdot\delta\mathbf{u}$ 导致如下表达式变换：

$$
\begin{aligned}
  g                             &~~\rightarrow~~ \delta g               \\
  g^2                           &~~\rightarrow~~ 2\;g\;\delta g         \\
  g\;h                          &~~\rightarrow~~ g\;\delta h+h\;\delta g\\
  \frac{\partial g}{\partial x}                 &~~\rightarrow~~ \frac{\partial (\delta g)}{\partial x} \\
  \left(\frac{\partial g}{\partial x}\right)^2  &~~\rightarrow~~ 2\;\frac{\partial g}{\partial x}\;\frac{\partial (\delta g)}{\partial x}
\end{aligned} \tag{8}
$$

此处 $g$ 与 $h$ 表示任意变量，$x$ 表示任意坐标。例如 $\partial j/\partial\phi$ 变为 $\partial(\delta j)/\partial\phi$。

## 广义方程

考虑形如

$$
\sum_i a_i(\mathbf{u},t)\frac{\partial \mathbf{A}_i( \partial\mathbf{u})}{t} = \mathbf{B}(\mathbf{u},t), \tag{9}
$$

的方程组，其中 $a_i$ 一般可以是空间微分算子。对此类方程可以导出与 (2) 类似的离散（取 $\phi=0$）。

先考虑显式（前向）与隐式（后向）Euler 格式。两种情形下时间导数 $\partial\mathbf{A}/\partial t$ 都替换为差商 $(\mathbf{A}^{n+1}-\mathbf{A}^n)/\Delta t$，其余各项在显式 Euler 中于时间步 $n$ 取值，在隐式 Euler 中于时间步 $n+1$ 取值：

$$
\begin{aligned}
&\text{Explicit:}\qquad &&\sum_i a_i^n (\mathbf{A}_i^{n+1}-\mathbf{A}_i^n) = \Delta t\mathbf{B}^n, \\
&\text{Implicit:}\qquad &&\sum_i a_i^{n+1} (\mathbf{A}_i^{n+1}-\mathbf{A}_i^n) = \Delta t\mathbf{B}^{n+1}.
\end{aligned} \tag{10}
$$

Crank-Nicolson 格式就是两种 Euler 格式的平均：

$$
\sum_i (\frac{1}{2}a_i^{n+1}+\frac{1}{2}a_i^n)(\mathbf{A}_i^{n+1}-\mathbf{A}_i^n) = \Delta t(\frac{1}{2}\mathbf{B}^{n+1}+\frac{1}{2}\mathbf{B}^n). \tag{11}
$$

另一方面，BDF2 格式通过在 $\mathbf{A}_i^{n+1}$ 附近对 $\mathbf{A}_i^n$ 与 $\mathbf{A}_i^{n-1}$ 作 Taylor 展开，得到时间步 $n+1$ 处时间导数的二阶近似：

$$
\mathbf{A}_i^n = \mathbf{A}_i^{n+1} - \Delta t\left(\frac{\partial \mathbf{A}_i}{\partial t}\right)^{n+1} + \frac{(\Delta t)^2}{2}\left(\frac{\partial^2\mathbf{A}_i}{\partial t^2}\right)^{n+1} + ... \\
\mathbf{A}_i^{n-1} = \mathbf{A}_i^{n+1} - 2\Delta t\left(\frac{\partial \mathbf{A}_i}{\partial t}\right)^{n+1} + 2(\Delta t)^2\left(\frac {\partial^2 \mathbf{A}_i}{\partial t^2}\right)^{n+1} + ... \tag{12}
$$

将上述两式都对一阶时间导数求解，可得

$$
\begin{aligned}
&(*)\qquad &&\left(\frac{\partial \mathbf{A}_i}{\partial t}\right)^{n+1} = \frac{\mathbf{A}_i^{n+1}-\mathbf{A}_i^n+\frac{1}{2}\Delta t\left(\frac{\partial^2 \mathbf{A}_i}{\partial t^2}\right)^{n+1}}{\Delta t}, \\
&(**)\qquad &&\left(\frac{\partial \mathbf{A}_i}{\partial t}\right)^{n+1} = \frac{\mathbf{A}_i^{n+1}-\mathbf{A}_i^{n-1}+2\Delta t\left(\frac{\partial^2 \mathbf{A}_i}{\partial t^2}\right)^{n+1}}{2\Delta t}.
\end{aligned} \tag{13}
$$

由此得到

$$
\left(\frac{\partial \mathbf{A}_i}{\partial t}\right)^{n+1} = a(*)+b(**) = \frac{(a+\frac{1}{2}b)\mathbf{A}_i^{n+1}-a\mathbf{A}_i^n-\frac{1}{2}b\mathbf{A}_i^{n-1}+(\frac{1}{2}a+b)\Delta t\left(\frac{\partial^2 \mathbf{A}_i}{\partial t^2}\right)^{n+1}}{\Delta t}, \tag{14}
$$

其中 $a+b=1$。为获得二阶精度，施加条件 $\frac{1}{2}a+b=0$，于是 $a=2$、$b=-1$。在时间步 $n+1$ 处计算式 (9)，并代入时间步 $n+1$ 处 $\partial\mathbf{A}/\partial t$ 的二阶近似，即得 BDF2 格式：

$$
\sum_i a_i^{n+1} (\frac{3}{2}\mathbf{A}_i^{n+1}-2\mathbf{A}_i^n+\frac{1}{2}\mathbf{A}_i^{n-1}) = \Delta t\mathbf{B}^{n+1}. \tag{15}
$$

将式 (10)、(11) 与 (15) 推广，可以写成：

$$
\sum_i [\theta a_i^{n+1} + (1-\theta)a_i^n][(1+\xi)\mathbf{A}_i^{n+1} - (1+2\xi)\mathbf{A}_i^n + \xi\mathbf{A}_i^{n-1}] = \Delta t[\theta\mathbf{B}^{n+1} + (1-\theta)\mathbf{B}^n]. \tag{16}
$$

代入表 1 中相应的 $\theta$ 与 $\xi$ 取值，即可由式 (16) 得到 Crank-Nicolson、BDF2 与隐式 Euler 格式。

### 参考文献
  * **[Beam80]** Beam, R.M. and Warming, R.F. Alternating direction implicit methods for parabolic equations with a mixed derivative. SIAM Journal on Scientific and Statistical Computing, 1(1), 131 (1980). ISSN 01965204. [[http://dx.doi.org/10.1137/0901007|doi:10.1137/0901007]]
  * **[Hirsch91]**: Hirsch, C. Numerical computation of internal and external flows. Volume 1: Fundamentals of Numerical Discretization. J. Wiley, Chichester (1991). ISBN 9780471923855.
