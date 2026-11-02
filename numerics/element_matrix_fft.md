---
title: "单元矩阵 FFT"
nav_order: 4
parent: "数值方法与工具"
layout: default
render_with_liquid: false
---

# 单元矩阵组装

## 概述

`mod_elt_matrix_fft.f90` 计算单个有限元对全局稀疏矩阵与右端向量的贡献。它在外层组装循环中每个单元被调用一次，
该循环位于 `matrix/construct_matrix_mod.f90`。

**签名**（与物理模型无关的接口）：

```fortran
subroutine element_matrix_fft(element, nodes, xpoint2, xcase2,           &
                R_axis, Z_axis, psi_axis, psi_bnd, R_xpoint, Z_xpoint,   &
                ELM, RHS, tid,                                           &
                ELM_p, ELM_n, ELM_k, ELM_kn, RHS_p, RHS_k,               &
                eq_g, eq_s, eq_t, eq_p, eq_ss, eq_st, eq_tt,             &
                delta_g, delta_s, delta_t,                               &
                i_tor_min, i_tor_max, aux_nodes, ELM_pnn, get_terms)
```


几何／物理参数（`xpoint2`、`xcase2`、`R_axis` 等）是与具体模型相关的输入，
用于描述平衡位形，并原样传入弱形式求值过程。
`eq_g/s/t/p/ss/st/tt` 与 `delta_g/s/t` 是预先分配的工作数组
（大小 `n_plane × n_var × n_gauss × n_gauss`），用于场合成；
它们由外层组装循环传入，以避免反复分配。`tid` 是 OpenMP 线程标识。

**输出**——`ELM(DIM0, DIM0)` 与 `RHS(DIM0)`，其中
`DIM0 = n_tor × n_vertex_max × n_degrees × n_var`。
它们直接对应全局 BCOO 矩阵中的密集 $b \times b$ 块；块布局见
[稀疏矩阵格式](sparse-matrix.md)。

**FFT 工作区**——`ELM_p`、`ELM_n`、`ELM_k`、`ELM_kn`、`ELM_pnn`
（大小 `n_plane × DIM1 × DIM1`，`DIM1 = n_vertex_max × n_var × n_degrees`）以及
`RHS_p`、`RHS_k`（大小 `n_plane × DIM1`），用于存放 FFT 路径中逐平面的 Gauss 求和结果。它们由调用方声明并传入，
从而在多个单元之间复用存储，无需重新分配。

---

## 场的表示

JOREK 把三维场表示为环向角 $\phi$ 上的傅里叶级数：

$$f(R, Z, \phi) = \sum_{n=0}^{n_\text{tor}-1} f_n(R, Z) \cdot H_n(\phi)$$

傅里叶基 $H_n(\phi)$ 由实值余弦与正弦谐波组成，
按顺序连续存放：

```text
index in n_tor:   1      2        3        4        5      ...
                  n=0   n=n₁(c)  n=n₁(s)  n=n₂(c)  n=n₂(s) ...
```

数组 `HZ(in, mp)` 存放第 `in` 个谐波在第 `mp` 个
环向平面（`n_plane` 个等距角之一，覆盖整个周期域）上的值。
数组 `mode(in)` 存放与每个谐波对应的整数模数
（`in=1` 时为 0，`in=2,3` 时为 $n_1$，依此类推）。

极向方向使用双三次 Hermite 基函数 $H_{i,j}(R,Z)$
（顶点 $i$、Hermite 自由度 $j$）。完整的三维基是二者的乘积
$H_{i,j}(R,Z) \times H_n(\phi)$。

---

## 计算路径

该例程在运行时于两条路径之间选择：

```fortran
if (i_tor_min == 1 .and. i_tor_max == n_tor) then
    use_fft = (n_tor >= n_tor_fft_thresh)   ! global matrix: FFT if many modes
else
    use_fft = .false.                        ! harmonic sub-matrix: always direct
end if
```

`n_tor_fft_thresh` 是 namelist 参数（默认 2）；它也可由各模型按需覆盖。

---

## 直接谐波路径（`use_fft = .false.`）

用于 `n_tor` 较小的情况，或为块谐波预条件器构造单个谐波子矩阵时。

```text
n_tor_start = i_tor_min,  n_tor_end = i_tor_max
HHZ = HZ          (actual Fourier values at each plane)
```

**循环结构：**

