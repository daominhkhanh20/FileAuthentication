#from mysql.connector.constants import ServerCmd
import requests

#import test
from hash import Hash,ElgamalCrypto
#from database import Database
import time
import argparse
import vlc
import threading


parser=argparse.ArgumentParser()
parser.add_argument('--url',type=str,required=False,help='link to download')
parser.add_argument('--path_file',type=str,required=False,help='path to file concat')
parser.add_argument('--file_name',type=str,required=False)
parser.add_argument('--file_name_saved',type=str,required=False)
arg=parser.parse_args()


class show_video(threading.Thread):
    def __init__(self, path_file):
        threading.Thread.__init__(self)
        self.path_file = path_file

    def run(self):
        media = vlc.MediaPlayer('/home/daominhkhanh/Documents/ATTT/Authentication/a.mp4')
        media.play()
        # while (True):
        #     time.sleep(1)
        #     if not media.is_playing():
        #         media.stop()
        #         break


class Security:
    def __init__(self):
        #self.database=Database()
        self.hash = Hash()
        self.chunk_size = self.hash.size_block+32
        self.elgama=ElgamalCrypto()
    
    def download(self,url,public_key,private_key):
        hash_code_block=h0
        print(h0)
        url1=url+'public_key='+public_key
        h0_encode=requests.get(url1,stream=True)
        h0=self.elgama.decode(h0_encode,private_key)
        h0=bytes(h0)
        
        hash_code_block=h0
        response=requests.get(url,stream=True)
        fw = open('/home/daominhkhanh/Documents/ATTT/Authentication/a.mp4', 'wb')
        for i,chunk in enumerate(response.iter_content(chunk_size=self.chunk_size)):
            print(i)
            if hash_code_block != self.hash.hash_code(chunk):
                print("Error file")
                print(chunk)
                print(i)
                return False
            else:
                chunks = []
                chunks.append(chunk[:992])
                chunk_block = b''.join(chunks)
                fw.write(chunk_block)
                #fw.close()
                if i == 2000:
                    thread = show_video('/home/daominhkhanh/Documents/ATTT/Authentication/a.mp4')
                    thread.start()
                hash_code_block=chunk[-32:]
        return True
    
    def check_file(self,path_file,file_name_saved):
        file_name=path_file[path_file.rfind('/')+1:]
        # h0=self.database.get_h0(file_name)
        h0 = b"\x8dP\xe1\t\n}\x8c\xf8\xe8T\xcb'\x8c +\xfd\xa7%\x1dln\x0c&'5a&\x17'>M\xff"
        with open(path_file,'rb') as file:
            data=file.read()
        n_blocks=len(data)//self.chunk_size+1
        hash_code_block=h0
        chunk=[]

        #fw = open('/home/winner/Desktop/FileAuthentication/a.mp4','wb')

        for i in range(n_blocks):
            temp=data[self.chunk_size*i:min(len(data),self.chunk_size*(i+1))]
            if hash_code_block==self.hash.hash_code(temp):
                hash_code_block=temp[-32:]
                chunk = []
                chunk.append(temp[:992])
                # ADD TO PLAY VIDEO ith-block
                chunk_block = b''.join(chunk)
                #fw.write(chunk_block)
                # if i == 2:
                #     thread = show_video('/home/winner/Desktop/FileAuthentication/a.mp4')
                #     thread.start()
            else:
                return False
        
        #chunk=b''.join(chunk)
        # with open('/home/winner/Desktop/FileAuthentication/VideoDownload/{}'.format(file_name_saved),'wb') as file:
        #     file.write(chunk)
        return True


if __name__ == '__main__':
    check=Security()
    start_time=time.time()
    if arg.path_file is not None:
        if check.check_file(arg.path_file,arg.file_name_saved):
            print("Success")
        else:
            print("Error")
    elif arg.url is not None:
        #h0 = check.database.get_h0(arg.file_name)
        h0 = b"\x8dP\xe1\t\n}\x8c\xf8\xe8T\xcb'\x8c +\xfd\xa7%\x1dln\x0c&'5a&\x17'>M\xff"
        if check.download(arg.url,h0) is True:
            print("Success")
        else:
            print("Failed")
    #print(f"Time:{time.time()-start_time}")

'''
python3 check.py --url 'https://dl.dropboxusercontent.com/s/tvhxrghpbrv94qr/video_concat.mp4?dl=0' --file_name 'video_concat.mp4'
python3 check.py --path_file '/home/winner/Desktop/FileAuthentication/VideoConcat/birthday_concat.mp4' --file_name_saved 'video.mp4'
'''
