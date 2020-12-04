import re
import os
import sys
import threading

this = sys.modules[__name__]

serialRegEx = re.compile(' serial=[0-9]+')

active = False
mySerial = ''
pixmapSerial = ''
waitForPixmap = False
insidePixmap = False
aktuellPixmap = ''
inAktuellerPixmap = False
cmdUp = None
cmdDown = None

blinkShouldBeOn = False
threadLock = threading.Lock()

class myBlinkThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global threadLock, blinkShouldBeOn
        global cmdUp, cmdDown
        blinkIsOn = False
        print("Thread started")
        while True:
            threadLock.acquire(1)
            print("Thread "+str(blinkShouldBeOn)+" "+str(blinkIsOn))
            if blinkShouldBeOn and not blinkIsOn:
                if cmdUp is not None:
                    os.system(cmdUp)
                blinkIsOn = True
            elif not blinkShouldBeOn and blinkIsOn:
                if cmdDown is not None:
                    os.system(cmdDown)
                blinkIsOn = False
        
threadLock.acquire(1)
thread = None

# A ist ohne notification
pixmapA = "00 00 00 00 00 00 00 00 00 00 00 00 0c 55 aa ff 6d 54 a1 fd c1 55 a3 fe f2 54 a2 fe fe 55 a3 fe ff 55 a2 fe ff 55 a2 fe ff 55 a2 fe ff 55 a2 fe ff 55 a2 fe ff 55 a2 fe fe 55 a3 fe f2 54 a2 fe c1 55 a3 fe 6d 54 a1 fd 0c 55 aa ff 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 3c 51 9d fb dc 53 a1 ff fe 54 a1 fe ff 54 a0 fe ff 54 a0 fe ff 54 a0 fe ff 54 a0 fe ff 54 a0 fe ff 54 a0 fe ff 54 a0 fe ff 54 a0 fe ff 54 a0 fe ff 54 a0 fe ff 54 a0 fe ff 54 a0 fe fe 54 a1 fe dc 53 a1 fe 3b 52 a0 ff 00 00 00 00 00 00 00 00 00 00 00 00 3c 51 9d fb f0 53 9f fe ff 53 9f fe ff 53 9f fe ff 53 9f fe ff 53 9f fe ff 53 9f fe ff 53 9f fe ff 53 9f fe ff 53 9f fe ff 53 9f fe ff 53 9f fe ff 53 9f fe ff 53 9f fe ff 53 9f fe ff 53 9f fe ff 53 9f fe ff 53 9f fe f0 53 9f fe 3b 52 a0 ff 00 00 00 00 0c 40 95 ff dc 51 9e fe ff 51 9d fd ff 51 9d fd ff 51 9d fd ff 51 9d fd ff 51 9d fd ff 51 9d fd ff 51 9d fd ff 51 9d fd ff 51 9d fd ff 51 9d fd ff 51 9d fd ff 51 9d fd ff 51 9d fd ff 51 9d fd ff 51 9d fd ff 51 9d fd ff 51 9d fd ff 51 9d fd dc 51 9e fe 0c 40 95 ff 6d 50 9a fd fe 50 9c fd ff 50 9b fd ff 50 9b fd ff 50 9b fd ff 50 9b fd ff 50 9b fd ff 50 9b fd ff 50 9b fd ff 50 9b fd ff 50 9b fd ff 50 9b fd ff 50 9b fd ff 50 9b fd ff 50 9b fd ff 50 9b fd ff 50 9b fd ff 50 9b fd ff 50 9b fd ff 50 9b fd fe 50 9c fd 6d 50 9a fd c1 4f 9b fc ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd c1 4f 9b fc f2 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd f1 4e 99 fd fe 4c 98 fd ff 4d 97 fd ff 4d 97 fd ff 4d 97 fd ff 8b bb fd ff d2 e4 fd ff d4 e5 fd ff d4 e5 fd ff d4 e5 fd ff d4 e5 fd ff d3 e5 fd ff cf e2 fd ff ae cf fd ff 59 9e fd ff 4d 97 fd ff 4e 98 fd ff 82 b6 fd ff 91 bf fd ff 4d 97 fd ff 4d 97 fd ff 4d 97 fd fe 4c 98 fd ff 4b 95 fd ff 4b 95 fd ff 4b 95 fd ff 4b 95 fd ff c8 de fd ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff bd d8 fd ff 4f 97 fd ff 9e c6 fd ff f8 fb fe ff c9 df fd ff 4b 95 fd ff 4b 95 fd ff 4b 95 fd ff 4b 95 fd ff 4a 94 fd ff 4a 94 fd ff 4a 94 fd ff 4a 94 fd ff c8 de fd ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff e6 f0 fd ff 91 be fd ff fc fd fd ff fe fe fe ff c9 df fd ff 4a 94 fd ff 4a 94 fd ff 4a 94 fd ff 4a 94 fd ff 49 92 fd ff 49 92 fd ff 49 92 fd ff 49 92 fd ff c8 de fd ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff ea f2 fd ff ae ce fd ff fe fe fe ff fe fe fe ff c9 de fd ff 49 92 fd ff 49 92 fd ff 49 92 fd ff 49 92 fd ff 48 91 fc ff 48 91 fc ff 48 91 fc ff 48 91 fc ff c7 dd fd ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff eb f3 fd ff ae ce fd ff fe fe fe ff fe fe fe ff c9 de fd ff 48 91 fc ff 48 91 fc ff 48 91 fc ff 48 91 fc ff 47 8f fc ff 47 8f fc ff 47 8f fc ff 47 8f fc ff c0 d9 fd ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff eb f2 fd ff 90 bb fc ff fc fc fd ff fe fe fe ff c8 dd fd ff 47 8f fc ff 47 8f fc ff 47 8f fc ff 47 8f fc ff 46 8e fc ff 46 8e fc ff 46 8e fc ff 46 8e fc ff 8f ba fc ff fc fd fd ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff ea f2 fd ff 51 95 fc ff 98 c0 fc ff f8 fa fd ff c7 dc fd ff 46 8e fc ff 46 8e fc ff 46 8e fc ff 46 8e fc fe 44 8d fc ff 44 8c fc ff 44 8c fc ff 44 8c fc ff 48 8e fc ff 90 ba fc ff c6 db fd ff cd e0 fd ff cf e1 fd ff cf e1 fd ff cf e1 fd ff cf e1 fd ff cf e1 fd ff a3 c6 fd ff 47 8d fc ff 45 8d fc ff 79 ac fc ff 8a b6 fc ff 44 8c fc ff 44 8c fc ff 44 8c fc fe 44 8d fc f2 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc f1 44 8b fc c1 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc c1 42 89 fb 6d 42 88 fd fe 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc fe 41 88 fc 6d 3f 88 fa 0c 40 80 ff dc 40 86 fc ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb dc 40 86 fc 0c 40 80 ff 00 00 00 00 3b 3d 86 ff f0 3f 85 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb f0 3f 85 fb 3b 3d 86 fb 00 00 00 00 00 00 00 00 00 00 00 00 3c 3b 84 fb dc 3d 83 fc fe 3d 84 fb ff 3d 83 fb ff 3d 83 fb ff 3d 83 fb ff 3d 83 fb ff 3d 83 fb ff 3d 83 fb ff 3d 83 fb ff 3d 83 fb ff 3d 83 fb ff 3d 83 fb ff 3d 83 fb ff 3d 83 fb fe 3d 84 fb dc 3d 83 fc 3b 3d 82 fb 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 0c 40 80 ff 6d 3d 81 fa c1 3d 81 fb f1 3c 81 fb fe 3c 82 fb ff 3c 81 fb ff 3c 81 fb ff 3c 81 fb ff 3c 81 fb ff 3c 81 fb ff 3c 81 fb fe 3c 82 fb f1 3c 81 fb c1 3d 81 fb 6d 3d 81 fa 0c 2a 80 ff 00 00 00 00 00 00 00 00 00 00 00 00"
# B ist mit 5 notifications...vermutlich
pixmapB = "00 00 00 00 00 00 00 00 00 00 00 00 0c 55 aa ff 6d 54 a1 fd c1 55 a3 fe f2 54 a2 fe fe 55 a3 fe ff 55 a2 fe ff 55 a2 fe ff 55 a2 fe ff 55 a2 fe ff 49 61 98 ff 7b 2a 41 ff a7 00 00 ff a7 00 00 f1 a2 00 00 9c 71 00 00 2c 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 3c 51 9d fb dc 53 a1 ff fe 54 a1 fe ff 54 a0 fe ff 54 a0 fe ff 54 a0 fe ff 54 a0 fe ff 54 a0 fe ff 4c 91 e5 ff 8d 18 25 ff f6 00 00 ff ff 00 00 ff ff 00 00 ff ff 00 00 ff ff 00 00 ff fe 00 00 fb d3 00 00 8d 74 00 00 00 00 00 00 00 00 00 00 00 00 00 00 3c 51 9d fb f0 53 9f fe ff 53 9f fe ff 53 9f fe ff 53 9f fe ff 53 9f fe ff 53 9f fe ff 53 9f fe ff 4c 8e e3 ff a6 17 25 ff ff 00 00 ff ff 18 18 ff ff 3f 3f ff ff 3f 3f ff ff 3f 3f ff ff 3f 3f ff ff 1b 1b ff ff 00 00 fe f4 00 00 8d 74 00 00 00 00 00 00 0c 40 95 ff dc 51 9e fe ff 51 9d fd ff 51 9d fd ff 51 9d fd ff 51 9d fd ff 51 9d fd ff 51 9d fd ff 50 9b fa ff 7f 27 3f ff ff 00 00 ff ff 00 00 ff ff 63 63 ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff 6f 6f ff ff 00 00 ff ff 00 00 fe f1 00 00 5b 30 00 00 6d 50 9a fd fe 50 9c fd ff 50 9b fd ff 50 9b fd ff 50 9b fd ff 50 9b fd ff 50 9b fd ff 50 9b fd ff 45 75 be ff dd 00 00 ff ff 00 00 ff ff 00 00 ff ff 63 63 ff ff ff ff ff ff 52 52 ff ff 31 31 ff ff 31 31 ff ff 15 15 ff ff 00 00 ff ff 00 00 ff ff 00 00 d5 97 00 00 c1 4f 9b fc ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 5d 41 6a ff ff 00 00 ff ff 00 00 ff ff 00 00 ff ff 63 63 ff ff ff ff ff ff d2 d2 ff ff cd cd ff ff 8f 8f ff ff 15 15 ff ff 00 00 ff ff 00 00 ff ff 00 00 ff d3 00 00 f2 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 7b 26 3f ff ff 00 00 ff ff 00 00 ff ff 00 00 ff ff 53 53 ff ff a5 a5 ff ff 86 86 ff ff c4 c4 ff ff fe fe ff ff aa aa ff ff 00 00 ff ff 00 00 ff ff 00 00 ff ff 00 00 fe 4c 98 fd ff 4d 97 fd ff 4d 97 fd ff 4d 97 fd ff 8b bb fd ff d2 e4 fd ff d4 e5 fd ff d4 e5 fd ff 9c 39 3f ff ff 00 00 ff ff 00 00 ff ff 00 00 ff ff 00 00 ff ff 00 00 ff ff 00 00 ff ff 1b 1b ff ff ec ec ff ff e5 e5 ff ff 0b 0b ff ff 00 00 ff ff 00 00 ff ff 00 00 ff 4b 95 fd ff 4b 95 fd ff 4b 95 fd ff 4b 95 fd ff c8 de fd ff fe fe fe ff fe fe fe ff fe fe fe ff a6 62 62 ff ff 00 00 ff ff 00 00 ff ff 00 00 ff ff 5c 5c ff ff 34 34 ff ff 11 11 ff ff 5c 5c ff ff f8 f8 ff ff d3 d3 ff ff 03 03 ff ff 00 00 ff ff 00 00 ff db 00 00 ff 4a 94 fd ff 4a 94 fd ff 4a 94 fd ff 4a 94 fd ff c8 de fd ff fe fe fe ff fe fe fe ff fe fe fe ff c1 b7 b7 ff e4 00 00 ff ff 00 00 ff ff 00 00 ff ff a0 a0 ff ff fb fb ff ff fb fb ff ff fd fd ff ff ea ea ff ff 4b 4b ff ff 00 00 ff ff 00 00 ff ff 00 00 ff 90 13 20 ff 49 92 fd ff 49 92 fd ff 49 92 fd ff 49 92 fd ff c8 de fd ff fe fe fe ff fe fe fe ff fe fe fe ff f9 f9 f9 ff ac 31 31 ff ff 00 00 ff ff 00 00 ff ff 02 02 ff ff 2d 2d ff ff 4a 4a ff ff 42 42 ff ff 10 10 ff ff 00 00 ff ff 00 00 ff ff 00 00 ff f9 00 00 ff 43 55 92 ff 48 91 fc ff 48 91 fc ff 48 91 fc ff 48 91 fc ff c7 dd fd ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff dd da da ff c8 18 18 ff ff 00 00 ff ff 00 00 ff ff 00 00 ff ff 00 00 ff ff 00 00 ff ff 00 00 ff ff 00 00 ff ff 00 00 ff fa 00 00 ff 69 34 5b ff 48 91 fc ff 47 8f fc ff 47 8f fc ff 47 8f fc ff 47 8f fc ff c0 d9 fd ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff dd da da ff b1 18 18 ff fc 00 00 ff ff 00 00 ff ff 00 00 ff ff 00 00 ff ff 00 00 ff ff 00 00 ff df 00 00 ff 6b 35 5d ff 46 8e f9 ff 47 8f fc ff 46 8e fc ff 46 8e fc ff 46 8e fc ff 46 8e fc ff 8f ba fc ff fc fd fd ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff f3 f3 f3 ff a9 80 80 ff ad 2f 2f ff bf 00 00 ff bf 00 00 ff bb 09 09 ff 90 3c 4a ff 3d 69 bb ff 44 8b f8 ff 46 8e fc ff 46 8e fc fe 44 8d fc ff 44 8c fc ff 44 8c fc ff 44 8c fc ff 48 8e fc ff 90 ba fc ff c6 db fd ff cd e0 fd ff cf e1 fd ff cf e1 fd ff cf e1 fd ff cf e1 fd ff cf e1 fd ff 9f c1 f7 ff 3f 80 e4 ff 3e 7f e4 ff 67 9a e8 ff 8a b6 fc ff 44 8c fc ff 44 8c fc ff 44 8c fc fe 44 8d fc f2 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc f1 44 8b fc c1 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc c1 42 89 fb 6d 42 88 fd fe 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc fe 41 88 fc 6d 3f 88 fa 0c 40 80 ff dc 40 86 fc ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb dc 40 86 fc 0c 40 80 ff 00 00 00 00 3b 3d 86 ff f0 3f 85 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb f0 3f 85 fb 3b 3d 86 fb 00 00 00 00 00 00 00 00 00 00 00 00 3c 3b 84 fb dc 3d 83 fc fe 3d 84 fb ff 3d 83 fb ff 3d 83 fb ff 3d 83 fb ff 3d 83 fb ff 3d 83 fb ff 3d 83 fb ff 3d 83 fb ff 3d 83 fb ff 3d 83 fb ff 3d 83 fb ff 3d 83 fb ff 3d 83 fb fe 3d 84 fb dc 3d 83 fc 3b 3d 82 fb 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 0c 40 80 ff 6d 3d 81 fa c1 3d 81 fb f1 3c 81 fb fe 3c 82 fb ff 3c 81 fb ff 3c 81 fb ff 3c 81 fb ff 3c 81 fb ff 3c 81 fb ff 3c 81 fb fe 3c 82 fb f1 3c 81 fb c1 3d 81 fb 6d 3d 81 fa 0c 2a 80 ff 00 00 00 00 00 00 00 00 00 00 00 00"
# C ist mit 1 rotem Punkt...vermutlich
pixmapC = "00 00 00 00 00 00 00 00 00 00 00 00 0c 55 aa ff 6d 54 a1 fd c1 55 a3 fe f2 54 a2 fe fe 55 a3 fe ff 55 a2 fe ff 55 a2 fe ff 55 a2 fe ff 55 a2 fe ff 55 a2 fe ff 55 a2 fe fe 55 a3 fe f2 54 a2 fe c3 4d 76 b8 d0 93 00 00 ff a7 00 00 f9 a5 00 00 83 5f 00 00 00 00 00 00 00 00 00 00 00 00 00 00 3c 51 9d fb dc 53 a1 ff fe 54 a1 fe ff 54 a0 fe ff 54 a0 fe ff 54 a0 fe ff 54 a0 fe ff 54 a0 fe ff 54 a0 fe ff 54 a0 fe ff 54 a0 fe ff 54 a0 fe ff 54 a0 fe ff 4f 7e c7 ff c4 0b 11 ff ff 00 00 ff ff 00 00 ff ff 00 00 fe fa 00 00 9c 79 00 00 00 00 00 00 3c 51 9d fb f0 53 9f fe ff 53 9f fe ff 53 9f fe ff 53 9f fe ff 53 9f fe ff 53 9f fe ff 53 9f fe ff 53 9f fe ff 53 9f fe ff 53 9f fe ff 53 9f fe ff 53 9f fe ff 53 9f fe ff 79 2a 43 ff ff 00 00 ff ff 00 00 ff ff 00 00 ff ff 00 00 ff ff 00 00 ff db 00 00 0c 40 95 ff dc 51 9e fe ff 51 9d fd ff 51 9d fd ff 51 9d fd ff 51 9d fd ff 51 9d fd ff 51 9d fd ff 51 9d fd ff 51 9d fd ff 51 9d fd ff 51 9d fd ff 51 9d fd ff 51 9d fd ff 51 9d fd ff 91 13 1f ff ff 00 00 ff ff 00 00 ff ff 00 00 ff ff 00 00 ff ff 00 00 ff ff 00 00 6d 50 9a fd fe 50 9c fd ff 50 9b fd ff 50 9b fd ff 50 9b fd ff 50 9b fd ff 50 9b fd ff 50 9b fd ff 50 9b fd ff 50 9b fd ff 50 9b fd ff 50 9b fd ff 50 9b fd ff 50 9b fd ff 50 9b fd ff 86 1d 2f ff ff 00 00 ff ff 00 00 ff ff 00 00 ff ff 00 00 ff ff 00 00 ff ee 00 00 c1 4f 9b fc ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4f 9a fd ff 4d 67 a9 ff df 03 06 ff ff 00 00 ff ff 00 00 ff ff 00 00 ff fd 00 00 ea 85 18 27 f2 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 4e 99 fd ff 55 5e 9b ff b5 0a 10 ff df 00 00 ff da 01 01 ff 79 28 42 f1 49 90 ee fe 4c 98 fd ff 4d 97 fd ff 4d 97 fd ff 4d 97 fd ff 8b bb fd ff d2 e4 fd ff d4 e5 fd ff d4 e5 fd ff d4 e5 fd ff d4 e5 fd ff d3 e5 fd ff cf e2 fd ff ae cf fd ff 59 9e fd ff 4d 97 fd ff 4e 98 fd ff 82 b6 fd ff 89 af e3 ff 3c 76 c5 ff 3d 78 c9 ff 4d 97 fd fe 4c 98 fd ff 4b 95 fd ff 4b 95 fd ff 4b 95 fd ff 4b 95 fd ff c8 de fd ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff bd d8 fd ff 4f 97 fd ff 9e c6 fd ff f8 fb fe ff c9 df fd ff 4b 95 fd ff 4b 95 fd ff 4b 95 fd ff 4b 95 fd ff 4a 94 fd ff 4a 94 fd ff 4a 94 fd ff 4a 94 fd ff c8 de fd ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff e6 f0 fd ff 91 be fd ff fc fd fd ff fe fe fe ff c9 df fd ff 4a 94 fd ff 4a 94 fd ff 4a 94 fd ff 4a 94 fd ff 49 92 fd ff 49 92 fd ff 49 92 fd ff 49 92 fd ff c8 de fd ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff ea f2 fd ff ae ce fd ff fe fe fe ff fe fe fe ff c9 de fd ff 49 92 fd ff 49 92 fd ff 49 92 fd ff 49 92 fd ff 48 91 fc ff 48 91 fc ff 48 91 fc ff 48 91 fc ff c7 dd fd ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff eb f3 fd ff ae ce fd ff fe fe fe ff fe fe fe ff c9 de fd ff 48 91 fc ff 48 91 fc ff 48 91 fc ff 48 91 fc ff 47 8f fc ff 47 8f fc ff 47 8f fc ff 47 8f fc ff c0 d9 fd ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff eb f2 fd ff 90 bb fc ff fc fc fd ff fe fe fe ff c8 dd fd ff 47 8f fc ff 47 8f fc ff 47 8f fc ff 47 8f fc ff 46 8e fc ff 46 8e fc ff 46 8e fc ff 46 8e fc ff 8f ba fc ff fc fd fd ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff fe fe fe ff ea f2 fd ff 51 95 fc ff 98 c0 fc ff f8 fa fd ff c7 dc fd ff 46 8e fc ff 46 8e fc ff 46 8e fc ff 46 8e fc fe 44 8d fc ff 44 8c fc ff 44 8c fc ff 44 8c fc ff 48 8e fc ff 90 ba fc ff c6 db fd ff cd e0 fd ff cf e1 fd ff cf e1 fd ff cf e1 fd ff cf e1 fd ff cf e1 fd ff a3 c6 fd ff 47 8d fc ff 45 8d fc ff 79 ac fc ff 8a b6 fc ff 44 8c fc ff 44 8c fc ff 44 8c fc fe 44 8d fc f2 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc ff 43 8a fc f1 44 8b fc c1 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc ff 42 89 fc c1 42 89 fb 6d 42 88 fd fe 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc ff 41 88 fc fe 41 88 fc 6d 3f 88 fa 0c 40 80 ff dc 40 86 fc ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb ff 40 86 fb dc 40 86 fc 0c 40 80 ff 00 00 00 00 3b 3d 86 ff f0 3f 85 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb ff 3e 84 fb f0 3f 85 fb 3b 3d 86 fb 00 00 00 00 00 00 00 00 00 00 00 00 3c 3b 84 fb dc 3d 83 fc fe 3d 84 fb ff 3d 83 fb ff 3d 83 fb ff 3d 83 fb ff 3d 83 fb ff 3d 83 fb ff 3d 83 fb ff 3d 83 fb ff 3d 83 fb ff 3d 83 fb ff 3d 83 fb ff 3d 83 fb ff 3d 83 fb fe 3d 84 fb dc 3d 83 fc 3b 3d 82 fb 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 0c 40 80 ff 6d 3d 81 fa c1 3d 81 fb f1 3c 81 fb fe 3c 82 fb ff 3c 81 fb ff 3c 81 fb ff 3c 81 fb ff 3c 81 fb ff 3c 81 fb ff 3c 81 fb fe 3c 82 fb f1 3c 81 fb c1 3d 81 fb 6d 3d 81 fa 0c 2a 80 ff 00 00 00 00 00 00 00 00 00 00 00 00"

