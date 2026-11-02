---
title: "垂直稳定的主动控制器模型"
parent: "ASDEX Upgrade"
layout: default
render_with_liquid: false
---

# 垂直稳定的主动控制器模型 {#active-controller-model-for-vertical-stabilization}
JOREK 中加入了一个 PID 控制器，以便在含 $n=0$ 的自由边界模拟中实现主动稳定。

## 基本原理


它依据垂直轴位置及其在模拟中的演化，作用于特定线圈，规律为：

$$
\begin{align}
\Delta I &=  K_\text{P}\,e(t) + K_\text{D} \frac{\mathrm{d} e(t)}{\mathrm{d} t} + K_\text{I} \int_{t_0}^{t} e(t)
\end{align}
$$

其中 $e=Z(t)-Z_\text{ref}(t)$ 是对参考值的偏差，$K_\text{P}$、$K_\text{I}$、$K_\text{D}$ 分别为比例、积分和微分增益。

## 在 JOREK 中的实现

上式经离散化后写入 `vacuum/vacuum_response.dat` 中的 `coil_current_source` 例程，位置在 PF 线圈电流剖面插值之后。其形式如下：

$$
\begin{align}
\mathrm{d}Z_\text{err} &= Z_\text{axis}(t_n) - Z_\text{ref}(t_n)\\
\mathrm{d}Z_\text{der} &= \frac{Z_\text{axis}(t_n) - Z_\text{axis}(t_{n-1})}{\Delta t}\\
\mathrm{d}Z_\text{integral} +&= \left(Z_\text{axis}(t_n) - Z_\text{ref}(t_{n})\right)\Delta t \\\\
\Delta I &=   K_\text{P}\,\mathrm{d}Z_\text{err} + K_\text{D}\,\mathrm{d}Z_\text{der}   + K_\text{I} \,\mathrm{d}Z_\text{integral}\\
I(i) &=  I(i) + \mathrm{vert\\_FB\\_amp\\_ts}(i)\,\Delta I  
\end{align}
$$

其功能如下，相关参数列于下表：

- 在给定时刻之后启用控制器：`start_VFB_ts`
- 使用恒定参考值或输入剖面
- 设定节拍时间，即控制器起作用的周期间隔
- 逐个线圈设定电流上限
- 逐个线圈设定放大因子，以分配控制作用

只有指定了放大因子且已超过启动时刻，控制器才会启用。

## 参数

| 参数 | 说明 | 典型取值 |
| --- | --- | --- |
| `vert_FB_gain(1)` | 比例增益 $K_\text{P}$ | `1.e0`（视算例而定） |
| `vert_FB_gain(2)` | 微分增益 $K_\text{D}$ | `1.e0` |
| `vert_FB_gain(3)` | 积分增益 $K_\text{I}$ | `1.e0` |
| `start_VFB_ts` [$t_{\text{JOREK}}$] | 垂直反馈的启动时刻 | `-` |
| `vert_FB_amp_ts` | 各线圈的增益放大因子 | 上侧线圈 $>0$，下侧线圈 $<0$ |
| `I_coils_max` [A] | PF 线圈允许的最大电流 | 视算例而定 |
| `vert_FB_tact` [$t_{\text{JOREK}}$] | 仅周期性施加 VFB | 可选 |
| `Z_ref_ts(t)` | 参考轴位置的时间轨迹 | 视算例而定 |
| `vert_pos_file` [$t_{\text{JOREK}}$ \| m] | 随时间变化的轴位置的输入文件 | - |


## 如何指定输入剖面

位置可由下列任一方式给出：

- 输入剖面文件（`vert_pos_file`）
  - 时间以 [$t_{\text{JOREK}}$] 给出
  - 垂直位置以 [m] 给出
  - 当模拟时间长于剖面所覆盖的范围时，取剖面最后一个值作为参考。
- 输入参数 `Z_axis_ref`，该参数也用于自由边界平衡
- 若以上都未指定，则采用轴的初始值或重启值

## 调参
最优增益因算例而异，取决于平衡参数与使用场景。

通常，控制器启用后的最初几个时间步内轴会振荡。
可利用该振荡调整增益。此外，也可用目标值的突变（阶跃响应）来改进参数设置。

调参可分三步进行：

- 在其他增益为 0 的情况下增大 $K_\text{P}$，直到振荡幅度较小、阶跃响应下的超调也较小。若 $K_\text{P}$ 过大，响应会超调并使系统失稳。
- 增大 $K_\text{D}$ 以抑制振荡。
- 若稳态存在误差，则增大 $K_\text{I}$。（目前为止我未看到明显效果，仅用 $K_\text{P}$ 与 $K_\text{D}$ 增益时误差通常已很小。）


