#import random
import numpy as np
import json


def generate_random_data(max_change=0.15, min_val=0.01, max_val=1.0):
    """
    Generate a variation of the input data by randomly increasing/decreasing values.
    
    Args:
        original_data (list): Original dataset with 67 float values.
        max_change (float): Maximum allowed change (increase or decrease).
        min_val (float): Minimum value for the new data (0.1).
        max_val (float): Maximum value for the new data (1.0).
    
    Returns:
        list: New dataset with varied values.
    """
# Original dataset
#    original_data = [
#    0.734500750153661, 0.012759170653907496, 0.0, 0.16108452950558214, 0.18819776714513556,
#    0.17384370015948963, 0.3237639553429027, 0.2886762360446571, 0.49282296650717705,
#    0.6299840510366826, 0.5821371610845295, 0.7192982456140351, 0.29984051036682613,
#    0.2886762360446571, 0.430622009569378, 0.2727272727272727, 0.19138755980861244,
#    0.19776714513556617, 0.28708133971291866, 0.37320574162679426, 0.6985557783658096,
#    0.6682615629984051, 0.6092503987240829, 0.5614035087719298, 0.30303030303030304,
#    0.2711323763955343, 0.2583732057416268, 0.4529505582137161, 0.11164274322169059,
#    0.22169059011164274, 0.2966507177033493, 0.22328548644338117, 0.3492822966507177,
#    0.4864433811802233, 0.6650717703349283, 0.810207336523126, 0.7240829346092504,
#    0.8421052631578947, 0.8213716108452951, 0.6889952153110048, 0.8564593301435407,
#    0.45454545454545453, 0.8229665071770335, 1.0, 0.48165869218500795, 0.5215311004784688,
#    0.16905901116427433, 0.3004784688995215, 0.4251993620414673, 0.44657097288676234,
#    0.6491228070175439, 0.7200956937799043, 0.8405103668261563, 0.6810207336523126,
#    0.4076555023923445, 0.23700159489633174, 0.11483253588516747, 0.2784688995215311,
#    0.5861244019138756, 0.4920255183413078, 0.3289922150658493, 0.43219972469425305,
#    0.6128128665439596, 0.6369501066989895, 0.45680484394964327
#    ]
#
    original_data = [0.806, 0.278, 0.268, 0.386, 0.406, 0.396, 0.505, 0.480, 0.629, 0.729,
    0.694, 0.795, 0.488, 0.480, 0.583, 0.468, 0.408, 0.413, 0.478, 0.541,
    0.779, 0.757, 0.714, 0.679, 0.490, 0.467, 0.457, 0.600, 0.350, 0.431,
    0.485, 0.432, 0.524, 0.624, 0.755, 0.861, 0.798, 0.884, 0.869, 0.772,
    0.895, 0.601, 0.870, 1.000, 0.621, 0.650, 0.392, 0.488, 0.579, 0.595,
    0.743, 0.795, 0.883, 0.767, 0.567, 0.442, 0.352, 0.472, 0.697, 0.628,
    0.509, 0.585, 0.717, 0.734, 0.603]

    # Convert input to numpy array for efficient computation
    data = np.array(original_data)

    # Perform a random circular shift
#TODO if I shift data, it does not filter DEZ
#    shift_amount = np.random.randint(0, len(data))  # Random shift between 0 and 66
    shift_amount = 0 
    rotated_data = np.roll(data, shift_amount)  # Circular shift by random amount    
    #rotated_data = data
    # Generate random changes within [-max_change, max_change]
    changes = np.random.uniform(-max_change, max_change, len(data))
    
    # Apply changes and clip to ensure values stay within [min_val, max_val]
    varied_data = np.clip(rotated_data + changes, min_val, max_val)
    print (varied_data)    
    return varied_data.tolist()

def generate_multiple_variations(original_data, num_variations=5, max_change=0.15, min_val=0.1, max_val=1.0):
    """
    Generate multiple variations of the original dataset.
    
    Args:
        original_data (list): Original dataset.
        num_variations (int): Number of variations to generate.
        max_change (float): Maximum allowed change.
        min_val (float): Minimum value for the new data.
        max_val (float): Maximum value for the new data.
    
    Returns:
        list: List of varied datasets.
    """
    variations = []
    for _ in range(num_variations):
        variation = generate_data_variation(original_data, max_change, min_val, max_val)
        variations.append(variation)
    return variations



# Fix values below 0.1 in the original data to meet the [0.1, 1] constraint
#original_data = [max(x, 0.1) for x in original_data]

# Generate multiple variations
#num_variations = 3  # Number of variations to generate
#variations = generate_multiple_variations(original_data, num_variations=num_variations)

# Generate plot JSON for the first variation
#plot_json = generate_plot_json(variations[0])

# Print variations for verification
#for i, variation in enumerate(variations):
#    print(f"Variation {i+1}:", variation)

# Print plot JSON for the first variation (optional, for verification)
#print("\nPlot JSON for Variation 1:", json.dumps(plot_json, indent=2))






#def generate_random_data(length=70, period1=6, period2=13, noise_level=0.18):
#    """
#    Generate synthetic data mimicking the provided dataset with quasi-periodic patterns.
#    
#    Args:
#        length (int): Number of data points (default: 70).
#        period1 (float): Primary period of sinusoidal component (default: 7).
#        period2 (float): Secondary period for added complexity (default: 14).
#        noise_level (float): Magnitude of random noise (default: 0.15).
#    
#    Returns:
#        np.array: Array of length values in [0, 1] with periodic pattern.
#    """
#    t = np.arange(length)
#    # Combine two sinusoids for quasi-periodic pattern
#    base_pattern = 0.5 * np.sin(2 * np.pi * t / period1) + 0.3 * np.sin(2 * np.pi * t / period2)
#    
#    # Add controlled noise
#    noise = np.random.normal(0, noise_level, length)
#    synthetic_data = base_pattern + noise
#    
#    # Normalize to [0, 1]
#    synthetic_data = (synthetic_data - np.min(synthetic_data)) / (np.max(synthetic_data) - np.min(synthetic_data))
#    
#    # Ensure some troughs reach near 0.0 and peaks near 1.0
#    synthetic_data = np.clip(synthetic_data, 0.0, 1.0)
#    
#    return np.round(synthetic_data, 6)



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
