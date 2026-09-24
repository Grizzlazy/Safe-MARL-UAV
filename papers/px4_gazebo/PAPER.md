# Paper

**Status: SELECTED for the PX4/Gazebo track — approved 2026-09-23. Public code: NONE (confirmed). No longer blocked.**

Verified 2026-09-22; **unblocked and completed 2026-09-23 from the published PDF**
(`papers/2025_Xiang_Decentralized Consensus Inference-Based Hierarchical Reinforcement Learning for.pdf`, 15 pp.).

The previously blocking gaps — the MAPPO baseline numbers and the reward
functional forms — are now resolved and transcribed below. Implementation on this
track is unblocked.

> **Read this first.** PX4/Gazebo is **not the training environment**. Policies
> are trained in MPE (a lightweight 2-D particle simulator) and PX4/Gazebo SITL is
> used only to **validate** the trained policy under realistic quadrotor dynamics.
> Every PX4/Gazebo multi-UAV MARL paper found in this search follows that pattern
> (see `papers/CANDIDATES.md`). Any plan assuming "train MARL inside Gazebo" should
> be rejected on evidence, not attempted.

Fields are **[VERIFIED]** (read from the published PDF) or **[NOT VERIFIED]**.

## Citation

Yuming Xiang, Sizhao Li, Rongpeng Li, Zhifeng Zhao, Honggang Zhang.
"Decentralized Consensus Inference-Based Hierarchical Reinforcement Learning for
Multiconstrained UAV Pursuit-Evasion Game."
*IEEE Transactions on Neural Networks and Learning Systems*, 36(10):18229–18243,
October 2025.

[VERIFIED] — Crossref, confirmed against the PDF. Received 23 May 2024; accepted
21 June 2025; published 18 July 2025.

Affiliations: Zhejiang University; Zhejiang Lab; Macau University of Science and
Technology. [VERIFIED]

## DOI / URL

- DOI: https://doi.org/10.1109/TNNLS.2025.3582909 — [VERIFIED]
- Preprint: https://arxiv.org/abs/2506.18126 — [VERIFIED]
- Local copy: `papers/2025_Xiang_Decentralized Consensus Inference-Based Hierarchical Reinforcement Learning for.pdf` — [VERIFIED]

## Public Code

**None found.** [VERIFIED by absence]

Negative searches (2026-09-22): GitHub repository search for `ConsMAC …` and
`CI-HRL …` → 0 results; web search for an authors'/Zhejiang Lab release → nothing;
**no code-availability statement anywhere in the published PDF**.

**Consequence: reimplementation, not a code run.**

### Important correction about XTDrone [VERIFIED]

An earlier draft of this file speculated the SITL setup was built on XTDrone.
**It is not.** The paper states:

> "Different from existing open-source SITL work such as XT-Drone [50], in our
> simulation the UAV node makes fully distributed and asynchronous decisions based
> on partial observations within a limited communication range…"

XTDrone is cited as *contrast*, not as a dependency. Their SITL harness is custom
and unreleased.

`robin-shaun/XTDrone` (1,723★, MIT) remains a reasonable public starting point for
**our own** multi-UAV PX4+ROS+Gazebo harness, as does PX4's own
`launch/multi_uav_mavros_sitl.launch`. Neither reproduces their architecture.

## Environment

Two environments, serving different purposes. [VERIFIED]

1. **MPE** (Multi-Agent Particle Environment) — where all training and the full
   quantitative comparison happen. 2-D, **fixed altitude**; UAV coordinates
   randomly initialized in [−2, 2] m on x and y.
2. **SITL** — ROS + **Gazebo-Classic** + **PX4** autopilot, for validating the
   trained policy.

### SITL architecture [VERIFIED — Fig. 8 and §V-D2a]

```
Distributed Algorithm :  CI-HRL Actor per agent  (independent Python process,
                         offboard mode, CI-HRL + ConsMAC-A)
        ↕  action / observation
Onboard UAV Process   :  one ROS node per agent; agents broadcast state and
                         observations over ROS topics via MAVROS (UDP)
        ↕  action / sensor data / position
Autopilot Firmware    :  one PX4 instance per agent; computes motor and actuator
                         values with its PID controller
        ↕  motor commands / sensor data (TCP)
Simulator             :  Gazebo — motion dynamics, sensors, position per UAV
```

