# -*- coding: utf-8 -*-
"""Final_diploma_f1_ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12NCJxJiuc10SzbJgVRObW0rTDLK4sS3E
"""

#!pip install fastf1

#!pip install seaborn

#!pip install windrose

#Import Libraries
import os
import sys
import fastf1
try:
    fastf1.Cache.enable_cache(sys.path[0]+"/fastf1_cache")
except:
    os.makedirs(sys.path[0]+"/fastf1_cache")
    fastf1.Cache.enable_cache(sys.path[0]+"/fastf1_cache")
from fastf1 import plotting
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D
import datetime
import seaborn as sns
sns.set_style("darkgrid")
import pandas as pd
import numpy as np
from windrose import WindroseAxes
pd.set_option('display.max_columns', None)

"""

Загрузка гонки (ввод страны и год)"""

# Ввод гонки ,секции,страны
year = 2024
location = 'Monza'
session = 'R'

# get session
"""
    session identifier:
    'FP1'-1тренировка, 'FP2'-1тренировка, 'FP3'-3тренировка, 'Q'-квалификация, 'S'- гонка(спринт), 'SQ'-квалификацияспринт , 'R- гонка
    'Practice 1', 'Practice 2', 'Practice 3', 'Qualifying', 'Sprint', 'Sprint Qualifying', 'Sprint Shootout', 'Race'
"""

race = fastf1.get_session(year, location, session)
race.load(weather=True)

# Загружаем данные о погоде
weather_data = race.weather_data # Use the race object instead of the session string

# Визуализация температуры воздуха
plt.figure(figsize=(10, 6))
plt.plot(weather_data['Time'], weather_data['AirTemp'], label='Температура воздуха')
plt.title("Температура воздуха во время гонки")
plt.xlabel("Время")
plt.ylabel("Температура (°C)")
plt.legend()
plt.show()

# Визуализация розы ветров
ax = WindroseAxes.from_ax()
ax.bar(weather_data['WindDirection'], weather_data['WindSpeed'], normed=True, opening=0.8, edgecolor='white')
ax.set_title("Роза ветров")
plt.show()

# Загружаем данные сессии гонки (Гран-при Монцы 2024 года, гонка)
session = fastf1.get_session(2024, 'Monza', 'R') # Use fastf1 instead of f1
session.load(telemetry=True)  # Загружаем данные телеметрии

# Извлекаем данные о погоде для каждого круга
weather_data = session.laps.get_weather_data()

# Преобразуем данные в формат DataFrame для лучшего отображения
weather_df = pd.DataFrame(weather_data)

# Выводим таблицу с данными о погоде и ветре
print(weather_df.head())  # Отображаем первые  5 строк для п

# Отображаем основные данные о результатах гонки
race_results = session.results # Assign the results to the race_results variable
print(race_results[['DriverNumber', 'BroadcastName', 'Abbreviation',
                    'TeamName', 'Position', 'GridPosition',
                    'Q1', 'Q2', 'Q3', 'Time', 'Status', 'Points']])

# Визуализируем позиции гонщиков на финише
plt.figure(figsize=(14, 6))
sns.barplot(x='Position', y='FullName', data=race_results.sort_values('Position'))
plt.title("Финишные позиции гонщиков в Гран-при Монцы 2024 года")
plt.xlabel("Финишная позиция")
plt.ylabel("Гонщик")
plt.show()

# Подробный анализ каждого гонщика
for driver in session.drivers:
    driver_laps = session.laps.pick_driver(driver)

    # Отображаем основные данные по кругам гонщика
    print(f"\nГонщик: {driver_laps['Driver'].iloc[0]}")
    print(driver_laps[['LapNumber', 'LapTime', 'Sector1Time', 'Sector2Time', 'Sector3Time', ]])

    # Визуализация времени кругов для каждого гонщика
    plt.figure(figsize=(10, 5))
    plt.plot(driver_laps['LapNumber'], driver_laps['LapTime'].dt.total_seconds(), label=driver_laps['Driver'].iloc[0])
    plt.title(f"Время кругов для гонщика {driver_laps['Driver'].iloc[0]}")
    plt.xlabel("Номер круга")
    plt.ylabel("Время круга (секунды)")
    plt.legend()
    plt.show()

# Включаем кэш
fastf1.Cache.enable_cache('fastf1_cache')

# Загружаем данные о Гран-при Италии 2024 года (Монца)
race = fastf1.get_event(2024, 'Monza')

# Загружаем данные гоночной сессии
session = race.get_session('R')
session.load()

