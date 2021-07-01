import requests
import os 
url="https://dl.dropboxusercontent.com/s/5ahdou3su4ubsgw/birthday.mp4?dl=0"
response=requests.get(url,stream=True)
data_file=open('/home/daominhkhanh/Documents/ATTT/Authentication/video5.mp4','wb')
for chunk in response.iter_content(chunk_size=2048):
    temp=os.urandom(100)
    chunk=chunk+temp
    print(len(chunk))
    data_file.write(chunk)


data_file.close()

