import sys
from PyQt5.QtWidgets import*
import re
import requests


list_of_cities = []
with open("capitalsid.csv", encoding='utf-8') as raw:
    for line in raw:
        line = line.strip()
        raw_line = list(re.split(r',', line))
        list_of_cities.append(raw_line)        # Формируется исходный список
list_of_cities.pop(0)                              # Удаляются заголовки

# По списку отправляются запросы, из ответов извлекаются нужные данные и добавляются в список
# https://api.openweathermap.org/data/2.5/weather?id={city id}&appid={API key}&lang={lang}
for line in list_of_cities:
    city_id = line[1]
    api = 'https://api.openweathermap.org/data/2.5/weather?id=' + city_id + '&appid=XXXXXXXXXXXXXXXXXXXXXXXXXXX&lang=ru'
    json_data = requests.get(api).json()
    condition = json_data['weather'][0]['description']
    temp = int(json_data['main']['temp'] - 273.15)
    wind = json_data['wind']['speed']
    name = json_data['name']
    line.append(condition)
    line.append(temp)
    line.append(wind)
    line.append(name)
# Пример list_of_cities ['AE', '292968', '0', 'Abu Dhabi', 'ясно', 32, 1.03, 'Абу-Даби']

# Из полученных ответов формируются списки для заполнения оконного приложения
list_condition = ['Любые']
min_temperature = 50
max_temperature = -50
max_wind = 0
for line in list_of_cities:
    if line[4] not in list_condition:
        list_condition.append(line[4])
    if min_temperature > line[5]:
        min_temperature = line[5]
    if max_temperature < line[5]:
        max_temperature = line[5]
    if max_wind < line[6]:
        max_wind = line[6]
# Пример list_of_conditions ['Любые', 'ясно', 'небольшая облачность', 'пасмурно', 'облачно с прояснениями']

list_temperature = ['Любая']
for i in range(min_temperature - 1, max_temperature + 1, 5):
    list_temperature.append('От ' + str(i) + ' до ' + str(i+5))
# Пример list_of_temperature ['Любая', 'От -1 до 4', 'От 4 до 9', 'От 9 до 14', 'От 14 до 19', 'От 19 до 24']

list_wind = ['Любой']
for j in range(0, int(max_wind) + 1, 3):
    list_wind.append('От ' + str(j) + ' до ' + str(j+3))
# Пример list_of_wind ['Любой', 'От 0 до 3', 'От 3 до 6', 'От 6 до 9', 'От 9 до 12']

# Создается и запускается оконное приложение
app = QApplication(sys.argv)
w = QWidget()
w.resize(300, 400)
w.move(100, 100)
w.setWindowTitle('Где моя погода?')

condition = QLabel('Погодные условия')
condition_box = QComboBox()
condition_box.addItems(list_condition)
temperature = QLabel('Температура, градусы Цельсия')
temperature_box = QComboBox()
temperature_box.addItems(list_temperature)
wind = QLabel('Ветер, м/сек')
wind_box = QComboBox()
wind_box.addItems(list_wind)
show_button = QPushButton('Показать')
list_window = QListWidget()

line = QVBoxLayout()
line.addWidget(condition)
line.addWidget(condition_box)
line.addWidget(temperature)
line.addWidget(temperature_box)
line.addWidget(wind)
line.addWidget(wind_box)
line.addWidget(show_button)
line.addWidget(list_window)
w.setLayout(line)

city_list = []
for line in list_of_cities:
    city_list.append(line[7])
city_list.sort()
list_window.addItems(city_list)


def show():
    take_temperature = temperature_box.currentText()
    if take_temperature != 'Любая':
        t1, t2 = re.findall('[-]?\d+', take_temperature)
    else:
        t1, t2 = '-100', '100'
    take_wind = wind_box.currentText()
    if take_wind != 'Любой':
        w1, w2 = re.findall('[-]?\d+', take_wind)
    else:
        w1, w2 = '0', '100'
    take_condition = condition_box.currentText()
    if take_condition != 'Любые':
        city_list = []
        for line in list_of_cities:
            if line[4] == take_condition and line[5] > int(t1) and line[5] <= int(t2) and line[6] > int(w1) and line[6] <= int(w2):
                city_list.append(line[7])
        city_list.sort()
        list_window.clear()
        list_window.addItems(city_list)
    else:
        city_list = []
        for line in list_of_cities:
            if line[5] > int(t1) and line[5] <= int(t2) and line[6] > int(w1) and line[6] <= int(w2):
                city_list.append(line[7])
        city_list.sort()
        list_window.clear()
        list_window.addItems(city_list)

show_button.clicked.connect(show)

w.show()
sys.exit(app.exec_())
