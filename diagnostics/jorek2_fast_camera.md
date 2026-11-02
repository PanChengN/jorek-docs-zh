---
title: "jorek2_fast_camera"
nav_order: 25
render_with_liquid: false
parent: "General"
---

## jorek2_fast_camera

### 并行化
该诊断按视线数目（即像素数）并行。  
因此运行时需要使用大量 MPI 进程（而不是线程）。

### ADAS 数据
运行该诊断需要一个文件：my_pec.dat，它必须位于运行目录中。  
该文件包含 Dalpha 谱线的 ADAS 发射率，其值由电子密度与温度决定。  
这是本代码可以做出的主要改进之一：使用精确的 ADAS 数据，目前针对 Dalpha，但未来也可能用于杂质辐射。  
除此之外，只需要 jorek_restart.h5 文件。

### 相机视角与几何
该诊断目前按 MAST 快相机的视角设置。  
可以在文件本身（`jorek/diagnostics/jorek2_fast_camera.f90`）中修改，涉及以下参数：  
`pixel_dim` ：像素尺寸  
`n_pixels_hor` ：水平像素数  
`n_pixels_ver` ：垂直像素数  
`X_cam` ：相机位置  
`Y_cam` ：相机位置  
`Z_cam` ：相机位置  
`focus` ：镜头焦距  
`toroidal_angle_location` ：环向角位置（比直接用 X,Y,Z 更方便，这样 Z 可以始终取零）  
`angle_hor` ：相机朝向（水平）  
`angle_ver` ：相机朝向（垂直）  
`light_saturation` ：改变相机最大饱和度的因子（否则会采用最亮像素的光强）  
`colormap` ：通常只用黑白，但也可以用热力图或彩虹色……  
''''  
  

所有输入参数既可在编译前于代码 `jorek2_fast_camera.f90` 中设置，也可在运行时于输入文件 `fast_cam.nml` 中设置，后者必须放在运行目录中。  
JET 与 MAST 的这些文件示例可在 `jorek/util/fast_camera/` 中找到



### 中性粒子
Dalpha 发射用到中性粒子密度。若使用 model500，则程序为此使用真实的 rho_n 变量；但例如使用 model303 时，中性粒子密度是在代码内（或在 `fast_cam.nml` 输入文件内）手工设定的：  
`  rhon_prof(1) = 1.d-3  ! Core value [10^20 m^(-3)]`  
`  rhon_prof(2) = 1.d-1  ! SOL value [10^20 m^(-3)]`  
`  rhon_prof(3) = 3.d-1  ! Lower-divertor value [10^20 m^(-3)]`  
`  rhon_prof(4) = 3.d-1  ! Upper-divertor value [10^20 m^(-3)]`  
`  rhon_prof(5) = 0.10   ! Edge-psi tanh width [psi_norm]`  
`  rhon_prof(6) = 0.95   ! Edge-psi tanh position [psi_norm]`  
`  rhon_prof(7) = 0.20   ! Lower-divertor tanh width [m]`  
`  rhon_prof(8) = -0.05  ! Lower-divertor tanh position relative to Z_xpoint(1) [m]`  
`  rhon_prof(9) = 0.20   ! Upper-divertor tanh width [m]`  
`  rhon_prof(10)= +0.05  ! Upper-divertor tanh position relative to Z_xpoint(2) [m]`  


### 视线积分
沿视线的积分采用用户指定的步长（单位为米），例如  
`step   = 1.d-3`  
但也可以使用变化的积分步长，其取值取决于我们是进入等离子体芯部（MAST 上发射较低），还是位于等离子体边界处（目前取 `psi_n=0.6`）。  
这完全是人为设定的，用户可以通过修改变量来启用  
`go_faster_in_core = .true.`  


### 输出格式
目前输出仅写为 .ppm 图像，这是一种非常简单的格式。  
可能更希望同时支持 .vtk 输出格式，或者 h5……  


### 反射
目前只对环向对称的壁包含反射。  
做法是在 JOREK 输入文件中指定限制器轮廓：  
`n_limiter`  
`R_limiter(:)`  
`Z_limiter(:)`  
并在代码中（或 `fast_cam.nml` 输入文件中）设置反射标志与反射系数：  
`include_reflections`  
`reflective_coefficient`  
只计入第一次反射。  
要把代码扩展到能包含 CAD 结构上的反射还需要更多工作，但目前代码中的视线结构已经准备好，可以相对容易地实现这一点。


### 示例
下面是 MAST 上快相机的示例，以及 JET 上包含反射的广角视图  
![](fast_camera_mast2.png?400)  
![](fast_camera_jet2.png?400)
