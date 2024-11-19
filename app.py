
#this function get real time cryptocurrency price every day at 8PM
#this also save the data as csv

import requests
import pandas as pd
from datetime import datetime

url = "https://api.coingecko.com/api/v3/coins/markets"


params = {
    'vs_currency' : 'usd',
    'order' : 'market_cap_desc',
    'per_page' : 250,
    'page' : 1
}
response = requests.get(url, params = params)

if response.status_code == 200:
    print("Connection Successful!\n Getting Data...")
    data = response.json()
    
    # print(data) 
    
    if isinstance(data, list):
        df = pd.DataFrame(data)
    elif isinstance(data, dict):
        df = pd.DataFrame([data])  # Wrap in a list if it's a single dictionary
    else:
        raise ValueError("Unexpected data format")

    df = df[[
        'id', 'current_price', 'market_cap', 'price_change_percentage_24h', 'ath', 'atl'
    ]]
    
    #creating new column
    today = datetime.now().strftime('%d-%m-%Y %H-%M-%S')
    df['Time_stamp'] = today
    
    #getting top 10 by value change
    top_negative = df.sort_values(by='price_change_percentage_24h', ascending=True)
    top_negative_10 = top_negative.head(10)
    top_negative_10.to_csv(f'Top_neg_10 {today} .csv', index=False)
    
    #positive top 10
    top_positive = df.sort_values(by='price_change_percentage_24h', ascending=False)
    top_positive_10 = top_positive.head(10)
    top_positive_10.to_csv(f'Top_pos_10 {today} .csv', index=False)
    
    
    
    #saving data as csv
    # df.to_csv(f'cryptocurrency_price {today}.csv', index=False)
    print(f"Top 10 crypto with highest change in ratio {today}:\n{top_positive_10}")
    print("Data saved successfully")
    
    
    
else:
    print(f"Error code {response.status_code}")
    