# Определяем цвета для каждой команды
team_colors = {
    'Ferrari': 'red',
    'McLaren': 'orange',
    'Red Bull Racing': 'blue',
    'Mercedes': 'silver',
    'Aston Martin': 'green',
    'Alpine': 'lightblue',
    'AlphaTauri': 'darkblue',
    'Williams': 'royalblue',
    'Alfa Romeo': 'darkred',
    'Haas': 'black'
}

# Получаем все круги гонщиков
laps = session.laps

# Переходим к каждому кругу и извлекаем позицию каждого гонщика на каждом круге
positions = pd.DataFrame()

for drv in session.drivers:
    driver_laps = laps.pick_driver(drv)
    driver_laps['Driver'] = drv
    driver_laps['Team'] = driver_laps['Team']  # Добавляем данные о команде
    driver_positions = driver_laps[['LapNumber', 'Position', 'Driver', 'Team']]
    positions = pd.concat([positions, driver_positions])

# Теперь строим график изменения позиций гонщиков на протяжении гонки
plt.figure(figsize=(12, 8))

# Проходим по каждому уникальному гонщику и строим график по командам
for driver in positions['Driver'].unique():
    driver_data = positions[positions['Driver'] == driver]
    team_name = driver_data['Team'].iloc[0]  # Получаем название команды гонщика
    color = team_colors.get(team_name, 'gray')  # Получаем цвет команды, если нет — серый

    # Строим график для каждого гонщика
    plt.plot(driver_data['LapNumber'], driver_data['Position'], label=driver, color=color)

# Инвертируем ось Y, так как 1-я позиция выше 20-й
plt.gca().invert_yaxis()

plt.title("Изменение позиций гонщиков на протяжении гонки - Монца 2024")
plt.xlabel("Номер круга")
plt.ylabel("Позиция")
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))  # Легенда с именами гонщиков
plt.grid(True)
plt.show()

results = session.results.loc[:,['Abbreviation','TeamName', 'ClassifiedPosition', 'Points']]
print(results)

# Включаем кэш
fastf1.Cache.enable_cache('fastf1_cache')

# Загружаем данные о Гран-при Италии 2024 года (Монца)
race = fastf1.get_event(2024, 'Monza')

# Загружаем данные гоночной сессии
session = race.get_session('R')
session.load()

# Определяем цвета для каждой команды
team_colors = {
       'Ferrari': 'red',
    'McLaren': 'orange',
    'Red Bull Racing': 'blue',
    'Mercedes': 'silver',
    'Aston Martin': 'green',
    'Alpine': 'lightblue',
    'AlphaTauri': 'darkblue',
    'Williams': 'royalblue',
'Alfa Romeo': 'darkred',
    'Haas': 'black',
}


# Получаем все круги гонщиков
laps = session.laps

# Переходим к каждому кругу и извлекаем позицию каждого гонщика на каждом круге
positions = pd.DataFrame()

for drv in session.drivers:
    driver_laps = laps.pick_driver(drv)
    driver_laps['Driver'] = drv
    driver_laps['Team'] = driver_laps['Team']  # Добавляем данные о команде
    driver_positions = driver_laps[['LapNumber', 'Position', 'Driver', 'Team']]
    positions = pd.concat([positions, driver_positions])

# Агрегируем данные по пит-стопам
pitstop = session.laps.loc[
    (session.laps.LapNumber != 1.0) &
    (session.laps.PitInTime.combine_first(session.laps.PitOutTime).notnull()),
    ['Team', 'Driver', 'LapNumber', 'PitOutTime', 'PitInTime']
].sort_values(by=['Team', 'Driver', 'LapNumber']).reset_index()

# Вычисление времени, затраченного на каждый пит-стоп
pitstop['pittime'] = (pitstop.PitOutTime - pitstop.PitInTime.shift(1)).dt.total_seconds()

# Агрегирование данных по командам
pitstop_team_data = pitstop.groupby(['Team'])['pittime'].mean().sort_values().round(3)

# Создание палитры цветов для команд
color_palette = {team: team_colors.get(team, 'gray') for team in pitstop_team_data.index}

# Построение графика
plt.figure(figsize=(20, 6))
barplot = sns.barplot(x=pitstop_team_data.index, y=pitstop_team_data.values, palette=color_palette, edgecolor='black')
plt.ylabel('Время (с)')
plt.xlabel('Команда')
plt.ylim(19, 30)

# Добавление подписей к столбцам
for i, value in enumerate(pitstop_team_data):
    plt.text(i, value + 0.1, f'{value:.2f}', ha='center')

