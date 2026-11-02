---
title: "中性粒子与杂质"
nav_order: 7
parent: "动理学粒子模块"
layout: default
render_with_liquid: false
---

# 动理学中性粒子与杂质
JOREK 的动理学中性粒子和/或杂质扩展可用于以比基础 MHD 模型或流体中性粒子与杂质模型更高的保真度模拟等离子体刮削层（SOL）。

* [耦合方案](../neutrals_and_impurities/ncs_ics_coupling_scheme.md)
* [已实现的原子过程](../neutrals_and_impurities/ncs_ics_atomic_processes.md)
  * [中性粒子间碰撞](../neutrals_and_impurities/neutral_neutral_collisions.md)
  * [杂质碰撞](../neutrals_and_impurities/impurity_collisions.md)
* [等离子体–壁相互作用](../neutrals_and_impurities/particle_wall_interactions.md)
* [气体注入](../neutrals_and_impurities/gas_puffing.md)
* [教程](../neutrals_and_impurities/tutorial.md)

更多细节请查看 kinetic_main.f90 与 mod_particle_evolution.f90，或联系 [Máté](mate.szuecs@ipp.mpg.de) 或 [Daniel](D.Maris@differ.nl|Daniel)。

## 发表文献与参考资料
* Liang, Y. C., et al. "JOREK simulations of the X-point radiator formation and its movement in ASDEX Upgrade." arXiv preprint arXiv:2602.08614 (2026).
* Szücs, M. (2024). Modeling detachment and burn-through in small edge localized mode regimes using the nonlinear magnetohydrodynamic code JOREK. Master Thesis, Technische Universität München, München.
* Maris, D. "Time-dependent Scrape-Off Layer simulations with JOREK for detachment control." (2024). MSc Thesis, Eindhoven University of Technology.
* Korving, S. Q. (2024). MHD Simulations of Neutral and Impurity Transport in ELM-controlled Plasmas: with application to ITER. [Phd Thesis 1 (Research TU/e / Graduation TU/e), Applied Physics and Science Education]. Eindhoven University of Technology.
* Korving, S. Q., et al. "Simulation of neoclassical heavy impurity transport in ASDEX Upgrade with applied 3D magnetic fields using the nonlinear MHD code JOREK." Physics of Plasmas 31.5 (2024).
* Korving, S. Q., et al. "Development of the neutral model in the nonlinear MHD code JOREK: Application to E× B drifts in ITER PFPO-1 plasmas." Physics of Plasmas 30.4 (2023).
* Van Vugt, D. C., et al. "Kinetic modeling of ELM-induced tungsten transport in a tokamak plasma." Physics of Plasmas 26.4 (2019).
* van Vugt, D. C. (2019). Nonlinear coupled MHD-kinetic particle simulations of heavy impurities in tokamak plasmas. [Phd Thesis 1 (Research TU/e / Graduation TU/e), Applied Physics and Science Education]. Technische Universiteit Eindhoven.
