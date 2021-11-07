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

# Удаляем нулевые значения по столбцу 'Year', делаем его целочисленным для удобства
# Удаляем нулевые значения по столбцу 'Publisher'

st.set_page_config(layout = "wide")
with st.container() as row_description:
    st.markdown("Hello it's my github")
    github = st.button(label = 'Github')
#open my github
if github: open_link("https://github.com/iilyazakos")

games.drop(games[games['Year'] == 0.0].index, inplace = True)
games.drop(games[games['Publisher'] == 0].index, inplace = True)
games['Year'] = games['Year'].astype('int64')
# games.info()
# games.head()

#__________________________________________________________
# Метрики
# st.title('Average number of sales in North America, Europe, Japan, all and other in millions')
with st.container() as row_game_total:
    st.markdown('Average number of sales in North America, Europe, Japan, all and other in millions')
    col_NA_sales, col_EU_sales, col_JP_sales, col_other_sales, col_global_sales = st.columns(5)
    with col_NA_sales:
        st.metric(label = 'North America', value = round(games['NA_Sales'].mean(), 2))
    with col_EU_sales:
        st.metric(label = 'Europe', value = round(games['EU_Sales'].mean(), 2))
    with col_JP_sales:
        st.metric(label='Japan', value=round(games['JP_Sales'].mean(), 2))
    with col_other_sales:
        st.metric(label='Other', value=round(games['Other_Sales'].mean(), 2))
    with col_global_sales:
        st.metric(label='Global', value=round(games['Global_Sales'].mean(), 2))

# _________________________________________________________
# В какой год выходило больше всего игр

with st.container() as row_game_year:
    col_year_max, col_game_platform = st.columns(2)
    with col_year_max:

        game_year_max = games[['Year', 'Name']]
        game_year_max = (game_year_max.groupby(['Year'])['Name'].count()).reset_index()
        game_year_max.drop(game_year_max[game_year_max['Year'] == 2020].index, inplace = True)
        game_year_max.drop(game_year_max[game_year_max['Year'] == 2017].index, inplace = True)
        game_year_max.columns = ['Year', 'Number of games']

        st.plotly_chart(px.line(game_year_max, x = 'Year',
                                y = 'Number of games', title = 'In which year did the most games come out'), use_container_width = True)

# Игры по платформам
    with col_game_platform:
        game_platform = games[['Platform', 'Name']]
        game_platform = (game_platform.groupby(['Platform'])['Name'].count()).reset_index()
        game_platform.columns = ['Platform', 'Number of games']

        st.plotly_chart(px.bar(game_platform, x = 'Platform', y = 'Number of games',
                               title = 'Games on platforms'), use_container_width = True)

# _______________
# Продажи на платформах по годам
dynamics_Global_Sales_year = games[['Platform', 'Year', 'Global_Sales']]
select_platform = st.multiselect('select platforms', games['Platform'].unique(), 'GB')
data_for_fig = pd.DataFrame({'platforms': select_platform})
dynamics_Global_Sales_year = dynamics_Global_Sales_year[dynamics_Global_Sales_year['Platform'].isin(select_platform)]
dynamics_Global_Sales_year = (dynamics_Global_Sales_year.groupby(['Year', 'Platform'])['Global_Sales'].sum()).reset_index()
dynamics_Global_Sales_year.columns = ['Years', 'Platform', 'Global Sales in millions of dollars']

st.plotly_chart(px.bar(dynamics_Global_Sales_year, x = 'Years', y = 'Global Sales in millions of dollars', color = 'Platform', barmode='overlay'), use_container_width = True)
# _________________________________________________________
# У каких Publisher самые большие продожи
with st.container() as row_game_platform:
    game_max_public = games[['Publisher', 'Global_Sales']]
    game_max_public = (game_max_public.groupby(['Publisher'])['Global_Sales'].count()).reset_index()
    game_max_public.columns = ['Publisher', 'Global Sales in millions of dollars']

    st.plotly_chart(px.line(game_max_public, x = 'Global Sales in millions of dollars', y = 'Publisher',
                            title = 'Which Publisher has the biggest sales'), use_container_width = True)

# _________________________________________________________
# В каком жанре выпускалось больше всего игр
with st.container() as row_genre_max_produced:
    col_genre_max_produced, col_different_sales = st.columns(2)

    with col_genre_max_produced:
        game_genre_max_produced = games[['Name', 'Genre']]
        game_genre_max_produced = (game_genre_max_produced.groupby(['Genre'])['Name'].count()).reset_index()
        game_genre_max_produced.columns = ['Number of games', 'Genre']

        st.plotly_chart(px.bar(game_genre_max_produced, x = 'Genre', y = 'Number of games',
                                        labels={'Genre':'Number of games',
                                                'Number of games':'Genre'},
                                        title = 'Which genre produced the most games'), use_container_width = True)

    with col_different_sales:
        data_different_sales = games[['Genre', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']]
        data_different_sales = (data_different_sales.groupby(['Genre'])[
                                    'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales'].sum()).reset_index()
        data_different_sales.columns = ['Genre', 'Sales in North America in millions', 'Sales in Europe in millions',
                                        'Sales in Japan in millions', 'Other sales in millions',
                                        'All sales worldwide in millions']
        type_of_sales = st.radio('Select sales region',
                                 ('Sales in North America in millions', 'Sales in Europe in millions',
                                  'Sales in Japan in millions', 'Other sales in millions',
                                  'All sales worldwide in millions'))
        if type_of_sales == 'Sales in north america in millions': st.plotly_chart(
            px.bar(data_different_sales, x='Genre', y='Sales in North America in millions', title = 'Sales in different categories'), use_container_width=True)

        if type_of_sales == 'Sales in europe in millions': st.plotly_chart(
            px.bar(data_different_sales, x='Genre', y='Sales in Europe in millions', title = 'Sales in different categories'), use_container_width=True)

        if type_of_sales == 'Sales in Japan in millions': st.plotly_chart(
            px.bar(data_different_sales, x='Genre', y='Sales in Japan in millions', title = 'Sales in different categories'), use_container_width=True)

        if type_of_sales == 'Other sales in millions': st.plotly_chart(
            px.bar(data_different_sales, x='Genre', y='Other sales in millions', title = 'Sales in different categories'), use_container_width=True)

        if type_of_sales == 'All sales worldwide in millions': st.plotly_chart(
            px.bar(data_different_sales, x='Genre', y='All sales worldwide in millions', title = 'Sales in different categories'), use_container_width=True)