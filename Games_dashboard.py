'''
streamlit Games dashboard
'''

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from bokeh.models.widgets import Div


def open_link(url, new_tab=True):
    if new_tab: js = f"window.open('{url}')"
    else: js = f"window.location.href = '{url}'"
    html = '<img src onerror="{}">'.format(js)
    div = Div(text = html)
    st.bokeh_chart(div)


_game = pd.read_csv("https://github.com/iilyazakos/games_dashboard/blob/main/game_sales.csv?raw=true")
games = _game[['Rank', 'Name', 'Platform', 'Year',
               'Genre', 'Publisher', 'NA_Sales', 'EU_Sales',
               'JP_Sales', 'Other_Sales', 'Global_Sales']].replace([np.nan, np.inf], 0)

# Multiply all sales by 1000000 because in the dataset they are in millions of pieces
games[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']] = games[[
    'NA_Sales', 'EU_Sales','JP_Sales', 'Other_Sales', 'Global_Sales']] * 1000000

# Delete the values for 2020 and 2017 because they are broken
games.drop(games[games['Year'] == 2020].index, inplace=True)
games.drop(games[games['Year'] == 2017].index, inplace=True)

st.set_page_config(layout = "wide")
st.title('Game sales dashboard')
st.write('Visualization and analytics of games released from 1980 to 2016 by different companies on different platforms')

# Open Github
with st.container() as row_description:
    github = st.button(label = 'My Github')
if github: open_link("https://github.com/iilyazakos")

# We remove zero values for the 'Year' column, make it an integer for convenience
# Deleting null values in the 'Publisher' column
# For convenience, we make the values of 'Year' integer
games.drop(games[games['Year'] == 0.0].index, inplace = True)
games.drop(games[games['Publisher'] == 0].index, inplace = True)
games['Year'] = games['Year'].astype('int64')


