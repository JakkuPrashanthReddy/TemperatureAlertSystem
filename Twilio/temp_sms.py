from boltiot import Sms, Bolt

import configuration
import json
import time

minimum_limit = 26
maximum_limit = 40

mybolt = Bolt(configuration.API_KEY, configuration.DEVICE_ID)
sms = Sms(configuration.SID, configuration.AUTH_TOKEN, configuration.TO_NUMBER, configuration.FROM_NUMBER)

while True:
    response1 = mybolt.isOnline()
    _data = json.loads(response1)
    online = str(_data['value'])
    if online == 'online':
        print("\ndevice is online...")
        time.sleep(10)
        print("Reading sensor value...")
        response2 = mybolt.analogRead('A0')
        data_ = json.loads(response2)
        print("Sensor value is : " + str(data_['value']))
        try:
            sensor_value = int(data_['value'])
            Temperature = (100 * sensor_value) / 1024
            print("Current Temperature in Your Room : " + str(Temperature) + "\n\n")
            if Temperature >= maximum_limit or Temperature <= minimum_limit:
                # Twilio
                print("Making request to Twilio to send a SMS")
                response3 = sms.send_sms("The Current temperature sensor value is " + str(
                    sensor_value) + "\n The Current Temperature in Your Room is : " + str(Temperature))
                print("Response received from Twilio is: " + str(response3))
                print("Status of SMS at Twilio is :" + str(response3.status))

                response = mybolt.digitalWrite('1', 'HIGH')
                print(response)
                time.sleep(10)
                response = mybolt.digitalWrite('1', 'LOW')
                print(response)
        except Exception as e:
            print("Error occured: Below are the details...")
            print(e)
    else:
        print("Device is Offline...\n You Cannot Perform Monitoring")
        break
    time.sleep(10)
