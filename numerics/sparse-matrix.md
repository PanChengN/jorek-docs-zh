---
title: "稀疏矩阵格式"
nav_order: 5
parent: "数值方法与工具"
layout: default
render_with_liquid: false
---

# 稀疏矩阵格式

JOREK 中所有线性代数的核心数据结构是 `type_SP_MATRIX`，
定义在 `datatypes/mod_sparse_matrix.f90` 中。
**主存储格式为块坐标格式（BCOO, block coordinate）**：非零元以密集 $b \times b$ 块的扁平列表存储，
在标量层面共用同一套 `irn`/`jcn`/`val` 数组。块 CSR 视图（`iblockptr`）按需从 BCOO 数据导出，供迭代求解器与 GPU 路径使用。

---

## 块结构与自由度

JOREK 使用双三次 Hermite 有限元。每个物理网格节点携带
$n_\text{dof} = n_\text{dof,1D}^2$ 个 Hermite 自由度索引，对应该处的函数值及其极向导数（$\partial_R$、$\partial_Z$、
$\partial_R\partial_Z$）。对默认的三次阶数（`n_order = 3`），每个物理节点有
$n_\text{dof} = 2^2 = 4$ 个 Hermite 自由度索引。每个 Hermite
自由度索引在全局矩阵中占据独立的**块行**，大小为 $b$——因此矩阵中的
"节点 $i$" 始终指 Hermite 自由度索引 $i$，而不是物理网格点。

块大小与全局矩阵维数为

$$b = n_\text{var} \times n_\text{tor}, \qquad
n_\text{global} = N_\text{unique} \times b$$

其中 $n_\text{var}$ 是 MHD 变量个数，$n_\text{tor}$ 是保留的环向傅里叶模数，
$N_\text{unique}$ 是唯一 Hermite 自由度索引的数目。乘积 $b$ 存放在 `a_mat%block_size` 中。

**轴共享。** 在磁轴上，全部 $N_\text{axis}$ 个轴节点共用一个函数值 Hermite 自由度索引（全局索引 1）。它们的导数自由度索引（$\partial_R$、$\partial_Z$、$\partial_R\partial_Z$）仍按节点各自独立。
与不带磁轴的网格相比，这节省了 $N_\text{axis} - 1$ 个索引：

$$N_\text{unique}
  = N_\text{nodes} \times n_\text{dof} - (N_\text{axis} - 1)$$

其中 $N_\text{nodes}$ 是物理网格节点数，$N_\text{axis}$ 是轴节点数。代码以所有节点上
Hermite 自由度索引的最大值隐式计算 $N_\text{unique}$：

```fortran
ng = max(node%index) * block_size  ! = N_unique * b
```

**块行** $i$ 对应 Hermite 自由度索引 $i$。对每个通过有限元模板与 $i$ 耦合的
Hermite 自由度索引 $j$，该块行都有一个 $b \times b$ 非零块。块行
$i$ 中非零块的个数是 `ijA_size(i)`；所有块行中的最大值是 `maxsize`。

### 自由度排序与索引映射

自由度（Hermite 自由度索引 $i$、变量 $v$、环向分量 $t$）的标量行（或列）索引为

$$\text{idx}(i,\,v,\,t) \;=\; (i-1)\,b \;+\; (v-1)\,n_\text{tor} \;+\; t$$

变量变化最慢（步长 $n_\text{tor}$），环向模数变化最快
（步长 1）。下图给出一个小例子（$N_\text{unique} = 3$、$n_\text{var} = 2$、$n_\text{tor} = 3$、$b = 6$）的布局：

```
 ┌───┬───┬───┬───┬───┬───┐     ┌───┬───┬───┬───┬───┬───┐     ···
 │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │     │ 7 │ 8 │ 9 │10 │11 │12 │     ···
 ├───┴───┴───┼───┴───┴───┤     ├───┴───┴───┼───┴───┴───┤     ···
 │   var 1   │   var 2   │     │   var 1   │   var 2   │     ···
 ├───────────┴───────────┤     ├───────────┴───────────┤     ···
 │    Hermite DOF 1      │     │    Hermite DOF 2      │     ···
 ├───────────────────────┘     └───────────────────────┘
 │                       Node 1                              ···
 └──────────────────────────────────────────────────────
```

