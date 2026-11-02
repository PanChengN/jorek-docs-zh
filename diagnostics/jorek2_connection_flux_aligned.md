---
title: "Jorek2_connection_flux_aligned"
nav_order: 23
render_with_liquid: false
parent: "General"
---

## Jorek2_connection_flux_aligned

#### 概述
JOREK 中已有若干 jorek2_connection 的实现，可输出 VTK 格式的磁力线结果。本诊断是其中一个修改版本，它输出按磁面平均的连接长度——定义为磁力线在撞击给定边界（通常为壁面）之前所走过的距离。这样便可用于生成沿径向平均的 $\Psi_N-t$ 图，以评估遍历性与平行输运。

#### 运行代码
运行方式为

  ```
  mpirun -np X jorek2_connection_flux_aligned < ./input_file
  ```
 
#### 输出

输出生成：

- connections.txt：连接长度的单条磁力线数据。
- strikes.txt：各条磁力线在 (R, Z, phi) 中的最终位置。初始温度与归一化极向磁通被保存下来，作为起点的度量。同时记录连接长度以及一个布尔量 in_domain，它表示该磁力线是否已撞到所定义的边界。
- poinc_R-Z.dat/poinc_rho-theta.dat：基于磁力线追踪的庞加莱图。经验表明，庞加莱图最好使用 jorek2_poincare 生成，因为要得到统计上显著的连接长度数据所需的磁力线条数太多，难以画出好的庞加莱图。

#### 程序设置
算例目录中的 connect.nml 文件用于为该例程设置参数：
  &connect_params
   n_turns     = 150                          ! number of toroidal turns to follow a fieldline
   n_phi       = 1000                         ! number of steps per toroidal turn
   tol         = 1.d-6                        ! tolerance when stepping from element to element
   phi_start   = 0.0                          ! starting toroidal angle
   ntheta      = 200                          ! number of poloidal starting points on each flux surface
   n_rcoord       = 21                           ! number of radial starting points on each flux surface
   rcoord_range_min = 0.001                     ! minimum psi normalised
   rcoord_range_max = 0.999                     ! maximum psi normalised (< 0.999)
   rcoord_strike_bnd = 999.0                    ! Boundary to define strike points on (if psin>psin_max then the simulation boundary is used)
   /
