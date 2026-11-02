---
title: "测试用简化平衡"
nav_exclude: true
parent: "ASDEX Upgrade"
layout: default
render_with_liquid: false
---

# 测试用简化平衡

## 大长径比撕裂模测试算例（"intear"）

- R0=10m，a=1m（圆形截面）
- 以下信息应足以确定该测试算例：

```text
rho  = const = 1
T    = 0.0497 - 0.0393 * PsiN
Btor = F0/R with F0=10
PsiN = a1*r + a2*r^2 + (1-a1-a2)*r^3 mit a1=-0.062829 und a2=1.84896
q    = 1.71001 + 0.64087 PsiN + 1.81974 PsiN^2 - 2.49093 PsiN^3 + 2.29412 PsiN^4
Psi_axis = -0.20266
Psi_bnd  = 0
n0   = 6*10^19 m^-3
rho0 = 2*10^-7 kg/m^3 -> sqrt(mu0 rho0)=5e-7 is the JOREK time normalization
```

- 柱近似下取：`Btor = 1` 与 `R = 10`
- rho 与 T 的归一化见[此处](../physics/normalization)
- 详细比较时需要约定的细节：eta、visco、ZK_par、ZK_perp、D_perp 等

<!-- ## 为 Isabel 准备的内扭曲模平衡

- [jorek-input-aug-like-fixed-boundary-equilibrium-for-isabel-with-q0-larger-than-1.tar.gz](assets/asdex_upgrade/jorek-input-aug-like-fixed-boundary-equilibrium-for-isabel-with-q0-larger-than-1.tar.gz)
- [current_profile_for_isabel.dat.tar.gz](assets/asdex_upgrade/current_profile_for_isabel.dat.tar.gz)
- [rminor_profile_for_isabel.dat.tar.gz](assets/asdex_upgrade/rminor_profile_for_isabel.dat.tar.gz) -->
