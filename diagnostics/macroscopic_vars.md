---
title: "Macroscopic_vars.dat"
nav_order: 25
render_with_liquid: false
parent: "诊断与后处理"
---

该文件包含仿真中特定时间步的能量与增长率，可用 [plot_live_data.sh](plot_live_data.sh.md) 脚本绘制这些量随时间的变化。

格式为
   @rcs_version:  GIT revision        b575260-dirty
   @jorek_model:   303
   @n_tor:     3
   @n_plane:     8
   @n_period:     1

随后是各特定时刻的一系列数值
   @times:     1   1.000000000E+03
   @energies:  1.000000000E+03  2.012235987E-02  2.073465471E-22  1.291279331E-16  1.245421010E-19
   @growth_rates:  1.500000000E+03 -8.745715263E-13  6.921484349E-04  7.638978557E-06 -2.518593016E-06
