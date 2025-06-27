import numpy as np
import pandas as pd

# Set random seed for reproducibility
np.random.seed(42)

# Parameters
n_samples = 5000  # Total number of arrays (50% random, 50% patterned)
array_size = 70   # Each array has 70 values
value_range = (1, 100)  # Values between 1 and 100
max_diff = 20     # Maximum difference between consecutive values
n_peaks = 4       # Number of values > 80 in patterned arrays
min_peak_distance = 8  # Minimum distance between peaks

# Function to generate a random array with max consecutive difference <= 20
def generate_random_array(size, value_range, max_diff):
    array = np.zeros(size, dtype=int)
    array[0] = np.random.randint(value_range[0], value_range[1] + 1)
    for i in range(1, size):
        min_val = max(value_range[0], array[i-1] - max_diff)
        max_val = min(value_range[1], array[i-1] + max_diff)
        array[i] = np.random.randint(min_val, max_val + 1)
    return array

# Function to generate a patterned array with exactly 4 peaks > 80, at least 8 indices apart
def generate_pattern_array(size, value_range, max_diff, n_peaks, min_peak_distance):
    # Initialize array
    array = np.zeros(size, dtype=int)
    
    # Select peak indices ensuring minimum distance
    possible_indices = list(range(size))
    peak_indices = []
    while len(peak_indices) < n_peaks:
        if not possible_indices:
            return generate_pattern_array(size, value_range, max_diff, n_peaks, min_peak_distance)
        idx = np.random.choice(possible_indices)
        peak_indices.append(idx)
        start = max(0, idx - min_peak_distance)
        end = min(size, idx + min_peak_distance + 1)
        possible_indices = [i for i in possible_indices if i < start or i >= end]
    peak_indices.sort()

    # Generate array values
    for i in range(size):
        if i == 0:
            # First value: random within constraints
            if i in peak_indices:
                array[i] = np.random.randint(81, value_range[1] + 1)
            else:
                array[i] = np.random.randint(value_range[0], 80 + 1)
        else:
            # Determine valid range based on previous value and peak/non-peak status
            min_val = max(value_range[0], array[i-1] - max_diff)
            max_val = min(value_range[1], array[i-1] + max_diff)
            if i in peak_indices:
                min_val = max(81, min_val)
            else:
                max_val = min(80, max_val)
            
            # Check for valid range
            if min_val > max_val:
                # Adjust previous value to make the current value feasible
                if i in peak_indices:
                    # Need a peak (> 80), so ensure previous value allows it
                    prev_min = max(1, min_val - max_diff)
                    prev_max = min(80 if i-1 not in peak_indices else 100, max_val + max_diff)
                else:
                    # Need a non-peak (≤ 80), so ensure previous value allows it
                    prev_min = max(1, min_val - max_diff)
                    prev_max = min(80, max_val + max_diff)
                
                # Ensure the adjustment respects the difference with array[i-2]
                if i > 1:
                    prev_min = max(prev_min, array[i-2] - max_diff)
                    prev_max = min(prev_max, array[i-2] + max_diff)
                
                if prev_min <= prev_max:
                    array[i-1] = np.random.randint(prev_min, prev_max + 1)
                    # Recalculate min_val and max_val
                    min_val = max(value_range[0], array[i-1] - max_diff)
                    max_val = min(value_range[1] if i in peak_indices else 80, array[i-1] + max_diff)
                else:
                    # If still invalid, retry the entire array
                    return generate_pattern_array(size, value_range, max_diff, n_peaks, min_peak_distance)
            
            # Final check before assigning
            if min_val > max_val:
                return generate_pattern_array(size, value_range, max_diff, n_peaks, min_peak_distance)
            array[i] = np.random.randint(min_val, max_val + 1)
    
    # Verify exactly 4 peaks > 80 at the chosen indices
    peaks = np.where(array > 80)[0]
    if len(peaks) != n_peaks or not np.array_equal(peaks, peak_indices):
        return generate_pattern_array(size, value_range, max_diff, n_peaks, min_peak_distance)
    
    # Verify consecutive differences
    if np.any(np.abs(np.diff(array)) > max_diff):
        return generate_pattern_array(size, value_range, max_diff, n_peaks, min_peak_distance)
    
    return array

# Generate dataset
n_random = n_samples // 2  # 2500 random arrays
n_pattern = n_samples // 2  # 2500 patterned arrays

random_arrays = [generate_random_array(array_size, value_range, max_diff) for _ in range(n_random)]
random_labels = [0] * n_random

pattern_arrays = [generate_pattern_array(array_size, value_range, max_diff, n_peaks, min_peak_distance) 
                  for _ in range(n_pattern)]
pattern_labels = [1] * n_pattern

# Combine datasets
X = np.vstack((random_arrays, pattern_arrays))
y = np.array(random_labels + pattern_labels)

# Shuffle the dataset
indices = np.random.permutation(n_samples)
X = X[indices]
y = y[indices]

# Verify constraints
def verify_array(array, max_diff, is_pattern):
    if not (np.all(array >= 1) and np.all(array <= 100)):
        return False
    if np.any(np.abs(np.diff(array)) > max_diff):
        return False
    if is_pattern:
        peaks = np.where(array > 80)[0]
        if len(peaks) != 4:
            return False
        for i in range(1, len(peaks)):
            if peaks[i] - peaks[i-1] < min_peak_distance:
                return False
    return True

# Verify all arrays
for i in range(n_samples):
    is_pattern = y[i] == 1
    if not verify_array(X[i], max_diff, is_pattern):
        print(f"Failed array {i} (label {y[i]}): {X[i]}")
        print(f"Peaks (> 80): {np.where(X[i] > 80)[0]}")
        print(f"Consecutive differences: {np.abs(np.diff(X[i]))}")
        assert False, f"Array {i} does not meet constraints"

# Save dataset to CSV
data = np.hstack((X, y.reshape(-1, 1)))
columns = [f'value_{i+1}' for i in range(array_size)] + ['label']
df = pd.DataFrame(data, columns=columns)
df.to_csv('array_dataset.csv', index=False)
print("Dataset generated and saved to 'array_dataset.csv'")

# Print sample arrays
print("\nSample Random Array (label 0):")
print(random_arrays[0])
print(f"Peaks (> 80): {np.where(random_arrays[0] > 80)[0]}")
print("\nSample Patterned Array (label 1):")
print(pattern_arrays[0])
print(f"Peaks (> 80): {np.where(pattern_arrays[0] > 80)[0]}")

# Split into train, validation, and test sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_test, y_test, test_size=0.5, random_state=42)

np.save('X_train.npy', X_train)
np.save('y_train.npy', y_train)
np.save('X_val.npy', X_val)
np.save('y_val.npy', y_val)
np.save('X_test.npy', X_test)
np.save('y_test.npy', y_test)
print("Train, validation, and test sets saved as .npy files")
