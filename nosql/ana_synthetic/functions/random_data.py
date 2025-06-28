#import random
import numpy as np
import json


def generate_random_data(length=70, period1=7, period2=14, noise_level=0.15):
    """
    Generate synthetic data mimicking the provided dataset with quasi-periodic patterns.
    
    Args:
        length (int): Number of data points (default: 70).
        period1 (float): Primary period of sinusoidal component (default: 7).
        period2 (float): Secondary period for added complexity (default: 14).
        noise_level (float): Magnitude of random noise (default: 0.15).
    
    Returns:
        np.array: Array of length values in [0, 1] with periodic pattern.
    """
    t = np.arange(length)
    # Combine two sinusoids for quasi-periodic pattern
    base_pattern = 0.5 * np.sin(2 * np.pi * t / period1) + 0.3 * np.sin(2 * np.pi * t / period2)
    
    # Add controlled noise
    noise = np.random.normal(0, noise_level, length)
    synthetic_data = base_pattern + noise
    
    # Normalize to [0, 1]
    synthetic_data = (synthetic_data - np.min(synthetic_data)) / (np.max(synthetic_data) - np.min(synthetic_data))
    
    # Ensure some troughs reach near 0.0 and peaks near 1.0
    synthetic_data = np.clip(synthetic_data, 0.0, 1.0)
    
    return np.round(synthetic_data, 6)



#def generate_random_data(n=69):
#    assert n >= 33, "Need enough space to insert 4 high values with 8 apart"
#
#    valid_quads = []
#    for i in range(0, n - 24):
#        for j in range(i + 8, n - 16):
#            for k in range(j + 8, n - 8):
#                for l in range(k + 8, n):
#                    valid_quads.append((i, j, k, l))
#
#    chosen_quad = random.choice(valid_quads)
#    high_positions = set(chosen_quad)
#
#    data = [random.randint(30, 70)]
#    for i in range(1, n):
#        if i in high_positions:
#            value = random.randint(81, 100)
#        else:
#            prev = data[i - 1]
#            low = max(1, prev - 20)
#            high = min(100, prev + 20)
#            value = random.randint(low, high)
#            if value > 80:
#                value = random.randint(low, min(80, high))
#        data.append(value)
#
#    return data
