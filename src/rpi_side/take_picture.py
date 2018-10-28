#coding:utf-8

import subprocess as sp
import time
from datetime import datetime
from pathlib import Path

class AutoTakePictures:
    def __init__(self,save_dir="./campic"):
        self.save_dir = Path(save_dir)
        if self.save_dir.exists() is False:
            self.save_dir.mkdir()

    def sendServer(self,server,user,key):
        cmd = "scp -i {key} -r {savedir} {user}@{server}:~/picture_sender_app/static/".format(key=key,savedir=self.save_dir,user=user,server=server)
        print(cmd)
        sp.call(cmd.split())
        
    def capture(self):
        cmd = "fswebcam -r 2560x1920 {savedir}/image_{date}.jpg".format(savedir=self.save_dir,date=datetime.now().strftime('%Y%m%d_%H%M%S'))
        print(cmd)
        sp.call(cmd.split())
        time.sleep(5)

    def delete(self):
        target_files = self.save_dir.glob("*.jpg")
        list(map(lambda x:x.unlink(),target_files))

if __name__ == '__main__':
    picture = AutoTakePictures(save_dir="./campic")
    picture.capture()
    
