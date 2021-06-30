from mysql.connector.constants import ServerCmd
import requests 
from hash import Hash
from database import Database

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
                break
    
    def check_file(self,path_file,file_name):
        h0=self.database.get_h0(file_name)
        print(h0)
        print("Time read data")
        with open(path_file,'rb') as file:
            data=file.read()
        print('Time check')
        n_blocks=len(data)//self.chunk_size+1
        hash_code_block=h0
        for i in range(n_blocks):
            temp=data[self.chunk_size*i:min(len(data),self.chunk_size*(i+1))]
            if hash_code_block==self.hash.hash_code(temp):
                hash_code_block=temp[-32:]
                # if chunk is None:
                #     chunk=temp[:1024]
                # else:
                #     chunk=chunk+temp[:1024]
            else:
                return False
        # with open('/home/daominhkhanh/Documents/ATTT/Authentication/VideoDownload/{}'.format(file_name),'wb') as file:
        #     file.write(chunk)

        return True

# check=Security()
# if check.check_file('/home/daominhkhanh/Documents/ATTT/Authentication/VideoConcat/kk.mp4','birthday_concat.mp4'):
#     print("Success")
# else:
#     print("Error")

        
