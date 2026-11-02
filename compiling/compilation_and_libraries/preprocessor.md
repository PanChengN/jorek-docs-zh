---
title: "预处理器标志"
nav_order: 4
parent: "编译与依赖库"
grand_parent: "编译与运行"
layout: default
render_with_liquid: false
---

# 预处理指令

JOREK 使用 **fpp 预处理器**（[Intel 的相关说明](https://software.intel.com/de-de/node/510269)）。`fpp` 在实际编译之前处理源文件，由此实现条件编译。**预处理指令**写入代码中（以 `#` 开头），可用于检测**预处理符号**（如 `USE_BLOCK`、`JOREK_MODEL`）。

## 预处理指令的两个示例

- 封装模型相关的部分：

```fortran
#if JOREK_MODEL == 500
use mgi_module
#endif
```

- 为同一问题实现不同的解决方案，例如求解器对矩阵的分析：

```fortran
#ifdef USE_BLOCK
  pastix_iparm(IPARM_DOF_NBR) = block_size
#else
  pastix_iparm(IPARM_DOF_NBR) = 1
#endif
```

## 设置预处理符号

`USE_BLOCK` 这类预处理符号通常由命令行选项定义，例如对 Intel Fortran 编译器使用

```text
-DUSE_BLOCK
```

在 JOREK 中，我们为此定义了相应开关，因此只需在 `Makefile.inc` 中设置

```make
USE_BLOCK = 1
```

即可覆盖最重要的那些开关（概览见下表）。

## 重要预处理符号列表

下表汇总了最重要的预处理符号及其设置方式。

| 预处理符号 | 在 Makefile.inc 中的设置 | 说明 |
|----------|--------|--------|
| USE_MUMPS | USE_MUMPS = 1 | 使用 MUMPS 求解器 |
| USE_PASTIX | USE_PASTIX = 1 | 使用 PaStiX 求解器（**推荐**） |
| USE_MURGE | USE_PASTIX_MURGE = 1 | 使用 PaStiX 的 MURGE 接口 |
| USE_HIPS | USE_HIPS = 1 | 使用 HIPS 求解器 |
| USE_WSMP | USE_WSMP = 1 | 使用 WSMP 求解器 |
| USE_FFTW | USE_FFTW = 1 | 使用 FFTW 库进行快速傅里叶变换（**推荐**） |
| USE_BLOCK | USE_BLOCK = 1 | 利用矩阵的分块结构进行分析（**推荐**） |
| USE_HDF5 | USE_HDF5 = 1 | 使用 HDF5 数据格式 |
| MEMTRACE | FFLAGS := $(FFLAGS) -DMEMTRACE | 将内存使用信息输出到 `trace*` 文件中 |
| COMPARE_ELEMENT_MATRIX | FFLAGS := $(FFLAGS) -DCOMPARE_ELEMENT_MATRIX | 直接比较 `element_matrix` 与 `element_matrix_fft`，用于调试 |
| JOREK_MODEL | 自动设置 | 支持 `#if JOREK_MODEL == 500` 这类预处理指令 |
| FULL_MHD | 自动设置 | 用于模型 710 |
| FUNNELED | FFLAGS := $(FFLAGS) -DFUNNELED | 告知 PaStiX 不从 OpenMP 并行代码中调用 MPI（**许多机器上必需**） |
| WORLDWAR2 | FFLAGS := $(FFLAGS) -DWORLDWAR2 | 供 PaStiX 使用的标志（**`pastix_release_3945` 及更新版本必需**，另见编译说明） |

对于各依赖库，还需在 `Makefile.inc` 中设置额外变量，例如 FFTW 库需要 `LIBFFTW` 与 `INC_FFTW`。查阅 Makefile 以确定各依赖库需要指定哪些变量。
