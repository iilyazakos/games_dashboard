import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st


_game = pd.read_csv("https://github.com/iilyazakos/games_dashboard/blob/main/game_sales.csv?raw=true")
games = _game[['Rank', 'Name', 'Platform', 'Year',
                  'Genre', 'Publisher', 'NA_Sales', 'EU_Sales',
                  'JP_Sales','Other_Sales','Global_Sales']].replace([np.nan, np.inf], 0)


st.set_page_config(layout = "wide")
data_different_sales = games[['Genre', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']]
data_different_sales = (data_different_sales.groupby(['Genre'])['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales'].sum()).reset_index()
data_different_sales.columns = ['Genre', 'Sales in north america in millions', 'Sales in europe in millions', 'Sales in Japan in millions', 'Other sales in millions', 'All sales worldwide in millions']

type_of_sales = st.radio('Select sales region',
                    ('Sales in north america in millions', 'Sales in europe in millions', 'Sales in Japan in millions', 'Other sales in millions', 'All sales worldwide in millions'))


if type_of_sales == 'Sales in north america in millions': st.plotly_chart(px.bar(data_different_sales, x = 'Genre', y = 'Sales in north america in millions'), use_container_width = True)

if type_of_sales == 'Sales in europe in millions': st.plotly_chart(px.bar(data_different_sales, x = 'Genre', y = 'Sales in europe in millions'), use_container_width = True)

if type_of_sales == 'Sales in Japan in millions': st.plotly_chart(px.bar(data_different_sales, x = 'Genre', y = 'Sales in Japan in millions'), use_container_width = True)

if type_of_sales == 'Other sales in millions': st.plotly_chart(px.bar(data_different_sales, x = 'Genre', y = 'Other sales in millions'), use_container_width = True)

if type_of_sales == 'All sales worldwide in millions': st.plotly_chart(px.bar(data_different_sales, x = 'Genre', y = 'All sales worldwide in millions'), use_container_width = True)



