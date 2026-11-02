---
title: "构建系统"
nav_order: 2
parent: "编译与依赖库"
grand_parent: "编译与运行"
layout: default
render_with_liquid: false
---

# 构建系统

我们使用 `make` 编译代码。
构建系统由三部分组成：

- `Makefile`
- `Makefile.inc`
- `defaults.mk`

外加两个辅助脚本

- `util/makedepend`
- `util/obj_deps`

如希望进一步了解构建系统，建议同时阅读源码。

## 主 Makefile

这是你的 `make` 所读取的文件。

它包含默认规则（`clean` 等）以及待搜索源文件的目录列表。
对每个找到的源文件（匹配 `*.f90`），我们用 `util/obj_deps` 生成一个依赖文件（`.d`），其中包含该源文件的构建期与链接期依赖。
若该源文件提供 `PROGRAM`，还会额外添加一行。

`make` 首次读取该文件时，会自动尝试构建所有 `.d` 文件。
此后构建依赖图，你的程序便可编译。
程序即依据文件中是否存在 `PROGRAM` 关键字被自动发现。

## defaults.mk

该文件包含构建 Fortran 源文件所需的默认设置、编译标志与规则。
其中一些标志根据所用编译器定义，构建模板会被转换为规则。

## Makefile.inc

在该文件中可设定要使用哪些依赖库（`HDF5`、`HIPS`、`MUMPS`、`WSMP`、`PASTIX`、`MURGE`、`FFTW`、`LAPACK`、`BLAS`）。
还可设置特定的编译标志、选择所用模型并提供链接选项。
`Make.inc/` 中提供了许多示例

## util/makedepend

这是一个简单的 Perl 脚本，受 `sfmakedepend` 启发，用于通读 Fortran 源文件并查找

- `use` 语句
- `#include`
- `include`
- `module`
- `program`
- `subroutine calls`
- `external functions`

在查找完需调用的全部外部过程与需加载的模块之后，程序会尝试用 `find` 在传入的目录列表中定位相应文件。
为使这一机制工作，文件名必须与过程名一致。
脚本会执行一些已知的转换（例如 `pplot -> ppplib`）。当前的转换列表并不完备，将来大概还需补充。

## util/obj_deps

这是一段更简单的 Perl 脚本，它遍历 `.d` 依赖文件树，生成链接所需的依赖列表。
这样做是必要的，因为我们需要维护构建依赖与链接依赖两套不同的集合，而 `make` 无法替我们完成。
你大概不需要修改这个文件。
