import requests
import heyoo
from heyoo import WhatsApp
import os
import json
from dotenv import load_dotenv
from flask import Flask, request
import shutil
from inputimeout import inputimeout, TimeoutOccurred
Temp_access_token='EAAFvttE59XkBAIxoNk9mCbmvDo8bwPmBS2wpG93LHTeP4v5Nk6zqBpiqmQhh1JAjhmV2Ec0j3hRG49HPL0ZAy1EZAaeHgOZBHkZCsu5BQZAA74eADPLsAZCgWj8lWk0yigopsZBimXXjZAWDcrww0U27txK0FwYiXaZBiDH2jgVHKcVdGQuWBFfRe'
hed = {'Authorization': 'Bearer ' + Temp_access_token}
messenger = WhatsApp(Temp_access_token,phone_number_id='105358718868002')
print('Do you want to send a message')

 
#send to rasa
def send_rasa(sender, message):
    r = requests.post('http://localhost:5005/webhooks/rest/webhook', json={"sender":sender,"message": message})
    return r.json()


#Send Message
def send(type,to,data=None,id=None):
    if type == 'text':
        if data is not None:
            messenger.send_message(data,to)
        else:
            data=input('Enter Message')
            messenger.send_message(data,to)

    elif type == 'template':
        if data is not None:
            messenger.send_template(data,to)
        else:        
            data=input('Enter Template name')
            messenger.send_template(data,to)
    elif type == 'image':
        if id!=None:
            messenger.send_image(image=f'{id}', recipient_id=f"{to}",link=False)
           
        else:
            data=input('Enter link')
            messenger.send_image(image=f'{data}', recipient_id=f"{to}")
                 
    elif type == 'video':
        if id!=None:
            messenger.send_video(video=f'{id}', recipient_id=f"{to}",link=False)
           
        else:
            data=input('Enter link')
            messenger.send_video(video=f'{data}', recipient_id=f"{to}")
    elif type == 'audio':
        if id!=None:
            messenger.send_audio(audio=f'{id}', recipient_id=f"{to}",link=False)
           
        else:
            data=input('Enter link')
            messenger.send_audio(audio=f'{data}', recipient_id=f"{to}")
    elif type == 'document':
        
        if id!=None:
            messenger.send_document(document=f'{id}', recipient_id=f"{to}",link=False)
             
            
        else:
            data=input('Enter link')
            messenger.send_document(document=f'{data}', recipient_id=f"{to}")
    elif type == 'location':
        if data!=None:
            messenger.send_location(lat=f"{data['latitude']}", long=f"{data['longitude']}",name='Your current location',address=None,recipient_id=f"{to}")
        else:    
            lat=input('enter lat')
            long=input('enter lon')
            name=input('enter name')
            address='enter address'
            messenger.send_location(lat=f'{lat}',long='{long}',name=f'{name}',address=f'{address}', recipient_id=f"{to}")
       
#Recieve message                           
def recieve(type,data):
    if type == 'text':
        message = messenger.get_message(data)
        print(message)
        return message

    elif type == 'template':
        pass
    elif type == 'image':
        im_id=data['entry'][0]['changes'][0]['value']['messages'][0][f'{type}']['id']
        url='https://graph.facebook.com/v13.0/' + data['entry'][0]['changes'][0]['value']['messages'][0]['image']['id']
        url='https://graph.facebook.com/v13.0/' + im_id
        response = requests.get(url, headers=hed)
        
        return [im_id,response.json(),response]

    elif type == 'video':
        ved_id=data['entry'][0]['changes'][0]['value']['messages'][0][f'{type}']['id']
        url='https://graph.facebook.com/v13.0/' + ved_id
        response = requests.get(url, headers=hed)
        
        return [ved_id,response.json(),response]
    elif type == 'audio':
        aud_id=data['entry'][0]['changes'][0]['value']['messages'][0][f'{type}']['id']
        url='https://graph.facebook.com/v13.0/' + aud_id
        response = requests.get(url, headers=hed)
        
        return [aud_id,response.json(),response]
    
    elif type == 'document':
        doc_id=data['entry'][0]['changes'][0]['value']['messages'][0][f'{type}']['id']
        url='https://graph.facebook.com/v13.0/' + doc_id
        response = requests.get(url, headers=hed)
        
        return [doc_id,response.json(),response]


    elif type=='contacts':
        contact_info=data['entry'][0]['changes'][0]['value']['messages'][0]['contacts'][0]
        return contact_info
    elif type == 'location':
        address= data['entry'][0]['changes'][0]['value']['messages'][0]['location']  
        return address

