"""Module 24 - Neuromorphic SNN simulation."""


def izhikevich_step(v: float, u: float, i: float, a: float = 0.02, b: float = 0.2, c: float = -65, d: float = 8) -> tuple[float, float, bool]:
    v = v + 0.5 * (0.04 * v * v + 5 * v + 140 - u + i)
    v = v + 0.5 * (0.04 * v * v + 5 * v + 140 - u + i)
    u = u + a * (b * v - u)
    spike = v >= 30
    if spike:
        v = c
        u = u + d
    return v, u, spike


def stdp_update(weight: float, dt_ms: float, a_plus: float = 0.01, a_minus: float = 0.012) -> float:
    if dt_ms > 0:
        return min(1.0, weight + a_plus * (2.71828 ** (-dt_ms / 20)))
    return max(0.0, weight - a_minus * (2.71828 ** (dt_ms / 20)))


def energy_saved_joules(cpu_ops: int, snn_spikes: int) -> float:
    return max(0.0, cpu_ops * 1e-6 - snn_spikes * 1e-7)