Each UAV computes an expected **acceleration** from the CI-HRL output and
publishes it to the topic PX4 subscribes to. PX4 obtains real-time pose and sensor
messages from Gazebo over TCP, converts the acceleration request into motor and
actuator values via PID, and Gazebo integrates the next frame.

Protocol layers: MAVLINK, MAVROS, ROS. [VERIFIED]

## Simulator Version

- PX4 version — **[NOT VERIFIED]**, not stated.
- Gazebo — **Gazebo Classic**; exact version **[NOT VERIFIED]**.
- ROS version (ROS 1 vs ROS 2) — **[NOT VERIFIED]**.
- Ubuntu version — **[NOT VERIFIED]**.

### Reproducibility risk in the toolchain [VERIFIED]

PX4 documentation: *"Gazebo Classic is nearing feature-parity with Gazebo Classic
on PX4, and will soon replace it. Until then you can continue to use
Gazebo-Classic on Ubuntu 22.04 for the few cases where you still need to."*
Gazebo Classic is supported on **Ubuntu 22.04 only**; Gazebo Harmonic is the
successor. Latest PX4 release: v1.17.0 (2026-05-13).

Plan on a pinned Ubuntu 22.04 + Gazebo Classic + older-PX4 stack in Docker.

## Task

**Cooperative Evasion and Formation Coverage (CEFC)**, posed as a multi-constrained
pursuit-evasion game. A communication-limited UAV swarm must simultaneously
[VERIFIED]:

- reduce the **urgency** of target areas by reaching and covering them;
- maintain one of a set of **predefined formation patterns** `Δ_c`, splitting into
  groups as needed;
- **avoid obstacles and collisions**;
- **evade** a PPO-driven adversary that chases the nearest group of ≥ 3 members.

Safety-relevant: yes — obstacle and collision avoidance are explicit constraints
with a dedicated reward term and a reported collision-probability metric.

## Number of UAVs

- Main experiments: **N = 8**. [VERIFIED]
- Formation patterns: `C = {3,4,5,6,7,8}`; performance comparison focuses on
  patterns > 5. [VERIFIED]
- Large-scale generalization: **N = 8, 9, 10, 12, 15**. [VERIFIED]
- SITL: **8** UAVs. [VERIFIED]

## Observation Space

Per-agent local state `z_i(t)` [VERIFIED]:

- neighbor observations within observation distance **δ_obs = 3 m**;
- target-area and adversary information;
- **LiDAR detection results** (M rays), giving `d_im(t)`;
- messages received from neighbors (64-dim message `m`).

Exact vector dimensions and the value of M — **[NOT VERIFIED]**.

## Action Space

Two levels [VERIFIED]:

- **Low level:** continuous 2-D acceleration `[u_x, u_y]`; UAV velocity range
  **[−1, 1] m/s**; adversary velocity range **[−0.75, 0.75] m/s**.
- **High level:** discrete, **9-D** — anchor points on the x/y axes drawn from
  **{−8, 0, 8} m**, regenerated every **10** low-level steps.

## Reward

[VERIFIED — Appendix A, Equations (15)–(22), and Table VIII]

**Formation (15):** `R_f(t) = − Σ_{k=1..χ(t)} HD(Δ_nk, P_k(t)) − ω_l · R_f(t−1)`,
with `R_f(0)=0`, `ω_l` the formation lag coefficient, and `HD` the Hausdorff
distance `HD(E1,E2) = max_{x∈E1} min_{y∈E2} ‖x−y‖`.

**Navigation (16):** `R_n(t) = − Σ_{i∈N} Σ_{ℑ∈T} κ_ℑ(t) · ‖p_{i→ℑ}(t)‖`
— urgency-weighted Euclidean distance between agents and targets.

**Task accomplishment (17)–(19):**
`R_t(t) = Σ_{ℑ∈T} κ_ℑ(t) Σ_{k*} TR_{k*→ℑ}(t)` where
`TR_{k*→ℑ}(t) = n_{k*}` if `‖p̄_{k*→ℑ}(t)‖ < δ_task`, else `0`, and `k*` indexes
groups meeting formation tolerance `HD(Δ_nk*, P_k*) < δ_for`.
Urgency decays: `κ_ℑ(t+1) = max(κ_ℑ(t) − ω_d Σ_{k*} TR_{k*→ℑ}(t), 0)`, `κ_ℑ(0)=1`.

