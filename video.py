import threading
import vlc
import time
import os


class ShowVideo(threading.Thread):
    def __init__(self, path_file):
        threading.Thread.__init__(self)
        self.path_file = path_file

    def run(self):
        self.media = vlc.MediaPlayer(os.getcwd()+'/birthday.mp4')
        self.media.play()
        while (True):
            time.sleep(1)
            if not self.media.is_playing():
                self.media.stop()
                break
