import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        # static_image_mode = False,
        # max_num_hands = 2,
        # min_detection_confidence = 0.5,
        # min_tracking_confidence = 0.5
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        img, handLms, self.mpHands.HAND_CONNECTIONS)

                # for id, lm in enumerate(handLms.landmark):
                #     # print(id, lm)
                #     h, w, c = img.shape
                #     cx, cy = int(lm.x*w), int(lm.y*h)
                #     print(id, cx, cy)
                #     if id == 4:
                #     cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return img


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 78), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("Image", img)
        key = cv2.waitKey(1)

        # segment for press q or Q to quit the app
        if key == 81 or key == 113:
            break


if __name__ == "__main__":
    main()
print('THIS IS YOUR HAND')
