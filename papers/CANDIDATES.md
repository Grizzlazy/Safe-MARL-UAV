# Paper search log — Phase 1 candidate selection

Search date: 2026-09-22 / 2026-09-23. Performed by the implementation agent.

Purpose: record *how* the two Phase-1 papers were selected, what was rejected and
why, so the choice can be audited and redone. Nothing here is a result; this is a
literature-search record.

## Headline finding

**The intersection of {AirSim or PX4/Gazebo} × {multi-UAV MARL} × {public code with
a complete reported protocol} appears to be empty.**

This is the single most important input to the Phase-1 plan, and it contradicts
the natural assumption that "AirSim and PX4/Gazebo are standard MARL benchmarks."
They are not. They are simulators. The multi-UAV MARL literature overwhelmingly
trains in lightweight custom 2-D simulators (MPE-like, grid, or bespoke Python),
and uses AirSim or PX4/Gazebo either

- for **single-agent** DRL navigation (this is where the public code lives), or
- as a **validation / sim-to-sim transfer** step for a policy trained elsewhere.

Confidence: **moderate-to-high** for the negative result. It rests on ~15
independent searches across five indexes (below), not on one query. It is still a
negative result from keyword search and cannot be proven exhaustive. A paper
behind a paywall, in a non-English venue, or using a non-obvious phrasing could
have been missed.

## Where the search looked

| Index | Method | Outcome |
|---|---|---|
| arXiv API | `abs:"AirSim" AND abs:"multi-agent"`; `abs:"PX4" AND abs:"reinforcement learning"` | 7 + 7 hits, none a multi-UAV MARL paper on these simulators. arXiv metadata rarely names the simulator, so this index is weak here. |
| Semantic Scholar API | several UAV-MARL queries | mostly communications/networking MARL, not simulator-grounded control |
| GitHub search API | `airsim multi-agent reinforcement learning`, `airsim MARL drone swarm`, `px4 gazebo multi agent reinforcement learning`, `gazebo multi-uav reinforcement learning MAPPO`, plus `topic:airsim topic:reinforcement-learning` and `topic:px4 topic:reinforcement-learning` | decisive. The AirSim RL topic (27 repos) is **almost entirely single-agent**. The PX4 RL topic has 3 repos, none a paper-backed multi-UAV MARL implementation. |
| Papers With Code API | attempted | **defunct** — API no longer returns JSON |
| Web search | ~10 targeted queries across MDPI / IEEE / Springer / theses | produced the two selected candidates |

## Selected

### AirSim track → `papers/airsim/PAPER.md`

Fan et al., "UAV Collision Avoidance in Unknown Scenarios with Causal
Representation Disentanglement," *Drones* 9(1):10, 2024.
DOI 10.3390/drones9010010 (preprint arXiv:2407.04064).

Why: genuinely AirSim, genuinely multi-UAV (8 training, 6–12 testing), the task is
safety-relevant (collision avoidance), and the training hyperparameters and
results tables are reported in usable detail.

Against: **no public code**; simulator versions unstated; the Unreal scenes are
unidentified; and the algorithm is shared-policy SAC (independent learning), not a
named CTDE MARL method.

### PX4/Gazebo track → `papers/px4_gazebo/PAPER.md`

Xiang et al., "Decentralized Consensus Inference-Based Hierarchical Reinforcement
Learning for Multiconstrained UAV Pursuit-Evasion Game," *IEEE TNNLS*
36(10):18229–18243, 2025. DOI 10.1109/TNNLS.2025.3582909 (preprint
arXiv:2506.18126).

Why: real PX4 + Gazebo Classic + ROS SITL with 8 UAVs; **standard MAPPO is an
explicit baseline**, giving a named CTDE algorithm to reproduce; hyperparameters
largely reported; safety constraints (collision, obstacle) are explicit.