def handle_line(line, chatCommand, clearCommand):
    global blinkShouldBeOn, threadLock, cmdUp, cmdDown
    global thread
    if thread is None:
        thread = myBlinkThread()
        thread.start()
    cmdUp = chatCommand
    cmdDown = clearCommand
    if line.startswith("method call"):
        #print(line.rstrip())
        this.insidePixmap = False
        if line.endswith("path=/StatusNotifierItem; interface=org.freedesktop.DBus.Properties; member=Get\n"):
            # hier noch die serial holen
            m = this.serialRegEx.search(line)
            if m:
                this.mySerial = m.group()
                this.active = True
                #print(line.rstrip())
        else:
            this.active = False
    elif this.active:
        if line.startswith('   string "'):
            if line=='   string "IconPixmap"\n':
                this.waitForPixmap = True
                this.pixmapSerial = " reply_" + mySerial[1:] + "\n"
                this.active = False
        else:
            this.active = False
    
    if this.waitForPixmap:
        if line.startswith('method return '):
            if line.endswith(this.pixmapSerial):
                this.insidePixmap = True
                this.aktuellPixmap = ''
                this.inAktuellerPixmap = False
                this.waitForPixmap = False
    elif this.insidePixmap:
        if line[0]==' ':
            # aktuelle Pixmap erstellen
            if "int32 22" in line:
                this.inAktuellerPixmap = True
                this.aktuellPixmap = ''
            if inAktuellerPixmap:
                if line.startswith("               "):
                    this.aktuellPixmap = this.aktuellPixmap.strip() + ' ' + line.strip()
                elif line.endswith("]\n"):
                    if this.aktuellPixmap==this.pixmapA:
                        blinkShouldBeOn = False
                        threadLock.acquire(0)
                        threadLock.release()
                        print("   --> off")
                        #os.system('blink1-tool --off')
                    else:
                        blinkShouldBeOn = True
                        threadLock.acquire(0)
                        threadLock.release()
                        print("   --> ON")
                        #print(this.aktuellPixmap)
                        #os.system('blink1-tool --red --blink 2 ; blink1-tool --red')
                    this.inAktuellerPixmap = False
                    this.waitForPixmap = False
                    this.insidePixmap = False
        else:
            this.insidePixmap = False
