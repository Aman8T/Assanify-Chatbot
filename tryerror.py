import os
import requests
import shutil
def get_media(media_url, temp_access_token,file_name,specify_path=None):
    hed = {'Authorization': 'Bearer ' + Temp_access_token}
    read_data = requests.get(url,headers=hed,stream=True)
    read_data.raw.decode=True
    print(read_data)
    
    if read_data.status_code == 200:
        with open(file_name+'.pdf','wb') as f2:
            shutil.copyfileobj(read_data.raw, f2)
            f2.close()
        print('Image sucessfully Downloaded: ',file_name)
        file_path=os.path.abspath(file_name)
        print(file_path)


    else:
        print('Image Couldn\'t be retrieved')


url='https://lookaside.fbsbx.com/whatsapp_business/attachments/?mid=777471923248561&ext=1654776438&hash=ATsR_VZC2A_Kq7iF0qEplde0g6Aj8uITx_lf5oq3vu21hw'
file_name ='Bits_ID_Card' #prompt user for file_name
Temp_access_token='EAAEdqkBTO0YBALMxae3kAFjNDxBZBFpBsZAyrxuhOsac3WBFGWHmXZCVmyifTwybNgTXGgPthNn7jgsgu525YAZBXlUEPpvGuOiJXtuxG2vS3akZAPw7so6q70ZCxn9Ta3lVKAH5Eip2388ZA5gJ6l1qF10QOWvp7AGUW8OVOEwyT8lZCcIn7KyC1prDwZA37uqSf365FzBhs2gZDZD'
get_media(url,Temp_access_token,file_name)