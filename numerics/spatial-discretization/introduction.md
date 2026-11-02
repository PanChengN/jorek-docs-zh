---
title: "空间离散简介"
nav_order: 3
parent: "空间离散"
layout: default
render_with_liquid: false
---

# JOREK 中的空间离散引言

JOREK 的离散方案在文献 [O. Czarny, G. Huysmans, J.Comput.Phys 227, 7423 (2008)](https://www.sciencedirect.com/science/article/pii/S0021999108002118) 与 [S. Pamela et al. J. Comput. Phys. 464, 111101 (2022)](https://www.sciencedirect.com/science/article/pii/S0021999122001632?via%3Dihub) 中有详尽描述。这里概述其中最重要的几个方面以及代码实现。

如[此处](/docs/physics/coordinates.html)所详述，JOREK 采用柱坐标 $(R,Z,\phi)$。极向平面（变量 $R$ 与 $Z$）上的离散采用二维贝塞尔有限元，见[下一节](#2d-bezier-finite-elements-in-the-poloidal-plane)；而沿环向（变量 $\phi$）的离散则采用截断的实傅里叶级数，见[本节](#toroidal-discretization-with-real-fourier-series)。

在有限元 $K$ 上，采用局部坐标系 $s,t$（见[贝塞尔曲面引言](introduction-to-bezier.md)），两种离散合并后写成：

$$
\mathbf{X}^{(K)}(s,t,\phi) = \left(\sum_{l=1}^{N_\text{tor}} Z_l(\phi) \left (\sum_{i = 1}^{N_\text{vert}}\sum_{j = 1}^{\text{dof}} h^{ij} \vec{u}^{ijl} b_{i,j}(s,t)\right) \right ) \tag{1}
$$

其中 $\mathbf{X}$ 为变量构成的向量（即 $\rho$、$T$、$u$ 等）。
对于极向几何变量 $R,Z$，有类似的关系：

$$
\begin{pmatrix}
R \\
Z
\end{pmatrix}^{(K)}
(s,t,\phi) 
= \left(\sum_{l=1}^{N_{\text{coord_tor}}} Z_l(\phi) \left (\sum_{i = 1}^{N_{vert}}\sum_{j = 1}^{\text{dof}} h^{ij} \vec{v}^{ijl} b_{i,j}(s,t)\right) \right ) \tag{2}
$$

内层括号为极向离散，使用基函数 $b_{i,j}$；$Z_l$ 则是环向离散的基函数。

注意，在构造网格时，$(2)$ 中的全部自由度 $\vec{v}^{ijl}$ 以及 $h^{ij}$（对 $(2)$ 和 $(1)$ 均是）都已固定。

### 表述中的参数
- $N_\text{tor}$（代码中为 `n_tor`）与 $N_\text{coord_tor}$（代码中为 `n_coord_tor`）是两个须在编译期指定的参数（见[本节](#toroidal-discretization-with-real-fourier-series)）
- $N_\text{vert}$ 固定为 $4$ 
- $\text{dof}$（`n_degrees`），即每个变量（如 $T$）在每个顶点处的自由度数，由多项式阶数 `n_order`（用户可选择）按下式确定：`n_degrees = ((n_order+1)/2)^2`。

## 极向平面上的二维贝塞尔有限元 <a id="2d-bezier-finite-elements-in-the-poloidal-plane"></a>
采用 $n$ 阶 $G_m$ 连续贝塞尔有限元对极向平面 RZ 进行离散。  
每个贝塞尔有限元是一个含 $n^2$ 个控制点的贝塞尔曲面，其中 $4$ 个为插值点。

贝塞尔曲面定义为

$$
\mathbf{X}(s,t) = \sum_{i=0}^{n} \sum_{j=0}^{n} \mathbf{P}_{ij}B_i^n(s) B_j^n(s)  \tag{3}
$$

其中 $\mathbf{P}_{ij}$ 为控制点，$B_i^n$ 与 $B_j^n$ 为伯恩斯坦（Bernstein）多项式，定义为：

$$
B_i^n(s) = \frac{n!}{i!(n-i)!} s^i (1-s)^n-1
$$

需要注意，$(3)$ 中的向量 $\mathbf{X}$ 同时包含几何变量（$R$ 与 $Z$）与物理变量（如 $\Psi$、$\rho$、$T$ 等），因此写成：

$$
\mathbf{X} = 
\begin{pmatrix}
R \\
Z \\
\Psi \\
\rho \\
T \\
\vdots
\end{pmatrix}
$$

不过在实际实现中，几何变量与物理变量被_解耦_为两套独立的表述。详见[这一段](#decoupling-geometrical-variables-and-physical-variables)。

关于贝塞尔曲面的更深入说明见[贝塞尔曲面引言](introduction-to-bezier.md)。

### 节点表述
通常自由度（此处即控制点）按面（此处即贝塞尔片）分组。JOREK 则按节点分组。每个贝塞尔曲面有 $4$ 个插值点，称为节点。这意味着其余所有控制点都被归属到某一个插值点上。  
确实，如[贝塞尔曲面引言](introduction-to-bezier.md)所示，每个控制点都与某个节点上的导数相关联。

在 JOREK 中，每个节点都定义一个局部向量基，归属于该节点的控制点用该基表示。 
例如对双三次贝塞尔曲面，节点 $\mathbf{P}\_{00}$ 的控制点可表示为：

$$
\begin{align}
\mathbf{P}_{0,0} &= \vec{u}^{00} \\
\mathbf{P}_{0,1} &= \vec{u}^{00} + \vec{u}^{01}\, h_{01} \\
\mathbf{P}_{1,0} &= \vec{u}^{00} + \vec{u}^{10}\, h_{10} \\
\mathbf{P}_{1,1} &= \mathbf{P}_{0,1} + \mathbf{P}_{1,0} - \vec{u}^{00} + \vec{u}^{11}\, h_{11} \\ 
\end{align} \tag{4}
$$

其中 $h^{ij}$ 称为_单元尺寸_，在网格构造阶段设定。

该表述的主要优点是使 $G_m$ 连续性的施加更为简便。当 $4$ 个片共享节点 $\mathbf{P}_{00}$ 时，$G_m$ 连续性通过以下方式施加：
1. 在全部 $4$ 个片之间共享局部基 $\{\vec{u}^{ij}\}_{ij}$。
2. 对 $h_{ij}$ 施加某些简单约束（见[极向离散](poloidal-discretization.md)）

利用 $(4)$（可推广到任意阶 $n$ 的贝塞尔曲线，见[极向离散](poloidal-discretization.md)），$(3)$ 可改写为

$$
\mathbf{X}_{\text{pol}}^{(K)} = \sum_{i=0}^{\text{n_vertices}} \sum_{j=0}^{\text{n_degrees}} h^{ij}\vec{u}^{ij} b_{ij}^n(s,t) \tag{5}
$$

其中 $b_{ij}$ 为新的基函数，由归并所有含 $\vec{u}^{ij}$ 的项得到。


### 几何变量与物理变量的解耦 {#decoupling-geometrical-variables-and-physical-variables}
至此，向量 $\mathbf{X}$ 同时包含几何变量与物理变量。但在实际实现中，两套表述被解耦为两个类似但独立的表述。原因何在？因为二者具有不同的_环向_离散。

两套表述分别为

$$
\mathbf{X}_\text{pol}^{(K)}(s,t) = \sum_{i=0}^{N_\text{vert}-1} \sum_{j=0}^{\text{dof_per_vertex}} h^{ij} \vec{u}^{ij} b_{ij}(s,t)
$$

以及

$$
\begin{pmatrix} R \\ Z
\end{pmatrix}
_\text{pol}^{(K)}(s,t) = \sum_{i=0}^{N_\text{vert}-1} \sum_{j=0}^{\text{dof_per_vertex}} h^{ij} \vec{v}^{ij} b_{ij}(s,t)
$$

其中 $\mathbf{X}$ 现在只指物理变量。

注意 $h^{ij}$ 是**相同的**

## 采用实傅里叶级数的环向离散 {#toroidal-discretization-with-real-fourier-series}
环向离散同时施加于物理变量与坐标变量。两者采用相同的方法，即截断的实傅里叶级数，但使用不同的参数（所含谐波数与谐波的周期性，见表后）。

采用实傅里叶级数（$\cos$、$\sin$），如下表所示：

| JOREK 谐波 | 环向模数 | 环向基函数 |
|--|--|--|
| 1 | 0 | 1 |
| 2 | $n_\text{period}$ | $\cos(n_\text{period}\phi)$ |
| 3 | $n_\text{period}$ | $\sin(n_\text{period}\phi)$ |
| 4 | $2n_\text{period}$ | $\cos(2n_\text{period}\phi)$ |
| 5 | $2n_\text{period}$ | $\sin(2n_\text{period}\phi)$ |
| ... | ... | ... |
| n_$\text{tor}-1$ | $\frac{n_\text{tor}-1}{2} n_\text{period}$ | $\cos(\frac{n_\text{tor}-1}{2}n_\text{period}\phi)$ |
| n_$\text{tor}$ | $\frac{n_\text{tor}-1}{2} n_\text{period}$ | $\sin(\frac{n_\text{tor}-1}{2}n_\text{period}\phi)$ |

对物理离散，使用**硬编码参数** `n_tor` 与 `n_period` 选择参与模拟的谐波：
  * `n_tor`：实傅里叶模的总数（奇数）
  * `n_period`：环向周期性（正整数）

对坐标／几何离散，以相同方式使用 `n_coord_tor` 与 `n_coord_period`。

模拟中包含的**最大环向模数**为 `n_max=(n_tor-1)/2*n_period`。  
需有**足够数量的环向平面**以避免混叠。通常的最低要求为 `n_plane >= 2 * n_tor`。对具体算例扫描 `n_plane` 以确保收敛始终是好做法。若不使用 FFTW，`n_plane` 必须为 2 的幂。若使用 FFTW（更多说明见[此处](/docs/compiling/cat_compiling.md)），`n_plane` 可为任意正整数，但并非所有取值下 FFTW 的效率都相同。

## 汇总：环向与极向离散
将两种离散结合后，极向自由度对每个极向模 $l$ 各复制一份。即自由度总数为

$$
N_{\text{dof}} = \text{n_tor} (d-2) \left( \frac{n+1}{2}\right)^2
$$

由此得到表述 $(1)$ 与 $(2)$。


## 代码实现
代码中有两个基本类型：`type_node` 与 `type_element`（见 `data_structure.f90`）。

`type_node` 在 `node%values` 数组中存放自由度 $\vec{u}^{ij}$（物理变量），在 `node%x` 数组中存放 $\vec{v}^{ij}$（坐标）。

`type_element` 存放每个顶点的尺寸 $h^{ij}$。

下面举例说明自由度与尺寸的存储方式。 

固定环向模数 $l \in [0, \text{n_tor}]$ 后，物理自由度可按如下方式访问：

$$
\begin{align}
&\texttt{node\%values(l,1,1)} \rightarrow p_k  \\
&\texttt{node\%values(l,2,1)} \rightarrow u_k  \\
&\texttt{node\%values(l,3,1)} \rightarrow v_k  \\
&\texttt{node\%values(l,4,1)} \rightarrow w_k 
\end{align}
$$

第一个下标为环向模，第二个下标为自由度，第三个下标为变量 

$$
\begin{align}
&\texttt{element\%size(k,1)} \rightarrow h^{00} := 1  \\
&\texttt{element\%size(k,2)} \rightarrow h^{10} \\
&\texttt{element\%size(k,3)} \rightarrow h^{01} \\
&\texttt{element\%size(k,4)} \rightarrow h^{11}
\end{align}
$$

$$
\begin{align}
 &\texttt{node\%x(1,\mu)} \rightarrow p_k  \\
 &\texttt{node\%x(2,\mu)} \rightarrow u_k  \\
 &\texttt{node\%x(3,\mu)} \rightarrow v_k  \\
 &\texttt{node\%x(4,\mu)} \rightarrow w_k 
\end{align}
$$

对全部 $\nu = 1\ldots N_{var}$、$i_G, j_G = 1\ldots N_{Gauss}$ 及 $p = 1\ldots N_{plane}$，给定有限元内变量在给定高斯点 $(s_{i_G}, t_{j_G})$、环向位置 $\phi_p$ 处的值可表示为

$$
\begin{align}
X_{\nu}(s_{i_G},t_{j_G},\phi_{p}) &= \sum_{k = 1}^{N_{vert}}\sum_{j = 1}^{N_{ord}}\sum_{l = 1}^{N_{tor}} \mathrm{nodes}(i)\text{\%}\mathrm{values}(l,j,\nu) \\
&\qquad \cdot \mathrm{H}(k,j,i_G,j_G) \cdot \mathrm{element}\text{\%}\mathrm{size}(k,j) \cdot \mathrm{HZ}(l,p)
\end{align}
\tag{9}
$$

上述记号与 $(1)$、$(2)$ 略有不同。事实上 $H(k,j,i_g,j_g):=b_{kj}(s_{i_g}, t_{j_g})$ 。此外 $HZ(l,p):=Z_l(\phi_p)$。

### 高斯点
对计算量大的部分，即积分，使用预先算好的基函数 $b_{ij}$ 在高斯点上的取值。 
这些值由 `basis_at_gaussian.f90` 中的 `initialize_basis()` 函数计算，该函数在代码启动时调用。

### 使用高阶有限元
使用高阶有限元（$n\geq 7$）时，必须在编译代码之前生成基函数文件及其在高斯点上的取值。为此须调用 `tools/util/generate_codes_for_norder_gt_7.py`。该文件开头有一些须设定的参数，例如 `n_order`。

### 其他例程
其他涉及贝塞尔有限元的例程包括完成映射 $(K, s,t) \rightarrow (R,Z)$ 的例程（`interp_RZP.f90`）及其逆映射（`find_RZ.f90`）。$K$ 为一个有限元。

#### interp_RZP.f90
直接使用表达式 $(2)$。某些重载版本还提供直至二阶的导数（含交叉导数）$\partial_s^i \partial_t^j R$ 与 $\partial_s^i \partial_t^j Z$。 

#### find_RZ.f90 
不存在通用的映射 $(R,Z) \rightarrow (s,t)$，因为 $(s,t)$ 是各单元 $K$ 的局部坐标。一般而言没有直接方法判断哪个单元包含 $(R_\text{find},Z_\text{find})$，因此构建一棵树。  
不再遍历所有单元来判断哪个包含 $(R_\text{find},Z_\text{find})$，而是将单元组织为四叉树（`mod_quadtree.f90`）。关于该数据结构，可参见[四叉树的维基百科页面](https://en.wikipedia.org/wiki/Quadtree)。  
四叉树给出的不是唯一一个包含 $(R_\text{find},Z_\text{find})$ 的单元，而是若干_潜在容器_单元。  

使用四叉树之后，对每个剩余单元用 Newton 法求解下述方程组：
$$
\begin{cases}
R(s,t) = R_\text{find} \\
Z(s,t) = Z_\text{find}
\end{cases}
$$

对每个这样的单元执行 20 次 Newton 迭代；若仍未找到该点，则换用另一个起点重试。  
所用起点硬编码于 `find_RZ.f90` 文件中。  
第一个达到收敛（即误差低于某阈值）的单元连同求得的解 `s` 与 `t` 一起返回。

