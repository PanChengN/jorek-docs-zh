---
title: "空间离散与网格"
nav_order: 3
parent: "空间离散"
layout: default
render_with_liquid: false
---

<!-- untranslated-notice -->
<div class="warning" markdown="1">
**本页尚未翻译**，以下为 JOREK 官方英文原文。

原文页面：[Spatial discretization and mesh](https://iterorganization.github.io/JOREK/numerics/spatial-discretization/spatial-discretization-and-mesh.html)　·　源文件：`numerics/spatial-discretization/spatial-discretization-and-mesh.md`
</div>

# How does the poloidal mesh uses Bezier finite elements
When building the mesh, formulation $(2)$ in [Introduction to spatial Discretization in JOREK](introduction.md) is used.  
Each element is required to have a certain shape. For example:

<img src="../assets/grids/grid_polar.png">

This means that $\vec{v}^{ivl}$ and $h^{ij}$ must be imposed accordingly such that formulation $(2)$ in [Introduction to spatial Discretization in JOREK](introduction.md) expresses the desired shape. 

How $\vec{v}^{ivl}$ and $h^{ij}$ are set depends from the type of mesh. 

## Poloidal mesh in tokamaks
Being axisymmetric, tokamaks have the same poloidal mesh for each $\phi_p$ ($p=1\dots \texttt{n_planes}$).
This means that `n_coord_tor=1`. 

## Mesh in stellarators
In stellarators it might be desired to set `n_coord_tor>1` to use Fourier harmonics to model the non axisimmetry of the grid.
