import os
#os.system('mpg321 beepA.mp3 &')
beepAPath = 'beepA.mp3'
#os.system(f"XDG_RUNTIME_DIR=/home/pi/Documents/python/lostClock paplay {beepAPath}")
os.system('omxplayer  --no-keys --vol -100 /home/pi/Documents/python/lostClock/beepA.mp3 &')