行与列采用相同的排序。因此一个 $b \times b$ 块
$B(i,j)$ 分解为 $n_\text{var} \times n_\text{var}$
个大小为 $n_\text{tor} \times n_\text{tor}$ 的子块，每个变量耦合对一个：

```
 Block B(node i, node j)

           ← var 1 →   ← var 2 →   ···  ← var n_var →
         ┌───────────┬───────────┬─────┬────────────┐
 var 1   │    Bψψ    │    Bψu    │     │    BψT     │
         ├───────────┼───────────┼─────┼────────────┤
 var 2   │    Buψ    │    Buu    │     │    BuT     │
         ├───────────┼───────────┼─────┼────────────┤
 ...     │           │           │ ... │            │
         ├───────────┼───────────┼─────┼────────────┤
 var Nv  │    BTψ    │    BTu    │     │    BTT     │
         └───────────┴───────────┴─────┴────────────┘

 Each sub-block is n_tor × n_tor and encodes how one MHD variable at
 node i couples to one MHD variable at node j across all retained
 toroidal Fourier components.
```

---

## 主格式：块 COO（BCOO）

### 标量级数组

| 数组 | 大小 | 内容 |
| --- | --- | --- |
| `irn` | `nnz` | 每个标量非零元的全局标量行索引（以 1 为基） |
| `jcn` | `nnz` | 每个标量非零元的全局标量列索引（以 1 为基） |
| `val` | `nnz` | 每个标量非零元的数值 |

块在这些数组中**连续**存放：第 $k$ 个块（以 1 为基）
占据三个数组中从 $(k-1)b^2 + 1$ 到 $k b^2$ 的位置。
块内 $b^2$ 个元素按**行主序**排列
（局部行变化慢，局部列变化快）：
块的元素 $(r, c)$ 位于距块起点的偏移 $b(r-1) + c$ 处。
块本身的顺序是任意的（COO），不过实际组装是按行进行的，因此同一块行的块在存贮中连续出现。

### 块级结构数组

| 数组 | 大小 | 内容 |
| --- | --- | --- |
| `ijA_size` | `my_ind_size` | 块行 $i$ 中非零块的个数 |
| `irn_jcn` | `my_ind_size × maxsize` | `irn_jcn(i,k)` 是块行 $i$ 第 $k$ 个非零块的**块列索引** |
| `ijA_index` | `my_ind_size × maxsize` | `ijA_index(i,k)` 是块行 $i$ 第 $k$ 个非零块首元素在 `val` 中的**以 1 为基的标量位置** |

这三个数组提供了对 BCOO 列表的随机访问视图，无需依赖排序。

### 状态标志

| 标志 | 置位条件 |
| --- | --- |
| `bcsr_mapped` | 已计算 `iblockptr` 与 `jcn_block` |
| `device_mapped` | 矩阵数组已在 GPU 上分配 |
| `scaled` | 已施加对角行／列缩放 |
| `equilibrated` | 已施加完全均衡缩放 |

---

## 存储布局：算例演示

下面的例子使用 **3 个块行、3 个块列，b = 2**，
得到 $n_\text{global} = 6$ 和 7 个非零块（$\text{nnz} = 7 \times 4 = 28$）。

### 1 — 块级稀疏模式

```
         bcol 1   bcol 2   bcol 3
       ┌────────┬────────┬────────┐
brow 1 │ B(1,1) │ B(1,2) │        │
       ├────────┼────────┼────────┤
brow 2 │ B(2,1) │ B(2,2) │ B(2,3) │
       ├────────┼────────┼────────┤
brow 3 │        │ B(3,2) │ B(3,3) │
       └────────┴────────┴────────┘
```

### 2 — 扁平 BCOO：val / irn / jcn

第 $k$ 个块占据三个数组中从 $(k-1)\,b^2+1$ 到 $k\,b^2$ 的位置。

```
 ┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
 │ B(1,1)  │ B(1,2)  │ B(2,1)  │ B(2,2)  │ B(2,3)  │ B(3,2)  │ B(3,3)  │
 └─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┘
    ^1         ^5        ^9        ^13       ^17       ^21       ^25
  block 1    block 2   block 3   block 4   block 5   block 6   block 7
```

放大到第 1 个块——B(1,1) 按其 $b^2 = 4$ 个标量以**行主序**存放：

