---
title: "Viper"
nav_order: 12
parent: "HPC 与 PC 配置"
grand_parent: "编译与依赖库"
layout: default
render_with_liquid: false
---

# MPCDF 的 Viper 超级计算机系统

- 768 个 CPU 计算节点  
  （AMD EPYC Genoa 9554 CPU，128 核，每节点至少 512 GB 内存，理论峰值性能 4.9 PFlop/s（FP64））
- 228 个 GPU 节点，共包含 456 个 APU  
  （将于 2024 年内陆续部署）

- <https://docs.mpcdf.mpg.de/doc/computing/viper-user-guide.html>

## 通过网关登录

```bash
ssh <user>@gate.mpcdf.mpg.de
```

```bash
ssh <user>@viper.mpcdf.mpg.de
```

## 文件系统

文件系统 `/u`（指向 `/viper/u` 的符号链接）用于长期存放用户数据（源文件、配置文件等）。`/u` 的容量为 1.2 PB。你的主目录位于 `/u` 中。`/u` 的默认磁盘配额为 1.0 TB，文件数配额为 256K 个文件。可用如下命令检查你在 `/u` 中的磁盘配额：

```bash
/usr/lpp/mmfs/bin/mmlsquota viper_u
```

文件系统 `/ptmp`（指向 `/viper/ptmp` 的符号链接）用于批处理作业的 I/O（12 PB，无系统备份）。`/ptmp` 中超过 12 周未被访问的文件将被自动删除。如有必要，可在事先通知的前提下缩短 12 周的期限。

按现行政策，`/ptmp` 上不施加配额。

`/r` 文件系统（指向 `/ghi/r` 的符号链接）用于暂存归档数据。它仅在登录节点 `viper.mpcdf.mpg.de` 和交互节点 `viper-i.mpcdf.mpg.de` 上可用。

每个用户在 `/r/<initial>/<userid>` 下有一个子目录用于存放数据。为提高效率，在归档到 `/r` 之前应将文件打包为 tar 文件，大小约为 1 GB 至 1 TB。请避免归档大量小文件。当文件系统 `/r` 的占用超过某一阈值时，文件将从磁盘转移到磁带，并优先从未被使用时间最长的大文件开始。

请不要将文件系统 `/tmp` 或 `$TMPDIR` 用于临时数据，而应使用 `/ptmp`，它可从 Viper 集群的所有节点访问。

如果某个应用确实依赖节点本地存储，请使用环境变量 `JOB_TMPDIR` 与 `JOB_SHMTMPDIR` 所指的目录，它们为每个 Slurm 作业单独设置。

## 编译 JOREK

将下列各行加入 `.bashrc` 文件：

```bash
module purge
module load intel/2024.0 impi/2021.11 mkl/2024.0
module load hdf5-mpi/1.14.1
module load fftw-mpi/3.3.10

export LD_LIBRARY_PATH=${FFTW3_ROOT}/lib:${HDF5_ROOT}/lib:${MKLROOT}/lib:${LD_LIBRARY_PATH}
```

`Makefile.inc` 示例：

```makefile
MODEL             = model303

FC                = mpiifx
CC                = mpiicx
CXX               = mpiicpx

FLAGS += -O2 -march=znver4
COMPILER_FAMILY   = intel

USE_PASTIX        = 0
USE_PASTIX_MURGE  = 0
USE_PASTIX6       = 0
USE_STRUMPACK     = 1
USE_MUMPS         = 0
USE_BLOCK         = 1
USE_HDF5          = 1
USE_FFTW          = 1
USE_MKL           = 0

LIBDIR = /u/ihol/lib/intel

ifeq (1, $(USE_STRUMPACK))
 MKLLIB= -L${MKLROOT}/lib/intel64 -lmkl_scalapack_lp64 -lmkl_intel_lp64 \
         -lmkl_intel_thread -lmkl_core -lmkl_blacs_intelmpi_lp64
 MKLINC = -I${MKLROOT}/include

 GKLIB_HOME = $(LIBDIR)/GKlib/install
 METIS_HOME = $(LIBDIR)/METIS/install
 PARMETIS_HOME = $(LIBDIR)/ParMETIS/install
 STRUMPACK_HOME=$(LIBDIR)/STRUMPACK-7.2.0/install

 STRUMPACKINC = -I$(STRUMPACK_HOME)/include
 STRUMPACKLIB = -L$(STRUMPACK_HOME)/lib64 -lstrumpack

 STRUMPACKINC += -I$(METIS_HOME)/include -I$(GKLIB_HOME)/include -I$(PARMETIS_HOME)/include
 STRUMPACKLIB += -L$(METIS_HOME)/lib -lmetis -L$(GKLIB_HOME)/lib -lGKlib -L$(PARMETIS_HOME)/lib -lparmetis

 STRUMPACKINC += $(MKLINC)
 STRUMPACKLIB += $(MKLLIB)

 DEFINES += -DNEWSPK
endif

# --- FFTW Library
LIBFFTW           = -L$(FFTW_HOME)/lib -lfftw3
INC_FFTW          = -I$(FFTW_HOME)/include

# --- HDF5 Library
HDF5INCLUDE = $(HDF5_HOME)/include
HDF5LIB     = -L$(HDF5_HOME)/lib -lhdf5hl_fortran -lhdf5_hl -lhdf5_fortran -lhdf5 -lz
```

## 运行 JOREK

批处理作业脚本示例：

```bash
#!/bin/bash -l
#SBATCH -D ./
#SBATCH -J JOREK
#SBATCH --nodes=1
#SBATCH --tasks-per-node=4
#SBATCH --cpus-per-task=32
#SBATCH --time=01:00:00

export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}
export OMP_PLACES=cores

export EXECUTABLE="./jorek_model303"

srun ${EXECUTABLE} <inxflow |& tee logfile.out
```
