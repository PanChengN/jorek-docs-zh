---
title: "TOK-I 集群"
nav_order: 9
parent: "HPC 与 PC 配置"
grand_parent: "编译与依赖库"
layout: default
render_with_liquid: false
---

# 在 IPP Garching 的 TOK-I 集群上运行 JOREK

> **本页在集群升级到 SLES15 之后刚刚更新。如发现新系统上有任何不正确之处，请予以更正。**

- [TOK Wiki 中关于该集群的信息](https://tok.ipp.mpg.de/wiki/TOK/index.php/Computing-TOKI)

```bash
ssh toki01.bc.rzg.mpg.de
...
ssh toki08.bc.rzg.mpg.de
```

## 所需模块

```bash
module load git intel/2023.1.0.x impi/2021.9 mkl fftw-mpi gnuplot hdf5-mpi
```

请加入你的 `~/.bashrc` 或 `~/.alias` 文件。

```bash
module load impi-interactive
```

建议**不要**将 `impi-interactive` 加入 `.bashrc`，因为这会使命在 TOK 集群上的仿真无法运行。

## 编译 JOREK 与依赖库

- [依赖库与 JOREK 的安装／编译](../compiling.md)按常规方式进行
- 也可以直接使用通过下列方式加载的依赖库：

```bash
module load pastix
```

> **警告：** 在 IPP 的集群（TOK-I、TOK、DRACO 与 COBRA）上，当每个谐波使用多于一个 MPI 任务运行 JOREK 时似乎存在问题。运行会在第一个时间步中的首次 PASTIX 调用处挂起。在这种情况下，`Pastix_5.2.3` 与 `Scotch_5.1.12b` 的组合已被证实可以解决该问题。

以下 `Makefile.inc` 文件应可让你编译 JOREK：

```makefile
# JOREK configuration file for compilation on the TOK cluster at IPP Garching
# see also https://www.jorek.eu/wiki/doku.php?id=draco
 
MODEL             = model307
 
FC                = mpiifort
CC                = mpiicc
CXX               = mpiicpc
 
COMPILER_FAMILY   = intel
 
USE_PASTIX        = 1
USE_STRUMPACK     = 0
USE_MUMPS         = 1
USE_PASTIX_MURGE  = 0
USE_BLOCK         = 1
USE_HDF5          = 1
USE_FFTW          = 1
USE_MKL           = 0
 
 
LIBDIR = /tokp/work/ihol/bin/intel
 
ifeq (1, $(USE_MUMPS))
 MKLLIB += -L${MKLROOT}/lib/intel64 -lmkl_scalapack_lp64 -lmkl_intel_lp64 \
         -lmkl_sequential -lmkl_core -lmkl_blacs_intelmpi_lp64
 MKLINC = -I${MKL_HOME}/include
 
 MUMPSDIR = $(LIBDIR)/MUMPS_5.2.1
 LIB_MUMPS = -L$(MUMPSDIR)/lib -ldmumps -lmumps_common -lpord
 INC_MUMPS = $(MUMPSDIR)/include
 
 LIB_MUMPS += $(MKLLIB)
 INC_MUMPS += $(MKLINC)
endif
 
 
ifeq (1, $(USE_PASTIX))
 MKLLIB += -L${MKL_HOME}/lib/intel64 -lmkl_intel_lp64 -lmkl_sequential -lmkl_core
 MKLINC = -I${MKL_HOME}/include
 
 PASTIX_DIR = $(LIBDIR)/pastix_5.2.3/install
 SCOTCH_DIR = $(LIBDIR)/scotch_5.1.12
 
 LIB_PASTIX = -L$(PASTIX_DIR) -lpastix -L$(SCOTCH_DIR)/lib -lscotch -lscotcherrexit
 INC_PASTIX = -I$(PASTIX_DIR)/include
 
 INC_PASTIX += $(MKLINC)
 LIB_PASTIX += $(MKLLIB)
 
endif
 
ifeq (1, $(USE_STRUMPACK))
 MKLLIB = -L${MKLROOT}/lib/intel64 -lmkl_scalapack_lp64 -lmkl_intel_lp64 \
         -lmkl_intel_thread -lmkl_core -lmkl_blacs_intelmpi_lp64
 MKLINC = -I${MKLROOT}/include
 
 METIS_HOME=$(LIBDIR)/metis_git/install
 PARMETIS_HOME=$(LIBDIR)/ParMETIS_git/install
 GKLIB_HOME=$(LIBDIR)/GKlib_git/install
 
 STRUMPACK_HOME=$(LIBDIR)/STRUMPACK-7.1.3/install
 
 STRUMPACKINC = -I$(STRUMPACK_HOME)/include
 STRUMPACKLIB = -L$(STRUMPACK_HOME)/lib64 -lstrumpack
 
 STRUMPACKINC += -I$(METIS_HOME)/include -I$(GKLIB_HOME)/include
 STRUMPACKLIB += -L$(METIS_HOME)/lib -lmetis -L$(GKLIB_HOME)/lib -lGKlib
 
 STRUMPACKINC += -I$(PARMETIS_HOME)/include
 STRUMPACKLIB += -L$(PARMETIS_HOME)/lib -lparmetis
 
 STRUMPACKINC += $(MKLINC)
 STRUMPACKLIB += $(MKLLIB)
 
 DEFINES += -DNEWSPK
endif
 
# --- FFTW Library
#LIBFFTW           = -Wl -rpath -L$(FFTW_HOME)/lib -lfftw3
LIBFFTW           = $(FFTW_HOME)/lib/libfftw3.a
INC_FFTW          = -I$(FFTW_HOME)/include
 
# --- HDF5 Library
HDF5INCLUDE = $(HDF5_HOME)/include
#HDF5LIB     = -Wl -rpath -L$(HDF5_HOME)/lib -lhdf5hl_fortran -lhdf5_hl -lhdf5_fortran -lhdf5 -lz
HDF5LIB     = $(HDF5_HOME)/lib/libhdf5hl_fortran.a  $(HDF5_HOME)/lib/libhdf5_hl.a  $(HDF5_HOME)/lib/libhdf5_fortran.a $(HDF5_HOME)/lib/libhdf5.a -L$(HDF5_HOME)/lib  -lz
```

## 文件系统

- 最好将运行目录放在 `/tokp/work/<user>/`
- 也可以使用：
  - `/tokp/scratch/<user>/` ——不做备份
  - `/ptmp1/work/<user>/`
  - `/ptmp1/scratch/<user>/` ——不做备份

## 批处理提交

_不可用。_

## 交互式运行

- 事先用 `top` 检查机器是否已被他人大量占用
- 不要运行很长的仿真
- 由于每个节点有 24 核，一条经验法则是 OpenMP 线程数 × MPI 任务数不应超过 20

```bash
export OMP_NUM_THREADS=<number-of-OpenMP-threads>
nice mpirun -n <mpi-tasks> ./jorek_model199 < ./input | tee logfile
```

在 TOK-I 上运行时，如果出现下面的错误，请指定 JOREK 二进制的路径：

```bash
env: ‘jorek_model199’: No such file or directory
```

### 不使用 MPI

要运行轴对称仿真，请只使用一个 MPI 任务：

```bash
mpirun -n 1 ./jorek_model199 < ./input | tee logfile
```

由于 JOREK 始终包含 MPI，这已经是尽可能接近"不使用 MPI"的运行方式。

### 交互式回归测试

要以交互方式运行回归测试，请设置：

```bash
export MPIRUN="mpirun -n 1"
```

然后按常规方式执行：

```bash
./non_regression_tests/run_test.sh
```
