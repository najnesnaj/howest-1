Synthetic
---------


- we have a certain pattern we are interested in (eg 65 quarters of stock data (market_cap) of Deutz)


===> now we want to build a model that recognises the pattern
===> we create synthetic data based on the data of Deutz


functions:
   random_data.py
(this function takes the normalised data from deutz, add and substract a randomised parametervalue of .15 to the data, and it shifts the data over random quarters)

====> verify behaviour  

plot_synthetic.py
this plots the synthic data, so you can check the result visually

====> it the synthetic data is OK, we can create a model with it
train_pattern_model.py
-> model.keras


=====> finally we can test the model with the synthetic data and totally random data
-> the synthetic data should be detected as true
test_pattern_data.py


