
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
data = pd.read_csv('cleaned_data.csv')

# Convert 'time' column to datetime and set it as index if needed
# data['time'] = pd.to_datetime(data['time'])
# data.set_index('time', inplace=True)

# Sum all the fossil fuel generation columns
fossil_fuel_columns = [
    'generation fossil brown coal/lignite', 'generation fossil coal-derived gas',
    'generation fossil gas', 'generation fossil hard coal', 'generation fossil oil'
]
data['total_fossil_fuel_generation'] = data[fossil_fuel_columns].sum(axis=1)

# List all the non-fossil fuel generation columns
non_fossil_fuel_columns = [
    'generation biomass', 'generation geothermal', 
    'generation hydro pumped storage consumption',
    'generation hydro run-of-river and poundage', 
    'generation hydro water reservoir',
    'generation nuclear', 'generation other', 'generation other renewable',
    'generation solar', 'generation waste', 'generation wind offshore',
    'generation wind onshore'
]

# Sum all the non-fossil fuel generation columns
data['total_non_fossil_fuel_generation'] = data[non_fossil_fuel_columns].sum(axis=1)

# Filter data for different weather conditions
sunny_days = data[data['weather_description'] == 'clear sky']
rainy_days = data[data['rain_1h'] > 0]  # assuming rain_1h column exists and such threshold makes sense
windy_days = data[data['wind_speed'] > 6]  # assuming wind_speed column exists and such threshold makes sense

# Plotting energy generation in different weather conditions
plt.figure(figsize=(14, 7))

# Fossil fuel generation
sns.lineplot(data=sunny_days, x='time', y='total_fossil_fuel_generation', label='Fossil - Sunny Days')
sns.lineplot(data=rainy_days, x='time', y='total_fossil_fuel_generation', label='Fossil - Rainy Days')
sns.lineplot(data=windy_days, x='time', y='total_fossil_fuel_generation', label='Fossil - Windy Days')

# Non-fossil fuel generation
sns.lineplot(data=sunny_days, x='time', y='total_non_fossil_fuel_generation', label='Non-Fossil - Sunny Days')
sns.lineplot(data=rainy_days, x='time', y='total_non_fossil_fuel_generation', label='Non-Fossil - Rainy Days')
sns.lineplot(data=windy_days, x='time', y='total_non_fossil_fuel_generation', label='Non-Fossil - Windy Days')

plt.title('Energy Generation in Different Weather Conditions')
plt.xlabel('Time')
plt.ylabel('Energy Generation (MWh)')
plt.legend()
plt.show()

# To get specific numbers, we can calculate the means for each condition
print('Average fossil fuel generation on sunny days:', sunny_days['total_fossil_fuel_generation'].mean())
print('Average fossil fuel generation on rainy days:', rainy_days['total_fossil_fuel_generation'].mean())
print('Average fossil fuel generation on windy days:', windy_days['total_fossil_fuel_generation'].mean())

print('Average non-fossil fuel generation on sunny days:', sunny_days['total_non_fossil_fuel_generation'].mean())
print('Average non-fossil fuel generation on rainy days:', rainy_days['total_non_fossil_fuel_generation'].mean())
print('Average non-fossil fuel generation on windy days:', windy_days['total_non_fossil_fuel_generation'].mean())
