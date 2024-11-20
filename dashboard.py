import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(layout="wide")

def create_monthly_avg_pollutant(df, year):
    df['year_month'] = pd.to_datetime(df['year_month'])
    monthly_avg_pollutant = df.groupby('year_month')[['SO2', 'NO2', 'O3']].mean().reset_index()
    
    
    monthly_avg_pollutant = monthly_avg_pollutant[monthly_avg_pollutant['year_month'].dt.year==year]
    return monthly_avg_pollutant

def create_monthly_avg_pm25(df):
    df['year_month'] = pd.to_datetime(df['year_month'])
    pm25_by_station_year = df.groupby(by=['station', 'year_month']).agg(avg_pm25=('PM2.5', 'mean')).reset_index()
    
    pm25_by_station_year = pm25_by_station_year[pm25_by_station_year['year_month'].dt.year > 2013]
    pm25_by_station_year = pm25_by_station_year[pm25_by_station_year['year_month'].dt.year < 2017]
    return pm25_by_station_year

def getHighestandLowest(df, range):
    df = df[df['year_month'].dt.year >= range[0]]
    df = df[df['year_month'].dt.year <= range[1]]
    sorted_df = df.groupby(by="station").agg({
        'PM2.5':['mean'],
    }).sort_values(by=("PM2.5","mean"), ascending=False).reset_index()
    return sorted_df["station"].iloc[0], sorted_df["station"].iloc[-1]

all_df = pd.read_csv("all_data.csv")
aoti_df = all_df[all_df["station"]=="Aotizhongxin"]
changping_df = all_df[all_df["station"]=="Changping"]
dingling_df = all_df[all_df["station"]=="Dingling"]
dongsi_df = all_df[all_df["station"]=="Dongsi"]
guanyuan_df = all_df[all_df["station"]=="Guanyuan"]
gucheng_df = all_df[all_df["station"]=="Gucheng"]
huairou_df = all_df[all_df["station"]=="Huairou"]
nongzhan_df = all_df[all_df["station"]=="Nongzhanguan"]
shunyi_df = all_df[all_df["station"]=="Shunyi"]
tiantan_df = all_df[all_df["station"]=="Tiantan"]
wanliu_df = all_df[all_df["station"]=="Wanliu"]
wanshou_df = all_df[all_df["station"]=="Wanshou"]

st.header('Air Quality Analysis :sparkles:')

st.subheader('')



st.subheader("Average SO2, NO2 and O3 Statistics")
col1, col2 = st.columns(2)




with col1:
    station = st.selectbox(
        label="Select station for monthly analysis",
        options=('Aotizhongxin', 'Changping', 'Dingling', 'Guanyuan', 'Gucheng', 'Huairou', 'Nongzhanguan', 'Shunyi', 'Tiantan', 'Wanliu', 'Wanshou')
    )
    match station:
        case "Aotizhongxin":
            selected_df = aoti_df
        case "Changping":
            selected_df = changping_df
        case "Dingling":
            selected_df = dingling_df
        case "Guanyuan":
            selected_df = guanyuan_df
        case "Gucheng":
            selected_df = gucheng_df
        case "Huairou":
            selected_df = huairou_df
        case "Nongzhanguan":
            selected_df = nongzhan_df
        case "Shunyi":
            selected_df = shunyi_df
        case "Tiantan":
            selected_df = tiantan_df
        case "Wanliu":
            selected_df = wanliu_df
        case "Wanshouxigong":
            selected_df = wanshou_df

    year = st.radio(
        label="Select year",
        options=(2014, 2015, 2016),
        horizontal=False
    )

    monthly_avg_pollutant = create_monthly_avg_pollutant(selected_df, year)

with col2:
    fig, ax = plt.subplots(figsize=(10,6))

    ax.plot(monthly_avg_pollutant["year_month"], monthly_avg_pollutant["SO2"], label="SO2", marker='o')
    ax.plot(monthly_avg_pollutant["year_month"], monthly_avg_pollutant["NO2"], label="NO2", marker='o')
    ax.plot(monthly_avg_pollutant["year_month"], monthly_avg_pollutant["O3"], label="O3", marker='o')
    plt.title(f"Average SO2, NO2, and O3 per Month ({year}) in {station}")
    plt.grid(True)

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    
    st.pyplot(fig)

st.subheader("Statistics of Average PM2.5")
col1, col2 = st.columns(2)
with col1:
    values = st.slider(
        label='Select a range of year',
        min_value=2014, max_value=2016, value=(2014, 2016))
    
    pm25_by_station_year = create_monthly_avg_pm25(all_df)
    pm25_by_station_year = pm25_by_station_year[pm25_by_station_year['year_month'].dt.year>=values[0]]
    pm25_by_station_year = pm25_by_station_year[pm25_by_station_year['year_month'].dt.year<=values[1]]
    df_station = pm25_by_station_year.groupby(by=['station'])

    highest, lowest = getHighestandLowest(all_df, values)

    
    st.metric("Highes PM2.5 Average", value=highest)
    st.metric("Lowest PM2.5 Average", value=lowest)

with col2:
    fig, ax = plt.subplots(figsize=(11,8))


    custom_colors = {highest: 'red', lowest: 'blue'} 

    for key, group in df_station:
        if key[0] in custom_colors:
            color = custom_colors[key[0]]
            opacity = 1
        else:
            color = 'gray'
            opacity = 0.4
        ax.plot(group['year_month'], group['avg_pm25'], label=key, color=color, alpha=opacity, marker="o")

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid()
    plt.xticks(rotation=45)
    plt.title(f"Average PM2.5 per Month ({values[0]}-{values[1]}) in Every District" if values[0]<values[1] else f"Average PM2.5 per Month ({values[0]}) in Every District")
    st.pyplot(fig)


