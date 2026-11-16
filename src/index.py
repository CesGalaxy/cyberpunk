import cam
import effects.index

c = cam.Video()

f = effects.index.Gray()
f.move(10, 10)

c.effects.append(f)

c.loop()