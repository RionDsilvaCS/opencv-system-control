import cv2
import mediapipe as mp


class handDetector():

    def __init__(self, mode=False, max_hands=2, detection_conf=0.5, track_conf=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_conf = detection_conf
        self.track_conf =track_conf

        self.mp_hands = mp.solutions.hands
        # self.hands = self.mp_hands.Hands(self.mode, self.max_hands, self.detection_conf, self.track_conf)
        self.hands = self.mp_hands.Hands(min_detection_confidence=self.detection_conf)
        self.mp_draw_skeleton = mp.solutions.drawing_utils


    def findHands(self, img, draw=True):
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb_img)
        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                
                if draw:
                    self.mp_draw_skeleton.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return img


    def handPosition(self, img, hand_num=0, draw=True):
        lm_list = []

        if self.results.multi_hand_landmarks:
            try:
                single_hand = self.results.multi_hand_landmarks[hand_num]
                for id, lm in enumerate(single_hand.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y* h)
                    lm_list.append([id, cx, cy])
                    if draw:
                        cv2.circle(img, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
            except(IndexError):
                pass
            
        return lm_list


def main():
    cam_width, cam_height = 640, 480

    cap = cv2.VideoCapture(0)
    detector = handDetector()
    cap.set(3, cam_width)
    cap.set(4, cam_height)

    while True:
        success, img = cap.read()
        
        img = detector.findHands(img)
        hand_list = detector.handPosition(img)
        if len(hand_list) != 0:
            print(hand_list[4])


        cv2.imshow("Img", img)
        cv2.waitKey(1)


if __name__=="__main__":
    main()