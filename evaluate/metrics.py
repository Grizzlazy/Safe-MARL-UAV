"""Evaluation metrics, defined exactly as the two reproduced papers define them.

AirSim track  -- Fan et al., Drones 9(1):10, 2025, Section 4.2.1.
                 SSR, ISR, SPL, Extra Distance, Average Speed.
PX4 track     -- Xiang et al., IEEE TNNLS 36(10), 2025, Sections V-B1 and V-D1.
                 R_L/R_H, F, N, C, and the reward decomposition R_t/R_n/R_e, E.

Do not add metrics that neither paper reports (AGENT.md §10). Do not change a
definition to make results look better -- change it only if the paper is
misread, and then say so in the relevant PAPER.md.
"""

from __future__ import annotations

import dataclasses
from typing import Sequence

import numpy as np

# ---------------------------------------------------------------------------
# AirSim track (Drones 2025)
# ---------------------------------------------------------------------------


@dataclasses.dataclass
class UAVEpisodeResult:
    """One UAV's outcome in one episode."""

    reached_goal: bool
    collided: bool
    shortest_distance_m: float   # l -- straight-line start to target
    path_length_m: float         # p -- distance actually flown
    flight_time_s: float

    @property
    def success(self) -> bool:
        """Paper's ISR wording: reaches its target *without* colliding."""
        return self.reached_goal and not self.collided


def swarm_success_rate(episodes: Sequence[Sequence[UAVEpisodeResult]]) -> float:
    """SSR (%) -- fraction of episodes in which EVERY UAV succeeds.

    Drones 2025: "the fraction of trials where the entire UAV fleet successfully
    reaches the designated target locations".
    """
    if not episodes:
        return float("nan")
    whole = [all(u.success for u in ep) for ep in episodes]
    return 100.0 * float(np.mean(whole))


def individual_success_rate(episodes: Sequence[Sequence[UAVEpisodeResult]]) -> float:
    """ISR (%) -- fraction of individual UAVs that succeed, pooled over episodes."""
    uavs = [u for ep in episodes for u in ep]
    if not uavs:
        return float("nan")
    return 100.0 * float(np.mean([u.success for u in uavs]))


def spl(episodes: Sequence[Sequence[UAVEpisodeResult]]) -> float:
    """SPL (%) -- Success weighted by Path Length.

    Drones 2025 Eq. (12):  SPL = sigma * l / max(l, p)
    sigma is the binary success indicator, so failures contribute 0.
    """
    uavs = [u for ep in episodes for u in ep]
    if not uavs:
        return float("nan")
    vals = []
    for u in uavs:
        if not u.success:
            vals.append(0.0)
            continue
        denom = max(u.shortest_distance_m, u.path_length_m)
        # A zero-length task is degenerate; treat as perfect rather than dividing by 0.
        vals.append(1.0 if denom <= 0 else u.shortest_distance_m / denom)
    return 100.0 * float(np.mean(vals))


def extra_distance(episodes: Sequence[Sequence[UAVEpisodeResult]]) -> tuple[float, float]:
    """Extra Distance (m) as (mean, std) -- flown path minus shortest path.

    The paper reports this as "mean/std" over UAVs.
    """
    uavs = [u for ep in episodes for u in ep]
    if not uavs:
        return float("nan"), float("nan")
    extras = np.array([u.path_length_m - u.shortest_distance_m for u in uavs], dtype=float)
    return float(extras.mean()), float(extras.std())


def average_speed(episodes: Sequence[Sequence[UAVEpisodeResult]]) -> tuple[float, float]:
    """Average Speed (m/s) as (mean, std) over all UAVs."""
    uavs = [u for ep in episodes for u in ep]
    speeds = np.array(
        [u.path_length_m / u.flight_time_s for u in uavs if u.flight_time_s > 0],
        dtype=float,
    )
    if speeds.size == 0:
        return float("nan"), float("nan")
    return float(speeds.mean()), float(speeds.std())


def airsim_metrics(episodes: Sequence[Sequence[UAVEpisodeResult]]) -> dict[str, float]:
    """All five Drones-2025 metrics in one dict, keys matching configs/airsim.yaml."""
    ed_mean, ed_std = extra_distance(episodes)
    sp_mean, sp_std = average_speed(episodes)
    return {
        "ssr": swarm_success_rate(episodes),
        "isr": individual_success_rate(episodes),
        "spl": spl(episodes),
        "extra_distance": ed_mean,
        "extra_distance_std": ed_std,
        "average_speed": sp_mean,
        "average_speed_std": sp_std,
        "n_episodes": len(episodes),
    }


# ---------------------------------------------------------------------------
# PX4/Gazebo track (TNNLS 2025)
# ---------------------------------------------------------------------------


def hausdorff_distance(a: np.ndarray, b: np.ndarray) -> float:
    """One-sided HD as the paper defines it: max_{x in A} min_{y in B} ||x - y||.

    TNNLS 2025 Appendix A: HD(E1, E2) = max_{x in E1} min_{y in E2} ||x - y||.
    Note this is the *directed* distance -- not the symmetric Hausdorff.
    """
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.size == 0 or b.size == 0:
        return float("nan")
    d = np.linalg.norm(a[:, None, :] - b[None, :, :], axis=-1)
    return float(d.min(axis=1).max())


def formation_stability(
    formation_errors_m: Sequence[float], dt_s: float, threshold_m: float = 1.0
) -> float:
    """F (s) -- time per episode with HD-based formation error below threshold."""
    err = np.asarray(formation_errors_m, dtype=float)
    return float(np.sum(err < threshold_m) * dt_s)


def navigation_efficiency(
    distances_to_target_m: Sequence[float], dt_s: float, threshold_m: float = 1.0
) -> float:
    """N (s) -- time spent within `threshold_m` of the destination."""
    d = np.asarray(distances_to_target_m, dtype=float)
    return float(np.sum(d < threshold_m) * dt_s)


def collision_probability(collision_flags: Sequence[bool]) -> float:
    """C (%) -- fraction of timesteps in a collision state."""
    f = np.asarray(collision_flags, dtype=bool)
    if f.size == 0:
        return float("nan")
    return 100.0 * float(f.mean())


def danger_time(
    adversary_distances_m: Sequence[float], dt_s: float, threshold_m: float = 2.0
) -> float:
    """E (s) -- average time per round in a dangerous state (adversary < 2 m)."""
    d = np.asarray(adversary_distances_m, dtype=float)
    return float(np.sum(d < threshold_m) * dt_s)


# ---------------------------------------------------------------------------
# Aggregation across seeds
# ---------------------------------------------------------------------------


def aggregate_seeds(per_seed: Sequence[dict[str, float]]) -> dict[str, dict[str, float]]:
    """Aggregate per-seed metric dicts into mean/std/n.

    Neither paper reports seeds or error bars, so results produced here MUST be
    labelled "our mean +/- std over N seeds" whenever they are placed beside a
    paper's unlabelled point estimate (AGENT.md §9).
    """
    if not per_seed:
        return {}
    keys = set().union(*(d.keys() for d in per_seed))
    out: dict[str, dict[str, float]] = {}
    for k in sorted(keys):
        vals = np.array(
            [d[k] for d in per_seed if k in d and d[k] is not None], dtype=float
        )
        vals = vals[~np.isnan(vals)]
        if vals.size == 0:
            continue
        out[k] = {
            "mean": float(vals.mean()),
            "std": float(vals.std(ddof=1)) if vals.size > 1 else 0.0,
            "n_seeds": int(vals.size),
        }
    return out
