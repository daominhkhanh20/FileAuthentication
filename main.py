import requests
import os 
url="https://drive.google.com/uc?export=download&id=1uhtGwqLceXQzCD_kR0BcnrNIgB4M8ZL4"
response=requests.get(url,stream=True)
data_file=open('/home/daominhkhanh/Documents/ATTT/Authentication/video5.mp4','wb')
temp=0
n_chunk=0
for chunk in response.iter_content(chunk_size=1024+32):
    data_file.write(chunk)
    temp+=len(chunk)
    n_chunk+=1
print(n_chunk)
print(temp)
data_file.close()

