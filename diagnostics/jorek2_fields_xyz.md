---
title: "jorek2_fields_xyz"
nav_order: 27
render_with_liquid: false
parent: "General"
---

# jorek2_fields_xyz

本程序读取 JOREK 重启文件，并计算任意 (x,y,z) 点处的磁场。与 jorek2_postroc 的不同之处在于，即使在 JOREK 网格之外也能得到场值。例如，可用它从 JOREK 重启文件生成 GEQDSK 文件。

要得到完整的场，**必须以完全自由边界模式（含 n=0 模）运行模拟**。否则无法得知等离子体区域之外的真空场。关于如何以自由边界模式运行，参见[此处](jorek-starwall-faqs.md)。若算例以 freeboundary=.f. 运行，则只能得到等离子体电流产生的场。

它涉及等离子体内昂贵的体积分计算，因此对于大算例应使用多个 MPI 进程并行运行。提交与 JOREK 相同的作业脚本即可（只需把 "jorek_modelXXX" 换成 "jorek2_fields_xyz"。编译时只需输入

   make -j 8 jorek2_fields_xyz

作为输入，必须在文件 xyz.nml 中以笛卡尔坐标给出各点，格式为

   number_of_points
   x_1       y_1       z_1  
   x_2       y_2       z_2  
    :         :         :   
    :         :         :   
   x_n       y_n       z_n  

切勿把点正好指定在 STARWALL 的线圈/壁面三角形上。否则这些点处可能出现奇异性！

要选择给定的 JOREK 重启文件，请创建一个名为 steps.nml 的文件，第一行写 3 个整数（istart, iend, delta_step）。例如要读取从 100 到 520、间隔 10 步的重启文件，只需在 steps.nml 中写入这一行

   100  520  10

场输出到文件 "fields_xyz.dat"，并按线圈/壁面/等离子体贡献分别列出。 

注意，为计算所需的等离子体场，n_plane 通常应大于 60（即使是二维情形）
