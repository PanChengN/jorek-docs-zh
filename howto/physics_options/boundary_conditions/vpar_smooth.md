---
title: "掠射角下的平行速度平滑"
nav_order: 3
parent: "边界条件"
grand_parent: "物理选项"
layout: default
render_with_liquid: false
---

<!-- untranslated-notice -->
<div class="warning" markdown="1">
**本页尚未翻译**，以下为 JOREK 官方英文原文。

原文页面：[Vpar smoothing at grazing angles](https://iterorganization.github.io/JOREK/howto/physics_options/boundary_conditions/vpar_smooth.html)　·　源文件：`howto/physics_options/boundary_conditions/vpar_smooth.md`
</div>

## Vpar boundary condition smoothing at grazing angles

A smoothing function can be applied to smooth the jumps in parallel velocity boundary condition (Mach=1), which happens where $\mathbf{B} \cdot \mathbf{n} \approx 0$. More information can be found in [1] (subsection 2.1.1).

To use this function, include `vpar_smoothing` in your input file and set proper values for `vpar_smoothing_coef(1)`, `vpar_smoothing_coef(2)` and `vpar_smoothing_coef(3)`. Here is an example used in [1]:

```fortran
vpar_smoothing = .t.
vpar_smoothing_coef(1) = 0.02     ! B.n/B at which the transition takes place
vpar_smoothing_coef(2) = 0.016    ! width for transition the vpar = 0 --> vpar=cs
vpar_smoothing_coef(3) = 0.005754 ! offset to make vpar=0 at 0 degrees
```
[1] [F J Artola et al 2021 Plasma Phys. Control. Fusion 63 064004](https://iopscience.iop.org/article/10.1088/1361-6587/abf620)
