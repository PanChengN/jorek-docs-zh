---
title: "含动理学中性粒子与杂质运行"
nav_order: 8
parent: "中性粒子与杂质"
layout: default
render_with_liquid: false
---

# 含动理学中性粒子与杂质运行
本教程说明如何在 JOREK 仿真中引入动理学中性粒子和/或杂质。假定用户已熟悉如何单独运行 JOREK 算例，参见 [[running_jorek_for_the_first_time|首次运行 JOREK]]。

## 1. 可执行文件与输入文件
目前只能在名为 kinetic_develop 的分支上进行仿真（该分支将合并到 develop）。检出该分支，在 **`Makefile.inc`** 中选择 **`model600`**，并用你偏好的模型设置编译 kinetic_main。需要注意的是，使用这些粒子运行需要选项 `with_vpar=.true.`。该模型同时支持单温与双温设置，也支持 `ntor=1` 或更高值。

原子物理过程的反应速率从 OpenADAS 文件中提取，本教程所需的文件见：

插值背景场需要形式为 jorek_restart.h5 的 JOREK 重启文件。

# 2. 引入中性粒子
要引入氘种类的中性粒子，需在 namelist 中加入以下行：
```
restart_particles =.f.
tstep_particles = 5.d-7

deuterium_adas = .t.
```
其中 `tstep_particles` 定义粒子步长（每个流体步）以秒计，`restart_particles` 表示没有可用的粒子重启文件。否则设为 .t. 并准备好 **`part_restart.h5`**。将 `deuterium_adas=.t.` 设为 X。

我们定义阀门，并在由多边形或圆定义的阀门内部初始化粒子：
```
valves(1)%type = "poly"
valves(1)%poly_R = 3.86d0, 3.9d0, 3.86d0, 3.9d0
valves(1)%poly_Z = 0.1d0,  0.1d0,  0.0d0, 0.0d0
```
接下来初始化氘粒子组，给出 id（可自由选择）、电荷数、原子质量、耦合方案、要分配的粒子数以及粒子类型：
```
! Deuterium Neutrals (D01)
part_group_configs(1)%id = "D01"
part_group_configs(1)%Z = -2                             ! JOREK convention charge number for kinetic D
part_group_configs(1)%mass = 2.01410174369812            ! atomic mass in AMU
part_group_configs(1)%coupling_scheme = "ncs"            ! Neutral Coupling Scheme
part_group_configs(1)%n_particles = 1e4
part_group_configs(1)%type = "particle_kinetic_leapfrog" ! only supported type for neutrals and impurities
part_group_configs(1)%atom_data_suffix = "12_h"          ! ending of corresponding adas .dat files
```

要选择引入哪些原子物理过程：
```
part_group_configs(1)%use_kin_puffing = .t.
part_group_configs(1)%use_kin_cx = .t.
part_group_configs(1)%use_kin_ionisation = .t.
part_group_configs(1)%use_kin_recombination = .t.
part_group_configs(1)%use_kin_radiation = .t.
```

对于粒子–壁相互作用，此处选择反射：
```
part_group_configs(1)%wall_act_configs(1)%type = "reflection"
```

背景流体也会与壁相互作用，并可产生新的中性粒子：
```
fluid_configs(1)%Z=-2
fluid_configs(1)%wall_act_configs(1)%type="wall recomb"
fluid_configs(1)%wall_act_configs(1)%target_group_id="D01"
fluid_configs(1)%wall_act_configs(1)%supers_num_wall=200
```

D 从阀门注入的模式/速率由下式设定：
```
part_group_configs(1)%puff_ctrl(1)%times = 0.
part_group_configs(1)%puff_ctrl(1)%rates = 1.d20 !< constant puffing rate
part_group_configs(1)%puff_ctrl(1)%supers_num_puff = 40
```

现在照常运行 JOREK，但这次使用 kinetic_main。本教程所需的文件见：

我们稍微复杂化一点，引入中性粒子间碰撞：
```
part_group_configs(1)%use_kin_neutral_coll   = .t.
part_group_configs(1)%neutral_coll_dTw = 2.d-10, 273, 0.66
```

# 3. 引入杂质
在下面的示例中，我们将引入氮杂质（与前面描述的中性粒子一起），从与氘相同的阀门播撒。与中性粒子类似，在 namelist 中设置：
```
! Nitrogen Impurities (N01)
part_group_configs(2)%id = "N01"
part_group_configs(2)%Z = 7
part_group_configs(2)%mass = 14.0067396163940
part_group_configs(2)%coupling_scheme = "ics"
part_group_configs(2)%n_particles     = 1e4
part_group_configs(2)%type            = "particle_kinetic_leapfrog"

part_group_configs(2)%use_kin_puffing        = .t. 
part_group_configs(2)%use_kin_ionisation     = .t.
part_group_configs(2)%use_kin_radiation      = .t.
part_group_configs(2)%use_kin_bg_collisions  = .t.
part_group_configs(2)%atom_data_suffix = "96_n"
part_group_configs(2)%puff_ctrl(1)%times = 0     
part_group_configs(2)%puff_ctrl(1)%rates = 1.d19
part_group_configs(2)%puff_ctrl(1)%supers_num_puff = 20
```

现在就可以同时带中性粒子和杂质运行了。

# 4. 技巧与提示
  * 需要其他杂质种类时，必须修改参数 `Z`、`mass`、`atom_data_suffix`，并具备相应的 ADAS 文件。
  * 若关注刮削层（SOL），建议启用 `grid_to_wall` 并设置自然边界条件，使用：
  * 要在 vtk 中包含粒子投影，请在使用 **`convert2vtk.sh`** 时加上标志 `-proj jorek`
  * 过强的辐射会导致负温度和数值问题，确保不使用不合理的注入速率，然后可查看 [[corr_neg|以下功能允许对负密度或负温度进行"修正"，以避免浮点异常]] 中的一种变通办法。
