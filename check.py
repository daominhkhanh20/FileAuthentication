from mysql.connector.constants import ServerCmd
import requests
from hash import Hash
from database import Database
from video import ShowVideo
from elgamal.elgamal import Elgamal,CipherText
import os 

class Security:
    def __init__(self):
        self.database=Database()
        self.hash=Hash()
        self.chunk_size=self.hash.size_block+32
        self.path=os.getcwd()
    
    def download(self,url,a,b,private_key):
        cipher=CipherText(a,b)
        h0=bytes(Elgamal.decrypt(cipher,private_key))
        # print(h0)
        # print(url)
        response=requests.get(url,stream=True)
        hash_code_block=h0
        fw = open(os.path.join(self.path,'a.mp4'), 'wb')
        for i,chunk in enumerate(response.iter_content(chunk_size=self.chunk_size)):
            print(len(chunk))
            if(hash_code_block==self.hash.hash_code(chunk)):
                chunks = []
                chunks.append(chunk[:992])
                chunk_block = b''.join(chunks)
                fw.write(chunk_block)
                #fw.close()
                if i == 2000:
                    thread = ShowVideo(os.path.join(self.path,'a.mp4'))
                    thread.start()
                hash_code_block=chunk[-32:]
            else:
                print("Error file")
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

        return True
