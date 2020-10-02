data={"sound":0,"temp":0,"hum":0,"gas_MQ5":0,"timestamp":"1518551913891","gas_MQ3":0,"gas_MQ2":0,"light":0,"gas_MQ9":0,"team":"blue"}

Transporter_Queue={}
Transporter_Queue["Blue"]={}


if "team" in data:
    print("Team is %s",str(data['team']))
    if data['team'] == 'blue':
        Transporter_Queue["Blue"].update(data)
        print("Blue Queue contains %s",str(Transporter_Queue["Blue"]))

