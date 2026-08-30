"""Pure-Python double cart-pole integrator.

Port of the C++ extension in dpole.cpp (Wieland's equations, RK4).
The original C++ source is kept for reference; this module is the default.
"""
import math

FORCE_MAG = 10.0
GRAVITY = -9.8
LENGTH_1 = 0.5
LENGTH_2 = 0.05
MASSPOLE_1 = 0.1
MASSPOLE_2 = 0.01
MASSCART = 1.0
MUP = 0.000002
TAU = 0.01


def _step(action, state, dydx):
    force = (action - 0.5) * FORCE_MAG * 2.0
    costheta_1 = math.cos(state[2])
    sintheta_1 = math.sin(state[2])
    gsintheta_1 = GRAVITY * sintheta_1
    costheta_2 = math.cos(state[4])
    sintheta_2 = math.sin(state[4])
    gsintheta_2 = GRAVITY * sintheta_2

    ml_1 = LENGTH_1 * MASSPOLE_1
    ml_2 = LENGTH_2 * MASSPOLE_2
    temp_1 = MUP * state[3] / ml_1
    temp_2 = MUP * state[5] / ml_2

    fi_1 = (ml_1 * state[3] * state[3] * sintheta_1) + \
           (0.75 * MASSPOLE_1 * costheta_1 * (temp_1 + gsintheta_1))
    fi_2 = (ml_2 * state[5] * state[5] * sintheta_2) + \
           (0.75 * MASSPOLE_2 * costheta_2 * (temp_2 + gsintheta_2))

    mi_1 = MASSPOLE_1 * (1 - (0.75 * costheta_1 * costheta_1))
    mi_2 = MASSPOLE_2 * (1 - (0.75 * costheta_2 * costheta_2))

    dydx[1] = (force + fi_1 + fi_2) / (mi_1 + mi_2 + MASSCART)
    dydx[3] = -0.75 * (dydx[1] * costheta_1 + gsintheta_1 + temp_1) / LENGTH_1
    dydx[5] = -0.75 * (dydx[1] * costheta_2 + gsintheta_2 + temp_2) / LENGTH_2


def _rk4(f, state, dydx):
    hh = TAU * 0.5
    h6 = TAU / 6.0
    dym = [0.0] * 6
    dyt = [0.0] * 6
    yt = [0.0] * 6

    for i in range(6):
        yt[i] = state[i] + hh * dydx[i]

    _step(f, yt, dyt)
    dyt[0] = yt[1]
    dyt[2] = yt[3]
    dyt[4] = yt[5]

    for i in range(6):
        yt[i] = state[i] + hh * dyt[i]

    _step(f, yt, dym)
    dym[0] = yt[1]
    dym[2] = yt[3]
    dym[4] = yt[5]

    for i in range(6):
        yt[i] = state[i] + TAU * dym[i]
        dym[i] += dyt[i]

    _step(f, yt, dyt)
    dyt[0] = yt[1]
    dyt[2] = yt[3]
    dyt[4] = yt[5]

    for i in range(6):
        state[i] += h6 * (dydx[i] + dyt[i] + 2.0 * dym[i])


def integrate(action, state, stepnum):
    """Advance the cart-pole state by ``stepnum`` RK4 pairs.

    Parameters match the old C++ extension:
    action -- force mapped from network output in [0, 1]
    state -- list of 6 floats [x, xdot, theta1, theta1dot, theta2, theta2dot]
    stepnum -- number of outer integration steps
    """
    state = list(state)
    dydx = [0.0] * 6
    for _k in range(stepnum):
        for _i in range(2):
            dydx[0] = state[1]
            dydx[2] = state[3]
            dydx[4] = state[5]
            _step(action, state, dydx)
            _rk4(action, state, dydx)
    return state
