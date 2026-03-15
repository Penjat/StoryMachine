from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import laplace
from scipy.ndimage import gaussian_filter


def pink_noise(shape):
    noise = np.random.randn(*shape)

    F = np.fft.fftn(noise)

    freqs = np.meshgrid(*[np.fft.fftfreq(n) for n in shape], indexing="ij")
    radius = np.sqrt(sum(f**2 for f in freqs))
    radius[0, 0] = 1  # avoid divide-by-zero

    F_pink = F / np.sqrt(radius)

    pink = np.real(np.fft.ifftn(F_pink))
    return pink

def blue_noise(shape):
    noise = np.random.randn(*shape)

    F = np.fft.fftn(noise)

    freqs = np.meshgrid(*[np.fft.fftfreq(n) for n in shape], indexing="ij")
    radius = np.sqrt(sum(f**2 for f in freqs))

    radius[tuple([0]*len(shape))] = 1

    F_blue = F * np.sqrt(radius)

    blue = np.real(np.fft.ifftn(F_blue))
    return blue

def brown_noise(shape):
    noise = np.random.randn(*shape)

    F = np.fft.fftn(noise)

    freqs = np.meshgrid(*[np.fft.fftfreq(n) for n in shape], indexing="ij")
    radius = np.sqrt(sum(f**2 for f in freqs))

    radius[tuple([0]*len(shape))] = 1  # avoid divide-by-zero

    F_brown = F / (radius**2)

    brown = np.real(np.fft.ifftn(F_brown))

    # normalize 0–1
    brown -= brown.min()
    brown /= brown.max()

    return brown

def colored_noise(shape, alpha=0, min_val=-1, max_val=1):
    noise = np.random.randn(*shape)

    F = np.fft.fftn(noise)

    freqs = np.meshgrid(*[np.fft.fftfreq(n) for n in shape], indexing="ij")
    radius = np.sqrt(sum(f**2 for f in freqs))

    radius[tuple([0]*len(shape))] = 1

    F_colored = F / (radius ** (alpha/2))

    result = np.real(np.fft.ifftn(F_colored))

    # normalize 0–1
    result -= result.min()
    result /= result.max()

    # scale to desired range
    result = min_val + (max_val - min_val) * result

    return result

def perlin_noise_2d(shape, scale=10, octaves=1, seed=None):
    """
    Generate 2D Perlin noise.
    
    Parameters
    ----------
    shape : tuple of ints (height, width)
    scale : float
        How many “grid cells” fit across the image. Larger = smoother noise.
    octaves : int
        Number of octaves (higher = more detail)
    seed : int or None
        Random seed for reproducibility
        
    Returns
    -------
    2D numpy array in [-1, 1]
    """
    if seed is not None:
        np.random.seed(seed)
    
    height, width = shape
    noise = np.zeros((height, width))
    
    frequency = 1.0
    amplitude = 1.0
    max_amp = 0.0
    
    for _ in range(octaves):
        # Grid coordinates
        y = np.linspace(0, scale*frequency, height, endpoint=False)
        x = np.linspace(0, scale*frequency, width, endpoint=False)
        xi, yi = np.meshgrid(x, y)
        
        # Integer coordinates
        x0 = np.floor(xi).astype(int)
        y0 = np.floor(yi).astype(int)
        x1 = x0 + 1
        y1 = y0 + 1
        
        # Fractional parts
        xf = xi - x0
        yf = yi - y0
        
        # Random gradients at corners
        gradients = np.random.uniform(-1, 1, (scale*int(frequency)+2, scale*int(frequency)+2))
        g00 = gradients[y0 % gradients.shape[0], x0 % gradients.shape[1]]
        g10 = gradients[y0 % gradients.shape[0], x1 % gradients.shape[1]]
        g01 = gradients[y1 % gradients.shape[0], x0 % gradients.shape[1]]
        g11 = gradients[y1 % gradients.shape[0], x1 % gradients.shape[1]]
        
        # Dot product
        d00 = g00 * (xf) + g00 * (yf)
        d10 = g10 * (xf-1) + g10 * (yf)
        d01 = g01 * (xf) + g01 * (yf-1)
        d11 = g11 * (xf-1) + g11 * (yf-1)
        
        # Fade function
        def fade(t):
            return t**3 * (t * (t * 6 - 15) + 10)
        
        u = fade(xf)
        v = fade(yf)
        
        # Bilinear interpolation
        nx0 = d00*(1-u) + d10*u
        nx1 = d01*(1-u) + d11*u
        nxy = nx0*(1-v) + nx1*v
        
        # Add octave contribution
        noise += nxy * amplitude
        max_amp += amplitude
        
        amplitude /= 2
        frequency *= 2
    
    # Normalize to [-1, 1]
    noise /= max_amp
    noise -= noise.min()
    noise /= noise.max()
    noise = noise * 2 - 1
    
    return noise


img = Image.open('boat.JPG').resize((384,726))

img_array = np.asarray(img)



array = np.mean(img_array, axis=2)

shape = (726,384)
noise_img = perlin_noise_2d(shape, scale=8, octaves=4, seed=123)

array = array + colored_noise((726,384), -2, -100, 100)
array[array <= 180] = 0
array[array > 180] = 1


plt.imshow(array)
plt.axis('off') 
plt.show()





# plt.figure(figsize=(6,6))
# plt.imshow(noise_img, cmap='gray')
# plt.title("2D Perlin Noise")
# plt.axis('off')
# plt.show()


print("hello butt face")

