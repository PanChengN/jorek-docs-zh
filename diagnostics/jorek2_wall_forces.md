---
title: "jorek2_wall_forces"
nav_order: 32
render_with_liquid: false
parent: "General"
---

# jorek2_wall_forces

本程序读取 JOREK 重启文件并计算总壁力。**必须以完全自由边界模式（含 n=0 模）运行模拟**。否则无法得知等离子体区域之外的真空场。关于如何以自由边界模式运行，参见[此处](jorek-starwall-faqs.md)。 

它涉及等离子体内昂贵的体积分计算，因此对于大算例应使用多个 MPI 进程并行运行。提交与 JOREK 相同的作业脚本即可（只需把 "jorek_modelXXX" 换成 "jorek2_wall_forces"。编译时只需输入

   make -j 8 jorek2_wall_forces

更新 30.11.22 新的输入文件 

要选择给定的 JOREK 重启文件，请创建一个名为 wall_forces.nml 的文件
，格式如下
   &wall_forces
   istart     = 100  ! start index of restart file
   iend       = 1000 ! end index of restart file
   delta_step = 40   ! 
   scale_fact = 1.01 ! scaling factor of wall (1.01 default)
   n_phi_int  = 64   ! number of points for integration in the toroidal direction (to get B-field)
   
   /
力输出到 total_wall_forces_istart..iend..scale_fact.dat 文件

对于较旧的版本，wall_forces.nml 只需一行 istart iend delta_step：
   0 1000 100
结果保存在 total_wall_forces.dat 中

重要：为计算总壁力，需对包含 STARWALL 壁面的闭合曲面做积分（[本文中的公式 7](https://iopscience.iop.org/article/10.1088/1741-4326/aa8876/meta)）。该例程假定描述该曲面的三角形具有给定的排列顺序，而该曲面是 STARWALL 壁面的缩放版本。因此，取决于 STARWALL 中该顺序是如何确定的，三角形法向可能反号，计算出的力也随之反号。TODO：在例程中强制法向始终朝外，以确保总力的符号正确
