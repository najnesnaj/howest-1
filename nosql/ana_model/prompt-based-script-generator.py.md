import numpy as np

# Function to generate a single array with the specified pattern
def generate_synthetic_array(size=70):
    # Target statistical properties
    target_mean = 0.66
    target_std = 0.11
    min_val, max_val = 0.3, 0.9

    # Create a base pattern with periodic fluctuations
    t = np.linspace(0, 10, size)  # Time-like index for smooth transitions
    base_pattern = 0.66 + 0.15 * np.sin(2 * np.pi * t / 5)  # Periodic component (period ~5)
    peaks = np.random.choice([0, 0, 0, 0.2, 0.25], size=size, p=[0.8, 0.1, 0.05, 0.025, 0.025])  # Occasional peaks
    noise = np.random.normal(0, 0.05, size)  # Small noise for variability

    # Combine components
    synthetic_data = base_pattern + peaks + noise

    # Apply slight right skew using a transformation
    synthetic_data = np.clip(synthetic_data, min_val, max_val)
    synthetic_data = min_val + (max_val - min_val) * (synthetic_data - synthetic_data.min()) / (
        synthetic_data.max() - synthetic_data.min()
    )

    # Adjust mean and standard deviation
    current_mean = np.mean(synthetic_data)
    current_std = np.std(synthetic_data)
    synthetic_data = (synthetic_data - current_mean) * (target_std / current_std) + target_mean

    # Clip to ensure values stay within [0.3, 0.9]
    synthetic_data = np.clip(synthetic_data, min_val, max_val)

    # Round to two decimal places
    synthetic_data = np.round(synthetic_data, 2)

    return synthetic_data

# Function to format array as comma-separated string
def format_array_as_comma_separated(arr):
    return ", ".join(f"{x:.2f}" for x in arr)

# Generate multiple arrays
def generate_multiple_arrays(num_arrays=5, size=70):
    arrays = []
    for i in range(num_arrays):
        arr = generate_synthetic_array(size)
        arrays.append(arr)
        # Format as comma-separated string
        formatted_array = format_array_as_comma_separated(arr)
        print(f"Array {i + 1}:")
        print(formatted_array)
        print(f"Mean: {np.mean(arr):.2f}, Std: {np.std(arr):.2f}, Min: {np.min(arr):.2f}, Max: {np.max(arr):.2f}\n")
    return arrays

# Execute the generation
if __name__ == "__main__":
    np.random.seed(42)  # For reproducibility
    generated_arrays = generate_multiple_arrays(num_arrays=5)
