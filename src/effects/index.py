import cv2 as cv
import numpy as np

class Effect():
    def __init__(self):
        self.offsetX = 0
        self.offsetY = 0

    def move(self, x, y):
        self.offsetX = x
        self.offsetY = y
        # TODO: remove this shit

    def apply(self, frame: cv.typing.MatLike, points = np.array([[0, 0], [0, 100], [100, 0], [100, 100]], np.int32)) -> cv.typing.MatLike | None:
        # Positioning
        y1, x1 = np.argmin(points, axis=0)
        y2, x2 = np.argmax(points, axis=0)

        y1, x1 = points[y1][0], points[x1][1]
        y2, x2 = points[y2][0], points[x2][1]

        print(f"(x1, y1); (x2, y2) --> ({x1}, {y1}); ({x2}, {y2})")

        # TODO. remove this ASAP
        self.move(x1, y1)

        # w, h = x2 - x1, y2 - y1

        area = frame[y1:y2, x1:x2]

        render = self.draw(area)

        mask = np.zeros(frame.shape, np.int8)
        # pts = pts.reshape((-1,1,2))
        poly = cv.polylines(mask, [points], isClosed=True, color=255)

        poly = cv.bitwise_not(poly)
        poly = poly.astype(np.bool)
        
        mask[y1:y2, x1:x2] = area
        frame = cv.bitwise_and(frame, mask, mask=poly)

        #frame = cv.bitwise_xor(frame, poly)
        #render = cv.bitwise_and(render, poly)

        #frame = cv.add(frame, render)
        return frame

    def draw(self, frame: cv.typing.MatLike):
        print("Effect not defined! Skipped drawing!")
        return frame

class Gray(Effect):
    def draw(self, frame):
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        frame = cv.cvtColor(frame, cv.COLOR_GRAY2BGR)
        return frame