Against: **no public code**; the CEFC task environment is not released; PX4/Gazebo
is used for validation only, not training; reward functional forms and SITL
software versions are unreported; the numeric results table has not yet been
transcribed.

## Rejected, with reasons

| Candidate | Why rejected |
|---|---|
| `Lauqz/Drone-Swarm-RL-airsim-sb3` (97★) — AirSim + PettingZoo + SB3 multi-drone | Closest public *multi-drone AirSim RL* code found, but **no published paper** ("an official publication is currently in preparation"). Fails the "reproduce a published paper" requirement. Worth keeping as an engineering reference. |
| He et al. 2021, *Aerospace Sci. Tech.* 118:107052 + `heleidsn/UAV_Navigation_DRL_AirSim` (570★) | Best code-to-paper match on AirSim anywhere in this search — pinned versions, configs, commands. But **single UAV**, no multi-agent element. Retained as **infrastructure** for the AirSim track, not as the reproduction target. |
| PEDRA / D-PEDRA (`aqeelanwar/PEDRA`, 331★) | AirSim, public code, published papers, and D-PEDRA does support multiple drones. But the algorithms are single-drone DQN/PER-DDQN, not MARL; stack is Python 3.6 + UE 4.18.3 (2018-era). Stale. |
| Air Learning (`harvard-edge/airlearning`, 257★) | AirSim benchmark platform with public code and a *Machine Learning* journal paper, but single-UAV and last pushed 2021. |
| XTDrone (Xiao et al., ICRAS 2020; `robin-shaun/XTDrone`, 1.7k★, MIT) | A **platform paper**, not a MARL paper — there is no MARL experiment to reproduce. Retained as **infrastructure** for the PX4/Gazebo track; it is cited by the selected TNNLS paper. |
| RALLY (arXiv:2507.01378) | Uses Gazebo-ROS-PX4 SITL and is multi-UAV, but is **LLM-driven**, not a clean MARL baseline; MAPPO is not a baseline; no public code. |
| Zeng et al., "Decentralized Aerial Manipulation of a Cable-Suspended Load using MARL," CoRL 2025 (arXiv:2508.01522) | Genuine multi-UAV MARL with real hardware, but the task is cable-suspended load manipulation — wrong task family — and the simulator is not PX4/Gazebo. |
| `PX4-Gazebo-Simulation/drl_uav` | PX4 + Gazebo DRL, but single-agent. |
| Li et al., "An Extensible MARL Framework for Multi-UAV Collaborative Path Planning," SIMULTECH 2025 | IQL/VDN/QMIX on a **custom simulator** — neither AirSim nor PX4/Gazebo. |
| MPE-only multi-UAV MARL papers (ETS-MAPPO, AM-MAPPO, MPRS-MAPPO, CL-MAPPO, and similar) | Numerous and often well-specified, but none uses AirSim or PX4/Gazebo, so none satisfies the advisor's platform requirement. |
| `goatnav/project-argus` (AirSim + MAPPO + YOLO SAR) | 1 star, no paper, no protocol. Hobby project. |

## Platform health checks (2026-09-22) — all [VERIFIED]

| Item | Status |
|---|---|
| `microsoft/AirSim` | Not archived (last push 2026-09-15), but **last release v1.8.1, 2022-07-18** — effectively frozen at a UE 4.27-era stack |
| `CodexLabsLLC/Colosseum` (UE5 fork) | **Archived** |
| `PX4/PX4-Autopilot` | Active; latest release **v1.17.0** (2026-05-13) |
| Gazebo Classic on PX4 | **Deprecated.** PX4 docs: supported on **Ubuntu 22.04 only**, Gazebo Harmonic is the successor |
| `robin-shaun/XTDrone` | Active-ish (last push 2025-08-03), MIT licensed |

These matter: both selected papers depend on toolchains that are frozen or
deprecated. Pin versions and use Docker.

## Decisions taken (2026-09-23)