```text
for (ms, mt)        — n_gauss² poloidal Gauss points
  for mp = 1..n_plane
    synthesise fields at (ms, mt, mp)                  [eq_g, eq_s, …]
    for im = i_tor_min..i_tor_max                      [test mode]
      compute test basis  v = H(i,j,ms,mt) × HZ(im,mp)
      for (k,l) in n_vertex × n_degrees                [trial DOF]
        for in = i_tor_min..i_tor_max                  [trial mode]
          compute trial basis ψ = H(k,l,ms,mt) × HZ(in,mp)
          evaluate weak form → amat
          ELM(row(im), col(in)) += w × amat            [direct scatter]
```

环向积分以对全部 $n_\text{plane}$ 个平面及全部模式对 $(im, in)$ 的显式求和实现。
每个单元的开销：

$$\mathcal{O}\!\left(n_\text{gauss}^2 \times n_\text{plane} \times n_\text{tor}^2 \times n_\text{DOF}^2 \right)$$

其中 $n_\text{DOF} = n_\text{vertex} \times n_\text{degrees} \times n_\text{var}$。

---

## FFT 路径（`use_fft = .true.`）

当 `n_tor >= n_tor_fft_thresh` 时，用于全局单一（monolithic）矩阵。

```text
n_tor_start = n_tor_end = 1       (mode loop runs once)
HHZ = 1.0                         (no Fourier factor during integration)
```

该算法分两个阶段。

### 阶段 1 — 物理空间 Gauss 积分

```text
for (ms, mt)        — n_gauss² poloidal Gauss points
  for mp = 1..n_plane                                 [toroidal planes]
    synthesise fields at (ms, mt, mp)                  [eq_g, eq_s, …]
    compute test basis  v = H(i,j,ms,mt) × 1           [HHZ = 1]
    for (k,l) in n_vertex × n_degrees                  [trial DOF]
      compute trial basis ψ = H(k,l,ms,mt) × 1
      evaluate weak form:
        amat    → ELM_p(mp, trial_DOF, test_var) += w × amat
        amat_n  → ELM_n(mp, …)                  += w × amat_n
        amat_k  → ELM_k(mp, …)                  += w × amat_k
        amat_kn → ELM_kn(mp, …)                 += w × amat_kn
        amat_nn → ELM_pnn(mp, …)                += w × amat_nn
```

这五个逐平面缓冲区按双线性形式中出现的环向导数个数
区分贡献：

| 缓冲区 | 散射时的因子 | 含义 |
| --- | --- | --- |
| `ELM_p` | $1$ | 两侧均无环向导数 |
| `ELM_n` | $\text{mode}(m)$ | 试探函数上有 $\partial_\phi$ |
| `ELM_k` | $\text{mode}(k)$ | 测试函数上有 $\partial_\phi$ |
| `ELM_kn` | $\text{mode}(k)\cdot\text{mode}(m)$ | 两侧均有 $\partial_\phi$ |
| `ELM_pnn` | $\text{mode}(m)^2$ | 试探函数上有 $\partial_\phi^2$ |

之所以需要这样拆分，是因为 $\partial_\phi H_n(\phi)$ 会改变
谐波的余弦／正弦类型，并引入一个模数因子。

阶段 1 之后，每个缓冲区对每一对（测试自由度，试探自由度）都持有一个实值信号，
该信号在 `n_plane` 个等距环向角上采样。

### 阶段 2 — FFT 与谐波散射

对每一对（测试自由度，试探自由度）及每个缓冲区：

```text
in_fft = ELM_p[1:n_plane]
out_fft = r2c_FFT(in_fft)           ← dfftw_execute_dft_r2c  or  my_fft

for each (row mode k, col mode m):
    l = (k-1) + (m-1)    ← sum
    l = (k-1) - (m-1)    ← difference
    ELM[index_k, index_m] += ±Re/Im(out_fft[l+1]) × factor
```

实数到复数 DFT 由两个后端之一执行，在编译期通过
`USE_FFTW` 预处理宏选择：

