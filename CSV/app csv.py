import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Инициализация стиля графиков
sns.set()

# Заголовок приложения
st.title("Анализ CSV-файла")
st.write("Загрузите ваш CSV-файл и делайте аналитические выводы!")

# Загрузка файла с кешированием
@st.cache_data
def load_csv(file):
    return pd.read_csv(file)

# Загрузка CSV
uploaded_file = st.file_uploader("Выберите CSV-файл для анализа", type=["csv"])

if uploaded_file is not None:
    df = load_csv(uploaded_file)

    # Отображение первых строк
    st.subheader("Первые строки файла")
    st.write(df.head())

    # Выбор столбцов
    columns = df.columns.tolist()
    selected_cols = st.multiselect("Выберите столбцы для анализа", columns, default=columns[:1])

    if selected_cols:
        # Анализ первого выбранного столбца
        col = selected_cols[0]
        col_data = df[col]

        st.subheader(f"Статистика по столбцу: {col}")

        if pd.api.types.is_numeric_dtype(col_data):
            mean_val = col_data.mean()
            median_val = col_data.median()
            std_val = col_data.std()
            st.write(f"Среднее: {mean_val}")
            st.write(f"Медиана: {median_val}")
            st.write(f"Стандартное отклонение: {std_val}")

        elif pd.api.types.is_datetime64_any_dtype(col_data):
            min_date = col_data.min()
            max_date = col_data.max()
            st.write(f"Минимальная дата: {min_date}")
            st.write(f"Максимальная дата: {max_date}")

        else:
            st.write("Столбец содержит текстовые данные или тип данных не применяется для статистики.")

        # Построение графиков пар столбцов
        st.subheader("Построение графиков для пар столбцов")
        plot_type = st.selectbox("Выберите тип графика", ["Линейный", "Диаграмма рассеяния"])

        if len(selected_cols) >= 2:
            col_x = selected_cols[0]
            col_y = selected_cols[1]

            def plot_graph():
                plt.figure()
                if pd.api.types.is_numeric_dtype(df[col_x]) and pd.api.types.is_numeric_dtype(df[col_y]):
                    if plot_type == "Линейный":
                        plt.plot(df[col_x], df[col_y])
                        plt.xlabel(col_x)
                        plt.ylabel(col_y)
                        plt.title(f"Линейный график {col_x} vs {col_y}")
                    else:
                        plt.scatter(df[col_x], df[col_y])
                        plt.xlabel(col_x)
                        plt.ylabel(col_y)
                        plt.title(f"Диаграмма рассеяния {col_x} vs {col_y}")
                    st.pyplot(plt)
                else:
                    st.write("Для построения графика выбраны неподходящие типы данных.")

            plot_graph()
        else:
            st.write("Выберите хотя бы два столбца для построения графика.")

        # Построение графика распределения
        st.subheader("График распределения выбранного столбца")
        dist_plot_type = st.selectbox("Тип графика распределения", ["Гистограмма", "Кривая плотности", "Столбчатая"])

        def plot_distribution():
            plt.figure()
            if pd.api.types.is_numeric_dtype(col_data):
                if dist_plot_type == "Гистограмма":
                    sns.histplot(col_data, kde=False)
                    plt.title(f"Гистограмма по {col}")
                elif dist_plot_type == "Кривая плотности":
                    sns.kdeplot(col_data, fill=True)
                    plt.title(f"Плотность по {col}")
                elif dist_plot_type == "Столбчатая":
                    counts = col_data.value_counts()
                    counts.plot.bar()
                    plt.title(f"Столбчатая диаграмма по {col}")
            elif pd.api.types.is_datetime64_any_dtype(col_data):
                date_counts = col_data.dt.date.value_counts().sort_index()
                date_counts.plot.line()
                plt.title(f"Распределение дат по {col}")
            else:
                st.write("Неподдерживаемый тип данных для графика распределения.")
                return
            st.pyplot(plt)

        if st.button("Построить график распределения"):
            plot_distribution()

        # Диаграмма взаимного распределения
        st.subheader("Диаграмма взаимного распределения")
        if len(selected_cols) >= 2:
            col_x2 = selected_cols[0]
            col_y2 = selected_cols[1]

            plt.figure()
            sns.scatterplot(x=df[col_x2], y=df[col_y2])
            plt.title(f"Взаимное распределение: {col_x2} и {col_y2}")
            st.pyplot(plt)
        else:
            st.write("Для построения диаграммы взаимного распределения выберите хотя бы два столбца.")

        # Кнопка для сохранения текущего графика
        st.subheader("Экспорт изображений")
        if st.button("Сохранить текущий график как изображение"):
            filename = "plot.png"
            plt.savefig(filename)
            st.success(f"График сохранен как {filename}")
else:
    st.info("Пожалуйста, загрузите CSV-файл для начала анализа.")