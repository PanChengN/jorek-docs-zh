---
title: "含抗磁漂移运行"
nav_order: 1
parent: "物理项激活"
grand_parent: "物理选项"
layout: default
render_with_liquid: false
---

# 含抗磁漂移项运行

- 抗磁漂移项目前在模型 303、333、400、500、555 以及 **600** 中实现。
- 要开启这些项，在 namelist 输入文件中把输入参数 `tauIC` 设为正确的值：

$$
\tau_\text{IC} = \frac{m_\text{ion}}{2e\,F_0\sqrt{\mu_0\rho_0}}
$$

- 该表达式假定 $T_\text{ion}=T_\text{el}$，分母中的因子 2 即由此而来。
- 默认情况下抗磁项处于关闭状态：`tauIC` 预置为零。
- 按上述定义，`tauIC` 输入参数始终按单温度模型的形式给出。

## 示例

对 $n_0=10^{20}\,\mathrm{m}^{-3}$、$F_0=4.2$ 的 ASDEX Upgrade 氘等离子体，`tauIC` 的正确取值为 $3.8\times10^{-3}$：

$$
\begin{aligned}
\mu_0 &= 4\pi\times10^{-7}\,\mathrm{N}\,\mathrm{A}^{-2}, \\
e &= 1.6022\times10^{-19}\,\mathrm{C}, \\
m_D &= 3.344\times10^{-27}\,\mathrm{kg}, \\
\rho_0 &= 3.344\times10^{-7}\,\mathrm{kg}\,\mathrm{m}^{-3}, \\
\sqrt{\mu_0\rho_0} &= 6.5\times10^{-7}.
\end{aligned}
$$

对氘等离子体，该表达式可写为：

$$
\tau_\text{IC} = \frac{1.61\times10^8}{F_0\sqrt{n_0}}.
$$

## 一些估算

- **抗磁速度**为 $\mathbf{v}_\text{dia}=-(\nabla p\times\mathbf{B})/(qnB^2)$，其大小为 $v_\text{dia}=|\nabla p|/(qnB)$，其中 $q$ 为粒子电荷，$n$ 为粒子数密度。
- **抗磁频率**由 $\tau_\text{dia}=v_D/C$ 给出，其中 $C\approx2\pi r$ 为所考虑磁面的极向周长。在 ASDEX Upgrade 等离子体边界处，$C\approx4\,\mathrm{m}$。
