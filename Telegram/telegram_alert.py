import configuration as conf
import requests, json, time
from boltiot import Bolt

#configuring Bolt Wifi Module

mybolt = Bolt(conf.API_KEY,conf.DEVICE_ID)

while True:
    #CHECK WHETHER DEVICE IS ONLINE
    response1 = mybolt.isOnline()
    data1 = json.loads(response1)
    online = str(data1['value'])

    #condition for Device Status
    if online == 'online':
        print("Device is Online...\n Please wait 10 seconds \n")

        for i in range (1,11):
            print(i)
            time.sleep(1)

        print('\nReading sensor value...')
        response2 = mybolt.analogRead('A0')
        data2 = json.loads(response2)
        print("Sensor value is : " + str(data2['value']))
        try:
            sensor_value = int(data2['value'])
            Temperature = (100 * sensor_value) / 1024
            print("Current Temperature in Your Room : " + str(Temperature) + "\n\n")
            if Temperature >= conf.maximum_limit or Temperature <= conf.minimum_limit:
                url = "https://api.telegram.org/" + conf.BOT_ID + "/sendMessage"
                data = {
                    "chat_id": conf.CHAT_ID,
                    "text": "The Current temperature sensor value is " +str(sensor_value) + "\n The Current Temperature in Your Room is : "+ str(Temperature)
                }
                try:
                    response = requests.request("POST",url,params=data)
                    print("This is the Telegram URL")
                    print(url)
                    print("This is the Telegram response")
                    print(response.text)
                except Exception as e:
                    print("An error occurred in sending the alert message via Telegram")
                    print(e)
                response3 = mybolt.digitalWrite('1','HIGH')
                print(response3)
                time.sleep(10)
                response4 = mybolt.digitalWrite('1','LOW')
                print(response4)
        except Exception as e:
                    print("An error occurred in sending the alert message via Telegram")
                    print(e)
    else:
        print("\n\nDevice is Offline...\n You Cannot Perform Monitoring\n")
        for i in range (1,11):
            print(i)
            time.sleep(1)
        url = "https://api.telegram.org/" + conf.BOT_ID + "/sendMessage"
        data = {
            "chat_id": conf.CHAT_ID,
            "text": "Your Device is Offline... \n Please Turn On Device To Monitor Data... "
        }
        response = requests.request(
            "POST",
            url,
            params=data
        )
        print("This is the Telegram URL")
        print(url)
        print("This is the Telegram response")
        print(response.text)