---
title: "jorek2_four"
nav_order: 28
render_with_liquid: false
parent: "General"
---

## jorek2_four

程序 `jorek2_four`（`make jorek2_four`）可对文件
`jorek_restart.rst` 中所含的数据进行二维傅里叶分析。傅里叶分析在磁坐标下进行。

      jorek2_four < jorek-inputfile

通过在当前目录中放置 namelist 文件 `four_params.nml`，可修改部分数值参数。包含最重要参数及默认值的 namelist 文件如下：

              &four_params
                nstpts      = 30   ! Number of radial points
                deltaphi    = 0.3  ! Step size in toroidal direction
                rad_range = 0.001, 0.999 ! Radial range of normalized psi
              /

参数 `deltaphi` 的取值应使由磁力线追踪在每个磁面上获得约 200 至 1000 个点。还有一些其他参数通常无需修改（详见代码）。

- 输出写入 ASCII 文件 `Flux_modes_n000`，可方便地用 `gnuplot` 或 `xmgrace` 绘图。

- 主程序实现在 `diagnostics/jorek2_four.f90` 中，核心例程位于 `diagnostics/mod_fourier.f90`。

- 实现细节：
  - 代码采用 OpenMP 并行。
  - 首先在磁场的轴对称分量中进行磁力线追踪，起始点数目由参数 `nstpts` 给定。
  - 对每个磁面确定固定数目的极向点（由极向模数 `m_pol_range` 决定）。这些点在极向磁角 $\theta_{mag}$ 上等距分布。
  - 物理量被插值到这些等距点上后再作傅里叶变换。变换使用 FFTW。
  - 在 namelist 中设置 `debug = .true.` 时，会生成额外的调试输出，有助于查找问题。
