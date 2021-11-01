'''
streamlit Games dashboard
'''



import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Rank - Рейтинг общих продаж
# Name  - Название игр
# Platform  - Платформа выпуска игр (т. е. ПК,PS4 и т.д.)
# Year  - Год выпуска игры
# Genre  - Жанр игры
# Publisher  - Издатель игры
# NA_Sales - Продажи в Северной Америке (в миллионах)
# EU_Sales - Продажи в Европе (в миллионах)
# JP_Sales - Продажи в Японии (в миллионах)
# Other_Sales - Продажи в остальном мире (в миллионах)
# Global_Sales - Общий объем продаж по всему миру.

_game = pd.read_csv("https://github.com/iilyazakos/games_dashboard/blob/main/game_sales.csv?raw=true")
games = _game[['Rank', 'Name', 'Platform', 'Year',
                  'Genre', 'Publisher', 'NA_Sales', 'EU_Sales',
                  'JP_Sales','Other_Sales','Global_Sales']].replace([np.nan, np.inf], 0)

# Удаляем нулевые значения по столбцу 'Year', делаем его целочисленным для удобства
# Удаляем нулевые значения по столбцу 'Publisher'

games.drop(games[games['Year'] == 0.0].index, inplace = True)
games.drop(games[games['Publisher'] == 0].index, inplace = True)
games['Year'] = games['Year'].astype('int64')
# games.info()
# games.head()


# _________________________________________________________
# В какой год выходило больше всего игр

with st.container() as row_game_year_max:
    game_year_max = games[['Year', 'Name']]
    game_year_max = (game_year_max.groupby(['Year'])['Name'].count()).reset_index()
    game_year_max.drop(game_year_max[game_year_max['Year'] == 2020].index, inplace = True)
    game_year_max.drop(game_year_max[game_year_max['Year'] == 2017].index, inplace = True)
    game_year_max.columns = ['Year', 'Number of games']

    fig_line_year_max = go.Figure()
    fig_line_year_max = px.line(game_year_max, x = 'Year', y = 'Number of games', title = 'In which year did the most games come out')

    st.plotly_chart(fig_line_year_max, use_container_width = True)


# _________________________________________________________
# Игры по платформам
with st.container() as row_game_platform:
    game_platform = games[['Platform', 'Name']]
    game_platform = (game_platform.groupby(['Platform'])['Name'].count()).reset_index()
    game_platform.columns = ['Platform', 'Number of games']
    fig_game_platform = go.Figure()
    fig_game_platform = px.bar(game_platform, x = 'Platform', y = 'Number of games', title = 'Games on platforms')

    st.plotly_chart(fig_game_platform, use_container_width=True)


# _________________________________________________________
# У каких Publisher самые большие продожи
with st.container() as row_game_platform:
    game_max_public = games[['Publisher', 'Global_Sales']]
    game_max_public = (game_max_public.groupby(['Publisher'])['Global_Sales'].count()).reset_index()
    game_max_public.columns = ['Publisher', 'Global sales']
    fig_max_public = go.Figure()
    fig_max_public = px.line(game_max_public, x = 'Global sales', y = 'Publisher', title = 'Which Publisher has the biggest sales')

    st.plotly_chart(fig_max_public, use_container_width=True)
