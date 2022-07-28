import requests
from bs4 import BeautifulSoup
from kivy.core.text import LabelBase
from kivymd.app import MDApp
from kivy.lang import Builder
import math
from kivy.core.window import Window

Window.size = (350, 600)

kv = '''
MDFloatLayout:
    md_bg_color: 0/255, 181/255, 226/255, .8

    Image:
        source: "location.jfif"
        size_hint: .1, .1
        pos_hint: {"center_x": .5, "center_y": .95}
    MDLabel:
        id:location
        text: ""
        pos_hint: {"center_x": .5, "center_y": .89}
        halign: "center"
        font_size: "20sp"
        font_name: "BPoppins"
    Image:
        id: weather_image
        source: ""
        size_hint: .3, .3
        pos_hint: {"center_x": .5, "center_y": .77}
    MDLabel:
        id: temperature
        text: ""
        markup: True
        pos_hint: {"center_x": .5, "center_y": .62}
        halign: "center"
        font_size: "60sp"
    MDLabel:
        id : weather
        text: ""
        pos_hint: {"center_x": .48, "center_y": .55}
        halign: "center"
        font_size: "25sp"
        font_name: "Poppins"
    MDFloatLayout:
        pos_hint: {"center_x": .25, "center_y": .45}
        size_hint: .22, .1
        Image:
            source: "humidity.jfif"
            pos_hint: {"center_x": .1, "center_y": .5}
        MDLabel:
            id: humidity
            text: ""
            pos_hint: {"center_x": 1, "center_y": .7}
            font_size: "18sp"
            font_name: "Poppins"
        MDLabel:
            text: "Humidity"
            markup: True
            pos_hint: {"center_x": 1, "center_y": .3}
            font_size: "14sp"
            font_name: "Poppins"

    MDFloatLayout:
        pos_hint: {"center_x": .7, "center_y": .45}
        size_hint: .22, .1
        Image:
            source: "wind.jfif"
            pos_hint: {"center_x": .1, "center_y": .5}
        MDLabel:
            id: wind_speed
            text: ""
            pos_hint: {"center_x": 1.1, "center_y": .7}
            font_size: "16sp"
            font_name: "Poppins"

        MDLabel:
            text: "Wind"
            pos_hint: {"center_x": 1.1, "center_y": .3}
            font_size: "14sp"
            font_name: "Poppins"
            
    MDFloatLayout:
        pos_hint: {"center_x": .25, "center_y": .3}
        size_hint: .22, .1
        Image:
            source: "min.jfif"
            pos_hint: {"center_x": .1, "center_y": .5}
        MDLabel:
            id: temp_min
            text: ""
            pos_hint: {"center_x": 1, "center_y": .7}
            font_size: "18sp"
            font_name: "Poppins"
        MDLabel:
            text: "Minimum"
            pos_hint: {"center_x": 1.1, "center_y": .3}
            font_size: "14sp"
            font_name: "Poppins"
    MDFloatLayout:
        pos_hint: {"center_x": .7, "center_y": .3}
        size_hint: .22, .1
        Image:
            source: "max.jfif"
            pos_hint: {"center_x": .1, "center_y": .5}
        MDLabel:
            id: temp_max
            text: ""
            pos_hint: {"center_x": 1, "center_y": .7}
            font_size: "18sp"
            font_name: "Poppins"
        MDLabel:
            text: "Maximum"
            pos_hint: {"center_x": 1.1, "center_y": .3}
            font_size: "14sp"
            font_name: "Poppins"
        
            
    MDFloatLayout:
        size_hint_y: .25
        canvas:
            Color:
                rgb: rgba(215,164,237,255)
            RoundedRectangle:
                size: self.size
                pos:self.pos
                radius: [10,10,0,0]
        MDFloatLayout:
            pos_hint: {"center_x": .5, "center_y": .71}
            size_hint: .9, .30
            canvas:
                Color:
                    rgb: rgba(138,43,226, 255)
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [6]
            TextInput:
                id: city_name
                hint_text: "Enter City Name"
                size_hint: 1,None
                pos_hint: {"center_x": .5, "center_y": .5}
                height: self.minimum_height
                multiline: False
                font_name: "BPoppins"
                font_size: "20sp"
                hint_text_color: 1,1,1,1
                foreground_color: 1,1,1,1
                background_color: 1,1,1,0
                padding: 15
                cursor_color: 1,1,1,1
                cursor_width: "2sp"
        Button:
            text: "Get weather"
            font_name: "BPoppins"
            font_size: "20sp"
            size_hint: .9, .40
            pos_hint: {"center_x": .5, "center_y": .30}
            background_color: 1,1,1,0
            color: rgba(138,43,226,255)
            on_release: app.search_weather()
            canvas.before:
                Color:
                    rgb: 1,1,1,1
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [6]

'''


class Weather_Now_Application(MDApp):
    api_key = "7ccab37f9c05fa178e9e5d5806da6f7e"

    def on_start(self):
        try:
            soup = BeautifulSoup(requests.get(f"https://www.google.com/search?q=weather+at+my+current+location").text,
                                 "html.parser")
            temp = soup.find("span", class_="BNeawe tAd8D AP7Wnd")
            location = ''.join(filter(lambda item: not item.isdigit(), temp.text)).split(",", 1)
            self.get_weather(location[0])
        except requests.ConnectionError:
            print("No Internet Connection")
            exit()


    def build(self):
        return Builder.load_string(kv)

    def get_weather(self, city_name):
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={self.api_key}"

            response = requests.get(url)
            x = response.json()
            if x["cod"] != "404":
                temperature = round(x["main"]["temp"] - 273.15)
                humidity = x["main"]["humidity"]
                weather = x["weather"][0]["main"]
                id = str(x["weather"][0]["id"])
                wind_speed = round(x["wind"]["speed"] * 18 / 5)
                temp_min = int(math.floor(x['main']['temp_min'] - 273.15))
                temp_max = int(math.ceil(x['main']['temp_max'] - 273.15))
                location = x["name"] + ", " + x["sys"]["country"]
                self.root.ids.temperature.text = f"[b]{temperature}[/b]°"
                self.root.ids.weather.text = str(weather)
                self.root.ids.humidity.text = f"{humidity}%"
                self.root.ids.wind_speed.text = f"{wind_speed} km/h"
                self.root.ids.temp_min.text = f"{temp_min}°"
                self.root.ids.temp_max.text = f"{temp_max}°"
                self.root.ids.location.text = location
                if id == "800":
                    self.root.ids.weather_image.source = "sun.jfif"
                elif "200" <= id <= "232":
                    self.root.ids.weather_image.source = "storm.jfif"
                elif "300" <= id <= "321" or "500" <= id <= "531":
                    self.root.ids.weather_image.source = "rain.jfif"
                elif "600" <= id <= "622":
                    self.root.ids.weather_image.source = "snow.jfif"
                elif "701" <= id <= "781":
                    self.root.ids.weather_image.source = "haze.jfif"
                elif "801" <= id <= "804":
                    self.root.ids.weather_image.source = "cloud.jfif"
            else:
                print("City not found")
        except requests.ConnectionError:
            print("No internet connection!")

    def search_weather(self):
        city_name = self.root.ids.city_name.text
        if city_name != "":
            self.get_weather(city_name)


if __name__ == '__main__':
    LabelBase.register(name="Poppins", fn_regular="Poppins-Medium.ttf")
    LabelBase.register(name="BPoppins", fn_regular="Poppins-SemiBold.ttf")
    Weather_Now_Application().run()











