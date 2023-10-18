import cv2
import numpy as np
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc


class SystemMod():

    def __init__(self, vol_control_color = (255, 0, 255), bright_control_color = (255, 255, 0)):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = interface.QueryInterface(IAudioEndpointVolume)

        vol_range = self.volume.GetVolumeRange()

        self.min_vol = vol_range[0]
        self.max_vol = vol_range[1]

        self.vol_control_color = vol_control_color
        self.bright_control_color = bright_control_color


    def volControl(self, img, hand_pos, hand_pt_1=4, hand_pt_2=8):
        x1, y1 = hand_pos[hand_pt_1][1], hand_pos[hand_pt_1][2]
        x2, y2 = hand_pos[hand_pt_2][1], hand_pos[hand_pt_2][2]
        cx, cy = (x1+x2)//2 , (y1+y2)//2

        cv2.circle(img, (x1, y1), 8, self.vol_control_color, cv2.FILLED)
        cv2.circle(img, (x2, y2), 8, self.vol_control_color, cv2.FILLED)
        cv2.circle(img, (cx, cy), 8, self.vol_control_color, cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), self.vol_control_color, 3)

        length = math.hypot(x2-x1, y2-y1)

        vol = np.interp(length, [0, 150], [self.min_vol, self.max_vol])

        self.volume.SetMasterVolumeLevel(vol, None)

        return img


    def brightControl(self, img, hand_pos, hand_pt_1=4, hand_pt_2=8):
        x1, y1 = hand_pos[hand_pt_1][1], hand_pos[hand_pt_1][2]
        x2, y2 = hand_pos[hand_pt_2][1], hand_pos[hand_pt_2][2]
        cx, cy = (x1+x2)//2 , (y1+y2)//2

        cv2.circle(img, (x1, y1), 8, self.bright_control_color, cv2.FILLED)
        cv2.circle(img, (x2, y2), 8, self.bright_control_color, cv2.FILLED)
        cv2.circle(img, (cx, cy), 8, self.bright_control_color, cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), self.bright_control_color, 3)

        length = math.hypot(x2-x1, y2-y1)

        bright = np.interp(length, [0, 150], [0, 100])

        sbc.set_brightness(bright, display=0)

        return img
    
    