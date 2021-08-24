import os
import shutil
import requests
import pandas as pd
import numpy as np
import glob

'''
# Function to download file from url
def download_file(url, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    local_filename = url.split('/')[-1].replace(" ", "_")
    path = os.path.join(dest_folder, local_filename)
    r = requests.get(url, stream = True)
    if r.ok:
        with open(path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    else:
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))
        print(url)

stations = ['S24','S60','S07','S77','S55','S40','S66','S33','S23','S78','S24'] # Station ids for chosen stations from weather.gov


# Download csv file from 1980 to 2020 for specified stations
dest_folder = 'weather_data'
for s in stations:
    for i in range(1980,2021):
        for j in range(1,13):
            if len(str(j)) == 1:
                j = str(0) + str(j)
            url = 'http://www.weather.gov.sg/files/dailydata/DAILYDATA_'+str(s)+'_'+str(i)+str(j)+'.csv'
            download_file(url, dest_folder)
'''

##################################################################################

# Data processing

# Combine all csv
os.chdir(r'weather_data')
all_filenames = [i for i in glob.glob('*.{}'.format('csv'))]

file = pd.read_csv(all_filenames[0], encoding = None)
file.columns = ['station','year','month','day','daily_total_rainfall','highest_30min_rainfall','highest_60min_rainfall','highest_120min_rainfall','mean_temp','max_temp','min_temp','mean_wind','max_wind']
weird_text = file.iloc[0]['max_wind']

combined_csv = pd.DataFrame()
for f in all_filenames:
    file = pd.read_csv(f, encoding = None)
    file.columns = ['station','year','month','day','daily_total_rainfall','highest_30min_rainfall','highest_60min_rainfall','highest_120min_rainfall','mean_temp','max_temp','min_temp','mean_wind','max_wind']
    file = file.replace(weird_text, np.nan)
    file = file.replace('-', np.nan)
    combined_csv = pd.concat([combined_csv, file])
combined_csv.to_csv('combined_csv', index = False, encoding = 'utf-8-sig')

# Set index to datetimeindex
combined_csv = combined_csv.loc[~combined_csv.year.isnull()]
combined_csv['date'] = pd.to_datetime(combined_csv['year'].astype(int).astype(str) + '-' + combined_csv['month'].astype(int).astype(str) + '-' + combined_csv['day'].astype(int).astype(str))
#combined_csv = combined_csv.set_index('date')

# Find missing dates per region and concat empty dataframes
for s in combined_csv.station.unique():
    temp = pd.date_range(start = '1980-01-01', end = '2020-12-31').difference(combined_csv.loc[combined_csv.station == str(s)]['date'])
    if len(temp)>1:
        temp_df = pd.DataFrame(data = {'date':temp, 'station':str(s),'year':temp.year,'month':temp.month,'day':temp.day,'daily_total_rainfall':np.nan})
        combined_csv = pd.concat([combined_csv, temp_df])
    else:
        continue

# Impute missing data based on average rainfall on the particular day of the year throughout dataset
combined_csv['daily_total_rainfall'] = combined_csv['daily_total_rainfall'].astype('float64')
combined_csv['impute'] = combined_csv['daily_total_rainfall']
combined_csv = combined_csv.set_index('date')
combined_csv = combined_csv.reset_index()
combined_null = combined_csv.loc[(combined_csv['daily_total_rainfall'].isnull())]

def impute(df, r):
    r['impute'] = df.loc[(df.station == r.station)&(df.month == r.month)&(df.day == r.day)]['daily_total_rainfall'].mean()
    return r

combined_null = combined_null.apply(lambda x: impute(combined_csv, x), axis = 1)
combined_csv['impute'] = combined_csv['impute'].fillna(combined_null['impute'])
combined_csv = combined_csv.set_index('date')

# Insert geographical coordinates
coordinates = [['Changi', 1.3678, 103.9826],['Sentosa Island', 1.2500, 103.8279], ['Macritchie Reservoir',1.3417, 103.8338],
               ['Queenstown', 1.2937, 103.8125],['Buangkok',1.3837,103.8860],['Mandai',1.4036,103.7898],['Kranji Reservoir', 1.4387, 103.7363],
               ['Jurong Pier',1.3081,103.7100],['Tengah',1.3858,103.7114],['Tanjong Katong',1.3070,103.8907],['Seletar',1.4166,103.8654]]
combined_csv['latitude'] = np.nan
combined_csv['longitude'] = np.nan
for c in coordinates:
    combined_csv.loc[combined_csv.station == c[0], 'latitude'] = c[1]
    combined_csv.loc[combined_csv.station == c[0], 'longitude'] = c[2]

df_out = combined_csv[['station','impute','latitude','longitude']]
df_out.to_csv('cleaned_combined.csv')



