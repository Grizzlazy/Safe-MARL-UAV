# Paper

**Status: SELECTED for the AirSim track — approved 2026-09-23. Public code: NONE (confirmed).**

Phase 1 commits to this paper knowing no official code exists, so reproduction
means reimplementation. The single-UAV alternative with official code
(He et al. 2021) was considered and **rejected as the target** — it would be a
safe reproduction of the wrong thing. It is retained as infrastructure only.

Verified 2026-09-22; **fully updated 2026-09-23 from the published PDF**
(`papers/drones-09-00010-v2.pdf`, 20 pp.).

Fields are marked **[VERIFIED]** (read from the published PDF) or
**[NOT VERIFIED]**. Nothing is guessed.

> **Correction on first reading of the published version.** The published paper
> differs substantially from the arXiv preprint: different metrics (5, not 4),
> seven baselines instead of one, different result values, and different
> hardware. **All preprint-derived figures previously in this file have been
> replaced.** Cite and reproduce the published version, not arXiv:2407.04064.

## Citation

Zhun Fan, Zihao Xia, Che Lin, Gaofei Han, Wenji Li, Dongliang Wang, Yindong Chen,
Zhifeng Hao, Ruichu Cai, Jiafan Zhuang.
"UAV Collision Avoidance in Unknown Scenarios with Causal Representation
Disentanglement." *Drones*, 9(1):10, 2025. MDPI.

[VERIFIED] — Crossref record for `10.3390/drones9010010`, confirmed against the
PDF (running head "Drones 2025, 9, 10").

Related preprint, **materially different content**, use only as background:
arXiv:2407.04064, "Collision Avoidance for Multiple UAVs in Unknown Scenarios
with Causal Representation Disentanglement."

Sibling paper by the same group (secondary option):
Che Lin et al., "Improving Generalization in Collision Avoidance for Multiple
Unmanned Aerial Vehicles via Causal Representation Learning," *Sensors*
25(11):3303, 2025, https://doi.org/10.3390/s25113303. [VERIFIED]

### Base paper — REQUIRED READING for T1 [VERIFIED]

Huaxing Huang, Guijie Zhu, Zhun Fan, Hao Zhai, Yuwei Cai, Ze Shi, Zhaohui Dong,
Zhifeng Hao. "Vision-based Distributed Multi-UAV Collision Avoidance via Deep
Reinforcement Learning for Navigation." **IROS 2022**.
DOI `10.1109/IROS47612.2022.9981803`; preprint https://arxiv.org/abs/2203.02650
(local copy fetched to scratchpad; **download into `papers/` before relying on it**).

This is reference [12] of the *Drones* paper — the origin of the **SAC + RAE**
baseline, by the same group. **It specifies the network architecture that the
Drones paper omits**, so the T1 target is far better specified than
"no code" first suggested. Its details are folded into the sections below and
attributed `[VERIFIED — IROS22]`.

## DOI / URL

- DOI: https://doi.org/10.3390/drones9010010 — [VERIFIED]
- Local copy: `papers/drones-09-00010-v2.pdf` — [VERIFIED]

## Public Code

**None.** [VERIFIED — Data Availability Statement now read]

> "Data Availability Statement: The data presented in this study are available
> upon request from the corresponding author."

No repository, no supplementary code. There is a supplementary **video** only.

Also negative: GitHub repository search (three query variants) returned 0 results.

**Consequence: reproduction = full reimplementation** of both the method and the
multi-UAV AirSim environment.

**Worth doing:** the corresponding author explicitly invites data requests. An
email could yield code or the Unreal scenes and would materially cut the effort.

### Public infrastructure that lowers the cost [VERIFIED]

