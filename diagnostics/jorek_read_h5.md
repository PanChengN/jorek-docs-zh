---
title: "util/jorek_read_h5.py"
nav_order: 36
render_with_liquid: false
parent: "General"
---

## util/jorek_read_h5.py
`jorek_read_h5.py` 是一个 Python 脚本，它把 jorek 的输出数据做成 **.vtk** 对象。该对象随后由 `test_jorek_read_h5.py` 调用，由后者把数据写入 **.vtk** 或 .**vtu** 文件。要正确运行这个 Python 脚本，必须先理解 *test* 文件中的基本参数与 writer 属性。

### util/test_jorek_read.h5.py

首先，我们要选择变量以及存放所需数据的 jorek 文件。  
```
f.read('/tmp/jorek_restart.h5', variables=[2, 5])
```
选择变量时，我们在所需变量列表中给出它们的编号，其中 *0 = psi, 1 = u, 2 = j, 3 = w, 4 = rho, 5 = T, 6 = v_par*。

其次，我们要决定网格的几何形态。关于网格单元的更详细说明放在接下来两节中，这里只解释输入参数。  
```
grid = f.to_vtk(n_sub=3, phi=[0,180], n_plane=3, quadratic=False, bezier=False)
```
**n_sub**（subdivisions，细分数）指定 jorek 单元在 RZ 平面内的每条边上要包含多少个点（最小 = 2）。jorek 单元的数目由 jorek 文件固定，这里我们只是“提高分辨率”。  
**phi** 是网格极角的区间，单位为度（最小 = 0，最大 = 360）。若区间的起点与终点相同，则网格为二维。  
**n_plane** 告诉我们在环向坐标上网格使用多少个 RZ 平面，三维单元就是在这些平面之间构造的。若平面数等于“1”，则网格为二维。  
**quadratic** 与 **bezier** 是两个布尔参数，用于描述单元的性质（在几何部分说明）。

最后，我们选择输出文件的格式：`.vtu` 用 `writer=vtk.vtkXMLUnstructuredGridWriter()`，`.vtk` 用 `writer=vtk.vtkUnstructuredGridWriter()`；如需把编码改为 "ascii"，用 `writer.SetDataModeToAscii()`；再用 `writer.SetFileName('jorek_2d.vtu')` 指定文件名。

### 基本几何
当 `bezier=False` 时使用基本几何。这里的网格单元在二维中只用 4 个点、在三维中只用 8 个点，各点以直线相连，因此它们的 vtk 类型是 [quad](https/*vtk.org/doc/nightly/html/classvtkquad.html.md) 与 [hexahedron](https/*vtk.org/doc/nightly/html/classvtkhexahedron.html.md)。  
若 `quadratic=True`，单元会稍复杂一些。二维时为 [quadratic quad](https/*vtk.org/doc/nightly/html/classvtkquadraticquad.html.md)，它在四个角上有 4 个节点、每条边中点还有 4 个节点。三维中沿用同样的边中点思路，得到 [quadratic hexahedron](https/*vtk.org/doc/nightly/html/classvtkquadratichexahedron.html.md)，共 20 个节点。边中点的计算方式与更高细分时相同，采用 Bezier 插值，详见 [Daan Van Vugt 的论文](https://research.tue.nl/en/publications/nonlinear-coupled-mhd-kinetic-particle-simulations-of-heavy-impur)。

### Bezier 几何
Bezier 几何最为复杂，但它能在可视化平台（如 **paraview**）中，用同样多的点提高非线性细分层级，因为它用 Bezier 多项式从初始控制点插值出更多点。  
这里所用的 RZ 平面内控制点计算方式在*论文*中有说明。二维时，这些控制点用于构造 [bezier quadrilateral](https/*vtk.org/doc/nightly/html/classvtkbezierquadrilateral.html.md)。结果是每个单元由 4x4 个节点构成。二维与三维单元所用的节点排布见[此 pdf](https/*staging.coreform.com/papers/implementation-of-rational-bezier-cells-into-vtk-report.pdf.md)。

转到三维时，[bezier hexahedron](https/*vtk.org/doc/nightly/html/classvtkbezierhexahedron.html.md) 由 3 个平面、每面 4x4 个点构成，即每个单元 48 个节点。由于我们的单元不是 *pdf* 中的 4x4x4，我们只是跳过不存在的节点。单元形状的各向异性结构由 `SetHigherOrderDegrees()` 指定，形如 `[3,3,2]`，写在 *jorek_read_h5.py// 中。（尽管单元由 4x4x3 个点构成，每个维度上给出的数目要少 1。）下面给出了示例单元的图、其顶视图与侧视图以及它的点，并作为 ![ VTK file for ParaView](vtk_bezier_hexahedron.zip?linkonly) 提供。

![](points_and_surface.png?800)
![](side_view.png?430)
![](top_view.png?430)

RZ 平面内的控制点仍用先前的办法计算，而环向方向则改用另一种方法。由于圆弧只能用有理二次 Bezier 曲线表示，这些控制点必须带有有理权重。如前所述，单元由 3 个平面构成，其中中间平面必须带有有理权重。若第一个与第三个平面之间的夹角为 *2α*（第二个平面位于 α 处），则权重按 `w=cos(α)` 计算，第二个平面内各点的新半径（极角不变）按 `R=r/cos(α)` 计算。在顶视图中可以看到带权重的控制点位置。有理二次 Bezier 曲线的说明见[此指南](https://ctan.math.illinois.edu/macros/latex/contrib/lapdf/rcircle.pdf)。

对于 Bezier 单元必须使用 *.vtu* 文件格式，因为 *.vtk* writer 在写入权重与高阶次数时仍有问题。Bezier 单元需要 VTK 9 版本，该版本也包含在 SMITER 1.6.3 中，并配有打过补丁的 *ParaView* *5.8.0* 或 *ParaView* 5.9.1。
