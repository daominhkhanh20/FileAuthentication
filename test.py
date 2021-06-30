with open('video5.mp4','rb') as file:
    data=file.read()
size=2048+100
n_sample=len(data)//size
chunk=None
for i in range(n_sample):
    temp=data[i*size:min(len(data),(i+1)*size)]
    if chunk is None:
        chunk=temp[:-100]
    else:
        chunk=chunk+temp[:-100]

if len(data)-size*n_sample>0:
    temp=data[size*n_sample:]
    chunk=chunk+temp[-100:]

with open('video3.mp4',"wb") as file:
    file.write(chunk)