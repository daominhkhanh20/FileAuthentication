from Crypto.Hash import SHA256
from database import Database
import time 
class Hash:
    def __init__(self,size_block=1024):
        self.size_block=size_block

    def hash_code(self,message):
        self.hash_function=SHA256.new()
        self.hash_function.update(message)
        return self.hash_function.digest()

    
    def hash_file(self,database,path_video):
        with open(path_video,'rb') as file:
            data=file.read()
        
        n_block=len(data)//self.size_block +1
        video_data=None
        hash_code_block=None
        for i in range(n_block,0,-1):
            temp=data[self.size_block*(i-1):min(len(data),self.size_block*i)]
            if hash_code_block is None:
                hash_code_block=self.hash_code(temp)
            else:
                hash_code_block_new=self.hash_code(temp+hash_code_block)
                
            if video_data is None:
                video_data=temp
            else:
                video_data=temp+hash_code_block+video_data
                hash_code_block=hash_code_block_new

        file_name=path_video[path_video.rfind('/')+1:]
        name=file_name[:file_name.find(".")]
        file_name=name+'_concat.mp4'
        new_path='/home/daominhkhanh/Documents/ATTT/Authentication/VideoConcat/'+file_name
        with open(new_path,'wb') as file:
            file.write(video_data)
        
        database.insert_file(file_name=file_name,file_path=new_path,h0=hash_code_block)

        
# hash=Hash()
# db=Database()
# start_time=time.time()
# hash.hash_file(db,'/home/daominhkhanh/Documents/ATTT/Authentication/Video/birthday.mp4')
# print("{}s".format(time.time()-start_time))