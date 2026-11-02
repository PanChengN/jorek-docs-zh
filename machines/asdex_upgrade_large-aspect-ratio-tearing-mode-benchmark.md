---
title: "大长径比撕裂模基准算例"
nav_exclude: true
parent: "ASDEX Upgrade"
layout: default
render_with_liquid: false
---

# 大长径比撕裂模基准算例

- 圆形等离子体
- `eta` 在整个计算域内为常数
- 无 `visco`
- 密度恒为 $7.24\cdot10^{19}m^{-3}$（氘）
- 对 JOREK 归一化：
  - $\rho_0=n_0\cdot m_D=7.24\cdot10^{19}m^{-3}\cdot3.34\cdot10^{-27}kg=2.42\cdot10^{-7}kg\,m^{-3}$
  - $\sqrt{\mu_0\rho_0}=5.5\cdot10^{-7}$
  - $\sqrt{\mu_0/\rho_0}=2.3$

## 长径比 10 的算例

### Beta ~ 0 的算例

- 来自 Erika 的信息（Cotrans 输出）：[tearcirc_ar10_beta0.tar.gz](assets/asdex_upgrade/tearcirc_ar10_beta0.tar.gz)
- 运行所需：
  - $R=10m$
  - $a=1m$
  - $\Psi_{axis}-\Psi_{bnd}=1.2495 Wb$
  - $F_{pol}=-1.2495\Psi_N$
    - $FF'=-1.2495\Psi_N$
  - $F_0\approx9.969$，即 $B_{tor}\approx1T$
  - [作为 Psi_N 函数的 q 剖面](assets/asdex_upgrade/q_tearcirc_ar10_b0.dat.gz)
    - $q=1.8\dots4.09$

<!-- - 增长率比较：

| eta | CASTOR3D | Q.Yu | JOREK | Flexi |
| --- | -------- | ---- | ----- | ----- |
|     |          |      |       |       | -->
