from pycaret.datasets import get_data
import yfinance as yf
import pandas as pd
ticker = "DEZ.DE"
stock_data = yf.download(ticker, start="2000-01-01", end="2025-07-22", progress=False)

# Prepare the data (use closing price as the target variable)
#data = stock_data[['Close']].reset_index()
data = stock_data[['Close']].copy()
#data['Date'] = pd.to_datetime(data['Date'])
#data.set_index('Date', inplace=True)
#B is business days
data = data.asfreq('B', method='ffill') 
#data.index = data.index.to_period(freq='B')


#data.plot()
print (data.head())
print (data.tail())
from pycaret.time_series import *

#exp_name = setup(data = data,  fh = 12, session_id=123, numeric_imputation="ffill")
exp_name = setup(data = data,  fh = 12, session_id=123)


exp_name.check_stats()
plot_model(plot = "decomp_classical")
best = compare_models()
#fh = forecast horizon
plot_model(best, plot = 'forecast', data_kwargs = {'fh': 24})
plot_model(best, plot = 'residuals')
plot_model(best, plot = 'insample')
# finalize model
final_best = finalize_model(best)

# save model
save_model (final_best, 'final_best_model_DEZ')

