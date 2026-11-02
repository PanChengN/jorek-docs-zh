---
title: "动理学粒子模块"
nav_order: 6
parent: "物理模型"
layout: default
render_with_liquid: false
---

## 动理学框架简介

动理学模拟使用试验粒子（有时也称为示踪粒子、超粒子或标记粒子，尽管这些说法的含义存在细微差别）来表示待模拟的真实粒子（例如单个原子）的底层分布函数。这与流体模拟形成对照：在流体模拟中，真实粒子（例如等离子体离子与电子）由网格上的物理量（如密度与温度）表示。动理学粒子不是用确定性方程来演化等离子体状态（如流体求解器那样），而是通过从相互作用的统计分布中抽取随机相互作用结果来更新。正因为这种随机性（如同蒙特卡洛赌场中的随机性），这类模拟常被称为蒙特卡洛模拟。

JOREK 中的动理学扩展是一个灵活的框架，包含动理学中性粒子、杂质、逃逸电子与高能粒子的选项，并提供不同的方案来建立与 MHD 流体的双向耦合。动理学扩展由 kinetic_main 程序运行，它是动理学扩展中对应于 jorek_model600（由 jorek2_main.f90 编译而成）的程序。使用 kinetic_main 时，可直接从 namelist 输入文件中选择模拟设置（细节将在本页及其子页面中说明）。

目前动理学扩展位于一个名为 "kinetic_develop" 的独立分支中。正在进行的努力是把许多独立示例程序的功能整合进 "kinetic_main"，从而不再需要那些独立的示例文件（一旦完成，kinetic_develop 将合并进 develop）。

要使用 kinetic_main，首先需要编译。确认你的硬编码设置正确（`./util/config.sh`）且与 kinetic_main 兼容（目前 kinetic_main 与 with_vpar 和 with_TiTe 兼容，但不与 with_neutrals 和 with_impurities 兼容，因为后者假定你会以动理学方式处理这些。此外，一切都应与 2D 和 3D 兼容，因此你可以选择 n_tor、n_plane 与 n_period 的任意常规组合。如果你不清楚这是什么，请参见[首次运行 jorek](../../howto/running_jorek_for_the_first_time.md)）。然后，只需在你的 jorek 文件夹中运行以下命令来编译 kinetic_main：

```bash
  make kinetic_main
```

要运行 kinetic_main，你需要一个初始的基准 MHD jorek_restart.h5 文件，例如通过以 restart=.f. 运行 jorek_model600 生成的文件。（关于运行流体模型的更多信息，请参见[首次运行 jorek](../../howto/running_jorek_for_the_first_time.md)，不过务必使用 model600）。kinetic_main 会自动从运行所在的文件夹加载 jorek_restart.h5（若不存在则抛出错误）。

此外，视你的应用而定，你可能还需要在模拟文件夹中放置额外文件，例如 wall.txt（当使用 grid_to_wall=.true. 且未使用 patches 时），或 acd12_h.dat 之类的文件（其中包含动理学中性粒子/杂质与等离子体反应的速率系数），或 y_DD.dat 之类的文件（其中包含 Eckstein 系数，用以描述溅射等壁相互作用的速率）。

此外，你还需要一个 namelist 输入文件，其中同时包含 MHD 等离子体和你所引入的动理学粒子的输入（很快会说明）。

模拟文件夹中备齐了正确的文件，就可以直接这样运行：

```bash
  kinetic_main < namelist
```

### 动理学 namelist 输入基础 

kinetic_main 中的动理学粒子种类通过输入文件中的 "part_group_configs" 控制。同一组内的所有粒子都代表相同的底层粒子种类（例如 W 杂质或逃逸电子），但每个试验粒子都拥有各自的位置、权重与速度/动量/能量（取决于粒子类型）等。

要添加一个粒子组（即一个动理学种类），请相应设置其定义变量（这些变量适用于该组内的所有单个粒子：）

| 变量 | 含义 |
| - | - |
| %id | 该粒子组的 3 字母唯一标识（代码其余部分与输出文件将用此 ID 指代该组。id 为必需项且必须唯一） |
| %Z | 原子质量数（整数，e 为 -1，D 为 -2，T 为 -3） |
| %mass | 粒子组的质量（单位 AMU） |
| %coupling_scheme | 三字母代码，指定该组如何与 MHD 等离子体耦合，参见[[coupling_schemes | 耦合方案]] |
| %n_particles | 该组可拥有的模拟试验粒子的最大数目（为方便可写成 1e6 这样的实数） |
| %type | 粒子类型同时定义了粒子拥有哪些变量（如电荷 q、速度、能量、动量、磁矩等）以及粒子如何被推进器推进，从而在一个时间步之后传播到新的位置 |

然后，视粒子类型与耦合方式而定，你可能还需要指定额外的标志，用以描述要模拟哪些与等离子体的相互作用等。更多内容见 [particles](../particles.md) 页面中"可用的耦合类型与教程"一节所链接的各页。
