from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit
from PyQt6.QtGui import QIcon, QFont
from PyQt6 import QtCore, QtWidgets
import requests
import sys

API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # Your openweathermap.org API key here <---

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.search_button = None
        self.textbox = None
        self.weather_label = None
        self.wind_label = None

        self.initUI()

    def Textboxes(self):
        self.textbox = QLineEdit(self)
        self.textbox.resize(250, 45)
        self.textbox.setStyleSheet(
            "border-radius: 10px; border: 1px solid black; padding-left: 5px; padding-right: 5px;"
            "background: transparent; background-color: #FFFFFF"
        )
        self.textbox.setPlaceholderText("Enter a city")
        self.textbox.setFont(QFont('Open Sans Light', 12))
        self.textbox.move(30, 20)

    def Buttons(self):
        self.search_button = QtWidgets.QPushButton(self)
        self.search_button.resize(120, 35)
        self.search_button.setStyleSheet(
            "QPushButton { border-radius: 10px; border: 1px solid black; background: transparent;"
            "background-color: #FFFFFF }"
            "QPushButton:pressed { background-color: gray }"
        )
        self.search_button.setFont(QFont('Open Sans Light', 12))
        self.search_button.move(95, 80)
        self.search_button.setText("Enter")
        self.search_button.clicked.connect(self.search_button_clicked)

    def Labels(self):
        self.weather_label = QLabel(self)
        self.weather_label.setStyleSheet(
            "border-radius: 10px; border: 1px solid black; background: transparent;"
            "background-color: #FFFFFF;"
        )
        self.weather_label.resize(270, 100)
        self.weather_label.move(20, 130)
        self.weather_label.setFont(QFont('Open Sans Light', 70))
        self.weather_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.wind_label = QLabel(self)
        self.wind_label.setStyleSheet(
            "border-radius: 10px; border: 1px solid black; background: transparent;"
            "background-color: #FFFFFF;"
        )
        self.wind_label.resize(270, 100)
        self.wind_label.move(20, 250)
        self.wind_label.setFont(QFont('Open Sans Light', 60))
        self.wind_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def initUI(self):
        self.setWindowTitle("weather.io")
        self.setWindowIcon(QIcon("icon.png"))
        self.setFixedSize(310, 380)
        self.Buttons()
        self.Textboxes()
        self.Labels()

        self.weather_init()

    def weather_init(self):
        temp, wind = get_init_request_info()

        self.weather_label.setText(temp + "°C")
        self.wind_label.setText(wind + "km/h")

        if int(temp) < 0:
            self.setStyleSheet("background-color: #78AFFF")
        else:
            self.setStyleSheet("background-color: #FEE591")

    def search_button_clicked(self):
        city_name = self.textbox.text()
        data = get_request(city_name)

        if check_if_code_400_or_404_or_401(data["cod"]) is True:
            temp, wind = get_info(data)
            self.weather_label.setText(temp + "°C")
            self.wind_label.setText(wind + "km/h")
            if int(temp) < 0:
                self.setStyleSheet("background-color: #78AFFF")
            else:
                self.setStyleSheet("background-color: #FEE591")
        else:
            self.textbox.clear()


def has_numbers(string):
    return any(char.isdigit() for char in string)


def get_init_request_info():
    init_ip_request = requests.get("https://api.ipify.org?format=json").json()
    init_city_name_request = requests.get("http://ip-api.com/json/" + init_ip_request["ip"]).json()
    init_data = requests.get("https://api.openweathermap.org/data/2.5/weather?q=" + init_city_name_request["city"] +
                             "&appid=" + API_KEY).json()

    temp = int(round((float(init_data["main"]["temp"]) - 273.15), 0))
    wind_speed = int(round((float(init_data["wind"]["speed"]) * 1.609344), 0))

    return str(temp), str(wind_speed)


def get_request(city_name):
    data_request = requests.get("https://api.openweathermap.org/data/2.5/weather?q=" + city_name +
                                "&appid=" + API_KEY).json()
    return data_request


def get_info(data):
    temp = int(round((float(data["main"]["temp"]) - 273.15), 0))
    wind_speed = int(round((float(data["wind"]["speed"]) * 1.609344), 0))
    return str(temp), str(wind_speed)


def check_if_code_400_or_404_or_401(data):
    if int(data) != 400 and int(data) != 404 and int(data) != 401:
        return True
    else:
        return False


if __name__ == "__main__":
    weather_app = QApplication(sys.argv)
    main_win = mainWindow()

    main_win.show()
    sys.exit(weather_app.exec())
