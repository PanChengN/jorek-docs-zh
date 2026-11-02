---
title: "粒子推进器"
nav_order: 7
parent: "动理学粒子模块"
layout: default
render_with_liquid: false
---

# 可用的粒子推进器：

- Boris（见 G.L. Delzanno, E. Camporeale / JCP 253 (2013) 259-277）：
    - `boris_all_initial_half_step_backwards_RZPhi(particle, mass, fields, time, timestep)`
    - `boris_push_cylindrical(particle, mass, E, B, timestep)`
- Runge Kutta（C. Sommariva et al., Nucl. Fusion 58 (2018) 016043）
    - `runge_kutta_fixed_dt_relativistic_particle_push_jorek(fields,time,timestep,mass,particle)`
    - `runge_kutta_fixed_dt_gc_push_jorek_radreact(fields,t,dt,mass,particle)`
- 保体积格式（volume preserving scheme）（见 R. Zhang et al., Phys. Plasmas 22 (2015) 044501, C. Sommariva et al., Nucl. Fusion 58 (2018) 016043）
    - `volume_preserving_push_jorek(particle,fields,mass,time,timestep,ifail)`
    - `volume_preserving_radiation_push_jorek(particle,fields,mass,time,timestep,ifail)`

关于可用于逃逸电子、并在推进中计入库仑碰撞效应的推进器的更多信息，请参见[粒子追踪器中的逃逸电子物理](runaway_electrons/runaway_electron_pushers.md)。 