**Evasion (20):** `R_e(t) = − Σ_{i∈N} max(δ_{a,e} − ‖p_{i→A}(t)‖, 0)`.

**Collision avoidance (21)–(22):** `R_c(t) = − Σ_{i∈N} Σ_{j≠i, j∈I} CR_{i→j}(t)`
where `I` is the set of agents and obstacles and

```
CR_{i→j}(t) = ω_cr1 · (δ_s   − d_im(t)) + C1 ,   d_im(t) < δ_s
            = ω_cr2 · (δ_a,c − d_im(t)) + C2 ,   δ_s < d_im(t) < δ_a,c
            = 0                              ,   d_im(t) > δ_a
```

with `d_im(t) = min(d_i1(t), …, d_iM(t))` from LiDAR.

### Reward parameters [VERIFIED — Table VIII]

| Parameter | Value |
|---|---|
| Formation lag coefficient ω_l | 0.3 |
| Decay factor ω_d | 0.003 |
| Alert distances (δ_a,e, δ_a,c) | (2 m, 0.5 m) |
| Formation tolerance δ_for | 1 m |
| Target area radius δ_task | 3 m |
| Minimum safety distance δ_s | 0.2 m |
| Collision constants (ω_cr1, ω_cr2, C1, C2) | (24, 8, 3, 1) |

### Reward weights [VERIFIED — Table I]

| Level | Weights |
|---|---|
| Low `R_L` | (ω_f, ω_n, ω_c) = (15, 4, 100) |
| High `R_H` | (ω_t, ω_n, ω_e) = (10, 0.1, 100) |

## Algorithm

**CI-HRL**, two levels [VERIFIED]:

- **High level:** MAPPO + **ConsMAC** (Consensus-oriented Multi-Agent
  Communication) — selects anchor points from an inferred global consensus.
  ConsMAC-A (anchor-point labels) and ConsMAC-O (global-observation labels) are
  the two supervision variants.
- **Low level:** **AT-M** (Alternative Training-based MAPPO) + policy distillation
  — formation, navigation and obstacle avoidance.

CTDE with **parameter sharing** across agents (θ_i = θ ∀i). [VERIFIED]

The important point for us: **plain MAPPO is a reported baseline**, so there is a
named, standard CTDE MARL algorithm to reproduce.

## Baselines

- **Low level (Table II):** MADDPG, ORCA-F, CL-M, AT-M-Step 1/2/3, AT-M-Safe.
  **MAPPO is not in this table.** [VERIFIED]
- **Communication (Fig. 5, curves only):** MAPPO, HASAC, TarMAC, MASIA, NVIF,
  ConsMAC-A, ConsMAC-O. **Learning curves, no numeric table.** [VERIFIED]
- **Full system (Table IV):** MAPPO+AT-M, HASAC+AT-M, TarMAC+AT-M, MASIA+AT-M,
  NVIF+AT-M, and CI-HRL variants. [VERIFIED]

> **Critical for scoping:** the MAPPO baseline in Table IV is **"MAPPO + AT-M"** —
> MAPPO as the *high-level* policy on top of the paper's AT-M *low-level* policy.
> There is **no standalone-MAPPO number** anywhere in the paper. Reproducing that
> row therefore requires AT-M as well, which is a substantial part of their
> contribution. See Reproduction Target for how we handle this.

## Training Configuration

[VERIFIED]

