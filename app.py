import cv2
import HandTrackMod as htm
import SystemControlMod as scm

detector = htm.handDetector(detection_conf=0.7)
tracker = scm.SystemMod()
cam_width, cam_height = 640, 480

cap = cv2.VideoCapture(0)

cap.set(3, cam_width)
cap.set(4, cam_height)


while True:

    success, img = cap.read()

    img = detector.findHands(img, draw=False)
    hand_position_r = detector.handPosition(img, draw=False, hand_num=0)
    hand_position_l = detector.handPosition(img, draw=False, hand_num=1)

    if len(hand_position_r) != 0:
        img = tracker.volControl(img=img, hand_pos=hand_position_r)


    if len(hand_position_l) != 0:
        img = tracker.brightControl(img=img, hand_pos=hand_position_l)


    cv2.imshow("Img", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()