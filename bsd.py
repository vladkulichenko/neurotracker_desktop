import pandas as pd
import time


data = pd.read_csv("data.csv")
for i in range(len(data['time'])):
    print(f"time: {data['time'][i]} || Valence: {data['Valence'][i]}")
    time.sleep(data['time'][i+1] - data['time'][i])