- **FFTW**（定义了 `USE_FFTW`，推荐）——调用
  `dfftw_execute_dft_r2c(fftw_plan, in_fft, out_fft)`。计划句柄
  `fftw_plan`（存放在 `phys_module` 中）在启动时用
  `dfftw_plan_dft_r2c_1d` 为长度为 `n_plane` 的变换创建一次。FFTW
  \[[Frigo & Johnson, 2005](https://doi.org/10.1109/JPROC.2004.840301)\]
  在创建计划时会针对给定的 `n_plane` 自动选择最高效的算法；因此
  建议把 `n_plane` 取为小素数的乘积（2 的幂最优）。

- **内部兜底实现**（未定义 `USE_FFTW`）——调用 `my_fft`，一个为可移植性而内置的简单
  DFT 实现。其复杂度为 $\mathcal{O}(n_\text{plane}^2)$，
  仅用于测试或无法获得 FFTW 的平台。

该机制源于三角函数的积化和差恒等式。记
$\hat{f}_l = \text{DFT}(f)_l$（采用 r2c 约定
$\text{Re}(\hat{f}_l) = \int f\cos(l\phi)\,\mathrm{d}\phi$，
$\text{Im}(\hat{f}_l) = -\int f\sin(l\phi)\,\mathrm{d}\phi$），
则模式对 $(k, m)$ 处 `ELM` 的四个余弦／正弦子元素为：

$$\begin{aligned}
(\cos_k,\,\cos_m):\quad & +\operatorname{Re}(\hat{f}_{k+m}) + \operatorname{Re}(\hat{f}_{k-m}) \\
(\sin_k,\,\cos_m):\quad & -\operatorname{Im}(\hat{f}_{k+m}) - \operatorname{Im}(\hat{f}_{k-m}) \\
(\cos_k,\,\sin_m):\quad & -\operatorname{Im}(\hat{f}_{k+m}) + \operatorname{Im}(\hat{f}_{k-m}) \\
(\sin_k,\,\sin_m):\quad & -\operatorname{Re}(\hat{f}_{k+m}) + \operatorname{Re}(\hat{f}_{k-m})
\end{aligned}$$

四种情形读取的都是同样的两个 FFT 频点 $l = (k-1) \pm (m-1)$；
区别只在于使用 Re 还是 Im，以及符号如何。代码对 $l \ge 0$ 显式写出这四种加法，
而对 $l < 0$ 借助共轭对称性 $\hat{f}_{-l} = \overline{\hat{f}_l}$ 处理（它会翻转
Im 的符号）。五个缓冲区各自独立贡献，并各自按对应的模数因子缩放。

**每个单元的开销：**

$$\text{Phase 1: }\mathcal{O}\!\left(n_\text{gauss}^2 \times n_\text{plane} \times n_\text{DOF}^2\right)$$

$$\text{Phase 2: }\mathcal{O}\!\left(n_\text{tor}^2 \times n_\text{DOF}^2\right)$$

由于 $n_\text{plane} \approx 2\,n_\text{tor}$，阶段 1 随
$n_\text{tor}$ 线性增长而非二次增长，在高模数下可带来可观的节省。

---

## 数据流图

```text
 nodes (DOF values)
        │
        ▼
 ┌─────────────────────────────────┐
 │  Field synthesis  (eq_g/s/t/…)  │  n_plane × n_gauss² × n_var
 │  IFFT-like:                     │
 │  eq(mp,var,ms,mt) =             │
 │    Σ_{in,j} val × H × HZ(in,mp) │
 └───────────────┬─────────────────┘
                 │
        ┌────────┴────────┐
        │ direct path     │ FFT path
        │ (small n_tor)   │ (large n_tor)
        │                 │
        ▼                 ▼
 ELM directly      per-plane buffers
 at each           ELM_p / ELM_n
 mode pair         ELM_k / ELM_kn
 (k, m)            ELM_pnn
                       │
                       │  r2c FFT per (DOF pair, buffer)
                       ▼
                   out_fft[l]
                       │
                       │  scatter at l = (k-1) ± (m-1)
                       ▼
                  ELM[mode k, mode m]
```

---

## 源文件对照

| 文件 | 作用 |
| --- | --- |
| `models/model600/mod_elt_matrix_fft.f90` | 完整物理实现，model 600 为参考版本 |
| `models/model*/mod_elt_matrix_fft.f90` | 各模型变体（接口相同） |
| `models/phys_module.f90` | `HZ`、`mode`、`n_tor_fft_thresh`、`fftw_plan` |
| `gauss/basis_at_gaussian.f90` | 预先计算的 Gauss 点处 `H`、`H_s`、`H_t` 等 |
| `models/mod_settings.f90` | 编译期 `n_plane`、`n_order`、`n_tor` |
| FFTW 库 | [fftw.org](https://www.fftw.org) —— Frigo & Johnson, *Proc. IEEE* 93(2), 2005 |



