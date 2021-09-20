from pynput.keyboard import Key, Controller
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import socket
import numpy as np

keyboard = Controller()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
min_vol, max_vol, _ = volume.GetVolumeRange()

s = socket.socket()
port = 5050
maxConnections = 5
IP = socket.gethostname()

s.bind(('', port))

s.listen(maxConnections)
print("Server started at " + IP + " on port " + str(port))

clientsocket, address = s.accept()
print("Connection made")


def volume_up(n):
    for i in range(int(n / 2)):
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)


def volume_down(n):
    for i in range(int(n / 2)):
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)


running = True

while running:
    message = clientsocket.recv(1024).decode()

    try:
        percentage = int(message)

        # round percentage to nearest tenth place
        percentage = round(percentage / 10) * 10

        percentage = np.interp(percentage, [0, 100], [min_vol, max_vol])
        volume.SetMasterVolumeLevel(percentage, None)

    except:
        pass
