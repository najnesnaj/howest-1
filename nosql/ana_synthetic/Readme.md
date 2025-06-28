Synthetic
---------


- we have a certain pattern we are interested in (eg 70 quarters of stock data (market_cap) of Deutz)


===> now we want to build a model that recognises the pattern


===> let the LLM generate a prompt (we feed it the normalised data from Deutz)
------------------------------------------------------------------------------

generate a prompt that instructs a LLM to create synthetic data that must emphesize the existence of a pattern in the data : this contains a pattern [0.45 0.65 0.84 0.66 0.68 0.6  0.76 0.72 0.71 0.69 0.62 0.57 0.59 0.64
 0.64 0.84 0.67 0.68 0.51 0.38 0.43 0.44 0.62 0.6  0.75 0.67 0.8  0.68
 0.76 0.62 0.8  0.89 0.77 0.57 0.74 0.67 0.7  0.68 0.6  0.57 0.73 0.55
 0.67 0.74 0.75 0.68 0.57 0.54 0.56 0.64 0.58 0.72 0.65 0.48 0.67 0.53
 0.65 0.8  0.68 0.79 0.6  0.66 0.86 0.8  0.76 0.58 0.76 0.65 0.66 0.74] and this does not [0.77 0.84 0.88 0.86 0.78 0.97 0.87 0.69 0.52 0.43 0.45 0.28 0.12 0.02
 0.16 0.22 0.26 0.29 0.15 0.11 0.3  0.45 0.56 0.39 0.38 0.42 0.42 0.59
 0.6  0.68 0.82 0.88 0.68 0.88 0.95 0.95 0.84 0.92 0.91 0.76 0.62 0.74
 0.66 0.62 0.5  0.45 0.31 0.5  0.7  0.54 0.45 0.38 0.44 0.33 0.18 0.2
 0.24 0.3  0.14 0.09 0.07 0.26 0.13 0.1  0.25 0.43 0.55 0.43 0.63 0.73]



FOR DEZ:DE market_cap
generate a pythonscript that mimics this data : 


[0.734500750153661,0.012759170653907496,0.0,0.16108452950558214,0.18819776714513556,0.17384370015948963,0.3237639553429027,0.2886762360446571,0.49282296650717705,0.6299840510366826,0.5821371610845295,0.7192982456140351,0.29984051036682613,0.2886762360446571,0.430622009569378,0.2727272727272727,0.19138755980861244,0.19776714513556617,0.28708133971291866,0.37320574162679426,0.6985557783658096,0.6682615629984051,0.6092503987240829,0.5614035087719298,0.30303030303030304,0.2711323763955343,0.2583732057416268,0.4529505582137161,0.11164274322169059,0.22169059011164274,0.2966507177033493,0.22328548644338117,0.3492822966507177,0.4864433811802233,0.6650717703349283,0.810207336523126,0.7240829346092504,0.8421052631578947,0.8213716108452951,0.6889952153110048,0.8564593301435407,0.45454545454545453,0.8229665071770335,1.0,0.48165869218500795,0.5215311004784688,0.16905901116427433,0.3004784688995215,0.4251993620414673,0.44657097288676234,0.6491228070175439,0.7200956937799043,0.8405103668261563,0.6810207336523126,0.4076555023923445,0.23700159489633174,0.11483253588516747,0.2784688995215311,0.5861244019138756,0.4920255183413078,0.3289922150658493,0.43219972469425305,0.6128128665439596,0.6369501066989895,0.45680484394964327]


def generate_synthetic_data(length=65, period=8, noise_level=0.15):
    """
    Generate synthetic data mimicking the provided dataset with a quasi-periodic pattern.
    
    Args:
        length (int): Number of data points (default: 65).
        period (float): Period of the sinusoidal component (default: 8).
        noise_level (float): Magnitude of random noise (default: 0.15).
    
    Returns:
        list: Normalized synthetic data with 65 values in [0, 1].
    """
    # Generate base sinusoidal pattern
    t = np.arange(length)
    # Combine two sinusoids with different periods for varied oscillations
    base_pattern = 0.5 * np.sin(2 * np.pi * t / period) + 0.3 * np.sin(2 * np.pi * t / (period * 2))
    
    # Add controlled noise
    noise = np.random.normal(0, noise_level, length)
    synthetic_data = base_pattern + noise
    
    # Normalize to [0, 1]
    synthetic_data = (synthetic_data - np.min(synthetic_data)) / (np.max(synthetic_data) - np.min(synthetic_data))
    
    # Round to 6 decimal places
    synthetic_data = np.round(synthetic_data, 6).tolist()
    
    return synthetic_data



