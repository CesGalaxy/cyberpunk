from time import time

import cv2 as cv
import numpy as np

class Video:
    def __init__(self):
        self.cap = cv.VideoCapture(0)
        if not self.cap.isOpened():
            print("Cannot open camera!")
            exit()
        
        cv.namedWindow("frame")

        self.last_tick = time()
        self.fps = 0
        self.effects = []

    def frame(self) -> bool:
        # FPS
        now = time()
        dT = now - self.last_tick
        dFPS = 1 / dT
        self.fps = dFPS

        # Draw
        ret, frame = self.cap.read()

        if not ret:
            print("Can't receive frame (stram end?).")
            return False
        
        frame = cv.flip(frame, 1)
        
        ok, frame = self.draw(frame)

        if not ok:
            print("Cannot draw next frame.")
            return False

        cv.imshow('frame', frame)

        # Keys
        if cv.waitKey(1) == ord('q'):
            print("Quitting...")
            return False

        return True

    def draw(self, frame: cv.typing.MatLike) -> tuple[bool, cv.typing.MatLike]:
        for effect in self.effects:
            frame = effect.apply(frame)
        return True, frame

    def loop(self):
        while True:
            ok = self.frame()

            if not ok:
                print("==== NOT OK ====")
                break

        self.cap.release()
        cv.destroyAllWindows()