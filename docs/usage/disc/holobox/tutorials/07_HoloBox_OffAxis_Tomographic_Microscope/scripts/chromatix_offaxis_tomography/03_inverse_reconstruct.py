import jax
import jax.numpy as jnp
import optax
import chromatix.functional as cf

def forward_one_angle(sample_delay, sample_absorption, angle_rad, params):
    # rotate volume around the tube axis (simplified placeholder)
    # implement rotation with jax.scipy.ndimage.map_coordinates or your own sampler
    # sample_delay_rot = rotate(sample_delay, angle_rad)
    # sample_absorption_rot = rotate(sample_absorption, angle_rad)
    sample_delay_rot = sample_delay
    sample_absorption_rot = sample_absorption

    ref = cf.plane_wave(
        shape=params["shape"], dx=params["dx"], spectrum=params["wavelength"],
        spectral_density=1.0, power=1.0, kykx=params["kykx"]
    )
    samp = cf.plane_wave(
        shape=params["shape"], dx=params["dx"], spectrum=params["wavelength"],
        spectral_density=1.0, power=1.0
    )
    samp = cf.multislice_thick_sample(
        samp, sample_absorption_rot, sample_delay_rot,
        params["n_medium"], params["thickness"], N_pad=0
    )
    holo = (ref + samp).intensity
    return holo

@jax.jit
def loss_fn(sample_delay, sample_absorption, angles, measured, params):
    pred = jax.vmap(lambda a: forward_one_angle(sample_delay, sample_absorption, a, params))(angles)
    data_loss = jnp.mean((pred - measured)**2)
    # simple TV-like proxy (use a better one in practice)
    reg = 1e-4 * (jnp.mean(jnp.abs(jnp.diff(sample_delay, axis=-1))) + jnp.mean(jnp.abs(jnp.diff(sample_delay, axis=-2))))
    return data_loss + reg

def run_optimization(measured, angles, params, iters=200):
    key = jax.random.PRNGKey(0)
    z = params["z_slices"]
    H, W = params["shape"]
    sample_delay = jnp.zeros((z, H, W), dtype=jnp.float32)
    sample_abs = jnp.zeros((z, H, W), dtype=jnp.float32)

    opt = optax.adam(1e-2)
    opt_state = opt.init((sample_delay, sample_abs))

    @jax.jit
    def step(state, opt_state):
        sd, sa = state
        loss, grads = jax.value_and_grad(loss_fn, argnums=(0, 1))(sd, sa, angles, measured, params)
        updates, opt_state2 = opt.update(grads, opt_state, state)
        state2 = optax.apply_updates(state, updates)
        return state2, opt_state2, loss

    state = (sample_delay, sample_abs)
    for _ in range(iters):
        state, opt_state, loss = step(state, opt_state)
    return state, loss