====> result "Generate an array of 70 floating-point numbers that emphasizes a subtle, repeating pattern similar to a reference dataset, while maintaining synthetic distinctiveness. The data should range between 0.3 and 0.9, with a mean around 0.66 and a standard deviation of approximately 0.11, exhibiting a slightly right-skewed distribution. The pattern should include periodic fluctuations, such as alternating clusters of higher values (0.7–0.9) and lower values (0.3–0.6), with smooth transitions and occasional peaks, resembling a structured but non-obvious sequence. Avoid the randomness of a comparison dataset with values between 0.02 and 0.97, a mean around 0.49, and a standard deviation of about 0.27, which lacks discernible patterns and appears more uniformly scattered. Round all generated values to two decimal places."


====> now we feed this back into the LLM and ask it to come up with a python script


====>test with real data:
DEZ:DE,65,"[0.8058, 0.2777, 0.2684, 0.3862, 0.4061, 0.3956, 0.5053, 0.4796, 0.6289, 0.7293, 0.6943, 0.7946, 0.4877, 0.4796, 0.5834, 0.4679, 0.4084, 0.4131, 0.4784, 0.5414, 0.7795, 0.75
73, 0.7141, 0.6791, 0.4901, 0.4667, 0.4574, 0.5998, 0.3501, 0.4306, 0.4854, 0.4317, 0.5239, 0.6243, 0.755, 0.8611, 0.7981, 0.8845, 0.8693, 0.7725, 0.895, 0.6009, 0.8705, 1.0, 0.6208, 0
.6499, 0.3921, 0.4882, 0.5795, 0.5951, 0.7433, 0.7952, 0.8833, 0.7666, 0.5666, 0.4418, 0.3524, 0.4721, 0.6972, 0.6284, 0.5091, 0.5846, 0.7167, 0.7344, 0.6026, 0.0, 0.0, 0.0, 0.0, 0.0]"
,Pattern,0.7328902
BWB:DE,34,"[0.3204, 0.2644, 0.5061, 0.2244, 0.3442, 0.3728, 0.3304, 0.3144, 0.2149, 0.197, 0.2113, 0.205, 0.2605, 0.3006, 0.2653, 0.271, 0.3079, 0.2198, 0.2016, 0.2036, 0.1996, 0.2144,
 0.1317, 0.1221, 0.1211, 0.188, 0.4778, 1.0, 0.6998, 0.5394, 0.4792, 0.4482, 0.3826, 0.4905, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0
.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]",No Pattern,9.281479e-07

====>test with LLM generated data

LLM1,70,"[0.8222, 0.8, 0.8667, 0.7, 1.0, 0.6889, 1.0, 0.8222, 0.8889, 1.0, 1.0, 0.6778, 0.9444, 0.9111, 0.6444, 0.9111, 0.6111, 0.7444, 0.6667, 0.6667, 0.5889, 0.7778, 0.4222, 0.6667, 0.5111, 0.5667, 0.6333, 0.4667, 0.5667, 0.6111, 0.4889, 0.5778, 0.7222, 0.4111, 0.4667, 0.7, 0.8111, 1.0, 0.8111, 0.6222, 0.5889, 0.8556, 1.0, 0.6444, 0.8333, 0.9222, 0.7667, 1.0, 0.9556, 0.5889, 0.8444, 0.8778, 0.6889, 0.5222, 0.8556, 0.4333, 0.5, 0.6778, 0.7667, 0.7778, 0.4333, 0.7556, 0.5667, 0.5889, 0.5444, 0.8, 0.3778, 0.4667, 0.9, 0.8222]",Pattern,0.90355134
generated-by-script-by-LLM,70,"[0.7386, 0.8523, 0.7841, 0.9773, 0.8864, 0.8295, 0.8295, 0.9205, 0.8864, 0.9432, 0.9205, 0.8864, 0.8295, 0.7727, 0.8068, 0.8523, 0.7955, 0.6818, 0.7273, 0.7159, 0.6136, 0.6477, 0.625, 0.5455, 0.6136, 0.6136, 0.6364, 0.6364, 0.5227, 0.5568, 0.6477, 0.6705, 0.7045, 0.9091, 0.7614, 0.8182, 0.8409, 0.8523, 0.8182, 0.8977, 0.8409, 0.875, 0.875, 0.9091, 1.0, 0.7955, 0.9205, 0.7841, 0.8182, 0.875, 0.7955, 0.7045, 0.6932, 0.7386, 0.6364, 0.6591, 0.6364, 0.5795, 0.7159, 0.625, 0.4773, 0.5909, 0.5568, 0.6477, 0.5682, 0.625, 0.8977, 0.7273, 0.6477, 0.7273]",Pattern,0.9126168


------------------------------------------------

this docker container allows for displaying the synthetic data generated by the function under the directory functions (this allows for changing / trying out different function without rebuilding the container) 
building the application : 
docker build -t ana_synthetic .
docker run -p 8003:8000 -v ./functions:/app/functions ana_synthetic

==> copy new function to ./functions
