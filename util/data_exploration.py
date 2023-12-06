import pandas as pd
import matplotlib.pyplot as plt

def check_all_zero(df):
    all_zero_column=[]
    for column in df:
        all_zeros_or_null = (df[column] == 0) | pd.isnull(df[column])
        if all_zeros_or_null.all()==True:
            all_zero_column.append(column)
    return all_zero_column

def drop_column(df, columns):
    return df.drop(columns, axis=1)

# focus on total load actual 
# we are looking at predicting power usage, only look at total load actually
def pre_process_totalload(df):
    df["time"] = pd.to_datetime(df["time"] ,utc=True)

    df.set_index('time', inplace=True)
    total_load_df = df[["total load actual"]]

    total_load_df["month"]= total_load_df.index.month
    total_load_df["weekday"]= total_load_df.index.weekday
    total_load_df["hour"]= total_load_df.index.hour

    return total_load_df

def plot_bars(data, figsize=None, tick_gap=1, series=None):
    plt.figure(figsize=figsize)
    x = data.index
    plt.bar(x, data, width=0.7)
    if series is not None:
        plt.plot(series.index, series, color='tab:orange')
    if tick_gap > 0:
        plt.xticks(x[::tick_gap], data.index[::tick_gap], rotation=45)
    plt.grid(linestyle=':')
    plt.tight_layout()




