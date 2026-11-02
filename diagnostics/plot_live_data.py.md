---
title: "Reads and plot ''macroscopic_vars.dat''"
nav_order: 15
render_with_liquid: false
parent: "Running JOREK"
---

#### 读取并绘制 ''macroscopic_vars.dat''
本脚本是 [plot_live_data.sh](plot_live_data.sh.md) 的 Python 版本，用于 `gnuplot` 不稳定时（例如使用 x-terminal 时）。

用法：
```
plot_live_data.py
```
选项：
```
  -h, --help  show this help message and exit
  -legend     Print legend
  -q Q        Plot given quantity
  -f F        File name
  -l          List plottable quantities
  -ps         Save plot into eps file
  -nology     Linear y axis
```
