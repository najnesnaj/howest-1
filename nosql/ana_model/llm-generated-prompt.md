
let the LLM generate a prompt
------------------------------

generate a prompt that instructs a LLM to create synthetic data that must emphesize the existence of a pattern in the data : this contains a pattern [0.45 0.65 0.84 0.66 0.68 0.6  0.76 0.72 0.71 0.69 0.62 0.57 0.59 0.64
 0.64 0.84 0.67 0.68 0.51 0.38 0.43 0.44 0.62 0.6  0.75 0.67 0.8  0.68
 0.76 0.62 0.8  0.89 0.77 0.57 0.74 0.67 0.7  0.68 0.6  0.57 0.73 0.55
 0.67 0.74 0.75 0.68 0.57 0.54 0.56 0.64 0.58 0.72 0.65 0.48 0.67 0.53
 0.65 0.8  0.68 0.79 0.6  0.66 0.86 0.8  0.76 0.58 0.76 0.65 0.66 0.74] and this does not [0.77 0.84 0.88 0.86 0.78 0.97 0.87 0.69 0.52 0.43 0.45 0.28 0.12 0.02
 0.16 0.22 0.26 0.29 0.15 0.11 0.3  0.45 0.56 0.39 0.38 0.42 0.42 0.59
 0.6  0.68 0.82 0.88 0.68 0.88 0.95 0.95 0.84 0.92 0.91 0.76 0.62 0.74
 0.66 0.62 0.5  0.45 0.31 0.5  0.7  0.54 0.45 0.38 0.44 0.33 0.18 0.2
 0.24 0.3  0.14 0.09 0.07 0.26 0.13 0.1  0.25 0.43 0.55 0.43 0.63 0.73]



use the prompt
--------------



"Generate an array of 70 floating-point numbers that emphasizes a subtle, repeating pattern similar to a reference dataset, while maintaining synthetic distinctiveness. The data should range between 0.3 and 0.9, with a mean around 0.66 and a standard deviation of approximately 0.11, exhibiting a slightly right-skewed distribution. The pattern should include periodic fluctuations, such as alternating clusters of higher values (0.7–0.9) and lower values (0.3–0.6), with smooth transitions and occasional peaks, resembling a structured but non-obvious sequence. Avoid the randomness of a comparison dataset with values between 0.02 and 0.97, a mean around 0.49, and a standard deviation of about 0.27, which lacks discernible patterns and appears more uniformly scattered. Round all generated values to two decimal places."

