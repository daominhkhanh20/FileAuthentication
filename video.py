import threading
import vlc
import time


class ShowVideo(threading.Thread):
    def __init__(self, path_file):
        threading.Thread.__init__(self)
        self.path_file = path_file

    def run(self):
        media = vlc.MediaPlayer('/home/winner/Desktop/FileAuthentication/a.mp4')
        media.play()
        while (True):
            time.sleep(1)
            if not media.is_playing():
                media.stop()
                break