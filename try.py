import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st


_game = pd.read_csv("https://github.com/iilyazakos/games_dashboard/blob/main/game_sales.csv?raw=true")
games = _game[['Rank', 'Name', 'Platform', 'Year',
                  'Genre', 'Publisher', 'NA_Sales', 'EU_Sales',
                  'JP_Sales','Other_Sales','Global_Sales']].replace([np.nan, np.inf], 0)

games.drop(games[games['Year'] == 0.0].index, inplace = True)
games.drop(games[games['Publisher'] == 0].index, inplace = True)
games['Year'] = games['Year'].astype('int64')

st.set_page_config(layout = "wide")
dynamics_Global_Sales_year = games[['Platform', 'Year', 'Global_Sales']]
select_platform = st.multiselect('select platforms', games['Platform'].unique(), 'GB')
data_for_fig = pd.DataFrame({'platforms': select_platform})
dynamics_Global_Sales_year = dynamics_Global_Sales_year[dynamics_Global_Sales_year['Platform'].isin(select_platform)]
dynamics_Global_Sales_year = (dynamics_Global_Sales_year.groupby(['Year', 'Platform'])['Global_Sales'].sum()).reset_index()
dynamics_Global_Sales_year.columns = ['Years', 'Platform', 'Global Sales in millions of dollars']

type_fig = st.radio('choose the type of chart',
                    ('Line', 'Bar', 'Dots (scatter)', 'dots with line', 'dots with different sizes'))


if type_fig == 'Line': st.plotly_chart(px.line(dynamics_Global_Sales_year, x = 'Years', y = 'Global Sales in millions of dollars', color = 'Platform'), use_container_width = True)

if type_fig == 'Bar': st.plotly_chart(px.bar(dynamics_Global_Sales_year, x = 'Years', y = 'Global Sales in millions of dollars', color = 'Platform'), use_container_width = True)

if type_fig == 'Dots (scatter)': st.plotly_chart(px.scatter(dynamics_Global_Sales_year, x = 'Years', y = 'Global Sales in millions of dollars', color = 'Platform'), use_container_width = True)

if type_fig == 'dots with line': st.plotly_chart(px.line(dynamics_Global_Sales_year, x = 'Years', y = 'Global Sales in millions of dollars', color = 'Platform', markers = True), use_container_width = True)

if type_fig == 'dots with different sizes': st.plotly_chart(px.scatter(dynamics_Global_Sales_year, x = 'Years', y = 'Global Sales in millions of dollars', color = 'Platform', size = 'Global Sales in millions of dollars'), use_container_width = True)



