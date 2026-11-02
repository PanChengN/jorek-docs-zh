---
title: "含动理学逃逸电子运行"
nav_order: 8
parent: "动理学逃逸电子"
layout: default
render_with_liquid: false
---

# 在 kinetic_main 上入门全动理学逃逸电子（进行中，2026 年 2 月，Chizhou） 

本工作基于 kinetic_develop 分支[动理学框架简介](./../particle_introduction.md)，其中逃逸电子超级粒子以全轨道演化，并与流体等离子体耦合。可执行文件 kinetic_main 的编译方法见[动理学框架简介](./../particle_introduction.md)，其过程与 jorek2_main 类似。Strumpack 求解器已可用于动理学模拟。JOREK 中动理学模型的更一般介绍见[粒子](./../particle.md)

# 初始化逃逸电子

除 jorek_restart.h5 之外，任何带粒子的模拟都需要一个 part_restart.h5 文件。没有粒子重启文件时，kinetic_main 的运行方式与 jorek2_main 相同。初始化指南见[在相空间中初始化粒子](./../initialization.md)。作为起点，particles/examples 中的 ''test_initialisation_phase_space'' 是初始化逃逸电子的良好示例，其中能量、投掷角和环向坐标谱在指定区间内均匀初始化，而极向分布可设为跟随流体重启文件 ''jorek_equilibrium_restart.h5'' 中的电流密度。

**注意：** 这些示例脚本现已过时。在最新的 kinetic_main 中，''group%id'' 应为三个字母，而脚本中为 "001"。你需要编辑粒子重启文件中的 group id。 

# 运行 main_kinetic

''main_kinetic'' 的运行方式与 ''jorek2_main'' 类似，但它**只能**从 ''jorek_restart.h5'' **和** ''part_restart.h5'' 重启，而不能用 ''restart=.f.'' 创建新的平衡。除粒子重启文件外，还需在 namelist 中添加粒子组的一些额外信息（同样参见[动理学框架简介](./../particle_introduction.md)）。下面给出一个逃逸电子专用的示例。可将其加到流体 namelist 的末尾：

```
 restart_particles = .true.                                 ! If false, run as pure fluid without REs
 ! Particle properties in new format
 part_group_configs(1)%id                          = 'REs'  ! group id you give when initializing particles, MUST be 3 letters
 part_group_configs(1)%Z                           = -1
 part_group_configs(1)%coupling_scheme             = 'rep'  
 part_group_configs(1)%type                        = 'particle_kinetic_relativistic'
 part_group_configs(1)%n_particles                 = 1e6    ! number of super particles
 part_group_configs(1)%mass                        = 0.000548579870184805     
 part_group_configs(1)%num_re                      = 1.175403e16      ! number of physical REs, doesn't work if initialized according to current
 part_group_configs(1)%use_kin_recombination       = .false.

! Projecting (particle field -> MHD) smoothing
 filter_hyper        = 1.d-9
 filter_hyper_n0  = 1.d-9
 filter_par            = 5.d-1
 filter_par_n0       = 5.d-1
```

引入粒子时，通过保持总电流一致，部分欧姆电流会自动转换为由粒子携带的逃逸电子电流[逃逸电子](./runaway_electrons.md)。这可能引入噪声，因此建议先在不引入新物理的情况下运行一段时间，使流体模型趋于平滑。若要构造电流完全由逃逸电子携带的情形，可将 ''eta'' 设为较大值，并将 ''particles/mod_fields.f90'' 第 199 行的 ''E=0''，这样欧姆电流会衰减，而逃逸电子不会被人为感生的电场加速。   



   