| Setting | Value |
|---|---|
| Low-level training | 500 episodes × 100 time steps |
| High-level pretraining | 1,000 episodes × 400 time steps |
| High-level fine-tuning | 500 episodes × 400 time steps |
| Anchor-point regeneration | every 10 steps |
| Low-level anchor init | random in [−5, 5] m (x and y) |
| AT-M alternative training steps | 3 |
| Parallel threads | 20 |
| PPO epochs | 15 |
| Optimizer | Adam, lr 1e-4 |
| PPO (γ, ε, λ) | **(0.8, 0.2, 0.95)** |
| Low-level network | 3-layer MLP, hidden 128 |
| Global estimator | 3-layer MLP |
| Distance encoder | single linear layer |
| Other MLP modules | 2 layers |
| Attention | 4 heads, dim 64 |
| Message `m` dimension | 64 |
| ConsMAC training | every 20 episodes, 5,000 updates, batch 2,048 |
| Policy distillation | hidden 256, Adam 1e-4, 300,000 episodes, batch 600, replay 60,000 steps |
| Obstacle density (train) | 0 and 3e-2 /m²; denser test 5e-2 /m² |
| Target areas | \|T\| = 2, drawn from {(−8,−8), (−8,8), (8,−8), (8,8)} m |
| Adversary | single-agent PPO, same network as low-level policy |

γ = 0.8 is confirmed from Table I — **not** a typo.

**[NOT VERIFIED]:** entropy coefficient, value-loss coefficient, minibatch size,
gradient clipping, **number of random seeds**, adversary PPO hyperparameters.

## Evaluation Metrics

[VERIFIED]

**Low level:** `R_L` (avg reward per step), **F** formation stability (seconds per
episode with HD-based formation error < 1 m), **N** navigation efficiency (seconds
in proximity, ‖p̄−p_a‖ < 1 m), **C** average collision probability (%).

**High level / full system:** `R_H` (avg reward per step), `R_t` task reward,
`R_n` navigation reward, `R_e` evasion reward, **E** average time of dangerous
situations per round (agent-adversary distance < 2 m).

All evaluations average over **50 episodes**. [VERIFIED]

## Main Experiments

[VERIFIED]

1. Low-level comparison in MPE, patterns c = 6, 7, 8 (Table II).
2. Communication-module comparison incl. MAPPO (Fig. 5, curves) and overhead
   (Table III).
3. ConsMAC-A ablation (Fig. 6).
4. Full-system comparison, **including MAPPO+AT-M** (Table IV).
5. Adversary-strategy robustness: PPO, DDPG, R-Largest, R-Nearest (Table V).
6. Large-scale generalization N = 8–15 (Table VI).
7. **SITL validation** with wind, sensing deviation, distributed hardware
   (Table VII).

## Reported Results

[VERIFIED — transcribed from the published PDF, 50 episodes each]

### Table IV — full-system comparison (N = 8). **This is the reproduction target.**

| Method | R_H ↑ | R_t ↑ | R_n ↑ | R_e ↑ | E ↓ |
|---|---|---|---|---|---|
| **MAPPO + AT-M** | **−397.29** | **54.33** | **−334.95** | **−116.68** | **8.78** |
| HASAC + AT-M | −381.07 | 105.70 | −347.82 | −138.95 | 11.42 |
| TarMAC + AT-M | −432.81 | 29.81 | −367.06 | −95.56 | 7.16 |
| MASIA + AT-M | −404.45 | 31.89 | −336.17 | −100.19 | 7.72 |
| NVIF + AT-M | −403.79 | 16.12 | −340.58 | −79.33 | 5.94 |
| CI-HRL-w-CL-M-wo-FT | −408.55 | 38.81 | −326.08 | −121.29 | 9.48 |
| CI-HRL-w-CL-M | −320.69 | 74.13 | **−288.11** | −106.70 | 8.40 |
| CI-HRL-DT | −366.95 | 79.72 | −381.52 | −65.16 | 5.16 |
| CI-HRL-wo-FT | −351.27 | 58.31 | −301.65 | −107.93 | 7.66 |
| **CI-HRL (theirs)** | **−281.56** | **107.37** | −327.27 | **−61.66** | **4.46** |

### Table II — low-level comparison (excerpt, c = 8)

| Method | R_L ↑ | F (s) ↑ | N (s) ↑ | C (%) ↓ |
|---|---|---|---|---|
| MADDPG | – | 0.02 | 49.30 | – |
| ORCA-F | −195.23 | 7.74 | 28.52 | 0.66 |
| CL-M | −121.90 | 29.30 | 34.08 | 1.30 |
| AT-M-Step 1 | −506.48 | 45.84 | 53.92 | 13.20 |
| AT-M-Step 2 | −266.94 | 0.10 | 1.68 | 2.56 |
| **AT-M-Step 3** | −106.94 | 41.52 | 36.90 | 1.14 |
| AT-M-Safe | **−72.57** | 20.26 | 26.60 | **0.62** |

