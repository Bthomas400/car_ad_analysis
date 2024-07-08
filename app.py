import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv('vehicles_us.csv')

#create new manufacturer column
df['manufacturer']=df['model'].apply(lambda x: x.split()[0])

#text header above the dataframe
st.header('Data Viewer')

#display the data frame
st.dataframe(df)

# Header
st.header('Car Advertisement Analysis')

# Histogram
if st.checkbox('Show Histogram of Car Prices'):
    fig = px.histogram(df, x='price', nbins=150, title='Histogram of Car Prices')
    st.plotly_chart(fig)

# Scatter Plot
if st.checkbox('Show Scatter Plot of Mileage vs Price'):
    fig = px.scatter(df, x='odometer', y='price', title='Scatter Plot of Mileage vs Price')
    st.plotly_chart(fig)

#Condition by Manufactuer 

if st.checkbox('Show Barchart of Condition by Manufactuer'):
    condition_count = df.groupby(['manufacturer', 'condition']).size().reset_index(name='counts')
    fig = px.bar(condition_count, x='manufacturer', y='counts', color='condition', title='Condition by Manufacturer')

    st.plotly_chart(fig)

#Average Price by Model Year

if st.checkbox('Show Barchart of Average Price by Model Year'):
    avg_price_year = df.groupby('model_year')['price'].mean().reset_index()
    fig = px.bar(avg_price_year, x='model_year', y='price', title='Average Price by Model Year')

    st.plotly_chart(fig)


