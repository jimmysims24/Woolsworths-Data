import pandas as pd
from plotnine import *

# Load and preprocess the data
data = pd.read_csv('WoolworthsDemand2024.csv')

date_columns = pd.to_datetime(data.columns[1:], format='%Y-%m-%d')
formatted_dates = date_columns.strftime('%Y-%m-%d')
data.columns = [data.columns[0]] + formatted_dates.tolist()
date_columns = data.columns[1:]
data = pd.melt(data, id_vars=['Store'], value_vars=date_columns, var_name='Date', value_name='Demand')
data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')

# Filter out weekends
data = data[data['Date'].dt.dayofweek < 5]  # Monday=0, Sunday=6

# Calculate average and median demands
daily_avg_demand = data.groupby('Date')['Demand'].mean().reset_index()
daily_median_demand = data.groupby('Date')['Demand'].median().reset_index()
store_avg_demand = data.groupby('Store')['Demand'].mean().reset_index()
store_median_demand = data.groupby('Store')['Demand'].median().reset_index()

# Plot average demand per day (weekdays only)
time_series_avg_plot = (ggplot(daily_avg_demand, aes(x='Date', y='Demand'))
        + geom_line()
        + labs(title='Average Weekday Demand per Day (Across all Stores)', x='Date', y='Average Demand (Pallets)')
        + theme(axis_text_x=element_text(rotation=45, hjust=1, size=8)))

# Plot median demand per day (weekdays only)
time_series_median_plot = (ggplot(daily_median_demand, aes(x='Date', y='Demand'))
        + geom_line(color='red')
        + labs(title='Median Weekday Demand per Day (Across all Stores)', x='Date', y='Median Demand (Pallets)')
        + theme(axis_text_x=element_text(rotation=45, hjust=1, size=8)))

# Plot average daily demand per store
histogram_avg_plot = (ggplot(store_avg_demand, aes(x='Store', y='Demand', fill='Store'))
        + geom_bar(stat='identity')
        + guides(fill=False)
        + labs(title='Average Daily Weekday Demand per Store in the Month', x='Store', y='Average Demand (Pallets)')
        + theme(axis_text_x=element_text(rotation=90, hjust=1, size=6)))

# Plot median daily demand per store
histogram_median_plot = (ggplot(store_median_demand, aes(x='Store', y='Demand', fill='Store'))
        + geom_bar(stat='identity')
        + guides(fill=False)
        + labs(title='Median Daily Weekday Demand per Store in the Month', x='Store', y='Median Demand (Pallets)')
        + theme(axis_text_x=element_text(rotation=90, hjust=1, size=6)))

# Draw and show plots
time_series_avg_plot.draw()
time_series_median_plot.draw()
histogram_avg_plot.draw()
histogram_median_plot.draw()

time_series_avg_plot.show()
time_series_median_plot.show()
histogram_avg_plot.show()
histogram_median_plot.show()
