---
title: "原子过程"
nav_order: 8
parent: "中性粒子与杂质"
layout: default
render_with_liquid: false
---

<!-- untranslated-notice -->
<div class="warning" markdown="1">
**本页尚未翻译**，以下为 JOREK 官方英文原文。

原文页面：[Atomic Processes](https://iterorganization.github.io/JOREK/physics/kinetic_models/neutrals_and_impurities/ncs_ics_atomic_processes.html)　·　源文件：`physics/kinetic_models/neutrals_and_impurities/ncs_ics_atomic_processes.md`
</div>

# Atomic physics
Currently the following atomic physics processes are modeled, usually using coefficients from OpenADAS ([[adas|Brief overview]]):

**Neutrals:**
  * *Line radiation*: energy sink for background plasma.
  * *Ionization*: kinetic neutral -> background fluid ion.
  * *Recombination*: background fluid ion -> kinetic neutral.
  * *Charge-exchange*: modeled here as elastic collision between a background fluid- and kinetic ion, changes particle velocity and contributes to parallel momentum coupling term.
  * [Neutral neutral collisions](../../howto/neutral_neutral_collisions.md)

**Impurities:**
  * *Radiation*: including line radiation, Bremsstrahlung and contribution from recombination.
  * *Ionization*: increases charge state by one.
  * *Recombination*: decreases charge state by one.
  * *Collisions*: currently binary collisions with the background plasma ions, resulting in neoclassical effects.