```
 position in val:   1     2     3     4
 val:              a₁₁   a₁₂   a₂₁   a₂₂   (aᵢⱼ = entry at local row i, col j)
 irn:               1     1     2     2     (global scalar row)
 jcn:               1     2     1     2     (global scalar col)
```

### 3 — 块结构数组

`ijA_size`、`irn_jcn` 和 `ijA_index` 提供对扁平
BCOO 列表的随机访问，无需依赖排序：

```
 brow │ ijA_size │  irn_jcn(brow, :)  │  ijA_index(brow, :)
──────┼──────────┼────────────────────┼─────────────────────
  1   │    2     │   1    2           │    1    5
  2   │    3     │   1    2    3      │    9   13   17
  3   │    2     │   2    3           │   21   25
```

`irn_jcn(i,k)` 是所耦合节点的全局块节点索引（= 块列号）。
`ijA_index(i,k)` 是该块起始处 `val` 中以 1 为基的标量位置——
例如 `ijA_index(2,3) = 17` 表示 B(2,3) 从 `val(17)` 开始，因此其元素
$(r,c)$ 位于 `val(17 + b*(r-1) + c - 1)`。

### 4 — 导出的 BCSR：iblockptr

经过 `set_block_csr_permutations` 之后，`iblockptr` 把同一份 BCOO 数据表达为块上的 CSR 行指针：

```
 iblockptr:   1               3                      6               8
              │               │                      │               │
              ▼               ▼                      ▼               ▼
 flat list: [ B(1,1) B(1,2) | B(2,1) B(2,2) B(2,3) | B(3,2) B(3,3) ]
              └─ brow 1 ──┘   └──── brow 2 ──────┘   └─ brow 3 ──┘
```

块行 $i$ 拥有扁平列表位置 `iblockptr(i)` … `iblockptr(i+1)−1`，
因此 `bcsr_matv` 的内层循环可直接以每块 $b^2$ 的固定偏移在 `val` 上跨步。

---

## 导出格式：块 CSR（BCSR）

BCSR 视图在首次需要时（标志 `bcsr_mapped`）由
`matrix/sorting_module.f90` 中的 `set_block_csr_permutations()` 惰性计算。

### 转换做了什么

`set_block_csr_permutations` 遍历扁平 BCOO 块列表，
统计每个块行拥有多少个块：

```fortran
do i = 1, nnz_blocks
    i_glob   = (i - 1)*b*b + 1               ! first scalar entry of block i
    j        = (irn(i_glob) - offset)/b + 1  ! block row of block i
    jcn_block(i) = jcn(i_glob)/b + 1         ! block column of block i
    iblockptr(j+1) = iblockptr(j+1) + 1
end do
! prefix-sum iblockptr → CSR row pointers
```

会分配并填充两个新数组：

| 数组 | 大小 | 内容 |
| --- | --- | --- |
| `iblockptr` | `my_ind_size + 1` | 块 CSR 行指针：块行 $i$ 拥有块 `iblockptr(i)` … `iblockptr(i+1)-1` |
| `jcn_block` | `nnz_blocks` | BCSR 枚举中第 $j$ 个块的块列索引 |

`val`、`irn` 和 `jcn` 数组**不重排**；`iblockptr` 只是把既有的 BCOO 顺序表达为 CSR 结构。这样做之所以正确，是因为前缀和构造按顺序分配块索引区间，
所以只有当扁平 BCOO 列表已**按块行排序**时——即第 1 行的所有块都在第 2 行的所有块之前，依此类推——它才会产生有效的指针。
这一顺序由逐行的有限元组装保证。

### 标量 CSR 

需要时（例如 PaStiX），由 `convert_sorting()` 另行执行一次标量 CSR 转换。该例程：

1. 在每个标量行内把 `jcn` 与 `val` 按列号升序排序。
2. 用所得的标量 CSR 行指针**就地**覆写 `irn(1:nr+1)`
   （内部先算在局部数组中，再拷入）。

该调用之后 `irn` 不再存放行索引——其前 `nr+1` 个元素此刻是标量 CSR 行指针。`irn` 中 `nr+1` 之后的其余元素已失效，不应读取。注意 `a_mat%iptr` 是另一个独立的数组指针，**不**由 `convert_sorting` 设置；需要在 `iptr` 名下取得行指针的调用方必须显式复制或做别名。

