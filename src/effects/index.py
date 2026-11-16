from re import X

import cv2 as cv
import numpy as np

class Effect():
    def __init__(self):
        self.offsetX = 0
        self.offsetY = 0
        self.points = np.array([], np.int32)
        self.poly = np.zeros((0, 0), np.uint8)
        self.polynot = np.zeros((0, 0), np.uint8)
        self.mask = np.zeros((0, 0, 3), np.uint8)
        
        self.set_points([[1, 1], [1, 2], [2, 2], [2, 1]])

    def move(self, x, y):
        self.offsetX = x
        self.offsetY = y
        # TODO: remove this shit
    
    def set_points(self, points):
        self.points = np.array(points, np.int32)
        
        # Positioning
        x1, y1 = np.argmin(points, axis=0)
        x2, y2 = np.argmax(points, axis=0)

        x1, y1 = points[x1][0], points[y1][1]
        x2, y2 = points[x2][0], points[y2][1]

        # w, h = x2 - x1, y2 - y1
        # print(f"(x1, y1); (x2, y2) --> ({x1}, {y1}); ({x2}, {y2})")

        # TODO: remove this ASAP
        self.move(x1, y1)
        
        self.box = x1, y1, x2, y2
    
    def cache_size(self, frame: cv.typing.MatLike):
        if (self.poly.size != frame.size / 3) or (self.mask.size != frame.size):
            self.poly = np.zeros((frame.shape[0], frame.shape[1]), np.uint8)
            # pts = pts.reshape((-1,1,2))
            self.poly = cv.fillPoly(self.poly, [self.points], color=255)
            self.polynot = cv.bitwise_not(self.poly)
            self.mask = np.zeros(frame.shape, np.uint8)

    def apply(self, frame: cv.typing.MatLike) -> cv.typing.MatLike | None:
        x1, y1, x2, y2 = self.box
        
        self.cache_size(frame)
        
        # Apply the effect
        self.mask[y1:y2, x1:x2] = self.draw(frame[y1:y2, x1:x2])
        
        self.mask = cv.bitwise_and(self.mask, self.mask, mask=self.poly)
        frame = cv.bitwise_and(frame, frame, mask=self.polynot)

        #frame = cv.bitwise_xor(frame, poly)
        #render = cv.bitwise_and(render, poly)

        frame = cv.add(frame, self.mask)
        return frame

    def draw(self, frame: cv.typing.MatLike):
        print("Effect not defined! Skipped drawing!")
        return frame

class Green(Effect):
    def __init__(self):
        Effect.__init__(self)
        self.set_points([[100, 100], [80, 150], [120, 300], [200, 280], [250, 150]])
    
    def draw(self, frame):
        # frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # frame = cv.cvtColor(frame, cv.COLOR_GRAY2BGR)
        # frame = cv.subtract(frame, (255, 0, 255))
        frame = cv.multiply(frame, (0, 2, 0))
        return frame

class Pink(Effect):
    def __init__(self):
        Effect.__init__(self)
        self.set_points([[120, 300], [400, 280], [250, 150], [200, 280]])
    
    def draw(self, frame):
        frame = cv.multiply(frame, (2, 0, 2))
        return frame