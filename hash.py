from Crypto.Hash import SHA256
from database import Database
import time 
from elgamal.elgamal import Elgamal

from elgamal.elgamal import Elgamal

class ElgamalCrypto:
    def __init__(self,n_bits=128):
        self.n_bits=n_bits

    def gen_key(self):
        pb,pv=Elgamal.newkeys(self.n_bits)
        return pb,pv

    def encode(self,message,public_key):
        return Elgamal.encrypt(message,public_key)

    def decode(self,message,private_key):
        return Elgamal.decrypt(message,private_key)


class Hash:
    def __init__(self,size_block=992):
        self.size_block=size_block

    def hash_code(self,message):
        self.hash_function=SHA256.new()
        self.hash_function.update(message)
        return self.hash_function.digest()

    
    def hash_file(self,database,path_video):
        with open(path_video,'rb') as file:
            data=file.read()
        
        n_block=len(data)//self.size_block +1
        video_data=[]
        hash_code_block=None
        for i in range(n_block,0,-1):
            temp=data[self.size_block*(i-1):min(len(data),self.size_block*i)]
            if hash_code_block is None:
                hash_code_block=self.hash_code(temp)
            else:
                hash_code_block_new=self.hash_code(temp+hash_code_block)
                
            if len(video_data)==0:
                video_data.append(temp)
            else:
                video_data.append(temp+hash_code_block)
                hash_code_block=hash_code_block_new

        file_name=path_video[path_video.rfind('/')+1:]
        name=file_name[:file_name.find(".")]
        file_name=name+'_concat.mp4'
        new_path='/media/daominhkhanh/D:/Data/Project/FileAuthentication/VideoConcat/'+file_name
        video_data.reverse()
        video_data=b''.join(video_data)
        with open(new_path,'wb') as file:
            file.write(video_data)
        
        #database.insert_file(file_name=file_name,file_path=new_path,h0=hash_code_block)

        
# hash=Hash()
# db=Database()
# start_time=time.time()
# hash.hash_file(db,'/media/daominhkhanh/D:/Data/Project/FileAuthentication/birth_day_error.mp4')
# print("{}s".format(time.time()-start_time))