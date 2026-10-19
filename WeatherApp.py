from re import match
import sys
from unittest import case 
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt
import requests

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter a City Name",self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperatere_label = QLabel( self)
        self.emotji_label = QLabel(self)
        self.description_label = QLabel( self)
        self.initui()
        
    def initui(self):
        
        self.setWindowTitle("Weather App")
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperatere_label)
        vbox.addWidget(self.emotji_label)
        vbox.addWidget(self.description_label)
         
        self.setLayout(vbox)
        
        
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperatere_label.setAlignment(Qt.AlignCenter)
        self.emotji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperatere_label.setObjectName("temperatere_label")
        self.emotji_label.setObjectName("emotji_label")
        self.description_label.setObjectName("description_label")
        
        self.setStyleSheet("""
                            
                            QLabel#city_label{
                               font-size:40px;
                               font-style: italic;
                           }
                            QLineEdit#city_input{
                               font-size : 20px;
                               font-style : italic;
                           }
                            QPushButton#get_weather_button{
                               font-size:30px;
                               font-weight: bold;
                               font-style : italic;
                           }
                           QLabel#temperatere_label{
                               font-size: 75px;
                           }
                           QLabel#emotji_label{
                               font-size :70px;
                               font-family : segoe UI emoji;
                           }
                           QLabel#description_label{
                               font-size:50px;
                               font-style:italic;
                               
                           }
                           
                           """)
        self.get_weather_button.clicked.connect(self.get_weather)
        

    def get_weather(self):
        api_key = "2e5d6d5f2e9298eb15fb15da202b65c2"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        
        try:    
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
                
            if data["cod"] == 200:
                self.display_weather(data)
                
                
        except requests.exceptions.HTTPError as http_error:
            
            match response.status_code:
                case 400:
                    self.display_error("Bad Request:\nPlease check your input")
                
                case 401:
                    self.display_error(" Unauthorized:\ninvalid API key")
                case 403:
                    self.display_error("Forbidden:\naccess denied")
                case 404:
                    self.display_error("Not found:\ncity not found")
                case 500:
                    self.display_error("Internal Server:\nPlease try again later")
                case 502:
                    self.display_errort("Bad gateway:\nInvalid responds from the server ")
                case 503:
                    self.display_errort("Service Unavalibel:\nServer is donw")
                case 504:
                    self.display_error("Gateway timeout:\nNo respondds from the server")
                case _:
                    self.display_error(f"HTTP error occured:\n{ http_error}")
                    
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck ypur connection")
        
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")
        
        except requests.exceptions.TooManyRedirects:
            self.display_error(("Too many redirects:\nCheck the URL"))
            
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request error:\n{req_error}")
            
    
    def  display_error(self, message):
         self.temperatere_label.setStyleSheet("font-size - 30px")
         self.temperatere_label.setText(message)
         self.emotji_label.clear()
         self.description_label.clear()
    
    def display_weather(self,data):
        self.temperatere_label.setStyleSheet("font-size - 75px")
        temperatere_K = data["main"]["temp"]
        temperatere_c = temperatere_K - 273.15
        temperatere_f = (temperatere_K* 9/5)- 459.67
        weather_id =  data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]
        
        
        
        
        self.temperatere_label.setText(f"{temperatere_c:.0f}°C")
        self.emotji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)
      
    @staticmethod 
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return " ⛈️ "
        elif 300 <= weather_id <= 321:
            return " 🌥️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "🌨️"
        elif 701 <= weather_id <= 741:
            return " 🌫️ "
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return " 🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return " "
        


if __name__ == "__main__":
    app =QApplication(sys.argv)
    weatherapp = WeatherApp()
    weatherapp.show()
    sys.exit(app.exec_())