(c = 6 and c = 7 blocks are in the PDF, p. 18237, if needed.)

### Table III — communication overhead

| Method | Content | Dim |
|---|---|---|
| MAPPO | – | 0 |
| HASAC | – | 0 |
| TarMAC | latent vector | 64 |
| MASIA | local observation | 38 |
| NVIF | latent vector + local observation | 102 |
| ConsMAC | latent vector | 64 |

### Table V — adversary strategies (CI-HRL)

| | PPO | DDPG | R-Largest | R-Nearest |
|---|---|---|---|---|
| R_t | 107.37 | 161.97 | 151.74 | 187.87 |
| R_e | −61.66 | −82.43 | −55.48 | −79.54 |
| E | 4.46 | 6.42 | 4.44 | 5.80 |

### Table VI — large-scale generalization (per-agent averages)

| N | R_H/N | R_t/N | R_n/N | R_e/N | E/N |
|---|---|---|---|---|---|
| 8 | −35.20 | 13.42 | −40.91 | −7.71 | 0.56 |
| 9 | −36.80 | 15.67 | −43.13 | −9.34 | 0.68 |
| 10 | −41.16 | 10.11 | −43.61 | −7.66 | 0.60 |
| 12 | −42.26 | 8.91 | −44.97 | −6.20 | 0.49 |
| 15 | −45.31 | 4.09 | −41.46 | −7.95 | 0.63 |

### Table VII — SITL validation of AT-M (1000-step game)

| Critical event | c=5 F(s) | c=5 N(s) | c=5 C(%) | c=6 F(s) | c=6 N(s) | c=6 C(%) |
|---|---|---|---|---|---|---|
| SITL-S | 693 | 722.4 | 0 | 711 | 645 | 0 |
| Wind 3 m/s | 669.3 | 651.3 | 0 | 637 | 644 | 0 |
| Wind 5 m/s | 643.2 | 579.2 | 0 | 586 | 632.5 | 0 |
| Wind 8 m/s | 558 | 549 | 0 | 530 | 628 | 0 |
| Deviation 0.3 m | 683 | 652 | 0 | 667 | 639 | 0 |
| Deviation 0.5 m | 647.5 | 628.7 | 0 | 616 | 623 | 0.33 |
| Deviation 0.8 m | 545.5 | 605.5 | 2.95 | 534 | 551 | 1.20 |
| SITL-M | 652.8 | 711.1 | 0 | 676.1 | 647.9 | 0 |

| Critical event | c=7 F(s) | c=7 N(s) | c=7 C(%) | c=8 F(s) | c=8 N(s) | c=8 C(%) |
|---|---|---|---|---|---|---|
| SITL-S | 746 | 707 | 0 | 712 | 696.5 | 0 |
| Wind 3 m/s | 582 | 636 | 0 | 612.6 | 631.3 | 0 |
| Wind 5 m/s | 577 | 585 | 0 | 593.7 | 615.7 | 0 |
| Wind 8 m/s | 521 | 508 | 0 | 524 | 580 | 0 |
| Deviation 0.3 m | 676.3 | 703.2 | 0 | 616.3 | 649 | 0 |
| Deviation 0.5 m | 606 | 690.5 | 0.60 | 600.3 | 643 | 0.28 |
| Deviation 0.8 m | 590 | 593 | 2.20 | 503 | 551 | 2.18 |
| SITL-M | 691.4 | 700.8 | 0 | 654 | 705.7 | 0 |

Wind speeds follow a Gaussian with the stated mean; sensing deviation is Gaussian
with the stated mean. Obstacle radius is 0.4 m, which is why deviation ≥ 0.5 m
starts producing collisions. [VERIFIED]

SITL-S = single device; SITL-M = multi-device LAN deployment (Jetson TX2 NX runs
one agent at **12.3 ms/decision**; an RTX 4090 machine runs the other seven at
**0.96 ms/decision**). Asynchronous AT-M under SITL-M reaches **97.1%** of
single-device completion; CI-HRL effective formation rate over 50 SITL episodes is
**92.7%** of SITL-S. [VERIFIED]