plt.title(f'Среднее время на пит-стопах \nМонца 2024\n', fontsize=20)
plt.xticks(rotation=45)  # Поворот меток на оси X для улучшения читаемости
plt.tight_layout()



print(pitstop_team_data.index.unique())

# Включаем кэш
fastf1.Cache.enable_cache('fastf1_cache')

# Загружаем данные о Гран-при Италии 2024 года (Монца)
race = fastf1.get_event(2024, 'Monza')

# Загружаем данные гоночной сессии
session = race.get_session('R')
session.load()

# Определяем цвета для каждой команды
team_colors = {
    'Ferrari': 'red',
    'McLaren': 'orange',
    'Red Bull Racing': 'blue',
    'Mercedes': 'silver',
    'Aston Martin': 'green',
    'Alpine': 'lightblue',
    'AlphaTauri': 'darkblue',
    'Williams': 'royalblue',
    'Alfa Romeo': 'darkred',
    'Haas': 'black',
}

# Получаем все круги гонщиков
laps = session.laps

# Агрегируем данные по пит-стопам
pitstop = session.laps.loc[
    (session.laps.LapNumber != 1.0) &
    (session.laps.PitInTime.combine_first(session.laps.PitOutTime).notnull()),
    ['Team', 'Driver', 'LapNumber', 'PitOutTime', 'PitInTime']
].sort_values(by=['Team', 'Driver', 'LapNumber']).reset_index()

# Вычисляем время, затраченное на каждый пит-стоп
pitstop['pittime'] = (pitstop.PitOutTime - pitstop.PitInTime.shift(1)).dt.total_seconds()

# Группируем данные по каждому гонщику
pitstop_driver_data = pitstop.groupby(['Driver', 'Team'])['pittime'].mean().sort_values().round(3)

# Создание палитры цветов для гонщиков на основе их команд
color_palette = [team_colors.get(team, 'gray') for team in pitstop_driver_data.index.get_level_values('Team')]

# Построение графика
plt.figure(figsize=(20, 6))
barplot = sns.barplot(x=pitstop_driver_data.index.get_level_values('Driver'), y=pitstop_driver_data.values, palette=color_palette, edgecolor='black')
plt.ylabel('Время (с)')
plt.xlabel('Гонщик')
plt.ylim(19, 30)

# Добавление подписей к столбцам
for i, value in enumerate(pitstop_driver_data):
    plt.text(i, value + 0.1, f'{value:.2f}', ha='center')

plt.title(f'Среднее время на пит-стопах по гонщикам \nМонца 2024\n', fontsize=20)
plt.xticks(rotation=45)  # Поворот меток на оси X для улучшения читаемости
plt.tight_layout()
plt.show()

df = session.laps

# Выводим список столбцов для проверки их имен
print(df.columns)

# Получаем времена круга для каждого гонщика на каждом составе шин
# Только для выбранных кругов с нормальными условиями на треке (Track Status = 1)
plt.figure(figsize=(20, 6))

# Проверьте, что в DataFrame действительно есть столбец 'Compound'
if 'Compound' in df.columns:
    for compound in df['Compound'].unique():  # Перебираем каждый уникальный состав шин
        average_laptime_per_tyrelife = {}  # Словарь для хранения среднего времени круга по износу шин
        data_tyre = df[df['Compound'] == compound]  # Отфильтровываем данные для текущего состава шин

        # Для каждого значения износа шин (Tyre Life)
        for tyrelife in range(1, int(data_tyre['TyreLife'].max()) + 1):
            # Считаем среднее время круга при данных условиях трека и износе шин
            avg_laptime = data_tyre.loc[
                (data_tyre['TyreLife'] == tyrelife) & (data_tyre['TrackStatus'] == '1'),
                'LapTime'
            ].mean()

            # Convert Timedelta to seconds
            average_laptime_per_tyrelife[tyrelife] = avg_laptime.total_seconds()

        # Извлекаем ключи (износ шин) и значения (среднее время круга)
        key = list(average_laptime_per_tyrelife.keys())
        value = list(average_laptime_per_tyrelife.values())

        # This if statement was not indented properly
        if compound == 'HARD':
            color = 'black'  # Для HARD шин меняем цвет на черный
        elif compound == 'SOFT':
            color = 'red'  # Определяем цвет для шин SOFT
        else:
            color = 'yellow'  # Определяем цвет для шин MEDIUM

        # Строим график для текущего состава шин
        plt.plot(key, value, color=color, marker='o', label=compound)

    plt.ylabel('Время круга (с)')
    plt.xlabel('Износ шин (Tyre Life)')
    plt.title('Время круга в зависимости от износа шин \n' + str(race.name), fontsize=20)
    # # Если нет дождя, определяем лимиты для оси Y на основе медианы времени круга
    # if not rain:
    #     plt.ylim(df['LapTime'].median() - 3, df['LapTime'].median() + 3)

    # Добавляем легенду
    plt.legend(title="Состав шин")
    plt.show()

