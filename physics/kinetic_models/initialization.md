---
title: "初始化"
---

# 动理学粒子初始化 

所谓初始化，我们指的是在 kinetic_main 开始模拟之前，粒子所获得的初始分布。初始化可以通过 3 种方式进行：或者不初始化任何内容，或者从重启文件初始化粒子，或者按某种初始分布初始化粒子。

# 不初始化 
只需在 namelist 中设置 restart_particles=.f.，并且不要为 part_group_configs(...)%init_function 与 %init_pdf 设置任何内容。这意味着在 kinetic_main 开始模拟时，尚无模拟粒子。例如，这对于中性粒子模拟很有用，因为中性粒子会在模拟过程中通过（壁）复合自动被充入/生成。 

# 重启粒子 
要从文件重启粒子，请设置 restart_particles=.t.。在初始化期间，kinetic_main 会自动在模拟文件夹中查找 part_restart.h5 文件，并把该文件中的所有组直接加载进模拟。为此，你的 namelist 输入文件中也需要有相应的组。这意味着你的 namelist 输入中需要有与重启前各组具有相同 %id、%Z、%mass 与 %type 的条目，但你可以改变每组的 %n_particles（不过目前只能增大，不能减小）。

如果你希望新模拟中的 part_groups 比 restart_file 中的更多或更少，建议通过把 namelist 输入 "part_groups_in_use" 设为你希望在新模拟中使用的 ID 列表来表明你的意图（例如 `part_groups_in_use = "D01" "N01"`）。如果你想从 part_restart.h5 文件中丢弃某些组，你**必须**指定 "part_groups_in_use"。你的输出文件中会出现信息，说明哪些组已加载、哪些组已被丢弃。

part_restart.h5 文件在每次 kinetic_main 模拟成功结束时自动生成，并且每 500 个 jorek 步会生成一个中间文件 "interim_part_restart.h5"（若已存在先前的中间重启文件，则将其覆盖，以节省磁盘空间，因为这些重启文件可达数 GB 数据）。 

# 按给定分布初始化粒子 

!!! 在此处补上初始化器（@James）
