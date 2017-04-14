import yweather

def main(message):
    locationraw = message.content.split(' ', 1)[1]
    locationcode = yweather.fetch_woeid(locationraw)
    weather = yweather.fetch_weather(locationcode, metric=True)
    print(weather["condition"]["text"])
    return [["text", weather["condition"]["text"]]]