#download message
def download(type,id,url):
    file_name='download'+'_'+type+'_'+id
    if type == 'image':
        read_data = requests.get(url,headers=hed,stream=True)
        read_data.raw.decode=True
        
    
        if read_data.status_code == 200:
            with open(file_name+'.jpg','wb') as f2:
                shutil.copyfileobj(read_data.raw, f2)
                f2.close()
            #print('Image sucessfully Downloaded: ',file_name)
            file_path=os.path.abspath(file_name)
            return file_path


        else:
            return 'image could not be downloaded'

    elif type == 'video':
        read_data = requests.get(url,headers=hed,stream=True)
        read_data.raw.decode=True
        
    
        if read_data.status_code == 200:
            with open(file_name+'.mp3','wb') as f2:
                shutil.copyfileobj(read_data.raw, f2)
                f2.close()
            #print('video sucessfully Downloaded: ',file_name)
            file_path=os.path.abspath(file_name)
            return file_path
        else:
            return 'image could not be downloaded'    
    elif type == 'audio':
        read_data = requests.get(url,headers=hed,stream=True)
        read_data.raw.decode=True
        
    
        if read_data.status_code == 200:
            with open(file_name+'.mp3','wb') as f2:
                shutil.copyfileobj(read_data.raw, f2)
                f2.close()
            #print('audio sucessfully Downloaded: ',file_name)
            file_path=os.path.abspath(file_name)
            return file_path
        else:
            return 'image could not be downloaded'    
    elif type == 'document':
        read_data = requests.get(url,headers=hed,stream=True)
        read_data.raw.decode=True
        
    
        if read_data.status_code == 200:
            with open(file_name+'.pdf','wb') as f2:
                shutil.copyfileobj(read_data.raw, f2)
                f2.close()
            #print('document sucessfully Downloaded: ',file_name)
            file_path=os.path.abspath(file_name)
            return file_path
        else:
            return 'image could not be downloaded'    
 
app = Flask(__name__)
 
# Load .env file
load_dotenv()
 
 
VERIFY_TOKEN = "asanify"
 
@app.route("/webhook", methods=["GET", "POST"])
def hook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Invalid verification token"
 
    data = request.get_json()
    changed_field = messenger.changed_field(data)
    if changed_field == "messages":
        new_message = messenger.get_mobile(data)
        if new_message:
            mobile = messenger.get_mobile(data)
            name = messenger.get_name(data)
            message_type = messenger.get_message_type(data)
            #print(message_type)
            #print(data)
 
            #FOR TEXT MESSAGES
            if message_type == "text":
                #RECIEVE
                got_message=recieve(message_type,data)
                #print(got_message,data)
                
                print(f"{name} with this {mobile} number sent  {got_message}")
                
                #Integrating with rasa
                rasa_message = send_rasa(name,got_message)
              
                     

                #SEND
                for i in rasa_message:
                    send('text',mobile,i['text'])
               
                
            
            #get Location            
            elif message_type == "location":
                
                #RECIEVE
                address =recieve(message_type,data)

                # Integrating with rasa
                rasa_message = send_rasa(name,'location')
                #print(rasa_message)
                #print(address)
                
                
                #SEND
                send('location',mobile,address)
                for i in rasa_message:
                    send('text',mobile,i['text'])
 
               
            #get image
            elif message_type == "image":
                #RECIEVE
                image_data=recieve(message_type,data)[1]
                im_id=recieve(message_type,data)[0]
                print(recieve(message_type,data)[2])
                im_url=image_data['url']
                
                #DOWNLOAD
                download(message_type,im_id,im_url)
                print(download(message_type,im_id,im_url))

                # Integrating with rasa
                rasa_message = send_rasa(name,message_type)
                
                #SEND
                send(message_type,mobile,None,im_id)
                send('text',mobile,'This is the image you sent')
                for i in rasa_message:
                    send('text',mobile,i['text'])
                

            #get document
            elif message_type == "document":
                #RECIEVE
                doc_data=recieve(message_type,data)[1]
                doc_id=recieve(message_type,data)[0]
                print(recieve(message_type,data)[2])
                doc_url=doc_data['url']

                #DOWNLOAD
                download(message_type,doc_id,doc_url)
                print(download(message_type,doc_id,doc_url))

                #SEND
                send(message_type,mobile,None,doc_id)
                send('text',mobile,'This is the document you sent')
                
            #get contact
            elif message_type == "contacts":
                contact_info=str(recieve(message_type,data))
                print(contact_info)
                send('text',mobile,contact_info)   
               
            #get_audio
            elif message_type == "audio":
                #RECIEVE
                aud_data=recieve(message_type,data)[1]
                aud_id=recieve(message_type,data)[0]
                print(recieve(message_type,data)[2])
                aud_url=aud_data['url']

                #DOWNLOAD
                download(message_type,aud_id,aud_url)
                print(download(message_type,aud_id,aud_url))

                #SEND
                send(message_type,mobile,None,aud_id)
                send('text',mobile,'This is the audio you sent')

            #get_vedio
            elif message_type == "video":
                #RECIEVE
                ved_data=recieve(message_type,data)[1]
                ved_id=recieve(message_type,data)[0]
                print(recieve(message_type,data)[2])
                ved_url=ved_data['url']

                #DOWNLOAD
                download(message_type,ved_id,ved_url)
                print(download(message_type,ved_id,ved_url))

                #SEND 
                send(message_type,mobile,None,ved_id)
                send('text',mobile,'This is the video you sent')
                           
 
 
 
 
                                   
 
            elif message_type == "interactive":
                message_response = messenger.get_interactive_response(data)
                print(message_response)
 
            else:
                pass
        else:
            delivery = messenger.get_delivery(data)
            if delivery:
                print(f"Message : {delivery}")
            else:
                print("No new message")
    return "ok"
 
 
if __name__ == "__main__":
    #USER INPUT
    try:
        user_input = inputimeout(prompt='You have 10 seconds to type "Y" or "N"---->', timeout=10)
    except TimeoutOccurred:
        user_input = 'N'
        print('Lets move ahead')
    
    if user_input=='Y':
        message_type = input('enter message type')
        to=input('enter number preceeded by 91')
        send(message_type, to)
    else:
        pass 
    
    #CLIENT INPUT
    app.run(port=5002, debug=True)
    
