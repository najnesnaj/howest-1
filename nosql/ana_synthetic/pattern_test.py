import numpy as np
from tensorflow import keras
import sys

def load_and_predict(input_array, model_path='pattern_classifier.keras', threshold=0.5):
    """
    Load the Keras model and predict if the input array has a pattern.
    
    Args:
        input_array (list or np.array): Array of 70 values in [0, 1].
        model_path (str): Path to the trained Keras model (default: 'pattern_classifier.keras').
        threshold (float): Probability threshold for classification (default: 0.5).
    
    Returns:
        None: Prints whether the array has a pattern and the prediction probability.
    """
    # Validate input
    input_array = np.array(input_array, dtype=float)
    if len(input_array) != 70:
        print("Error: Input array must contain exactly 70 values.")
        return
    if not (np.all(input_array >= 0) and np.all(input_array <= 1)):
        print("Error: All values must be between 0 and 1.")
        return
    
    # Load the model
    try:
        model = keras.models.load_model(model_path)
    except Exception as e:
        print(f"Error: Could not load model from {model_path}. {str(e)}")
        return
    
    # Reshape input for the model (1, 70)
    input_array = input_array.reshape(1, 70)
    
    # Make prediction
    try:
        prediction = model.predict(input_array, verbose=0)[0][0]
        label = "has pattern" if prediction >= threshold else "no pattern"
        print(f"Prediction: The input array {label}.")
        print(f"Probability of having a pattern: {prediction:.6f}")
    except Exception as e:
        print(f"Error during prediction: {str(e)}")

def main():
    # Example input array (replace with your own or pass via command line)
    example_array = [0.734500750153661,0.012759170653907496,0.0,0.16108452950558214,0.18819776714513556,0.17384370015948963,0.3237639553429027,0.2886762360446571,0.49282296650717705,0.6299840510366826,0.5821371610845295,0.7192982456140351,0.29984051036682613,0.2886762360446571,0.430622009569378,0.2727272727272727,0.19138755980861244,0.19776714513556617,0.28708133971291866,0.37320574162679426,0.6985557783658096,0.6682615629984051,0.6092503987240829,0.5614035087719298,0.30303030303030304,0.2711323763955343,0.2583732057416268,0.4529505582137161,0.11164274322169059,0.22169059011164274,0.2966507177033493,0.22328548644338117,0.3492822966507177,0.4864433811802233,0.6650717703349283,0.810207336523126,0.7240829346092504,0.8421052631578947,0.8213716108452951,0.6889952153110048,0.8564593301435407,0.45454545454545453,0.8229665071770335,1.0,0.48165869218500795,0.5215311004784688,0.16905901116427433,0.3004784688995215,0.4251993620414673,0.44657097288676234,0.6491228070175439,0.7200956937799043,0.8405103668261563,0.6810207336523126,0.4076555023923445,0.23700159489633174,0.11483253588516747,0.2784688995215311,0.5861244019138756,0.4920255183413078,0.3289922150658493,0.43219972469425305,0.6128128665439596,0.6369501066989895,0.4568048439496432] 
    # Truncate or pad the example array to exactly 70 values
    example_array = example_array[:70] if len(example_array) > 70 else example_array + [0] * (70 - len(example_array))
    
    # Run prediction
    print("Running prediction on input array...")
    load_and_predict(example_array)

if __name__ == "__main__":
    # Optionally, accept input array from command line as a comma-separated string
    if len(sys.argv) > 1:
        try:
            input_array = [float(x) for x in sys.argv[1].split(',')]
            load_and_predict(input_array)
        except ValueError:
            print("Error: Command-line input must be a comma-separated list of 70 numbers.")
    else:
        main()
