---
title: "随机数发生器"
nav_order: 6
parent: "数值方法与工具"
layout: default
render_with_liquid: false
---

# JOREK 中的随机数发生器

JOREK-particles 扩展需要大量随机数，例如在粒子初始化程序中。
为同时满足速度、统计质量和并行正确性三方面的要求，JOREK 使用 [PCG](http://www.pcg-random.org/) 系列伪随机数发生器，并可选配 Sobol' 准随机序列发生器。


## 为什么不使用 Fortran 内置 RNG？

Fortran 内在函数 `random_number` 存在若干局限，使其不适合 JOREK 的使用场景。
Fortran 内置的随机数发生器依赖编译器，且往往质量不高。此外它们不是线程安全的，若不加外部加锁，无法在 OpenMP 并行区中使用。
它们还没有提供跨步抽样（strided sampling）与跳进到特定值（jump-ahead）的功能。
而在不同 MPI 任务上生成相互关联的随机数集合时，这些特性非常有用。

## 实现

所有发生器共用一个抽象接口，定义在 `tools/mod_rng.f90` 中，因此在更换发生器时无需修改调用代码。该接口目前由以下实现提供：


- pcg32（`tools/mod_pcg32_rng.f90`，使用 `tools/mod_pcg32.f90` 与 `tools/pcg_basic.c`）
- Sobol 序列（`tools/mod_sobseq_rng.f90`，使用 `tools/mod_sobseq.f90`）

### 接口

RNG 接口的实现必须提供以下例程：

- `initialize(rng, n_dims, seed, n_streams, i_stream, ierr)`
- `next(rng, out)`
- `jump_ahead(rng, delta)`

其名称应是不言自明的。



## 用法

### `rng%initialize` 的参数：

| 参数 | 说明 |
|---|---|
| `n_dims` | 每次调用 `next` 所产生的随机数个数。 |
| `seed` | 发生器的整数种子。 |
| `n_streams` | 正在初始化的独立流的总数（跨所有线程与进程）。 |
| `i_stream` | 分配给本实例的流的索引，取值范围 `[1, n_streams]`。 |
| `ierr` | 成功时返回 0，失败时返回非零值。  |

### 串行场景

请参考以下串行场景（仅一个 OpenMP 线程）中的示例：

```fortran
  use mod_pcg32_rng
  use mod_random_seed
  real*8 :: rans(7)
  type(pcg32_rng) :: rng ! or class(type_rng), allocatable :: rng ! and allocate(pcg32_rng::rng)
  call rng%initialize(n_dims=7, seed=random_seed(), n_streams=1, i_stream=1, ierr=ifail)
  ! create 7 random numbers per call on 1 thread selecting the first stream
  
  call rng%next(rans)
```



### OpenMP 并行场景

在并行场景中，会定义若干条随机数流，每个线程选择其中一条。
下面的 OpenMP 示例改编自 `particles/examples/W_sputtering_rad_coll.f90`：

```fortran
  type(pcg32_rng), dimension(:), allocatable :: rng
  real*8 :: ran(6)
  integer :: n_stream, i_rng, i, j
  
  seed = random_seed()
  n_stream = 1
  !$ n_stream = omp_get_max_threads()
  allocate(rng(n_stream))
  do i=1,n_stream
    call rng(i)%initialize(6, seed, n_stream, i)
  end do
  
  !$omp parallel default(private), shared(rng)
  i_rng = 1
  !$ i_rng = omp_get_thread_num()+1
  
  !$omp do
  do j=1,size(particles,1)
    call rng(i_rng)%next(ran)
  end do
  !$omp end do
  !$omp end parallel
```

### MPI + OpenMP 混合场景

要在 MPI-OpenMP 混合架构下使用，需要跨处理器计算流的编号与索引。
结合上面的示例，用几个 MPI 调用即可轻松做到。

```fortran
  call MPI_COMM_RANK(MPI_COMM_WORLD, my_id, ierr)
  call MPI_COMM_SIZE(MPI_COMM_WORLD, n_cpu, ierr)

  ! Calculate a single random seed and communicate it over MPI
  if (my_id .eq. 0) seed = random_seed()
  call MPI_Bcast(seed, 1, MPI_INTEGER, 0, MPI_COMM_WORLD, ierr)

  ! Set up rngs
  n_threads = 1
!$ n_threads = omp_get_max_threads()
  allocate(rng(0:n_threads-1), source=pcg32_rng())
  n_streams = n_cpu*n_threads
  do i_thread=0, n_threads-1
    seq=my_id*n_threads + i_thread + 1
    call rng(i_thread)%initialize(5, seed, n_streams, seq, ierr)
    if(ierr .ne. 0) call MPI_ABORT(MPI_COMM_WORLD, -1, ierr)
  end do
``` 

### 播种

`tools/mod_random_seed.f90` 中提供了一个为发生器生成种子的模块，种子来自 `/dev/urandom`，或将时间与当前进程 pid 做异或得到。
若需要跨多次运行可复现（例如调试），请把 `random_seed()` 替换为固定的整数。

## Sobol' 序列 QRNG

`sobseq` 发生器有一些特性需要谨慎处理。

### 输出流的相关性

Sobol' 序列的优势在于输出流中的相关性，但这也会引起一些问题。
例如在 sobseq 发生器的第一条流中，每个偶数都 > 0.5。
这对并行中的拒绝采样有影响——在那里我们使用跨步发生器来提供多条流。非常重要的一点是：让每个线程尝试相同数量的样本，而不是追求相同数量的被接受提议。

### 跨步生成

由于 `sobseq` 发生器采用跨步实现，它只能接受 2 的幂次条数的流。

### 播种

Sobol' 序列无法用任意数值播种。调用 `rng%initialize` 时 `seed` 参数被忽略。



