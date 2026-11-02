---
title: "Raven"
nav_order: 11
parent: "HPC 与 PC 配置"
grand_parent: "编译与依赖库"
layout: default
render_with_liquid: false
---

# MPCDF 的 Raven 系统

## 基本信息

文档：

- **[Raven 用户指南](https://docs.mpcdf.mpg.de/doc/computing/raven-user-guide.html)**
- [MPCDF 的 Raven](https://www.mpcdf.mpg.de/services/supercomputing/raven)

**计算节点：**

- 目前为 360 个节点
- 每节点 2×36 核
- 每节点内存：240 GB

### 访问集群

首先登录网关机：

```bash
ssh gate.mpcdf.mpg.de
```

然后从网关机执行：

```bash
ssh raven[01-02]i
```

### 文件系统

登录节点上可以访问 AFS。

`/u` 与 `/ptmp` 两个文件系统在登录节点和计算节点上均可访问。

- 数据可以存放在 `/u/<user>` 下；适用 2.5 TB 的配额  
  （通过 `'/usr/lpp/mmfs/bin/mmlsquota raven_u'` 检查）
- `/ptmp/<user>` 应用作临时存储

两个文件系统均**不做自动备份**。

注意，`/ptmp/` 上的文件若 12 周未被访问，将被**自动删除**。

## 编译 JOREK

- 将下列各行加入 `.bashrc` 文件：

```bash
module purge
module load intel/2025.1 impi/2021.15
module load mkl/2025.1
module load fftw-mpi
module load hdf5-mpi
module load hwloc/2.2

export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${INTEL_HOME}/compiler/latest/linux/compiler/lib/intel64/
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${MKLROOT}/lib/intel64
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${HDF5_ROOT}/lib
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${FFTW_HOME}/lib
```

- 如需使用预编译的外部求解器库，请向 `ihor.holod@ipp.mpg.de` 发送申请，并说明你的 Raven 用户名。

- `Makefile.inc` 示例  
  （注意 PaStiX 与 STRUMPACK 不应同时选用）：

```makefile
MODEL             = model303
FC                = mpiifx
CC                = mpiicx
CXX               = mpiicpx
 
FFLAGS += -O3 -mcmodel=medium
EXTRA_FLAGS += -lstdc++
COMPILER_FAMILY   = intel
# Never use STRUMPACK and PASTIX at the same time 
USE_PASTIX        = 0
USE_PASTIX_MURGE  = 0
USE_PASTIX6       = 0
USE_STRUMPACK     = 1
USE_MUMPS         = 1
USE_BLOCK         = 1
USE_HDF5          = 1
USE_FFTW          = 1
USE_MKL           = 0
USE_DIRECT_CONSTRUCTION=0
USE_BICGSTAB=0
LIBS += -liomp5 -pthread -ldl -lm
 
LIBDIR = /raven/u/ihol/lib/intel

ifeq (1, $(USE_PASTIX))

 MKLLIB += -L${MKLROOT}/lib/intel64 -lmkl_intel_lp64 -lmkl_sequential -lmkl_core
 MKLINC = -I${MKLROOT}/include
 PASTIX_DIR = $(LIBDIR)/pastix_5.2.3/install
 SCOTCH_DIR = $(LIBDIR)/scotch_5.1.12

 LIB_PASTIX = -L$(PASTIX_DIR) -lpastix -L$(SCOTCH_DIR)/lib -lscotch -lscotcherr
 INC_PASTIX = -I$(PASTIX_DIR)/include

 INC_PASTIX += $(MKLINC)
 LIB_PASTIX += $(MKLLIB)

endif

ifeq (1, $(USE_MUMPS))
# --- MUMPS
 MKLLIB += -L${MKLROOT}/lib/intel64 -lmkl_scalapack_lp64 -lmkl_intel_lp64 \
         -lmkl_intel_thread -lmkl_core -lmkl_blacs_intelmpi_lp64
 MKLINC = -I${MKLROOT}/include
 MUMPS_DIR = $(LIBDIR)/MUMPS_5.4.1
 LIB_MUMPS = -L$(MUMPS_DIR)/lib -ldmumps -lmumps_common -lpord
 INC_MUMPS = $(MUMPS_DIR)/include

 LIB_MUMPS += $(MKLLIB)
 INC_MUMPS_EXTRA += $(MKLINC)

endif

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

## 提交作业

下面是一个 SLURM 作业脚本示例：

```bash
#!/bin/bash -l
#SBATCH -D ./
#SBATCH -J jorek
#SBATCH -C icelake
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=2
#SBATCH --cpus-per-task=36
#SBATCH --time=00:10:00

source $HOME/.bashrc

export OMP_NUM_THREADS=36
export OMP_PLACES=cores

srun ./jorek_model303 < intear > logout.out
```

## 交互式运行

要在 Raven 上交互运行，请通过以下方式进入交互节点：

```bash
ssh raven-i
```

或

```bash
ssh raven[03-06]
```

存在以下限制：

- 核数（`<= 8`）
- 内存（`<= 256000M`）
- 时间（`<= 2 hours`）

（我的作业在核数超过推荐值时也能启动，但用户指南警告不要这样做。）

```bash
srun -n N_TASKS -p interactive --time=TIME_LESS_THAN_2HOURS --mem=MEMORY_LESS_THAN_32G ./EXECUTABLE
```

示例：

```bash
export OMP_NUM_THREAD=4
nice srun -n 2 -p interactive --time=00:30:00 --mem=16GB ./jorek_model600 < input_jorek | tee logfile
```

分配资源可能需要一点时间。
