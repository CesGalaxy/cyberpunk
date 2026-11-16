import cam
import effects.index

c = cam.Video()

f = effects.index.Green()

p = effects.index.Pink()

c.effects.append(f)
c.effects.append(p)

c.loop()