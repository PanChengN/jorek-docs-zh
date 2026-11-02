---
title: "掠射角下的平行速度平滑"
nav_order: 3
parent: "边界条件"
grand_parent: "物理选项"
layout: default
render_with_liquid: false
---

## 掠射角下 Vpar 边界条件的平滑

可使用平滑函数来平滑平行速度边界条件（Mach=1）中的跳变，这类跳变出现在 $\mathbf{B} \cdot \mathbf{n} \approx 0$ 的位置。更多信息见 [1]（第 2.1.1 小节）。

要使用该功能，请在输入文件中加入 `vpar_smoothing`，并为 `vpar_smoothing_coef(1)`、`vpar_smoothing_coef(2)` 和 `vpar_smoothing_coef(3)` 设置合适的值。以下是 [1] 中使用的示例：

```fortran
vpar_smoothing = .t.
vpar_smoothing_coef(1) = 0.02     ! B.n/B at which the transition takes place
vpar_smoothing_coef(2) = 0.016    ! width for transition the vpar = 0 --> vpar=cs
vpar_smoothing_coef(3) = 0.005754 ! offset to make vpar=0 at 0 degrees
```
[1] [F J Artola et al 2021 Plasma Phys. Control. Fusion 63 064004](https://iopscience.iop.org/article/10.1088/1361-6587/abf620)
