from mysql.connector.constants import ServerCmd
import requests
from hash import Hash
from database import Database
import time 
import argparse

parser=argparse.ArgumentParser()
parser.add_argument('--url',type=str,required=False,help='link to download')
parser.add_argument('--path_file',type=str,required=False,help='path to file concat')
parser.add_argument('--file_name',type=str,required=False)
parser.add_argument('--file_name_saved',type=str,required=False)
arg=parser.parse_args()

class Security:
    def __init__(self):
        self.database=Database()
        self.hash=Hash()
        self.chunk_size=self.hash.size_block+32
    
    def download(self,url,h0):
        response=requests.get(url,stream=True)
        hash_code_block=h0
        print(h0)
        for i,chunk in enumerate(response.iter_content(chunk_size=self.chunk_size)):
            if(hash_code_block==self.hash.hash_code(chunk)):
                hash_code_block=chunk[-32:]
                temp=chunk[:-32]
            else:
                print("Error file")
                #print(chunk)
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
        
        # chunk=b''.join(chunk)
        # with open('/home/daominhkhanh/Documents/ATTT/Authentication/VideoDownload/{}'.format(file_name_saved),'wb') as file:
        #     file.write(chunk)

        return True

if __name__=='__main__':
    check=Security()
    start_time=time.time()
    if arg.path_file is not None:
        if check.check_file(arg.path_file,arg.file_name_saved):
            print("Success")
        else:
            print("Error")
    elif arg.url is not None:
        h0=check.database.get_h0(arg.file_name)
        if check.download(arg.url,h0) is True:
            print("Success")
        else:
            print("Failed")
    print(f"Time:{time.time()-start_time}")

'''
python3 check1.py --url 'https://dl.dropboxusercontent.com/s/tvhxrghpbrv94qr/video_concat.mp4?dl=0' --file_name 'video_concat.mp4'
python3 check.py --path_file '/home/daominhkhanh/Documents/ATTT/Authentication/VideoConcat/birthday_concat.mp4' --file_name_saved 'video.mp4'
'''
#https://dl.dropboxusercontent.com/s/ermco3yn3gtece4/birthday_concat.mp4?dl=0