---
title: "编译"
nav_order: 1
parent: "编译与依赖库"
grand_parent: "编译与运行"
layout: default
render_with_liquid: false
---

# 编译 JOREK

**本页说明编译 JOREK 所需的依赖库、构建选项及其他组成部分。在自行编译任何依赖之前，先确认你的 HPC 系统上是否已提供以模块形式准备好的依赖库。**

**向在相关机器上工作的同事询问他们推荐的模块与配置，并查阅 [HPC 与 PC 配置](hpc_pc_configurations.md) 一节了解针对具体系统的说明。**

- **从 git 仓库检出代码**，方法见[此处](../get_jorek.md)。
- **编译 JOREK**，方法见本页末尾。

## 专题指南

- [在 macOS 上编译](./hpc_pc_configurations/macos.md)
- [编译 MUMPS（+METIS）](./compiling_mumps.md)
- [以 64 位整数编译](./compiling_int64.md)
- [不使用 Intel MKL 编译全部依赖库](./compiling_wo_mkl.md)

## SCOTCH

*Scotch 是一个用于图与网格／超图划分、图聚类以及稀疏矩阵排序的软件包。*

- [在此下载源代码](https://files.inria.fr/pastix/releases/) 或使用[包含 `libesmumps` 的版本](http://gforge.inria.fr/frs/download.php/file/28978/scotch_5.1.12b_esmumps.tar.gz)
- 目前推荐 5.1.12b 版；最近 6.0.4 版也能正常工作，但若每个环向谐波需要多个 MPI 任务则尚不适用（该功能将在 6.1.x 中加入）
- 用以下命令解压

```bash
tar -xvzf scotch_5.1.12b.tar.gz
```

- 在 `src/` 目录下创建配置文件 `Makefile.inc`
  - 通用示例见 `src/Make.inc/`
  - [适用于 JOREK 的示例（Scotch 5.1.12b）](exp_scotch.md)
- 编译该库：

```bash
make clean
make -j 8 scotch
make -j 8 ptscotch
```

## PaStiX（6.x 之前的版本）

*PaStiX 是一款基于直接法、用于超大规模稀疏线性系统的高性能并行求解器。它还提供自适应分块 iLU(k) 分解，可用作并行预条件器。*

- [在此下载源代码](https://files.inria.fr/pastix/releases/)
- **注意：PaStiX 修订号 3519 至 4030 存在缺陷，会导致内存消耗过大！**
- 用以下命令解压：

```bash
tar -xvjf pastix_5.2.3.tar.bz2
```

- 在 `src/` 目录下创建配置文件 `config.in`
  - 通用示例见 `src/config/`
  - [适用于 JOREK 的示例（PaStiX 修订号 4492）](exp_pastix.md)
  - 不要忘记取消注释 `config.in` 中 Options 项下的内存使用统计
- 编译该库：

```bash
make clean
make -j 8
make -j 8 install
```

- PaStiX 编译完成后可以对其安装进行验证：

```bash
# simplest example
make examples
mpirun -np <Nprocs> ./example/bin/simple -rsa matrix/small.rsa -t <nthreads> -v 4

# Calling PaStiX with separated steps (as in Jorek)
mpirun -np <Nprocs> ./example/bin/step-by-step -rsa matrix/small.rsa -t <nthreads> -v 4

# Calling PaStiX with several communicators (as in Jorek)
mpirun -np <Nprocs> ./example/bin/multi-comm -rsa matrix/small.rsa -t <nthreads> -v 4
```

## PaStiX 6

PaStiX 的新版本（带有块低秩压缩等新特性）。

- [在此下载源代码](https://gforge.inria.fr/frs/?group_id=186)（发行版本）
- [在此下载最新的 develop 版本](https://gitlab.inria.fr/solverstack/pastix)（git 下载方法见 Readme）
- [下载 2019/07 用于基准测试与 BLR 测试的版本的 tar.gz](assets/compiling/pastix6.tar.gz)
- 若非从 git 下载，则用以下命令解压：

```bash
tar -xvzf pastix-6.0.2.tar.gz
```

- 进入 PaStiX 6 主目录，创建 `build` 子目录，并用 CMake 构建。可设置多个选项，其中大部分会自动设定，但你或许需要指定排序库（Scotch 或 Metis）及其编译所用的编译器，以及安装前缀（PaStiX 6 的安装位置）。此时命令行参数如下（将 `...` 替换为相应路径）：

```bash
mkdir build
cd build
cmake .. -DSCOTCH_DIR=... -DCMAKE_C_COMPILER=... -DCMAKE_INSTALL_PREFIX=...
```

- 与之前的版本一样，现在也可以在 PaStiX 主目录下安装 PaStiX 6：

```bash
make clean
make -j 8
make -j 8 install
```

## FFTW

*JOREK 还使用 FFTW 进行快速傅里叶变换。该库通常可通过 `module load fftw` 在机器上获得。* 另见[此处](preprocessor.md)了解如何引入 FFTW。

## 编译 JOREK

我们使用 `Make` 编译 JOREK，并通过 `util/makedepend` 生成依赖关系。
详见 [Makefile](makefile.md)。

- **为你的系统创建 JOREK 配置文件 `trunk/Makefile.inc`**，示例见 `trunk/Make.inc/`。
- 添加以下各行以链接各依赖库：

```make
# SCOTCH Library: Automatically included via the pastix-conf script calls below

# PaStiX Library:
USE_PASTIX        = 1
USE_PASTIX_MURGE  = 1  # Different way for matrix assembly, the choice is up to you
PASTIX_HOME       = <path-to-pastix>/install/
LIB_PASTIX        = `$(PASTIX_HOME)/pastix-conf --libs`
LIB_PASTIX_MURGE  = `$(PASTIX_HOME)/pastix-conf --libs_murge`
LIB_PASTIX_BLAS   = `$(PASTIX_HOME)/pastix-conf --blas`
INC_PASTIX        = `$(PASTIX_HOME)/pastix-conf --incs`

# FFTW Library: FFTW_HOME might be set by "module load fftw", otherwise do so manually
LIBFFTW           = $(FFTW_HOME)/lib/libfftw3.a
```

- 对于修订号 3945 之后的 PaStiX，还需额外添加以下内容（另见[预处理器标志](preprocessor.md)）：

```make
FFLAGS := $(FFLAGS) -DFUNNELED -DWORLDWAR2
```

- 若使用 **PaStiX 6.x**，则需要正确设置 `USE_PASTIX6=1`、`PASTIX6_HOME`、`LIB_PASTIX6`、`LIB_PASTIX6_BLAS` 与 `INC_PASTIX6`，而不用上面列出的那些参数。此时 `USE_PASTIX` 必须为 0。

- 正确设置[硬编码参数](hard-coded_parameters.md)。例如：

```bash
./util/config.sh model=303 n_tor=3 n_period=8 n_plane=8   # set hard-coded parameters
./util/config.sh                                          # check hard-coded parameters
```

- 编译主程序和／或诊断工具：

```bash
make                       # compile main program jorek_modelxxx
make jorek2vtk
make jorek2_postproc
...
```

- 可以并行编译，例如使用 8 个线程：

```bash
make -j 8
```

### 单个源文件的特殊编译选项

- 现在可以为单个源文件指定特殊编译选项（追加到常规的 `FFLAGS`）。下例针对文件 `models/model333/element_matrix_fft.f90`（写入 `Makefile.inc`）：

```make
.obj/element_matrix_fft.o: FFLAGS+=-O3
```

### 备注

- **切换物理模型或硬编码参数时**，重新编译之前应始终执行 `make clean`。当不同模型下文件之间的依赖关系不同时（由预处理指令决定），`make clean` 并不足够，需要执行 `make cleanall`。`./util/config.sh` 已作调整，可自动完成这一操作。
- **编译器优化：**（初步内容——后续更新）
  - 在 Garching 本地 Linux 集群和超级计算机 Hydra 上的测试表明，最佳优化选项似乎就是 `-fast -DUSE_BLOCK`，无需再加 `-O2 -xSSE4.2` 之类的东西。两套系统均配备与 Helios 非常相似的 Intel Ivy Bridge 处理器。
