---
title: "极向离散"
nav_order: 3
parent: "空间离散"
layout: default
render_with_liquid: false
---


# 极向离散

JOREK 在极向平面 $RZ$ 上采用等参 $G_m$ 连续贝塞尔有限元进行空间离散。它不把控制点当作“直接”自由度，而是采用另一种称为*节点表述*的表述（见[此处](#bezier-finite-element-nodal-representation)），这大大便于在多个有限元之间施加 $G_m$ 连续性。等参与 $G_m$ 连续（$m\in \mathbb{N}$）的含义稍后说明。

关于贝塞尔曲线、贝塞尔曲面的概览，以及如何由它们过渡到贝塞尔有限元的概念，见[贝塞尔曲面引言](introduction-to-bezier.md)

以参数 $s,t\in [0,1]$ 作为贝塞尔有限元的局部坐标，则单个 $n$ 阶贝塞尔有限元上的离散写成

$$
X_\text{pol}^{(K)}(s,t) = \sum_{i=0}^{n}\sum_{j=0}^{n} \mathbf{P}_{ij} B_i^n(s)B_j^n(t) \tag{3}
$$

其中 $B_i^n$ 与 $B_j^n$ 为伯恩斯坦多项式，$P_{ij}$ 为曲面的控制点。

如下一节所述，方程 $(3)$ 被改写为更方便的形式，即：

$$
X_\text{pol}^{(K)}(s,t) = \sum_{i=0}^{N_\text{vert}-1} \sum_{j=0}^{\text{dof_per_vertex}} h^{ij} \vec{u}^{ij} b_i(s,t)
$$

### 贝塞尔有限元的节点表述 {#bezier-finite-element-nodal-representation}
JOREK 采用贝塞尔有限元的一种特殊表述，称为节点表述。  
节点即插值点。在贝塞尔曲面上，无论选取何种多项式阶数，插值点恒为 $4$ 个。  
所谓节点表述，指自由度（即控制点）归属于节点（插值点）而非单元。此外，控制点按其所辅助的节点分组（大体上按与其相近的节点，见下一段的图示），再改写为该节点加上若干向量（这些向量才是新的自由度）：$\mathbf{P}\_{ij} = \mathbf{P}\_{00} + \sum_l c_l \vec{u}^l$。

当阶数 $n$ 为奇数时，每组有 $(n+1)^2/4$ 个点。JOREK 未对偶数 $n$ 定义节点表述。  
用于构造节点 $\mathbf{P}\_{00}$ 全部辅助控制点的向量构成该节点的局部向量基。

本节随后以双三次贝塞尔有限元为例说明，它是 JOREK 中用得最多的有限元。
接着讨论 JOREK 中实现的、推广到任意多项式阶数（不限于双三次）的**广义节点表述**，并说明在该表述上施加 $G_m$ 连续性更为简单。
最后简要说明为何选取这一特殊表述以及它的意义。

#### 双三次贝塞尔有限元的节点表述
该表述基于以下工作：[O. Czarny, G. Huysmans, J.Comput.Phys 227, 7423 (2008)](https://www.sciencedirect.com/science/article/pii/S0021999108002118)。

对双三次贝塞尔有限元，伯恩斯坦多项式基是三次伯恩斯坦多项式基的笛卡尔积。 

如下图所示，控制点被分为 4 组，用 4 种不同颜色区分：

$$
\begin{matrix}
\color{red}{30}      &&& \color{red}{31}      &&& \color{green}{32}      &&& \color{green}{33} \\
\color{red}{\times} &&& \color{red}{\bullet} &&& \color{green}{\bullet} &&& \color{green}{\times} \\ \\
\color{red}{20}      &&& \color{red}{21}      &&& \color{green}{22}      &&& \color{green}{23} \\
\color{red}{\bullet} &&& \color{red}{\bullet} &&& \color{green}{\bullet} &&& \color{green}{\bullet} \\ \\
10      &&& 11      &&& \color{blue}{12}      &&& \color{blue}{13} \\
\bullet &&& \bullet &&& \color{blue}{\bullet} &&& \color{blue}{\bullet} \\ \\
00      &&& 01      &&& \color{blue}{02}      &&& \color{blue}{03} \\
\times &&& \bullet &&& \color{blue}{\bullet} &&& \color{blue}{\times} \\ \\
\end{matrix}
$$

其中 $\times$ 表示节点（插值点），$\bullet$ 表示非插值控制点

然后对每组 $i$ 引入向量 $p_i, v_i, u_i$ 与 $w_i$，以及
某些预定义量 $h_{u,i}$ 与 $h_{v,i}$

$$
\begin{align}
\mathbf{P}_{0,0} &= p_1 \
\mathbf{P}_{0,1} &= p_1 + v_1\, h_{v,1} \\
\mathbf{P}_{1,0} &= p_1 + u_1\, h_{u,1} \\
\mathbf{P}_{1,1} &= P_{0,1} + P_{1,0} - p_1 + w_1\, h_{w,1} \\ \\
\mathbf{P}_{3,0} &= p_2 \\
\mathbf{P}_{3,1} &= p_2 + v_2\, h_{v,2} \\
\mathbf{P}_{2,0} &= p_2 + u_2\, h_{u,2} \\
\mathbf{P}_{2,1} &= P_{3,1} + P_{2,0} - p_2 + w_2\, h_{w,2} \\ \\
\mathbf{P}_{3,3} &= p_3 \\
\mathbf{P}_{3,2} &= p_3 + v_3\, h_{v,3} \\
\mathbf{P}_{2,3} &= p_3 + u_3\, h_{u,3} \\
\mathbf{P}_{2,2} &= P_{2,3} + P_{3,2} - p_3 + w_3\, h_{w,3} \\ \\
\mathbf{P}_{0,3} &= p_4 \\
\mathbf{P}_{0,2} &= p_4 + v_4\, h_{v,4} \\
\mathbf{P}_{1,3} &= p_4 + u_4\, h_{u,4} \\
\mathbf{P}_{1,2} &= P_{0,2} + P_{1,3} - p_4 + w_4\, h_{w,4}
\end{align}
\tag{4}
$$

特别地，拼接多个贝塞尔有限元时，除特殊点（网格轴与 X 点）或边界外，每个节点都由 $4$ 个单元共享。 
这里不考察_每个单元的自由度数量_，而考察_每个节点的自由度数量_。因此改用下图而非前图：前图仅用于引入自由度的分组，下图以一个由 4 个有限元拼合而成的节点 $\mathbf{P}\_{00}$ 为中心，更贴合实际所用的形式：

$$
\begin{matrix}
\text{-11}      &&& \text{01}      &&& \text{11}      \\ 
\bullet &&& \bullet &&& \bullet  \\ 
\text{-10}      &&& \text{00}      &&& \text{10}      \\ 
\bullet &&& \times &&& \bullet  \\ 
\text{-11} &&& \text{0-1}      &&& \text{1-1}      \\ 
\bullet &&& \bullet &&& \bullet  \\ 
\end{matrix}
$$

上图中已假定 $G_0$ 连续，因为 4 个“拼合”的有限元在边上共享相同的控制点（因而也共享相同的边）。

将位于 $P_{00}$ 右上方的有限元记为 $\xi_{11}$，左上方的记为 $\xi_{-11}$，左下方的记为 $\xi_{-1-1}$，右下方的记为 $\xi_{1-1}$。



#### 贝塞尔有限元的广义节点表述 {#generalized-nodal-representation-of-bezier-finite-element}
文献 [S. Pamela et al. J. Comput. Phys. 464, 111101 (2022)](https://www.sciencedirect.com/science/article/pii/S0021999122001632?via%3Dihub) 把上一段针对双三次单元的结果推广到任意阶 $n$，并始终施加 $m=(n-1)/2$ 的 $G_m$ 连续性。
不再使用 $p_i,u_i,v_i,w_i$ 向量，而记作 $u_{ij}$，并把 $h_{u,i}$ 换成 $h^{ij}$。例如在双三次情形下有 $u_{i0}:=p_i, u_{i1}:=u_i, ...$。 
于是，仅针对节点 $\mathbf{P}_{00}$ 所属组的广义表述如下：

$$
\mathbf{P}_{ij} = h^{ij}\vec{u}^{ij} + \sum_{k=0}^i\sum_{l=0}^j (-1)^{1+i+j+k+l}(1-\delta_{ki}\delta_{lj}) 
\begin{pmatrix}
i \\ k
\end{pmatrix}
\begin{pmatrix}
j \\ l
\end{pmatrix}
\mathbf{P}_{kl} \tag{5}
$$

其中 $0\leq i,j \leq (n+1)/2$

严格来说，该表述只针对共享 $\mathbf{P}\_{00}$ 的 4 个拼合片中第 1 个单元，即单元 $\xi_{11}$。
$\xi_{-1-1}$、$\xi_{-11}$、$\xi_{1-1}$ 的表述见[附录 A](#appendix-a-full-generic-nodal-formulation)。


#### <u>在广义节点表述上施加连续性</u>
共享节点上的 $G_m$ 连续性通过施加下述约束获得。

对 $\forall j, \ \ h^{-ij}$ 的约束为：
$$
h^{-ij} = 
\begin{cases}
-\alpha h^{ij} & \text{for } i = 1 \text{ and } \alpha > 0 \\
h^{ij} & for i \neq 1
\end{cases} \tag{6a}
$$

对 $\forall i, \ \ h^{i-j}$ 的约束为：

$$
h^{i-j} = 
\begin{cases}
-\beta h^{ij} & \text{for } j = 1 \text{ and } \beta > 0 \\
h^{ij} & for j \neq 1
\end{cases} \tag{6b}
$$

其中负下标用于表示单元 $\xi_{-11}$、$\xi_{1-1}$ 或 $\xi_{-1-1}$ 的尺寸。例如 $h^{-21}$ 属于 $\xi_{-11}$（“第一下标为负、第二下标为正”）。

推导见 [S. Pamela et al. J. Comput. Phys. 464, 111101 (2022)](https://www.sciencedirect.com/science/article/pii/S0021999122001632?via%3Dihub)。

#### <u>关于该表述的直观理解</u>
如 [S. Pamela et al. J. Comput. Phys. 464, 111101 (2022)](https://www.sciencedirect.com/science/article/pii/S0021999122001632?via%3Dihub) 的推论 1 所证明，在所采用的这一特殊节点表述中，向量 $u^{ij}$ 的方向与符号（而非绝对值）与**导数**相同

$$
\frac{\partial^{i+j} \mathbf{P}}{\partial^{i} s \partial^{j} t}(s=0,t=0)
$$

这一点非常有用，例如在构造网格时，因为正是用 $R$ 与 $Z$ 的导数来获得磁面对齐的网格。

### 采用节点表述的有限元基
如上一段所示，节点表述指把自由度（控制点）归属于节点而非单元。
此外，控制点被改写为其所属节点加上若干向量（这些向量才是新的自由度）。 
自由度表示的这一改变（由控制点变为某节点上的局部向量）意味着表述 $(3)$ 必须改动，尤其要把与控制点对应的基 $\{B_i^n(s)B_j^n(t) \}_{i,n=0\dots n}$ 换成与向量 $\vec{u}^{ij}$ 对应的基。 
做法是改写 $(5)$，使其右端不出现 $\mathbb{P}\_{xy}$，从而每个 $\mathbb{P}\_{ij}$ 只依赖 $h^{xy}$ 与 $\vec{u}^{xy}$；再把结果代入 $(3)$ 并按 $\vec{u}^{ij}$ 归并。 

单元 $K$ 上的新表述为：

$$
X_{\text{pol}}^{(K)} = \sum_{i=0}^{\text{n_vertices}} \sum_{j=0}^{\text{n_degrees}} h^{ij}\vec{u}^{ij} b_{ij}^n(s,t) \tag{7}
$$

在三次情形下得到如下基：
$$
\begin{array}{r l}
b_{1,1} &= (1 - s)^{2} (1 - t)^{2} (1 + 2 s) (1 + 2 t) \\
b_{1,2} &= 3 (1 - s)^{2} (1 - t)^{2} s (1 + 2 t) \\
b_{1,3} &= 3 (1 - s)^{2} (1 - t)^{2} (1 + 2 s) t \\
b_{1,4} &= 9 (1 - s)^{2} (1 - t)^{2} s t \\
b_{2,1} &= s^{2} (1 - t)^{2} (3 - 2 s) (1 + 2 t) \\
b_{2,2} &= 3 s^{2} (1 - t)^{2} (1 - s) (1 + 2 t) \\
b_{2,3} &= 3 s^{2} (1 - t)^{2} (3 - 2 s) t \\
b_{2,4} &= 9 s^{2} (1 - t)^{2} (1 - s) t \\
b_{3,1} &= s^{2} t^{2} (3 - 2 s) (3 - 2 t) \\
b_{3,2} &= 3 s^{2} t^{2} (1 - s) (3 - 2 t) \\
b_{3,3} &= 3 s^{2} t^{2} (3 - 2 s) (1 - t) \\
b_{3,4} &= 9 s^{2} t^{2} (1 - s) (1 - t) \\
b_{4,1} &= (1 - s)^{2} t^{2} (1 + 2 s) (3 - 2 t) \\
b_{4,2} &= 3 (1 - s)^{2} t^{2} s (3 - 2 t) \\
b_{4,3} &= 3 (1 - s)^{2} t^{2} (1 + 2 s) (1 - t) \\
b_{4,4} &= 9 (1 - s)^{2} t^{2} s (1 - t) .
\end{array}
\tag{8}
$$



### 真实自由度、尺寸以及几何坐标与物理变量的分离
当采用 $n$ 阶贝塞尔曲面且 $\mathbf{P} \in \mathbb{R}^{d}$ 时，每个顶点有一个由 $\left(\frac{n+1}{2}\right)^2$ 个向量构成的基（例如 $n=3$ 时为 4 个向量）。 
理论上 $\vec{u}^{ij}$ 的每个分量都是自由度，因此理论上的自由度总数为向量数的 $d$ 倍。

然而，与 $\vec{u}^{ij}$ 前两个分量对应的空间坐标 $R$ 与 $Z$，在**构造网格**时即被**固定**。 
因此真实的自由度数为
$$
N_{\text{dof}} = (d-2)\left(\frac{n+1}{2}\right)^2
$$

构造网格时，尺寸 $h^{ij}$ 的取值也随之确定。 

贝塞尔曲线在几何坐标与物理坐标上的用法不同，因此分成两套独立表述是合理的：

$$
X_\text{pol}^{(K)}(s,t) = \sum_{i=0}^{N_\text{vert}-1} \sum_{j=0}^{\text{dof_per_vertex}} h^{ij} \vec{u}^{ij} b_{ij}(s,t)
$$

以及

$$
\begin{pmatrix} R \\ Z
\end{pmatrix}
_\text{pol}^{(K)}(s,t) = \sum_{i=0}^{N_\text{vert}-1} \sum_{j=0}^{\text{dof_per_vertex}} h^{ij} \vec{v}^{ij} b_{ij}(s,t)
$$

注意两套表述中的 $h^{ij}$ 与 $b_{ij}$ 完全相同！几何变量与物理变量共用同一基 $\{b_{ij}\}$ 的表述称为**等参**表述。


## 附录 A：完整的通用节点表述 {#appendix-a-full-generic-nodal-formulation}
[前一段](#generalized-nodal-representation-of-bezier-finite-element)引入的通用节点表述只给出单元 $\xi_{11}$ 的控制点。要表示单元 $\xi_{-1-1}$、$\xi_{-11}$、$\xi_{1-1}$ 的控制点，表述基本相同，但须处理负下标。关键在于：尺寸（$h^{ij}$）随单元而变（依赖具体单元），而基向量 $\vec{u}^ij$ 在全部 4 个单元中相同。 

$\xi_{11}$ 的表述（与[前一段](#generalized-nodal-representation-of-bezier-finite-element)相同）：
$$
\mathbf{P}_{ij} = h^{ij}\vec{u}^{ij} + \sum_{k=0}^i\sum_{l=0}^j (-1)^{1+i+j+k+l}(1-\delta_{ki}\delta_{lj}) 
\begin{pmatrix}
i \\ k
\end{pmatrix}
\begin{pmatrix}
j \\ l
\end{pmatrix}
\mathbf{P}_{kl}
$$ 
其中 $0\leq i,j \leq (n+1)/2$

$\xi_{-11}$ 的表述：
$$
\mathbf{P}_{-ij} = h^{-ij}\vec{u}^{ij} + \sum_{k=0}^i\sum_{l=0}^j (-1)^{1+i+j+k+l}(1-\delta_{ki}\delta_{lj}) 
\begin{pmatrix}
i \\ k
\end{pmatrix}
\begin{pmatrix}
j \\ l
\end{pmatrix}
\mathbf{P}_{-kl}
$$ 
其中 $0\leq i,j \leq (n+1)/2$

$\xi_{-1-1}$ 的表述：
$$
\mathbf{P}_{-i-j} = h^{-i-j}\vec{u}^{ij} + \sum_{k=0}^i\sum_{l=0}^j (-1)^{1+i+j+k+l}(1-\delta_{ki}\delta_{lj}) 
\begin{pmatrix}
i \\ k
\end{pmatrix}
\begin{pmatrix}
j \\ l
\end{pmatrix}
\mathbf{P}_{-k-l}
$$ 
其中 $0\leq i,j \leq (n+1)/2$

$\xi_{1-1}$ 的表述：
$$
\mathbf{P}_{i-j} = h^{i-j}\vec{u}^{ij} + \sum_{k=0}^i\sum_{l=0}^j (-1)^{1+i+j+k+l}(1-\delta_{ki}\delta_{lj}) 
\begin{pmatrix}
i \\ k
\end{pmatrix}
\begin{pmatrix}
j \\ l
\end{pmatrix}
\mathbf{P}_{k-l}
$$ 
其中 $0\leq i,j \leq (n+1)/2$