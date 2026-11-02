---
title: "绘制内存使用"
nav_order: 14
render_with_liquid: false
parent: "代码开发"
---

#### 绘制内存使用
内存使用情况由带内存监视脚本运行 JOREK 时生成，例如
```
mpirun mem_monitor jorek
```
运行后会生成文件 `mem_pid_*.log`。`plot_mlog.py` 脚本读取这些文件，并绘制内存使用随时间的变化。

此外，JOREK 可以生成带任意标记的时间线文件，这些标记可叠加在时间历程之上。为此需要修改源代码，在需要处加入 `use matio_module, only: timestamp` 和 `call timestamp("Arbitrary time mark",<my_id>)`。这会生成文件 `timeline00<my_id>.out`，其中包含一行 `xxxxxx.xxxxx      Arbitrary time mark`。`plot_mlog.py` 脚本可通过选项 `-tline <timeline_file_name>` 读取该文件。
