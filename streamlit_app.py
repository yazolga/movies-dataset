import altair as alt # установка декларативной библиотеки визуализации данных
import pandas as pd # установка библиотека для обработки и анализа структурированных данных
import streamlit as st # установка библиотеки для разработки веб-приложений

# Показать заголовок и описание страницы.
st.set_page_config(page_title="Данные фильмов", page_icon="🎬")
st.title("🎬 Данные фильмов")
st.write(
    """
    Это приложение визуализирует данные из [Базы данных фильмов (TMDB)](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata).
    Оно показывает, какой жанр фильмов показал лучшие кассовые сборы за эти годы. Просто
    нажмите на виджеты ниже, чтобы изучить!
    """
)


# Загрузка данныех из CSV. Мы их кэшируем, чтобы не перезагружаться каждый раз 
# при повторном запуске приложения (например, если пользователь взаимодействует с виджетами).
@st.cache_data
def load_data():
    df = pd.read_csv("data/movies_genres_summary.csv") # файл с таблицей, на основе нее делается визуализация
    return df


df = load_data()

# Отображение виджета множественного выбора с жанрами с помощью `st.multiselect`.
genres = st.multiselect(
    "Жанры",
    df.genre.unique(),
    ["Боевик", "Приключение", "Комедия", "Драма", "Ужастик"],
)

# Показ виджета-слайдера с годами с помощью `st.slider`.
years = st.slider("Годы", 2010, 2012, (2014, 2016))

# Фильтруем фрейм данных на основе входных данных виджета и изменяем его форму.
df_filtered = df[(df["genre"].isin(genres)) & (df["year"].between(years[0], years[1]))]
df_reshaped = df_filtered.pivot_table(
    index="year", columns="genre", values="gross", aggfunc="sum", fill_value=0
)
df_reshaped = df_reshaped.sort_values(by="year", ascending=False)


# Отобразить данные в виде таблицы, используя `st.dataframe`.
st.dataframe(
    df_reshaped,
    use_container_width=True,
    column_config={"year": st.column_config.TextColumn("Год")},
)

# Отобразить данные в виде линейного графика из Altair, используя `st.altair_chart`.
df_chart = pd.melt(
    df_reshaped.reset_index(), id_vars="year", var_name="genre", value_name="gross"
)
chart = (
    alt.Chart(df_chart)
    .mark_line()
    .encode(
        x=alt.X("year:N", title="Год"),
        y=alt.Y("gross:Q", title="Доход ($)"),
        color="genre:N",
    )
    .properties(height=320)
)
st.altair_chart(chart, use_container_width=True)
