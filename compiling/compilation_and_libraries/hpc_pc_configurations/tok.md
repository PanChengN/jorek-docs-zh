---
title: "TOK 集群"
nav_order: 10
parent: "HPC 与 PC 配置"
grand_parent: "编译与依赖库"
layout: default
render_with_liquid: false
---

# 在 TOK Linux 集群上运行 JOREK（2025 年安装）

## 基本信息

- [关于 TOK 集群的信息](https://hpc.wiki.ipp.mpg.de/tok_batch_cluster_in_garching)

**有两个登录节点可用**（仅用于编译与提交作业）：

```bash
ssh tok[11-12].ipp.mpg.de
```

**交互节点池**（用于运行小型测试）：

为运行小型交互测试，可使用硬件略旧的 TOK-I 集群 `toki01...toki12.ipp.mpg.de`。

**计算节点：**

- 72 个节点
- 每个节点 2 颗 AMD EPYC 9754 CPU，每颗 128 核，基础频率 2.25 GHz
- 每节点内存：768 GB
- 操作系统：SLES15

## 所需模块

编译所需的基本模块集：

```bash
module load intel/2025.1 impi/2021.15 mkl/2025.1 fftw-mpi/3.3.10 hdf5-mpi/1.14.1
```

交互运行（不使用 SLURM）所需的附加模块：

```bash
module load impi-interactive
```

后处理分析、可视化、数据与代码共享所需的附加模块：

```bash
module load visit
module load paraview
module load git
module load gnuplot
module load texlive
module load imagemagick
module load datashare
```

你可以将这些模块加入 `~/.bashrc` 文件（不推荐，因为与其他环境的冲突很难排查），也可以使用 `module save/restore` 功能。

## 编译 JOREK 与依赖库

> **警告：** 在 IPP 的集群（TOK-I、TOK、DRACO 与 COBRA）上，当每个谐波使用多于一个 MPI 任务运行 JOREK 时似乎存在问题。运行会在第一个时间步中的首次 PASTIX 调用处挂起。在这种情况下，`Pastix_5.2.3` 与 `Scotch_5.1.12b` 的组合已被证实可以解决该问题。

- [依赖库与 JOREK 的安装／编译](../compiling.md)按常规方式进行。
- 也可以直接使用 Ihor Holod 已编译好的库（可能需要向 Matthias Hoelzl 申请访问权限），对应的 `Makefile.inc` 文件如下：

```makefile
# JOREK configuration file for compilation on the TOK cluster at IPP Garching
# from: https://jorek.eu/wiki/doku.php?id=garching-tok-cluster
 
MODEL             = model199
 
FC                = mpiifx
CC                = mpiicx
CXX               = mpiicpx
 
FFLAGS += -O2 -march=native
 
COMPILER_FAMILY   = intel
 
USE_PASTIX        = 0
USE_STRUMPACK     = 1
USE_MUMPS         = 0
USE_PASTIX_MURGE  = 0
USE_BLOCK         = 1
USE_HDF5          = 1
USE_FFTW          = 1
USE_MKL           = 0
 
# folder owned by Matthias Hoelzl - ask for access if needed
LIBDIR = /tokp/work/mhoelzl/bin-of-ihol/intel/
 
ifeq (1, $(USE_MUMPS))
 MKLLIB= -L${MKLROOT}/lib/intel64 -lmkl_scalapack_lp64 -lmkl_intel_lp64 \
         -lmkl_intel_thread -lmkl_core -lmkl_blacs_intelmpi_lp64 \
         -Wl,-rpath,${MKLROOT}/lib/intel64
 MKLINC = -I${MKL_HOME}/include
 
 MUMPSDIR = $(LIBDIR)/MUMPS_5.2.1
 LIB_MUMPS = -L$(MUMPSDIR)/lib -ldmumps -lmumps_common -lpord
 INC_MUMPS = $(MUMPSDIR)/include
 
 LIB_MUMPS += $(MKLLIB)
 INC_MUMPS += $(MKLINC)
endif
 
 
ifeq (1, $(USE_PASTIX))
 MKLLIB = -L${MKL_HOME}/lib/intel64 -lmkl_intel_lp64 -lmkl_sequential -lmkl_core \
         -Wl,-rpath,${MKLROOT}/lib/intel64
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
         -lmkl_intel_thread -lmkl_core -lmkl_blacs_intelmpi_lp64 \
         -Wl,-rpath,${MKLROOT}/lib/intel64
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
LIBFFTW           = -L$(FFTW_HOME)/lib -lfftw3 -Wl,-rpath,$(FFTW_HOME)/lib
INC_FFTW          = -I$(FFTW_HOME)/include
 
# --- HDF5 Library 
HDF5INCLUDE = $(HDF5_HOME)/include
HDF5LIB     = -L$(HDF5_HOME)/lib -lhdf5hl_fortran -lhdf5_hl -lhdf5_fortran -lhdf5 -lz  -Wl,-rpath,$(HDF5_HOME)/lib
```

## 文件系统

- 最好将仿真放在 `/tokp/work/<user>`（你的主目录）
- 默认情况下你在 `/tokp/work/<user>` 的配额为 2 TB，且这些数据会自动备份
- **使用 scratch 目录时要小心，因为没有自动备份**

## 批处理提交

- 提交作业：

```bash
sbatch jobscript
```

- 查看作业状态：

```bash
squeue -u <username>
```

- 取消作业：

```bash
scancel <jobid>
```

- 列出可用队列（分区）：

```bash
sinfo
```

### 作业脚本示例

#### 串行作业

```bash
#!/bin/bash -l
#SBATCH -J jorek_testing      #Job name
#SBATCH -o ./%x.%j.out        #stdout (%x=jobname, %j=jobid)
#SBATCH -e ./%x.%j.err        #stderr (%x=jobname, %j=jobid)
#SBATCH -D ./                 #Initial working directory
#SBATCH --partition=s.tok     #Queue/Partition
#SBATCH --qos=s.tok.standard  #Quality of Service: s.tok.short, s.tok.standard, s.tok.long, tok.debug
#SBATCH --nodes=1             #Total number of nodes  
#SBATCH --ntasks-per-node=1   #MPI tasks per node
#SBATCH --cpus-per-task=1     #CPUs per task for OpenMP
#SBATCH --mem-per-cpu 1GB     #Set memory requirement (default: 1 GB, max: 5GB)
#SBATCH --time=12:00:00       #Wall clock limit
##
#SBATCH --mail-type=end       #Send mail, e.g. for begin/end/fail/none
#SBATCH --mail-user=YOUR_USER_ID@rzg.mpg.de  #Mail address

export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
# For pinning threads correctly:
export OMP_PLACES=cores 

# Run the program:
srun ./jorek_model199 < ./intear
```

#### OpenMP 作业

```bash
#!/bin/bash -l
#SBATCH -J jorek_testing_omp      #Job name
#SBATCH -o ./%x.%j.out        #stdout (%x=jobname, %j=jobid)
#SBATCH -e ./%x.%j.err        #stderr (%x=jobname, %j=jobid)
#SBATCH -D ./                 #Initial working directory
#SBATCH --partition=p.tok.openmp     #Queue/Partition
#SBATCH --qos=p.tok.openmp.48h       #Quality of Service: p.tok.openmp.2h, p.tok.openmp.24h, p.tok.openmp.48h, tok.debug
#SBATCH --nodes=1             #Total number of nodes  
#SBATCH --ntasks-per-node=1   #MPI tasks per node
#SBATCH --cpus-per-task=4     #CPUs per task for OpenMP
#SBATCH --mem-per-cpu 1GB     #Set memory requirement (default: 1 GB, max: 5GB)
#SBATCH --time=12:00:00       #Wall clock limit
##
#SBATCH --mail-type=end       #Send mail, e.g. for begin/end/fail/none
#SBATCH --mail-user=YOUR_USER_ID@rzg.mpg.de  #Mail address

export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
# For pinning threads correctly:
export OMP_PLACES=cores 

# Run the program:
srun ./jorek_model199 < ./intear | tee logfile
```

#### OpenMP + MPI 作业

```bash
#!/bin/bash -l
#SBATCH -J jorek_testing           #Job name
#SBATCH -o ./%x.%j.out             #stdout (%x=jobname, %j=jobid)
#SBATCH -e ./%x.%j.err             #stderr (%x=jobname, %j=jobid)
#SBATCH -D ./                      #Initial working directory
#SBATCH --partition=p.tok          #Queue/Partition
#SBATCH --qos=p.tok.48h            #Quality of Service: p.tok.2h, p.tok.48, tok.debug
#SBATCH --nodes=2                  #Total number of nodes  
#SBATCH --ntasks-per-node=1        #MPI tasks per node
#SBATCH --cpus-per-task=2          #CPUs per task for OpenMP
#SBATCH --mem 90GB                 #Set mem./node requirement (default: 63000MB, max: 190GB)
#SBATCH --time=12:00:00            #Wall clock limit
##
#SBATCH --mail-type=end            #Send mail, e.g. for begin/end/fail/none
#SBATCH --mail-user=YOUR_USER_ID@rzg.mpg.de  #Mail address

export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
# For pinning threads correctly:
export OMP_PLACES=cores 

# Run the program:
srun ./jorek_model199 < ./intear | tee logfile
```

TOK 集群的更多作业脚本示例见[此处](https://hpc.wiki.ipp.mpg.de/tok_batch_cluster_in_garching)。

## VNC Viewer

虚拟网络连接（VNC）服务器的搭建在[此处](https://www.mpcdf.mpg.de/services/computing/software/vnc-at-the-mpcdf)有概述。

除上述命令外，已观察到可视化软件在新系统上可能崩溃，原因似乎与所需字体有关的错误。因此建议在建立 VNC 服务器时加上以下选项：

```bash
vncserver -fp "built-ins"
```

## 也许有用

### 具有依赖关系的作业

- 将以下内容加入 `~/.bashrc` 文件（该文件可能不存在，必要时请创建）：

```bash
function qsubchain() {
if [ $# -lt 2 ]; then
  echo "Usage: qsubchain jobscript1 jobscript2 [...]"
  return
fi

thejobids=""
depend=""
while [ $# -gt 0 ]; do
  thejobid=`sbatch $depend $1 | sed -e 's/Submitted batch job *//'`
  thejobids="$thejobids $thejobid"
  depend="--dependency=afterok:$thejobid"
  shift
done
echo "JobIDs: $thejobids"
unset depend thejobid thejobids
}
```

- 之后即可一次提交两个或更多作业脚本，其中第二个作业仅在第一个作业完成后启动，依此类推：

```bash
$ qsubchain jobscript1 jobscript2
JobIDs:  43693 43694
```