import fastf1
import matplotlib.pyplot as plt
race_name="Monza"

fig, ax = plt.subplots(figsize=(20, 10))  # Создаем фигуру и оси для графика
plt.title('Стратегия шин \n' + race_name, fontsize=30)  # Устанавливаем заголовок графика
plt.xlabel('Круги')  # Устанавливаем подпись оси X
plt.grid(False)  # Отключаем сетку

# Получаем словарь цветов для разных составов шин
compound_color = fastf1.plotting.COMPOUND_COLORS

# Группируем данные по гонщику, стинту, составу шин и новизне шин
tyre_stint = df.groupby(['Driver', 'Stint', 'Compound', 'FreshTyre']).agg({'LapNumber': 'min', 'TyreLife': 'count'}).reset_index()

# Используем результаты гонки
for drv in list(results.Abbreviation)[::-1]:  # Перебираем гонщиков в обратном порядке
    driver_stints = tyre_stint[tyre_stint['Driver'] == drv]  # Фильтруем данные по текущему гонщику

    # Отрисовываем каждый стинт для текущего гонщика
    for idx, row in driver_stints.iterrows():
        plt.barh(
            y=drv,  # Сокращение гонщика по оси Y
            width=row["TyreLife"],  # Ширина бара - количество кругов
            left=max(row['LapNumber'] - 1, 0),  # Позиция на оси X - номер круга начала стинта
            color=compound_color.get(row.Compound, 'green'),  # Цвет стинта на основе состава шин
            edgecolor="black",  # Цвет границы бара
            alpha=0.6 if not row.FreshTyre else 1,  # Прозрачность для старых шин
            hatch='/' if not row.FreshTyre else None  # Штриховка для старых шин
        )

        # Добавляем номер круга начала стинта
        if not row['LapNumber'] <= 1.0:
            plt.text(row['LapNumber'] - 1.25, drv, round(row['LapNumber'] - 1),
                     fontweight='extra bold', backgroundcolor='black', color='white')

    # Добавляем общее количество кругов для гонщика на график
    plt.text(df.LapNumber.max() + 1, drv, driver_stints['TyreLife'].sum(),
             fontweight='extra bold', backgroundcolor='black', color='white')

# Показать график
plt.show()

#Время круга для топ 5 гонщиков
# Топ 5 гонщиков (по финальным результатам гонки)
# Используем переменную 'results' вместо 'race.results'
top_5_drivers = list(results.Abbreviation.iloc[:5])

# data cleaning
df_top5 = df.loc[df.Driver.isin(top_5_drivers),['LapTime','LapNumber','Driver']]
df_top5 = df_top5.reset_index(drop=True)

#Словарь для топ 5 гонщиков
driver_color = {
    'LEC': 'red',
    'PIA': 'yellow',
    'NOR': 'orange',
    'SAI': 'blue',
    'HAM': 'grey'
}


plt.figure(figsize=(20,6))
sns.lineplot(df_top5, x=df_top5['LapNumber'], y=df_top5['LapTime'], marker = "o", hue=df_top5['Driver'], palette = driver_color)
plt.ylabel('Время круга (с)')
plt.xlabel('Круги')
plt.title('Время круга в гонке \n'+race_name,  fontsize=20)

# Set rain to False т к в этот день дождя не было
rain = False


plt.show()

# Отфильтруем круги с действительным временем и без удаленных кругов
valid_laps = df[(df['LapTime'].notna()) & (df['Deleted'] == False)]

# Найдем минимальное время круга (самый быстрый круг)
fastest_lap = valid_laps.loc[valid_laps['LapTime'].idxmin()]

# Получим информацию о самом быстром круге
fastest_driver = fastest_lap['Driver']
fastest_lap_time = fastest_lap['LapTime']
fastest_lap_number = fastest_lap['LapNumber']

# Выводим информацию
print(f"Самый быстрый круг был у {fastest_driver} на круге {fastest_lap_number}, с временем {fastest_lap_time}.")