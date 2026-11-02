---
title: "编译 MUMPS"
nav_order: 6
parent: "编译与依赖库"
grand_parent: "编译与运行"
layout: default
render_with_liquid: false
---

# 编译 MUMPS

本文档是安装 MUMPS 及其依赖（并行版本）的简要指南。

## 依赖

- BLAS
- MPI
- BLACS
- ScaLAPACK

通常还会安装 SCOTCH 或 METIS 用于图划分，特别是在 MUMPS 中使用 Block-Low-Rank 压缩时。

## BLAS

BLAS 一般可通过包管理器安装，或已作为模块提供。

## MPI

MPI 有多个版本（`mpich`、`mpich2`、`openmpi`），通常系统上已经具备，也可通过包管理器安装。

## BLACS {#blacs}
> BLACS（Basic Linear Algebra Communication Subprograms）项目是一项持续开展的研究，其目标是建立一个面向线性代数的消息传递接口，使其能在各种分布式内存平台上高效、统一地实现。

更多信息见 [netlib](http://www.netlib.org/blacs/)。

若系统上还没有 BLACS（例如由 MKL 提供）：

- 在[此处](http://www.netlib.org/blacs/mpiblacs.tgz)下载 MPI 版本
- 运行：
  ```bash
  tar zxvf mpiblacs.tgz
  ```
- 运行：
  ```bash
  cp BMAKES/Bmake.MPI-LINUX Bmake.inc
  ```
- 编辑 `Bmake.inc`，正确设置 `BTOPdir`
- 若要用 OpenMPI 而非 MPICH 构建，见[此页面](https://www.open-mpi.org/faq/?category=mpi-apps#blacs)
- 构建 MPI 版本：
  ```bash
  make mpi
  ```
- 依赖库将放在 `BLACS/LIB`

## ScaLAPACK {#scalapack}
> ScaLAPACK 是面向并行分布式内存机器的高性能线性代数例程库。ScaLAPACK 可求解稠密与带状线性系统、最小二乘问题、特征值问题以及奇异值问题。

若系统上还没有 ScaLAPACK（例如由 MKL 提供）：

- 下载 [scalapack-2.0.2.tgz](http://www.netlib.org/scalapack/scalapack-2.0.2.tgz) 或更新版本
- 运行：
  ```bash
  tar zxvf scalapack-2.0.2.tgz
  ```
- 忽略 ScaLAPACK 安装包中自带的 BLACS 目录
- 运行：
  ```bash
  cp SLmake.inc.example SLmake.inc
  ```
- 编辑 `SLmake.inc` 的说明见[此页面](https://www.open-mpi.org/faq/?category=mpi-apps#scalapack)
- 编译 ScaLAPACK：
  ```bash
  make
  ```
- 输出文件为当前目录下的 `libscalapack.a`

## METIS

> METIS 是一组串行程序，用于图划分、有限元网格划分，以及为稀疏矩阵生成减少填充的排序。

- 下载 [METIS 5.1.0](http://glaros.dtc.umn.edu/gkhome/fetch/sw/metis/metis-5.1.0.tar.gz)（串行版本）或 [ParMETIS 4.0.3](http://glaros.dtc.umn.edu/gkhome/fetch/sw/parmetis/parmetis-4.0.3.tar.gz)（并行版本）
- 安装说明、文档以及可能更新的版本见 [METIS 网站](http://glaros.dtc.umn.edu/gkhome/views/metis)
- 运行：
  ```bash
  tar xvzf parmetis-4.0.3.tar.gz
  ```
- 配置：
  ```bash
  make config prefix=PARMETIS_ROOT
  ```
  其中 `PARMETIS_ROOT` 按实际情况替换
- 编译：
  ```bash
  make
  ```
- 安装：
  ```bash
  make install
  ```
- 注意：若下载的是 ParMETIS 但同时也需要 METIS，则后者位于 `metis` 子目录中。进入该子目录，重复上述步骤即可（根目录相应修改）。

## 编译 MUMPS 本身

> MUMPS 是一个并行稀疏直接求解器。

它可以在 JOREK 求解器中选择性使用，并用于杂质输运的粒子相关例程。

- [在此下载源码](http://mumps.enseeiht.fr/MUMPS_5.2.0.tar.gz)
- 解包：
  ```bash
  tar zxvf MUMPS_5.2.0.tar.gz
  ```
- 从 `Make.inc` 目录中复制适配本机架构的 `Makefile.inc`。这些 Makefile 中也包含按需调整的说明。`INSTALL` 文件含有进一步的安装说明。
- 编辑 `Makefile.inc`，填入 BLACS 与 ScaLAPACK 的路径，例如：

```makefile
BLACS_DIR = /home/daan/source/BLACS/LIB
SCALAP  = -llapack -L$(BLACS_DIR) /home/daan/source/scalapack-2.0.2/libscalapack.a \
          $(BLACS_DIR)/blacs_MPI-LINUX-0.a \
          $(BLACS_DIR)/blacsF77init_MPI-LINUX-0.a \
          $(BLACS_DIR)/blacsCinit_MPI-LINUX-0.a
#SCALAP  = -lscalapack -lblacs  -lblacsF77init -lblacsCinit
```

- 若要使用 SCOTCH 排序，将 `LSCOTCHDIR` 设为带 `esmumps` 的 scotch
  - SCOTCH 的编译见[主编译指南](./compiling.md)
  - SCOTCH 排序的相关信息见[此页面](http://mumps.enseeiht.fr/index.php?page=faq#2)
- 若要使用 METIS 排序，将 `LMETISDIR` 与 `IMETIS` 设为相应路径，并取消 `LMETIS` 的注释
  - METIS 的编译见上文
- 编译各精度的依赖库：
  ```bash
  make all
  ```
- 在 `lib/` 目录中可找到 `cmumps`、`dmumps`、`mumps_common` 和 `pord` 依赖库
