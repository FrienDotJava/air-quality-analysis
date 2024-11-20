import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def create_monthly_avg_pollutant(df, year):
    monthly_avg_pollutant = df.groupby('year_month')[['SO2', 'NO2', 'O3']].mean().reset_index()
    monthly_avg_pollutant['year_month'] = monthly_avg_pollutant['year_month'].dt.to_timestamp()
    
    monthly_avg_pollutant = monthly_avg_pollutant[monthly_avg_pollutant['year_month'].dt.year==year]
    return monthly_avg_pollutant

def create_monthly_avg_pm25(df):
    pm25_by_station_year = df.groupby(by=['station', 'year_month']).agg(avg_pm25=('PM2.5', 'mean')).reset_index()
    
    pm25_by_station_year['year_month'] = pm25_by_station_year['year_month'].dt.to_timestamp()
    pm25_by_station_year = pm25_by_station_year[pm25_by_station_year['year_month'].dt.year > 2013]
    pm25_by_station_year = pm25_by_station_year[pm25_by_station_year['year_month'].dt.year < 2017]
    return pm25_by_station_year

all_df = pd.read_csv("all_data.csv")
aoti_df = pd.read_csv('Air-quality-dataset/PRSA_Data_Aotizhongxin_20130301-20170228.csv')
changping_df = pd.read_csv('Air-quality-dataset/PRSA_Data_Changping_20130301-20170228.csv')
dingling_df = pd.read_csv('Air-quality-dataset/PRSA_Data_Dingling_20130301-20170228.csv')
dongsi_df = pd.read_csv('Air-quality-dataset/PRSA_Data_Dongsi_20130301-20170228.csv')
guanyuan_df = pd.read_csv('Air-quality-dataset/PRSA_Data_Guanyuan_20130301-20170228.csv')
gucheng_df = pd.read_csv('Air-quality-dataset/PRSA_Data_Gucheng_20130301-20170228.csv')
huairou_df = pd.read_csv('Air-quality-dataset/PRSA_Data_Huairou_20130301-20170228.csv')
nongzhan_df = pd.read_csv('Air-quality-dataset/PRSA_Data_Nongzhanguan_20130301-20170228.csv')
shunyi_df = pd.read_csv('Air-quality-dataset/PRSA_Data_Shunyi_20130301-20170228.csv')
tiantan_df = pd.read_csv('Air-quality-dataset/PRSA_Data_Tiantan_20130301-20170228.csv')
wanliu_df = pd.read_csv('Air-quality-dataset/PRSA_Data_Wanliu_20130301-20170228.csv')
wanshou_df = pd.read_csv('Air-quality-dataset/PRSA_Data_Wanshouxigong_20130301-20170228.csv')

st.header('Air Quality Analysis :clouds:')