---

## MPI 分布

矩阵按**块行**分布到各 MPI 进程：每个进程拥有一段连续且互不重叠的块行，
并存储落在这些行中的所有非零元。列索引（`jcn`、`jcn_block`）始终是全局的——
本地行可以与完整矩阵中任意一列耦合，不论该列所在的行由哪个进程拥有。

### 划分

```text
rank 0       rank 1       rank 2         ...     rank P-1
┌──────────┐ ┌──────────┐ ┌──────────┐          ┌──────────┐
│ brow  1  │ │ brow K₀+1│ │ brow K₁+1│          │ brow K   │
│   ...    │ │   ...    │ │   ...    │    ...   │   ...    │
│ brow K₀  │ │ brow K₁  │ │ brow K₂  │          │ brow Nᵤ  │
└──────────┘ └──────────┘ └──────────┘          └──────────┘
 my_ind_min   my_ind_min   my_ind_min             my_ind_min
 = 1          = K₀+1       = K₁+1                = K+1
```

每个进程的范围是 `[my_ind_min, my_ind_max]`（以 1 为基的块行索引）。
全局目录数组 `index_min(1:ncpu)` 与 `index_max(1:ncpu)` 让任意进程都能算出其他进程的范围。

本地标量行数与索引偏移直接由此得到：

$$n_r = \texttt{my_ind_size} \times b, \qquad
  \text{offset} = (\texttt{my_ind_min} - 1) \times b$$

其中 $b$ 是块大小。全局标量行索引 $g$ 映射为本地标量行 $g - \text{offset}$。

### 组装

组装完全是本地的：每个进程遍历自己的单元集，在累加贡献之前检查某测试函数块行是否落在 `[my_ind_min, my_ind_max]` 内。矩阵填充过程中不需要进程间通信。

### 分布模式

| 字段 | 类型 | 含义 |
| --- | --- | --- |
| `ng` | integer | 全局标量维数 $n_\text{global}$ |
| `nr` | integer | 本地拥有的标量行（`my_ind_size × b`） |
| `nc` | integer | 本地拥有的标量列（行分布时等于 `ng`） |
| `nnz` | integer | 本地拥有的标量非零元个数 |
| `my_ind_min`, `my_ind_max` | integer | 本进程的闭区间块行范围 |
| `my_ind_size` | integer | `my_ind_max − my_ind_min + 1` |
| `index_min(:)`, `index_max(:)` | integer(ncpu) | 所有进程的块行范围 |
| `ncpu` | integer | MPI 进程数 |
| `comm` | integer | MPI 通信器 |
| `row_distributed` | logical | `.true.`——按行划分（标准的瞬态矩阵） |
| `col_distributed` | logical | `.true.`——列也划分（PaStiX 路径） |
| `reduced` | logical | `.true.`——完整矩阵在所有进程上各存一份 |

全局瞬态矩阵的标准配置是
`row_distributed = .true.`、`col_distributed = .false.`、`reduced = .false.`。

**`col_distributed`** 为 PaStiX 直接求解器而设，该库要求输入为列分布的 CSR。`convert_sorting()` 之后 `irn` 被标量 CSR 行指针覆写，列划分信息用于确定本地列范围。

**`reduced`** 用于必须在每个进程上都有完整副本的矩阵
（例如某些预条件器子矩阵）。此模式下 `nnz` 统计的是全局非零元个数，`irn`/`jcn`/`val` 在每个进程上都保存完整矩阵。

---

## 各类使用方所采用的格式

| 使用方 | 格式 | 关键数组 |
| --- | --- | --- |
| 直接组装／有限元例程 | BCOO | `irn`, `jcn`, `val`, `ijA_size`, `irn_jcn`, `ijA_index` |
| 矩阵—向量乘积（CPU） | BCOO / BCSR | `iblockptr`, `irn`, `jcn`, `val` |
| 矩阵—向量乘积（GPU） | 标量 CSR / BCSR | `iblockptr`, `iptr`/`irn`, `jcn`, `val` |
| MUMPS 直接求解 | 标量 COO（行分布） | `irn`, `jcn`, `val` |
| PaStiX 直接求解 | 标量 CSR（列分布） | `iptr`, `jcn`, `val` |
| STRUMPACK 直接求解 | 标量 COO | `irn`, `jcn`, `val` |
