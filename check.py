from mysql.connector.constants import ServerCmd
import requests 
from hash import Hash
from database import Database
import time 
class Security:
    def __init__(self):
        self.database=Database()
        self.hash=Hash()
        self.chunk_size=self.hash.size_block+32
    
    def download(self,url,h0):
        response=requests.get(url,stream=True)
        hash_code_block=h0
        for i,chunk in enumerate(response.iter_content(chunk_size=self.chunk_size)):
            if(hash_code_block==self.hash.hash_code(chunk)):
                hash_code_block=chunk[-32:]
            else:
                print("Error file")
                print(chunk)
                print(i)
                return False
        return True
    
    def check_file(self,path_file,file_name_saved):
        file_name=path_file[path_file.rfind('/')+1:]
        h0=self.database.get_h0(file_name)
        with open(path_file,'rb') as file:
            data=file.read()
        n_blocks=len(data)//self.chunk_size+1
        hash_code_block=h0
        chunk=[]
        for i in range(n_blocks):
            temp=data[self.chunk_size*i:min(len(data),self.chunk_size*(i+1))]
            if hash_code_block==self.hash.hash_code(temp):
                hash_code_block=temp[-32:]
                chunk.append(temp[:992])
            else:
                return False
        
        chunk=b''.join(chunk)
        with open('/home/daominhkhanh/Documents/ATTT/Authentication/VideoDownload/{}'.format(file_name_saved),'wb') as file:
            file.write(chunk)

        return True

check=Security()
# if check.check_file('/home/daominhkhanh/Documents/ATTT/Authentication/VideoConcat/video_concat.mp4','video_concat.mp4'):
#     print("Success")
# else:
#     print("Error")
start_time=time.time()
h0=check.database.get_h0('video_concat.mp4')
if check.download('https://dl.dropboxusercontent.com/s/tvhxrghpbrv94qr/video_concat.mp4?dl=0',h0) is True:
    print("Success")
else:
    print("Failed")
print(f"Time:{time.time()-start_time}")

        