import requests
    # import the library
import subprocess


sender = input("What is your name?\n")

bot_message = ""
message='yes'
r = requests.post('http://localhost:5005/webhooks/rest/webhook', json={"message": message})

print("Bot says, ",end=' ')
for i in r.json():
    bot_message = i['text']
    print(f"{bot_message}")