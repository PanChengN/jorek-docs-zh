---
title: "粒子类型"
nav_order: 7
parent: "动理学粒子模块"
layout: default
render_with_liquid: false
---

# 粒子类型（见 `particles/mod_particle_types.f90`）

下表列出了不同的粒子类型及其变量。所有粒子都具有对应于 particle base 的变量，并根据其类型附加额外变量。 

| 类型      | 变量      | 单位          | 说明 |
| --------- | -------------- | -------------- | ------- |
| particle base   | x(3)    | [m,m,rad]       | 粒子在 (R,Z, phi) 空间中的位置 |
|                 | st(2)   | [real*8]        | 局部有限元坐标 |
|                 | weight  | [real*4]        | 粒子权重，\"真实\"粒子总数 = sum(weights)|
|                 | i_elm   | [integer]       | 包含该粒子的单元编号|
|                 | i_life  | [integer]       | 度量该粒子被重复使用的频次"|
|                 | t_birth | [s]             | 度量粒子的诞生时间|
| _kinetic        | v(3)    | [m/s]           | 速度，SI 单位，方向为 (R,Z,phi)|
|                 | q       | [e]       | 电荷 |
| _kinetic_leapfrog| v(3)    | [m/s]     | 在 **t = t(n-1/2)** 时刻的速度，方向为 (R,Z,phi)|
|                 | q       | [e]       | 电荷|
| _kinetic_relativistic| p(3) |[AMU m/s]| 动量 **[X,Y,Z]**|
|                 | q       | [e] | 电荷|
|                 | q       | [e]       | 电荷|
| _gc             | E       | [eV]      | 动能|
|                 | mu      | [eV]      | 磁矩（其符号决定平行速度的方向）|
|                 | q       | [e]       | 电荷 |
| _gc_relativistic| p(2) |[AMU m/s, AMU m<sup>2</sup>/(T*s<sup>2</sup>)]| 1：平行动量，2：磁矩|
|                 | q | [e]| 电荷 |

**粒子类型转换：**

（见 `particles/pushers/mod_boris.f90` 与 `particles/pushers/mod_kinetic_relativistic.f90`）

  * `kinetic_leapfrog_to_gc(node_list, element_list, particle_in, E, B, mass, dt)`
  * `gc_to_kinetic_leapfrog(particle_in, node_list, element_list, chi, E, B, mass, dt)`
  * `kinetic_to_kinetic_leapfrog(particle_in, E, B, mass, dt)`
  * `kinetic_leapfrog_to_kinetic(particle_in, E, B, mass, dt)`
  * `kinetic_to_gc(node_list, element_list, particle_in, B, mass)` 
  * `gc_to_kinetic(node_list, element_list, particle_in, chi, B, mass)`
  * `relativistic_kinetic_to_particle(node_list,element_list,particle_in, particle_out,mass,B)`
  * `relativistic_kinetic_to_relativistic_gc(node_list,element_list, particle_in,mass,B)`
  * `relativistic_kinetic_to_gc(node_list,element_list,particle_in,mass,B)` 
  * `gc_to_relativistic_kinetic(node_list,element_list,particle_in,time,mass,chi,B)`
  
