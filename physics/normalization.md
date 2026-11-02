---
title: "归一化"
nav_order: 2
parent: "物理模型"
layout: default
render_with_liquid: false
---

# JOREK 中的归一化

* 下标 "SI" 表示以 SI 单位给出的量，而 JOREK 单位下的量不写下标。
* 注意：重要的归一化因子 $\sqrt{\mu_{0}/\rho_{0}}$ 与 $\sqrt{\mu_{0}\rho_{0}}$ 会写入 JOREK 日志文件，以便查阅。 
* 注意：只有设置了输入参数 `central_density` 与 `central_mass`，这些数值才是正确的。 

## SI 单位与归一化单位之间的换算

| 物理量 | 物理单位（SI） | 换算关系 | 说明 |
| :--- | :--- | :--- | :--- |
| 大半径 | $R_{SI}[m]$ | $=R$ | 大半径 |
| 竖直坐标 | $Z_{SI}[m]$ | $=Z$ | 竖直坐标 |
| 磁场矢量 | $B_{SI}[T]$ | $=B$ | 磁场矢量 |
| 电场矢量 | $E_{SI}[Vm^{-1}]$ | $=E/\sqrt{\mu_{0}\rho_{0}}$ | 电场矢量 |
| 极向磁通 | $\Psi_{SI}[Tm^{2}]$ | $=\Psi$ | 极向磁通 |
| 环向电流密度 | $j_{\phi,SI}[Am^{-2}]$ | $=-j/(R~\mu_{0})$ | 环向电流密度；$j_{\phi,SI}=j_{SI}\cdot\hat{e}_{\phi}$ |
| 逃逸电子数密度 | $n_{r,SI}[m^{-3}]$ | $=n_{r}(\frac{1}{eR})\sqrt{\frac{\rho_{0}}{\mu_{0}}}$ | 逃逸电子数密度 |
| 逃逸电子平行动量 | $P_{\parallel,SI}[kg~m~s^{-1}]$ | $=P_{\parallel}m_{e0}c$ | 逃逸电子平行动量 |
| 粒子密度 | $n_{SI}[m^{-3}]$ | $=\rho~n_{0}$ | 粒子密度（$\rho$ 为归一化密度剖面，应作为输入给出） |
| 杂质数密度 | $n_{imp,SI}[m^{-3}]$ | $=\rho_{imp}\;n_{0}\;\mu_{imp}$ | 杂质数密度 |
| 质量密度 | $\rho_{SI}[kg~m^{-3}]$ | $=\rho~\rho_{0}$ | 质量密度 = 离子质量 X 粒子密度 |
| 杂质质量密度 | $\rho_{imp,SI}[kg/m^{3}]$ | $=\rho_{imp}\rho_{0}$ | 杂质质量密度 |
| 温度 | $T_{SI}[K]$ | $=T/(k_{B}\mu_{0}n_{0})$ | 温度：电子温度 + 离子温度 |
| 温度（eV） | $T_{eV}[eV]$ | $=T/(e~\mu_{0}n_{0})$ | 以 eV 表示的温度 |
| 极向电流流函数 | $FF_{SI}^{\prime}[T^{2}m^{2}/(Weber/rad)]$ | $=FF^{\prime}$ | 极向电流流函数 $F=RB_{\phi}$ ${}^{\prime}=d/d\psi$ |
| 等离子体压强 | $p_{SI}[Nm^{-2}]$ | $=\rho~T/\mu_{0}$ | 等离子体压强 |
| 速度矢量 | $v_{SI}[ms^{-1}]$ | $=v/\sqrt{\mu_{0}\rho_{0}}$ | 速度矢量 |
| 平行速度分量 | $v_{\parallel,SI}[ms^{-1}]$ | $=v_{\parallel}\cdot B_{SI}/\sqrt{\mu_{0}\rho_{0}}$ | 平行速度分量，其中 $B_{SI}=\vert B_{SI}\vert $ |
| 速度流函数 | $u_{SI}[ms^{-1}]$ | $=u/\sqrt{\mu_{0}\rho_{0}}$ | $Ru$ 为速度流函数，$F_0 u$ 为势 |
| 环向涡量 | $\omega_{\phi,SI}[m^{-1}s^{-1}]$ | $=\omega/\sqrt{\mu_{0}\rho_{0}}$ | 环向涡量 |
| 时间 | $t_{SI}[s]$ | $=t\cdot\sqrt{\mu_{0}\rho_{0}}$ | 时间 |
| 增长率 | $\gamma_{SI}[s^{-1}]$ | $=\gamma/\sqrt{\mu_{0}\rho_{0}}$ | 增长率；$\gamma_{SI}=\ln[E_{SI}(t_{2})/E_{SI}(t_{1})]/[2\Delta t_{SI}]$ 能量 $E_{SI}[J]$ |
| 电阻率 | $\eta_{SI}[\Omega m]$ | $=\eta\cdot\sqrt{\mu_{0}/\rho_{0}}$ | 电阻率，另见关于 Spitzer 电阻率的说明 |
| 超电阻率 | $\eta_{num,SI}[\Omega m^{2}]$ | $=\eta_{num}\cdot\sqrt{\mu_{0}/\rho_{0}}$ | 超电阻率 |
| 动力黏性 | $\mu_{SI} [kg~m^{-1}s^{-1}]$ | $=\mu\cdot\sqrt{\rho_{0}/\mu_{0}}$ | 动力黏性 |
| 超黏性 | $\mu_{num,SI}[kg~ms^{-1}]$ | $=\mu_{num}\cdot\sqrt{\rho_{0}/\mu_{0}}$ | 超黏性 |
| 运动黏性 | $\nu_{SI}[m^{2}s^{-1}]$ | $=\mu_{SI}/\rho_{SI}$ | 运动黏性（$\rho_{SI}$ 为局部质量密度，单位 $kg~m^{-3}$） |
| 粒子扩散系数 | $D_{SI}[m^{2}s^{-1}]$ | $=D/\sqrt{\mu_{0}\rho_{0}}$ | 粒子扩散系数（\parallel 或 $\perp$）；通常 $D_{\parallel}=0$ |
| 热扩散系数 | $K_{SI}[kg~m^{-1}s^{-1}]$ | $=K\cdot\sqrt{\rho_{0}/\mu_{0}}/(\gamma-1)$ | 热扩散系数（\parallel 或 $\perp$），其中 $\chi_{SI} [m^{2}s^{-1}]=K_{SI}/\rho_{SI}$ 且 $\kappa_{SI} [m^{-1}s^{-1}]=n_{SI}\chi_{SI}$ |
| 热源 | $S_{T,SI}[Wm^{-3}]$ | $=S_{T}/((\gamma-1)\mu_{0}\sqrt{\mu_{0}\rho_{0}})$ | 热源 |
| 粒子源 | $S_{\rho,SI}[kg~s^{-1}m^{-3}]$ | $=S_{\rho}\cdot\sqrt{\rho_{0}/\mu_{0}}$ | 粒子源 |
| 壁电阻率 | $\eta_{wall,thin,SI} [\Omega]$ | $=\eta_{wall,thin}\cdot\sqrt{\mu_{0}/\rho_{0}}$ | 壁电阻率（与 JOREK-STARWALL 相关）；$\eta_{wall,thin,SI} [\Omega] = \eta_{wall,SI} [\Omega m] / d_{wall} [m]$。例如 ITER：$8\cdot10^{-7}\Omega m / (6cm) = 1.33\cdot10^{-5}\Omega$ |
| 电离／复合速率 | $R_{ion/rec,SI}[m^{-3}s^{-1}]$ | $=R_{ion/rec}/(\sqrt{\mu_{0}\rho_{0}}n_{0})$ | 电离与复合速率 |
| 电离能 | $E_{ion,SI}[J]$ | $=\xi_{ion}/((\gamma-1)\mu_{0}n_{0})$ | 电离能 |
| 辐射速率 | $L_{rad,SI}[Wm^{3}]$ | $=L_{rad}/((\gamma-1)\mu_{0}\sqrt{\mu_{0}\rho_{0}}n_{0}^{2}\frac{m_{i}}{m_{imp}})$ | 辐射速率（model501） |
| 辐射功率密度 | $P_{rad,SI}[Wm^{-3}]$ | $=P_{rad}/((\gamma-1)\mu_{0}\sqrt{\mu_{0}\rho_{0}})$ | 辐射功率密度（model501） |
| 粒子电荷 | $q_{SI}[As]$ | $=q\sqrt{\rho_{0}/\mu_{0}}$ | 粒子电荷 |
| 新经典摩擦速率 | $\mu_{neo,SI}[s^{-1}]$ | $=\mu_{neo}/\sqrt{\rho_{0}\mu_{0}}$ | 新经典摩擦速率 |

## 其中已定义：

* **$n_{0}[m^{-3}]$**: $= \text{central\\_density } 10^{20}$。central_density 在 `preset_parameters.f90` 中有默认值，应在输入文件中指定。
* **$\rho_{0}[kg~m^{-3}]$**: $= \text{central\\_mass}*m_{AMU}*n_0$。central_mass 在 `preset_parameters.f90` 中有默认值，应在输入文件中指定。 
* **$\gamma$**: $= \text{GAMMA}$。GAMMA 在 `preset_parameters.f90` 中的默认值为 $5/3$。 
* **$\mu_{imp}$**: `m_i_over_m_imp` $= m_{i}/m_{imp}$。由杂质种类确定。

## 常用常数：

* $m_{e0}=0.911\cdot10^{-30}kg$
* $m_{AMU}=1.661\cdot10^{-27}kg$
* $m_{deuterium}=2.014101777811AMU$
* $m_{tritium}=5.007\cdot10^{-27}kg$
* $\mu_{0}=4\cdot\pi\cdot10^{-7}Vs/(Am)$
* $e=1.602176565\cdot10^{-19}C$