**Not reported [NOT VERIFIED]:** number of random seeds, error bars on any table.
All values are unlabelled point estimates over 50 episodes.

## Reproduction Target

In increasing order of ambition. **Stop at the first tier that fails.**

- **T0 — infrastructure.** Multi-UAV PX4 SITL + Gazebo Classic (8 vehicles) in
  Docker on Ubuntu 22.04, via `multi_uav_mavros_sitl.launch` or XTDrone as a
  starting point. Confirm we can command 8 vehicles in offboard mode with
  acceleration setpoints and read their states over MAVROS. Toolchain only.
- **T1 — primary target.** Reconstruct the **CEFC task in MPE** (N = 8) and train
  a **standard MAPPO** agent on it, reporting `R_H, R_t, R_n, R_e, E` over 50
  episodes.
  **Scoping caveat:** the paper's MAPPO row is MAPPO+AT-M, so our
  standalone-MAPPO number is **not** directly comparable to −397.29. Two honest
  options, to be decided after T0: (a) report our MAPPO as a *new* baseline on our
  reconstruction and compare only qualitatively; or (b) additionally implement
  AT-M-Step 3 to match their low-level policy and make the comparison direct.
  Option (b) is materially more work — decide explicitly, do not drift into it.
- **T2 — stretch.** Transfer the trained policy into PX4/Gazebo SITL with 8 UAVs
  and report F, N, C as in Table VII. This is the part that actually exercises
  PX4/Gazebo.
- **T3 — out of scope for Phase 1.** Full CI-HRL (ConsMAC + AT-M + policy
  distillation). Do not commit to this.

## Hardware Requirements

**[NOT VERIFIED]** for training — the paper does not state its training hardware
or wall-clock time.

Reported for SITL deployment [VERIFIED]: NVIDIA Jetson TX2 NX (one agent,
12.3 ms/decision) and an RTX 4090 machine (seven agents, 0.96 ms/decision).

Our estimate, stated as an estimate: MPE training with 20 parallel threads is
CPU-bound and workstation-feasible. Running 8 PX4 SITL instances plus Gazebo
Classic is the heavy part — expect a many-core requirement and roughly real-time
(non-accelerated) execution.

## Known Limitations

1. **No public code** for CI-HRL, ConsMAC, AT-M, or the CEFC environment.
2. **The CEFC MPE environment is not released** and must be reconstructed from
   prose. Largest source of deviation.
3. **No standalone-MAPPO baseline exists** — the MAPPO row includes AT-M
   (see Baselines). This complicates the comparison; handle explicitly.
4. **No SITL software versions** (PX4, Gazebo Classic, ROS, Ubuntu all unstated).
5. **Gazebo Classic is deprecated**, Ubuntu 22.04 only.
6. **No seeds and no error bars** on any table.
7. Their SITL harness is **custom and unreleased** — explicitly not XTDrone.
8. PX4/Gazebo is validation, not training, limiting what a "PX4/Gazebo
   reproduction" can claim.
9. Several environment details remain unspecified: map extent, obstacle radius in
   MPE (0.4 m is stated for SITL), LiDAR ray count M, exact observation vector
   layout.

## Deviations We Expect

Declared in advance, before any run:

- **Our reconstruction of CEFC will differ** in what the paper does not specify
  (map extent, obstacle placement, LiDAR ray count M, observation vector layout).
  Each choice is logged here with its value. Absolute reward values are therefore
  **not comparable**; what we can defend is the relative ordering of algorithms
  within our own reconstruction.
- **Our own MAPPO implementation** (or a standard public one, cited and pinned).
- **The MAPPO comparison is not like-for-like** unless AT-M is also implemented —
  stated prominently wherever results are reported.
- **SITL stack pinned by us** (Ubuntu 22.04 + Gazebo Classic + a stated PX4
  version, in Docker) and recorded, since the paper gives none.
- **Seeds 0,1,2,3,4** (project default), since the paper reports no seed protocol.
  Reported as mean ± std and **explicitly labelled** against their unlabelled
  50-episode point estimates.
- If SITL proves too slow, the number of SITL evaluation episodes is reduced and
  **the reduced count is stated**, not quietly shrunk.
