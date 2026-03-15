import matplotlib.pyplot as plt


import numpy as np

def triangle_wave(t, freq=1):
    """
    Triangle wave with amplitude [-1, 1] and given frequency.
    t : array-like
    freq : number of cycles per unit of t
    """
    return 2 * np.abs(2*(t*freq - np.floor(t*freq + 0.5))) - 1


def square_wave(t, freq=1):
    """
    Square wave with amplitude [-1, 1] and given frequency.
    """
    return np.sign(np.sin(2 * np.pi * freq * t))


def saw_wave(t, freq=1):
    """
    Sawtooth wave with amplitude [-1, 1] and given frequency.
    """
    return 2*(t*freq - np.floor(t*freq + 0.5))



def colored_noise_wave(t, alpha=0):
    """
    Generate colored noise as a wave function.
    
    Parameters
    ----------
    t : 1D array of time values
    alpha : spectral exponent
        -1 = blue, 0 = white, 1 = pink, 2 = brown
    
    Returns
    -------
    1D array of same shape as t, values in [-1, 1]
    """
    N = len(t)
    
    # Start with white noise
    noise = np.random.randn(N)
    
    # FFT
    F = np.fft.fft(noise)
    
    # Frequency bins
    freqs = np.fft.fftfreq(N)
    radius = np.abs(freqs)
    radius[0] = 1  # avoid divide-by-zero
    
    # Scale amplitudes according to alpha
    F_colored = F / (radius ** (alpha / 2))
    
    # Back to time domain
    result = np.real(np.fft.ifft(F_colored))
    
    # Normalize to [-1, 1]
    result -= result.min()
    result /= result.max()
    result = result * 2 - 1
    
    return result

def perlin_noise_1d(t, seed=None):
    if seed is not None:
        np.random.seed(seed)
    
    N = len(t)
    # Generate random gradients at integer points
    gradients = np.random.uniform(-1, 1, N+1)
    
    # Find integer parts and fractional parts
    t_floor = np.floor(t * (N-1)).astype(int)
    t_frac  = t * (N-1) - t_floor
    
    # Linear interpolation
    g0 = gradients[t_floor]
    g1 = gradients[t_floor + 1]
    
    # Smoothstep for smooth interpolation
    fade = t_frac**3 * (t_frac * (t_frac * 6 - 15) + 10)
    
    return (1 - fade) * g0 + fade * g1


t = np.linspace(0, 1, 1000)

plt.figure(figsize=(12,6))

# plt.plot(t, triangle_wave(t, freq=5), label='Triangle Wave')
# plt.plot(t, square_wave(t, freq=5), label='Square Wave')
# plt.plot(t, saw_wave(t, freq=5), label='Saw Wave')
# plt.plot(t, colored_noise_wave(t, alpha=0), label='White Noise', alpha=0.6)
plt.plot(t, saw_wave(t, freq=5) + colored_noise_wave(t, alpha=0)*0.4, label='Pink Noise', alpha=0.6)
# plt.plot(t, colored_noise_wave(t, alpha=2), label='Brown Noise', alpha=0.6)
# plt.plot(t, colored_noise_wave(t, alpha=-1), label='Blue Noise', alpha=0.6)

t = np.linspace(0, 1, 1000)

plt.figure(figsize=(12,4))
plt.plot(t, perlin_noise_1d(t, seed=42), label='Perlin Noise')
plt.plot(t, triangle_wave(t, freq=5), label='Triangle Wave', alpha=0.5)
plt.grid(True)
plt.legend()
plt.show()
