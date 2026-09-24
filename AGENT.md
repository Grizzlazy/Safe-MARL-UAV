# AGENT.md

## Project: Safe MARL for Multi-UAV Swarm

### Goal
Build a small, reproducible research codebase for the course project **Safe Multi-Agent Reinforcement Learning (MARL) for multi-UAV swarm**.

## Phase 1 — Reproduce published work

Phase 1 is **not** the proposed research contribution. The goal is to reproduce existing published multi-UAV MARL results using the platforms suggested by the advisor:

- AirSim
- PX4/Gazebo

For each track, select a specific published paper and document:

- citation, year, DOI/URL
- public code repository, if available
- simulator/environment version
- task/scenario
- algorithm
- hyperparameters/configuration
- evaluation metrics
- reported results
- reproduced results
- deviations

Do not invent a new benchmark and call it a reproduction benchmark.

Do not treat RescueNet or C2A as MARL environments. They are datasets and may only be used if a selected published MARL paper explicitly uses them.

Do not automatically treat UAVBench as a MARL training environment. Verify the selected paper and benchmark protocol first.

## Phase 2 — Research extension

Only after Phase 1 works, identify limitations/gaps and implement a new mechanism. Candidate directions from the advisor include:

- safety shield
- MPC-based safety layer
- constraint repair
- battery constraints
- collision avoidance
- no-fly zones
- connectivity constraints
- robust/uncertain MARL
- multi-objective MARL
- dynamic/online optimization

Keep Phase 2 code separate from the Phase 1 reproduction implementation.

## Reproduction tracks

### Track A — AirSim

Directory:

    environments/airsim/
    reproduce/airsim.py
    configs/airsim.yaml
    results/airsim/

AirSim is the simulator/platform. The exact task, scenario, algorithm and configuration must come from the selected paper.

### Track B — PX4/Gazebo

Directory:

    environments/px4_gazebo/
    reproduce/px4_gazebo.py
    configs/px4_gazebo.yaml
    results/px4_gazebo/

PX4/Gazebo is the simulator/autopilot stack. The exact task, scenario, algorithm and configuration must come from the selected paper.

Do not assume the two tracks implement identical environments.

## Paper selection

Before implementing an algorithm, create:

    papers/airsim/PAPER.md
    papers/px4_gazebo/PAPER.md

Each PAPER.md must contain:

    # Paper
    ## Citation
    ## DOI / URL
    ## Code repository
    ## Environment
    ## Task
    ## Algorithm
    ## Baselines
    ## Metrics
    ## Reported experiments
    ## Reproduction target
    ## Known gaps

Do not claim exact reproduction is possible until the environment, algorithm and experimental protocol are checked.

## Algorithm organization

Keep algorithms modular:

    algorithms/
      ippo.py
      mappo.py

If the selected paper provides official code, prefer using it when licensing/project requirements allow. Otherwise reproduce the algorithm faithfully.

Do not silently change observation/action spaces, reward, architecture, training budget, optimizer, discount factor, PPO clipping, entropy coefficient, number of agents, episode length, or evaluation protocol. Document necessary changes.

## Minimal environment interface

Where practical, expose:

    reset()
    step(actions)
    close()

Adapters translate simulator-native APIs into the training/evaluation format. Do not build a large abstraction framework.

## Training and reproducibility

Example commands:

    python reproduce/airsim.py --config configs/airsim.yaml
    python reproduce/px4_gazebo.py --config configs/px4_gazebo.yaml

Every run must record:

- random seed
- git commit/version
- configuration
- simulator version
- algorithm
- number of UAVs
- training steps
- checkpoint
- evaluation results

Default seeds when feasible:

    [0, 1, 2, 3, 4]

Report mean ± standard deviation. If the paper uses another protocol, reproduce that first and optionally add seeds.

## Evaluation

Follow the selected paper as closely as possible and record its reported metrics. Potential Safe MARL/multi-UAV metrics include:

- episode reward
- task/mission success rate
- collision count/rate
- minimum inter-UAV distance
- obstacle violations
- boundary/no-fly-zone violations
- mission completion time
- energy/battery consumption
- trajectory/path efficiency
- training time
- inference/runtime

Clearly distinguish:

    Paper reported result
    Reproduced result
    Our additional experiment

## Comparison with paper

Use a table such as:

| Item | Paper | Ours |
|---|---|---|
| Environment | ... | ... |
| UAVs | ... | ... |
| Algorithm | ... | ... |
| Training steps | ... | ... |
| Seeds | ... | ... |
| Reward | ... | ... |
| Success rate | ... | ... |
| Collision rate | ... | ... |
| Runtime | ... | ... |

If results differ substantially, investigate simulator/version, hardware, seed, hyperparameters, reward, observation/action mismatch, training budget and evaluation protocol. Do not tune solely to match the paper without documenting it.

## Phase 2 safety extension

Reuse the reproduced baseline. Example:

    MAPPO
      |
      +-- Safety Shield
      +-- Constraint Repair
      +-- MPC safety layer

Compare the original reproduced method against the proposed method under the same environment/scenarios/seeds/protocol whenever possible. For safety methods evaluate collision rate, constraint violation, task success, reward, runtime overhead and scalability.

## Repository structure

Keep the repository small:

    safe-marl-uav/
    ├── AGENT.md
    ├── README.md
    ├── requirements.txt
    ├── papers/
    │   ├── airsim/PAPER.md
    │   └── px4_gazebo/PAPER.md
    ├── configs/
    │   ├── airsim.yaml
    │   └── px4_gazebo.yaml
    ├── environments/
    │   ├── airsim/adapter.py
    │   └── px4_gazebo/adapter.py
    ├── algorithms/
    │   ├── ippo.py
    │   └── mappo.py
    ├── reproduce/
    │   ├── airsim.py
    │   └── px4_gazebo.py
    ├── evaluate/
    │   ├── metrics.py
    │   └── compare.py
    ├── utils/seed.py
    └── results/

Do not create unnecessary modules.

## Development order

1. Select and verify the AirSim paper.
2. Select and verify the PX4/Gazebo paper.
3. Write both PAPER.md files.
4. Verify simulator versions, dependencies and hardware requirements.
5. Run original/public code when available.
6. Create minimal adapters only where necessary.
7. Reproduce the main experiment.
8. Run multiple seeds and evaluate.
9. Compare against the paper.
10. Only then begin Phase 2.

## Important constraints

1. Do not invent benchmark results.
2. Do not claim reproduction without actually running the experiment.
3. Do not use a synthetic environment as the main Phase 1 result.
4. Do not call RescueNet/C2A a MARL benchmark.
5. Do not automatically call UAVBench a MARL environment.
6. Do not add Safety Shield/MPC/Constraint Repair to Phase 1.
7. Do not over-engineer the codebase.
8. Keep simulator-specific code inside its adapter.
9. Keep the reproduced baseline unchanged whenever possible.
10. Document every deviation from the paper.

## Definition of Done — Phase 1

- [ ] one AirSim paper selected and documented
- [ ] one PX4/Gazebo paper selected and documented
- [ ] both experiment protocols verified
- [ ] public code used when available
- [ ] main experiment runs successfully
- [ ] results saved reproducibly
- [ ] multiple seeds evaluated where feasible
- [ ] paper and reproduced results compared
- [ ] deviations documented
- [ ] source code runnable by another group member

Phase 2 starts only after these requirements are satisfied.
