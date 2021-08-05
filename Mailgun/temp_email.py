import configuration, json, time
from boltiot import Bolt, Email

minimum_limit = 25
maximum_limit = 40

mybolt = Bolt(configuration.API_KEY, configuration.DEVICE_ID)
mailer = Email(configuration.MAILGUN_APIKEY, configuration.SANDBOX_URL, configuration.SENDER_EMAIL, configuration.RECIPIENT_EMAIL)

while True:
    response1 = mybolt.isOnline()
    data1 = json.loads(response1)
    online = str(data1['value'])

    if online == 'online':
        print("\nDevice is Online...")
        time.sleep(10)
        print("Reading Sensor value...")
        response2 = mybolt.analogRead('A0')
        data2 = json.loads(response2)
        print("Sensor value is : "+ str(data2['value']))
        try:
            sensor_value = int(data2['value'])
            Temperature = (100 * sensor_value) / 1024
            print("Current Temperature in Your Room : " + str(Temperature) + "\n\n")
            if Temperature >= maximum_limit or Temperature <= minimum_limit:
                print("Making request to Mailgun to send Email...")
                response3 = mailer.send_email("Alert !","The Current temperature sensor value is " +str(sensor_value) + "\n The Current Temperature in Your Room is : "+ str(Temperature))
                response_text = json.loads(response3.text)
                print("Response received from Mailgun is: " + str(response_text['message']))
                response = mybolt.digitalWrite('1', 'HIGH')
                print(response)
                time.sleep(10)
                response = mybolt.digitalWrite('1', 'LOW')
                print(response)
        except Exception as e:
            print ("Error occured: Below are the details...")
            print (e)
    else:
        print("Device is Offline...\n You Cannot Perform Monitoring")
        break
    time.sleep(10)