`heleidsn/UAV_Navigation_DRL_AirSim` — https://github.com/heleidsn/UAV_Navigation_DRL_AirSim
(570★; last push 2025-07-19; **no license file — check before reuse**).
Official code for He, Aouf, Song, *Aerospace Science and Technology* 118:107052,
2021 (https://doi.org/10.1016/j.ast.2021.107052).

A working, version-pinned AirSim → Gym → Stable-Baselines3 pipeline with
depth-image observations and SAC/PPO/TD3 (AirSim v1.6.0, Python 3.8, PyTorch
1.10.1, gym 0.21.0, SB3 v1.4.0). **Single-UAV**; extending to N drones is our work.

## Environment

Unreal Engine + the AirSim plugin. Problem formalized as a **Dec-POMDP**.
[VERIFIED]

**Training scene** — `playground`, **no obstacles**. Each training cycle assigns
start and target positions randomly inside a **14 m × 14 m × 5 m** volume.
[VERIFIED]

**Test scenes** — `forest` (main, unseen obstacles), plus `snowy mountain` and
`valley` as extra unseen scenes; `playground` is also reported as the "seen"
case. [VERIFIED]

**Test initialization** — all drones placed uniformly on a circle of **16 m
radius** at a fixed altitude, each targeting the opposite side of the circle.
This is the deliberately hard, high-conflict configuration. [VERIFIED]

Low-level control is AirSim's built-in PID; the policy emits velocity commands
only. [VERIFIED]

| PID controller | K_P | K_I | K_D |
|---|---|---|---|
| Linear velocity | 0.2 | 2.0 | 0.0 |
| Angular velocity | 0.25 | 0.0 | 0.0 |

| UAV specification | Value |
|---|---|
| Mass | 0.8 kg |
| Rotor count | 4 |
| Motor output range | 0 – 1 |
| Minimum angling throttle | 0.05 |
| Maximum angular rate | 2.5 rad/s |
| Body box (m) | 0.2413 × 0.1143 × 0.0762 |

## Simulator Version

- AirSim version — **[NOT VERIFIED]**, not stated anywhere in the paper.
- Unreal Engine version — **[NOT VERIFIED]**, not stated.
- OS: Ubuntu 20.04. [VERIFIED]

### Reproducibility risk in the toolchain [VERIFIED]

- `microsoft/AirSim` is not archived (last push 2026-09-15) but its **last tagged
  release is v1.8.1, 2022-07-18** — effectively frozen at a UE 4.27-era stack.
- The UE5 community fork `CodexLabsLLC/Colosseum` is **archived**.

Pin every version explicitly; expect setup friction.

## Task

Decentralized collision-avoidance navigation for a UAV swarm in unknown cluttered
outdoor scenes. Each UAV flies to its own goal while avoiding static obstacles and
the other UAVs, using a forward-facing depth camera and an IMU — a partially
observable setting. [VERIFIED]

Safety-relevant: yes, collision avoidance is the core objective. [VERIFIED]

## Number of UAVs

- Default / training: **8**. [VERIFIED]
- UAV scalability sweep (test time): **8, 10, 12, 14**. [VERIFIED]
- Obstacle-count sweep (test time): **4, 6, 8, 10** (4 is the default). [VERIFIED]

## Observation Space

Three components per drone [VERIFIED]:

1. `o_t` — encoded **depth image** (forward-facing camera);
2. `o_g` — **target position** in the UAV's own body coordinate frame;
3. `o_v` — the UAV's **flight speed**.

Depth image resolution — **[NOT VERIFIED]**.

The encoder output is split into three latent blocks [VERIFIED]:

| Latent | Meaning | Dim |
|---|---|---|
| `Z1` | task-irrelevant (e.g. background) — **discarded** | n1 = 8 |
| `Z2` | task-relevant, scenario-specific (e.g. obstacle distribution) | n2 = 6 |
| `Z3` | task-relevant, scenario-invariant (e.g. distance to obstacle) | n3 = 42 |

Only `Z2` and `Z3` reach the policy. [VERIFIED]

## Action Space

Continuous 3-D: `a = [v_x_cmd, v_z_cmd, v_ω_cmd]` — forward velocity, vertical
ascent rate, and yaw/turn rate. [VERIFIED]

Action bounds and control frequency — **[NOT VERIFIED]**.

## Reward

`r = r_g + r_c` [VERIFIED — Equations (2)–(4)]

```
r_g = r_arrival                       if d_t < 0.5
    = α_goal * (d_t − d_{t−1})        otherwise

r_c = r_collision                     if crashed
    = α_avoid * max(d_safe − d_min, 0) otherwise
```

Training values [VERIFIED]: `r_arrival = 50`, `r_collision = −10`,
`α_goal = 3`, `α_avoid = −0.05`, `d_safe = 5`.

`d_t` is the UAV-to-target distance at time `t`; `d_min` is the distance to the
nearest obstacle.

> Note the sign convention: `α_goal = +3` multiplies `(d_t − d_{t−1})`, which is
> **negative when closing on the target**. Read literally this penalizes progress.
> Treat as a likely sign-convention slip in the paper and **verify empirically**
> during reimplementation; log whichever convention we use as a deviation.

## Algorithm

**Soft Actor-Critic (SAC)** plus the paper's **Causal Representation
Disentanglement (CRD)** module on the visual encoder. Built on SAC + RAE.
[VERIFIED]

Training regime: **centralized training with multiple UAVs, distributed execution
at test time**. [VERIFIED]

**Classification caveat — flag to the advisor. [VERIFIED]**
This is a **single shared policy** run independently by each UAV. It is
*independent learning*, **not** a CTDE method with a centralized joint-action
critic, and therefore **not** MAPPO / MADDPG / QMIX. If the project requires a
named CTDE MARL algorithm, this paper does not supply one.

## Baselines

Seven rows, all trained under identical environments and parameters, following
each method's official implementation [VERIFIED]:

1. **SAC + RAE** — the base method
2. `+ AutoAugment` — augmentation
3. `+ DrAC` — augmentation
4. `+ L1 Norm` — regularization
5. `+ L2 Norm` — regularization
6. `+ CRL` — prior causal representation learning
7. `+ CRD` — **the paper's method**

Disentanglement comparison (Table 8): β-VAE, Factor-VAE, DAVA. [VERIFIED]

## Training Configuration

[VERIFIED — Table 3 of the published paper, complete]

| Parameter | Value |
|---|---|
| Batch size | 128 |
| Max episodes | 300 |
| Update times | 400 |
| Replay buffer capacity | 20,000 |
| Discount γ | 0.99 |
| Encoder learning rate | 1e-4 |
| Critic learning rate | 1e-4 |
| Critic target update frequency | 2 |
| Critic Q-function soft-update rate τ_Q | 0.01 |
| Critic encoder soft-update rate τ_enc | 0.05 |
| Actor learning rate | 1e-4 |
| Actor update frequency | 2 |
| Actor log-stddev bounds | [−10, 2] |
| Optimizer | Adam |
| n1 / n2 / n3 | 8 / 6 / 42 |

### Network architecture [VERIFIED — IROS22, not stated in the Drones paper]

The Drones paper omits the architecture; the base paper specifies it in full:

| Component | Specification |
|---|---|
| Encoder input | **three consecutive depth images** (temporal stack) |
| Encoder | 4 conv layers + 1 FC → **50-dim latent**, with layer normalization |
| Conv layer 1 | 32 2-D filters, kernel 3, **stride 2**, ReLU |
| Conv layers 2–4 | 32 2-D filters, kernel 3, **stride 1**, ReLU |
| Decoder | 1 FC + 4 deconv layers, mirroring the encoder |
| Actor | 3-layer MLP, **1024** hidden units → 3-D mean + covariance (Gaussian) |
| Critic (Q) | 3-layer MLP, **1024** units |
| Gradient rule | **actor gradients do not update the conv encoder** |
| RAE regularization | λ_z = 1e-6, λ_φ = 1e-7 |

> Dimension mismatch to resolve: the base encoder emits a **50-dim** latent, but
> the Drones paper splits the latent into n1+n2+n3 = 8+6+42 = **56**. The CRD
> variant evidently widens it. For the **SAC+RAE baseline (T1)** use 50.

Base-paper training hyperparameters [VERIFIED — IROS22], where they **differ**
from the Drones table: max episodes **200** (vs 300), and critic / actor /
autoencoder learning rates **1e-3** (vs 1e-4). Replay 20,000, batch 128, γ 0.99,
τ_Q 0.01, τ_enc 0.05, update frequencies 2, Adam, log-stddev bounds [−10, 2] —
these match.

Base-paper environment [VERIFIED — IROS22]: ROS **noetic** + AirSim, PyTorch;
circle scenario **radius 12 m** (the Drones paper uses 16 m); 8 UAVs default with
an 8/10/12/14 sweep; initial and goal positions randomized in **3-D**;
trained on Intel i9-11900K + NVIDIA Quadro RTX 4000.

**Still [NOT VERIFIED] in both papers:** **depth image resolution**, camera FOV,
SAC entropy target/temperature, episode length in steps, replay warm-up,
**number of random seeds**, number of evaluation episodes per cell, AirSim
clock-speed factor.

## Evaluation Metrics

[VERIFIED — five metrics]

1. **SSR** — Swarm Success Rate: fraction of trials where **every** UAV reaches
   its target. The strict, mission-level metric.
2. **ISR** — Individual Success Rate: fraction of UAVs reaching their target
   without collision within the time limit.
3. **SPL** — Success weighted by Path Length: `SPL = σ · l / max(l, p)`, with `l`
   the shortest start-to-target distance, `p` the distance actually flown, and
   `σ` a binary success indicator.
4. **Extra Distance** (m) — mean extra distance over the shortest path;
   reported as mean/std.
5. **Average Speed** (m/s) — mean velocity over testing; reported as mean/std.

## Main Experiments

[VERIFIED]

1. **Generalization** — train in obstacle-free `playground`, test zero-shot in
   `forest` with circle initialization (Table 4, 7 methods).
2. **Ablation on latent components** — which of Z1/Z2/Z3 feed the policy (Table 5).
3. **Scalability** — vary obstacle count (4–10) and UAV count (8–14) (Table 6).
4. **More scenes** — playground / forest / snowy mountain / valley (Table 7).
5. **Disentanglement comparison** — vs β-VAE, Factor-VAE, DAVA (Table 8).

## Reported Results

[VERIFIED — transcribed from the published PDF]

### Table 4 — main comparison (forest, unseen background + obstacles, circle init)

| Method | SSR (%) | ISR (%) | SPL (%) | Extra Distance (m) | Avg Speed (m/s) |
|---|---|---|---|---|---|
| SAC + RAE | 29.6 | 87.7 | 82.2 | 10.591/4.443 | 0.457/0.090 |
| + AutoAugment | 53.4 | 90.6 | 82.7 | 3.192/0.840 | 0.854/0.154 |
| + DrAC | 50.0 | 88.7 | 77.4 | 4.712/1.547 | 1.026/0.190 |
| + L1 Norm | 69.6 | 92.9 | 84.2 | 2.459/0.855 | 0.870/0.107 |
| + L2 Norm | 58.4 | 93.1 | 79.8 | 4.410/1.522 | 0.912/0.113 |
| + CRL | 71.1 | 94.5 | 85.1 | 3.924/0.883 | 0.844/0.097 |
| **+ CRD (theirs)** | **93.6** | **98.9** | **87.3** | 3.728/0.677 | 0.812/0.086 |

### Table 5 — latent component ablation

| Z1 | Z2 | Z3 | SSR (%) | ISR (%) |
|---|---|---|---|---|
| | ✓ | ✓ | 93.6 | 98.9 |
| | ✓ | | 8.9 | 71.6 |
| | | ✓ | 6.4 | 67.3 |
| ✓ | ✓ | ✓ | 11.7 | 78.4 |

### Table 6 — scalability

| Sweep | Count | SAC+RAE SSR | SAC+RAE ISR | +CRD SSR | +CRD ISR |
|---|---|---|---|---|---|
| Obstacles | 4 | 29.6 | 87.7 | 93.6 | 98.9 |
| | 6 | 22.4 | 82.6 | 89.6 | 97.6 |
| | 8 | 18.4 | 80.6 | 87.0 | 96.8 |
| | 10 | 16.6 | 78.9 | 80.0 | 95.7 |
| UAVs | 8 | 29.6 | 87.7 | 93.6 | 98.9 |
| | 10 | 20.0 | 84.0 | 91.8 | 93.6 |
| | 12 | 11.8 | 82.4 | 89.6 | 91.0 |
| | 14 | 2.5 | 80.6 | 85.4 | 88.2 |

### Table 7 — across scenes

| Scene | Seen? | Method | SSR (%) | ISR (%) | SPL (%) | Extra Dist (m) | Avg Speed (m/s) |
|---|---|---|---|---|---|---|---|
| Playground | Seen | Baseline | 87.5 | 96.4 | 81.4 | 6.156/3.449 | 0.527/0.099 |
| | | + CRD | 100.0 | 100.0 | 87.8 | 4.458/0.302 | 0.852/0.038 |
| Forest | Unseen | Baseline | 29.6 | 87.7 | 82.2 | 10.591/4.443 | 0.457/0.090 |
| | | + CRD | 93.6 | 98.9 | 86.1 | 3.254/0.564 | 0.812/0.086 |
| Snowy mountain | Unseen | Baseline | 65.1 | 92.8 | 72.3 | 9.236/2.927 | 0.504/0.068 |
| | | + CRD | 99.2 | 99.8 | 88.5 | 3.629/0.309 | 0.967/0.061 |
| Valley | Unseen | Baseline | 52.3 | 91.2 | 68.2 | 11.361/5.329 | 0.460/0.092 |
| | | + CRD | 96.8 | 99.8 | 88.6 | 3.568/0.359 | 0.931/0.056 |

> Forest SPL for CRD is 87.3 in Table 4 and 86.1 in Table 7. Minor internal
> inconsistency in the paper; noted, not resolved.

**Not reported [NOT VERIFIED]:** number of seeds, number of evaluation trials per
cell, and whether values are means over runs. **These are single unlabelled
numbers**, so our multi-seed mean ± std must be labelled as such when compared.

## Reproduction Target

In increasing order of ambition. **Stop at the first tier that fails.**

- **T0 — infrastructure (must pass first).** AirSim + multi-drone `settings.json`;
  confirm we can spawn, command and read depth images from 8 drones at an
  accelerated clock. `heleidsn/UAV_Navigation_DRL_AirSim` is a *reference* for the
  AirSim→Gym→SB3 wiring and version pinning. Reproducing that repo's single-UAV
  result is **not** a Phase-1 milestone (decided 2026-09-23).
- **T1 — primary target.** Reimplement the **SAC + RAE baseline**, 8 UAVs, train
  in an obstacle-free playground (14×14×5 m), test in a forest scene with circle
  init (r = 16 m). Report SSR / ISR / SPL / Extra Distance / Average Speed against
  the paper's SAC+RAE row (29.6 / 87.7 / 82.2 / 10.591 / 0.457).
- **T2 — stretch.** Add the CRD module and test whether the SSR gain
  (29.6 → 93.6) reproduces.

T1 is the honest Phase-1 deliverable. T2 should not be promised up front.

## Hardware Requirements

Reported [VERIFIED]: Ubuntu 20.04, **Intel i9-13900K**, **NVIDIA RTX 4090**.

> The arXiv preprint reports i7-12700 + RTX 3060 instead. The published figures
> above supersede it.

**[NOT VERIFIED]:** wall-clock training time, GPU memory, disk for Unreal scenes.

Practical: AirSim + Unreal needs a GPU and a desktop OS; it will not run headless
without extra work. Our available hardware should be compared against an RTX 4090
before promising a timeline.

## Known Limitations

1. **No public code**, and no public Unreal scenes. Dominant risk.
2. **No AirSim/UE version stated**, and the AirSim toolchain is frozen at v1.8.1.
3. Unreal scenes are **not identified by asset name or source**, so ours will
   differ and absolute numbers will not match.
4. **Not a CTDE MARL algorithm** (see Algorithm).
5. **No seed protocol, no trial counts, no error bars** anywhere in the results.
6. A likely **sign-convention slip** in `r_g` (see Reward).
7. Minor internal inconsistency between Tables 4 and 7 (forest SPL).
8. Wall-clock: 8 drones with image observations in AirSim is slow.

## Deviations We Expect

Declared in advance, before any run:

- **Scenes will differ.** We cannot obtain their Unreal environments. We will
  document ours (asset source, obstacle density, map size) and treat absolute
  SSR/ISR as **not directly comparable**; the defensible comparison is the
  *relative* ordering of methods measured within our own scene.
- **Our own implementation**, not the authors'. Every unreported choice (encoder
  CNN, entropy target, episode length, depth resolution) is picked by us and
  **logged here with its value**.
- **Reward sign convention** for `r_g` resolved empirically and recorded.
- **AirSim / Unreal versions ours**, pinned in config and stated.
- **Seeds 0,1,2,3,4** (project default), since the paper reports no seed protocol.
  Reported as mean ± std and **explicitly labelled** when set beside the paper's
  unlabelled single values.
- Training episodes may be cut if wall-clock proves prohibitive; any cut is
  recorded here with the achieved step count.