1. **AirSim track targets Fan et al. 2024** — the multi-UAV paper, accepting that
   no official code exists. The single-UAV alternative with public code
   (He et al. 2021) was considered and **rejected as the target**: it would be a
   safe reproduction of the wrong thing. It stays as infrastructure.
   Reproducing it is no longer a Phase-1 milestone.
2. **Blocked PDFs are obtained manually.** The user downloads the IEEE TNNLS and
   MDPI *Drones* PDFs through institutional access; the agent transcribes the
   tables into the two PAPER.md files. **No code is written on the PX4/Gazebo
   track until that transcription is done** — building against a misread task
   specification is the most expensive mistake available here.
3. Author contact was **not** chosen as a blocking step. It remains a free option
   worth doing in parallel (open action 4).

## Open actions — status as of 2026-09-23

1. ~~Download the *Drones* PDF, confirm identity with arXiv:2407.04064, read the
   Data Availability Statement.~~ **DONE.** Both PDFs are in `papers/`.
   - Data Availability: *"The data presented in this study are available upon
     request from the corresponding author."* **No code, no repository.**
   - **The published paper differs materially from the preprint** — 5 metrics not
     4, 7 baselines not 1, different result values, different hardware
     (i9-13900K + RTX 4090, not i7-12700 + RTX 3060). `papers/airsim/PAPER.md`
     has been rewritten from the published version; preprint figures are void.
2. ~~Transcribe the TNNLS MAPPO baseline row and SITL results.~~ **DONE.**
   Tables I–VIII are transcribed into `papers/px4_gazebo/PAPER.md`.
   - Extraction note: the tables are **embedded as images**; both pypdf and
     PyMuPDF text extraction return only captions. They were recovered by
     rendering pages 8–14 at 200 dpi and reading them visually. Anyone re-checking
     this should do the same rather than trusting a text dump.
   - **Key scoping discovery:** there is **no standalone-MAPPO number** in the
     paper. Table IV's MAPPO row is **"MAPPO + AT-M"** — MAPPO as high-level policy
     on top of the authors' AT-M low-level policy. A like-for-like comparison
     requires implementing AT-M too. Recorded in the PAPER.md reproduction plan.
3. ~~Read TNNLS Sections III–IV for the reward functional forms.~~ **DONE.**
   They are in **Appendix A**, Equations (15)–(22), with parameters in Table VIII.
   All five reward terms are now fully specified in `papers/px4_gazebo/PAPER.md`.
4. ~~Correct the XTDrone assumption.~~ **DONE.** The TNNLS SITL harness is
   **not** built on XTDrone — the paper cites XTDrone explicitly as a contrast
   ("Different from existing open-source SITL work such as XT-Drone…"). Their
   harness is custom and unreleased. XTDrone remains useful as a starting point
   for *our own* harness, nothing more.
5. **Still open:** email both author groups about code/scene release. The *Drones*
   corresponding author explicitly invites data requests, so this is low-cost and
   could substantially cut the AirSim effort.
6. **NEW, found 2026-09-23 — the AirSim base paper.** Reference [12] of the
   *Drones* paper is Huang et al., "Vision-based Distributed Multi-UAV Collision
   Avoidance via Deep RL for Navigation," **IROS 2022** (arXiv:2203.02650), by the
   same group. It is the origin of the SAC+RAE baseline and **specifies the whole
   network architecture that the Drones paper omits** — 4-conv encoder → 50-dim
   latent, 3×1024 actor/critic MLPs, RAE λ values, and the rule that actor
   gradients must not update the encoder. Folded into `papers/airsim/PAPER.md`.
   **This materially lowers the AirSim T1 risk:** despite "no public code", the
   SAC+RAE baseline is now specified nearly end-to-end across the two papers.
   Remaining unknowns there are depth-image resolution, camera FOV, episode
   length and the SAC entropy target.

## Safe-MARL search (2026-09-23)

