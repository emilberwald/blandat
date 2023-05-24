def integrate0(*, x0, v0, a0, dt):
    return x0 + (v0 + 1 / 2 * a0 * dt) * dt

def integrate(*, x, t, dx2dt2, dt):
    return x[-1] + ((x[-1] - x[-2]) / (t[-1] - t[-2]) + 1 / 2 * dx2dt2(x[-1], t[-1]) * (t[-1] - t[-2] + dt)) * dt
