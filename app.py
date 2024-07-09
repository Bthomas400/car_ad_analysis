import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv('vehicles_us.csv')

# Remove outliers for model_year and price
df = df[(df['model_year'] >= df['model_year'].quantile(0.05)) & (df['model_year'] <= df['model_year'].quantile(0.95))]
df = df[(df['price'] >= df['price'].quantile(0.05)) & (df['price'] <= df['price'].quantile(0.95))]

# Fill missing values based on group medians
df['model_year'] = df.groupby('model')['model_year'].transform(lambda x: x.fillna(x.median()))
df['cylinders'] = df.groupby('model')['cylinders'].transform(lambda x: x.fillna(x.median()))
df['odometer'] = df.groupby(['model_year', 'model'])['odometer'].transform(lambda x: x.fillna(x.mean()))

df['paint_color'] = df['paint_color'].fillna('Unknown')

# Fill any remaining NaN values with 0
df['odometer'] = df['odometer'].fillna(0)



# Convert model_year to datetime format
df['model_year'] = pd.to_datetime(df['model_year'], format='%Y').dt.year
df['model_year'] = df['model_year'].astype(str)

#Changing data type 
df['cylinders'] = df['cylinders'].astype('int64')



#fill `is_4wd` with 'yes' and 'no'
df['is_4wd']=df['is_4wd'].fillna('no')
df['is_4wd'] = df['is_4wd'].replace(1, 'yes')



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