Prompted by the project title — *Safe* MARL for multi-UAV — a dedicated search of
the safe-MARL literature was run: GitHub (`safe multi-agent reinforcement
learning` → 44 repos, plus `safe MARL UAV`, `MACPO`, `constrained MARL`), arXiv
API, and web.

### The selected PX4/Gazebo paper already is a Safe MARL paper

This was under-weighted in the first pass. CI-HRL (TNNLS 2025) carries a full
safety apparatus, all [VERIFIED] from the PDF:

| Safety element | Evidence |
|---|---|
| Explicit safety distances | δ_s = 0.2 m (min safety), δ_a,c = 0.5 m (collision alert) |
| Dedicated collision reward | Eq. (21)–(22), weight ω_c = 100 — the largest low-level weight |
| Safety as a reported metric | **C, average collision probability (%)**, in every table |
| A conservative safety *variant* | **AT-M-Safe** — trades performance for safety: at c = 8, C drops 1.14 % → 0.62 % while F falls 41.52 → 20.26 s |
| A classical safe-control baseline | **ORCA-F** (Optimal Reciprocal Collision Avoidance + leader-follower) |
| Safety under perturbation | Table VII — collision rate vs wind and sensing deviation |

The **AT-M-Step 3 vs AT-M-Safe vs ORCA-F** comparison is precisely a
performance-versus-safety trade-off study. That maps 1:1 onto the ablation
AGENT.md asks for (no-safety vs reward-penalty vs explicit mechanism), and leaves
a clean slot for a Phase-2 runtime shield as a fourth point on the same curve.

**Conclusion: no paper change is needed for the PX4/Gazebo track.**

### Safe-MARL resources found (support, not reproduction targets)

| Resource | Use | Caveat |
|---|---|---|
| `Qeneb/SS-MARL` (11★) — *Scalable Safe MARL*, arXiv:2501.13727 | MPE modified for **cost constraints**; `MultiAgentConstrainEnv` is a ready scaffold for CMDP-style safe MARL. Runs on CPU. | **arXiv preprint only, not published**; **no license file**; ships only its own GNN algorithm — MAPPO/MACPO/MAPPO-Lagrangian are *not* included despite the README naming them |
| `Qeneb/SMARL-MAFOA` (8★) — *Safe MARL for Multi-Agent Formation Obstacle Avoidance* | Formation + obstacle avoidance in MPE, 3–5 agents, with real-robot experiments | Ground vehicles, not UAVs; no license; venue unclear |
| ElSayed-Aly et al., *Safe MARL via Shielding*, **AAMAS 2021** (arXiv:2101.11196) | **Phase-2 conceptual reference** — centralized vs factored shielding | No public code |
| `chauncygu/Safe-Reinforcement-Learning-Baselines` | Curated index of safe-RL / safe-MARL baselines and which have code | Index only |
| `chauncygu/Safe-Multi-Agent-Mujoco` (79★), `-Isaac-Gym` (66★), `-Robosuite` (27★) | Established safe-MARL benchmark suites | Not UAV; Isaac Gym needs an NVIDIA GPU |

None is a better Phase-1 target than CI-HRL: SS-MARL and SMARL-MAFOA are
unpublished and unlicensed, and none is multi-UAV.

## Consequences for the plan

- **AirSim track is unblocked** and fully specified: reward constants, the
  complete hyperparameter table, PID gains, UAV physical specs, scene geometry
  (14×14×5 m training volume, 16 m test circle), and all four results tables.
- **PX4/Gazebo track is unblocked**, with one new complication: the MAPPO baseline
  is not standalone (see item 2), so the T1 comparison must be scoped explicitly
  rather than assumed.
- Neither paper reports **seeds or error bars**. Every result in both papers is an
  unlabelled point estimate (50 episodes for TNNLS; trial count unstated for
  Drones). Our mean ± std must always be labelled as such in comparisons.
