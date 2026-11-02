---
title: "以 64 位整数编译"
nav_order: 5
parent: "编译与依赖库"
grand_parent: "编译与运行"
layout: default
render_with_liquid: false
---

# 以长整数编译 JOREK 与求解器

以长整数编译代码可使用更大的矩阵。

通常稀疏求解器会采用分布式矩阵，因此增加 MPI 进程数即可减小每个进程上的矩阵索引规模。

然而这带来两个问题：

1. 增加 MPI 进程会提高整体内存占用。
2. 部分求解器（如 PASTIX）没有分布式矩阵选项。

STRUMPACK 具备分布式矩阵选项，Block-Jacobi 谐波矩阵中用到了该选项，但目前 `solve_strumpack_all.f90` 尚未使用。

无论如何，每个谐波只使用 1 个 MPI 进程、其余核心全部以 OMP 方式使用，都能降低内存需求。在 Intel Optane、SGI UV-2000 或 HPE SuperdomeFlex 这类内存密集型架构上，这一点至关重要。

下面概述如何以长整数编译各求解器与 JOREK。

## METIS & PARMETIS

METIS 与 PARMETIS 只需修改 include 文件中的整数长度：

- `include/metis.h`
- `include/parmetis.h`

Marconi 上 METIS 的 CMake 命令如下（使用 Intel 编译器）：

```bash
cmake ../ -DGKLIB_PATH="../GKlib" -DCMAKE_INSTALL_PREFIX="../install" -DCMAKE_C_COMPILER=mpiicc -DCMAKE_CXX_COMPILER=mpiicpc -DCMAKE_Fortran_COMPILER=mpiifort
```

## SCOTCH

SCOTCH 需在 `Makefile.inc` 中加上编译标志

```makefile
CFLAGS = other_flags -DINTSIZE64
```

## PASTIX

在 Pastix-5 中，需修改指定整数长度的段落，改为：

```makefile
VERSIONINT = _int64
CCTYPES = -DINTSSIZE64
```

## STRUMPACK

在 STRUMPACK 中，需将下列文件中的行

```cpp
template<typename scalar_t,typename integer_t>
```

改为

```cpp
template<typename scalar_t,typename integer_t=int64_t>
```

涉及文件：

- `StrumpackSparseSolver.hpp`
- `StrumpackSparseSolverBase.hpp`
- `StrumpackSparseSolverMPIDist.hpp`

对 STRUMPACK，Marconi 上编译前的 CMake 命令为：

```bash
export ScaLAPACKLIBS="-L$MKLROOT/lib/intel64 -lmkl_scalapack_lp64 -lmkl_intel_lp64 -lmkl_intel_thread -lmkl_core -lmkl_blacs_intelmpi_lp64 -liomp5 -lpthread -lm -ldl"
```

```bash
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../install -DCMAKE_CXX_COMPILER=mpiicpc -DCMAKE_C_COMPILER=mpiicc -DCMAKE_Fortran_COMPILER=mpiifort -DCMAKE_CXX_FLAGS=-std=c++14 -DSTRUMPACK_USE_OPENMP=ON -DTPL_ENABLE_BPACK=OFF -DTPL_ENABLE_ZFP=OFF -DTPL_ENABLE_SLATE=OFF -DTPL_METIS_INCLUDE_DIRS=/marconi_work/FUA34_ELM-UK/spamela/STRUMPACK_tries/try_intel_64/metis-5.1.0/install/include -DTPL_METIS_LIBRARIES="-L/marconi_work/FUA34_ELM-UK/spamela/STRUMPACK_tries/try_intel_64/metis-5.1.0/install/lib -lmetis" -DTPL_SCALAPACK_LIBRARIES="$ScaLAPACKLIBS" ../
```

当然，需相应更新 METIS/PARMETIS 的位置。

## JOREK

在 JOREK 中，只需在 `Makefile.inc` 中使用指令

```makefile
USE_INTSIZE64 = 1
```