# Metrics
with st.container() as row_game_total:
    col_top_sales_region, col_top_platform, col_top_publisher, col_top_genre = st.columns(4)
    with col_top_sales_region:
        value = games[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum().sort_values(ascending = False).index[0].replace('_Sales', '')
        if value == 'NA': st.metric(label = 'Region with the highest sales', value = 'North america')
        elif value == 'EU': st.metric(label = 'Region with the highest sales', value = 'Europe')
        elif value == 'JP': st.metric(label ='Region with the highest sales', value ='Japan')
        elif value == 'Other': st.metric(label ='Region with the highest sales', value ='Other regions')
    with col_top_platform:
        st.metric(label = 'Platform with the biggest sales', value = games.groupby('Platform')['Global_Sales'].sum().sort_values(ascending = False).index[0])
    with col_top_publisher:
        st.metric(label = 'Publisher with the biggest sales', value = games.groupby('Publisher')['Global_Sales'].sum().sort_values(ascending = False).index[0])
    with col_top_genre:
        st.metric(label = 'Category with the biggest sales', value = games.groupby('Genre')['Global_Sales'].sum().sort_values(ascending = False).index[0])


# In which year did the most games come out
with st.container() as row_game_year:
    col_year_max, col_game_platform = st.columns(2)
    with col_year_max:
        game_year_max = games[['Year', 'Name']]
        game_year_max = (game_year_max.groupby(['Year'])['Name'].count()).reset_index()
        game_year_max.columns = ['Year', 'Number of games']

        st.plotly_chart(px.line(game_year_max, x = 'Year',
                                y = 'Number of games', title = 'In which year did the most games come out'), use_container_width = True)

# Platform on Games
    with col_game_platform:
        game_platform = games[['Platform', 'Name']]
        game_platform = (game_platform.groupby(['Platform'])['Name'].count()).reset_index()
        game_platform.columns = ['Platform', 'Number of games']

        st.plotly_chart(px.bar(game_platform, x = 'Platform', y = 'Number of games',
                               title = 'Games on platforms'), use_container_width = True)


# Продажи на платформах по годам
with st.container() as col_dynamics_Global_Sales:
    dynamics_Global_Sales_year = games[['Platform', 'Year', 'Global_Sales']]
    select_platform = st.multiselect('Select platforms', games['Platform'].unique(), 'GB')
    data_for_fig = pd.DataFrame({'platforms': select_platform})
    dynamics_Global_Sales_year = dynamics_Global_Sales_year[dynamics_Global_Sales_year['Platform'].isin(select_platform)]
    dynamics_Global_Sales_year = (dynamics_Global_Sales_year.groupby(['Year', 'Platform'])['Global_Sales'].sum()).reset_index()
    dynamics_Global_Sales_year.columns = ['Years', 'Platform', 'Global Sales']

    st.plotly_chart(px.bar(dynamics_Global_Sales_year, x = 'Years', y = 'Global Sales', color = 'Platform', barmode = 'overlay'), use_container_width = True)


# Which Publisher has the biggest sales
with st.container() as row_game_platform:
    game_max_public = games[['Publisher', 'Global_Sales']]
    game_max_public = (game_max_public.groupby(['Publisher'])['Global_Sales'].sum().sort_values()).reset_index()
    game_max_public.columns = ['Publisher', 'Global Sales']
    round_1 = st.select_slider(label = 'Select the minimum number of sales', options = game_max_public['Global Sales'], value = 81530000)
    game_max_public = game_max_public[game_max_public['Global Sales'] >= round_1]

    st.plotly_chart(px.bar(game_max_public, x = 'Global Sales', y = 'Publisher', height = 550,
                            title = 'Which Publisher has the biggest sales'), use_container_width = True)

with st.container() as select_region:
    one, two_true, three = st.columns(3)
    with two_true:
        type_of_sales = st.radio('Select sales region',
                   ('Sales in North America', 'Sales in Europe',
                    'Sales in Japan', 'Other sales',
                     'All sales worldwide'))

# Which genre produced the most games
with st.container() as row_genre_max_produced:
    col_genre_max_produced, col_different_sales = st.columns(2)
    with col_genre_max_produced:
        game_genre_max_produced = games[['Name', 'Genre']]
        game_genre_max_produced = (game_genre_max_produced.groupby(['Genre'])['Name'].count()).reset_index()
        game_genre_max_produced.columns = ['Number of games', 'Genre']

        st.plotly_chart(px.bar(game_genre_max_produced, x = 'Genre', y = 'Number of games',
                                        labels = {'Genre':'Number of games',
                                                'Number of games':'Genre'},
                                        title = 'Which genre produced the most games'), use_container_width = True)

    with col_different_sales:
        data_different_sales = games[['Genre', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']]
        data_different_sales = (data_different_sales.groupby(['Genre'])[
                                    'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales'].sum()).reset_index()
        data_different_sales.columns = ['Genre', 'Sales in North America', 'Sales in Europe',
                                        'Sales in Japan', 'Other sales',
                                        'All sales worldwide']
        if type_of_sales == 'Sales in North America': st.plotly_chart(
            px.bar(data_different_sales, x = 'Genre', y = 'Sales in North America', title = 'Sales in different categories'), use_container_width = True)

        elif type_of_sales == 'Sales in Europe': st.plotly_chart(
            px.bar(data_different_sales, x = 'Genre', y = 'Sales in Europe', title = 'Sales in different categories'), use_container_width = True)

        elif type_of_sales == 'Sales in Japan': st.plotly_chart(
            px.bar(data_different_sales, x = 'Genre', y='Sales in Japan', title = 'Sales in different categories'), use_container_width = True)

        elif type_of_sales == 'Other sales': st.plotly_chart(
            px.bar(data_different_sales, x = 'Genre', y = 'Other sales', title = 'Sales in different categories'), use_container_width = True)

        elif type_of_sales == 'All sales worldwide': st.plotly_chart(
            px.bar(data_different_sales, x = 'Genre', y = 'All sales worldwide', title = 'Sales in different categories'), use_container_width = True)